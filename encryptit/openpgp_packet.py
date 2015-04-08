from .compat import OrderedDict
from .decoder import consume_header, decode_body


class OpenPGPPacket(object):
    @classmethod
    def from_stream(cls, f, packet_location):
        return cls(f, packet_location)

    def __init__(self, f, packet_location):
        self.f = f
        self.packet_location = packet_location
        self._header = None
        self._body = None

    def serialize(self):
        return OrderedDict([
            ('location', self.packet_location),
            ('header', self.header),
            ('body', self.body),
        ])

    @property
    def header(self):
        if self._header is None:
            self.f.seek(self.packet_location.header_start)
            self._header = consume_header(self.f)

        return self._header

    @property
    def body(self):
        if self._body is None:
            self.f.seek(self.packet_location.body_start)
            self._body = decode_body(
                self.f,
                self.packet_location.body_start,
                self.packet_location.body_length,
                self.header.packet_type)

        return self._body
