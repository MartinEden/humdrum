from bs4 import BeautifulSoup
import requests


def get_repos(uri):
    r = requests.get(uri)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.table
    for row in table.find_all('tr')[1:]:
        column = row.find_all('td')[0]
        yield "%s%s" % (uri, column.a['href'])

if __name__ == "__main__":
    for repo in get_repos("http://hg.lshift.net"):
        print repo
