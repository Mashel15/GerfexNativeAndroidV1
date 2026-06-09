import json, time
from pathlib import Path

BASE = Path(__file__).resolve().parent
MEMORY_FILE = BASE / "memory.json"
ACTIONS_FILE = BASE / "actions.json"

def load_json(path, default):
    path = Path(path)
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def save_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_memory():
    return load_json(MEMORY_FILE, {"project_notes": []})

def save_memory(memory):
    save_json(MEMORY_FILE, memory)
    return {"ok": True, "file": str(MEMORY_FILE)}

def append_memory_note(note):
    memory = load_memory()
    memory.setdefault("project_notes", [])
    memory["project_notes"].append({"note": note, "time": time.time()})
    save_memory(memory)
    return {"ok": True, "note": note}

def log_action(action):
    actions = load_json(ACTIONS_FILE, {"action_history": []})
    actions.setdefault("action_history", [])
    actions["action_history"].append(action)
    save_json(ACTIONS_FILE, actions)
    return {"ok": True, "action": action}
