
import json

def parse_stream(chunks):
    """Return (parsed_json, chunks_consumed), or (None, len(chunks)) if incomplete."""

    text = ""
    depth = 0
    in_string = False
    escape = False
    started = False

    for i, chunk in enumerate(chunks):
        text += chunk

        for char in chunk:
            if in_string:
                if escape:
                    escape = False
                elif char == '\\':
                    escape = True
                elif char == '"':
                    in_string = False

            else:
                if char == '"':
                    in_string = True

                elif char == '{':
                    depth += 1
                    started = True

                elif char == '}':
                    depth -= 1

                    if started and depth == 0:
                        # JSON object is complete
                        try:
                            # Handle optional markdown fences
                            cleaned = text.strip()
                            if cleaned.startswith("```"):
                                cleaned = cleaned.split('\n', 1)[1]
                                cleaned = cleaned.rsplit("```", 1)[0]

                            return json.loads(cleaned), i + 1

                        except json.JSONDecodeError:
                            return None, len(chunks)

    return None, len(chunks)
