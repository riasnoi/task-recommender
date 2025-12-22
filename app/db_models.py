from datetime import date, datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, default="student", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    topic = Column(String, nullable=True)
    difficulty = Column(String, nullable=True)
    tags = Column(JSONB, default=list)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Attempt(Base):
    __tablename__ = "attempts"

    attempt_id = Column(String, primary_key=True, index=True)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    status = Column(String, nullable=False)
    accepted = Column(Boolean, default=False)
    answer_lang = Column(String, nullable=True)
    client_meta = Column(JSONB, nullable=True)
    errors = Column(JSONB, nullable=True)
    score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task")
    user = relationship("User")


class TopicProgress(Base):
    __tablename__ = "topic_progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    topic = Column(String, nullable=False)
    mastery = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("user_id", "topic", name="uq_topic_progress_user_topic"),)


class RecommendationRun(Base):
    __tablename__ = "recommendation_runs"

    run_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class RecommendationItem(Base):
    __tablename__ = "recommendation_items"

    id = Column(Integer, primary_key=True)
    run_id = Column(String, ForeignKey("recommendation_runs.run_id"), nullable=False)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)
    rank = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    reasons = Column(JSONB, default=list)


class PlanItem(Base):
    __tablename__ = "plan_items"

    item_id = Column(String, primary_key=True)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    due = Column(Date, nullable=False)
    status = Column(String, default="pending")
