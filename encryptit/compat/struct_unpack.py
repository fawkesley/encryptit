"""
Python 2.6 `struct.unpack` differs from 2.7, 3.x as it cannot accept a
`bytearray` argument.

We use the `bytearray_or_str` helper to get round this.
"""

import struct

from .bytearray_or_str import bytearray_or_str


def struct_unpack(format_string, byte_array):
    _validate_format_string(format_string)

    return struct.unpack(format_string, bytearray_or_str(byte_array))


def _validate_format_string(format_string):
    """
    Ensure that either little endian (<) or big endian (>) is specified.
    """
    if not format_string.startswith('<') and not format_string.startswith('>'):
        raise ValueError(
            'Byte order must be specified. See '
            'https://docs.python.org/3/library/struct.html'
            '#byte-order-size-and-alignment')
