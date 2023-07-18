#!/usr/bin/env python3
'''Write a Python script that provides some stats about Nginx logs stored in MongoDB:

Database: logs
Collection: nginx
Display (same as the example):
first line: x logs where x is the number of documents in this collection
second line: Methods:
5 lines with the number of documents with the method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
in this order (see example below - warning: it’s a tabulation before each line)
one line with the number of documents with:
method=GET
path=/status
You can use this dump as data sample: dump.zip
'''

import pymongo
from pymongo import MongoClient


def log_nginx_stats(mongo_collection):
    '''provides some stats about Nginx logs stored in MongoDB'''
    # client = MongoClient('mongodb://localhost:27017')
    print("{} logs".format(mongo_collection.count_documents({})))

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        print("\tmethod {}: {}".format(
            method, mongo_collection.count_documents({"method": method})))

    print("{} status check".format(mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})))


if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017')
    nginx_collection = client.logs.nginx
    log_nginx_stats(nginx_collection)
