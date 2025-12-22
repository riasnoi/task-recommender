from app.clients.postgres import build_postgres_dsn
from app.config import get_settings

def get_postgres_dsn() -> str:
    settings = get_settings()
    return build_postgres_dsn(settings)
