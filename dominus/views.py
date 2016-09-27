import flask

def root():
    return flask.render_template('root.html')
