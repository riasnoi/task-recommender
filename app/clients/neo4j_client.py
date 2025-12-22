from neo4j import GraphDatabase

from app.clients.neo4j import build_neo4j_url
from app.config import get_settings


def get_neo4j_driver():
    settings = get_settings()
    return GraphDatabase.driver(build_neo4j_url(settings), auth=(settings.neo4j_user, settings.neo4j_password))
