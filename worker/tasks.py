import uuid
import os
from nlp.parser import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_structured_syllabus,
)
from nlp.decompose import decompose_topic, generate_cards_for_node
from nlp.scheduler import greedy_pack
from export.pdf_export import generate_pdf
from utils.config import DEFAULT_WEEKLY_HOURS, DEFAULT_TOTAL_WEEKS

# Folder where PDFs will be saved
PDF_DIR = "plans"
os.makedirs(PDF_DIR, exist_ok=True)


def process_syllabus(file_path, file_type="pdf", user_constraints=None):
    user_constraints = user_constraints or {}
    weekly_hours = user_constraints.get("hours_per_week", DEFAULT_WEEKLY_HOURS)
    total_weeks = user_constraints.get("total_weeks", DEFAULT_TOTAL_WEEKS)

    # Extract text from file
    if file_type == "pdf":
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_docx(file_path)

    # Parse structured syllabus
    structured = extract_structured_syllabus(text)

    # Decompose topics into nodes
    nodes = {}
    counter = 0
    for module in structured["modules"]:
        title = module["title"]
        context = module.get("content", "")
        subnodes = decompose_topic(title, context)
        for sn in subnodes:
            nid = f"n{counter}"
            nodes[nid] = {
                "title": sn.get("title") or sn.get("topic") or sn["title"],
                "objective": sn.get("objective", ""),
                "est_hours": sn.get("est_hours", 1),
                "difficulty": sn.get("difficulty", "mid"),
                "prerequisites": sn.get("prerequisites", []),
            }
            counter += 1

    # Schedule weeks
    weeks = greedy_pack(nodes, total_weeks=total_weeks, hours_per_week=weekly_hours)
    plan_weeks = []
    for week in weeks:
        week_topics = []
        for tid in week["topics"]:
            n = nodes[tid]
            n["cards"] = generate_cards_for_node(n)
            week_topics.append(n)
        plan_weeks.append({"topics": week_topics, "remaining": week["remaining"]})

    # Build final plan
    plan = {"course_title": structured.get("title", "Course"), "weeks": plan_weeks}

    filename = f"plan_{uuid.uuid4().hex[:8]}.pdf"
    pdf_path = os.path.join(PDF_DIR, filename)
    generate_pdf(plan, pdf_path)

    return {"plan": plan, "pdf": pdf_path}
