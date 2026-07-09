"""
config.py — Central configuration and prompt templates for Content Engine Pro.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# ── API Keys ───────────────────────────────────────────────────────────────────
OPENAI_API_KEY      = os.getenv("OPENAI_API_KEY", "")
OPENROUTER_API_KEY  = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_PAID_KEY = os.getenv("OPENROUTER_PAID_KEY", "")

# ── Endpoints ──────────────────────────────────────────────────────────────────
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# ── Models ─────────────────────────────────────────────────────────────────────
PRIMARY_TEXT_MODEL  = "openai/gpt-oss-20b:free"
FALLBACK_TEXT_MODELS = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "openai/gpt-4o-mini",
]
AUDIO_MODEL  = "tts-1"
AUDIO_VOICE  = "nova"
VIDEO_MODEL  = "alibaba/wan-2.6"

MAX_TOKENS = 400

# ── Tone descriptors ───────────────────────────────────────────────────────────
TONE_DESCRIPTORS = {
    "Playful": "fun, witty, youthful, uses light humour and casual language",
    "Premium": "sophisticated, polished, luxurious, aspirational, minimal jargon",
    "Eco":     "warm, earthy, conscious, purpose-driven, community-oriented",
    "Modern":  "clean, bold, forward-thinking, tech-savvy, direct",
}

# ── Channel descriptors ────────────────────────────────────────────────────────
CHANNEL_DESCRIPTORS = {
    "B2B LinkedIn": {
        "desc": "professional, data-driven, ROI-focused, formal language, business outcomes",
        "platform": "LinkedIn",
        "audience_note": "business decision-makers and professionals",
    },
    "Gen-Z TikTok": {
        "desc": "casual, trendy, short sentences, slang OK, emoji-friendly, authentic and raw",
        "platform": "TikTok",
        "audience_note": "Gen-Z users aged 16-24",
    },
    "Parents Facebook": {
        "desc": "warm, trustworthy, family-oriented, practical benefits, relatable tone",
        "platform": "Facebook",
        "audience_note": "parents aged 28-45",
    },
}

# ── Text generation prompts ────────────────────────────────────────────────────
TAGLINE_PROMPT = """
You are a world-class copywriter. Write ONE compelling campaign tagline for:

Product / Brand : {product}
Target Audience : {audience}
Brand Tone      : {tone_desc}

Rules:
- Maximum 10 words
- No quotation marks
- Return ONLY the tagline, nothing else
""".strip()

BLOG_INTRO_PROMPT = """
You are a content strategist. Write a 120-word blog introduction for:

Product / Brand : {product}
Target Audience : {audience}
Brand Tone      : {tone_desc}
Campaign Tagline: {tagline}

Rules:
- Exactly ~120 words
- Hook the reader in the first sentence
- End with a soft call-to-action
- No headers or bullet points, flowing prose only
""".strip()

SOCIAL_POSTS_PROMPT = """
You are a social media expert. Output ONLY a JSON object, nothing else.
No markdown, no explanation, no backticks. Just the raw JSON.

Product: {product}
Audience: {audience}
Tone: {tone_desc}
Tagline: {tagline}

Required format (keep each value short):
{{"twitter":"tweet under 200 chars with 1 hashtag","instagram":"caption 2 sentences with 3 hashtags","linkedin":"professional post 2 sentences no hashtags"}}
""".strip()

IMAGE_PROMPT_TEMPLATE = """
A high-quality hero marketing image for '{product}' targeting '{audience}'.
Style: {tone_desc}.
Campaign tagline: '{tagline}'.
Clean, professional, photorealistic, suitable for a brand campaign.
Wide aspect ratio, no text overlays.
""".strip()

VIDEO_PROMPT_TEMPLATE = """
A cinematic 5-second promotional video for '{product}' targeting '{audience}'.
Tone: {tone_desc}.
Campaign tagline: '{tagline}'.
Visual style: clean, modern, professional brand advertisement.
Smooth camera movement, lifestyle shots, product in use.
""".strip()

# ── Critic prompts ─────────────────────────────────────────────────────────────
CRITIC_PROMPT = """
You are a senior marketing quality reviewer. Evaluate the following content assets.

Product : {product}
Audience: {audience}
Tone    : {tone_desc}

TAGLINE : {tagline}
BLOG    : {blog}
SOCIAL  : {social}

Score each asset 1-10 and output ONLY a JSON object — no markdown, no explanation.
Format:
{{
  "tagline_score": 0,
  "tagline_feedback": "...",
  "tagline_pass": true,
  "blog_score": 0,
  "blog_feedback": "...",
  "blog_pass": true,
  "social_score": 0,
  "social_feedback": "...",
  "social_pass": true,
  "overall": "brief summary under 20 words"
}}

Pass threshold: score >= 7. Be critical and specific.
""".strip()

# ── Voiceover script prompt ────────────────────────────────────────────────────
VOICEOVER_SCRIPT_PROMPT = """
You are a professional voiceover scriptwriter. Convert this blog intro into a
natural 30-second narration script for a brand ad.

Product : {product}
Tagline : {tagline}
Blog    : {blog}

Rules:
- Max 70 words
- Warm, conversational spoken English
- End with the tagline
- No stage directions, no brackets
- Return ONLY the script
""".strip()

# ── Channel adaptation prompts ─────────────────────────────────────────────────
ADAPT_TAGLINE_PROMPT = """
Rewrite this tagline for {platform} targeting {audience_note}.
Style: {channel_desc}
Original tagline: {tagline}
Product: {product}

Return ONLY the rewritten tagline, max 12 words, no quotes.
""".strip()

ADAPT_BLOG_PROMPT = """
Rewrite this blog intro for {platform} targeting {audience_note}.
Style: {channel_desc}
Original blog: {blog}
Product: {product}

Return ONLY the rewritten blog, ~100 words, no headers.
""".strip()

ADAPT_SOCIAL_PROMPT = """
Rewrite these social posts for {platform} targeting {audience_note}.
Style: {channel_desc}
Original posts: {social}
Product: {product}

Output ONLY a JSON object:
{{"twitter":"...","instagram":"...","linkedin":"..."}}
""".strip()
