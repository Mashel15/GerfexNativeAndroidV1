import json
import time
import uuid

def make_command(
    goal,
    params=None,
    source="user"
):

    return {
        "id": str(uuid.uuid4()),
        "time": time.time(),
        "source": source,

        "goal": goal,

        "params": params or {},

        "status": "created"
    }

def make_result(
    command,
    ok,
    data=None,
    error=None
):

    return {
        "command_id": command["id"],
        "goal": command["goal"],

        "ok": ok,

        "time": time.time(),

        "data": data or {},

        "error": error
    }

def update_status(
    command,
    status
):

    command["status"] = status

    return command

if __name__ == "__main__":

    cmd = make_command(
        "youtube.search.open_first",
        {
            "query": "OpenAI"
        }
    )

    update_status(
        cmd,
        "running"
    )

    result = make_result(
        cmd,
        ok=True,
        data={
            "video": "OpenAI demo"
        }
    )

    print(json.dumps({
        "command": cmd,
        "result": result
    }, ensure_ascii=False, indent=2))
