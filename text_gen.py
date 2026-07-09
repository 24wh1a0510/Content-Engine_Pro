"""
text_gen.py — Text generation with model fallback chain.
"""

from openai import OpenAI
from config import (
    OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MAX_TOKENS,
    PRIMARY_TEXT_MODEL, FALLBACK_TEXT_MODELS,
    TAGLINE_PROMPT, BLOG_INTRO_PROMPT, SOCIAL_POSTS_PROMPT,
)
from utils import build_context, parse_social_json, friendly_error


def _client() -> OpenAI:
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is missing in your .env file.")
    return OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        default_headers={
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Content Engine Pro",
        },
    )


def _call(prompt: str) -> str:
    """Call LLM with automatic fallback across models."""
    client = _client()
    models = [PRIMARY_TEXT_MODEL] + FALLBACK_TEXT_MODELS
    last_error = None

    for model in models:
        try:
            resp = client.chat.completions.create(
                model=model,
                max_tokens=MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )
            content = resp.choices[0].message.content
            if content and content.strip():
                return content.strip()
        except Exception as e:
            last_error = e
            err = str(e)
            if any(code in err for code in ("402", "404", "429")):
                continue
            raise

    raise RuntimeError(
        f"All models exhausted. Last error: {last_error}"
    )


def generate_tagline(product: str, audience: str, tone: str) -> str:
    try:
        return _call(TAGLINE_PROMPT.format(**build_context(product, audience, tone)))
    except Exception as e:
        raise RuntimeError(friendly_error(e, "Tagline")) from e


def generate_blog_intro(product: str, audience: str, tone: str, tagline: str) -> str:
    try:
        return _call(BLOG_INTRO_PROMPT.format(**build_context(product, audience, tone, tagline)))
    except Exception as e:
        raise RuntimeError(friendly_error(e, "Blog")) from e


def generate_social_posts(product: str, audience: str, tone: str, tagline: str) -> dict:
    try:
        raw = _call(SOCIAL_POSTS_PROMPT.format(**build_context(product, audience, tone, tagline)))
        return parse_social_json(raw)
    except Exception as e:
        raise RuntimeError(friendly_error(e, "Social")) from e
