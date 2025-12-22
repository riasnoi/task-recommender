from fastapi import APIRouter

from . import attempts, auth, plan, recommendations, stats, tasks, ui

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(tasks.router)
api_router.include_router(attempts.router)
api_router.include_router(recommendations.router)
api_router.include_router(plan.router)
api_router.include_router(stats.router)
api_router.include_router(ui.router)
