import glob
import json
import os

from os.path import basename, dirname, join as pjoin

from nose.tools import assert_equal

from encryptit.openpgp_message import OpenPGPMessage
from encryptit.dump_json import OpenPGPJsonEncoder

from ..sample_files import SAMPLE_DIR

EXPECTED_JSON_DIR = pjoin(dirname(__file__), 'expected_json')

assert_equal.__self__.maxDiff = None


def _get_expected(filename):
    full_filename = pjoin(EXPECTED_JSON_DIR, filename + '.expected.json')
    with open(full_filename, 'r') as f:
        return f.read()


def _write_out_got_json(filename, got_json):
    full_filename = _make_got_json_filename(filename)
    with open(full_filename, 'w') as f:
        return f.write(got_json)


def _delete_got_json(filename):
    full_filename = _make_got_json_filename(filename)
    if os.path.exists(full_filename):
        os.unlink(full_filename)


def _make_got_json_filename(filename):
    return pjoin(EXPECTED_JSON_DIR, filename + '.__GOT__.json')


def test_openpgp_message_serialize():
    for filename in glob.glob(pjoin(EXPECTED_JSON_DIR, '*.expected.json')):
        sample_filename = filename[0:-len('.expected.json')]

        yield check_json_against_expected, basename(sample_filename)


def check_json_against_expected(filename):
    # convert to JSON then back again in order to compare as python objects -
    # less picky than comparing as strings.

    with open(pjoin(SAMPLE_DIR, filename), 'rb') as f:
        message = OpenPGPMessage.from_stream(f)
        got_json = json.dumps(
            message.serialize(), cls=OpenPGPJsonEncoder, indent=2)

    expected_json = _get_expected(filename)

    try:
        assert_equal(json.loads(expected_json), json.loads(got_json))
    except AssertionError:
        _write_out_got_json(filename, got_json)
        raise
    else:
        _delete_got_json(filename)
