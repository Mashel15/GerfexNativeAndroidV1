import json

from skills.youtube_skill import (
    youtube_search_open_first
)

SKILLS = {

    "youtube.search.open_first": {
        "handler": youtube_search_open_first,
        "description": "Search YouTube and open first ranked video"
    }

}

def list_skills():

    return {

        name: {
            "description": info["description"]
        }

        for name, info in SKILLS.items()
    }

def has_skill(goal):

    return goal in SKILLS

def execute_goal(
    goal,
    params=None
):

    params = params or {}

    if goal not in SKILLS:

        return {
            "ok": False,
            "reason": "unknown_goal",
            "goal": goal
        }

    handler = SKILLS[goal]["handler"]

    if goal == "youtube.search.open_first":

        return handler(
            params.get("query", "")
        )

    return {
        "ok": False,
        "reason": "handler_not_implemented"
    }

if __name__ == "__main__":

    print(json.dumps({
        "skills": list_skills()
    }, ensure_ascii=False, indent=2))
