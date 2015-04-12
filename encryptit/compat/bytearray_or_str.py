"""
In Python 2.6 some things like `struct.unpack`, `hashlib.sha1().update`
cannot take a `bytearray`.

The `bytearray` seems the most portable container so we use it extensively in
the codebase.

This compatibility function converts it to a `str` on Python 2.6 only.
"""

import sys


def bytearray_or_str(byte_array):
    _validate_got_bytearray(byte_array)

    if _is_version_2_6():
        return str(byte_array)
    else:
        return byte_array


def _validate_got_bytearray(byte_array):
    if not isinstance(byte_array, bytearray):
        raise TypeError(
            'Can only accept `bytearray` not: {0}'.format(type(byte_array)))


def _is_version_2_6():
    (major, minor, _, _, _) = sys.version_info
    return major == 2 and minor == 6
