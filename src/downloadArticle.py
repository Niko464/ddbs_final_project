from hdfs import InsecureClient
import os
import time
import sys

def downloadEntireArticle(hdfsclient, path, articleId):
    local_path = "./" + str(articleId)
    hdfs_path = f"/data/articles/{articleId}/"
    print(f"Downloading {hdfs_path} to {local_path}")
    hdfsclient.download(
        hdfs_path=hdfs_path,
        local_path=local_path,
        overwrite=True,
    )

def main():
    hdfsclient = InsecureClient("http://localhost:9870", user="root")

    if len(sys.argv) < 2:
        print("Usage: python downloadArticle.py <articleId>")
        sys.exit(1)
    start = time.time()
    downloadEntireArticle(hdfsclient, "./", "article" + str(sys.argv[1]))
    end = time.time()
    print(f"Time taken to download: {round(end - start, 2)}s")

    

if __name__ == "__main__":
    main()