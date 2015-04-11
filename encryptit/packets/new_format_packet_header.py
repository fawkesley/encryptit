from ..exceptions import MalformedPacketError
from ..compat import struct_unpack
from ..stream_utils import read_bytes


from .generic_packet_header import GenericPacketHeader
from .packet_type import PacketType


class NewFormatPacketHeader(GenericPacketHeader):
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
        return 'NewFormatPacketHeader: {0}'.format(self.packet_type)
