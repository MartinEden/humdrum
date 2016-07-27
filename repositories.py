import datetime
import json
import os

import bitbucket_helper
import github_helper
import mercurial_server

from commit import Commit
import git_helper
import hg_helper
from settings import settings


class RepositoryStatus(object):
    def __init__(self, uri, name, filename,commits):
        self.uri = uri
        self.name = name
        self.filename = filename
        self.commits = sorted(commits, key=lambda x: x.timestamp, reverse=True)

    @property
    def latest(self):
        if self.commits:
            return self.commits[0]
        return None

    @property
    def count(self):
        return len(self.commits)

    def as_dict(self):
        d = {
            'uri': self.uri,
            'name': self.name,
            'activity': self.count,
            'latest': None,
            'commits': list(x.as_dict() for x in self.commits)
        }
        if self.latest:
            d['latest'] = self.latest.as_dict()
        return d


class RepositoryMonitor(object):
    def __init__(self):
        self.repos = []

    def add(self, uri):
        self.repos.append(uri)

    def get_status(self):
        for repo in self.repos:
            try:
                print 'Checking %s' % repo
                yield self.get_repo_status(repo)
            except Exception as err:
                print "Error checking %s. %s" % (repo, err)

    @classmethod
    def get_repo_helper(cls, uri):
        if git_helper.GitHelper.test(uri):
            return git_helper.GitHelper(uri)
        elif hg_helper.HgHelper.test(uri):
            return hg_helper.HgHelper(uri)
        else:
            print "Unable to understand this uri: %s" % uri

    @classmethod
    def get_repo_status(cls, uri):
        repo = cls.get_repo_helper(uri)
        repo.setup()
        repo.sync()
        return RepositoryStatus(uri, repo.name, repo.filename, repo.status())


class TotalStatus(object):
    @classmethod
    def load_from_disk(cls):
        repos = []
        for path in os.listdir('data'):
                with open('data/' + path) as f:
                    repo = json.loads(f.read())
                    if repo['activity'] > 0:
                        repos.append(repo)
        repos = sorted(repos, key=lambda x: x['activity'], reverse=True)
        return repos

    @classmethod
    def parse(cls, json_as_text):
        l = []
        data = json.loads(json_as_text)
        for item in data:
            l.append({
                'uri': item['uri'],
                'name': item['name'],
                'activity': item['activity'],
                'latest': Commit.from_dict(item['latest'])
            })
        return l

    @classmethod
    def fetch(cls):
        monitor = RepositoryMonitor()
        repos = settings.all_repos()
        repos += github_helper.get_repos("lshift")
        repos += bitbucket_helper.get_repos("lshift")
        repos += mercurial_server.get_repos("http://hg.lshift.net")

        for repo in repos:
            monitor.add(repo)
        return monitor.get_status()

    @classmethod
    def write_to_disk(cls):
        for repo in cls.fetch():
            path = 'data/%s.json' % repo.filename
            try:
                with open(path, 'w') as f:
                    f.write(json.dumps(repo.as_dict(), indent=4))
            except Exception as e:
                print "Unable to save to %s" % path
                print e.strerror


if __name__ == "__main__":
    TotalStatus.write_to_disk()
