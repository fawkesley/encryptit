from .compat import OrderedDict
from .decoder import find_packets
from .openpgp_packet import OpenPGPPacket


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
        return cls(f, packet_locations=find_packets(f))

    def __init__(self, f, packet_locations=None):
        assert packet_locations is None or \
            isinstance(packet_locations, list), type(packet_locations)

        self.f = f
        self.packet_locations = packet_locations

    def serialize(self):
        return OrderedDict([
            ('packets', self.packets),
        ])

    @property
    def packets(self):
        return [OpenPGPPacket.from_stream(self.f, pl)
                for pl in self.packet_locations]
