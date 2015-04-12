from io import BytesIO
from nose.tools import assert_equal, assert_raises

from encryptit.packets import GenericPacketBody
from encryptit.exceptions import MalformedPacketError


BODY = bytearray([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

TESTS = [
    (0, 10, bytearray([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])),
    (1, 9, bytearray([1, 2, 3, 4, 5, 6, 7, 8, 9])),
    (0, 9, bytearray([0, 1, 2, 3, 4, 5, 6, 7, 8])),
]


def _make_body(body_start, body_length):
    return GenericPacketBody.from_stream(
        BytesIO(BODY), body_start, body_length)


def test_raw_reads_correct_start_and_length():
    for body_start, body_length, expected_raw in TESTS:
        body = _make_body(body_start, body_length)
        assert_equal(expected_raw, body.raw)


def test_that_raw_works_multiple_times():
    body = GenericPacketBody.from_stream(BytesIO(BODY), 3, 5)
    assert_equal(body.raw, body.raw)


def test_that_reading_too_much_data_raises_malformed_packet_error():
    for body_start in range(10):
        body_length = 11 - body_start  # 1 byte too long
        yield assert_detects_malformed_packet, body_start, body_length


def assert_detects_malformed_packet(body_start, body_length):
    body = _make_body(body_start, body_length)

    def get_raw():
        return body.raw

    assert_raises(MalformedPacketError, get_raw)


def test_that_body_start_after_end_of_data_raises_malformed_packet_error():
    assert_detects_malformed_packet(10, 1)


def test_that_invalid_body_start_or_length_explodes_at_instantiation():
    yield assert_raises, ValueError, _make_body, -1, 1
    yield assert_raises, ValueError, _make_body, 0, -1
    yield assert_raises, ValueError, _make_body, 0, 0  # body can't be zero
