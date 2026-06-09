import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOWNLOAD_UI = Path("/sdcard/Download/gerfex_ui.xml")
LOCAL_UI = ROOT / "ui.xml"

IGNORE = {
    "ESC", "CTRL", "ALT", "TAB", "☰", "⇳",
    "HOME", "END", "PGUP", "PGDN",
    "←", "→", "↑", "↓", "↹"
}


def parse_bounds(bounds_text):
    nums = list(map(int, re.findall(r"\d+", bounds_text or "")))
    if len(nums) >= 4:
        x1, y1, x2, y2 = nums[:4]
        return [x1, y1, x2, y2], [(x1 + x2) // 2, (y1 + y2) // 2]
    return [0, 0, 0, 0], [0, 0]


def choose_ui_file():
    if DOWNLOAD_UI.exists():
        return DOWNLOAD_UI
    if LOCAL_UI.exists():
        return LOCAL_UI
    return None


def read_screen():
    ui_file = choose_ui_file()

    if not ui_file:
        return {
            "ok": False,
            "reason": "ui_xml_not_found",
            "checked": [str(DOWNLOAD_UI), str(LOCAL_UI)]
        }

    try:
        root = ET.parse(ui_file).getroot()
    except Exception as e:
        return {
            "ok": False,
            "reason": "ui_xml_parse_failed",
            "error": str(e),
            "file": str(ui_file)
        }

    items = []

    for node in root.iter():
        text = node.attrib.get("text", "").strip()

        if not text or text in IGNORE:
            continue

        bounds, center = parse_bounds(node.attrib.get("bounds", ""))

        items.append({
            "text": text,
            "id": node.attrib.get("resource-id", ""),
            "class": node.attrib.get("class", ""),
            "clickable": node.attrib.get("clickable", "false"),
            "enabled": node.attrib.get("enabled", "false"),
            "bounds": bounds,
            "center": center
        })

    return {
        "ok": True,
        "source_file": str(ui_file),
        "node_count": len(items),
        "items": items
    }


if __name__ == "__main__":
    print(json.dumps(read_screen(), ensure_ascii=False, indent=2))
