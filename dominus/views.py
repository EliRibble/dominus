import collections
import flask
import functools
import json
import dominus.platform
import logging

LOGGER = logging.getLogger(__name__)

blueprint = flask.Blueprint('views', __name__)

def parse(args):
    def _decorate(request_handler):
        @functools.wraps(request_handler)
        def _parse():
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
            return request_handler(values)
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
    kingdoms = dominus.platform.get_kingdoms()
    return flask.render_template('kingdoms.html', kingdoms=kingdoms)

@blueprint.route('/kingdom/add/', methods=['GET'])
def add_kingdom_get():
    cards = dominus.platform.get_cards()
    return flask.render_template('add_kingdom.html', cards=cards)

@blueprint.route('/kingdom/add/', methods=['POST'])
@parse({
    'name'      : str,
    'creator'   : str,
})
def add_kingdom_post(arguments):
    LOGGER.debug("Got POST %s", arguments)
    cards = []
    for key, value in flask.request.form.items():
        if not key.startswith('card'):
            continue
        cards.append(value)
    cards = [card for card in cards if card]
    dominus.platform.create_kingdom(arguments['name'], arguments['creator'], cards)
    return flask.redirect('/kingdoms/')

