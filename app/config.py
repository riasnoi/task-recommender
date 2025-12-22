from functools import lru_cache
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    student_name: str = Field(..., env="STUDENT_NAME")
    db_host: str = Field(..., env="DB_HOST")

    postgres_host: str = Field(..., env="POSTGRES_HOST")
    postgres_port: int = Field(..., env="POSTGRES_PORT")
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., env="POSTGRES_DB")

    mongo_host: str = Field(..., env="MONGO_HOST")
    mongo_port: int = Field(..., env="MONGO_PORT")
    mongo_user: str = Field(..., env="MONGO_USER")
    mongo_password: str = Field(..., env="MONGO_PASSWORD")
    mongo_db: str = Field(..., env="MONGO_DB")

    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")
    redis_db: int = Field(..., env="REDIS_DB")

    qdrant_host: str = Field(..., env="QDRANT_HOST")
    qdrant_port: int = Field(..., env="QDRANT_PORT")

    neo4j_host: str = Field(..., env="NEO4J_HOST")
    neo4j_port: int = Field(..., env="NEO4J_PORT")
    neo4j_user: str = Field(..., env="NEO4J_USER")
    neo4j_password: str = Field(..., env="NEO4J_PASSWORD")

    rabbitmq_host: str = Field(..., env="RABBITMQ_HOST")
    rabbitmq_port: int = Field(..., env="RABBITMQ_PORT")
    rabbitmq_user: str = Field(..., env="RABBITMQ_USER")
    rabbitmq_password: str = Field(..., env="RABBITMQ_PASSWORD")
    rabbitmq_exchange: str = Field("learning.tasks", env="RABBITMQ_EXCHANGE")

    class Config:
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings()
