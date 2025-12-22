from typing import List

from pydantic import BaseModel

class RecommendationItem(BaseModel):
    taskId: str
    rank: int
    score: float
    reasons: List[str]


class RecommendationResponse(BaseModel):
    runId: str
    items: List[RecommendationItem]
