from contextlib import contextmanager
import os


@contextmanager
def pushd(path):
    old_path = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_path)


def to_filename(string):
    return "".join(x if x.isalnum() else "_" for x in string)

DEVNULL = open(os.devnull, 'wb')