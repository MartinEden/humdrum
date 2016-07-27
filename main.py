import datetime
import flask

from repositories import TotalStatus
from settings import settings

app = flask.Flask(__name__)
app.config['DEBUG'] = True

width = 1250
leftMargin = 250
laneHeight = 100


def get_days():
    today = datetime.date.today()
    day = today - datetime.timedelta(days=6)
    days = []
    x = 0
    column_width = (width - leftMargin) / 7
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


@app.route('/json')
def json():
    data = {
        'settings': settings.data,
        'status': TotalStatus.load_from_disk(),
        'days': get_days(),
        'width': width,
        'laneHeight': laneHeight,
    }
    return flask.json.jsonify(data)


@app.route('/')
def index():
    return flask.render_template('status.html', days=get_days(), width=width)#


@app.route('/settings/repo/remove', methods=['POST'])
def settings_repo_remove():
    repo = flask.request.form['repo']
    if repo:
        settings.remove_repo(repo)
        settings.save()
        return "Yes"
    return "No", 500


@app.route('/settings/repo/add', methods=['POST'])
def settings_repo_add():
    repo = flask.request.form['repo']
    if repo:
        settings.add_repo(repo)
        settings.save()
        return "Yes"
    return "No", 500

app.run()
