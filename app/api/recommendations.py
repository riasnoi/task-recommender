from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas import RecommendationResponse
from app.services import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/", response_model=RecommendationResponse)
def get_recommendations(db: Session = Depends(get_db)):
    return RecommendationService(db).get_recommendations()


@router.post("/recompute")
def recompute_recommendations(db: Session = Depends(get_db)):
    return RecommendationService(db).recompute()
