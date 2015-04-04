from .exceptions import InsufficientBytesReadError


def read_bytes(f, size, exception=InsufficientBytesReadError):
    """
    Read exactly `size` bytes from the file object and return a `bytearray`,
    or blow up with an exception.

    Note that the returned `bytearray` is a Python 2/3 compatibility
    improvement as `f.read()[x]` returns a (1-char) string on Py2 and
    an integer on Py3.
    """
    result = f.read(size)
    if len(result) != size:
        raise exception(
            'Tried to read {} bytes, got {}'.format(size, len(result)))
    return bytearray(result)


def seek_relative(f, by):
    assert isinstance(by, int), '{} {}'.format(by, type(by))
    f.seek(by, 1)  # whence=1: current position
