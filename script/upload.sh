#!/bin/sh -eux

CODE_DIR=$(dirname $0)/../encryptit
VERSION_FILE=${CODE_DIR}/__init__.py


checkout_master() {
    git checkout master
    git pull --ff-only
}

upload_to_pypi() {
	python setup.py sdist upload --sign
}


checkout_master
upload_to_pypi
