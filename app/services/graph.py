from app.clients.neo4j import build_neo4j_url
from app.config import get_settings

def get_neo4j_url() -> str:
    settings = get_settings()
    return build_neo4j_url(settings)
