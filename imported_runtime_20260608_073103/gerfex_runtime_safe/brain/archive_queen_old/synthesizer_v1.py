import json
from pathlib import Path


f = Path("ranked_results.json")

if not f.exists():
    f = Path("collector_results.json")

if not f.exists():
    print("NO RESULTS TO SYNTHESIZE")
    raise SystemExit(0)


try:
    data = json.loads(f.read_text(encoding="utf-8"))
except Exception:
    data = []


print("\nGERFEX ANSWER\n")

if not data:
    print("لم أجد نتائج كافية لبناء إجابة.")
    raise SystemExit(0)


top = data[:3]

print("وجدت عدة نتائج مرتبطة بالطلب. أفضل النتائج الحالية:\n")

for i, item in enumerate(top, 1):
    title = item.get("title", "بدون عنوان")
    source = item.get("source", "unknown")
    date = item.get("description", "")
    link = item.get("link", "")

    print(f"{i}. {title}")
    print(f"   المصدر: {source}")

    if date:
        print(f"   التاريخ: {date}")

    if link:
        print(f"   الرابط: {link}")

    print()


print("الخلاصة:")
print("هذه نتائج أولية من مصادر أخبار فعلية.")
print("يمكنك اختيار نتيجة لفتحها لاحقًا.")

print()
print("يمكنك قول:")
print("افتح 1")
print("افتح 2")
print("افتح 3")
