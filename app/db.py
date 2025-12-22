from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.clients.postgres import build_postgres_dsn
from app.config import get_settings

settings = get_settings()
engine = create_engine(build_postgres_dsn(settings))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
