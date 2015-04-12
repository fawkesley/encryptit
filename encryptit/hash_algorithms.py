#!/usr/bin/env python3

import hashlib

from .compat import OrderedDict, bytearray_or_str

from .length import Length


def decode_hash_algorithm(octet):
    if not isinstance(octet, int) or not 0 <= octet < 256:
        raise TypeError('Bad octet value: `{0}` of type `{1}`'.format(
            octet, type(octet)))

    try:
        return BYTE_TO_HASH[octet]
    except KeyError:
        raise ValueError(
            'Unknown hash algorithm `{0}`. See '
            'http://tools.ietf.org/html/rfc4880#section-9.4'.format(octet))


class HashAlgorithm():
    """
    9.4. Hash Algorithms
    http://tools.ietf.org/html/rfc4880#section-9.4
    """
    def __init__(self):
        raise RuntimeError('HashAlgorithm should not be instantiated')

    @classmethod
    def new(cls):
        return HashWrapper(cls.hash_constructor())

    @classmethod
    def serialize(cls):
        return OrderedDict([
            ('name', cls.__name__),
            ('octet_value', HASH_TO_BYTE[cls]),
            ('digest_length', cls.length),
        ])


class HashWrapper():
    def __init__(self, hash_instance):
        self._h = hash_instance

    def update(self, data):
        return self._h.update(bytearray_or_str(data))

    def digest(self):
        return bytearray(self._h.digest())

    def hexdigest(self):
        return self._h.hexdigest()


class MD5(HashAlgorithm):
    length = Length(bits=128)  # 16 octets
    hash_constructor = hashlib.md5


class SHA1(HashAlgorithm):
    length = Length(bits=160)  # 20 octets
    hash_constructor = hashlib.sha1


class RIPEMD160(HashAlgorithm):
    length = Length(bits=160)  # 20 octets

    @staticmethod
    def hash_constructor():
        return hashlib.new('ripemd160')


class SHA256(HashAlgorithm):
    length = Length(bits=256)  # 32 octets
    hash_constructor = hashlib.sha256


class SHA384(HashAlgorithm):
    length = Length(bits=384)  # 48 octets
    hash_constructor = hashlib.sha384


class SHA512(HashAlgorithm):
    length = Length(bits=512)  # 64 octets
    hash_constructor = hashlib.sha512


class SHA224(HashAlgorithm):
    length = Length(bits=224)  # 28 octets
    hash_constructor = hashlib.sha224


BYTE_TO_HASH = {
    1: MD5,
    2: SHA1,
    3: RIPEMD160,
    8: SHA256,
    9: SHA384,
    10: SHA512,
    11: SHA224,
}

HASH_TO_BYTE = dict(
    [(v, k) for k, v in BYTE_TO_HASH.items()]
)
