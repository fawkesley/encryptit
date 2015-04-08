import sys

from ..dump_json import dump_stream


def dump_json(filename):
    with open(filename, 'rb') as f:
        dump_stream(f, sys.stdout)
