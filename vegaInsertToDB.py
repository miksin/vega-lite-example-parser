#!/usr/bin/env python

import os
import json
import subprocess
from pymongo import MongoClient

BASE_PATH = os.path.dirname(__file__)
EXE_PATH = os.path.join(BASE_PATH, 'extract_data.py')
LIST_PATH = os.path.join(BASE_PATH, 'list_specs.py')
SPEC_PATH = os.path.join(BASE_PATH, 'specs')

DB_URI = 'mongodb://localhost:27017/'
DB_NAME = 'data_recommendation'
CO_NAME = 'example_data'

def main():
    client = MongoClient(DB_URI)
    db = client[DB_NAME]
    collection = db[CO_NAME]

    print 'ready to insert, count: {}'.format(collection.find().count())

    spec_list = json.loads(subprocess.check_output([LIST_PATH]))

    for spec in spec_list:
        try:
            spec_path = os.path.join(SPEC_PATH, str(spec))
            if str(spec)[-5:] != '.json':
                spec_path = os.path.join(SPEC_PATH, str(spec) + '.json')
            
            template = str(open(spec_path, 'rb').read())
            extract_out = subprocess.check_output([EXE_PATH, str(spec)], stderr=open(os.devnull, 'w'))
            data_point = json.loads(extract_out)

            insert_obj = {
                "name": str(spec),
                "source": "vega-lite",
                "template": template,
                "data": data_point,
            }

            record_id = collection.insert_one(insert_obj).inserted_id
            print 'insert object {} id: {}'.format(str(spec), record_id)

        except subprocess.CalledProcessError:
            pass

    print 'complete, count: {}'.format(collection.find().count())


if __name__ == '__main__':
    main()
