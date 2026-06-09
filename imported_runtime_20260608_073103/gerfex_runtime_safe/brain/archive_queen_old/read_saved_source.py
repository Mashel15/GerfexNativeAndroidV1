import json
from pathlib import Path


data = json.loads(Path("ranked_results.json").read_text(encoding="utf-8"))

item = data[0]

title = item.get("title", "بدون عنوان")
source = item.get("source", "unknown")
date = item.get("description", "")
link = item.get("link", "")

summary = f"""ملخص أولي للخبر:

العنوان:
{title}

المصدر:
{source}

التاريخ:
{date}

الفهم المبدئي:
هذا الخبر مرتبط بموضوع الذكاء الاصطناعي، ويبدو أنه يتناول جانبًا من التحذيرات أو المخاوف المرتبطة بتأثيرات الذكاء الاصطناعي. هذه قراءة أولية مبنية على بيانات البحث، وليست قراءة كاملة للمقال.

الرابط:
{link}

الخطوة التالية:
يمكن فتح المصدر في المتصفح أو البحث بعنوان الخبر للوصول إلى النص الكامل.
"""

Path("article_summary.txt").write_text(summary, encoding="utf-8")

print(summary)
