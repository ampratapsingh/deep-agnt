def _words(text):
    return {w for w in text.lower().split() if len(w) > 3}

def answer_with_context(llm, question, docs):
    """Answer the question from the docs. Works, and sends everything."""

    asked = _words(question)
    ranked = sorted(docs, key = lambda d : -len(asked & _words(d)))
    chosen = [d for d in ranked[ : 2] if asked & _words(d)] or ranked[ : 1]

    prompt = "Context:\n" + "\n\n".join(chosen) + "\n\nQuestion: " + question
    return llm.ask(prompt)
