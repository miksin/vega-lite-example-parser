#!/usr/bin/env python

import os
import re
import json

BASE_PATH = os.path.dirname(__file__)
SPEC_PATH = os.path.join(BASE_PATH, 'specs')

def main():
    spec_paths = os.listdir(SPEC_PATH)

    spec_names = []
    for spec_path in spec_paths:
        m = re.match(r'(.*)\.json$', spec_path)
        if m:
            spec_names.append(m.group(1))

    print json.dumps(spec_names)

if __name__ == '__main__':
    main()
