from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional


@dataclass
class UserModel:
    id: str
    email: str
    role: str = "student"
    created_at: Optional[datetime] = None


@dataclass
class TaskModel:
    id: str
    title: str
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    tags: List[str] = None
    published: bool = False
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class AttemptModel:
    attempt_id: str
    task_id: str
    user_id: str
    status: str
    accepted: bool
    answer_lang: Optional[str] = None
    client_meta: Optional[dict] = None
    errors: Optional[List[str]] = None
    score: Optional[float] = None
    created_at: Optional[datetime] = None


@dataclass
class TopicProgressModel:
    user_id: str
    topic: str
    mastery: float
    updated_at: Optional[datetime] = None


@dataclass
class RecommendationItemModel:
    task_id: str
    rank: int
    score: float
    reasons: List[str]


@dataclass
class RecommendationRunModel:
    run_id: str
    user_id: str
    items: List[RecommendationItemModel]
    created_at: Optional[datetime] = None


@dataclass
class PlanItemModel:
    item_id: str
    task_id: str
    user_id: str
    due: date
    status: str
