#!/usr/bin/env python3
'''Create a Cache class. In the __init__ method, store an instance of the Redis
client as a private variable named _redis (using redis.Redis()) and flush the
instance using flushdb.

Create a store method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid), store the input
data in Redis using the random key and return the key.

Type-annotate store correctly. Remember that data can be a str, bytes,
int or float.
'''
import redis
from typing import Union, Optional, Callable
from uuid import uuid4, UUID
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''Counts the number of times a method is called'''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function'''
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    '''Stores the history of inputs and outputs for a
    particular function'''
    input_list_key = method.__qualname__ + ":inputs"
    output_list_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function'''
        self._redis.rpush(input_list_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_list_key, str(output))
        return output
    return wrapper


def replay(method: Callable):
    '''Displays the history of calls of a particular function'''
    cache = redis.Redis()
    name = method.__qualname__
    input_list_key = name + ":inputs"
    output_list_key = name + ":outputs"
    assert cache.llen(input_list_key) and cache.llen(output_list_key)
    inputs = cache.lrange(input_list_key, 0, cache.llen(input_list_key))
    outputs = cache.lrange(output_list_key, 0, cache.llen(output_list_key))

    print("{} was called {} times:".format(name, cache.llen(input_list_key)))

    for input, output in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, input.decode('utf-8'),
                                     output.decode('utf-8')))


class Cache:
    '''A Cache class using Redis as a data store'''

    def __init__(self) -> None:
        '''Initialize Cache instance'''
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Store data in Redis'''
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable]
            = None) -> Union[str, bytes, int, float]:
        '''Get data from Redis'''
        data = self._redis.get(key)
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        '''Convert bytes to str'''
        data = self._redis.get(key)
        return data.decode('utf-8')

    def get_int(self, key: str) -> int:
        '''Convert bytes to int'''
        data = self._redis.get(key)
        try:
            data = int(data.decode('utf-8'))
        except ValueError:
            data = 0
        return data
