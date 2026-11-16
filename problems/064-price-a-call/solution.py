
import math

def call_cost(usage, price):
    """The cost of one call, in micro-dollars, rounded up."""

    total = 0

    for kind in ["input", "output", "cache_read", "cache_write"]:
        tokens = usage.get(f"{kind}_tokens", 0)
        rate = price.get(kind, 0)

        total += tokens * rate

    return math.ceil(total / 1_000_000)


def cost_report(calls, prices):
    """Totals by model and overall, and the models that could not be priced."""

    totals = {}
    unknown = set()

    for call in calls:
        model = call["model"]
        usage = call["usage"]

        if model not in prices:
            unknown.add(model)
            continue

        if model not in totals:
            totals[model] = 0

        # Accumulate RAW cost, without rounding individual calls
        for kind in ["input", "output", "cache_read", "cache_write"]:
            tokens = usage.get(f"{kind}_tokens", 0)
            rate = prices[model].get(kind, 0)

            totals[model] += tokens * rate

    # Round each model's total once
    by_model = {
        model: math.ceil(raw_cost / 1_000_000)
        for model, raw_cost in totals.items()
    }

    # Round overall raw cost once
    total = math.ceil(sum(totals.values()) / 1_000_000)

    return {
        "by_model": by_model,
        "total": total,
        "unknown": sorted(unknown)
    }
