#!/usr/bin/env python3
""" 0x02-redis_basic/exercise.py """

import redis

import uuid
from typing import Union, Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    """Call history decorator
       Args:
        method (Callable): method to be decorated

       Returns:
          Callable: decorated method
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        This function serves as a wrapper to log inputs
        and outputs of the given method.
        It takes in 'self', '*args', and '**kwargs' as
        parameters and returns the output.
        """
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        output = method(self, *args, **kwargs)

        self._redis.rpush(input_key, str(args))
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


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


def replay(fn: Callable):
    """Display the history of calls of a particular function"""
    with redis.Redis() as r:
        f_name = fn.__qualname__
        n_calls = int(r.get(f_name) or 0)
        print(f'{f_name} was called {n_calls} times:')

        ins = [i.decode('utf-8') if isinstance(i, bytes) else "" for i in r.lrange(f_name + ":inputs", 0, -1)]
        outs = [o.decode('utf-8') if isinstance(o, bytes) else "" for o in r.lrange(f_name + ":outputs", 0, -1)]

        for i, o in zip(ins, outs):
            print(f'{f_name}(*{i}) -> {o}')


class Cache():
    """Cache class with redis"""

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
