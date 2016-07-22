from commit import Commit
import git
from subprocess import call, check_output

from file_helpers import pushd, DEVNULL
from repo_helper import RepoHelper


class GitKey(object):
    def __init__(self, name):
        self.name = name


class GitHelper(RepoHelper):
    def __init__(self, uri):
        super(GitHelper, self).__init__(uri)

    def setup(self):
        self.repo = git.Repo.init(self.local_path, bare=True)

        if GitKey('origin') in self.repo.remotes:
            self.remote = self.repo.remotes['origin']
            self.remote.set_url(self.uri)
        else:
            self.remote = self.repo.create_remote('origin', self.uri)
        assert self.remote.exists()

    def sync(self):
        with pushd(self.local_path):
            call(['git', 'fetch'])

    @property
    def name(self):
        name = super(GitHelper, self).name
        if name[-4:] == ".git":
            stop_at = len(name) - 4
            name = name[0:stop_at]
        return name

    def status(self):
        with pushd(self.local_path):
            raw = check_output(['git', 'log', '--all',
                                '--format=%H,%cn,%cI',
                                '--after', self._start_date().isoformat()])
        for line in raw.split('\n'):
            if line.strip():
                parts = line.split(',')
                yield Commit(*parts)

    @classmethod
    def test(cls, uri):
        return call(['git', 'ls-remote', uri], stdout=DEVNULL, stderr=DEVNULL) == 0
