"""Small helper utilities for sanitization and content filtering."""

import re


def sanitize_text(text: str) -> str:
    """Basic sanitization: strip and collapse whitespace."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def simple_moderation_filter(text: str) -> str:
    """A naive output filter that redacts a small blacklist of words.

    This is intentionally simple: production systems should use a proper
    content moderation API or larger blocklist rules.
    """
    blacklist = ["password", "ssn", "secret"]
    out = text
    for b in blacklist:
        out = re.sub(re.escape(b), "[REDACTED]", out, flags=re.IGNORECASE)
    return out
