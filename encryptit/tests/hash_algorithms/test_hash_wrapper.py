from hashlib import sha1
from nose.tools import assert_equal

from ..test_utils import assert_is_instance

from encryptit.hash_algorithms import HashWrapper


SHA1_HASH_OF_ZERO = '5ba93c9db0cff93f52b521d7420e43f6eda2784f'


def test_update_handles_bytearray_correctly():
    h = HashWrapper(sha1())
    h.update(bytearray([0]))
    assert_equal(SHA1_HASH_OF_ZERO, h.hexdigest())


def test_that_digest_method_returns_bytearray():
    h = HashWrapper(sha1())
    h.update(bytearray([0]))
    yield assert_is_instance, h.digest(), bytearray
    yield assert_equal, h.digest()[0:4], bytearray([0x5b, 0xa9, 0x3c, 0x9d])
