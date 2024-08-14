#!/usr/bin/env python3
""" Cache class """

import redis
import uuid
from typing import Union, Callable
import functools


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a method."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Generate the key using the method's qualified name
        key = method.__qualname__
        # Increment the count in Redis
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """ Cache class """
    def __init__(self) -> None:
        """ Initialize Redis client and flush the database """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store data in Redis and return the generated key """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        """
        Retrieve data from Redis and apply an
        optional conversion function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Helper method to retrieve a string from Redis"""
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Helper method to retrieve an integer from Redis"""
        return self.get(key, int)

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store data in Redis and return the generated key """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
