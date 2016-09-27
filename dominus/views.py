import flask
import dominus.platform

def root():
    return flask.render_template('root.html')

def admin():
    sets = sorted(dominus.platform.get_sets(), key=lambda x: x['name'])
    return flask.render_template('admin.html', sets=sets)

