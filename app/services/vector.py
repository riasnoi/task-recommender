from app.clients.qdrant import build_qdrant_url
from app.config import get_settings

def get_qdrant_url() -> str:
    settings = get_settings()
    return build_qdrant_url(settings)
