#!/usr/bin/env python3
"""Open a collection and returns all documents in it."""


def list_all(mongo_collection):
    """
    Retrieve all documents from the specified mongo_collection.
    :param mongo_collection: The collection to retrieve documents from.
    :type mongo_collection: collection
    :return: A list of documents from the collection,
     or an empty list if no documents are found.
    :rtype: list
    """
    document = mongo_collection.find()
    if not document:
        return []
    return document
