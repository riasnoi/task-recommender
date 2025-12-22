from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas import PlanItem, PlanRange
from app.services import PlanService

router = APIRouter(prefix="/plan", tags=["plan"])


@router.get("/today", response_model=List[PlanItem])
def plan_today(db: Session = Depends(get_db)):
    return PlanService(db).plan_today()


@router.get("/", response_model=PlanRange)
def plan_range(from_: date = Query(..., alias="from"), to: date = Query(..., alias="to"), db: Session = Depends(get_db)):
    return PlanService(db).plan_range(from_=from_, to=to)


@router.post("/items/{item_id}/complete")
def complete_item(item_id: str, db: Session = Depends(get_db)):
    return PlanService(db).complete_item(item_id)


@router.post("/items/{item_id}/skip")
def skip_item(item_id: str, db: Session = Depends(get_db)):
    return PlanService(db).skip_item(item_id)
