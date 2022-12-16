
# Description: This script loads a file into a mongo collection

import pymongo
import json
import sys, time


batch_size=1000

try:
    client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000, connect=True)
    client.server_info() # force connection on a request as the
                         # connect=True parameter of MongoClient seems
                         # to be useless here 
except pymongo.errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    print(err)
    sys.exit(1)

db = client['test']

batch=[]
for name in ["user","read","article"]:
    print(f"Loading {name} into mongo")
    start_time = time.time()
    for line in open(f'/home/cbihan/db-generation/{name}.dat').readlines():
        l=json.loads(line)
        batch.append(l)
        if len(batch)==batch_size:
            db[name].insert_many(batch)
            batch=[]
    if len(batch)>0:
        db[name].insert_many(batch)
        batch = []
    end_time = time.time()
    print(f"Loaded {name} into mongo in {end_time-start_time} seconds")