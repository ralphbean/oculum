import flask
import hashlib
import charts

import sqlalchemy
import datanommer.models as m
m.init('postgres://datanommer:bunbunbun@localhost/datanommer')

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
    columns = 6
    n = rows * columns

    # TODO -- throw this away and return the 'top' n users.

    # TODO -- make this a classmethod in datanommer
    users = m.session.query(m.User)\
        .order_by(sqlalchemy.func.random())\
        .limit(n)\
        .all()

    gravatars = [
        (user.name, make_gravatar(user.name)) for user in users
    ]

    return flask.render_template(
        "index.html",
        gravatars=gravatars,
        rows=rows,
        columns=columns,
    )


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
