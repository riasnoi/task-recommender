from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import Task, TaskCreate, TaskPublishResponse
from app.api.dependencies import get_db
from app.services import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[Task])
def list_tasks(topic: Optional[str] = None, difficulty: Optional[str] = None, tags: Optional[str] = None, db: Session = Depends(get_db)):
    return TaskService(db).list_tasks(topic=topic, difficulty=difficulty, tags=tags)


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: str, db: Session = Depends(get_db)):
    try:
        return TaskService(db).get_task(task_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return TaskService(db).create_task(task)


@router.post("/{task_id}/publish", response_model=TaskPublishResponse)
def publish_task(task_id: str, db: Session = Depends(get_db)):
    return TaskService(db).publish_task(task_id)
