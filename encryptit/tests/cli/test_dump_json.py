import json

import mock
from six import StringIO

from ..sample_files import SAMPLE_FILES

from encryptit.cli.dump_json import dump_json


def test_that_dump_json_opens_file_and_write_valid_json_to_stream():
    for _, full_filename in SAMPLE_FILES:
        yield check_can_open_file, full_filename


def check_can_open_file(full_filename):
    with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        dump_json(full_filename)
        mock_stdout.seek(0)

        data = json.loads(mock_stdout.read())
        assert 'packets' in data
