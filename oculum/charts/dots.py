import calendar
from datetime import (
    datetime,
    timedelta,
)

import pygal
import pygal.style

from sqlalchemy.orm.exc import NoResultFound
import datanommer.models as m
m.init('postgres://datanommer:blahah@localhost/datanommer')

title_template = 'Fedora Development Activity for %s@fedoraproject.org'


def message_count(user, start):
    end = start + timedelta(days=1)

    if not user:
        return 0

    return len([
        msg for msg in user.messages
        if msg.timestamp >= start and msg.timestamp < end
    ])


def make_chart(username, style='default', **args):
    if isinstance(style, list):
        style = style[0]
    style = pygal.style.styles[style]
    chart = pygal.Dot(
        x_label_rotation=90,
        style=style,
    )
    chart.title = title_template % username

    try:
        user = m.User.query.filter(m.User.name == username).one()
    except NoResultFound:
        user = None

    base = datetime.today()

    weekrange = list(reversed(range(52)))

    chart.x_labels = [
        "Week %02i %i" % (date.isocalendar()[1], date.isocalendar()[0])
        for date in (base - timedelta(weeks=i) for i in weekrange)
    ]

    for day in [6, 0, 1, 2, 3, 4, 5]:
        print "Building series for %s." % calendar.day_name[day]
        offset = timedelta(days=(base.weekday() - day) % 7)
        weeks = (base - offset - timedelta(weeks=i) for i in weekrange)
        chart.add(
            calendar.day_name[day],
            [message_count(user, date) for date in weeks]
        )

    return chart
