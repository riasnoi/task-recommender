from dataclasses import asdict
from typing import List, Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from app.domain import TaskModel
from app.messaging import get_publisher
from app.repositories.postgres import PostgresTaskRepository
from app.schemas import Task, TaskCreate, TaskPublishResponse


class TaskService:
    def __init__(self, db: Session) -> None:
        self.repo = PostgresTaskRepository(db)
        self.publisher = get_publisher()

    def list_tasks(self, topic: Optional[str] = None, difficulty: Optional[str] = None, tags: Optional[str] = None) -> List[Task]:
        tasks = self.repo.list(topic=topic, difficulty=difficulty, tags=tags)
        return [Task(**asdict(task)) for task in tasks]

    def get_task(self, task_id: str) -> Task:
        task = self.repo.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return Task(**asdict(task))

    def create_task(self, payload: TaskCreate) -> Task:
        model = TaskModel(
            id=str(uuid4()),
            title=payload.title,
            topic=payload.topic,
            difficulty=payload.difficulty,
            tags=payload.tags,
            published=False,
        )
        task = self.repo.create(model)
        return Task(**asdict(task))

    def publish_task(self, task_id: str) -> TaskPublishResponse:
        task = self.repo.publish(task_id)
        self.publisher.publish("task.published", {"taskId": task.id})
        return TaskPublishResponse(taskId=task.id, status="published")
