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

// missing popular rank collection
/*
db.getSiblingDB("test").createTrigger({
    update: "read",
    after: function(updateObject) {
      // Get the ID of the updated document
      var docId = updateObject.documentKey._id;
  
      // Get the updated document
      var doc = db.read.findOne({ _id: docId });
  
      // Get the aid (article ID) from the updated document
      var aid = doc.aid;
  
      // Find the corresponding "be-read" document
      var beReadDoc = db.beRead.findOne({ aid: aid });
  
      // If the "be-read" document doesn't exist, create it
      if (!beReadDoc) {
        beReadDoc = {
          aid: aid,
          readNum: 0,
          readUidList: [],
          commentNum: 0,
          commentUidList: [],
          agreeNum: 0,
          agreeUidList: [],
          shareNum: 0,
          shareUidList: []
        };
      }
  
      // Increment the readNum field in the "be-read" document
      beReadDoc.readNum++;
  
      // Add the uid from the updated "read" document to the readUidList
      beReadDoc.readUidList.push(doc.uid);
  
      // If the updated "read" document has a comment, increment the commentNum field
      // and add the uid to the commentUidList
      if (doc.commentOrNot) {
        beReadDoc.commentNum++;
        beReadDoc.commentUidList.push(doc.uid);
      }
  
      // If the updated "read" document has an agree, increment the agreeNum field
      // and add the uid to the agreeUidList
      if (doc.aggreeOrNot) {
        beReadDoc.agreeNum++;
        beReadDoc.agreeUidList.push(doc.uid);
      }
  
      // If the updated "read" document has a share, increment the shareNum field
      // and add the uid to the shareUidList
      if (doc.shareOrNot) {
        beReadDoc.shareNum++;
        beReadDoc.shareUidList.push(doc.uid);
      }
  
      // Save the updated "be-read" document
      db.beRead.save(beReadDoc);
    }
  });
  */