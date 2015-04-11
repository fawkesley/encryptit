# encoding: utf-8

from setuptools import setup, find_packages

import codecs
import os
import re


try:
    # Workaround for https://bugs.python.org/issue15881#msg170215
    # See: https://groups.google.com/forum/#!topic/nose-users/fnJ-kAUbYHQ
    # If this can be removed and the tests pass on Python 2.6, hooray!
    import multiprocessing
except ImportError:
    pass
else:
    del multiprocessing


def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    here = os.path.abspath(os.path.dirname(__file__))

    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

VERSION = find_version('encryptit', '__init__.py')


def get_install_requires():
    dependencies = ['docopt', 'pycrypto', 'six']
    try:
        from collections import OrderedDict  # Python 2.6 doesn't have it.
        OrderedDict  # To prevent unused PEP8 error :)
    except ImportError:
        dependencies.append('ordereddict')

    try:
        from enum import Enum
        Enum  # Prevent unused PEP8 error
    except ImportError:
        dependencies.append('enum34')

    return dependencies

setup(
    name='encryptit',
    packages=find_packages(),
    version=VERSION,
    description='OpenPGP API and CLI focusing on testing & clarity.',
    author='Paul M Furley',
    author_email='paul@paulfurley.com',
    url='https://github.com/paulfurley/encryptit',
    download_url=('https://github.com/paulfurley/encryptit/tarball/{0}'
                  .format(VERSION)),
    install_requires=get_install_requires(),
    entry_points={
        'console_scripts': [
            'encryptit=encryptit.__main__:main',
        ],
    },
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
