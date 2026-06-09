# Gerfex Semantic Core
# Merged from generic_semantic_engine_v1.py + screen_understanding.py

from pathlib import Path
import re
import json
import html

UI_XML = Path.home() / "storage/downloads/gerfex_ui.xml"

DEFAULT_PROFILE = {
    "positive": [],
    "negative": [],
    "navigation": [
        "الصفحة الرئيسية",
        "Shorts",
        "الاشتراكات",
        "أنت",
        "إنشاء",
        "HOME",
        "CTRL",
        "ALT",
        "ESC"
    ],
    "min_score": 1
}

YOUTUBE_PROFILE = {
    "positive": [
        "تشغيل الفيديو",
        "مشاهدة",
        "قبل",
        "أحدث الفيديوهات"
    ],
    "negative": [
        "إعلان",
        "Shorts",
        "الانتقال إلى القناة",
        "الاطّلاع على القناة",
        "البحث الصوتي",
        "معرفة المزيد",
        "تنزيل"
    ],
    "navigation": DEFAULT_PROFILE["navigation"],
    "min_score": 20
}

CHROME_PROFILE = {
    "positive": [
        "http",
        "https",
        "Search Results",
        "نتائج"
    ],
    "negative": [
        "Ad",
        "Sponsored",
        "إعلان"
    ],
    "navigation": DEFAULT_PROFILE["navigation"],
    "min_score": 10
}

PROFILES = {
    "default": DEFAULT_PROFILE,
    "youtube": YOUTUBE_PROFILE,
    "chrome": CHROME_PROFILE
}

def load_xml():
    if not UI_XML.exists():
        return ""
    return UI_XML.read_text(encoding="utf-8", errors="ignore")

def extract_items(xml):
    patterns = [
        re.compile(
            r'text="([^"]*)".+?bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"',
            re.DOTALL
        ),
        re.compile(
            r'content-desc="([^"]*)".+?bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"',
            re.DOTALL
        )
    ]

    items = []

    for pattern in patterns:
        for text, x1, y1, x2, y2 in pattern.findall(xml):
            text = html.unescape(text).strip()
            if not text:
                continue

            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

            items.append({
                "text": text,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "x": (x1 + x2) // 2,
                "y": (y1 + y2) // 2
            })

    return items

def classify_item(item, profile):
    text = item["text"]

    if any(n in text for n in profile.get("navigation", [])):
        return "navigation"

    if any(n in text for n in profile.get("negative", [])):
        return "negative"

    if any(p in text for p in profile.get("positive", [])):
        return "candidate"

    if len(text) > 45:
        return "possible_candidate"

    return "unknown"

def score_item(item, profile):
    text = item["text"]
    score = 0

    for p in profile.get("positive", []):
        if p in text:
            score += 40

    # Prefer full video title rows over small metadata labels
    if "تشغيل الفيديو" in text:
        score += 80

    # Penalize standalone view-count labels
    if "مشاهدة" in text and "تشغيل الفيديو" not in text and len(text) < 35:
        score -= 70

    for n in profile.get("negative", []):
        if n in text:
            score -= 80

    for nav in profile.get("navigation", []):
        if nav == text:
            score -= 100

    if len(text) > 45:
        score += 10

    if item["y"] > 2100:
        score -= 80

    if item["y"] < 220:
        score -= 30

    return score


def load_profile(profile_name):
    if profile_name == "youtube":
        return YOUTUBE_PROFILE

    if profile_name == "chrome":
        return CHROME_PROFILE

    return DEFAULT_PROFILE


def analyze(profile_name="default"):
    xml = load_xml()
    profile = load_profile(profile_name)

    raw_items = extract_items(xml)
    analyzed = []

    for item in raw_items:
        kind = classify_item(item, profile)
        score = score_item(item, profile)

        analyzed.append({
            **item,
            "kind": kind,
            "score": score
        })

    ranked = [
        x for x in analyzed
        if x["score"] >= profile.get("min_score", 1)
    ]

    ranked.sort(key=lambda x: x["score"], reverse=True)

    return {
        "profile": profile_name,
        "items_count": len(raw_items),
        "ranked_count": len(ranked),
        "ranked": ranked[:20]
    }

def best(profile_name="default"):
    result = analyze(profile_name)
    if not result["ranked"]:
        return None
    return result["ranked"][0]

if __name__ == "__main__":
    import sys

    profile = sys.argv[1] if len(sys.argv) > 1 else "youtube"

    print(json.dumps(
        analyze(profile),
        ensure_ascii=False,
        indent=2
    ))


# ---- screen understanding layer ----

from pathlib import Path
import re
import html

UI = Path.home() / "storage/downloads/gerfex_ui.xml"

def load_xml_for_screen():

    if not UI.exists():
        return ""

    return UI.read_text(
        encoding="utf-8",
        errors="ignore"
    )

def extract_texts(xml):

    values = []

    patterns = [
        r'text="([^"]+)"',
        r'content-desc="([^"]+)"'
    ]

    for pat in patterns:
        values.extend(
            re.findall(pat, xml)
        )

    clean = []

    blocked = {
        "",
        "ESC","CTRL","ALT","HOME",
        "END","PGUP","PGDN",
        "↑","↓","←","→",
        "☰","⇳","↹"
    }

    for v in values:

        v = html.unescape(v).strip()

        if v and v not in blocked:
            clean.append(v)

    return clean

def analyze_state():

    xml = load_xml_for_screen()

    texts = extract_texts(xml)

    state = {
        "package": None,
        "search_visible": False,
        "results_visible": False,
        "permission_dialog": False,
        "error_visible": False,
        "texts_count": len(texts),
        "top_texts": texts[:30]
    }

    if "com.google.android.youtube" in xml:
        state["package"] = "youtube"

    elif "com.android.chrome" in xml:
        state["package"] = "chrome"

    search_words = [
        "بحث",
        "Search"
    ]

    result_words = [
        "مشاهدة",
        "views",
        "نتائج",
        "results"
    ]

    permission_words = [
        "سماح",
        "Allow",
        "رفض",
        "Deny"
    ]

    error_words = [
        "خطأ",
        "Error",
        "Try again"
    ]

    for t in texts:

        low = t.lower()

        if any(w.lower() in low for w in search_words):
            state["search_visible"] = True

        if any(w.lower() in low for w in result_words):
            state["results_visible"] = True

        if any(w.lower() in low for w in permission_words):
            state["permission_dialog"] = True

        if any(w.lower() in low for w in error_words):
            state["error_visible"] = True

    return state

if __name__ == "__main__":

    import json

    print(
        json.dumps(
            analyze_state(),
            ensure_ascii=False,
            indent=2
        )
    )
