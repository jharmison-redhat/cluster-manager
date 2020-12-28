#!/bin/bash

if [ "$1" != "cat" ] && [ "$1" != "ls" ] && [ "$1" != "type" ]; then
    source /app/bin/shim-check.sh
fi

eval $@
