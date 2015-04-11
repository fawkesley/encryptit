from nose.tools import assert_equal

from ..sample_files import SAMPLE_FILES

from encryptit.__main__ import main

USAGE_MESSAGE = """
Usage:
    encryptit dumpjson <file.gpg>
    encryptit -h | --help
    encryptit --version
""".strip('\n')


def test_help_argument():
    for option in ['-h', '--help']:
        args = [option]
        yield assert_exits_with, None, args


def test_version_argument():
    yield assert_exits_with, None, ['--version']


def test_dumpjson_fails_without_file_argument():
    yield assert_exits_with, USAGE_MESSAGE, ['dumpjson']


def test_dumpjson_succeeds_with_valid_file_argument():
    (_, full_filename) = SAMPLE_FILES[0]
    # Note that None means return code 0 (OK) to sys.exit(...)
    assert_equal(None, main(args=['dumpjson', full_filename]))


def test_invalid_argument_fails():
    yield assert_exits_with, USAGE_MESSAGE, ['foobar']


def assert_exits_with(system_error_code, args):
    try:
        main(args=args)
    except SystemExit as e:
        print(repr(e))
        # assert_equal(system_error_code, e.code)
    else:
        assert False, "Did not raise SystemExit"
