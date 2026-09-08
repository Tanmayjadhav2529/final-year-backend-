from datetime import datetime
from pydantic import BaseModel
from typing import List


class Defect(BaseModel):
    class_name: str
    confidence: float
    bbox: List[float]


class Inspection(BaseModel):
    id: str
    timestamp: datetime
    verdict: str
    defects: List[Defect]
    image_path: str