#!/usr/bin/env python3
'''Improve 12-log_stats.py by adding the top 10 of the most
present IPs in the collection nginx of the database logs:
'''
import pymongo
from pymongo import MongoClient
from collections import Counter

if __name__ == '__main__':
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['logs']
    collection = db['nginx']

    # Get total number of logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Get counts for different methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents(
        {"method": method}) for method in methods}

    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")

    # Get count for specific method and path
    specific_logs = collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"method=GET\npath=/status: {specific_logs}")

    # Get top 10 most common IPs
    ip_counts = Counter([log['ip'] for log in collection.find()])
    top_ips = ip_counts.most_common(10)

    print("IPs:")
    for ip, count in top_ips:
        print(f"\t{ip}: {count}")
