from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas import Overview, TopicStat
from app.services import StatsService

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/overview", response_model=Overview)
def stats_overview(db: Session = Depends(get_db)):
    return StatsService(db).overview()


@router.get("/topics", response_model=List[TopicStat])
def stats_topics(db: Session = Depends(get_db)):
    return StatsService(db).topics()
