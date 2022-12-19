sh.addShard("shard1/shardserver1:27018");
sh.addShard("shard3/shardserver3:27018,shardserver4:27018");
sh.addShard("shard2/shardserver2:27018");

sh.enableSharding("test");
sh.shardCollection("test.user", { region: 1 });
sh.disableBalancing("test.user");
sh.splitAt("test.user", { region: "Beijing" });
sh.splitAt("test.user", { region: "Hong Kong" });
sh.moveChunk("test.user", { region: "Beijing" }, "shard1");
sh.moveChunk("test.user", { region: "Hong Kong" }, "shard2");

sh.shardCollection("test.article", { category: 1 });
sh.disableBalancing("test.article");
sh.splitAt("test.article", { category: "science" });
sh.splitAt("test.article", { category: "technology" });
sh.moveChunk("test.article", { category: "science" }, "shard3");
sh.moveChunk("test.article", { category: "technology" }, "shard2");

sh.shardCollection("test.read", { region: 1 });
sh.disableBalancing("test.read");
sh.splitAt("test.read", { region: "Beijing" });
sh.splitAt("test.read", { region: "Hong Kong" });
sh.moveChunk("test.read", { region: "Beijing" }, "shard1");
sh.moveChunk("test.read", { region: "Hong Kong" }, "shard2");

sh.shardCollection("test.beread", { category: 1 });
sh.disableBalancing("test.beread");
sh.splitAt("test.beread", { category: "science" });
sh.splitAt("test.beread", { category: "technology" });
sh.moveChunk("test.beread", { category: "science" }, "shard3");
sh.moveChunk("test.beread", { category: "technology" }, "shard2");

sh.shardCollection("test.popularrank", { temporalGranularity: 1 });
sh.disableBalancing("test.popularrank");
sh.splitAt("test.popularrank", { temporalGranularity: "weekly" });
sh.splitAt("test.popularrank", { temporalGranularity: "monthly" });
sh.moveChunk("test.popularrank", { temporalGranularity: "daily" }, "shard1");
sh.moveChunk("test.popularrank", { temporalGranularity: "weekly" }, "shard2");
sh.moveChunk("test.popularrank", { temporalGranularity: "monthly" }, "shard2");

// https://www.tecmint.com/monitor-mongodb-performance/
db.read.aggregate(
  [
    // Group the documents by "aid" (article ID)
    {
      $group: {
        _id: "$aid",
        readNum: { $sum: 1 }, // Count the number of reads for each article
        readUidList: { $push: "$uid" }, // Collect a list of all the user IDs that have read the article
        commentNum: {
          $sum: { $cond: [{ $eq: ["$commentOrNot", "1"] }, 1, 0] },
        }, // Count the number of comments for each article
        commentUidList: {
          $addToSet: { $cond: [{ $eq: ["$commentOrNot", "1"] }, "$uid", "$noval"] },
        }, // Collect a list of all the user IDs that have commented on the article
        agreeNum: { $sum: { $cond: [{ $eq: ["$agreeOrNot", "1"] }, 1, 0] } }, // Count the number of agrees for each article
        agreeUidList: {
          $addToSet: { $cond: [{ $eq: ["$agreeOrNot", "1"] }, "$uid", "$noval"] },
        }, // Collect a list of all the user IDs that have agreed on the article
        shareNum: { $sum: { $cond: [{ $eq: ["$shareOrNot", "1"] }, 1, 0] } }, // Count the number of shares for each article
        shareUidList: {
          $addToSet: { $cond: [{ $eq: ["$shareOrNot", "1"] }, "$uid", "$noval"] },
        }, // Collect a list of all the user IDs that have shared the article
      },
    },
    // Replace or upsert the documents in the "beRead" collection
    {
      $replaceWith: {
        $mergeObjects: [
          { _id: "$_id", timestamp: new Date() }, // Use the article ID as the _id and set the current timestamp
          "$$ROOT", // Use the rest of the fields from the grouped documents
        ],
      },
    },
    {
      $out: "truc2",
    },
  ],
  { allowDiskUse: true }
);

db.beread.aggregate(
  [
    // Match documents from the current day
    {
      $match: {
        timestamp: {
          $gte: new Date(new Date().setHours(0, 0, 0)),
          $lt: new Date(new Date().setHours(24, 0, 0)),
        },
      },
    },
    // Sort the documents by readNum in descending order
    {
      $sort: { readNum: -1 },
    },
    // Limit the results to the top 5 documents
    {
      $limit: 5,
    },
    // Project only the _id field
    {
      $project: {
        _id: 1,
      },
    },
    // Create a new document with the current timestamp and temporalGranularity set to "daily"
    {
      $replaceWith: {
        _id: new ObjectId(),
        timestamp: new Date(),
        temporalGranularity: "daily",
        articleAidList: "$$ROOT",
      },
    },
    {
      $out: "popularrank",
    },
  ],
  { allowDiskUse: true }
);

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