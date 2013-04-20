import pygal
import pygal.style

import fedmsg.config
import fedmsg.meta

from sqlalchemy.orm.exc import NoResultFound
import datanommer.models as m
m.init('postgres://datanommer:bunbunbun@localhost/datanommer')

title_template = 'Fedora Development Activity for %s@fedoraproject.org'

import math


def message_count(user, category):
    return math.log(len([
        msg for msg in user.messages
        if msg.category == category
    ]) + 1)


def add_to_chart(chart, username):
    try:
        user = m.User.query.filter(m.User.name == username).one()
    except NoResultFound:
        user = None

    config = fedmsg.config.load_config()
    fedmsg.meta.make_processors(**config)
    categories = [p.__name__.lower() for p in fedmsg.meta.processors]

    excluded = ['logger', 'announce', 'compose', 'unhandled']
    for item in excluded:
        categories.remove(item)

    data = [message_count(user, category) for category in categories]
    chart.x_labels = categories

    # Remove 'zero' valued categories.
    #chart.x_labels = [c for i, c in enumerate(categories) if data[i]]
    #data = [item for item in data if item]

    chart.add(username, data)

    return chart


def make_chart(username, style='default', **args):
    if isinstance(style, list):
        style = style[0]
    style = pygal.style.styles[style]
    chart = pygal.Radar(style=style)
    chart = add_to_chart(chart, username)
    return chart
