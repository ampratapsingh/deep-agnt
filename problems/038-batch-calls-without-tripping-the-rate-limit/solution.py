import time
from agentkit import APIError, RateLimitError, OverloadedError


def ask_with_backoff(llm, prompt, max_retries=5, base_delay=1.0, max_delay=30.0, jitter=None, sleep=time.sleep):
    """Retry busy signals with capped, jittered exponential backoff. Re-raise anything else."""
    delay = base_delay
    for attempt in range(max_retries + 1):
        try:
            return llm.ask(prompt)
        except (RateLimitError, OverloadedError):
            # The provider is busy. Retrying into the same congestion at the
            # same rate produces the same error; back off.
            if attempt == max_retries:
                raise
            wait = min(delay, max_delay)
            if jitter is not None:
                # Somewhere between half the delay and all of it, so clients
                # turned away together do not come back together.
                wait = wait * (0.5 + 0.5 * jitter())
            sleep(wait)
            delay *= 2
        # Any other error means the REQUEST is wrong. It propagates untouched:
        # retrying a malformed request just delays finding out.


def ask_all(llm, prompts, **kwargs):
    """Run every prompt with backoff, preserving order. A bad request is None; a provider that stays busy stops the batch."""
    replies = []
    for prompt in prompts:
        try:
            replies.append(ask_with_backoff(llm, prompt, **kwargs))
        except (RateLimitError, OverloadedError):
            # Out of retries: the provider is down, and the rest would hit the same wall.
            raise
        except APIError:
            # This request is wrong. The others are not.
            replies.append(None)
    return replies
