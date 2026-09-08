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

def get_inspection_trends():
    inspections = get_all_inspections()

    daily_data = {}

    for inspection in inspections:
        timestamp = inspection.get("timestamp")

        if not timestamp:
            continue

        date = timestamp[:10]

        if date not in daily_data:
            daily_data[date] = {
                "total": 0,
                "good": 0,
                "bad": 0
            }

        daily_data[date]["total"] += 1

        if inspection.get("verdict") == "GOOD":
            daily_data[date]["good"] += 1

        elif inspection.get("verdict") == "BAD":
            daily_data[date]["bad"] += 1

    daily_inspections = []

    for date, data in sorted(daily_data.items()):
        daily_inspections.append({
            "date": date,
            "total": data["total"],
            "good": data["good"],
            "bad": data["bad"]
        })

    return {
        "daily_inspections": daily_inspections
    }

@router.get("/trends")
def analytics_trends():
    return get_inspection_trends()