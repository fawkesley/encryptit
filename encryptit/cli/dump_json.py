import sys

from ..dump_json import dump_stream


def dump_json(filename):
    with open(filename, 'rb') as f:
        sys.stdout.write(dump_stream(f) + '\n')
