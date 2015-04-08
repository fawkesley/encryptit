import functools
import logging

from .compat import OrderedDict, struct_unpack
from .exceptions import MalformedPacketError
from .packet_location import PacketLocation
from .packets import PacketType
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
    Decode the header from the given stream and return a `NewPacketHeader` or
    `OldPacketHeader`, leaving the file handle pointing immediately after
    the header.
    """

    try:
        packet_tag = read_bytes(f, 1, NoMoreData)[0]
    except IndexError:
        raise NoMoreData

    seek_relative(f, -1)  # rewind!

    if is_new_packet_format(packet_tag):
        header = NewPacketHeader(f)
    else:
        header = OldPacketHeader(f)

    return header


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


class PacketHeader(object):
    def __init__(self, f):
        self.header_length = None
        self.body_length = None
        self.packet_type = None

    def serialize(self):
        return OrderedDict([
            ('packet_type', self.packet_type.name),
            ('packet_tag', self.packet_type.value),
            ('packet_format', self.packet_format),
            ('header_octets', self.header),
            ('body_octets', self.body),
        ])


class OldPacketHeader(PacketHeader):
    """
    4.2. Packet Headers - Old Format
    https://tools.ietf.org/html/rfc4880#section-4.2
    """
    packet_format = 'old'

    def __init__(self, f):
        """
        From https://tools.ietf.org/html/rfc4880#section-4.2:

        Old format packets contain:

        Bits 5-2 -- packet tag
        Bits 1-0 -- length-type
        """
        type_and_length = read_bytes(f, 1)[0]

        self._decode_packet_tag((0b00111100 & type_and_length) >> 2)
        self._decode_header_body_lengths(0b00000011 & type_and_length, f)

    def _decode_packet_tag(self, packet_tag):
        """
        https://tools.ietf.org/html/rfc4880#section-4.3
        """
        assert 0 <= packet_tag <= 15, (
            'Old Format Packet supports tag up to 15: {0}'.format(packet_tag))
        try:
            self.packet_type = PacketType(packet_tag)
        except ValueError as e:
            raise MalformedPacketError(e)

    def _decode_header_body_lengths(self, length_type, f):
        """
        Interprets the `length_type` and consumes a further 1, 2 or 4 octets
        which signify the body length.

        Sets `self.header_length` and `self.body_length` and leaves the file
        handle at end of the header (the start of the body).

        https://tools.ietf.org/html/rfc4880#section-4.2.1
        """
        if length_type == 0:  # 1 octet length (2 octet header)
            self.header_length = 2
            self.body_length = read_bytes(f, 1, MalformedPacketError)[0]

        elif length_type == 1:  # 2-octet length
            self.header_length = 3
            two_octets = read_bytes(f, 2, MalformedPacketError)
            self.body_length = struct_unpack('>H', two_octets)[0]

        elif length_type == 2:  # 4-octet length
            self.header_length = 5
            four_octets = read_bytes(f, 4, MalformedPacketError)
            self.body_length = struct_unpack('>I', four_octets)[0]

        else:
            raise NotImplementedError(
                'Unsupported packet length type: {0}, see '
                'https://tools.ietf.org/html/rfc4880#section-4.2.1'.format(
                    length_type))

    def __str__(self):
        return 'OldPacketHeader: {0}'.format(self.packet_type)


class NewPacketHeader(PacketHeader):
    packet_format = 'new'

    def __init__(self, f):
        type_octet = read_bytes(f, 1)[0]
        self._decode_packet_tag(0b00111111 & type_octet)  # bits 5-0
        self._decode_header_body_lengths(f)

    def _decode_packet_tag(self, packet_tag):
        try:
            self.packet_type = PacketType(packet_tag)
        except ValueError as e:
            raise MalformedPacketError(e)

    def _decode_header_body_lengths(self, f):
        """
        Consumes either 1, 2 or 5 octets and decodes them as the body length.
        Sets `self.body_length` and `self.header_length`, leaving the file
        handle at the end of the header (and start of the body).

        https://tools.ietf.org/html/rfc4880#section-4.2.2
        """
        first_octet = read_bytes(f, 1, MalformedPacketError)[0]

        if first_octet < 192:            # 4.2.2.1. One-Octet Lengths
            self.header_length = 2
            self.body_length = first_octet

        elif 192 <= first_octet <= 223:  # 4.2.2.2. Two-Octet Lengths
            # Although "in the range 192 to 223" is ambiguous on whether 223
            # is *inclusive*, we can show that it must be. By validating that
            #     `((223 - 192) << 8) + 0xFF + 192`
            # is equal to 8383 (see 4.2.2) rather than
            #     `((222 - 192) << 8) + 0xFF + 192`
            # which gives 8127
            second_octet = read_bytes(f, 1, MalformedPacketError)[0]
            self.header_length = 3
            self.body_length = ((first_octet - 192) << 8) + second_octet + 192

        elif first_octet == 255:         # 4.2.2.3. Five-Octet Lengths
            self.header_length = 6
            four_octets = read_bytes(f, 4, MalformedPacketError)
            self.body_length = struct_unpack('>I', four_octets)[0]

        else:
            raise NotImplementedError(
                'Partial Body Lengths not yet supported, see '
                'https://tools.ietf.org/html/rfc4880#section-4.2.2')

    def __str__(self):
        return 'NewPacketHeader: {0}'.format(self.packet_type)
