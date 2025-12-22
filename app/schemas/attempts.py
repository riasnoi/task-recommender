from typing import List, Optional

from pydantic import BaseModel

class AttemptCreate(BaseModel):
    taskId: str
    answer: str
    answerLang: str
    clientMeta: Optional[dict] = None


class AttemptResponse(BaseModel):
    attemptId: str
    status: str
    accepted: bool


class Attempt(BaseModel):
    attemptId: str
    taskId: str
    status: str
    accepted: bool
    errors: Optional[List[str]] = None
