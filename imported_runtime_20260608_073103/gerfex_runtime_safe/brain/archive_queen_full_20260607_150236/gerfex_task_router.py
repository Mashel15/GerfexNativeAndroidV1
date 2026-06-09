import subprocess
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
try:
    from skills.skill_registry import execute_goal
except Exception:
    execute_goal = None

def extract_topic(prompt: str):
    text = prompt or ""

    remove_words = [
        "تابع", "آخر", "اخر", "أخبار", "اخبار",
        "وافتح", "افتح", "أهم نتيجة", "اهم نتيجة",
        "ثم", "لخصها", "لخص", "أعطني", "اعطني",
        "أهم خبر", "اهم خبر"
    ]

    for w in remove_words:
        text = text.replace(w, "")

    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return "أخبار الذكاء الاصطناعي"

    return "أخبار " + text

def run_task(prompt: str):
    text = (prompt or "").lower().strip()

    if "يوتيوب" in text or "youtube" in text:
        query = prompt
        for w in ["ابحث في يوتيوب عن", "ابحث يوتيوب عن", "افتح يوتيوب عن", "وافتح أول نتيجة", "وافتح اول نتيجة", "افتح أول نتيجة", "افتح اول نتيجة"]:
            query = query.replace(w, "")
        query = query.strip(" ؟?،,.")

        if execute_goal:
            result = execute_goal("youtube.search.open_first", {"query": query})
            return {
                "ok": result.get("ok", False),
                "reply": "نفذت بحث يوتيوب وفتحت أول نتيجة." if result.get("ok") else "حاولت تنفيذ يوتيوب لكن لم يكتمل التأكيد.",
                "result": result
            }

        return {
            "ok": False,
            "reply": "سجل المهارات غير متاح حاليًا."
        }

    if (
        "أخبار" in text
        or "اخبار" in text
        or "خبر" in text
        or "ai news" in text
    ):
        topic = extract_topic(prompt)

        r = subprocess.run(
            ["python", "autonomous_news.py", topic],
            capture_output=True,
            text=True
        )

        return {
            "ok": r.returncode == 0,
            "reply": r.stdout.strip()[-4000:] or "تم تنفيذ مهمة الأخبار.",
            "error": r.stderr.strip()
        }

    return {
        "ok": False,
        "reply": "لم أتعرف على مهمة مركبة مناسبة لهذا الطلب."
    }

if __name__ == "__main__":
    import sys
    prompt = " ".join(sys.argv[1:]) or "تابع أخبار الذكاء الاصطناعي وافتح أهم نتيجة ثم لخصها"
    print(run_task(prompt)["reply"])
