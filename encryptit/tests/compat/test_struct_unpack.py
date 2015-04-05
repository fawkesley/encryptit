from nose.tools import assert_equal, assert_raises
from encryptit.compat import struct_unpack

# See https://docs.python.org/2/library/struct.html

TESTS = [
    (bytearray([1, 2, 3, 4]), 'I', (67305985,)),
    (bytearray([1, 2, 3, 4]), 'HH', (513, 1027)),
    (bytearray([1, 2, 3, 4]), 'BBBB', (1, 2, 3, 4)),
]


UNSUPPORTED_TYPES = [
    bytes,
    str,
    list
]


def test_struct_unpack():
    for byte_array, format_string, expected in TESTS:
        yield assert_struct_unpack_equals, format_string, byte_array, expected


def assert_struct_unpack_equals(format_string, byte_array, expected):
    assert_equal(expected, struct_unpack(format_string, byte_array))


def test_non_bytearray_types_raise_type_error():
    for type_ in UNSUPPORTED_TYPES:
        yield assert_raises_for_type, type_


def assert_raises_for_type(type_):
    data = type_([1, 2, 3, 4])
    assert_raises(TypeError, lambda x: struct_unpack(data))
