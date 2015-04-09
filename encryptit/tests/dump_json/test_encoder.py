import json

from nose.tools import assert_equal

from encryptit.dump_json import OpenPGPJsonEncoder


def test_encode_bytearray():
    result = json.dumps(bytearray([0x01, 0x08]), cls=OpenPGPJsonEncoder)
    assert_equal('{"octets": "01:08", "length": 2}', result)
