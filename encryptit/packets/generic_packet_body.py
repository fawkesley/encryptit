from ..compat import OrderedDict
from ..stream_utils import read_bytes

from .base_packet_body import BasePacketBody


class GenericPacketBody(BasePacketBody):
    """
    Provides a generic `__init__` and `raw` method but no decoded data.
    Useful for packets we don't yet know how to decode or as a parent class
    of specific packet body types.
    """

    @classmethod
    def from_stream(cls, f, body_start, body_length):
        obj = cls()
        obj.f = f
        obj._body_start = body_start
        obj._body_length = body_length
        return obj

    def __init__(self):
        self.f = None
        self._body_start = None
        self._body_length = None

    @property
    def raw(self):
        self.f.seek(self._body_start)
        # Beware: Now we're loading into memory.
        return read_bytes(self.f, self._body_length)

    @property
    def decoded(self):
        return None

    def serialize(self):
        return OrderedDict([
            ('raw', self.raw),
            ('decoded', self.decoded),
        ])
