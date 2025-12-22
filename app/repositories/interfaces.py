from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from app.domain import (
    AttemptModel,
    PlanItemModel,
    RecommendationRunModel,
    TaskModel,
    TopicProgressModel,
    UserModel,
)


class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserModel]:
        raise NotImplementedError

    @abstractmethod
    def create(self, user: UserModel) -> UserModel:
        raise NotImplementedError


class TaskRepository(ABC):
    @abstractmethod
    def list(self, topic: Optional[str], difficulty: Optional[str], tags: Optional[str]) -> List[TaskModel]:
        raise NotImplementedError

    @abstractmethod
    def get(self, task_id: str) -> Optional[TaskModel]:
        raise NotImplementedError

    @abstractmethod
    def create(self, task: TaskModel) -> TaskModel:
        raise NotImplementedError

    @abstractmethod
    def publish(self, task_id: str) -> TaskModel:
        raise NotImplementedError


class AttemptRepository(ABC):
    @abstractmethod
    def create(self, attempt: AttemptModel) -> AttemptModel:
        raise NotImplementedError

    @abstractmethod
    def list(self, task_id: Optional[str], result: Optional[str]) -> List[AttemptModel]:
        raise NotImplementedError

    @abstractmethod
    def get(self, attempt_id: str) -> Optional[AttemptModel]:
        raise NotImplementedError


class RecommendationRepository(ABC):
    @abstractmethod
    def latest_for_user(self, user_id: str) -> Optional[RecommendationRunModel]:
        raise NotImplementedError

    @abstractmethod
    def save_run(self, run: RecommendationRunModel) -> RecommendationRunModel:
        raise NotImplementedError


class PlanRepository(ABC):
    @abstractmethod
    def today(self, user_id: str) -> List[PlanItemModel]:
        raise NotImplementedError

    @abstractmethod
    def range(self, user_id: str, from_: date, to: date) -> List[PlanItemModel]:
        raise NotImplementedError

    @abstractmethod
    def complete(self, item_id: str) -> PlanItemModel:
        raise NotImplementedError

    @abstractmethod
    def skip(self, item_id: str) -> PlanItemModel:
        raise NotImplementedError


class TopicProgressRepository(ABC):
    @abstractmethod
    def upsert(self, progress: TopicProgressModel) -> TopicProgressModel:
        raise NotImplementedError

    @abstractmethod
    def list_for_user(self, user_id: str) -> List[TopicProgressModel]:
        raise NotImplementedError
