import os
import re
from datetime import datetime
from docx import Document
from docx.text.paragraph import Paragraph
from docx.oxml import OxmlElement


def replace_in_runs(paragraph, placeholder, value):
    if value is None:
        value = ""
    value = str(value)

    if not paragraph.runs:
        if placeholder in paragraph.text:
            paragraph.text = paragraph.text.replace(placeholder, value)
        return

    full_text = "".join(run.text for run in paragraph.runs)
    if placeholder not in full_text:
        return

    new_text = full_text.replace(placeholder, value)
    paragraph.runs[0].text = new_text
    for run in paragraph.runs[1:]:
        run.text = ""


def replace_text_in_paragraphs(doc, replacements):
    for p in doc.paragraphs:
        for key, value in replacements.items():
            replace_in_runs(p, key, value)


def replace_text_in_tables(doc, replacements):
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for key, value in replacements.items():
                        replace_in_runs(paragraph, key, value)


def add_insert_paragraph_after():
    def insert_paragraph_after(self, text=None, style=None):
        new_p = OxmlElement("w:p")
        self._p.addnext(new_p)
        paragraph = Paragraph(new_p, self._parent)
        if text:
            paragraph.add_run(text)
        if style is not None:
            paragraph.style = style
        return paragraph

    Paragraph.insert_paragraph_after = insert_paragraph_after


def normalize_items(items):
    if items is None:
        return []

    if isinstance(items, str):
        text = items.strip()
        if not text:
            return []
        lines = [line.strip() for line in text.splitlines() if line.strip()]
    elif isinstance(items, list):
        lines = [str(item).strip() for item in items if str(item).strip()]
    else:
        lines = [str(items).strip()] if str(items).strip() else []

    cleaned = []
    for line in lines:
        line = re.sub(r"^[•\-\*]+\s*", "", line)
        line = re.sub(r"^[0-9٠-٩]+\s*[\.\)\-]\s*", "", line)
        cleaned.append(line.strip())

    return cleaned


def replace_placeholder_with_lines(doc, placeholder, items):
    clean_items = normalize_items(items)
    bullet_items = [f"• {item}" for item in clean_items if item]

    if not bullet_items:
        bullet_items = [""]

    for p in doc.paragraphs:
        full_text = "".join(run.text for run in p.runs) if p.runs else p.text
        if placeholder in full_text:
            replace_in_runs(p, placeholder, bullet_items[0])
            current_p = p
            for item in bullet_items[1:]:
                current_p = current_p.insert_paragraph_after(item, style=p.style)
            return

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    full_text = "".join(run.text for run in p.runs) if p.runs else p.text
                    if placeholder in full_text:
                        replace_in_runs(p, placeholder, bullet_items[0])
                        current_p = p
                        for item in bullet_items[1:]:
                            current_p = current_p.insert_paragraph_after(item, style=p.style)
                        return


def create_sop_doc_from_template(data):
    add_insert_paragraph_after()

    template_path = "templates/arabic_sop_template_placeholders.docx"
    doc = Document(template_path)

    os.makedirs("outputs", exist_ok=True)

    replacements = {
        "[عنوان الإجراء]": data.get("title", ""),
        "[الترميز]": data.get("code", ""),
        "[الإصدار]": data.get("version", "01"),
        "[تاريخ الإصدار]": data.get("issue_date", ""),
        "[تاريخ التعميم]": data.get("circular_date", ""),
        "[جهة الاعتماد]": data.get("approval_entity", ""),
        "[تاريخ الاعتماد]": data.get("approval_date", ""),
        "[التوقيع]": data.get("signature", ""),
        "[المراجع الرئيسية]": data.get("main_references", ""),
        "[النماذج المستخدمة]": data.get("used_forms", ""),
        "[صاحب الإجراء]": data.get("procedure_owner", ""),
        "[إدارة الجودة]": data.get("quality_management", ""),
        "[المدير المفوض]": data.get("authorized_manager", ""),
        "[المقدمة]": data.get("introduction", ""),
    }

    replace_text_in_paragraphs(doc, replacements)
    replace_text_in_tables(doc, replacements)

    replace_placeholder_with_lines(doc, "[الأنظمة]", data.get("systems", []))
    replace_placeholder_with_lines(doc, "[الهدف]", data.get("objective", []))
    replace_placeholder_with_lines(doc, "[المطابقة]", data.get("matching_logic", []))

    steps = data.get("steps", [])
    for i in range(1, 4):
        step_data = steps[i - 1] if i <= len(steps) else {}
        step_replacements = {
            f"[المسؤولية {i}]": step_data.get("responsibility", ""),
            f"[الإجراء {i}]": step_data.get("procedure", ""),
            f"[الأدوات {i}]": step_data.get("tools", ""),
        }
        replace_text_in_paragraphs(doc, step_replacements)
        replace_text_in_tables(doc, step_replacements)

    file_name = f"outputs/SOP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    doc.save(file_name)
    return file_name
