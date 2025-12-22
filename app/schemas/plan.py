from datetime import date
from typing import List

from pydantic import BaseModel

class PlanItem(BaseModel):
    itemId: str
    taskId: str
    due: date
    status: str


class PlanRange(BaseModel):
    from_: date
    to: date
    items: List[PlanItem]

    class Config:
        fields = {"from_": "from"}
