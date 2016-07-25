import datetime
from dateutil import parser
import requests

from secrets import bitbucket_credentials
from utc import utc


def get_repos(team_name):
    uri = 'http://api.bitbucket.org/2.0/repositories/' + team_name
    now = datetime.datetime.now(utc)
    limit = now - datetime.timedelta(days=7)

    while uri:
        r = requests.get(uri, auth=bitbucket_credentials)
        data = r.json()
        for repo in data['values']:
            last_updated = parser.parse(repo['updated_on'])
            # print repo['name'], ':', last_updated
            if last_updated >= limit:
                for handle in repo['links']['clone']:
                    if handle['name'] == 'ssh':
                        yield handle['href']

        if 'next' in data:
            uri = data['next']
        else:
            uri = None

if __name__ == "__main__":
    for repo in get_repos('lshift'):
        print repo