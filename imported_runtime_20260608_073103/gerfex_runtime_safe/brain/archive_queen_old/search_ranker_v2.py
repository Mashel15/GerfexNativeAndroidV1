import json
from pathlib import Path
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone


query = Path("last_query.txt").read_text(encoding="utf-8").lower()

data = json.loads(
    Path("collector_results.json").read_text(encoding="utf-8")
)

important_terms = [
    "ذكاء",
    "اصطناعي",
    "ai",
    "أخبار",
    "اخبار",
    "بحث",
]


trusted_sources = [
    "الجزيرة",
    "رويترز",
    "bbc",
    "cnn",
    "mastercard",
    "ibm",
    "google",
    "openai",
    "microsoft",
]


def recency_score(pub):
    if not pub:
        return 0

    try:
        dt = parsedate_to_datetime(pub)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        days = (now - dt).days

        if days <= 1:
            return 30
        if days <= 3:
            return 20
        if days <= 7:
            return 10
    except Exception:
        return 0

    return 0


def score(item):
    title = item.get("title", "").lower()
    src = item.get("source", "").lower()
    desc = item.get("description", "")

    s = 0

    if src == "google_news":
        s += 30

    for term in important_terms:
        if term in title or term in query:
            s += 8

    for word in query.split():
        if len(word) > 2 and word in title:
            s += 5

    for trusted in trusted_sources:
        if trusted in title:
            s += 20

    s += recency_score(desc)

    return s


for x in data:
    x["score"] = score(x)

ranked = sorted(
    data,
    key=lambda x: x["score"],
    reverse=True
)

Path("ranked_results.json").write_text(
    json.dumps(ranked, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("\nRANKED RESULTS:\n")

for i, x in enumerate(ranked, 1):
    print(f"{i}.", x.get("title", "?"))
    print("score:", x.get("score", 0))
    print("source:", x.get("source", "?"))
    print()
