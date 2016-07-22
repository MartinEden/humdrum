import datetime
import flask
import os

from repositories import TotalStatus

app = flask.Flask(__name__)
app.config['DEBUG'] = True

width = 1000


def get_days():
    today = datetime.date.today()
    day = today - datetime.timedelta(days=6)
    days = []
    x = 0
    column_width = width / 7
    while day <= today:
        days.append({
            "name": day.strftime('%A'),
            "x": x,
            "centre_x": x + column_width / 2,
            "value": day.isoformat(),
        })
        x += column_width
        day += datetime.timedelta(days=1)
    return days


@app.route('/status')
def status():
    data = {
        'status': TotalStatus.load_from_disk(),
        'days': get_days(),
        'width': width
    }
    return flask.json.jsonify(data)


@app.route('/')
def index():
    return flask.render_template('status.html', days=get_days(), width=width)

app.run()
