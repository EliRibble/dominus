import logging
import collections
import sqlalchemy
import chryso.connection
import dominus.tables

LOGGER = logging.getLogger(__name__)

Set = collections.namedtuple('Set', ('name', 'uuid'))
Card = collections.namedtuple('Card', ('name', 'type', 'set', 'uuid'))
Kingdom = collections.namedtuple('Kingdom', ('name', 'creator', 'cards', 'uuid'))

def create_card(set_, name, type_):
    engine = chryso.connection.get()
    query = dominus.tables.Card.insert().values(
        name=name,
        set=set_['uuid'],
        text='',
        type=type_,
    )
    engine.execute(query)
    LOGGER.debug("Created %s in %s", card, set_['name'])

def create_kingdom(name, creator, cards):
    engine = chryso.connection.get()
    with engine.atomic():
        all_cards = get_cards()
        cards_by_name = {card.name: card for card in all_cards}
        query = dominus.tables.Kingdom.insert().values(name=name, creator=creator)
        uuid = engine.execute(query).inserted_primary_key[0]
        LOGGER.debug("Created kingdom %s (%s) by %s", name, uuid, creator)
        query = dominus.tables.KingdomCard.insert().values([{
            'card'      : cards_by_name[card].uuid,
            'kingdom'   : uuid,
        } for card in cards])
        engine.execute(query)
        LOGGER.debug("Added cards %s to kingdom %s", cards, uuid)

def create_set(name):
    engine = chryso.connection.get()
    query = dominus.tables.Set.insert().values(name=name)
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

    query = sqlalchemy.select([dominus.tables.Card])

    rows = engine.execute(query).fetchall()
    return [Card(
        name = row[dominus.tables.Card.c.name],
        set  = row[dominus.tables.Card.c.set],
        type = row[dominus.tables.Card.c.type],
        uuid = row[dominus.tables.Card.c.uuid],
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
    query = sqlalchemy.select([dominus.tables.Kingdom])
    rows = engine.execute(query).fetchall()
    kingdoms = [Kingdom(
        cards   = cards_by_kingdom_uuid[row[dominus.tables.Kingdom.c.uuid]],
        creator = row[dominus.tables.Kingdom.c.creator],
        name    = row[dominus.tables.Kingdom.c.name],
        uuid    = row[dominus.tables.Kingdom.c.uuid],
    ) for row in rows]
    return kingdoms
