"""
adapter.py — Multi-channel content adaptation.
Rewrites tagline, blog, and social posts for a target channel.
Image and video assets are left unchanged.
"""

from typing import Optional, Callable
from config import (
    CHANNEL_DESCRIPTORS,
    ADAPT_TAGLINE_PROMPT, ADAPT_BLOG_PROMPT, ADAPT_SOCIAL_PROMPT,
)
from utils import parse_social_json, friendly_error
from text_gen import _call


def adapt_for_channel(
    product: str,
    audience: str,
    channel: str,
    tagline: str,
    blog: str,
    social: dict,
    status_callback: Optional[Callable[[str], None]] = None,
) -> dict:
    """
    Rewrite text assets for the given channel.

    Args:
        product, audience: brief context
        channel: one of CHANNEL_DESCRIPTORS keys
        tagline, blog, social: original text assets
        status_callback: optional progress updates

    Returns:
        dict with keys: tagline, blog, social (dict), channel, error (str|None)
    """
    cfg = CHANNEL_DESCRIPTORS.get(channel, {})
    if not cfg:
        return {
            "tagline": tagline, "blog": blog, "social": social,
            "channel": channel, "error": f"Unknown channel: {channel}",
        }

    ctx = {
        "platform":      cfg["platform"],
        "audience_note": cfg["audience_note"],
        "channel_desc":  cfg["desc"],
        "product":       product,
        "tagline":       tagline,
        "blog":          blog[:400],
        "social":        str(social)[:300],
    }

    result = {"channel": channel, "error": None}

    # ── Tagline ────────────────────────────────────────────────────────────────
    if status_callback:
        status_callback(f"Adapting tagline for {channel}…")
    try:
        result["tagline"] = _call(ADAPT_TAGLINE_PROMPT.format(**ctx))
    except Exception as e:
        result["tagline"] = tagline
        result["error"] = friendly_error(e, "Adapt tagline")

    # ── Blog ───────────────────────────────────────────────────────────────────
    if status_callback:
        status_callback(f"Adapting blog for {channel}…")
    try:
        result["blog"] = _call(ADAPT_BLOG_PROMPT.format(**ctx))
    except Exception as e:
        result["blog"] = blog
        if not result["error"]:
            result["error"] = friendly_error(e, "Adapt blog")

    # ── Social posts ───────────────────────────────────────────────────────────
    if status_callback:
        status_callback(f"Adapting social posts for {channel}…")
    try:
        raw = _call(ADAPT_SOCIAL_PROMPT.format(**ctx))
        result["social"] = parse_social_json(raw)
    except Exception as e:
        result["social"] = social
        if not result["error"]:
            result["error"] = friendly_error(e, "Adapt social")

    return result
