import io
import json
import os

from fastapi.testclient import TestClient

from main import app
from config import DATA_DIR


def test_inspect_image():

    # TestClient must be used as a context manager
    # so FastAPI's lifespan runs.
    with TestClient(app) as client:

        # Create a fake PNG file
        image = io.BytesIO(
            b"\x89PNG\r\n\x1a\n"
            b"fake-image-data"
        )

        response = client.post(
            "/inspect/",
            files={
                "file": (
                    "test.png",
                    image,
                    "image/png"
                )
            }
        )

        assert response.status_code == 200

        result = response.json()

        # Check response fields
        assert "id" in result
        assert "timestamp" in result
        assert "verdict" in result
        assert "defects" in result
        assert "image_path" in result

        # Current backend uses mock YOLO
        assert result["verdict"] == "GOOD"
        assert result["defects"] == []

        # Check inspection JSON file
        data_file = os.path.join(
            DATA_DIR,
            "inspections.json"
        )

        assert os.path.exists(data_file)

        with open(data_file, "r") as file:
            inspections = json.load(file)

        saved_inspection = next(
            item
            for item in inspections
            if item["id"] == result["id"]
        )

        assert saved_inspection["verdict"] == "GOOD"
        assert saved_inspection["defects"] == []
        assert saved_inspection["image_path"] == result["image_path"]