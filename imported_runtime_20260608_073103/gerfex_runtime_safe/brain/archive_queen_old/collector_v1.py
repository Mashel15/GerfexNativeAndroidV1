import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default


query = Path("last_query.txt").read_text(encoding="utf-8").strip()
sources = load_json("selected_sources.json", ["memory"])

results = []

if "memory" in sources:
    results.append({
        "title": "Local Memory",
        "source": "memory",
        "description": "ذاكرة Gerfex المحلية"
    })

if "tech_news" in sources:
    q = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={q}&hl=ar&gl=SA&ceid=SA:ar"

    try:
        with urllib.request.urlopen(url, timeout=12) as r:
            data = r.read()

        root = ET.fromstring(data)

        for item in root.findall(".//item")[:6]:
            title = item.findtext("title") or "Untitled"
            link = item.findtext("link") or ""
            pub = item.findtext("pubDate") or ""

            results.append({
                "title": title,
                "source": "google_news",
                "description": pub,
                "link": link
            })

    except Exception as e:
        results.append({
            "title": "Google News fetch failed",
            "source": "error",
            "description": str(e)
        })

Path("collector_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("GERFEX COLLECTOR RESULTS\n")

for i, x in enumerate(results, 1):
    print(i, x.get("title", "?"))
    print(x.get("source", "?"))
    print(x.get("description", ""))
    print("-" * 30)
