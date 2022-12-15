#!/bin/bash


mongosh --host config1 --port 27019 --eval \
'rs.initiate({_id : "configsvr", members: [{ _id : 0, host : "config1:27019" }, { _id : 1, host : "config2:27019" }]})';

mongosh --host shardserver1 --port 27018 --eval \
'rs.initiate({_id : "shard1", members: [{ _id : 0, host : "shardserver1:27018" }]})';

mongosh --host shardserver2 --port 27018 --eval \
'rs.initiate({_id : "shard2", members: [{ _id : 0, host : "shardserver2:27018" }]})';

mongosh --host shardserver3 --port 27018 --eval \
'rs.initiate({_id : "shard3", members: [{ _id : 0, host : "shardserver3:27018" }, { _id : 1, host : "shardserver4:27018" }]})';

mongosh --host router --port 27017 --eval \
'sh.addShard("configsvr/config1:27019,config2:27019"); sh.addShard("shard1/shardserver1:27018"); sh.addShard("shard3/shardserver3:27018,shardserver4:27018"); sh.addShard("shard2/shardserver2:27018")';


sleep 999999