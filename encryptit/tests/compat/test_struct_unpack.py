from nose.tools import assert_equal, assert_raises

from ..test_utils import assert_is_instance
from encryptit.compat import struct_unpack

# See https://docs.python.org/2/library/struct.html

TESTS = [
    # (0x01 << 24) + (0x02 << 16) + (0x03 << 8) + 0x04
    (bytearray([1, 2, 3, 4]), '>I', (16909060,)),

    # (0x04 << 24) + (0x03 << 16) + (0x02 << 8) + 0x01
    (bytearray([1, 2, 3, 4]), '<I', (67305985,)),

    # (0x01 << 8) + 0x02 and (0x03 << 8) + (0x04)
    (bytearray([1, 2, 3, 4]), '>HH', (258, 772)),

    # (0x02 << 8) + (0x01) and (0x04 << 8) + 0x03
    (bytearray([1, 2, 3, 4]), '<HH', (513, 1027)),

    (bytearray([1, 2, 3, 4]), '>BBBB', (1, 2, 3, 4)),
]


UNSUPPORTED_TYPES = [
    bytes,
    str,
    list
]

ALLOWED_BYTE_ORDERS = ['<', '>']
DISALLOWED_BYTE_ORDERS = ['@', '=', '!', '']


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
    assert_raises(TypeError, lambda: struct_unpack('I', data))


def test_disallowed_byte_order_characters():
    for byte_order in DISALLOWED_BYTE_ORDERS:
        yield assert_byte_order_raises_value_error, byte_order


def assert_byte_order_raises_value_error(byte_order):
    data = bytearray([0x01, 0x02])
    assert_raises(ValueError, lambda: struct_unpack(byte_order + 'H', data))


def test_allowed_byte_order_characters():
    for byte_order in ALLOWED_BYTE_ORDERS:
        yield assert_byte_order_is_ok, byte_order


def assert_byte_order_is_ok(byte_order):
    data = bytearray([0x01, 0x02])
    assert_is_instance(struct_unpack(byte_order + 'H', data)[0], int)
