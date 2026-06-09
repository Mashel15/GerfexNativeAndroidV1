import os
import subprocess
import time
from pathlib import Path
import urllib.parse

RISH = str(Path.home() / "rish/rish")
UI_XML = Path.home() / "storage/downloads/gerfex_ui.xml"

def rish(cmd):
    print("RISH:", cmd)

    r = subprocess.run(
        [RISH, "-c", cmd],
        text=True,
        capture_output=True,
        env={
            **os.environ,
            "RISH_APPLICATION_ID": "com.termux"
        }
    )

    if r.stdout:
        print(r.stdout)

    if r.stderr:
        print(r.stderr)

    return {
        "ok": r.returncode == 0,
        "stdout": r.stdout,
        "stderr": r.stderr,
        "cmd": cmd
    }

def tap(x, y):
    return rish(f"input tap {x} {y}")

def swipe(x1, y1, x2, y2, duration=400):
    return rish(
        f"input swipe {x1} {y1} {x2} {y2} {duration}"
    )

def type_text(text):
    safe = text.replace(" ", "%s")
    return rish(f'input text "{safe}"')

def press_enter():
    return rish("input keyevent 66")

def press_back():
    return rish("input keyevent 4")

def press_home():
    return rish("input keyevent 3")

def wait(seconds=1):
    time.sleep(seconds)
    return {
        "ok": True,
        "waited": seconds
    }

def dump_ui():
    rish("uiautomator dump /sdcard/Download/gerfex_ui.xml")

    if not UI_XML.exists():
        return {
            "ok": False,
            "xml": "",
            "reason": "ui_xml_missing"
        }

    xml = UI_XML.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    return {
        "ok": True,
        "xml": xml,
        "path": str(UI_XML)
    }

def open_url(url):
    return rish(
        f'am start -a android.intent.action.VIEW -d "{url}"'
    )

def open_youtube_results(query):
    q = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={q}"
    return open_url(url)

def open_chrome():
    return rish(
        "am start -n com.android.chrome/com.google.android.apps.chrome.Main"
    )

def open_settings():
    return rish(
        "am start -a android.settings.SETTINGS"
    )

def wait_for_package(package, attempts=12, delay=0.7):
    last_xml = ""

    for i in range(attempts):
        result = dump_ui()
        xml = result.get("xml", "")
        last_xml = xml

        if package in xml:
            return {
                "ok": True,
                "package": package,
                "attempt": i + 1,
                "xml": xml
            }

        time.sleep(delay)

    return {
        "ok": False,
        "package": package,
        "reason": "package_not_confirmed",
        "xml": last_xml
    }

def tap_item(item):
    return tap(
        item["x"],
        item["y"]
    )

if __name__ == "__main__":
    print("Action Executor V1 Ready")
