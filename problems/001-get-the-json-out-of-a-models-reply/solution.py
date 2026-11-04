import json


def parse_model_json(reply):
    start = reply.find("{")
    end = reply.rfind("}")

    if start == -1 or end == -1 or start >= end:
        return None

    raw_json = reply[start : end + 1]

    try:
        data = json.loads(raw_json)
        if isinstance(data, dict):
            return data
        return None
    except json.JSONDecodeError:
        return None
