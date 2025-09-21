from fastapi import FastAPI, File, UploadFile
from worker.tasks import process_syllabus
import shutil, os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/generate")
async def generate(file: UploadFile = File(...), hours_per_week: int = 8, total_weeks: int = 12):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    res = process_syllabus(file_path, "pdf" if file.filename.lower().endswith(".pdf") else "docx",
                           user_constraints={"hours_per_week": hours_per_week, "total_weeks": total_weeks})
    return {"status": "done", "pdf": res["pdf"], "plan_summary": {"weeks": len(res["plan"]["weeks"])}}
