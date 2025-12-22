from dataclasses import asdict
from typing import List, Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from app.domain import AttemptModel
from app.messaging import get_publisher
from app.repositories.postgres import PostgresAttemptRepository
from app.schemas import Attempt, AttemptCreate, AttemptResponse


class AttemptService:
    def __init__(self, db: Session) -> None:
        self.repo = PostgresAttemptRepository(db)
        self.publisher = get_publisher()

    def submit_attempt(self, payload: AttemptCreate) -> AttemptResponse:
        attempt = AttemptModel(
            attempt_id=str(uuid4()),
            task_id=payload.taskId,
            user_id="user-1",
            status="queued",
            accepted=True,
            answer_lang=payload.answerLang,
            client_meta=payload.clientMeta,
            errors=[],
        )
        attempt = self.repo.create(attempt)
        self.publisher.publish("attempt.submitted", {"attemptId": attempt.attempt_id, "taskId": attempt.task_id})
        return AttemptResponse(attemptId=attempt.attempt_id, status=attempt.status, accepted=attempt.accepted)

    def list_attempts(self, taskId: Optional[str] = None, result: Optional[str] = None) -> List[Attempt]:
        attempts = self.repo.list(task_id=taskId, result=result)
        return [Attempt(**asdict(attempt)) for attempt in attempts]

    def get_attempt(self, attempt_id: str) -> Attempt:
        attempt = self.repo.get(attempt_id)
        if not attempt:
            raise ValueError(f"Attempt {attempt_id} not found")
        return Attempt(**asdict(attempt))
