import os
from subprocess import call, check_output

from commit import Commit
from file_helpers import pushd, DEVNULL
from repo_helper import RepoHelper


class HgHelper(RepoHelper):
    def __init__(self, uri):
        super(HgHelper, self).__init__(uri)

    def setup(self):
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)
            with pushd(self.local_path):
                call(['hg', 'init'])

    def sync(self):
        with pushd(self.local_path):
            call(['hg', 'pull', self.uri], stdout=DEVNULL)

    def status(self):
        date_range = "%s to %s" % (self._start_date().isoformat(), self._end_date().isoformat())
        with pushd(self.local_path):
            args = ['hg', 'log',
                    '--template', '{node},{author},{date|isodate}\n',
                    '--date', date_range]
            raw = check_output(args)
        for line in raw.split('\n'):
            if line.strip():
                parts = line.split(',')
                yield Commit(*parts)

    @classmethod
    def test(cls, uri):
        return call(['hg', 'identify', uri], stdout=DEVNULL) == 0