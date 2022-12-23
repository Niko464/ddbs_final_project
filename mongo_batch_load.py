
# Description: This script loads a file into a mongo collection

import pymongo
import json
import sys
import time


def main():
    connection_string = sys.argv[1] if len(
        sys.argv) > 1 else 'mongodb://localhost:27017/'
    data_folder = sys.argv[2] if len(
        sys.argv) > 2 else '/home/cbihan/db-generation'
    db = None
    try:
        client = pymongo.MongoClient(
            connection_string, serverSelectionTimeoutMS=2000, connect=True)
        client.server_info()
        db = client['test']
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(err)
        sys.exit(1)

    start = time.time()
    #batch_load_into_db(db, data_folder)
    print(f"Batch load into db took {time.time()-start} seconds")
    start = time.time()
    generate_be_read(db)
    print(f"Generate be read took {time.time()-start} seconds")
    start = time.time()
    #generate_popular_rank(db)
    print(f"Generate popular rank took {time.time()-start} seconds")
    print("Done")


def batch_load_into_db(db, data_folder):
    batch = []
    for name in ["user", "read", "article"]:
        print(f"Loading {name} into mongo")
        start_time = time.time()
        file_lines = open(f'{data_folder}/{name}.dat').readlines()
        batch_size = max(5000, len(file_lines)//10)
        for line in file_lines:
            l = json.loads(line)
            batch.append(l)
            if len(batch) == batch_size:
                db[name].insert_many(batch, ordered=False)
                batch = []
        if len(batch) > 0:
            db[name].insert_many(batch, ordered=False)
            batch = []
        end_time = time.time()
        print(f"Loaded {name} into mongo in {end_time-start_time} seconds")


def generate_be_read(db):
    db["read"].aggregate(
        [
            {
                "$group": {
                    "_id": "$aid",
                    "readNum": {"$sum": 1},
                    "readUidList": {"$push": "$uid"},
                    "commentNum": {
                        "$sum": {"$cond": [{"$eq": ["$commentOrNot", "1"]}, 1, 0]},
                    },
                    "commentUidList": {
                        "$addToSet": {"$cond": [{"$eq": ["$commentOrNot", "1"]}, "$uid", "$noval"]},
                    },
                    "agreeNum": {"$sum": {"$cond": [{"$eq": ["$agreeOrNot", "1"]}, 1, 0]}},
                    "agreeUidList": {
                        "$addToSet": {"$cond": [{"$eq": ["$agreeOrNot", "1"]}, "$uid", "$noval"]},
                    },
                    "shareNum": {"$sum": {"$cond": [{"$eq": ["$shareOrNot", "1"]}, 1, 0]}},
                    "shareUidList": {
                        "$addToSet": {"$cond": [{"$eq": ["$shareOrNot", "1"]}, "$uid", "$noval"]},
                    },
                }
            },
            {
                "$replaceWith": {
                    "$mergeObjects": [
                        {"_id": "$_id", "timestamp": "$$NOW" },
                        "$$ROOT",
                    ]
                }
            },
            { "$merge": { "into": "beread" }}
        ],
        allowDiskUse=True
    )
    print("Done generating be read")


def generate_popular_rank(db):
    for granularity in [('%Y-%m', 'monthly'), ('%Y-w%U', 'weekly'), ('%Y-%m-%d', 'daily')]:
        db.read.aggregate([
            {"$group": {
                "_id": {"id": "$aid", "date": {"$dateToString": {"format": granularity[0], "date": {"$toDate": {"$toLong": "$timestamp"}}}}},
                "count": {"$sum": 1}}},
            {"$addFields": {
                "temporalGranularity": granularity[1]}},
            {"$sort": {
                "count": -1,
            }},
            {"$merge": {
                "into": "popularrank"}}
        ], allowDiskUse=True)
    print("Done generating popular rank")

if __name__ == '__main__':
    sys.exit(main())
