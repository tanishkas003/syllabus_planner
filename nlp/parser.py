import fitz  # PyMuPDF
from docx import Document
import re
import spacy

nlp_spacy = spacy.load("en_core_web_sm")


def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = []
    for page in doc:
        text.append(page.get_text("text"))
    return "\n".join(text)


def extract_text_from_docx(path):
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def normalize_text(text: str) -> str:
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()


def heuristic_split_sections(text: str):
    sections = []
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    cur = []
    for line in lines:
        if re.match(r"^(Module|Week|Unit|Chapter)\b", line, re.I) or (
            line.isupper() and len(line.split()) < 6
        ):
            if cur:
                sections.append("\n".join(cur))
            cur = [line]
        else:
            cur.append(line)
    if cur:
        sections.append("\n".join(cur))
    return sections


def extract_structured_syllabus(text: str):
    text = normalize_text(text)
    sections = heuristic_split_sections(text)
    modules = []
    for sec in sections:
        title = sec.splitlines()[0]
        content = "\n".join(sec.splitlines()[1:]).strip()
        lo = []
        m = re.search(
            r"(learning outcomes|learning objectives|outcomes)\s*[:\-]\s*(.*)",
            sec,
            re.I,
        )
        if m:
            lo = [s.strip() for s in re.split(r"[;\n]+", m.group(2)) if s.strip()]
        modules.append({"title": title, "content": content, "learning_objectives": lo})
    return {"raw_text": text, "modules": modules}
