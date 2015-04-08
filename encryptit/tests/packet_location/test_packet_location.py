import json

from nose.tools import assert_equal, assert_not_equal

from encryptit.packet_location import PacketLocation
from encryptit.dump_json import OpenPGPJsonEncoder

PACKET_LOCATION_1 = PacketLocation(
    header_start=10,
    body_start=12,
    body_length=8)

PACKET_LOCATION_2 = PacketLocation(
    header_start=PACKET_LOCATION_1.header_start,
    body_start=PACKET_LOCATION_1.body_start,
    body_length=PACKET_LOCATION_1.body_length)

PACKET_LOCATION_3 = PacketLocation(
    header_start=0,
    body_start=2,
    body_length=10)


def test_packet_location_header_length_field():
    assert_equal(2, PACKET_LOCATION_1.header_length)


def test_packet_location_header_end_field():
    assert_equal(12, PACKET_LOCATION_1.header_end)


def test_packet_location_body_end_field():
    assert_equal(20, PACKET_LOCATION_1.body_end)


def test_packet_location_json_serializing():
    # convert to JSON then back again in order to compare as python objects -
    # less picky than comparing as strings.

    as_json = json.dumps(PACKET_LOCATION_1, cls=OpenPGPJsonEncoder)
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


def test_packet_location_equality():
    yield assert_equal, PACKET_LOCATION_1, PACKET_LOCATION_2
    yield assert_not_equal, PACKET_LOCATION_1, PACKET_LOCATION_3
