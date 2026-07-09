"""
critic.py — AI self-critique loop.
Evaluates tagline, blog, and social posts.
Automatically triggers regeneration for failed items (max MAX_RETRIES).
"""

from typing import Callable, Optional
from config import CRITIC_PROMPT
from utils import build_context, parse_json_response, friendly_error
from text_gen import _call, generate_tagline, generate_blog_intro, generate_social_posts

MAX_RETRIES = 2
PASS_THRESHOLD = 7


def _evaluate(product: str, audience: str, tone: str,
               tagline: str, blog: str, social: dict) -> dict:
    """Run the critic LLM and return parsed scores."""
    ctx = build_context(product, audience, tone, tagline)
    social_str = f"Twitter: {social.get('twitter','')} | Instagram: {social.get('instagram','')} | LinkedIn: {social.get('linkedin','')}"
    prompt = CRITIC_PROMPT.format(
        product=product,
        audience=audience,
        tone_desc=ctx["tone_desc"],
        tagline=tagline,
        blog=blog[:300],
        social=social_str[:300],
    )
    try:
        raw = _call(prompt)
        data = parse_json_response(raw)
        # Ensure required keys with safe defaults
        return {
            "tagline_score":    int(data.get("tagline_score", 5)),
            "tagline_feedback": data.get("tagline_feedback", ""),
            "tagline_pass":     bool(data.get("tagline_pass", True)),
            "blog_score":       int(data.get("blog_score", 5)),
            "blog_feedback":    data.get("blog_feedback", ""),
            "blog_pass":        bool(data.get("blog_pass", True)),
            "social_score":     int(data.get("social_score", 5)),
            "social_feedback":  data.get("social_feedback", ""),
            "social_pass":      bool(data.get("social_pass", True)),
            "overall":          data.get("overall", "Evaluation complete."),
        }
    except Exception:
        # Critic failure is non-fatal — return neutral pass
        return {
            "tagline_score": 7, "tagline_feedback": "Critic unavailable.", "tagline_pass": True,
            "blog_score":    7, "blog_feedback":    "Critic unavailable.", "blog_pass":    True,
            "social_score":  7, "social_feedback":  "Critic unavailable.", "social_pass":  True,
            "overall": "Critic evaluation unavailable.",
        }


def run_critic_loop(
    product: str,
    audience: str,
    tone: str,
    tagline: str,
    blog: str,
    social: dict,
    status_callback: Optional[Callable[[str], None]] = None,
) -> tuple:
    """
    Evaluate content, regenerate failing assets up to MAX_RETRIES times.

    Returns:
        (tagline, blog, social, critic_report)
    """
    for attempt in range(1, MAX_RETRIES + 2):   # +2: initial eval + retries
        if status_callback:
            status_callback(f"Critic evaluation (attempt {attempt})…")

        report = _evaluate(product, audience, tone, tagline, blog, social)

        all_pass = report["tagline_pass"] and report["blog_pass"] and report["social_pass"]

        if all_pass or attempt > MAX_RETRIES:
            report["retries"] = attempt - 1
            return tagline, blog, social, report

        # Regenerate only the failing assets
        if not report["tagline_pass"]:
            if status_callback:
                status_callback(f"Regenerating tagline (score {report['tagline_score']}/10)…")
            try:
                tagline = generate_tagline(product, audience, tone)
            except Exception:
                pass  # keep original if regen fails

        if not report["blog_pass"]:
            if status_callback:
                status_callback(f"Regenerating blog (score {report['blog_score']}/10)…")
            try:
                blog = generate_blog_intro(product, audience, tone, tagline)
            except Exception:
                pass

        if not report["social_pass"]:
            if status_callback:
                status_callback(f"Regenerating social posts (score {report['social_score']}/10)…")
            try:
                social = generate_social_posts(product, audience, tone, tagline)
            except Exception:
                pass

    report["retries"] = MAX_RETRIES
    return tagline, blog, social, report
