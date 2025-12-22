from app.clients.redis import build_redis_url
from app.config import get_settings

def get_redis_url() -> str:
    settings = get_settings()
    return build_redis_url(settings)
