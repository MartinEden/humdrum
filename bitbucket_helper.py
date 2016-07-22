import requests
import urllib3

urllib3.disable_warnings()


def get_repos(team_name):
    uri = 'http://api.bitbucket.org/2.0/repositories/' + team_name
    while uri:
        r = requests.get(uri)
        data = r.json()
        for repo in data['values']:
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