from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from services.report_service import (
    get_inspection_report,
    generate_pdf_report
)


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/{inspection_id}")
def get_report(inspection_id: str):
    report = get_inspection_report(inspection_id)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Inspection not found"
        )

    return report


@router.get("/{inspection_id}/pdf")
def get_pdf_report(inspection_id: str):
    pdf_path = generate_pdf_report(inspection_id)

    if pdf_path is None:
        raise HTTPException(
            status_code=404,
            detail="Inspection not found"
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"inspection_report_{inspection_id}.pdf"
    )