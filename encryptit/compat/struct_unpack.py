"""
Python 2.6 `struct.unpack` differs from 2.7, 3.x as it cannot accept a
`bytearray` argument. The `bytearray` seems the most portable container
so the solution here is to provide a Python-2.6 specific wrapper which
converts the `bytearray` into `str`.
"""

import sys
import struct


def is_version_2_6():
    (major, minor, _, _, _) = sys.version_info
    return major == 2 and minor == 6


def _unpack_v26(format_string, byte_array):
    _validate_byte_array_type(byte_array)
    _validate_format_string(format_string)

    return struct.unpack(format_string, str(byte_array))


def _unpack_v27_v3x(format_string, byte_array):
    _validate_byte_array_type(byte_array)
    _validate_format_string(format_string)

    return struct.unpack(format_string, byte_array)


def _validate_byte_array_type(byte_array):
    if not isinstance(byte_array, bytearray):
        raise TypeError(
            'Can only unpack from `bytearray` not: {0}'.format(
                type(byte_array)))


def _validate_format_string(format_string):
    """
    Ensure that either little endian (<) or big endian (>) is specified.
    """
    if not format_string.startswith('<') and not format_string.startswith('>'):
        raise ValueError(
            'Byte order must be specified. See '
            'https://docs.python.org/3/library/struct.html'
            '#byte-order-size-and-alignment')

struct_unpack = _unpack_v26 if is_version_2_6() else _unpack_v27_v3x
