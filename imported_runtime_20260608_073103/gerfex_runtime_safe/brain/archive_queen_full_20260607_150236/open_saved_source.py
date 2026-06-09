import json
import re
import urllib.parse
from pathlib import Path

from android_bridge import open_url


def open_saved_source(command: str):
    m = re.search(r"\d+", command or "")
    index = int(m.group()) if m else 1

    data_path = Path("ranked_results.json")

    if not data_path.exists():
        return {"ok": False, "reply": "لا توجد نتائج محفوظة. ابحث أولًا."}

    data = json.loads(data_path.read_text(encoding="utf-8"))

    if index < 1 or index > len(data):
        return {"ok": False, "reply": f"لا توجد نتيجة رقم {index}."}

    item = data[index - 1]
    title = item.get("title", "خبر")
    q = urllib.parse.quote(title)
    short_url = f"https://www.google.com/search?q={q}"

    res = open_url(short_url)

    return {
        "ok": True,
        "reply": f"فتحت بحثًا قصيرًا عن النتيجة {index}: {title}",
        "queued": res
    }


if __name__ == "__main__":
    import sys
    command = " ".join(sys.argv[1:]) or "افتح 1"
    print(open_saved_source(command))
