import json, time
from pathlib import Path

BASE = Path(__file__).resolve().parent
RECOVERY_LOG = BASE / "recovery_log.json"

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

def log_recovery(step, reason):
    data = load_json(RECOVERY_LOG, [])
    item = {"step": step, "reason": reason, "time": time.time()}
    data.append(item)
    save_json(RECOVERY_LOG, data)
    return item

def should_retry(step):
    return step in ["read_fresh_ui", "arm_verify_full", "dump_ui", "screen_read"]

def wait_and_retry(step, reason, seconds=5):
    log_recovery(step, reason)
    time.sleep(seconds)
    return True
