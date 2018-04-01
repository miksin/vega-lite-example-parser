#!/usr/bin/env python

import os
import json
import csv
from sys import argv


BASE_PATH = os.path.dirname(__file__)
SPEC_PATH = os.path.join(BASE_PATH, 'specs')

def get_data(spec):
    if spec['data'].has_key('values'):
        return spec['data']['values']

    elif spec['data'].has_key('url'):
        data_path = spec['data']['url']
        with open(os.path.join(BASE_PATH, data_path), 'rb') as f:
            if data_path[-5:] == '.json':
                return json.load(f)
            if data_path[-4:] == '.csv':
                reader = csv.DictReader(f)
                return [record for record in reader]

    return []


def get_values(spec, data):
    col_info = spec['encoding']

    values = {}
    for col, info in col_info.items():
        if info.has_key('field'):
            values[col] = []
            for record in data:
                values[col].append(record[info['field']])

    return values


def filter_data(spec, data):
    cols = []
    new_data = []

    for col, info in spec['encoding'].items():
        if info.has_key('field'):
            cols.append(info['field'])

    for row in data:
        new_row = {k: v for k, v in row.items() if k in cols}
        new_data.append(new_row)

    return new_data



def main():
    if len(argv) < 2:
        print 'usage: python {} <spec-name>'.format(argv[0])
        exit(1)

    spec_path = os.path.join(SPEC_PATH, argv[1])
    if argv[1][-5:] != '.json':
        spec_path = os.path.join(SPEC_PATH, argv[1] + '.json')

    with open(spec_path) as f:
        spec = json.load(f)
        data = get_data(spec)
        #values = get_values(spec, data)
        values = filter_data(spec, data)

        print json.dumps(values)


if __name__ == '__main__':
    main()
