import json

from .compat import OrderedDict
from .openpgp_message import OpenPGPMessage


def dump_stream(f, output_stream, indent=4):
    message = OpenPGPMessage.from_stream(f)
    return json.dump(message, output_stream, indent=indent,
                     cls=OpenPGPJsonEncoder)


class OpenPGPJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytearray):
            return self.serialize_bytes(obj)

        if getattr(obj, 'serialize', None):
            return obj.serialize()

        return super(OpenPGPJsonEncoder, self).default(obj)

    @staticmethod
    def serialize_bytes(some_bytes):
        return OrderedDict([
            ('octets', ':'.join(['{0:02x}'.format(byte)
                                 for byte in some_bytes])),
            ('length', len(some_bytes)),
        ])
