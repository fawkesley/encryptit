import json
from os.path import join as pjoin

from encryptit.dump_json import dump_stream

from ..sample_files import SAMPLE_DIR, SAMPLE_FILES
from ..test_utils import assert_is_instance


def test_dump_stream_produces_valid_json():
    for short_filename, full_filename in SAMPLE_FILES:
        yield assert_produces_valid_json, short_filename


def assert_produces_valid_json(filename):
    with open(pjoin(SAMPLE_DIR, filename), 'rb') as f:
        json_string = dump_stream(f)

    assert_is_instance(json.loads(json_string), dict)
