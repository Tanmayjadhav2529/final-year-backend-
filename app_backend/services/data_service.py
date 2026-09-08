import json
import os

from config import DATA_DIR


DATA_FILE = os.path.join(DATA_DIR, "inspections.json")


def save_inspection(record: dict):
    """
    Save an inspection record to the local JSON file.
    """

    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            inspections = json.load(file)
    else:
        inspections = []

    inspections.append(record)

    with open(DATA_FILE, "w") as file:
        json.dump(inspections, file, indent=4)


def get_all_inspections():
    """
    Return all saved inspection records.
    """

    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)