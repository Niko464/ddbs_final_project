import sys
import pymongo
from hdfs import InsecureClient
import shutil
import os
from bson import ObjectId
import time

ARTICLE_NAME = "article"
hdfsclient = InsecureClient("http://localhost:9870", user="root")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def downloadEntireArticle(hdfsclient, path, articleId):
    local_path = path + str(articleId)
    #if the path exists, remove it
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    hdfs_path = f"/data/articles/{articleId}/"
    print(f"Downloading {hdfs_path} to {local_path}")
    hdfsclient.download(
        hdfs_path=hdfs_path,
        local_path=local_path,
        overwrite=True,
    )

def logError(msg):
	print(bcolors.FAIL + "ERROR " + msg + bcolors.ENDC)

def logInfo(msg):
	print(bcolors.WARNING + "INFO " + msg + bcolors.ENDC)

def hasEnoughArgs(numArgs, missingName, cmdName):
    if len(sys.argv) < numArgs:
        logError(f"Missing {missingName} argument")
        printGeneralUsage(cmdName)
        return False
    return True

def printGeneralUsage(level=None):
    CMD = "python app.py"
    if level == None:
        logInfo(f"Usage: {CMD} <'query' | 'update' | 'insert'>")
    if level == "query":
        logInfo(f"Usage: {CMD} query <tableName> <id>")
        logInfo("<tableName>: 'user' | 'read' | 'article' | 'be-read' | 'popular'")
        logInfo("<id>: the id of the user, read, article, etc")
    if level == "update":
        logInfo(f"Usage: {CMD} update <tableName> <id>")
        logInfo("<tableName>: 'user' | 'article'")
        logInfo("<id>: the id of the user or article")
    if level == "insert":
        logInfo(f"Usage: {CMD} insert read <userid> <articleid> <timestamp>")

def handleUserQuery(db):
    if hasEnoughArgs(4, "user id", "query") == False:
        return
    user = db.user.find_one({"uid": sys.argv[3]})
    if user == None:
        logError("No user found with that uid")
        return
    print("The requested user:")
    print(user)

def handleReadQuery(db):
    if hasEnoughArgs(4, "user id", "query") == False:
        return
    read = db.read.find_one({"uid": sys.argv[3]})
    if read == None:
        logError("No read found with that uid")
        return
    print("The requested read:")
    print(read)

def handleArticleQuery(db):
    if hasEnoughArgs(4, "article id", "query") == False:
        return
    article = db.article.find_one({"aid": sys.argv[3]})
    if article == None:
        logError("No article found with that aid")
        return
    print("The requested article:")
    print(article)
    print("Downloading the article's content...")
    downloadEntireArticle(hdfsclient, "./", ARTICLE_NAME + str(article["aid"]))
    print("The article's content:")
    with open(f"./{ARTICLE_NAME}{article['aid']}/" + article["text"], "r") as f:
        print(f.read())
    print("You can also go check out the article's media content that we downloaded at the following path:")
    print(f"./{ARTICLE_NAME}{article['aid']}")
    


def handleBeReadQuery(db):
    if hasEnoughArgs(4, "article id", "query") == False:
        return
    beRead = db.beread.find_one({"aid": sys.argv[3]})
    if beRead == None:
        logError("No beRead found with that aid")
        return
    print("The requested beRead:")
    print(beRead)

def handlePopularQuery(db):
    if hasEnoughArgs(5, "timestamp or granularity", "query") == False:
        return
    popular = db.popularrank.find_one({ "timestamp": sys.argv[3], "granularity": sys.argv[4]})
    if popular == None:
        logError("No popular found with that timestamp and granularity")
        return
    print("The requested popular articles:")
    for aid in popular["articleAidList"]:
        article = db.article.find_one({"aid": aid})
        print(article)



def handleUpdateUser(db):
    if hasEnoughArgs(4, "user id", "update") == False:
        return
    currentUser = db.user.find_one({"_id": ObjectId(sys.argv[3])})
    if currentUser == None:
        logError("No user found with that uid")
        return
    user = db.user.update_one({"_id": ObjectId(sys.argv[3])}, {"$set": {sys.argv[4]: sys.argv[5]}})
    print(f"Updated the user's region from {currentUser[sys.argv[4]]} to {sys.argv[5]}")

def handleUpdateArticle(db):
    if hasEnoughArgs(4, "article id", "update") == False:
        return
    currentArticle = db.article.find_one({"_id": ObjectId(sys.argv[3])})
    if currentArticle == None:
        logError("No article found with that aid")
        return
    article = db.article.update_one({"_id": ObjectId(sys.argv[3])}, {"$set": {sys.argv[4]: sys.argv[5]}})
    print(f"Updated the article's category from {currentArticle[sys.argv[4]]} to {sys.argv[5]}")



def handleInsertRead(db):
    if hasEnoughArgs(5, "user id or article id", "insert") == False:
        return
    ts = int(time.time() * 1000)
    read = db.read.insert_one({
        "uid": sys.argv[3],
        "aid": sys.argv[4],
        "timestamp": ts,
        "readTimeLength": "75",
        "agreeOrNot": "0",
        "commentOrNot": "0",
        "shareOrNot": "0",
        "commentDetail": "comments to this article: (456,2865)"
    })
    print(f"Inserted read with uid {sys.argv[3]}, aid {sys.argv[4]}, and timestamp {ts}")


def main():
    queryTypes = {
        "query": {
            "user": handleUserQuery,
            "read": handleReadQuery,
            "article": handleArticleQuery,
            "be-read": handleBeReadQuery,
            "popular": handlePopularQuery
        },
        "update": {
            "user": handleUpdateUser,
            "article": handleUpdateArticle
        },
        "insert": {
            "read": handleInsertRead
        }
    }
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient["test"]

    if len(sys.argv) < 2:
        printGeneralUsage()
        return
    command = sys.argv[1]
    if command not in queryTypes:
        logError(f"Invalid command: {command}")
        printGeneralUsage()
        return
    if len(sys.argv) < 3:
        printGeneralUsage(command)
        return
    tableName = sys.argv[2]
    if tableName not in queryTypes[command]:
        logError(f"Invalid tableName: {tableName}")
        printGeneralUsage(command)
        return
    queryTypes[command][tableName](db)


if __name__ == "__main__":
	main()