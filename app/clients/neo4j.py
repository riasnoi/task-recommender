from .settings import Settings

def build_neo4j_url(settings: Settings) -> str:
    return f"bolt://{settings.neo4j_host}:{settings.neo4j_port}"
