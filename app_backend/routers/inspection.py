from fastapi import APIRouter, File, UploadFile, Request

from services.inspection_service import save_image, run_inspection


router = APIRouter(
    prefix="/inspect",
    tags=["Inspection"]
)


@router.post("/")
async def inspect_image(
    request: Request,
    file: UploadFile = File(...)
):
    # Read uploaded image
    image_bytes = await file.read()

    # Save image locally
    image_path = save_image(
        image_bytes,
        file.filename
    )

    # Get YOLO model loaded in main.py
    model = request.app.state.model

    # Run inspection
    result = run_inspection(
        image=image_bytes,
        model=model
    )

    return {
        "image_path": image_path,
        **result
    }