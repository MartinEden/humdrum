from dateutil import parser


class Commit(object):
    def __init__(self, id, author, timestamp):
        self.id = id
        self.author = author
        self.timestamp = parser.parse(timestamp)

    def as_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, d):
        return Commit(d['id'], d['author'], d['timestamp'])

    def __str__(self):
        return "%s by %s at %s" % (self.id, self.author, self.timestamp)

