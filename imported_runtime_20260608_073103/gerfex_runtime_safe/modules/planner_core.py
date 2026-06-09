# Gerfex Planner Core
# Merged from planner_v2.py

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

from command_protocol_v1 import (
    make_command
)

def normalize(text):

    return (
        text.lower()
        .replace("أ", "ا")
        .replace("إ", "ا")
        .replace("آ", "ا")
        .strip()
    )

def extract_query(command, marker):

    if marker not in command:
        return ""

    q = command.split(marker, 1)[1]

    cleanup = [
        "وافتح اول نتيجه",
        "وافتح أول نتيجه",
        "وافتح اول نتيجة",
        "وافتح أول نتيجة",
        "افتح اول نتيجه",
        "افتح أول نتيجه",
        "افتح اول نتيجة",
        "افتح أول نتيجة"
    ]

    for c in cleanup:
        q = q.replace(c, "")

    return q.strip(" ؟?،,.").strip()

def plan(command_text):

    c = normalize(command_text)

    # YouTube search + open first

    if (
        "يوتيوب" in c
        and "افتح" in c
        and (
            "اول" in c
            or "أول" in command_text
        )
    ):

        query = extract_query(
            command_text,
            "عن"
        )

        return make_command(

            "youtube.search.open_first",

            {
                "query": query
            }
        )

    # YouTube search only

    if "يوتيوب" in c:

        query = extract_query(
            command_text,
            "عن"
        )

        return make_command(

            "youtube.search",

            {
                "query": query
            }
        )

    return make_command(

        "unknown",

        {
            "original": command_text
        }
    )

if __name__ == "__main__":

    examples = [

        "ابحث في يوتيوب عن OpenAI وافتح أول نتيجة",

        "ابحث في يوتيوب عن مباريات برشلونة",

        "افتح الإعدادات"

    ]

    results = []

    for e in examples:

        results.append({

            "input": e,

            "planned": plan(e)

        })

    print(json.dumps(
        results,
        ensure_ascii=False,
        indent=2
    ))
