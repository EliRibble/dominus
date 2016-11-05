import collections
import datetime
import logging
import uuid

import chryso.connection
import sqlalchemy
import werkzeug.security

import dominus.tables

LOGGER = logging.getLogger(__name__)

Set = collections.namedtuple('Set', ('name', 'uuid'))
Card = collections.namedtuple('Card', (
    'cost_in_debt',
    'cost_in_treasure',
    'is_in_supply',
    'name',
    'set',
    'types',
    'text',
    'uuid',
))
class Kingdom(): # pylint: disable=too-many-instance-attributes
    def __init__(self, name, created, creator, cards, _uuid):
        self.cards          = cards
        self.created        = created
        self.creator        = creator
        self.name           = name
        self.play_logs      = None
        self.rating_average = None
        self.rating_mine    = None
        self.uuid           = _uuid

    @property
    def sets(self):
        return {card.set for card in self.cards}

    def card_types(self):
        types = set()
        for card in self.cards:
            for type_ in card.types:
                types.add(type_)
        return types

    def cards_by_cost_in_treasure(self):
        results = collections.defaultdict(list)
        for card in self.cards:
            results[card.cost_in_treasure].append(card)
        return results

    def cards_by_cost_in_debt(self):
        results = collections.defaultdict(list)
        for card in self.cards:
            results[card.cost_in_debt].append(card)
        return results

def create_card(set_, name, cardtypes, cost_in_treasure, cost_in_debt, is_in_supply):
    engine = chryso.connection.get()
    query = dominus.tables.Card.insert().values( # pylint: disable=no-value-for-parameter
        cost_in_debt        = cost_in_debt,
        cost_in_treasure    = cost_in_treasure,
        is_in_supply        = is_in_supply,
        name                = name,
        set                 = set_.uuid,
        text                = '',
    )
    results = engine.execute(query)
    _uuid = results.inserted_primary_key[0]
    query = dominus.tables.CardType.insert().values([dict( # pylint: disable=no-value-for-parameter
        card=_uuid,
        name=cardtype,
    ) for cardtype in cardtypes])
    engine.execute(query)
    LOGGER.debug("Created %s in %s with types %s", name, set_.name, cardtypes)

def create_kingdom(name, creator, cards):
    engine = chryso.connection.get()
    with engine.atomic():
        all_cards = get_cards()
        cards_by_name = {card.name: card for card in all_cards}
        query = dominus.tables.Kingdom.insert().values(name=name, creator=creator) # pylint: disable=no-value-for-parameter
        _uuid = engine.execute(query).inserted_primary_key[0]
        LOGGER.debug("Created kingdom %s (%s) by %s", name, _uuid, creator)
        if not cards:
            return _uuid
        query = dominus.tables.KingdomCard.insert().values([{ # pylint: disable=no-value-for-parameter
            'card'      : cards_by_name[card].uuid,
            'kingdom'   : _uuid,
        } for card in cards])
        engine.execute(query)
        LOGGER.debug("Added cards %s to kingdom %s", cards, _uuid)
        return _uuid

def create_kingdom_play_log(user, kingdom_uuid, arguments):
    engine = chryso.connection.get()
    query = dominus.tables.KingdomPlay.insert().values( # pylint: disable=no-value-for-parameter
        creator         = user,
        kingdom         = kingdom_uuid,
        comments        = arguments['comments'],
        rating          = arguments['rating'],
        player_count    = arguments['player_count'],
    )
    _uuid = engine.execute(query).inserted_primary_key[0]
    LOGGER.debug("Created a play log on %s of %s for user %s with uuid %s", kingdom_uuid, arguments, user, _uuid)
    return _uuid

def create_kingdom_rating(user, kingdom_uuid, rating):
    engine = chryso.connection.get()
    try:
        with engine.atomic():
            query = dominus.tables.KingdomRating.insert().values( # pylint: disable=no-value-for-parameter
                creator = user,
                kingdom = kingdom_uuid,
                rating  = rating,
            )
            _uuid = engine.execute(query).inserted_primary_key[0]
            LOGGER.debug("Created a rating on %s of %s for user %s", kingdom_uuid, rating, user)
            return _uuid
    except chryso.errors.DuplicateKeyError:
        query = (dominus.tables.KingdomRating.update().values(rating=rating) # pylint: disable=no-value-for-parameter
            .where(dominus.tables.KingdomRating.c.creator == user)
            .where(dominus.tables.KingdomRating.c.kingdom == kingdom_uuid)
        )
        engine.execute(query)
        LOGGER.debug("Updated rating on %s of %s for user %s", kingdom_uuid, rating, user)

def create_set(name):
    engine = chryso.connection.get()
    query = dominus.tables.Set.insert().values(name=name) # pylint: disable=no-value-for-parameter
    engine.execute(query)
    LOGGER.debug("Created set %s", name)

def get_sets():
    engine = chryso.connection.get()

    query = sqlalchemy.select([dominus.tables.Set])

    rows = engine.execute(query).fetchall()
    return [Set(
        name=row[dominus.tables.Set.c.name],
        uuid=row[dominus.tables.Set.c.uuid],
    ) for row in rows]

def get_cards(card_uuids=None):
    engine = chryso.connection.get()

    query = sqlalchemy.select([dominus.tables.CardType])
    rows = engine.execute(query).fetchall()
    types_by_uuid = collections.defaultdict(list)
    for row in rows:
        types_by_uuid[row[dominus.tables.CardType.c.card]].append(row[dominus.tables.CardType.c.name])

    query = sqlalchemy.select([
        dominus.tables.Card,
        dominus.tables.Set.c.name,
    ], use_labels=True).select_from(
        dominus.tables.Card.join(dominus.tables.Set)
    )
    if card_uuids:
        query = query.where(dominus.tables.Card.c.uuid.in_(card_uuids))

    rows = engine.execute(query).fetchall()
    return [Card(
        cost_in_debt     = row[dominus.tables.Card.c.cost_in_debt],
        cost_in_treasure = row[dominus.tables.Card.c.cost_in_treasure],
        is_in_supply     = row[dominus.tables.Card.c.is_in_supply],
        name             = row[dominus.tables.Card.c.name],
        set              = row[dominus.tables.Set.c.name],
        text             = row[dominus.tables.Card.c.text],
        types            = set(types_by_uuid[row[dominus.tables.Card.c.uuid]]),
        uuid             = row[dominus.tables.Card.c.uuid],
    ) for row in rows]

def _add_cards_to_kingdoms(kingdom_by_uuid):
    engine = chryso.connection.get()
    query = (sqlalchemy.select([dominus.tables.KingdomCard])
        .where(dominus.tables.KingdomCard.c.kingdom.in_(kingdom_by_uuid.keys())))
    rows = engine.execute(query).fetchall()
    card_uuids = {row[dominus.tables.KingdomCard.c.card] for row in rows}
    cards = get_cards(card_uuids)
    cards_by_uuid = {card.uuid: card for card in cards}
    for row in rows:
        kingdom_uuid = row[dominus.tables.KingdomCard.c.kingdom]
        card_uuid = row[dominus.tables.KingdomCard.c.card]
        kingdom = kingdom_by_uuid[kingdom_uuid]
        card = cards_by_uuid[card_uuid]
        kingdom.cards.append(card)

def _add_ratings_to_kingdoms(user, kingdom_by_uuid):
    _add_my_ratings_to_kingdoms(user, kingdom_by_uuid)
    _add_average_ratings_to_kingdoms(kingdom_by_uuid)

def _add_my_ratings_to_kingdoms(user, kingdom_by_uuid):
    engine = chryso.connection.get()
    query = (sqlalchemy.select([dominus.tables.KingdomRating])
        .where(dominus.tables.KingdomRating.c.kingdom.in_(kingdom_by_uuid.keys()))
        .where(dominus.tables.KingdomRating.c.creator == user)
    )

    rows = engine.execute(query).fetchall()
    for row in rows:
        kingdom = row[dominus.tables.KingdomRating.c.kingdom]
        rating = row[dominus.tables.KingdomRating.c.rating]
        kingdom_by_uuid[kingdom].rating_mine = rating

def _add_average_ratings_to_kingdoms(kingdom_by_uuid):
    engine = chryso.connection.get()
    average = sqlalchemy.func.avg(dominus.tables.KingdomRating.c.rating)
    query = (sqlalchemy.select([
            dominus.tables.KingdomRating.c.kingdom,
            average,
        ]).group_by(dominus.tables.KingdomRating.c.kingdom)
        .where(dominus.tables.KingdomRating.c.kingdom.in_(kingdom_by_uuid.keys()))
    )
    rows = engine.execute(query).fetchall()
    for row in rows:
        kingdom = kingdom_by_uuid[row[dominus.tables.KingdomRating.c.kingdom]]
        kingdom.rating_average = round(row[average], 2)

def _add_play_logs_to_kingdoms(kingdom_by_uuid):
    engine = chryso.connection.get()
    query = (sqlalchemy.select([
            dominus.tables.KingdomPlay,
            dominus.tables.User.c.username,
        ]).select_from(
            dominus.tables.KingdomPlay.join(dominus.tables.User)
        )
        .where(dominus.tables.KingdomPlay.c.kingdom.in_(kingdom_by_uuid.keys()))
        .order_by(dominus.tables.KingdomPlay.c.created)
    )
    rows = engine.execute(query).fetchall()
    for kingdom in kingdom_by_uuid.values():
        kingdom.play_logs = []
    for row in rows:
        kingdom = kingdom_by_uuid[row[dominus.tables.KingdomPlay.c.kingdom]]
        kingdom.play_logs.append({
            'comments'   : row[dominus.tables.KingdomPlay.c.comments],
            'created'   : row[dominus.tables.KingdomPlay.c.created],
            'creator'   : row[dominus.tables.User.c.username],
            'player_count'   : row[dominus.tables.KingdomPlay.c.player_count],
            'rating'   : row[dominus.tables.KingdomPlay.c.rating],
        })

def get_kingdoms(user, kingdom_uuids=None, include_play_logs=True):
    engine = chryso.connection.get()

    query = (sqlalchemy.select([
        dominus.tables.Kingdom.c.created,
        dominus.tables.Kingdom.c.name,
        dominus.tables.Kingdom.c.uuid,
        dominus.tables.User.c.username,
    ]).select_from(
        dominus.tables.Kingdom.join(dominus.tables.User)
    ).where(dominus.tables.Kingdom.c.deleted == None)) # pylint: disable=singleton-comparison
    if kingdom_uuids:
        query = query.where(dominus.tables.Kingdom.c.uuid.in_(kingdom_uuids))
    rows = engine.execute(query).fetchall()
    kingdoms = [Kingdom(
        cards   = [],
        created = row[dominus.tables.Kingdom.c.created],
        creator = row[dominus.tables.User.c.username],
        name    = row[dominus.tables.Kingdom.c.name],
        _uuid   = row[dominus.tables.Kingdom.c.uuid],
    ) for row in rows]
    kingdom_by_uuid = {kingdom.uuid: kingdom for kingdom in kingdoms}
    _add_cards_to_kingdoms(kingdom_by_uuid)
    _add_ratings_to_kingdoms(user, kingdom_by_uuid)
    if include_play_logs:
        _add_play_logs_to_kingdoms(kingdom_by_uuid)
    return kingdoms

def delete_kingdom(user, _uuid):
    engine = chryso.connection.get()
    query = (dominus.tables.Kingdom.update() # pylint: disable=no-value-for-parameter
    .values(
        deleted=datetime.datetime.utcnow()
    ).where(dominus.tables.Kingdom.c.uuid == _uuid)
    .where(dominus.tables.Kingdom.c.creator == user))
    engine.execute(query)
    LOGGER.debug("Deleted kingdom %s", _uuid)

def create_user(username, password):
    engine = chryso.connection.get()

    _uuid = uuid.uuid4()
    statement = dominus.tables.User.insert().values( #pylint: disable=no-value-for-parameter
        password_hash   = werkzeug.security.generate_password_hash(password),
        username        = username,
        uuid            = _uuid,
    )
    engine.execute(statement)

    return _uuid

def user_by_credentials(username, password):
    engine = chryso.connection.get()

    query = dominus.tables.User.select().where(dominus.tables.User.c.username == username)
    result = engine.execute(query).first()
    if not result:
        return None

    password_hash = result[dominus.tables.User.c.password_hash]
    if not werkzeug.security.check_password_hash(password_hash, password):
        return None

    return dict(result)

def user_by_uuid(_uuid):
    engine = chryso.connection.get()

    query = dominus.tables.User.select().where(dominus.tables.User.c.uuid == _uuid)
    result = engine.execute(query).first()
    return dict(result) if result else None
