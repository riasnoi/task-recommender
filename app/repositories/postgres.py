from datetime import date, datetime
from typing import List, Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db_models import Attempt, PlanItem, RecommendationItem, RecommendationRun, Task, TopicProgress, User
from app.domain import (
    AttemptModel,
    PlanItemModel,
    RecommendationItemModel,
    RecommendationRunModel,
    TaskModel,
    TopicProgressModel,
    UserModel,
)
from app.repositories import (
    AttemptRepository,
    PlanRepository,
    RecommendationRepository,
    TaskRepository,
    TopicProgressRepository,
    UserRepository,
)


def _to_task_model(entity: Task) -> TaskModel:
    return TaskModel(
        id=entity.id,
        title=entity.title,
        topic=entity.topic,
        difficulty=entity.difficulty,
        tags=entity.tags or [],
        published=entity.published,
        created_at=entity.created_at,
    )


class PostgresUserRepository(UserRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> Optional[UserModel]:
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return None
        return UserModel(id=user.id, email=user.email, role=user.role, created_at=user.created_at)

    def create(self, user: UserModel) -> UserModel:
        entity = User(id=user.id or str(uuid4()), email=user.email, role=user.role, created_at=user.created_at or datetime.utcnow())
        self.db.add(entity)
        self.db.commit()
        return UserModel(id=entity.id, email=entity.email, role=entity.role, created_at=entity.created_at)


class PostgresTaskRepository(TaskRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, topic: Optional[str], difficulty: Optional[str], tags: Optional[str]) -> List[TaskModel]:
        query = self.db.query(Task)
        if topic:
            query = query.filter(Task.topic == topic)
        if difficulty:
            query = query.filter(Task.difficulty == difficulty)
        if tags:
            tag_set = set(tags.split(","))
            query = query.filter(Task.tags.op("&&")(list(tag_set)))
        tasks = query.all()
        return [_to_task_model(t) for t in tasks]

    def get(self, task_id: str) -> Optional[TaskModel]:
        entity = self.db.query(Task).get(task_id)
        return _to_task_model(entity) if entity else None

    def create(self, task: TaskModel) -> TaskModel:
        entity = Task(
            id=task.id or str(uuid4()),
            title=task.title,
            topic=task.topic,
            difficulty=task.difficulty,
            tags=task.tags,
            published=False,
            created_at=task.created_at or datetime.utcnow(),
        )
        self.db.add(entity)
        self.db.commit()
        return _to_task_model(entity)

    def publish(self, task_id: str) -> TaskModel:
        entity = self.db.query(Task).get(task_id)
        if not entity:
            raise KeyError(f"Task {task_id} not found")
        entity.published = True
        self.db.commit()
        return _to_task_model(entity)


class PostgresAttemptRepository(AttemptRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, attempt: AttemptModel) -> AttemptModel:
        entity = Attempt(
            attempt_id=attempt.attempt_id or str(uuid4()),
            task_id=attempt.task_id,
            user_id=attempt.user_id,
            status=attempt.status,
            accepted=attempt.accepted,
            answer_lang=attempt.answer_lang,
            client_meta=attempt.client_meta,
            errors=attempt.errors,
            score=attempt.score,
            created_at=attempt.created_at or datetime.utcnow(),
        )
        self.db.add(entity)
        self.db.commit()
        return AttemptModel(
            attempt_id=entity.attempt_id,
            task_id=entity.task_id,
            user_id=entity.user_id,
            status=entity.status,
            accepted=entity.accepted,
            answer_lang=entity.answer_lang,
            client_meta=entity.client_meta,
            errors=entity.errors,
            score=entity.score,
            created_at=entity.created_at,
        )

    def list(self, task_id: Optional[str], result: Optional[str]) -> List[AttemptModel]:
        query = self.db.query(Attempt)
        if task_id:
            query = query.filter(Attempt.task_id == task_id)
        if result:
            query = query.filter(Attempt.status == result)
        attempts = query.all()
        return [
            AttemptModel(
                attempt_id=a.attempt_id,
                task_id=a.task_id,
                user_id=a.user_id,
                status=a.status,
                accepted=a.accepted,
                answer_lang=a.answer_lang,
                client_meta=a.client_meta,
                errors=a.errors,
                score=a.score,
                created_at=a.created_at,
            )
            for a in attempts
        ]

    def get(self, attempt_id: str) -> Optional[AttemptModel]:
        a = self.db.query(Attempt).get(attempt_id)
        if not a:
            return None
        return AttemptModel(
            attempt_id=a.attempt_id,
            task_id=a.task_id,
            user_id=a.user_id,
            status=a.status,
            accepted=a.accepted,
            answer_lang=a.answer_lang,
            client_meta=a.client_meta,
            errors=a.errors,
            score=a.score,
            created_at=a.created_at,
        )


class PostgresRecommendationRepository(RecommendationRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def latest_for_user(self, user_id: str) -> Optional[RecommendationRunModel]:
        run = (
            self.db.query(RecommendationRun)
            .filter(RecommendationRun.user_id == user_id)
            .order_by(RecommendationRun.created_at.desc())
            .first()
        )
        if not run:
            return None
        items = (
            self.db.query(RecommendationItem)
            .filter(RecommendationItem.run_id == run.run_id)
            .order_by(RecommendationItem.rank.asc())
            .all()
        )
        return RecommendationRunModel(
            run_id=run.run_id,
            user_id=run.user_id,
            created_at=run.created_at,
            items=[
                RecommendationItemModel(
                    task_id=i.task_id,
                    rank=i.rank,
                    score=i.score,
                    reasons=i.reasons or [],
                )
                for i in items
            ],
        )

    def save_run(self, run: RecommendationRunModel) -> RecommendationRunModel:
        entity = RecommendationRun(run_id=run.run_id, user_id=run.user_id, created_at=run.created_at or datetime.utcnow())
        # ensure parent row exists before inserting children
        self.db.merge(entity)
        self.db.flush()
        self.db.query(RecommendationItem).filter(RecommendationItem.run_id == run.run_id).delete()
        for item in run.items:
            self.db.add(
                RecommendationItem(
                    run_id=run.run_id,
                    task_id=item.task_id,
                    rank=item.rank,
                    score=item.score,
                    reasons=item.reasons,
                )
            )
        self.db.commit()
        return run


class PostgresPlanRepository(PlanRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def today(self, user_id: str) -> List[PlanItemModel]:
        items = self.db.query(PlanItem).filter(PlanItem.user_id == user_id, PlanItem.due == date.today()).all()
        return [PlanItemModel(item_id=i.item_id, task_id=i.task_id, user_id=i.user_id, due=i.due, status=i.status) for i in items]

    def range(self, user_id: str, from_: date, to: date) -> List[PlanItemModel]:
        items = (
            self.db.query(PlanItem)
            .filter(PlanItem.user_id == user_id, PlanItem.due >= from_, PlanItem.due <= to)
            .all()
        )
        return [PlanItemModel(item_id=i.item_id, task_id=i.task_id, user_id=i.user_id, due=i.due, status=i.status) for i in items]

    def complete(self, item_id: str) -> PlanItemModel:
        item = self.db.query(PlanItem).get(item_id)
        if not item:
            raise KeyError(f"Plan item {item_id} not found")
        item.status = "completed"
        self.db.commit()
        return PlanItemModel(item_id=item.item_id, task_id=item.task_id, user_id=item.user_id, due=item.due, status=item.status)

    def skip(self, item_id: str) -> PlanItemModel:
        item = self.db.query(PlanItem).get(item_id)
        if not item:
            raise KeyError(f"Plan item {item_id} not found")
        item.status = "skipped"
        self.db.commit()
        return PlanItemModel(item_id=item.item_id, task_id=item.task_id, user_id=item.user_id, due=item.due, status=item.status)


class PostgresTopicProgressRepository(TopicProgressRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def upsert(self, progress: TopicProgressModel) -> TopicProgressModel:
        existing = (
            self.db.query(TopicProgress)
            .filter(TopicProgress.user_id == progress.user_id, TopicProgress.topic == progress.topic)
            .first()
        )
        if existing:
            existing.mastery = progress.mastery
            existing.updated_at = progress.updated_at or datetime.utcnow()
            entity = existing
        else:
            entity = TopicProgress(
                user_id=progress.user_id,
                topic=progress.topic,
                mastery=progress.mastery,
                updated_at=progress.updated_at or datetime.utcnow(),
            )
            self.db.add(entity)
        self.db.commit()
        return TopicProgressModel(
            user_id=entity.user_id,
            topic=entity.topic,
            mastery=entity.mastery,
            updated_at=entity.updated_at,
        )

    def list_for_user(self, user_id: str) -> List[TopicProgressModel]:
        items = self.db.query(TopicProgress).filter(TopicProgress.user_id == user_id).all()
        return [TopicProgressModel(user_id=i.user_id, topic=i.topic, mastery=i.mastery, updated_at=i.updated_at) for i in items]
