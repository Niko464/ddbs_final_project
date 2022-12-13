# DDBS Project

Final project for the Distributed Database Systems course at Tsinghua University 2022.

# Authors

Octopus773

Niko464

# start the cluster
docker-compose up -d

# connect to the router
docker exec -it mongo_router_1 mongo

# create the sharding
sh.addShard("shard1/localhost:27018")
sh.addShard("shard2/localhost:27019")
sh.addShard("shard3/localhost:27020")

# enable sharding on a database
sh.enableSharding("mydb")

# enable sharding on a collection
sh.shardCollection("mydb.myCollection", { "myField": "hashed" } )

# verify that the sharding is enabled
sh.status()

# check the number of shards
db.myCollection.getShardDistribution()

# split the collection in 2 shards
sh.splitAt("mydb.myCollection", { "myField": 1 })

# move the collection to a specific