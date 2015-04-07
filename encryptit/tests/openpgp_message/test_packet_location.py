import json

from nose.tools import assert_equal

from encryptit.openpgp_message import PacketLocation
from encryptit.dump_json import OpenPGPJsonEncoder

PACKET_LOCATION = PacketLocation(
    header_start=10,
    body_start=12,
    body_length=8)


def test_packet_location_header_length_field():
    assert_equal(2, PACKET_LOCATION.header_length)


def test_packet_location_header_end_field():
    assert_equal(12, PACKET_LOCATION.header_end)


def test_packet_location_body_end_field():
    assert_equal(20, PACKET_LOCATION.body_end)


def test_packet_location_serialize():
    # convert to JSON then back again in order to compare as python objects -
    # less picky than comparing as strings.

    as_json = json.dumps(PACKET_LOCATION.serialize(), cls=OpenPGPJsonEncoder)
    back_to_data = json.loads(as_json)

    assert_equal(
        {
            'header_start': 10,
            'header_length': 2,
            'header_end': 12,
            'body_start': 12,
            'body_length': 8,
            'body_end': 20,
        },
        back_to_data)
