from ..compat import struct_unpack
from ..exceptions import MalformedPacketError
from ..stream_utils import read_bytes

from .generic_packet_header import GenericPacketHeader
from .packet_type import PacketType


class OldFormatPacketHeader(GenericPacketHeader):
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
        return 'OldFormatPacketHeader: {0}'.format(self.packet_type)
