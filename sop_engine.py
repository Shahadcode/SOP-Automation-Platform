import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_sop_data(text, department, language="Arabic", mode="extract"):
    mode_instruction = ""
    if mode == "rewrite":
        mode_instruction = """
- المطلوب هو إعادة صياغة المحتوى بشكل مهني ورسمي ليتوافق مع النموذج الرسمي المختصر المعتمد.
- يجب ضغط المحتوى بذكاء داخل الحقول المتاحة فقط دون الإخلال بالمعنى.
"""
    else:
        mode_instruction = """
- المطلوب هو استخراج المحتوى من النص المرفوع وإعادة تنظيمه ليتوافق مع النموذج الرسمي المختصر المعتمد.
- يجب ضغط المحتوى بذكاء داخل الحقول المتاحة فقط دون الإخلال بالمعنى.
"""

    prompt = f"""
أنت خبير محترف في إعداد الإجراءات التشغيلية القياسية في البنوك.

النموذج النهائي ثابت ورسمي ولا يمكن تغييره.
يجب عليك إعادة تنظيم النص المرفوع ليتناسب فقط مع الحقول التالية الموجودة في النموذج الرسمي:
- عنوان الإجراء
- المقدمة
- الأنظمة المشاركة
- هدف الإجراء
- منطق المطابقة
- 3 خطوات فقط داخل جدول الإجراء

لا تنشئ أقساماً إضافية مستقلة.
بدلاً من ذلك:
- قم بدمج نطاق التطبيق والتعريف ضمن "المقدمة"
- قم بدمج الشروط والضوابط ضمن "منطق المطابقة"
- قم بدمج المسؤوليات والمستندات والمتابعة ضمن خطوات الإجراء الثلاث

{mode_instruction}

أعد النتيجة بصيغة JSON فقط، بهذا الشكل تماماً:

{{
  "title": "",
  "code": "",
  "department": "{department}",
  "version": "01",
  "issue_date": "",
  "circular_date": "",
  "approval_entity": "",
  "approval_date": "",
  "signature": "",
  "main_references": "",
  "used_forms": "",
  "procedure_owner": "",
  "quality_management": "",
  "authorized_manager": "",
  "introduction": "",
  "systems": [""],
  "objective": [""],
  "matching_logic": [""],
  "steps": [
    {{
      "no": "1",
      "responsibility": "",
      "procedure": "",
      "tools": ""
    }},
    {{
      "no": "2",
      "responsibility": "",
      "procedure": "",
      "tools": ""
    }},
    {{
      "no": "3",
      "responsibility": "",
      "procedure": "",
      "tools": ""
    }}
  ]
}}

التعليمات:
- جميع المخرجات بالعربية الرسمية فقط.
- "title" هو عنوان الإجراء الفعلي.
- "code" يترك فارغاً إذا لم يذكر في النص.
- "introduction" فقرة شاملة ومكثفة تتضمن الهدف العام + نطاق التطبيق + التعريف عند الحاجة.
- "systems" نقاط مختصرة فقط بدون ترقيم.
- "objective" نقاط مختصرة فقط بدون ترقيم.
- "matching_logic" نقاط مختصرة فقط بدون ترقيم وتشمل أهم الشروط والضوابط.
- "steps" يجب أن تكون 3 فقط لا غير.
- الخطوة 1 = الاستلام / التحقق / المراجعة الأولية
- الخطوة 2 = المعالجة / التسجيل / التنفيذ
- الخطوة 3 = المتابعة / المراجعة / التسوية / الإقفال
- "tools" تحتوي على الأدوات أو المستندات المتعلقة بكل خطوة.
- لا تكتب أي نص خارج JSON.

النص:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()
    elif content.startswith("```"):
        content = content.replace("```", "").strip()

    return json.loads(content)
