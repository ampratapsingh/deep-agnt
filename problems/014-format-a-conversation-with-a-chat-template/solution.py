def format_chat(messages):
    """The prompt string, ready for the assistant to continue."""
    if tokenizer.chat_template:
        #if chat template available then apply
        return tokenizer.apply_chat_template(
            messages,
            add_generation_prompt = True,
            tokenize = False
        )
    #else default template
    return "\n".join(
        f"{msg['role']} : {msg['content']}"
        for msg in messages
    )
    


def format_for_training(messages):
    """The full conversation including the assistant's reply."""
    if tokenizer.chat_template:
        return tokenizer.apply_chat_template(
            messages,
            tokenize = False,
            add_generation_prompt = False
        )
    return "\n".join(
        f"{msg['role']} : {msg['content']}"
        for msg in messages
    )
    
