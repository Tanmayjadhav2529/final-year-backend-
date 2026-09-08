from services.classification import classify_detections


def test_good_detection_result():

    detections = []

    result = classify_detections(detections)

    assert result["verdict"] == "GOOD"
    assert result["defects"] == []


def test_bad_detection_result():

    detections = [
        {
            "class_name": "crack",
            "confidence": 0.90,
            "bbox": [10, 20, 100, 120]
        }
    ]

    result = classify_detections(detections)

    assert result["verdict"] == "BAD"
    assert len(result["defects"]) == 1


def test_low_confidence_detection():

    detections = [
        {
            "class_name": "scratch",
            "confidence": 0.20,
            "bbox": [10, 20, 100, 120]
        }
    ]

    result = classify_detections(detections)

    assert result["verdict"] == "GOOD"
    assert result["defects"] == []