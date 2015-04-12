# You can test the hashes here on the command line:
# $ dd if=/dev/zero bs=1 count=1 | sha224sum

from collections import namedtuple

from nose.tools import assert_equal

from encryptit.hash_algorithms import (
    MD5, SHA1, RIPEMD160, SHA256, SHA384, SHA512, SHA224)

HashDefinition = namedtuple(
    'HashDefinition',
    'name,digest_bits,zero_hashed')

KNOWN_PROPERTIES = {
    # https://en.wikipedia.org/wiki/MD5
    MD5: HashDefinition(
        'MD5',
        128,
        '93b885adfe0da089cdf634904fd59f71'),

    # https://en.wikipedia.org/wiki/SHA-1
    SHA1: HashDefinition(
        'SHA1',
        160,
        '5ba93c9db0cff93f52b521d7420e43f6eda2784f'),

    # https://en.wikipedia.org/wiki/RIPEMD
    # dd if=/dev/zero bs=1 count=1 | openssl rmd160
    RIPEMD160: HashDefinition(
        'RIPEMD160',
        160,
        'c81b94933420221a7ac004a90242d8b1d3e5070d'),

    SHA256: HashDefinition(
        'SHA256',
        256,
        '6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d'),

    SHA384: HashDefinition(
        'SHA384',
        384,
        'bec021b4f368e3069134e012c2b4307083d3a9bdd206e24e5f0d86e13d6636655933'
        'ec2b413465966817a9c208a11717'),

    SHA512: HashDefinition(
        'SHA512',
        512,
        'b8244d028981d693af7b456af8efa4cad63d282e19ff14942c246e50d9351d22704a'
        '802a71c3580b6370de4ceb293c324a8423342557d4e5c38438f0e36910ee'),

    SHA224: HashDefinition(
        'SHA224',
        224,
        'fff9292b4201617bdc4d3053fce02734166a683d7d858a7f5f59b073'),
}


def test_hash_algorithms():
    for hash_cls, expected in KNOWN_PROPERTIES.items():
        yield assert_equal, expected.name, hash_cls.serialize()['name']
        yield assert_equal, expected.digest_bits, hash_cls.length.in_bits
        yield assert_equal, expected.zero_hashed, _hash_zero(hash_cls)


def _hash_zero(hash_cls):
    """
    Construct the hash context and update it with a single zero byte.
    """
    hasher = hash_cls.new()
    hasher.update(bytearray([0]))
    return hasher.hexdigest()
