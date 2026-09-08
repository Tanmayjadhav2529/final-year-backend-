import os
from datetime import datetime, timezone
from uuid import uuid4

from config import UPLOAD_DIR
from services.classification import classify_detections
from services.data_service import save_inspection


def save_image(image_bytes: bytes, filename: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_extension = os.path.splitext(filename)[1]
    inspection_id = str(uuid4())

    saved_filename = f"{inspection_id}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)

    with open(file_path, "wb") as file:
        file.write(image_bytes)

    return file_path


def run_inspection(image, model, image_path):
    mock_detections = []

    result = classify_detections(mock_detections)

    inspection_id = str(uuid4())

    record = {
        "id": inspection_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "verdict": result["verdict"],
        "defects": result["defects"],
        "image_path": image_path
    }

    save_inspection(record)

    return record