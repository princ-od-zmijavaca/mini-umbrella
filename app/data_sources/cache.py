import json
import redis


class RedisPool:
    def __init__(self, host: str, port: int, db: int):
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
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


redis_client = RedisClient(redis_pool=RedisPool(host="cache", port=6379, db=0))