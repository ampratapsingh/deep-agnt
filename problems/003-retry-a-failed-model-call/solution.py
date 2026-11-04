def call_with_retry(fn, max_attempts=3, base_delay=1.0):
    """Call fn(), retrying transient failures with exponential backoff.
    Re-raise the last exception once max_attempts is exhausted.
    """

    retryable_errs = (RateLimitError, TimeoutError, ServerError)
    for attempt in range(max_attempts):
        try:
            return fn()
        except retryable_errs:
            if attempt == max_attempts - 1:
                raise
            delay = base_delay * (2 ** attempt)
            sleep(delay)
            
    

