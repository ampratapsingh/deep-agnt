def ask_for_json(llm, prompt, schema, max_attempts=3):
    """Ask until the reply validates. Return the object, or None after max_attempts."""
    messages = [
        {
            "role" : "user",
            "content" : prompt
        }
    ]

    for _ in range(max_attempts):
        response = llm.messages.create(messages = messages)
        reply = response.text
        obj, err = validate(reply, schema)

        if err is None:
            return obj

        messages.append(
            {
                "role" : "assistant",
                "content" : reply
            }
        )

        messages.append(
            {
                "role" : "user",
                "content" : f"The JSON is invalid: {err}. Please return corrected JSON."
            }
        )

    return None
        
