from dataclasses import asdict
from datetime import date
from typing import List
from uuid import uuid4

import json
from app.clients.redis_client import get_redis_client
from sqlalchemy.orm import Session

from app.domain import PlanItemModel
from app.db_models import PlanItem as PlanItemEntity
from app.repositories.postgres import PostgresPlanRepository, PostgresTaskRepository
from app.schemas import PlanItem, PlanRange


class PlanService:
    def __init__(self, db: Session) -> None:
        self.repo = PostgresPlanRepository(db)
        self.tasks_repo = PostgresTaskRepository(db)
        self.db = db
        self.redis = get_redis_client()

    @staticmethod
    def _to_schema(item: PlanItemModel) -> PlanItem:
        return PlanItem(
            itemId=item.item_id,
            taskId=item.task_id,
            due=item.due,
            status=item.status,
        )

    def _ensure_plan_for_today(self) -> None:
        if not self.repo.today("user-1"):
            tasks = self.tasks_repo.list(topic=None, difficulty=None, tags=None)
            if tasks:
                item = PlanItemModel(
                    item_id=str(uuid4()),
                    task_id=tasks[0].id,
                    user_id="user-1",
                    due=date.today(),
                    status="pending",
                )
                entity = PlanItemEntity(
                    item_id=item.item_id,
                    task_id=item.task_id,
                    user_id=item.user_id,
                    due=item.due,
                    status=item.status,
                )
                self.db.add(entity)
                self.db.commit()

    def plan_today(self) -> List[PlanItem]:
        cached = self.redis.get("plan:user-1:today")
        if cached:
            data = json.loads(cached)
            return [PlanItem(**item) for item in data]
        self._ensure_plan_for_today()
        items = self.repo.today("user-1")
        result = [self._to_schema(item) for item in items]
        self.redis.setex("plan:user-1:today", 300, json.dumps([item.dict() for item in result]))
        return result

    def plan_range(self, from_: date, to: date) -> PlanRange:
        self._ensure_plan_for_today()
        items = self.repo.range("user-1", from_=from_, to=to)
        return PlanRange(from_=from_, to=to, items=[self._to_schema(item) for item in items])

    def complete_item(self, item_id: str) -> dict:
        item = self.repo.complete(item_id)
        self.redis.delete("plan:user-1:today")
        return {"itemId": item.item_id, "status": item.status}

    def skip_item(self, item_id: str) -> dict:
        item = self.repo.skip(item_id)
        self.redis.delete("plan:user-1:today")
        return {"itemId": item.item_id, "status": item.status}
