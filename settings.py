import json
from os.path import exists


class Settings(object):
    def __init__(self):
        self.data = dict()

    def load(self):
        self.data = json.loads(Settings.json())
        if not ('repos' in self.data):
            self.data['repos'] = []
        if not ('data_path' in self.data):
            self.data['data_path'] = 'repos'

    def save(self):
        with open('settings.json', 'w') as f:
            f.write(json.dumps(self.data, indent=4))

    def add_repo(self, uri):
        self.data['repos'].append(uri)

    def remove_repo(self, uri):
        self.data['repos'].remove(uri)

    def all_repos(self):
        return list(self.data['repos'])

    @classmethod
    def json(cls):
        if exists('settings.json'):
            with open('settings.json', 'r') as f:
                return f.read()
        return "{ }"

settings = Settings()
settings.load()
