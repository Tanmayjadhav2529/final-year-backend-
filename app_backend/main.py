from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO

from config import MODEL_PATH
from routers import inspection, analytics, report


@asynccontextmanager
async def lifespan(app: FastAPI):

    # ============================================================
    # YOLO MODEL LOADING
    # ============================================================
    # During development, our teammate's trained model may not
    # exist yet. So we check whether the model file exists.
    # ============================================================

    if os.path.exists(MODEL_PATH):

        print(f"Loading YOLO model from {MODEL_PATH}...")

        app.state.model = YOLO(MODEL_PATH)

        print("YOLO model loaded successfully.")

    else:

        print("YOLO model not found.")
        print("Running in MOCK mode.")

        app.state.model = None

    yield

    print("Shutting down...")


app = FastAPI(
    title="Metal Defect Detection API",
    lifespan=lifespan
)


# Frontend ↔ Backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


# Inspection API
app.include_router(inspection.router)
app.include_router(analytics.router)
app.include_router(report.router)