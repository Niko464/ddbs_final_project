from hdfs import InsecureClient
import os
from pathlib import Path
import time
import sys


def uploadEntireArticle(hdfsclient, path, articleId):
    # for root, dirs, files in os.walk(f"{path}"):
    #     for file in files:
    local_path = path#os.path.join(root, file)
    hdfs_path = f"/data/articles/{articleId}/"
    print(f"Uploading {local_path} to {hdfs_path}")
    hdfsclient.upload(
        hdfs_path=hdfs_path,
        local_path=local_path,
        overwrite=True,
        n_threads=0,
        cleanup=True,
    )



def main():
    if len(sys.argv) != 2:
        print("Usage: python uploadAllArticles.py <path to data>")
        sys.exit(1)
    hdfsclient = InsecureClient("http://localhost:9870", user="root")
    DATA_FOLDER = sys.argv[1]
    ARTICLES_DIR = f"{DATA_FOLDER}/articles/"

    start = time.time()
    print("Starting...")
    hdfsclient.upload(
        hdfs_path="/data/articles/",
        local_path=ARTICLES_DIR,
        overwrite=True,
        n_threads=256,
        cleanup=True,
    )
    end = time.time()
    print(f"Time taken to upload: {round(end - start, 2)}s")

    

if __name__ == "__main__":
    main()