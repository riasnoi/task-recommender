from typing import List, Optional

from pydantic import BaseModel

class Task(BaseModel):
    id: str
    title: str
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    tags: List[str] = []


class TaskCreate(BaseModel):
    title: str
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    tags: List[str] = []


class TaskPublishResponse(BaseModel):
    taskId: str
    status: str
