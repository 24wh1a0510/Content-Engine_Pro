"""
voiceover.py — Convert blog intro to narration script and generate MP3.
Uses OpenAI TTS (tts-1) via the OpenAI SDK.
"""

from pathlib import Path
from typing import Optional, Tuple

from config import OPENAI_API_KEY, AUDIO_MODEL, AUDIO_VOICE, VOICEOVER_SCRIPT_PROMPT
from utils import save_bytes, friendly_error
from text_gen import _call


def generate_narration_script(product: str, tagline: str, blog: str) -> str:
    """Convert blog intro to a natural spoken narration script."""
    prompt = VOICEOVER_SCRIPT_PROMPT.format(
        product=product,
        tagline=tagline,
        blog=blog[:500],
    )
    try:
        return _call(prompt)
    except Exception as e:
        # Fallback: truncate blog to 70 words as script
        words = blog.split()[:70]
        script = " ".join(words)
        if tagline not in script:
            script = script + f" {tagline}"
        return script


def generate_voiceover(
    product: str,
    tagline: str,
    blog: str,
) -> Tuple[Optional[Path], str]:
    """
    Generate voiceover MP3.
    Returns (audio_path_or_None, script_text).
    Never raises — audio failure is non-fatal.
    """
    script = generate_narration_script(product, tagline, blog)

    if not OPENAI_API_KEY:
        return None, script

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.audio.speech.create(
            model=AUDIO_MODEL,
            voice=AUDIO_VOICE,
            input=script,
            response_format="mp3",
        )
        audio_bytes = response.content
        path = save_bytes(audio_bytes, stem="voiceover", ext="mp3")
        return path, script
    except Exception as e:
        print(f"[Voiceover] TTS failed (non-fatal): {friendly_error(e, 'Voiceover')}")
        return None, script
