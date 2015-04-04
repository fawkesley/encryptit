from .compat import OrderedDict


class SerializeNameOctetValueMixin(object):
    def serialize(self):
        return OrderedDict([
            ('name', self.name),
            ('octet_value', self.value),
        ])
