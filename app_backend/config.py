import os
from dotenv import load_dotenv

load_dotenv()

# Base directory of the backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Local storage
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DATA_DIR = os.path.join(BASE_DIR, "data")

# YOLO model
MODEL_PATH = os.getenv(
    "MODEL_PATH",
    os.path.join(BASE_DIR, "models", "best.pt")
)

# Detection confidence
CONFIDENCE_THRESHOLD = float(
    os.getenv("CONFIDENCE_THRESHOLD", "0.5")
)