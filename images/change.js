// require the mongodb driver
import { MongoClient } from "mongodb";
// Connection URL
const url = "mongodb://localhost:27017";

// Database Name
const dbName = "test";

// Create a new MongoClient
const client = new MongoClient(url);

// Use connect method to connect to the Server
client.connect(function(err) {
    if (err) throw err;
    console.log("Connected successfully to server");

    const db = client.db(dbName);
    const collection = db.collection("read");

    // print the nmeof the collections


    // Create a change stream
    const changeStream = collection.watch([
        {
          $match: {
            operationType: "update"
          }
        },
        {
          $project: {
            fullDocument: 1
          }
        }
      ]);

      changeStream.on("change", function(change) {

        console.log("change", change);
        // Get the updated document
        var doc = change.fullDocument;
      
        // Get the aid (article ID) from the updated document
        var aid = doc.aid;
      
        // Find the corresponding "be-read" document
        var beReadDoc = db.collection("beRead").findOne({ aid: aid });
      
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
        db.collection("beRead").save(beReadDoc);
      });
});
  