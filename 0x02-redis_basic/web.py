#!/usr/bin/env python3
""" Cache class """

import redis
import uuid
from typing import Union, Callable


def get_page(url: str) -> str:
    """ Cache class """
