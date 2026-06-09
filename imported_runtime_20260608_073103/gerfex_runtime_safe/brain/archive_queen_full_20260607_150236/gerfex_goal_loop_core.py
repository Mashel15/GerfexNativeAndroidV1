import sys, json, time, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MEMORY = ROOT / "memory.json"
SEARCH_CORE = ROOT / "gerfex_search_core.json"

def load_json(path, default=None):
    if default is None:
        default = {}
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default

def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def run(script, *args):
    p = ROOT / script
    if not p.exists():
        return {"ok": False, "script": script, "error": "missing"}
    r = subprocess.run(["python", str(p), *args], capture_output=True, text=True)
    return {
        "ok": r.returncode == 0,
        "script": script,
        "stdout": r.stdout.strip(),
        "stderr": r.stderr.strip(),
        "returncode": r.returncode
    }

def detect_intent(command):
    c = command.lower()

    if ("افتح" in c or "open" in c) and ("ابحث" in c or "search" in c):
        return "task"

    if "ابحث في جوجل" in c or "قوقل" in c or "google" in c:
        return "browser_search"

    if "افتح" in c or "open" in c:
        return "open"

    if "اقرأ" in c or "لخص" in c or "read" in c:
        return "read"

    if any(x in c for x in ["آخر", "أخبار", "اخبار", "ابحث", "ما هو", "ماهي", "من هو", "متى", "news", "search"]):
        return "answer_search"

    return "observe"

def make_plan(intent, command):
    # Cleaned V1: keep only working news/search pipeline.
    # Removed old broken paths that referenced missing scripts:
    # task_planner, arm_selector, arm_executor, arm_verify_full,
    # search_engine, dump_current_ui, extract_search_results, recovery_reader.

    if intent in ["answer_search", "task", "browser_search", "read", "open"]:
        return [
            {"name":"load_search_core","script":None},
            {"name":"decide_sources","script":None},
            {"name":"source_selector","script":"source_selector_v1.py"},
            {"name":"collector","script":"collector_v1.py"},
            {"name":"rank_if_results_exist","script":"search_ranker_v2.py"},
            {"name":"synthesizer","script":"synthesizer_v1.py"}
        ]

    return [
        {"name":"load_search_core","script":None},
        {"name":"decide_sources","script":None},
        {"name":"source_selector","script":"source_selector_v1.py"},
        {"name":"collector","script":"collector_v1.py"},
        {"name":"rank_if_results_exist","script":"search_ranker_v2.py"},
        {"name":"synthesizer","script":"synthesizer_v1.py"}
    ]

def execute_plan(plan):
    results = []

    for step in plan:
        print(f"\n=== {step['name']} ===")

        if step["script"] is None:
            if step["name"] == "load_search_core":
                core = load_json(SEARCH_CORE, {})
                print(core.get("core_principle", "Search core loaded."))
                results.append({"ok": True, "step": step["name"]})

            elif step["name"] == "decide_sources":
                print("Decision: answer/search does not open browser automatically.")
                print("Next required layer: collector tools for official sources, web APIs, X/Twitter, Instagram, Wikipedia, YouTube.")
                results.append({"ok": True, "step": step["name"]})

            elif step["name"] == "open_reserved":
                print("Open mode reserved: later will open saved source by number.")
                results.append({"ok": True, "step": step["name"]})

            continue

        args = step.get("args", [])
        r = run(step["script"], *args)
        print(r.get("stdout", ""))
        if r.get("stderr"):
            print("STDERR:", r["stderr"])
        results.append(r)

    return results

def remember(command, intent, plan, results):
    data = load_json(MEMORY, {})
    data.setdefault("goal_loop_events", [])
    data["goal_loop_events"].append({
        "time": time.time(),
        "command": command,
        "intent": intent,
        "plan": plan,
        "results_count": len(results)
    })
    save_json(MEMORY, data)

def main():
    command = " ".join(sys.argv[1:]).strip()
    print("GERFEX PHASE 5 — GOAL LOOP CORE")
    print("COMMAND:", command or "(none)")

    intent = detect_intent(command)
    print("INTENT:", intent)

    Path("last_query.txt").write_text(command, encoding="utf-8")

    plan = make_plan(intent, command)
    print("\nPLAN:")
    print(json.dumps(plan, ensure_ascii=False, indent=2))

    results = execute_plan(plan)
    remember(command, intent, plan, results)

    print("\nGERFEX PHASE 5 DONE")

if __name__ == "__main__":
    main()
