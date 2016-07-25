import datetime
from dateutil import parser
import requests

from secrets import github_access_token
from utc import utc


def get_repos(org):
    uri = "https://api.github.com/orgs/%s/repos?access_token=%s" % (org, github_access_token)
    now = datetime.datetime.now(utc)
    limit = now - datetime.timedelta(days=7)

    while uri:
        r = requests.get(uri)
        for repo in r.json():
            last_updated = parser.parse(repo['pushed_at'])
            if last_updated >= limit:
                yield repo['ssh_url']  

        if 'next' in r.links:
            uri = r.links['next']['url']
        else:
            uri = None

if __name__ == "__main__":
    for repo in get_repos('lshift'):
        print repo