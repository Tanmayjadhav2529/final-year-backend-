from typing import List, Dict, Any

from config import CONFIDENCE_THRESHOLD


def classify_detections(detections: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Convert YOLO detections into the standard backend format.

    This currently expects a simple mock format.
    Later, this function can be adapted to the actual
    output format of the teammate's YOLO model.
    """

    defects = []

    for detection in detections:

        confidence = float(detection["confidence"])

        # Ignore detections below our confidence threshold
        if confidence < CONFIDENCE_THRESHOLD:
            continue

        defects.append({
            "class_name": detection["class_name"],
            "confidence": confidence,
            "bbox": detection["bbox"]
        })

    # No accepted defects = GOOD
    # At least one accepted defect = BAD
    verdict = "GOOD" if len(defects) == 0 else "BAD"

    return {
        "verdict": verdict,
        "defects": defects
    }