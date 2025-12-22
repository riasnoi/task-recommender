from typing import List

from pydantic import BaseModel

class Overview(BaseModel):
    progress: float
    streak: int


class TopicStat(BaseModel):
    topic: str
    mastery: float


class TopicsResponse(BaseModel):
    items: List[TopicStat]
