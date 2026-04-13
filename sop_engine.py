import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_sop_data(text, department, language="Arabic", mode="extract"):
    mode_instruction = ""
    if mode == "rewrite":
        mode_instruction = """
- المطلوب هو إعادة صياغة المحتوى بشكل مهني ورسمي ومحسن.
- يمكن تحسين الأسلوب، الترتيب، والوضوح مع الحفاظ على المعنى.
"""
    else:
        mode_instruction = """
- المطلوب هو الاستخراج المباشر من النص المرفوع قدر الإمكان.
- لا تقم بإضافة معلومات غير موجودة إلا عند الضرورة القصوى.
- إذا كانت بعض البيانات غير موجودة، اتركها فارغة أو بصياغة محدودة جداً.
"""

    prompt = f"""
أنت خبير محترف في إعداد الإجراءات التشغيلية القياسية في البنوك.

حوّل النص التالي إلى بيانات منظمة بصيغة JSON فقط، بدون أي شرح إضافي.
يجب أن تكون جميع النتائج باللغة العربية الرسمية المهنية.
يجب أن يكون الأسلوب مناسباً للاعتماد والتدقيق الداخلي والخارجي.
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
      "responsibility": "الموظف",
      "procedure": "",
      "tools": ""
    }}
  ]
}}

التعليمات:
- جميع المخرجات بالعربية فقط.
- استخدم لغة مصرفية رسمية وواضحة.
- اجعل "المقدمة" فقرة متكاملة.
- اجعل "الأنظمة المشاركة" قائمة JSON من نقاط كاملة.
- اجعل "هدف الاجراء" قائمة JSON من نقاط كاملة.
- اجعل "منطق المطابقة" قائمة JSON من النقاط، وليس نصاً واحداً.
- يجب أن تكون كل نقطة في "منطق المطابقة" جملة كاملة وواضحة.
- اجعل الخطوات قابلة للتنفيذ.
- لا تستخدم اللغة الإنجليزية إلا إذا كان اسم نظام أو مصطلحاً ثابتاً.

النص:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()
    elif content.startswith("```"):
        content = content.replace("```", "").strip()

    return json.loads(content)
