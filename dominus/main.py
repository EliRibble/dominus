import logging

import chryso.connection
import flask
import flask_login

import dominus.auth
import dominus.config
import dominus.tables
import dominus.views

def setup_db(db):
    engine = chryso.connection.Engine(db, dominus.tables)
    chryso.connection.store(engine)

def create_application():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)


    app = flask.Flask('dominus')

    config = dominus.config.get()
    setup_db(config['db'])

    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(dominus.auth.load_user)

    app.config.update(dict(
        FLASK_DEBUG = True,
        SECRET_KEY = 'development key',
    ))

    app.register_blueprint(dominus.auth.blueprint)
    app.register_blueprint(dominus.views.blueprint)
    app.before_request(dominus.auth.require_login)
    return app

def run():
    app = create_application()
    try:
        app.run(host='localhost', port=4554, debug=True)
    except KeyboardInterrupt:
        print("Shutting down...")
