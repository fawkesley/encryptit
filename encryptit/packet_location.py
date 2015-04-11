from .compat import OrderedDict


class PacketLocation(object):

    def __init__(self, header_start, body_start, body_length):
        self.header_start = header_start
        self.body_start = body_start
        self.body_length = body_length

    def serialize(self):
        return OrderedDict([
            ('header_start', self.header_start),
            ('header_length', self.header_length),
            ('header_end', self.header_end),
            ('body_start', self.body_start),
            ('body_length', self.body_length),
            ('body_end', self.body_end),
        ])

    @property
    def header_length(self):
        return self.body_start - self.header_start

    @property
    def header_end(self):
        return self.body_start

    @property
    def body_end(self):
        return self.body_start + self.body_length

    def __eq__(self, other):
        return other.__dict__ == self.__dict__
