#!/usr/bin/env python3
""" 0x02-redis_basic/exercise.py """

import redis

import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Count calls decorator

    Args:
        method (Callable): method to be decorated

    Returns:
        Callable: decorated method
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache():
    """Cache class with redis"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store method

        Args:
            data (Union[str, bytes, int, float]): Data to be stored

        Returns:
            str: string
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """Get method

        Args:
            key (str): key to get
            fn (callable, optional): callable function. Defaults to None.

        Returns:
            Union[str, bytes, int, float]: data
        """
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """Get string

        Args:
            key (str): key to get

        Returns:
            str: string
        """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Get integer

        Args:
            key (str): key to get

        Returns:
            int: integer
        """
        return self.get(key, int)
