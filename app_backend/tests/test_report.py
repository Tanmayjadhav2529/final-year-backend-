from fastapi.testclient import TestClient

from main import app
from services.data_service import get_all_inspections


def test_get_report():
    inspections = get_all_inspections()

    if not inspections:
        return

    inspection_id = inspections[0]["id"]

    with TestClient(app) as client:
        response = client.get(f"/reports/{inspection_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["inspection_id"] == inspection_id
    assert "timestamp" in data
    assert "verdict" in data
    assert "defects" in data
    assert "image_path" in data


def test_report_not_found():
    with TestClient(app) as client:
        response = client.get("/reports/invalid-inspection-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Inspection not found"