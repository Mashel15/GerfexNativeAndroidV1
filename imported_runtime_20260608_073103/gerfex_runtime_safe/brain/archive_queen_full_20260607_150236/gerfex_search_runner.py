import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run_search(command: str):
    r = subprocess.run(
        ["python", str(ROOT / "gerfex_goal_loop_core.py"), command],
        capture_output=True,
        text=True,
        cwd=str(ROOT)
    )

    output = r.stdout.strip()

    marker = "GERFEX ANSWER"
    if marker in output:
        answer = output.split(marker, 1)[1].strip()
        answer = answer.replace("GERFEX PHASE 5 DONE", "").strip()
    else:
        answer = output[-1200:] if output else "لم أستطع بناء نتيجة بحث."

    return {
        "ok": r.returncode == 0,
        "answer": answer,
        "raw": output,
        "error": r.stderr.strip()
    }


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "ابحث عن أخبار الذكاء الاصطناعي"
    print(run_search(q)["answer"])
