import collections
import functools
import json
import logging

import flask

import dominus.platform

LOGGER = logging.getLogger(__name__)

blueprint = flask.Blueprint('views', __name__)

def parse(args):
    def _decorate(request_handler):
        @functools.wraps(request_handler)
        def _parse(**kwargs):
            values = {}
            missing_parameters = []
            for key, converter in args.items():
                supplied = flask.request.form.get(key)
                if supplied is None:
                    missing_parameters.append(key)
                else:
                    values[key] = converter(supplied) if converter else supplied
            if missing_parameters:
                return (json.dumps({'errors': [{
                    'title' : "Missing required paramter '{}'".format(parameter),
                    'code'  : "missing-required-paramter",
                } for parameter in missing_parameters]}), 400, {})
            kwargs['arguments'] = values
            return request_handler(**kwargs)
        return _parse
    return _decorate

@blueprint.route('/', methods=['GET'])
def root():
    return flask.render_template('root.html')

@blueprint.route('/admin/', methods=['GET'])
def admin():
    sets = dominus.platform.get_sets()
    sets_by_uuid = {set_.uuid: set_ for set_ in sets}
    cards = dominus.platform.get_cards()
    cards_by_set = collections.defaultdict(list)
    for card in cards:
        set_ = sets_by_uuid[card.set]
        cards_by_set[set_.name].append(card)
    return flask.render_template('admin.html', cards_by_set=cards_by_set)

@blueprint.route('/kingdoms/', methods=['GET'])
def kingdoms():
    _kingdoms = dominus.platform.get_kingdoms(flask.session['user_id'])
    return flask.render_template('kingdoms.html', kingdoms=_kingdoms)

@blueprint.route('/kingdoms/add/', methods=['GET'])
def add_kingdom_get():
    cards = dominus.platform.get_cards()
    return flask.render_template('add_kingdom.html', cards=cards)

@blueprint.route('/kingdoms/add/', methods=['POST'])
@parse({
    'name'      : str,
})
def add_kingdom_post(arguments):
    LOGGER.debug("Got POST %s", arguments)
    cards = []
    for key, value in flask.request.form.items():
        if key in ['name', 'creator']:
            continue
        cards.append(value)
    cards = [card for card in cards if card]
    dominus.platform.create_kingdom(arguments['name'], flask.session['user_id'], cards)
    return flask.redirect('/kingdoms/')

@blueprint.route('/kingdom/<uuid:kingdom_id>/delete/', methods=['POST'])
def kingdom_delete(kingdom_id):
    dominus.platform.delete_kingdom(flask.session['user_id'], kingdom_id)
    return flask.redirect('/kingdoms/')

@blueprint.route('/kingdom/<uuid:kingdom_id>/', methods=['GET'])
def kingdom_get(kingdom_id):
    kingdom = dominus.platform.get_kingdoms(flask.session['user_id'], [kingdom_id])[0]
    return flask.render_template('kingdom.html', kingdom=kingdom)

@blueprint.route('/kingdom/<uuid:kingdom_id>/play-log/', methods=['POST'])
@parse({
    'comments'      : str,
    'player_count'  : int,
    'rating'        : int,
})
def kingdom_play_log_post(kingdom_id, arguments):
    dominus.platform.create_kingdom_play_log(flask.session['user_id'], kingdom_id, arguments)
    return flask.redirect('/kingdom/{}/'.format(kingdom_id))

@blueprint.route('/kingdom/<uuid:kingdom_id>/rating/', methods=['POST'])
@parse({'rating': int})
def kingdom_rating_post(kingdom_id, arguments):
    dominus.platform.create_kingdom_rating(flask.session['user_id'], kingdom_id, arguments['rating'])
    return flask.redirect('/kingdom/{}/'.format(kingdom_id))
