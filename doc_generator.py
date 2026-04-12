from docx import Document
from datetime import datetime
import os


def replace_text_in_paragraphs(doc, replacements):
    for p in doc.paragraphs:
        for key, value in replacements.items():
            if key in p.text:
                for run in p.runs:
                    run.text = run.text.replace(key, value)


def replace_text_in_tables(doc, replacements):
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for key, value in replacements.items():
                        if key in p.text:
                            for run in p.runs:
                                run.text = run.text.replace(key, value)


def join_list(items):
    return "\n".join([f"• {item}" for item in items if item.strip()])


def create_sop_doc_from_template(data):
    os.makedirs("outputs", exist_ok=True)

    template_path = "templates/arabic_sop_template_placeholders.docx"
    doc = Document(template_path)

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

        "[الأنظمة]": join_list(data.get("systems", [])),
        "[الهدف]": join_list(data.get("objective", [])),
        "[المطابقة]": join_list(data.get("matching_logic", [])),
    }

    replace_text_in_paragraphs(doc, replacements)
    replace_text_in_tables(doc, replacements)

    steps = data.get("steps", [])

    for i in range(1, 9):
        step_data = steps[i - 1] if i <= len(steps) else {}

        step_replacements = {
            f"[رقم {i}]": str(step_data.get("no", "")),
            f"[المسؤولية {i}]": step_data.get("responsibility", ""),
            f"[الإجراء {i}]": step_data.get("procedure", ""),
            f"[الأدوات {i}]": step_data.get("tools", ""),
        }

        replace_text_in_paragraphs(doc, step_replacements)
        replace_text_in_tables(doc, step_replacements)

    file_name = f"outputs/SOP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    doc.save(file_name)

    return file_name
