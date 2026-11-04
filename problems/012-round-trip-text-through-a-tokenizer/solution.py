def count_tokens(text):
    """Number of tokens, excluding any special tokens."""
    tok_cnt = len(tokenizer.encode(text, add_special_tokens = False))
    return tok_cnt


def roundtrip(text):
    """Encode then decode, returning the original text."""
    tok_enc = tokenizer.encode(text, add_special_tokens = False)
    return tokenizer.decode(tok_enc, add_special_tokens = False)
    


def token_strings(text):
    """The individual tokens, in order, as strings."""
    return tokenizer.tokenize(text, add_special_tokens = False)
    
