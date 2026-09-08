"""Currency conversion & Indian-style (lakh/crore) number formatting."""

USD_TO_INR = 94.5  # approximate mid-market rate

def to_inr(usd_amount: float) -> float:
    """Converts a raw USD figure to INR using the fixed session exchange rate."""
    return usd_amount * USD_TO_INR

def format_inr(amount: float, decimals: int = 0) -> str:
    """Formats a number with the Rupee symbol using Indian digit grouping
    (2-2-3, i.e. lakh/crore places) instead of the Western 3-3-3 grouping,
    e.g. 1234567 -> '₹12,34,567' rather than '₹1,234,567'."""
    is_negative = amount < 0
    amount = abs(round(amount, decimals))

    if decimals > 0:
        whole = int(amount)
        frac = f"{amount:.{decimals}f}".split(".")[1]
    else:
        whole = int(amount)
        frac = None

    s = str(whole)
    if len(s) <= 3:
        grouped = s
    else:
        last3 = s[-3:]
        rest = s[:-3]
        parts = []
        while len(rest) > 2:
            parts.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.insert(0, rest)
        grouped = ",".join(parts) + "," + last3

    result = f"₹{grouped}"
    if frac:
        result += f".{frac}"
    return f"-{result}" if is_negative else result

def format_inr_short(amount: float) -> str:
    """Formats a large INR figure in crore/lakh shorthand for headline coverage
    amounts, e.g. 94500000 -> '₹9.45 Cr', 4725000 -> '₹47.25 L'."""
    crore = amount / 1e7
    lakh = amount / 1e5
    if crore >= 1:
        return f"₹{crore:.2f} Cr".replace(".00", "")
    return f"₹{lakh:.2f} L".replace(".00", "")
