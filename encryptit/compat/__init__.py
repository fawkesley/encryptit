try:
    from collections import OrderedDict
except ImportError:  # Not available on Python 2.6
    from .ordered_dict import OrderedDict


from .struct_unpack import struct_unpack
from .abstract_class_method import abstractclassmethod
