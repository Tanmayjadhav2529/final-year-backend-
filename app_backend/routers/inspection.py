from fastapi import APIRouter, File, UploadFile, Request, HTTPException

from services.inspection_service import save_image, run_inspection


router = APIRouter(
    prefix="/inspect",
    tags=["Inspection"]
)


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("/")
async def inspect_image(
    request: Request,
    file: UploadFile = File(...)
):

    # Check file extension
    filename = file.filename or ""
    extension = filename.lower().rsplit(".", 1)[-1]

    if f".{extension}" not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG, and PNG images are allowed."
        )

    # Read uploaded file
    image_bytes = await file.read()

    # Check file size
    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image size must be less than 5 MB."
        )

    # Check empty file
    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # Save image locally
    image_path = save_image(
        image_bytes,
        filename
    )

    # Get YOLO model loaded in main.py
    model = request.app.state.model

    # Run inspection
    result = run_inspection(
        image=image_bytes,
        model=model,
        image_path=image_path
    )

    return {
        "image_path": image_path,
        **result
    }