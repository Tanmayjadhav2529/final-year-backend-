import os
from uuid import uuid4

from config import UPLOAD_DIR
from services.classification import classify_detections


def save_image(image_bytes: bytes, filename: str) -> str:
    """
    Save the uploaded image locally and return its path.
    """

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_extension = os.path.splitext(filename)[1]
    inspection_id = str(uuid4())

    saved_filename = f"{inspection_id}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)

    with open(file_path, "wb") as file:
        file.write(image_bytes)

    return file_path


def run_inspection(image, model):
    """
    Run the inspection pipeline.

    image:
        Image received from the frontend.

    model:
        YOLO model loaded in main.py.
    """

    # ============================================================
    # YOLO INTEGRATION
    # ============================================================
    #
    # For now, we are using a temporary mock result.
    #
    # Later, your teammate's actual YOLO model will be called here.
    #
    # Example idea:
    #
    # results = model(image)
    #
    # Then we will convert `results` into the format expected by
    # classification.py.
    #
    # ============================================================

    mock_detections = []

    # Send detections to classification.py
    result = classify_detections(mock_detections)

    return result