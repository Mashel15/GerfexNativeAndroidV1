from pathlib import Path
import json

q = Path("last_query.txt").read_text(encoding="utf-8").lower()

sports = ["النصر", "الهلال", "كرة", "مباراة", "دوري"]
knowledge = ["من هو", "متى", "أين", "مؤسس"]

if any(x in q for x in sports):
    sources = ["official", "twitter", "sport_sites"]
elif any(x in q for x in knowledge):
    sources = ["wikipedia", "reference"]
elif any(x in q for x in [
    "أخبار", "اخبار", "خبر", "سامسونج", "ذكاء", "ai", "تقنية", "شات"
]):
    sources = ["tech_news", "twitter", "youtube"]
else:
    sources = ["tech_news"]

Path("selected_sources.json").write_text(
    json.dumps(sources, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("SELECTED SOURCES\n")
for x in sources:
    print("-", x)
