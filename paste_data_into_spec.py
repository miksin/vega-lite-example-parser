#!/usr/bin/env python

import os
import json
import subprocess

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
EXE_PATH = os.path.join(BASE_PATH, 'extract_data.py')
LIST_PATH = os.path.join(BASE_PATH, 'list_specs.py')
SPEC_PATH = os.path.join(BASE_PATH, 'specs')
EXAMPLE_PATH = os.path.join(BASE_PATH, 'examples')


def main():
    spec_list = json.loads(subprocess.check_output([LIST_PATH]))
    success_list = []
    failed_list = []

    for spec in spec_list:
        try:
            spec_path = os.path.join(SPEC_PATH, str(spec))
            if str(spec)[-5:] != '.json':
                spec_path = os.path.join(SPEC_PATH, str(spec) + '.json')
            
            template = json.load(open(spec_path, 'rb'))
            extract_out = subprocess.check_output([EXE_PATH, str(spec)], stderr=open(os.devnull, 'w'))
            data_point = json.loads(extract_out)

            if template[u'data'].has_key(u'url'):
                template[u'data'][u'values'] = data_point
                template[u'data'].pop(u'url', None)
            
            ex_path = os.path.join(EXAMPLE_PATH, str(spec))
            if str(spec)[-5:] != '.json':
                ex_path = os.path.join(EXAMPLE_PATH, str(spec) + '.json')
            
            with open(ex_path, 'wb') as f:
                f.write(json.dumps(template))
            
            print 'Write: {}'.format(spec)
            success_list.append(spec)

        except:
            print 'Failed: {}'.format(spec)
            failed_list.append(spec)

    print 'finish, success: {}, failed: {}'.format(len(success_list), len(failed_list))


if __name__ == '__main__':
    main()
