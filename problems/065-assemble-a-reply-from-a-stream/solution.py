import json


def assemble(events):
    """Rebuild the reply from its stream events."""
    blocks = {}
    stop_reason = None
    input_tokens = output_tokens = 0
    complete = False

    for event in events:
        kind = event.get("type")
        if kind == "error":
            raise StreamError(event.get("error", {}).get("message", "stream error"))
        if kind == "message_start":
            input_tokens = event["message"]["usage"]["input_tokens"]
        elif kind == "content_block_start":
            blocks[event["index"]] = {"block": event["content_block"], "pieces": []}
        elif kind == "content_block_delta":
            delta = event["delta"]
            # Routed by index: deltas for different blocks can interleave.
            blocks[event["index"]]["pieces"].append(delta.get("text") or delta.get("partial_json") or "")
        elif kind == "message_delta":
            stop_reason = event["delta"].get("stop_reason")
            output_tokens = event["usage"]["output_tokens"]
        elif kind == "message_stop":
            complete = True
        # ping, content_block_stop and anything unrecognised carry nothing to keep.

    text = ""
    tool_calls = []
    for index in sorted(blocks):
        block = blocks[index]["block"]
        body = "".join(blocks[index]["pieces"])
        if block["type"] == "text":
            text += body
            continue
        try:
            arguments = json.loads(body) if body else {}
        except ValueError:
            # The stream died inside this call's arguments. Half a call is no call.
            continue
        tool_calls.append({"id": block["id"], "name": block["name"], "input": arguments})

    return {
        "text": text,
        "tool_calls": tool_calls,
        "stop_reason": stop_reason,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "complete": complete,
    }
