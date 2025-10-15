from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from worker.tasks import process_syllabus
import shutil, os

app = FastAPI()

# Directories
UPLOAD_DIR = "uploads"
TEMPLATES_DIR = "templates"
PDF_DIR = "plans"

# Ensure folders exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# Serve static PDFs
app.mount("/plans", StaticFiles(directory=PDF_DIR), name="plans")

@app.get("/", response_class=HTMLResponse)
async def home():
    html_path = Path(TEMPLATES_DIR) / "index.html"
    if html_path.exists():
        return html_path.read_text()
    return "<h1>Index file not found!</h1>"

@app.post("/generate")
async def generate(file: UploadFile = File(...), hours_per_week: int = 8, total_weeks: int = 12):
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Process syllabus and generate PDF
    res = process_syllabus(
        file_path,
        "pdf" if file.filename.lower().endswith(".pdf") else "docx",
        user_constraints={"hours_per_week": hours_per_week, "total_weeks": total_weeks},
    )

    # Build URL for generated PDF
    pdf_url = f"/plans/{Path(res['pdf']).name}"

    return {
        "status": "done",
        "pdf": pdf_url,
        "plan_summary": {"weeks": len(res["plan"]["weeks"])}
    }
