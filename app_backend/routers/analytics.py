from fastapi import APIRouter

from services.analytics_service import (
    get_summary,
    get_defect_distribution,
    get_inspection_trends
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/summary")
def analytics_summary():
    return get_summary()


@router.get("/defects")
def analytics_defects():
    return get_defect_distribution()


@router.get("/trends")
def analytics_trends():
    return get_inspection_trends()