import logging

import chryso.connection
import flask

import dominus.tables
import dominus.views


def run():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    app = flask.Flask('dominus')
    app.config.update(dict(
        FLASK_DEBUG = True,
        SECRET_KEY = 'development key',
    ))
    db = "postgres://dev:development@localhost:5432/dominus"
    engine = chryso.connection.Engine(db, dominus.tables)
    chryso.connection.store(engine)

    app.route('/')(dominus.views.root)

    try:
        app.run('localhost', '4554')
    except KeyboardInterrupt:
        print("Shutting down...")
