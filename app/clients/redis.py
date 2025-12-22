from .settings import Settings

def build_redis_url(settings: Settings) -> str:
    return f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"
