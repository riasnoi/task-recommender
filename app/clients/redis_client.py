import redis

from app.config import get_settings
from app.clients.redis import build_redis_url


def get_redis_client() -> redis.Redis:
    settings = get_settings()
    return redis.Redis.from_url(build_redis_url(settings), decode_responses=True)
