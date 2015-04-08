from ..compat import OrderedDict


class GenericPacketHeader(object):
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
