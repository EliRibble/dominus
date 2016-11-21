import logging

import chryso.errors
import flask
import flask_login

import dominus.platform

LOGGER = logging.getLogger(__name__)

blueprint = flask.Blueprint('auth', __name__)

@blueprint.route('/login/', methods=['GET'])
def get_login():
    return flask.render_template('login.html')

@blueprint.route('/login/', methods=['POST'])
def create_login():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    LOGGER.debug("Checking credentials for %s %s", username, password)
    record = dominus.platform.user_by_credentials(username, password)
    LOGGER.debug("Resulting user: %s", record)
    if not record:
        return flask.make_response('Your username or password is incorrect', 403)
    user = User(record['username'], record['uuid'])
    flask_login.login_user(user)
    return flask.redirect('/')

@blueprint.route('/login/', methods=['DELETE'])
def delete_login():
    flask_login.logout_user()
    return flask.redirect('/login/')

@blueprint.route('/register/', methods=['GET'])
def get_register():
    error = {
        'already-exists'    : 'That username already exists',
    }.get(flask.request.args.get('error'))
    return flask.render_template('register.html', error=error)

@blueprint.route('/register/', methods=['POST'])
def do_register():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    try:
        dominus.platform.create_user(username, password)
    except chryso.errors.DuplicateKeyError:
        return flask.redirect('/register/?error=already-exists')
    record = dominus.platform.user_by_credentials(username, password)
    user = User(record['username'], record['uuid'])
    flask_login.login_user(user)
    return flask.redirect('/')

class User():
    def __init__(self, username, uuid):
        self.username   = username
        self.uuid       = uuid

    def is_active(self): # pylint: disable=no-self-use
        return True

    def get_id(self):
        return self.uuid

    def is_authenticated(self): # pylint: disable=no-self-use
        return True

    def is_anonymous(self): # pylint: disable=no-self-use
        return False

def load_user(user_id):
    return dominus.platform.user_by_uuid(user_id)
