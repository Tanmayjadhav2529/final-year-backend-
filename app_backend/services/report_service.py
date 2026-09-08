import os

from services.data_service import get_all_inspections

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from config import DATA_DIR


def get_inspection_report(inspection_id: str):
    inspections = get_all_inspections()

    for inspection in inspections:
        if inspection["id"] == inspection_id:
            return {
                "inspection_id": inspection["id"],
                "timestamp": inspection["timestamp"],
                "verdict": inspection["verdict"],
                "defects": inspection.get("defects", []),
                "image_path": inspection.get("image_path")
            }

    return None

def generate_pdf_report(inspection_id: str):
    report = get_inspection_report(inspection_id)

    if report is None:
        return None

    os.makedirs(DATA_DIR, exist_ok=True)

    pdf_path = os.path.join(
        DATA_DIR,
        f"inspection_report_{inspection_id}.pdf"
    )

    pdf = canvas.Canvas(pdf_path, pagesize=A4)

    width, height = A4

    # Title
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, height - 50, "Metal Inspection Report")

    # Basic information
    pdf.setFont("Helvetica", 11)

    y = height - 90

    pdf.drawString(50, y, f"Inspection ID: {report['inspection_id']}")
    y -= 25

    pdf.drawString(50, y, f"Timestamp: {report['timestamp']}")
    y -= 25

    pdf.drawString(50, y, f"Verdict: {report['verdict']}")
    y -= 40

    # Defects
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Detected Defects")
    y -= 25

    pdf.setFont("Helvetica", 11)

    if report["defects"]:
        for defect in report["defects"]:
            pdf.drawString(
                60,
                y,
                f"Class: {defect['class_name']}"
            )
            y -= 20

            pdf.drawString(
                60,
                y,
                f"Confidence: {defect['confidence']:.2f}"
            )
            y -= 20

            pdf.drawString(
                60,
                y,
                f"Bounding Box: {defect['bbox']}"
            )
            y -= 30
    else:
        pdf.drawString(60, y, "No defects detected.")
        y -= 30

    # Image
    image_path = report.get("image_path")

    if image_path and os.path.exists(image_path):
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(50, y, "Inspection Image")
        y -= 20

        try:
            image = ImageReader(image_path)
            pdf.drawImage(
                image,
                50,
                max(50, y - 250),
                width=300,
                height=220,
                preserveAspectRatio=True,
                anchor="c"
            )
        except Exception:
            pdf.drawString(50, y, "Unable to load inspection image.")

    pdf.save()

    return pdf_path