import functools
import logging

from .exceptions import MalformedPacketError
from .packet_location import PacketLocation
from .packets import (get_packet_body_class, OldFormatPacketHeader,
                      NewFormatPacketHeader)
from .stream_utils import seek_relative, read_bytes

LOG = logging.getLogger(__name__)


class NoMoreData(StopIteration):
    pass


def as_list(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return list(func(*args, **kwargs))
    return wrapper


@as_list
def find_packets(f):
    """
    Scan through the file object yielding `PacketLocations` which contain the
    location (of the packet *body*), type and length of each packet.
    """
    while True:
        try:
            header = consume_header(f)
        except NoMoreData:
            break

        yield PacketLocation(
            header_start=f.tell() - header.header_length,
            body_start=f.tell(),
            body_length=header.body_length)

        seek_relative(f, header.body_length)


def consume_header(f):
    """
    Decode the header from the given stream and return a
    `NewFormatPacketHeader` or `OldFormatPacketHeader`, leaving the file handle
    pointing immediately after the header.
    """

    try:
        packet_tag = read_bytes(f, 1, NoMoreData)[0]
    except IndexError:
        raise NoMoreData

    seek_relative(f, -1)  # rewind!

    if is_new_packet_format(packet_tag):
        header = NewFormatPacketHeader(f)
    else:
        header = OldFormatPacketHeader(f)

    return header


def decode_body(f, start, length, packet_type):
    cls = get_packet_body_class(packet_type)
    return cls.from_stream(f, start, length)


def is_new_packet_format(packet_tag_byte):
    if not is_bit_set(packet_tag_byte, 7):  # bit 7 always set
        raise MalformedPacketError('First octet bit 7 is not set')

    return is_bit_set(packet_tag_byte, 6)


def is_bit_set(byte, bit):
    assert isinstance(byte, int), 'is_bit_set takes int, not {0}'.format(
        type(byte))
    assert 0 <= byte <= 255, 'byte must be 0 to 255: {0}'.format(byte)

    bitmasks = {
        0: 0b00000001,
        1: 0b00000010,
        2: 0b00000100,
        3: 0b00001000,
        4: 0b00010000,
        5: 0b00100000,
        6: 0b01000000,
        7: 0b10000000,
    }
    mask = bitmasks[bit]
    return (byte & mask) != 0
