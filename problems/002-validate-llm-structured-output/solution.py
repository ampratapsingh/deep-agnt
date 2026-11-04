import json

def validate_response(raw, schema):
    """Parse and validate a model's JSON reply against a {field: type} schema.

    Return the cleaned dict, or None if it cannot be trusted.
    """
    start = raw.find("{")
    end = raw.rfind("}")

    if start >= end or start == -1 or end == -1:
        return None

    #Step 1: Invalid JSON returns None
    try:
        data = json.loads(raw[start: end + 1])
    except (json.JSONDecodeError, TypeError):
        return None

    #Step 2: Anything that isn't an object (a list, a number, a string) returns None
    if not isinstance(data, dict):
        return None

    #Step 3: Every schema field must be present with the right type, or return None
    cleaned = {}
    for key, exp_val in schema.items():
        #Step 4: Drop any field the schema doesn't mention
        if key not in data:
            return None

        val = data[key]

        #Step 5: bool is not an int
        if exp_val is int and isinstance(val, bool):
            return None

        if not isinstance(val, exp_val):
            return None

        cleaned[key] = val

    return cleaned
    

    
