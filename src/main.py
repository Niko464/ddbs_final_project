from hdfs import InsecureClient
import os
from pathlib import Path

def uploadEntireArticle(hdfsclient, path, articleId):
    for root, dirs, files in os.walk(f"{path}/article{articleId}"):
        for file in files:
            local_path = os.path.join(root, file)
            hdfs_path = f"/data/articles/article{articleId}/" + file
            print(f"Uploading {local_path} to {hdfs_path}")
            hdfsclient.upload(
                hdfs_path=hdfs_path,
                local_path=local_path,
                overwrite=True,
            )

def downloadEntireArticle(hdfsclient, path, articleId):
    for root, dirs, files in os.walk(f"{path}/article{articleId}"):
        for file in files:
            local_path = "./article" + str(articleId) + "/"
            Path(local_path).mkdir(parents=True, exist_ok=True)
            hdfs_path = f"/data/articles/article{articleId}/" + file
            print(f"Downloading {hdfs_path} to {local_path}")
            hdfsclient.download(
                hdfs_path=hdfs_path,
                local_path=local_path,
                overwrite=True,
            )
    

def main():
    hdfsclient = InsecureClient("http://localhost:9870", user="root")
    # for i in range(2):
    #     uploadEntireArticle(hdfsclient, "../data/articles/", i)

    for i in range(2):
        downloadEntireArticle(hdfsclient, "../data/articles/", i)
    

if __name__ == "__main__":
    main()