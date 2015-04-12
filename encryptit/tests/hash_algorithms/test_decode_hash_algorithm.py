from nose.tools import assert_equal, assert_raises

from encryptit.hash_algorithms import (
    decode_hash_algorithm, MD5, SHA1, RIPEMD160, SHA256, SHA384, SHA512,
    SHA224)

HASH_ALGOS = {
    # https://tools.ietf.org/html/rfc4880#section-9.4
    1: MD5,
    2: SHA1,
    3: RIPEMD160,
    8: SHA256,
    9: SHA384,
    10: SHA512,
    11: SHA224,
}


def test_decode_returns_correct_hash_class():
    for octet, expected_class in HASH_ALGOS.items():
        got_class = decode_hash_algorithm(octet)
        yield assert_equal, expected_class, got_class


def test_decode_raises_value_error_on_all_other_octet_values():
    for bad_octet in set(range(256)) - set(HASH_ALGOS.keys()):
        yield assert_raises, ValueError, decode_hash_algorithm, bad_octet


def test_decode_raises_type_error_for_invalid_octet():
    for not_octet in [-1, 256, 1.0, '1']:
        yield assert_raises, TypeError, decode_hash_algorithm, not_octet
