#!/usr/bin/env python3
"""log stats from collection
"""
from pymongo import MongoClient


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_stats(mongo_collection, option=None):
    """Provides stats about Nginx logs stored in MongoDB"""
    if option:
        value = mongo_collection.count_documents(
            {
                "method": {"$regex": option}
            }
        )
        print(f"\tmethod {option}: {value}")
        return

    result = mongo_collection.count_documents({})
    print(f"{result} logs")
    print("Methods:")
    for method in METHODS:
        log_stats(nginx_collection, method)
    count_result = mongo_collection.count_documents({'path': '/status'})
    print(f"{count_result} status check")

    print("IPs:")
    top = top_ten_ips(nginx_collection)
    for ip in top:
        print(f"\t{ip.get('_id')}: {ip.get('count')}")


def top_ten_ips(mongo_collection):
    """Retrieves the top 10 most common IP addresses"""
    top = mongo_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    return top


if __name__ == "__main__":
    nginx_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    log_stats(nginx_collection)
