import flask
import hashlib
import charts

app = flask.Flask(__name__)


@app.route('/<username>/')
def profile(username):
    email = username + "@fedoraproject.org"
    digest = hashlib.md5(email).hexdigest()
    gravatar = "http://www.gravatar.com/avatar/%s" % digest
    return flask.render_template(
        "profile.html",
        username=username,
        gravatar=gravatar,
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
