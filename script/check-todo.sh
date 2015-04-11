#!/bin/sh

grep -Rin --exclude=*.pyc TODO encryptit/

EXITCODE=$?

if [ "$EXITCODE" = "0" ]; then
    echo "FAIL: Found one or more TODO entries."
    exit 1

elif [ "$EXITCODE" = "1" ]; then
    echo "OK"
    exit 0

else
    echo "Error running grep."
    exit 1
fi
