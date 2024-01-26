#!/usr/bin/env python3
"""Web Cache"""

import requests
import redis
from functools import wraps


store = redis.Redis()


def count_url_access(method):
    """
    Decorator function to count URL access and cache the data.

    Decorator function that caches the result of the method
    for a given URL.

    Args:
        url (str): The URL for which the result should be cached.

    Returns:
        str: The cached HTML content for the given URL.
    """
    @wraps(method)
    def wrapper(url):
        cached_key = f"cached:{url}"
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = f"count:{url}"
        html = method(url)

        store.incr(count_key)
        store.set(cached_key, html)
        store.expire(cached_key, 10)
        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """
    Decorator to count the number of times the function is accessed.
    Retrieves the content of the given URL and returns it as a string.
    """
    res = requests.get(url)
    return res.text
