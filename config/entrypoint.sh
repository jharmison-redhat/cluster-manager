#!/bin/bash

trap 'exit' INT

if [ "$DEVEL" ]; then
    echo "Development mode will loop forever and hot reload."
    while true; do
        FLASK_ENV=development entrypoint.py || sleep 1
    done
else
    exec entrypoint.py
fi
