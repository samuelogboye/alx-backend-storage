#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """


def top_students(mongo_collection):
    """
    Function to retrieve the top students from a MongoDB
    collection using aggregation.

    Parameters:
    - mongo_collection: The MongoDB collection from which to
    retrieve the top students.

    Returns:
    - A cursor with the top students sorted by average score
    in descending order.
    """
    top = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return top
