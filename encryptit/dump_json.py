import json

from .compat import OrderedDict
from .openpgp_message import OpenPGPMessage


def dump_stream(f, indent=4):
    message = OpenPGPMessage.from_stream(f)
    return json.dumps(message, indent=indent, cls=OpenPGPJsonEncoder)


class OpenPGPJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return self.serialize_bytes(obj)

        if getattr(obj, 'serialize'):
            return obj.serialize()

        return repr(obj)

    @staticmethod
    def serialize_bytes(some_bytes):
        return OrderedDict([
            ('octets', ':'.join(['{:02x}'.format(byte)
                                 for byte in some_bytes])),
            ('length', len(some_bytes)),
        ])
