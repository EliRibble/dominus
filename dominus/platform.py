import collections
import sqlalchemy
import chryso.connection
import dominus.tables

Card = collections.namedtuple('Card', ('name', 'type'))

def create_card(set_, card):
    engine = chryso.connection.get()
    query = dominus.tables.Card.insert().values(
        name=card.name,
        set=set_['uuid'],
        text='',
        type=card.type,
    )
    engine.execute(query)

def create_set(name):
    engine = chryso.connection.get()
    query = dominus.tables.Set.insert().values(name=name)
    engine.execute(query)

def get_sets():
    engine = chryso.connection.get()

    query = sqlalchemy.select([dominus.tables.Set])

    rows = engine.execute(query).fetchall()
    return [dict(row) for row in rows]

def get_cards():
    engine = chryso.connection.get()

    query = sqlalchemy.select([dominus.tables.Card])

    rows = engine.execute(query).fetchall()
    return [dict(row) for row in rows]

