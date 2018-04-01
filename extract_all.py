#!/usr/bin/env python

import os
import json
import subprocess

BASE_PATH = os.path.dirname(__file__)
EXE_PATH = os.path.join(BASE_PATH, 'extract_data.py')
LIST_PATH = os.path.join(BASE_PATH, 'list_specs.py')


def main():
    spec_list = json.loads(subprocess.check_output([LIST_PATH]))

    values = {}
    for spec in spec_list:
        try:
            extract_out = subprocess.check_output([EXE_PATH, str(spec)], stderr=open(os.devnull, 'w'))
            values[spec] = json.loads(extract_out)
        except subprocess.CalledProcessError:
            pass

    print json.dumps(values)


if __name__ == '__main__':
    main()
