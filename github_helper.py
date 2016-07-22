import requests
from secrets import github_access_token


def get_repos(org):
    uri = "https://api.github.com/orgs/%s/repos?access_token=%s" % (org, github_access_token)
    while uri:
        r = requests.get(uri)
        for repo in r.json():
            yield repo['ssh_url']

        if 'next' in r.links:
            uri = r.links['next']['url']
        else:
            uri = None

if __name__ == "__main__":
    for repo in get_repos('lshift'):
        print repo