import json
from os import environ
from urllib.parse import urlparse

import redis


class RedisPool:
    def __init__(self, host: str, port: int):
        self.pool = redis.ConnectionPool(host=host, port=port)
        self.connection = None

    def get_connection(self):
        self.connection = self.connection or redis.Redis(connection_pool=self.pool)
        return self.connection


class RedisClient:
    def __init__(self, redis_pool: RedisPool):
        try:
            self._redis_pool = redis_pool.get_connection()
        except Exception:
            print("redis connection error")

    def set(self, key: str, value: dict):
        self._redis_pool.set(key, json.dumps(value))

    def get(self, key: str):
        value = self._redis_pool.get(key)
        return json.loads(value) if value else None

    def delete(self, key: str):
        self._redis_pool.delete(key)


test = redis.ConnectionPool()

url = urlparse(environ.get("REDIS_URL"))
redis_client = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True, ssl_cert_reqs=None)


# redis_host = environ.get("REDISTOGO_URL") or "cache"
# redis_port = environ.get("REDIS_PORT") or 6379
# redis_db = environ.get("REDIS_DB") or 0
# redis_client = RedisClient(redis_pool=RedisPool(host=redis_url.hostname,port=redis_url.port))
# redis_client = RedisClient(redis_pool=RedisPool(host=redis_url.hostname,port=redis_url.port))
# redis_client = RedisClient(redis_pool=RedisPool(host=redis_host, port=redis_port, db=redis_db))
