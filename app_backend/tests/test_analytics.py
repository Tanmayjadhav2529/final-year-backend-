from services.analytics_service import get_defect_distribution, get_inspection_trends, get_summary


def test_analytics_summary():
    result = get_summary()

    assert "total_inspections" in result
    assert "good_count" in result
    assert "bad_count" in result
    assert "total_defects" in result
    assert "defect_rate" in result


def test_analytics_counts():
    result = get_summary()

    assert result["total_inspections"] >= 0
    assert result["good_count"] >= 0
    assert result["bad_count"] >= 0
    assert result["total_defects"] >= 0
    assert result["defect_rate"] >= 0

def test_defect_distribution():
    result = get_defect_distribution()

    assert "defects" in result
    assert isinstance(result["defects"], dict)

def test_inspection_trends():
    result = get_inspection_trends()

    assert "daily_inspections" in result
    assert isinstance(result["daily_inspections"], list)