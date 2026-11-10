from agentkit.tokenizer import count_tokens


def trim_history(messages, max_tokens):
    """Drop old turns until the conversation fits. Never the system prompt."""
    if not messages:
        return []

    # Rule 5: Return messages unchanged when they already fit
    if count_tokens(messages) <= max_tokens:
        return messages

    # Identify whether a system prompt exists at the start
    has_system = messages[0].get("role") == "system"
    system_msg = [messages[0]] if has_system else []
    
    # If there is only one message or just system prompt + nothing else
    if len(messages) <= len(system_msg):
        return messages

    # Rule 2: Most recent user message is at the end
    last_user = messages[-1]

    # History turns between system prompt and the latest user turn
    history = messages[len(system_msg) : -1]

    # Rule 3: Drop oldest turns in pairs (user + assistant) until it fits
    while history:
        candidate = system_msg + history + [last_user]
        if count_tokens(candidate) <= max_tokens:
            return candidate
        history = history[2:]

    # Check if system prompt + last user message fits
    candidate = system_msg + [last_user]
    if count_tokens(candidate) <= max_tokens:
        return candidate

    # Rule 4: System prompt + last user message exceeds budget;
    # truncate the last user message from the front, keeping its tail.
    user_copy = dict(last_user)
    content = user_copy.get("content", "")

    low = 0
    high = len(content)
    best_start = len(content)

    # Binary search to find the minimum cut from the front (keeping the longest tail)
    while low <= high:
        mid = (low + high) // 2
        user_copy["content"] = content[mid:]
        if count_tokens(system_msg + [user_copy]) <= max_tokens:
            best_start = mid
            high = mid - 1
        else:
            low = mid + 1

    user_copy["content"] = content[best_start:]
    return system_msg + [user_copy]
