#!/bin/bash

echo "Initializing cluster config in 10 seconds..."
sleep 10

echo "Initializing cluster config..."
mongosh --host config1 --port 27019 --eval \
'rs.initiate({_id : "config", members: [{ _id : 0, host : "config1:27019" }, { _id : 1, host : "config2:27019" }]})';

echo "Initializing shard1..."
mongosh --host shardserver1 --port 27018 --eval \
'rs.initiate({_id : "shard1", members: [{ _id : 0, host : "shardserver1:27018" }]})';

echo "Initializing shard2..."
mongosh --host shardserver2 --port 27018 --eval \
'rs.initiate({_id : "shard2", members: [{ _id : 0, host : "shardserver2:27018" }]})';

echo "Initializing shard3..."
mongosh --host shardserver3 --port 27018 --eval \
'rs.initiate({_id : "shard3", members: [{ _id : 0, host : "shardserver3:27018" }, { _id : 1, host : "shardserver4:27018" }]})';

echo "Initializing router in 10 seconds..."
sleep 10

mongosh --host router --port 27017 --file livescript.js

echo "MongoDB cluster initialized! Sleeping forever..."
echo "You can now connect to the cluster on localhost:27017"

sleep 999999