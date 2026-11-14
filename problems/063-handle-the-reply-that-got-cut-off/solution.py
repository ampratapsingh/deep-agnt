def complete(llm, messages, max_tokens=200, max_continues=3):
    """Get the whole reply, continuing when it is cut off. Return text and status."""

    # Copy messages so we don't modify the caller's original list
    conversation = messages.copy()

    full_text = ""

    for attempt in range(max_continues + 1):

        response = llm.messages.create(
            messages=conversation,
            max_tokens=max_tokens
        )

        # Extract the generated text and stop reason
        reply = response.content[0].text
        stop_reason = response.stop_reason

        full_text += reply

        if stop_reason == "end_turn":
            return {"text": full_text, "status": "complete"}

        elif stop_reason == "max_tokens":

            # If no more continuation attempts are allowed
            if attempt == max_continues:
                return {"text": full_text, "status": "truncated"}

            # Add the partial assistant response to conversation
            conversation.append({
                "role": "assistant",
                "content": reply
            })

            # Ask the model to continue
            conversation.append({
                "role": "user",
                "content": "Continue from where you stopped. Do not repeat the previous text."
            })

        elif stop_reason == "tool_use":
            return {"text": full_text, "status": "tool_use"}

        elif stop_reason == "refusal":
            return {"text": full_text, "status": "refused"}

        else:
            raise ValueError(f"Unknown stop reason: {stop_reason}")
