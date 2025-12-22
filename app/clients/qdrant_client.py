from qdrant_client import QdrantClient

from app.clients.qdrant import build_qdrant_url
from app.config import get_settings


def get_qdrant_client() -> QdrantClient:
    settings = get_settings()
    return QdrantClient(url=build_qdrant_url(settings))
