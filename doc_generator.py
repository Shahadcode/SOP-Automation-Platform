import os
from datetime import datetime
from docx import Document
from docx.text.paragraph import Paragraph
from docx.oxml import OxmlElement


def replace_text_in_paragraphs(doc, replacements):
    for p in doc.paragraphs:
        for key, value in replacements.items():
            if key in p.text:
                p.text = p.text.replace(key, value)


def replace_text_in_tables(doc, replacements):
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for key, value in replacements.items():
                        if key in paragraph.text:
                            paragraph.text = paragraph.text.replace(key, value)


def normalize_items(items):
    if items is None:
        return [""]

    if isinstance(items, str):
        text = items.strip()
        if not text:
            return [""]
        return [line.strip("•- \n\r\t") for line in text.splitlines() if line.strip()]

    if isinstance(items, list):
        cleaned = []
        for item in items:
            if item is None:
                continue
            item_str = str(item).strip()
            if item_str:
                cleaned.append(item_str)
        return cleaned if cleaned else [""]

    return [str(items).strip()] if str(items).strip() else [""]


def replace_placeholder_with_lines(doc, placeholder, items):
    clean_items = normalize_items(items)

    for p in doc.paragraphs:
        if placeholder in p.text:
            first_line = clean_items[0]
            p.text = p.text.replace(placeholder, first_line)

            current_p = p
            for item in clean_items[1:]:
                new_p = current_p.insert_paragraph_after(item)
                current_p = new_p
            return

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if placeholder in p.text:
                        first_line = clean_items[0]
                        p.text = p.text.replace(placeholder, first_line)

                        current_p = p
                        for item in clean_items[1:]:
                            new_p = current_p.insert_paragraph_after(item)
                            current_p = new_p
                        return


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


def create_sop_doc_from_template(data):
    add_insert_paragraph_after()

    template_path = "templates/arabic_sop_template_placeholders.docx"
    doc = Document(template_path)

    os.makedirs("outputs", exist_ok=True)

    replacements = {
        "[عنوان الإجراء]": data.get("title", ""),
        "[القسم]": data.get("department", ""),
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

    for i in range(1, 9):
        step_data = steps[i - 1] if i <= len(steps) else {}
        step_replacements = {
            f"[رقم {i}]": str(step_data.get("no", i if i <= 3 else "")),
            f"[المسؤولية {i}]": step_data.get("responsibility", ""),
            f"[الإجراء {i}]": step_data.get("procedure", ""),
            f"[الأدوات {i}]": step_data.get("tools", ""),
        }
        replace_text_in_paragraphs(doc, step_replacements)
        replace_text_in_tables(doc, step_replacements)

    file_name = f"outputs/SOP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    doc.save(file_name)
    return file_name
