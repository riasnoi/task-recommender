from .settings import Settings

def build_qdrant_url(settings: Settings) -> str:
    return f"http://{settings.qdrant_host}:{settings.qdrant_port}"
