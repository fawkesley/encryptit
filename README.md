# EncryptIt

[![Build Status](https://travis-ci.org/paulfurley/encryptit.svg?branch=master)](https://travis-ci.org/paulfurley/encryptit)

## OpenPGP Passphrase Encryption

EncryptIt is a PGP and GnuPG compatible encryption command-line tool and Python
library for strongly encrypting and decrypting files with passphrases.

This is minimal subset of RFC 4880 (OpenPGP) supporting only **symmetric
(passphrase) encryption**.

The focus is on **testing**, **clean code** and **compatibility**.

## Install

In a virtualenv:

    ```shell
    mkdir -p ~/venv && virtualenv ~/venv/encryptit
    pip install encrypit
    ```

For your local user only:

    ```shell
    pip install --user encryptit
    ```

Globally (not recommended):

    ```shell
    sudo pip install encrypit
    ```

## Encrypt a File

### Python API

    ```python
    from encryptit import encrypt_symmetric, make_passphrase

    from cleancrypt import encrypt_symmetric, generate_passphrase

    with open('diary.zip', 'rb') as f, open('diary.zip.gpg', 'wb') as g:
        passphrase = generate_passphrase()
        openpgp_message = encrypt_symmetric(f.read(), passphrase)
        g.write(openpgp_message)
    ```

### Command-line

    ```shell
    $ encryptit encrypt diary.zip --output diary.zip.gpg
    ```

### Technical Detail

 - `SymmetricKeyEncryptedSessionKeyPacket` with parameters:

   - `SaltedAndIteratedS2K` string-to-key method using SHA1 hash
   - `AES256` symmetric cipher
   - empty `encrypted session key` (session key is derived directly from
     passphrase)

 - `SymmetricEncryptedandIntegrityProtectedDataPacket`

### GnuPG equivalent

    ```shell
    $ gpg --symmetric diary.zip
    ```

## Decrypt a File

### Python API

    ```python
    from cleancrypt import decrypt_symmetric

    with open('diary.zip.gpg', 'rb') as f, open('diary.zip', 'wb') as g:
        passphrase = 'something stronger than this'
        plaintext = decrypt_symmetric(f.read(), passphrase)
        g.write(plaintext)
    ```

### Command-line

    ```shell
    $ encryptit decrypt diary.zip.gpg --output diary.zip
    ```

### GnuPG equivalent

    ```shell
    gpg diary.zip.gpg
    ```

### Technical Detail

1. Decodes a `SymmetricKeyEncryptedSessionKeyPacket` to derive the session
2. Decodes and decrypts a `SymmetricallyEncryptedDataPacket` or a
   `SymmetricEncryptedandIntegrityProtectedDataPacket`
3. Performs message integrity checking for packet types that support it.
4. Decodes decrypted `LiteralDataPacket` or `CompressedDataPacket`.

## Current Status (April 2015)

- Alpha (API Design)
- Active (but part-time) development.
- **Comments welcome on the API design!**

## Ambition

*To be the cleanest, most testable OpenPGP implementation.*

- Clean, helpful Pythonic API.
- Friendly and familiar command-line tools.
- CPython 2.6+, 3.2+ support, PyPy 2.7+, 3.2+ support.
- Very obvious code layout and implementation.
- Extremely high test coverage (at the expense of functionality).
- [PEP8](https://www.python.org/dev/peps/pep-0008/) compliant.

## Roadmap

- 0.1.0 `dumpjson` tool and API call

  - basic serialisation of *all* packet types
  - output will improve as packet serialization is extended

- 0.2.0 decode a standard configuration of a symmetrically encrypted file

  - single symmetric passphrase, no asymmetric encryption
  - `SaltedAndIteratedS2K`
  - `SHA1` hash.
  - `AES256` cipher.
  - `LiteralDataPacket` containing binary data.
  - Test suite for above packet types.

- 0.3.0 decode all symmetrically encrypted file variations

  - single symmetric passphrase, no asymmetric encryption
  - all S2K types
  - all iteration possibilities
  - all hash algorithms
  - all ciphers
  - all data packet types
  - test suite for above

- 0.4.0 decode symmetrically encrypted file which are also public-key encrypted

  - support file encrypted by 1x passphrase and 1x public key

- ...

- 1.0.0 symmetric encrypt/decrypt API and CLI


## Dual License: Affero GNU Public Licence v3

Copyright (C) 2015 Paul M Furley [paul@paulfurley.com](mailto:paul@paulfurley.com)

[GNU Affero Public License Version 3](https://www.gnu.org/licenses/agpl-3.0.html).

[Quick Summary of AGPLv3](https://tldrlegal.com/license/gnu-affero-general-public-license-v3-%28agpl-3.0%29)

**Dual-licensing outside AGPL is possible. Please email me to discuss.**

In order to be reliable, well tested and well supported, all software needs an
income stream.

## Other Python OpenPGP Efforts

EncryptIt focuses on a *well-tested subset* of OpenPGP.

For more funcionality, see these other projects (my initial thoughts included
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



