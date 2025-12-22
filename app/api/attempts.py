from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import Attempt, AttemptCreate, AttemptResponse
from app.api.dependencies import get_db
from app.services import AttemptService

router = APIRouter(prefix="/attempts", tags=["attempts"])


@router.post("/", response_model=AttemptResponse)
def submit_attempt(payload: AttemptCreate, db: Session = Depends(get_db)):
    return AttemptService(db).submit_attempt(payload)


@router.get("/", response_model=List[Attempt])
def list_attempts(taskId: Optional[str] = None, result: Optional[str] = None, db: Session = Depends(get_db)):
    return AttemptService(db).list_attempts(taskId=taskId, result=result)


@router.get("/{attempt_id}", response_model=Attempt)
def get_attempt(attempt_id: str, db: Session = Depends(get_db)):
    try:
        return AttemptService(db).get_attempt(attempt_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
