from .compat import OrderedDict


class Length(object):
    def __init__(self, bits=None, octets=None):
        if not self.ensure_exactly_one_non_null(bits, octets):
            raise ValueError('Exactly one of `bits` and `octets` required.')

        if bits is not None:
            if bits % 8 != 0:
                raise ValueError('Bits must be a multiple of 8')
            self._length_bits = bits

        elif octets is not None:
            self._length_bits = octets * 8

    @staticmethod
    def ensure_exactly_one_non_null(*args):
        non_nulls = list(filter(lambda x: x is not None, args))
        return len(non_nulls) == 1

    @property
    def in_bits(self):
        return self._length_bits

    @property
    def in_octets(self):
        return int(self._length_bits / 8)

    def serialize(self):
        return OrderedDict([
            ('bits', self.in_bits),
            ('octets', self.in_octets),
        ])
