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
Kingdom = collections.namedtuple('Kingdom', ('name', 'creator', 'cards', 'uuid'))

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
        query = dominus.tables.KingdomCard.insert().values([{ # pylint: disable=no-value-for-parameter
            'card'      : cards_by_name[card].uuid,
            'kingdom'   : _uuid,
        } for card in cards])
        engine.execute(query)
        LOGGER.debug("Added cards %s to kingdom %s", cards, _uuid)

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

def get_cards():
    engine = chryso.connection.get()

    query = sqlalchemy.select([dominus.tables.CardType])
    rows = engine.execute(query).fetchall()
    types_by_uuid = collections.defaultdict(list)
    for row in rows:
        types_by_uuid[row[dominus.tables.CardType.c.card]].append(row[dominus.tables.CardType.c.name])

    query = sqlalchemy.select([dominus.tables.Card])

    rows = engine.execute(query).fetchall()
    return [Card(
        cost_in_debt     = row[dominus.tables.Card.c.cost_in_debt],
        cost_in_treasure = row[dominus.tables.Card.c.cost_in_treasure],
        is_in_supply     = row[dominus.tables.Card.c.is_in_supply],
        name             = row[dominus.tables.Card.c.name],
        set              = row[dominus.tables.Card.c.set],
        text             = row[dominus.tables.Card.c.text],
        types            = set(types_by_uuid[row[dominus.tables.Card.c.uuid]]),
        uuid             = row[dominus.tables.Card.c.uuid],
    ) for row in rows]

def get_kingdoms():
    engine = chryso.connection.get()

    cards = get_cards()
    cards_by_uuid = {card.uuid: card for card in cards}
    query = sqlalchemy.select([dominus.tables.KingdomCard])
    rows = engine.execute(query).fetchall()
    cards_by_kingdom_uuid = collections.defaultdict(list)
    for row in rows:
        kingdom = row[dominus.tables.KingdomCard.c.kingdom]
        card_uuid = row[dominus.tables.KingdomCard.c.card]
        card = cards_by_uuid[card_uuid]
        cards_by_kingdom_uuid[kingdom].append(card)
    query = sqlalchemy.select([dominus.tables.Kingdom]).where(dominus.tables.Kingdom.c.deleted == None) # pylint: disable=singleton-comparison
    rows = engine.execute(query).fetchall()
    kingdoms = [Kingdom(
        cards   = cards_by_kingdom_uuid[row[dominus.tables.Kingdom.c.uuid]],
        creator = row[dominus.tables.Kingdom.c.creator],
        name    = row[dominus.tables.Kingdom.c.name],
        uuid    = row[dominus.tables.Kingdom.c.uuid],
    ) for row in rows]
    return kingdoms

def delete_kingdom(_uuid):
    engine = chryso.connection.get()
    query = dominus.tables.Kingdom.update().values(deleted=datetime.datetime.utcnow()).where(dominus.tables.Kingdom.c.uuid == _uuid) # pylint: disable=no-value-for-parameter
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
