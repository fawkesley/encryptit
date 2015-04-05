from .compat import OrderedDict
from collections import namedtuple


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


class PacketLocation(namedtuple('PacketLocation', 'start,length,packet_type')):
    def serialize(self):
        return OrderedDict([
            ('start', self.start),
            ('length', self.length),
            ('packet_type', self.packet_type),
        ])
