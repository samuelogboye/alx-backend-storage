#!/usr/bin/env python3
""" 0x02-redis_basic/exercise.py """

import redis

import uuid
from typing import Union, Callable


class Cache():
    """Cache class with redis"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

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
