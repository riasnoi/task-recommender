import logging

from fastapi import FastAPI

from .api.router import api_router
from .db import Base, engine
from .config import get_settings
from .db_models import Task, User

logging.basicConfig(level=logging.INFO)
settings = get_settings()
app = FastAPI(title="Learning Tasks Recommender API", version="0.1.0")


@app.get("/")
def root():
    return {"message": "Learning Tasks Recommender API"}


@app.get("/health")
def health():
    return {"status": "ok", "student": settings.student_name}


app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def on_startup() -> None:
    # Создаём таблицы, если их ещё нет (для простого MVP без миграций)
    Base.metadata.create_all(bind=engine)
    # Сидим базовые сущности, если пусто
    with engine.begin() as conn:
        user_count = conn.execute(User.__table__.select().limit(1)).fetchone()
        if not user_count:
            conn.execute(User.__table__.insert().values(id="user-1", email="student@example.com", role="student"))
        task_count = conn.execute(Task.__table__.select().limit(1)).fetchone()
        if not task_count:
            conn.execute(
                Task.__table__.insert().values(
                    id="task-1",
                    title="SQL joins basics",
                    topic="sql.joins",
                    difficulty="medium",
                    tags=["sql", "joins"],
                    published=True,
                )
            )
