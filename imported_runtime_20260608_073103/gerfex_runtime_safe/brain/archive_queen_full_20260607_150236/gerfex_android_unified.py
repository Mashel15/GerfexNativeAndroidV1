import json
import time
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
RUNTIME = ROOT / "runtime"
QUEUE_FILE = RUNTIME / "android_queue.txt"

APPS = {
    "chrome": "chrome",
    "google": "chrome",
    "browser": "chrome",
    "متصفح": "chrome",
    "كروم": "chrome",

    "settings": "settings",
    "الإعدادات": "settings",
    "اعدادات": "settings",

    "youtube": "youtube",
    "يوتيوب": "youtube",
}

ACTION_CATALOG = {
    "open_url": "Open URL through Android queue",
    "open_app": "Open known Android app",
    "search_google": "Open Google search in Chrome",
    "tap": "Tap screen coordinates",
    "swipe": "Swipe screen coordinates",
    "type_text": "Type text through Android input",
    "press_back": "Press BACK",
    "press_home": "Press HOME",
    "press_recent": "Press RECENTS",
    "press_enter": "Press ENTER",
    "wait": "Wait seconds",
    "dump_ui": "Dump UI XML",
    "screenshot": "Save screen screenshot",
}

def queue_action(action, **kwargs):
    RUNTIME.mkdir(parents=True, exist_ok=True)
    item = {
        "action": action,
        "args": kwargs,
        "time": time.time()
    }
    with QUEUE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
    return {
        "ok": True,
        "queued": item,
        "queue_file": str(QUEUE_FILE)
    }

def normalize_app(name):
    key = str(name or "").strip().lower()
    return APPS.get(key, key)

def open_url(url, browser="chrome"):
    return queue_action("open_url", url=str(url), browser=normalize_app(browser))

def search_google(query):
    q = str(query or "").strip()
    url = "https://www.google.com/search?q=" + quote(q)
    result = open_url(url, browser="chrome")
    result["reply"] = "فتحت بحث Google عن: " + q
    result["query"] = q
    result["url"] = url
    return result

def open_app(package):
    return queue_action("open_app", package=normalize_app(package))

def tap(x, y):
    return queue_action("tap", x=int(x), y=int(y))

def swipe(x1, y1, x2, y2, duration=500):
    return queue_action(
        "swipe",
        x1=int(x1),
        y1=int(y1),
        x2=int(x2),
        y2=int(y2),
        duration=int(duration)
    )

def type_text(text):
    return queue_action("type_text", text=str(text))

def press_back():
    return queue_action("key", key="BACK")

def press_home():
    return queue_action("key", key="HOME")

def press_recent():
    return queue_action("key", key="RECENTS")

def press_enter():
    return queue_action("key", key="ENTER")

def wait(seconds=1):
    return queue_action("wait", seconds=float(seconds))

def dump_ui(focus=None):
    if focus:
        return queue_action("dump_ui", focus=normalize_app(focus))
    return queue_action("dump_ui")

def screenshot():
    return queue_action("screenshot")

def status():
    queue_exists = QUEUE_FILE.exists()
    lines = []
    if queue_exists:
        try:
            lines = QUEUE_FILE.read_text(encoding="utf-8").splitlines()
        except Exception:
            lines = []
    return {
        "ok": True,
        "runtime": str(RUNTIME),
        "queue_file": str(QUEUE_FILE),
        "queue_exists": queue_exists,
        "pending_actions": len([x for x in lines if x.strip()]),
        "actions": ACTION_CATALOG,
        "apps": APPS
    }

def run(action, **kwargs):
    if action == "open_url":
        return open_url(kwargs.get("url"), kwargs.get("browser", "chrome"))
    if action == "search_google":
        return search_google(kwargs.get("query") or kwargs.get("text") or "")
    if action == "open_app":
        return open_app(kwargs.get("package") or kwargs.get("app"))
    if action == "tap":
        return tap(kwargs.get("x"), kwargs.get("y"))
    if action == "swipe":
        return swipe(kwargs.get("x1"), kwargs.get("y1"), kwargs.get("x2"), kwargs.get("y2"), kwargs.get("duration", 500))
    if action == "type_text":
        return type_text(kwargs.get("text", ""))
    if action == "press_back":
        return press_back()
    if action == "press_home":
        return press_home()
    if action == "press_recent":
        return press_recent()
    if action == "press_enter":
        return press_enter()
    if action == "wait":
        return wait(kwargs.get("seconds", 1))
    if action == "dump_ui":
        return dump_ui(kwargs.get("focus"))
    if action == "screenshot":
        return screenshot()
    if action == "status":
        return status()
    return {
        "ok": False,
        "reason": "unknown_android_action",
        "action": action,
        "available": list(ACTION_CATALOG.keys())
    }

if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    text = " ".join(sys.argv[2:])
    if action == "search_google":
        result = search_google(text)
    elif action == "open_app":
        result = open_app(text)
    elif action == "open_url":
        result = open_url(text)
    else:
        result = run(action)
    print(json.dumps(result, ensure_ascii=False, indent=2))
