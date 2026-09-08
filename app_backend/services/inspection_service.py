import json
import os
from datetime import datetime, timezone
from uuid import uuid4

from config import UPLOAD_DIR, DATA_DIR
from services.classification import classify_detections


def save_image(image_bytes: bytes, filename: str) -> str:
    """
    Save the uploaded image locally.
    """

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_extension = os.path.splitext(filename)[1]
    inspection_id = str(uuid4())

    saved_filename = f"{inspection_id}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)

    with open(file_path, "wb") as file:
        file.write(image_bytes)

    return file_path


def save_inspection(record: dict):
    """
    Save an inspection record to the local JSON file.
    """

    os.makedirs(DATA_DIR, exist_ok=True)

    data_file = os.path.join(DATA_DIR, "inspections.json")

    # Read existing inspections
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            inspections = json.load(file)
    else:
        inspections = []

    # Add new inspection
    inspections.append(record)

    # Save updated inspections
    with open(data_file, "w") as file:
        json.dump(inspections, file, indent=4)


def run_inspection(image, model, image_path):
    """
    Run the complete inspection workflow.
    """

    # ============================================================
    # YOLO INTEGRATION
    # ============================================================
    #
    # Temporary mock result.
    #
    # Later, your teammate's trained YOLO model will be called here.
    #
    # Example:
    #
    # results = model(image)
    #
    # Then we will convert the YOLO output into the format
    # expected by classification.py.
    #
    # ============================================================

    mock_detections = []

    # Convert detections into GOOD/BAD + defect information
    result = classify_detections(mock_detections)

    # Create inspection record
    inspection_id = str(uuid4())

    record = {
        "id": inspection_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "verdict": result["verdict"],
        "defects": result["defects"]
    }

    # Save inspection result
    save_inspection(record)

    return record