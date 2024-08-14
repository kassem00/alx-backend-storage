#!/usr/bin/env python3
""" Cache class """

import redis
import uuid
from typing import Union, Callable

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
        """Retrieve data from Redis and apply an optional conversion function."""
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
