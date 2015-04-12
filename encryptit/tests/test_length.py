from nose.tools import assert_equal, assert_raises

from encryptit.length import Length


def test_length_in_octets():
    l = Length(octets=10)
    assert_equal(10, l.in_octets)
    assert_equal(10 * 8, l.in_bits)


def test_length_in_bits():
    l = Length(bits=80)
    assert_equal(10, l.in_octets)
    assert_equal(10 * 8, l.in_bits)


def test_length_in_bits_must_be_multiple_of_8():
    for bits in [1, 2, 3, 4, 5, 6, 7]:
        yield assert_raises, ValueError, lambda: Length(bits=bits)


def test_both_bits_and_octets_cannot_be_given():
    assert_raises(ValueError, lambda: Length(octets=8, bits=80))


def test_serialize():
    assert_equal(
        {
            'bits': 80,
            'octets': 10
        },
        Length(octets=10).serialize()
    )
