import json
from os import environ
from urllib.parse import urlparse

import redis


class RedisPool:
    def __init__(self, host: str, port: str, username: str or None, password: str or None, ssl: bool = None,
                 ssl_cert_reqs: bool = None):
        self.pool = redis.ConnectionPool(host=host, port=port)
        self.username = username
        self.password = password
        self.ssl = ssl
        self.ssl_cert_reqs = ssl_cert_reqs
        self.connection = None

    def get_connection(self):
        self.connection = self.connection or redis.Redis(connection_pool=self.pool,
                                                         username=self.username,
                                                         password=self.password,
                                                         ssl=self.ssl,
                                                         ssl_cert_reqs=self.ssl_cert_reqs)
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


if environ.get("REDIS_URL"):
    url = urlparse(environ.get("REDIS_URL"))
    redis_host = url.hostname
    redis_port = url.port
    redis_username = url.username
    redis_password = url.password

    redis_client = RedisClient(
        redis_pool=RedisPool(host=redis_host, port=redis_port, username=redis_username, password=redis_password))
else:
    redis_host = "cache"
    redis_port = "6379"
    redis_client = RedisClient(redis_pool=RedisPool(host=redis_host, port=redis_port, username=None, password=None))

