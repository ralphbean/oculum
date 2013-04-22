import flask
import hashlib
import os

import shelve
import charts

import sqlalchemy
import datanommer.models as m
m.init('postgres://datanommer:bunbunbun@localhost/datanommer')

here = os.path.abspath(os.path.dirname(__file__))
datadir = os.path.join(here, '..', 'data')
gravatar_dir = os.path.join(datadir, 'gravatars')
montage_dir = os.path.join(datadir, 'montage')

app = flask.Flask(__name__)

def make_gravatar(username):
    email = username + "@fedoraproject.org"
    digest = hashlib.md5(email).hexdigest()
    gravatar = "http://www.gravatar.com/avatar/%s" % digest
    gravatar += "?s=128"
    return gravatar


@app.route('/')
def index():
    rows = 5
    columns = 12
    n = rows * columns

    return flask.render_template('index.html')


@app.route('/<username>/')
def profile(username):
    return flask.render_template(
        "profile.html",
        username=username,
        gravatar=make_gravatar(username),
    )


@app.route('/<username>/radar/')
def radar(username):
    args = flask.request.args
    chart = charts.make_radar_chart(username, **args)
    return chart.render_response()


@app.route('/<username>/dots/')
def dots(username):
    args = flask.request.args
    chart = charts.make_dots_chart(username, **args)
    return chart.render_response()
