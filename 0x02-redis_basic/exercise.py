#!/usr/bin/env python3
""" Cache class """


import redis
import uuid
from typing import Union


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
