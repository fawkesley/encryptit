from ..compat import OrderedDict


class GenericPacketHeader(object):
    def serialize(self):
        return OrderedDict([
            ('packet_type', self.packet_type),
            ('packet_format', self.packet_format),
            ('header_length', self.header_length),
            ('body_length', self.body_length),
        ])
