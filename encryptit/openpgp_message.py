from .compat import OrderedDict


class OpenPGPMessage(object):
    @classmethod
    def from_stream(cls, f):
        """
        Decode OpenPGP packets from a file-like object and return an
        `OpenPGPMessage` instance.

        Ciphertext data is decrypted lazily in order to support arbitrarily
        long encrypted files. Therefore the file handle must remain open until
        all packets have been decoded successfully, eg:

        ```
        with open('huge.gpg', 'rb') as f:
            openpgp_message = OpenPGPMessage.from_stream(f)
            print(f.serialize())  # f still in use
        ```
        """
        from .decoder import find_packets  # unavoidable circular import
        return cls(packet_locations=find_packets(f))

    def __init__(self, packet_locations=None):
        assert packet_locations is None or \
            isinstance(packet_locations, list), type(packet_locations)

        self.packet_locations = packet_locations

    def serialize(self):
        return OrderedDict([
            ('packet_locations', self.packet_locations),
        ])


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
