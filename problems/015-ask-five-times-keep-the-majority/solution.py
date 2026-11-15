from collections import Counter


def consistent_answer(llm, question, samples=5):
    """Ask `samples` times and return the most common normalised answer."""
    replies = []
    for _ in range(samples):
        reply = llm.ask(question)
        replies.append(reply.strip().lower().rstrip("."))
    return Counter(replies).most_common(1)[0][0]
