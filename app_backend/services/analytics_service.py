from services.data_service import get_all_inspections


def get_summary():
    inspections = get_all_inspections()

    total_inspections = len(inspections)

    good_count = sum(
        1 for inspection in inspections
        if inspection["verdict"] == "GOOD"
    )

    bad_count = sum(
        1 for inspection in inspections
        if inspection["verdict"] == "BAD"
    )

    total_defects = sum(
        len(inspection.get("defects", []))
        for inspection in inspections
    )

    defect_rate = (
        (bad_count / total_inspections) * 100
        if total_inspections > 0
        else 0
    )

    return {
        "total_inspections": total_inspections,
        "good_count": good_count,
        "bad_count": bad_count,
        "total_defects": total_defects,
        "defect_rate": round(defect_rate, 2)
    }


def get_defect_distribution():
    inspections = get_all_inspections()

    defect_counts = {}

    for inspection in inspections:
        for defect in inspection.get("defects", []):
            class_name = defect.get("class_name", "unknown")

            if class_name in defect_counts:
                defect_counts[class_name] += 1
            else:
                defect_counts[class_name] = 1

    return {
        "defects": defect_counts
    }


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