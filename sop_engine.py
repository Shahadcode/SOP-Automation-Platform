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
- مع ذلك، لا تختصر المحتوى اختصاراً مخلاً، واحتفظ بجميع التفاصيل الجوهرية الواردة في النص.
"""
    else:
        mode_instruction = """
- المطلوب هو الاستخراج المباشر من النص المرفوع قدر الإمكان.
- لا تقم بإضافة معلومات غير موجودة إلا عند الضرورة القصوى.
- إذا كانت بعض البيانات غير موجودة، اتركها فارغة أو بصياغة محدودة جداً.
- لا تختصر المحتوى، ويجب الحفاظ على جميع التفاصيل الجوهرية الواردة في النص الأصلي.
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
- اجعل "title" هو عنوان الإجراء الفعلي المستخرج من النص.
- اجعل "introduction" فقرة متكاملة وواضحة.
- لا تختصر الإجراء إذا كان النص يحتوي على تفاصيل كثيرة.
- يجب المحافظة على أكبر قدر ممكن من المحتوى الوارد في النص المرفوع.
- إذا كان النص يحتوي على العديد من الخطوات أو المسؤوليات، أعدها جميعاً داخل "steps" ولا تكتفِ بثلاث خطوات فقط.
- يمكن أن تحتوي "steps" على أي عدد مناسب من الخطوات بحسب النص.
- اجعل "systems" قائمة JSON من النقاط الكاملة فقط.
- اجعل "objective" قائمة JSON من النقاط الكاملة فقط.
- اجعل "matching_logic" قائمة JSON من النقاط الكاملة فقط.
- يجب أن تكون "systems" و "objective" و "matching_logic" على شكل نقاط Bullet فقط.
- لا تستخدم الترقيم 1، 2، 3 داخل هذه القوائم.
- كل عنصر يجب أن يكون جملة مستقلة مختصرة وواضحة.
- لا تجعل "systems" أو "objective" أو "matching_logic" نصاً واحداً أو فقرة واحدة.
- إذا لم يذكر النص الأنظمة بشكل مباشر، استخرج الأنظمة المحتملة المرتبطة بالإجراء فقط إذا كانت واضحة من السياق.
- اجعل كل خطوة في "steps" قابلة للتنفيذ ومرتبطة بالنص الأصلي.
- حقل "responsibility" يجب أن يحتوي على الجهة أو القسم أو الشخص المسؤول عن تنفيذ الخطوة.
- حقل "procedure" يجب أن يحتوي على نص الإجراء التفصيلي الخاص بتلك الخطوة.
- حقل "tools" يجب أن يحتوي على الأدوات أو النماذج أو المستندات المستخدمة في الخطوة إن وجدت، وإلا اتركه فارغاً.
- لا تستخدم اللغة الإنجليزية إلا إذا كان اسم نظام أو مصطلحاً ثابتاً.
- لا تترك placeholders مثل [عنوان الإجراء] أو [الترميز] أو أي نص شكلي مشابه.
- أخرج JSON صالحاً فقط.

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
