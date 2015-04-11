# EncryptIt

[![Build Status](https://travis-ci.org/paulfurley/encryptit.svg?branch=master)](https://travis-ci.org/paulfurley/encryptit)
[![Coverage Status](https://coveralls.io/repos/paulfurley/encryptit/badge.svg)](https://coveralls.io/r/paulfurley/encryptit)
[![Latest Version](https://pypip.in/version/encryptit/badge.svg)](https://pypi.python.org/pypi/encryptit/)
[![Supported Python versions](https://pypip.in/py_versions/encryptit/badge.svg)](https://pypi.python.org/pypi/encryptit/)
[![Development Status](https://pypip.in/status/encryptit/badge.svg)](https://pypi.python.org/pypi/encryptit/)
[![Supported Python implementations](https://pypip.in/implementation/encryptit/badge.svg)](https://pypi.python.org/pypi/encryptit/)

## OpenPGP API and CLI for Python

EncryptIt an [OpenPGP (RFC 4880)](https://tools.ietf.org/html/rfc4880) API and
CLI for Python, focusing on **testing and clarity**.

- *Currently* it provides a debugging tool, `encryptit dumpjson` which converts
OpenPGP binary messages into extremely verbose JSON. As decoders for individual [packet
types](https://tools.ietf.org/html/rfc4880#section-5) are added, the `dumpjson`
tool will become even more powerful.

- *Next* it will provide an API and CLI for **symmetrically encrypting and
decrypting files** using a passphrase.

- *Eventually* (and depending how it goes) we'll tackle **asymmetric (public / private key) encryption.**

See [milestones](https://github.com/paulfurley/encryptit/milestones) for more detail.


# Quickstart

## Install

It's Python, so you probably want to use a [virtualenv](https://virtualenv.pypa.io/en/latest/), then:

```sh
$ pip install encryptit
```

## Decode an OpenPGP binary file

```sh
# Create an encrypted file with GPG
$ echo "secret message" | gpg --symmetric /tmp/encrypted.gpg

# Decode with encryptit
$ encryptit dumpjson /tmp/encrypted.gpg
```

## Goals / Ambitions

*To be the cleanest, most testable OpenPGP implementation.*

- Clean, helpful Pythonic API.
- Friendly and familiar command-line tools.
- CPython 2.6+, 3.2+ support, PyPy 2.7+, 3.2+ support.
- Very obvious code layout and implementation.
- Extremely high test coverage (at the expense of functionality).
- [PEP8](https://www.python.org/dev/peps/pep-0008/) compliant.


## Software Licence: GNU Affero Public Licence v3

Copyright (C) 2015 Paul M Furley [paul@paulfurley.com](mailto:paul@paulfurley.com)

[GNU Affero Public License Version 3](https://www.gnu.org/licenses/agpl-3.0.html).

[Quick Summary of AGPLv3](https://tldrlegal.com/license/gnu-affero-general-public-license-v3-%28agpl-3.0%29)

**Proprietary re-licensing may be possible: please [email me to discuss](mailto:paul@paulfurley.com).**

## Other Python OpenPGP Efforts

Currently EncryptIt sacrifices functionality in favour of testing & reliability.

For more functionality, see these other projects (my initial thoughts included
alongside).

Updated 2015-05-02.

- [PGPy](https://github.com/SecurityInnovation/PGPy)

  - lots of functionality
  - TODO : look more into this one

- [OpenPGP-Python](https://github.com/singpolyma/OpenPGP-Python)

  - Lots of functionality.
  - MIT licence.
  - Quite a lot of tests, but unclear whether they're covering key things?
  - How to install?
  - Not PEP8 compliant.

- [python-pgp](https://github.com/mitchellrj/python-pgp)

  - Lots of functionality - awesome!
  - GPLv3 licence.
  - Very sparse testing (dealbreaker).
  - Existing tests currently failing on `master`
  - No Python 2 support.
  - Not PEP8 compliant.

- [OpenPGP](https://pypi.python.org/pypi/OpenPGP) [code](https://bitbucket.org/sourpoi/python-openpgp-2440/)

  - Implements obsolete RFC 2440.
  - Last updated 2005.
  - "Entertainment only"
  - No Python 3 support.
  - Source control is mercurial.
  - TODO: PEP8 compliant?
