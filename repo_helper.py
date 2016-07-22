import datetime
from os.path import join
from urlparse import urlparse

from file_helpers import to_filename


# 'Abstract' class
class RepoHelper(object):
    def __init__(self, uri):
        self.uri = uri
        self.filename = to_filename(self.uri)
        self.local_path = join('repos', self.filename)
        self.repo = 'Call setup first'
        self.remote = 'Call setup first'

    def setup(self):
        pass

    def sync(self):
        pass

    @property
    def name(self):
        name = self.uri.strip('/')
        return name.rsplit('/', 1)[-1]

    def status(self):
        pass

    def _end_date(self):
        return datetime.date.today()

    def _start_date(self):
        return self._end_date() - datetime.timedelta(days=7)

