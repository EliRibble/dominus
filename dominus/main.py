import logging

import chryso.connection
import flask

import dominus.tables
import dominus.views

def setup_db():
    db = "postgres://dev:development@localhost:5432/dominus"
    engine = chryso.connection.Engine(db, dominus.tables)
    chryso.connection.store(engine)

def run():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    setup_db()

    app = flask.Flask('dominus')
    app.config.update(dict(
        FLASK_DEBUG = True,
        SECRET_KEY = 'development key',
    ))

    app.route('/')(dominus.views.root)
    app.route('/admin/')(dominus.views.admin)

    try:
        app.run(host='localhost', port=4554, debug=True)
    except KeyboardInterrupt:
        print("Shutting down...")
