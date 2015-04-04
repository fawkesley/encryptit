import struct

from io import BytesIO

from nose.tools import assert_equal, assert_raises

from encryptit.decoder import consume_header
from encryptit.exceptions import MalformedPacketError


OLD_OCTET_0 = 0b10000000
NEW_OCTET_0 = 0b11000000

OLD_ONE_OCTET = 0
OLD_TWO_OCTETS = 1
OLD_FOUR_OCTETS = 2
OLD_INDETERMINATE = 3  # Indeterminate length byte, see 4.2.1

OLD_DISHONEST_LENGTH_PACKETS = [
    (OLD_ONE_OCTET, bytearray([])),

    # claim two octets, actually have 0 or 1
    (OLD_TWO_OCTETS, bytearray([])),
    (OLD_TWO_OCTETS, bytearray([0x00])),

    # claim 4 octets, actually have 0, 1, 2 or 3
    (OLD_FOUR_OCTETS, bytearray([])),
    (OLD_FOUR_OCTETS, bytearray([0x00])),
    (OLD_FOUR_OCTETS, bytearray([0x00, 0x00])),
    (OLD_FOUR_OCTETS, bytearray([0x00, 0x00, 0x00])),
]

NEW_DISHONEST_LENGTH_PACKETS = [
    # no length bytes - never valid
    bytearray([]),

    # claim 2 octets total, actually only 1
    bytearray([192]),
    bytearray([223]),

    # claim 5 octets, actually 1, 2, 3 or 4
    bytearray([255]),
    bytearray([255, 0x00]),
    bytearray([255, 0x00, 0x00]),
    bytearray([255, 0x00, 0x00, 0x00]),
]


def test_missing_bit_7_explodes():
    for octet in range(128):
        yield assert_raises_malformed, bytearray([octet])


def test_old_format_invalid_packet_tag():
    for bad_packet_tag in [0, 15]:
        octet = OLD_OCTET_0 | bad_packet_tag << 2
        yield assert_raises_malformed, bytearray([octet])


def test_new_format_invalid_packet_tag():
    # maximum value for 6 bytes is 63
    for bad_packet_tag in [0, 15] + list(range(20, 63 + 1)):
        octet = NEW_OCTET_0 | bad_packet_tag
        dummy_length_byte = 0x00
        yield assert_raises_malformed, bytearray([octet, dummy_length_byte])


def test_old_format_dishonest_length_header():
    packet_tag = 2  # arbitrary but valid
    base_octet = OLD_OCTET_0 | packet_tag << 2

    for length_type, length_octets in OLD_DISHONEST_LENGTH_PACKETS:
        packet = bytearray([base_octet | length_type]) + length_octets
        yield assert_raises_malformed, packet


def test_new_format_dishonest_length_header():
    packet_tag = 2  # arbitrary but valid
    base_octet = NEW_OCTET_0 | packet_tag

    for length_octets in NEW_DISHONEST_LENGTH_PACKETS:
        packet = bytearray([base_octet]) + length_octets
        yield assert_raises_malformed, packet


def test_old_format_blows_up_with_indeterminate_length():
    packet_tag = 3
    packet_octet = OLD_OCTET_0 | (packet_tag << 2) | OLD_INDETERMINATE
    stream = BytesIO(bytearray([packet_octet]))
    assert_raises(NotImplementedError, lambda: consume_header(stream))


def test_new_format_partial_length_explodes_with_first_octet():
    # "It is recognized by its one octet value that is greater than or equal to
    # 224, and less than 255."
    for length_first_octet in range(224, 255):
        yield assert_partial_length_blows_up, length_first_octet


def test_decode_old_format_header():
    for packet_tag in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
        for body_length in [0, 0xFF, 1 + 0xFF, 0xFFFF, 1 + 0xFFFF, 0xFFFFFFFF,
                            0xFFFFFFFF]:
            octets = _make_old_format_header(packet_tag, body_length)
            yield (assert_decodes_correctly,
                   octets, packet_tag, body_length, 'old')


def test_decode_new_format_header():
    for packet_tag in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                       13, 14, 17, 18, 19]:
        for body_length in [0, 191, 192, 8383, 8384, 0xFFFFFFFF]:
            octets = _make_new_format_header(packet_tag, body_length)
            yield (assert_decodes_correctly,
                   octets, packet_tag, body_length, 'new')


def assert_partial_length_blows_up(length_first_octet):
    packet_tag = 3
    packet_first_octet = NEW_OCTET_0 | packet_tag

    stream = BytesIO(bytearray([packet_first_octet, length_first_octet]))

    assert_raises(NotImplementedError, lambda: consume_header(stream))


def _make_old_format_header(packet_tag, body_length):
    tag_bits = (packet_tag & 0b00001111) << 2

    if 0 <= body_length <= 0xFF:
        length_type_bits = 0b00000000  # 0 means 1-octet length
        length_octets = bytearray([body_length])

    elif 0xFF < body_length <= 0xFFFF:
        length_type_bits = 0b00000001  # 1 means 2-octet length
        # https://docs.python.org/2/library/struct.html#format-characters
        length_octets = struct.pack('H', body_length)

    elif 0xFFFF < body_length <= 0xFFFFFFFF:
        length_type_bits = 0b00000010  # 2 means 4-octet length
        length_octets = struct.pack('I', body_length)

    else:
        raise ValueError(body_length)

    packet_first_octet = OLD_OCTET_0 | tag_bits | length_type_bits
    return bytearray([packet_first_octet]) + length_octets


def _make_new_format_header(packet_tag, body_length):
    tag_bits = (packet_tag & 0b00111111)

    assert 0 < tag_bits & 0b00111111 <= 19

    if 0 <= body_length <= 191:  # one-octet length
        length_octets = bytearray([body_length])

    elif 192 <= body_length <= 8383:  # two-octet length
        # https://tools.ietf.org/html/rfc4880#section-4.2.2.2

        tmp = body_length - 192
        first_octet = (tmp >> 8) + 192
        second_octet = tmp & 0xFF

        assert 192 <= first_octet <= 223, first_octet
        assert 0 <= second_octet <= 255, second_octet

        length_octets = bytearray([first_octet, second_octet])

    elif 8383 < body_length <= 0xFFFFFFFF:  # five-octet length
        # https://tools.ietf.org/html/rfc4880#section-4.2.2.3
        length_octets = bytearray([255]) + struct.pack('I', body_length)

    packet_first_octet = NEW_OCTET_0 | tag_bits
    return bytearray([packet_first_octet]) + length_octets


def assert_decodes_correctly(octets, expected_packet_tag,
                             expected_body_length, expected_packet_format):
    b = BytesIO(octets)
    header = consume_header(b)
    assert_equal(expected_packet_format, header.packet_format)
    assert_equal(expected_packet_tag, header.packet_type.value)
    assert_equal(expected_body_length, header.body_length)

    # test that consume read to the end of the header
    assert_equal(b'', b.read())


def assert_raises_malformed(octets):
    b = BytesIO(octets)
    assert_raises(MalformedPacketError, lambda: consume_header(b))
