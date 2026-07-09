"""
video_gen.py — Promotional video via OpenRouter Wan 2.6.

API flow:
  POST /api/v1/videos          → submit job, get job_id + polling_url
  GET  <polling_url>           → poll for completed/failed/cancelled/expired
  GET  /api/v1/videos/{id}/content?index=0  → download MP4 (auth required)
"""

import time
import httpx
from pathlib import Path
from typing import Callable, Optional, Tuple

from config import OPENROUTER_PAID_KEY, VIDEO_MODEL, VIDEO_PROMPT_TEMPLATE
from utils import build_context, save_bytes, friendly_error

BASE_URL   = "https://openrouter.ai/api/v1"
SUBMIT_URL = f"{BASE_URL}/videos"


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {OPENROUTER_PAID_KEY}",
        "Content-Type":  "application/json",
        "HTTP-Referer":  "http://localhost:8501",
        "X-Title":       "Content Engine Pro",
    }


def _submit(prompt: str) -> Tuple[str, str]:
    payload = {
        "model":        VIDEO_MODEL,
        "prompt":       prompt,
        "duration":     5,
        "aspect_ratio": "16:9",
        "resolution":   "720p",
    }
    resp = httpx.post(SUBMIT_URL, headers=_headers(), json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    job_id = data.get("id")
    if not job_id:
        raise RuntimeError(f"No job ID in response: {data}")
    polling_url = data.get("polling_url") or f"{BASE_URL}/videos/{job_id}"
    return job_id, polling_url


def _poll(job_id: str, polling_url: str,
          max_wait: int = 420, interval: int = 20,
          cb: Optional[Callable[[str], None]] = None) -> str:
    waited = 0
    while waited < max_wait:
        resp = httpx.get(polling_url, headers=_headers(), timeout=15)
        resp.raise_for_status()
        data   = resp.json()
        status = data.get("status", "unknown")

        if cb:
            cb(f"Video status: {status} ({waited}s elapsed…)")

        if status == "completed":
            unsigned = data.get("unsigned_urls") or []
            if unsigned and not unsigned[0].startswith("https://openrouter.ai/api/"):
                return unsigned[0]
            return f"{BASE_URL}/videos/{job_id}/content?index=0"

        if status in ("failed", "cancelled", "expired"):
            detail = data.get("error") or data.get("message") or "no detail"
            raise RuntimeError(f"Video job {status}: {detail}")

        time.sleep(interval)
        waited += interval

    raise RuntimeError(f"Video generation timed out after {max_wait}s.")


def _download(url: str) -> bytes:
    headers = {}
    if url.startswith("https://openrouter.ai/api/"):
        headers["Authorization"] = f"Bearer {OPENROUTER_PAID_KEY}"
    resp = httpx.get(url, headers=headers, timeout=180, follow_redirects=True)
    resp.raise_for_status()
    if "application/json" in resp.headers.get("content-type", ""):
        raise RuntimeError(f"Expected video bytes but got JSON: {resp.text[:200]}")
    return resp.content


def generate_promo_video(
    product: str, audience: str, tone: str, tagline: str,
    status_callback: Optional[Callable[[str], None]] = None,
) -> Path:
    try:
        if not OPENROUTER_PAID_KEY:
            raise RuntimeError("OPENROUTER_PAID_KEY missing in .env")
        ctx    = build_context(product, audience, tone, tagline)
        prompt = VIDEO_PROMPT_TEMPLATE.format(**ctx)

        if status_callback:
            status_callback(f"Submitting job to {VIDEO_MODEL}…")
        job_id, polling_url = _submit(prompt)

        if status_callback:
            status_callback(f"Job submitted ({job_id[:12]}…). Wan 2.6 takes 1–3 min…")
        video_url = _poll(job_id, polling_url, cb=status_callback)

        if status_callback:
            status_callback("Downloading video…")
        return save_bytes(_download(video_url), stem="promo", ext="mp4")

    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(friendly_error(e, "Video")) from e
