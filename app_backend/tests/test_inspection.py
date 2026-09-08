import io
import json
import os

from fastapi.testclient import TestClient

from main import app
from config import DATA_DIR


def test_invalid_file_type():

    with TestClient(app) as client:

        file = io.BytesIO(b"not an image")

        response = client.post(
            "/inspect/",
            files={
                "file": (
                    "test.txt",
                    file,
                    "text/plain"
                )
            }
        )

        assert response.status_code == 400
        assert response.json()["detail"] == (
            "Only JPG, JPEG, and PNG images are allowed."
        )


def test_empty_file():

    with TestClient(app) as client:

        file = io.BytesIO(b"")

        response = client.post(
            "/inspect/",
            files={
                "file": (
                    "empty.png",
                    file,
                    "image/png"
                )
            }
        )

        assert response.status_code == 400
        assert response.json()["detail"] == (
            "Uploaded file is empty."
        )


def test_file_too_large():

    with TestClient(app) as client:

        # Create a file slightly larger than 5 MB
        large_file = io.BytesIO(
            b"x" * (5 * 1024 * 1024 + 1)
        )

        response = client.post(
            "/inspect/",
            files={
                "file": (
                    "large.png",
                    large_file,
                    "image/png"
                )
            }
        )

        assert response.status_code == 413
        assert response.json()["detail"] == (
            "Image size must be less than 5 MB."
        )