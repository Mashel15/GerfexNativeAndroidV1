import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEARNING = ROOT / "learning"

PENDING = LEARNING / "pending_lessons.json"
APPROVED = LEARNING / "approved_knowledge.json"
REJECTED = LEARNING / "rejected_lessons.json"


def load(path):
    if not path.exists():
        return {"items": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"items": []}


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def extract_lesson(text):
    t = (text or "").strip()
    if not t:
        return None

    signals = [
        "لا تنسى",
        "تذكر",
        "اعتمد",
        "مهم",
        "يجب",
        "قاعدة",
        "تعلم",
        "من الآن",
        "لاحقا",
        "لا تستخدم",
        "لا تحذف",
        "احذف",
    ]

    if not any(x in t for x in signals):
        return None

    return {
        "id": int(time.time() * 1000),
        "lesson": t,
        "source": "conversation",
        "status": "pending",
        "confidence": 0.75,
        "created_at": time.time()
    }


def add_pending_lesson(text):
    lesson = extract_lesson(text)
    if not lesson:
        return {"ok": False, "reason": "no_lesson_detected"}

    data = load(PENDING)
    data.setdefault("items", [])
    data["items"].insert(0, lesson)
    save(PENDING, data)

    return {"ok": True, "lesson": lesson}


def approve_lesson(lesson_id):
    pending = load(PENDING)
    approved = load(APPROVED)

    items = pending.get("items", [])
    lesson = next((x for x in items if str(x.get("id")) == str(lesson_id)), None)

    if not lesson:
        return {"ok": False, "reason": "lesson_not_found"}

    lesson["status"] = "approved"
    lesson["approved_at"] = time.time()

    approved.setdefault("items", [])
    approved["items"].insert(0, lesson)

    pending["items"] = [x for x in items if str(x.get("id")) != str(lesson_id)]

    save(PENDING, pending)
    save(APPROVED, approved)

    return {"ok": True, "approved": lesson}


def reject_lesson(lesson_id):
    pending = load(PENDING)
    rejected = load(REJECTED)

    items = pending.get("items", [])
    lesson = next((x for x in items if str(x.get("id")) == str(lesson_id)), None)

    if not lesson:
        return {"ok": False, "reason": "lesson_not_found"}

    lesson["status"] = "rejected"
    lesson["rejected_at"] = time.time()

    rejected.setdefault("items", [])
    rejected["items"].insert(0, lesson)

    pending["items"] = [x for x in items if str(x.get("id")) != str(lesson_id)]

    save(PENDING, pending)
    save(REJECTED, rejected)

    return {"ok": True, "rejected": lesson}


if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "test"
    arg = " ".join(sys.argv[2:])

    if cmd == "add":
        print(json.dumps(add_pending_lesson(arg), ensure_ascii=False, indent=2))
    elif cmd == "approve":
        print(json.dumps(approve_lesson(arg), ensure_ascii=False, indent=2))
    elif cmd == "reject":
        print(json.dumps(reject_lesson(arg), ensure_ascii=False, indent=2))
    else:
        print("learning_manager ready")
