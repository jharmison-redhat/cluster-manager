#!/usr/bin/env python
from collections import defaultdict
import os
import yaml


drives_file = os.environ.get('DRIVES_FILE', '/data/drives.yml')


def return_zero():
    return 0


def good_fit(drive):
    if drive.get('type') == 'disk' and drive.get('children') is None:
        return True
    else:
        return False


with open(drives_file) as f:
    data = yaml.safe_load(f)

drives = data.get('drive_data')
use_drives = data.get('use_drives')

if use_drives is None:
    possible_drives = {}
    drive_size_count = defaultdict(return_zero)
    for node in drives:
        possible_drives[node] = []
        for drive in drives[node]:
            if good_fit(drive):
                possible_drives[node].append({
                    'path': '/dev/{}'.format(drive.get('name')),
                    'size': drive.get('size')
                })
                drive_size_count[drive.get('size')] += 1

    most_common_size = max(drive_size_count,
                           key=lambda x: drive_size_count[x])

    use_drives = {}
    drives_per_node = 0
    for node in possible_drives:
        use_drives[node] = []
        for drive in possible_drives[node]:
            if drive['size'] == most_common_size:
                use_drives[node].append(drive['path'])
        use_drives[node].sort()
        if drives_per_node == 0:
            drives_per_node = len(use_drives[node])
        elif drives_per_node != len(use_drives[node]):
            raise RuntimeError(('The number of detected drives per node is not'
                                ' consistent! Please check drives.yml.'))

    with open(drives_file, 'w') as f:
        yaml.safe_dump({
            'drive_data': drives,
            'use_drives': use_drives,
            'drives_per_node': drives_per_node
        }, f)
