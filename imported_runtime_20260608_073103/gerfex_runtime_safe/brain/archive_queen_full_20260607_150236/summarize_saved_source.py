import subprocess
from pathlib import Path


def summarize_saved_source(command: str):
    r = subprocess.run(
        ["python", "read_saved_source.py"],
        capture_output=True,
        text=True
    )

    if Path("article_summary.txt").exists():
        return {
            "ok": True,
            "reply": Path("article_summary.txt").read_text(encoding="utf-8")
        }

    return {
        "ok": False,
        "reply": r.stdout.strip() or "لم أستطع تلخيص النتيجة."
    }


if __name__ == "__main__":
    import sys
    command = " ".join(sys.argv[1:]) or "لخص 1"
    print(summarize_saved_source(command)["reply"])
