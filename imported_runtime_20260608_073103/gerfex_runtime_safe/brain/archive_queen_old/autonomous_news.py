import subprocess
import sys
from pathlib import Path

topic = " ".join(sys.argv[1:]).strip() or "أخبار الذكاء الاصطناعي"
query = "ابحث عن " + topic

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

print("GERFEX AUTONOMOUS NEWS TASK")

run(["python", "gerfex_goal_loop_core.py", query])
run(["python", "open_saved_source.py", "افتح 1"])
summary = run(["python", "summarize_saved_source.py", "لخص 1"])

final = [
    "تم تنفيذ مهمة الأخبار.",
    "",
    "الموضوع:",
    topic,
    "",
    "النتيجة المختارة:",
    "تم اختيار أفضل نتيجة حسب ترتيب Gerfex.",
    ""
]

if Path("article_summary.txt").exists():
    final.append(Path("article_summary.txt").read_text(encoding="utf-8"))
else:
    final.append(summary.stdout.strip() or "لم أستطع بناء ملخص.")

final += [
    "",
    "حالة الفتح:",
    "تم إرسال أمر فتح النتيجة إلى المتصفح حسب سياسة Gerfex الرسمية."
]

print("\n".join(final))
