from hdfs import InsecureClient
import os
from pathlib import Path
import time

def uploadEntireArticle(hdfsclient, path, articleId):
    for root, dirs, files in os.walk(f"{path}"):
        for file in files:
            local_path = os.path.join(root, file)
            hdfs_path = f"/data/articles/{articleId}/" + file
            print(f"Uploading {local_path} to {hdfs_path}")
            hdfsclient.upload(
                hdfs_path=hdfs_path,
                local_path=local_path,
                overwrite=True,
            )



def main():
    hdfsclient = InsecureClient("http://localhost:9870", user="root")
    DATA_FOLDER = "../data/"
    ARTICLES_DIR = f"{DATA_FOLDER}/articles/"

    start = time.time()
    files_and_directories = os.listdir(ARTICLES_DIR)
    for item in files_and_directories:
        path = os.path.join(ARTICLES_DIR, item)
        if os.path.isdir(path):
            uploadEntireArticle(hdfsclient, path, item)
    end = time.time()
    print(f"Time taken to upload: {round(end - start, 2)}s")

    

if __name__ == "__main__":
    main()