"""
utils.py — Shared helpers for Content Engine Pro.
"""

import json
import re
from pathlib import Path
from datetime import datetime


def build_context(product: str, audience: str, tone: str, tagline: str = "") -> dict:
    from config import TONE_DESCRIPTORS
    return {
        "product":   product,
        "audience":  audience,
        "tone":      tone,
        "tone_desc": TONE_DESCRIPTORS.get(tone, tone),
        "tagline":   tagline,
    }


def parse_json_response(raw: str) -> dict:
    """Robustly extract the first JSON object from an LLM response."""
    cleaned = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {}


def parse_social_json(raw: str) -> dict:
    data = parse_json_response(raw)
    return {
        "twitter":   data.get("twitter", ""),
        "instagram": data.get("instagram", ""),
        "linkedin":  data.get("linkedin", ""),
    }


def save_bytes(data: bytes, stem: str, ext: str) -> Path:
    assets_dir = Path(__file__).parent / "assets"
    assets_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = assets_dir / f"{stem}_{timestamp}.{ext}"
    path.write_bytes(data)
    return path


def friendly_error(exc: Exception, context: str = "") -> str:
    msg = str(exc)
    prefix = f"[{context}] " if context else ""
    if "401" in msg or "authentication" in msg.lower() or "api key" in msg.lower():
        return f"{prefix}API key missing or invalid."
    if "429" in msg or "rate limit" in msg.lower():
        return f"{prefix}Rate limit — wait a moment and retry."
    if "402" in msg or "credits" in msg.lower():
        return f"{prefix}Insufficient credits — top up at openrouter.ai/settings/credits."
    if "timeout" in msg.lower():
        return f"{prefix}Request timed out."
    return f"{prefix}Unexpected error: {msg}"
