import json
from os.path import join as pjoin
from six import StringIO

from encryptit.dump_json import dump_stream

from ..sample_files import SAMPLE_DIR, SAMPLE_FILES


def test_dump_stream_produces_valid_json():
    for short_filename, full_filename in SAMPLE_FILES:
        yield assert_produces_valid_json, short_filename


def assert_produces_valid_json(filename):
    with open(pjoin(SAMPLE_DIR, filename), 'rb') as f:
        json_stream = StringIO()  # JSON is a text stream.
        dump_stream(f, json_stream)
        json_stream.seek(0)
        json_string = json_stream.read()

    assert isinstance(json.loads(json_string), dict)
