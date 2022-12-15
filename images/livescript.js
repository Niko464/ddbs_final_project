sh.addShard("shard1/shardserver1:27018"); 
sh.addShard("shard3/shardserver3:27018,shardserver4:27018");
sh.addShard("shard2/shardserver2:27018")

sh.enableSharding("test")
sh.shardCollection("test.user", {region:1})
sh.disableBalancing("test.user")
sh.splitAt("test.user",{region:"Beijing" })
sh.splitAt("test.user",{region:"Hong Kong" })
sh.moveChunk("test.user",{region:"Beijing" }, "shard1")
sh.moveChunk("test.user",{region:"Hong Kong" }, "shard2")

sh.shardCollection("test.article", {category:1})
sh.disableBalancing("test.article")
sh.splitAt("test.article", { category: "science" })
sh.splitAt("test.article", { category: "technology" })
sh.moveChunk("test.article", { category: "science" }, "shard3")
sh.moveChunk("test.article", { category: "technology" }, "shard2")

sh.shardCollection("test.read", {region:1})
sh.disableBalancing("test.read")
sh.splitAt("test.read", { region: "Beijing" })
sh.splitAt("test.read", { region: "Hong Kong" })
sh.moveChunk("test.read", { region: "Beijing" }, "shard1")
sh.moveChunk("test.read", { region: "Hong Kong" }, "shard2")

sh.shardCollection("test.be-read", {category:1})
sh.disableBalancing("test.be-read")
sh.splitAt("test.be-read", { category: "science" })
sh.splitAt("test.be-read", { category: "technology" })
sh.moveChunk("test.be-read", { category: "science" }, "shard3")
sh.moveChunk("test.be-read", { category: "technology" }, "shard2")