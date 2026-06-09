import json
import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from android.action_executor_reference import (
    open_youtube_results,
    wait_for_package,
    tap_item,
    dump_ui
)

from modules.semantic_core import best

def wait_semantic_results():

    for i in range(12):

        result = dump_ui()

        xml = result.get("xml", "")

        if (
            "تشغيل الفيديو" in xml
            or "مشاهدة" in xml
            or "أحدث الفيديوهات" in xml
        ):
            return {
                "ok": True,
                "attempt": i + 1
            }

        time.sleep(1)

    return {
        "ok": False,
        "reason": "semantic_results_not_found"
    }

def confirm_video_opened():

    for i in range(10):

        result = dump_ui()

        xml = result.get("xml", "")

        opened = (
            "com.google.android.youtube" in xml
            and (
                "إيقاف مؤقت" in xml
                or "التالي" in xml
                or "مشترك" in xml
                or "إعجاب" in xml
                or "عدم الإعجاب" in xml
                or "تعليقات" in xml
                or "Share" in xml
                or "Pause" in xml
            )
        )

        if opened:
            return {
                "ok": True,
                "attempt": i + 1
            }

        time.sleep(1)

    return {
        "ok": False,
        "reason": "video_not_confirmed"
    }

def youtube_search_open_first(query):

    open_youtube_results(query)

    package = wait_for_package(
        "com.google.android.youtube"
    )

    if not package["ok"]:
        return package

    semantic = wait_semantic_results()

    if not semantic["ok"]:
        return semantic

    candidate = best("youtube")

    if not candidate:
        return {
            "ok": False,
            "reason": "no_candidate_found"
        }

    tap_item(candidate)

    confirmed = confirm_video_opened()

    return {
        "ok": confirmed["ok"],
        "query": query,
        "candidate": {
            "text": candidate["text"],
            "score": candidate["score"],
            "x": candidate["x"],
            "y": candidate["y"]
        },
        "confirm": confirmed
    }

if __name__ == "__main__":

    import sys

    query = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "OpenAI"
    )

    result = youtube_search_open_first(query)

    print(json.dumps(
        result,
        ensure_ascii=False,
        indent=2
    ))
