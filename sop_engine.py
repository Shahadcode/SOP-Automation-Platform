import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_sop_data(text, department, language="Arabic", mode="extract"):
    mode_instruction = ""
    if mode == "rewrite":
        mode_instruction = """
- المطلوب هو إعادة صياغة المحتوى بشكل مهني ورسمي ومحسن.
- لا يجوز اختصار المحتوى اختصاراً مخلاً.
- يجب الحفاظ على جميع الأقسام والتفاصيل والخطوات الواردة في النص.
"""
    else:
        mode_instruction = """
- المطلوب هو الاستخراج المباشر من النص المرفوع دون اختصار.
- لا تقم بتلخيص المحتوى.
- يجب الحفاظ على جميع الأقسام والتفاصيل والخطوات الواردة في النص الأصلي.
- لا تحذف أي جزء جوهري من المحتوى.
"""

    prompt = f"""
أنت خبير محترف في إعداد الإجراءات التشغيلية القياسية في البنوك.

حوّل النص التالي إلى بيانات منظمة بصيغة JSON فقط، بدون أي شرح إضافي.
يجب أن تكون جميع النتائج باللغة العربية الرسمية المهنية.
لا تكتب أي نص خارج JSON.

{mode_instruction}

أعد النتيجة بهذا الشكل تماماً:

{{
  "title": "",
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
  "scope": [
    ""
  ],
  "definition": "",
  "responsibilities": [
    {{
      "party": "",
      "details": [
        ""
      ]
    }}
  ],
  "classification_conditions": [
    ""
  ],
  "systems": [
    ""
  ],
  "objective": [
    ""
  ],
  "matching_logic": [
    ""
  ],
  "steps": [
    {{
      "no": "1",
      "responsibility": "",
      "procedure": "",
      "tools": ""
    }}
  ],
  "controls": [
    ""
  ],
  "documents_used": [
    ""
  ],
  "required_reports": [
    ""
  ]
}}

التعليمات:
- استخرج جميع الأقسام الموجودة في النص، ولا تختصرها.
- إذا كان النص يحتوي على "نطاق التطبيق" فضعه في "scope".
- إذا كان النص يحتوي على "التعريف" فضعه في "definition".
- إذا كان النص يحتوي على "المسؤوليات" فاستخرج جميع الجهات والمسؤوليات بالتفصيل داخل "responsibilities".
- إذا كان النص يحتوي على "شروط" أو "شروط التصنيف" فضعها في "classification_conditions".
- إذا كان النص يحتوي على "الضوابط الرقابية" فضعها في "controls".
- إذا كان النص يحتوي على "المستندات المستخدمة" فضعها في "documents_used".
- إذا كان النص يحتوي على "التقارير المطلوبة" فضعها في "required_reports".
- يجب أن تحتوي "steps" على جميع الخطوات المذكورة في النص، بما فيها الخطوات الفرعية إن وجدت.
- لا تكتفِ بثلاث خطوات فقط.
- يمكن أن تحتوي "steps" على أي عدد مناسب بحسب النص.
- اجعل "systems" و "objective" و "matching_logic" و "scope" و "classification_conditions" و "controls" و "documents_used" و "required_reports" قوائم JSON من نقاط كاملة.
- لا تستخدم الترقيم 1، 2، 3 داخل القوائم النصية.
- لا تختصر الفقرات أو النقاط.
- لا تترك placeholders مثل [عنوان الإجراء].
- أخرج JSON صالحاً فقط.

النص:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()
    elif content.startswith("```"):
        content = content.replace("```", "").strip()

    return json.loads(content)
