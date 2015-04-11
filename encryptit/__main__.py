# encoding: utf-8

"""
EncryptIt

  Usage:
    encryptit dumpjson <file.gpg>
    encryptit -h | --help
    encryptit --version

  Options:
    -h --help   Show this screen.
"""

from __future__ import unicode_literals

from docopt import docopt

from .cli import dump_json


def main(args=None):
    if args is None:
        import sys
        args = sys.argv[1:]

    from .__init__ import __version__

    version_string = (
        'EncryptIt {0}\n'
        'Copyright © 2015 Paul M Furley <paul@paulfurley.com>\n'
        'License AGPLv3: GNU Affero Public License version 3 '
        '<http://gnu.org/licenses/agpl.html>\n'
        'This is free software: you are free to change and redistribute it.\n'
        'There is NO WARRANTY, to the extend permitted by law.').format(
            __version__)

    arguments = docopt(__doc__, version=version_string, argv=args)
    if arguments['dumpjson'] is True:
        return dump_json(arguments['<file.gpg>'])
