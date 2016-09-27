import chryso.connection
import flask

import dominus.tables


def run():
    app = flask.Flask('dominus')

    db = "postgres://dev:development@localhost:5432/dominus"
    engine = chryso.connection.Engine(db, dominus.tables)
    chryso.connection.store(engine)

    print(engine.execute('select version()').fetchall())
