import json
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    from runtime.runtime_state import record
except Exception:
    def record(*args, **kwargs):
        return None

ROOT = Path(__file__).resolve().parent.parent
RUNTIME_QUEUE = ROOT / "runtime" / "android_queue.txt"
POLICY_FILE = ROOT / "runtime" / "browser_policy.json"


def load_browser_policy():
    try:
        return json.loads(POLICY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {
            "primary_browser": "chrome",
            "fallback_browser": "samsung"
        }


def queue_action(action, args=None):
    args = args or {}

    if action == "open_url":
        policy = load_browser_policy()
        args.setdefault("browser", policy.get("primary_browser", "chrome"))

    item = {
        "time": time.time(),
        "action": action,
        "args": args,
        "source": "agent_bridge_normalized"
    }

    RUNTIME_QUEUE.parent.mkdir(parents=True, exist_ok=True)

    with RUNTIME_QUEUE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

    record("queued_action", last_queued_action=item, status="queued")

    return {
        "ok": True,
        "queue_file": str(RUNTIME_QUEUE),
        "queued": item
    }


def open_app(package):
    return queue_action("open_app", {"package": package})


def open_url(url):
    return queue_action("open_url", {"url": str(url)})


def tap(x, y):
    return queue_action("tap", {"x": x, "y": y})


def swipe(x1, y1, x2, y2, duration=300):
    return queue_action("swipe", {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "duration": duration
    })


def type_text(text):
    return queue_action("type_text", {"text": str(text)})


def press_back():
    return queue_action("key", {"key": "BACK"})


def press_home():
    return queue_action("key", {"key": "HOME"})


def press_recent():
    return queue_action("key", {"key": "RECENTS"})


def wait(seconds):
    return queue_action("wait", {"seconds": float(seconds)})


def dump_ui():
    return queue_action("dump_ui", {})
