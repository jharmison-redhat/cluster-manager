#!/bin/bash

ME=$(dirname $0)

[ -f /data/drives.yml ] || detect drives
python3 $ME/configure.py $@ || exit 1

ansible-playbook $ME/local-storage.yml $@ || exit 1
ansible-playbook $ME/container-storage.yml $@ || exit 1
