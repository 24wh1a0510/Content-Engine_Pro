"""
app.py — Content Engine Pro · Streamlit UI

Same layout as Content Engine, plus three new sections:
  • Critic Report
  • Voiceover Player
  • Channel Adaptation Preview
"""

import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Content Engine Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main .block-container { padding-top:2rem; padding-bottom:3rem; max-width:1200px; }

.hero-title { font-size:2.4rem; font-weight:700; color:#0F172A; line-height:1.2; margin-bottom:.15rem; }
.hero-sub   { font-size:1rem; color:#64748B; margin-bottom:2rem; }
.accent     { background:linear-gradient(135deg,#6366F1,#8B5CF6);
              -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }

.section-header { font-size:.85rem; font-weight:600; color:#374151; text-transform:uppercase;
                  letter-spacing:.08em; margin-bottom:1rem; padding-bottom:.5rem;
                  border-bottom:2px solid #E5E7EB; }

.card { background:#FFFFFF; border-radius:14px; padding:1.25rem 1.4rem; margin-bottom:1rem;
        box-shadow:0 1px 3px rgba(0,0,0,.06),0 4px 16px rgba(0,0,0,.05); border:1px solid #F1F5F9; }
.card-title { font-size:.72rem; font-weight:600; text-transform:uppercase;
              letter-spacing:.1em; color:#94A3B8; margin-bottom:.6rem; }
.card-body  { font-size:.93rem; color:#1E293B; line-height:1.75; }
.card-placeholder { color:#CBD5E1; font-style:italic; }

.tagline-text { font-size:1.4rem; font-weight:700; color:#1E293B; line-height:1.4; }

.badge { display:inline-block; font-size:.68rem; font-weight:600; text-transform:uppercase;
         letter-spacing:.07em; padding:2px 9px; border-radius:20px; margin-bottom:5px; }
.badge-tw { background:#E0F2FE; color:#0369A1; }
.badge-ig { background:#FDF2F8; color:#9D174D; }
.badge-li { background:#EFF6FF; color:#1D4ED8; }
.social-block { margin-bottom:.9rem; padding-bottom:.9rem; border-bottom:1px solid #F1F5F9; }
.social-block:last-child { border-bottom:none; margin-bottom:0; padding-bottom:0; }

.script-box { background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px;
              padding:.85rem 1rem; font-size:.88rem; color:#334155;
              line-height:1.7; font-style:italic; }

/* Critic */
.critic-pass { background:#F0FDF4; border:1px solid #BBF7D0; border-radius:10px;
               padding:.75rem 1rem; color:#166534; font-size:.87rem; margin-bottom:.5rem; }
.critic-fail { background:#FFF1F2; border:1px solid #FECDD3; border-radius:10px;
               padding:.75rem 1rem; color:#BE123C; font-size:.87rem; margin-bottom:.5rem; }
.score-pill  { display:inline-block; font-weight:700; font-size:.85rem;
               padding:2px 10px; border-radius:12px; margin-right:6px; }
.score-hi  { background:#DCFCE7; color:#166534; }
.score-mid { background:#FEF9C3; color:#854D0E; }
.score-lo  { background:#FEE2E2; color:#991B1B; }

/* Channel chip */
.channel-chip { display:inline-block; font-size:.72rem; font-weight:700; text-transform:uppercase;
                letter-spacing:.08em; padding:3px 12px; border-radius:20px;
                background:#EEF2FF; color:#4338CA; margin-bottom:.75rem; }

[data-testid="stSidebar"] { background:#FAFAFA; border-right:1px solid #F1F5F9; }
.sidebar-brand { font-size:1.1rem; font-weight:700; color:#1E293B; }
.sidebar-sub   { font-size:.78rem; color:#94A3B8; margin-bottom:1rem; }

div[data-testid="stButton"] > button {
    width:100%; padding:.75rem 1rem;
    background:linear-gradient(135deg,#6366F1,#8B5CF6);
    color:white !important; font-weight:600; font-size:.92rem;
    border:none; border-radius:10px; cursor:pointer;
    box-shadow:0 4px 14px rgba(99,102,241,.35); transition:opacity .15s;
}
div[data-testid="stButton"] > button:hover    { opacity:.88; }
div[data-testid="stButton"] > button:disabled { opacity:.5; cursor:not-allowed; }
.stProgress > div > div > div > div { background:linear-gradient(135deg,#6366F1,#8B5CF6); }
.err { background:#FFF1F2; border:1px solid #FECDD3; border-radius:10px;
       padding:.85rem 1rem; color:#BE123C; font-size:.87rem; margin-bottom:.75rem; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
DEFAULTS = {
    "tagline": None, "blog_intro": None, "social_posts": None,
    "hero_path": None, "audio_path": None, "audio_script": None,
    "video_path": None, "errors": [],
    "critic_report": None,
    "voiceover_path": None, "voiceover_script": None,
    "adapted": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">⚡ Content Engine Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Brief in → five assets + critic + voiceover + adaptation.</div>', unsafe_allow_html=True)
    st.divider()

    product  = st.text_input("🏷️ Product / Brand Name", placeholder="e.g. NovaBrew Coffee")
    audience = st.text_input("🎯 Target Audience",       placeholder="e.g. Remote workers 25–40")
    tone     = st.selectbox("🎨 Brand Tone", ["Playful", "Premium", "Eco", "Modern"])

    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("✨ Generate Campaign", use_container_width=True)
    st.divider()

    st.markdown("**🔄 Channel Adaptation**")
    channel = st.selectbox("Target Channel", ["B2B LinkedIn", "Gen-Z TikTok", "Parents Facebook"])
    adapt_btn = st.button("🔀 Adapt for Channel", use_container_width=True,
                          disabled=not st.session_state.tagline)
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Text & Audio → OpenAI\nVideo → OpenRouter (Wan 2.6)")

# ── Page header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-title">AI <span class="accent">Content Engine Pro</span></div>
<div class="hero-sub">Brief In &nbsp;→&nbsp; Five Assets · Critic Loop · Voiceover · Channel Adaptation</div>
""", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
def plain_card(title, body_html, placeholder="Waiting for generation…"):
    body = body_html if body_html else f'<span class="card-placeholder">{placeholder}</span>'
    st.markdown(f'<div class="card"><div class="card-title">{title}</div>'
                f'<div class="card-body">{body}</div></div>', unsafe_allow_html=True)

def tagline_card(tagline):
    body = (f'<div class="tagline-text">"{tagline}"</div>'
            if tagline else '<span class="card-placeholder">Your tagline will appear here…</span>')
    st.markdown(f'<div class="card"><div class="card-title">💡 Campaign Tagline</div>'
                f'<div class="card-body">{body}</div></div>', unsafe_allow_html=True)

def social_card(posts, title="📲 Social Media Posts"):
    if not posts:
        plain_card(title, "", "Twitter · Instagram · LinkedIn posts will appear here…")
        return
    def block(cls, label, text):
        safe = (text or "").replace("\n", "<br>")
        return (f'<div class="social-block"><span class="badge {cls}">{label}</span>'
                f'<div style="font-size:.9rem;color:#1E293B;line-height:1.65">{safe}</div></div>')
    inner = (block("badge-tw", "𝕏 Twitter",   posts.get("twitter",""))
           + block("badge-ig", "📸 Instagram", posts.get("instagram",""))
           + block("badge-li", "💼 LinkedIn",  posts.get("linkedin","")))
    st.markdown(f'<div class="card"><div class="card-title">{title}</div>'
                f'<div class="card-body">{inner}</div></div>', unsafe_allow_html=True)

def score_pill(score):
    cls = "score-hi" if score >= 8 else "score-mid" if score >= 6 else "score-lo"
    return f'<span class="score-pill {cls}">{score}/10</span>'

def err_card(msg):
    st.markdown(f'<div class="err">⚠️ {msg}</div>', unsafe_allow_html=True)

# ── Main layout — two columns ──────────────────────────────────────────────────
left, right = st.columns(2, gap="large")

with left:
    st.markdown('<div class="section-header">📝 Text Assets</div>', unsafe_allow_html=True)
    tagline_card(st.session_state.tagline)
    blog_html = (st.session_state.blog_intro.replace("\n","<br>")
                 if st.session_state.blog_intro else "")
    plain_card("📰 Blog Introduction", blog_html, "200-word blog intro will appear here…")
    social_card(st.session_state.social_posts)

with right:
    st.markdown('<div class="section-header">🎨 Visual & Audio Assets</div>', unsafe_allow_html=True)

    # Hero image
    st.markdown('<div class="card"><div class="card-title">🎨 Hero Image</div>', unsafe_allow_html=True)
    if st.session_state.hero_path and Path(st.session_state.hero_path).exists():
        st.image(str(st.session_state.hero_path), use_column_width=True)
    else:
        st.markdown('<div class="card-body"><span class="card-placeholder">AI-generated hero image will appear here…</span></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Audio voiceover
    st.markdown('<div class="card"><div class="card-title">🔊 Audio Voiceover (30s Ad)</div>', unsafe_allow_html=True)
    if st.session_state.audio_path and Path(st.session_state.audio_path).exists():
        st.audio(str(st.session_state.audio_path), format="audio/mp3")
        if st.session_state.audio_script:
            st.markdown(f'<div class="script-box">📄 Script: {st.session_state.audio_script}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card-body"><span class="card-placeholder">AI-generated voiceover audio will appear here…</span></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Promo video
    st.markdown('<div class="card"><div class="card-title">🎬 Promotional Video</div>', unsafe_allow_html=True)
    if st.session_state.video_path and Path(st.session_state.video_path).exists():
        st.video(str(st.session_state.video_path))
        st.caption("Generated with Wan 2.6 via OpenRouter")
    else:
        st.markdown('<div class="card-body"><span class="card-placeholder">AI-generated promo video will appear here… (1–3 min)</span></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Errors ─────────────────────────────────────────────────────────────────────
for e in st.session_state.errors:
    err_card(e)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — CRITIC REPORT
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-header">🧠 Critic Report — AI Self-Evaluation</div>', unsafe_allow_html=True)

if st.session_state.critic_report:
    r = st.session_state.critic_report
    retries = r.get("retries", 0)
    if retries:
        st.info(f"🔄 {retries} regeneration(s) triggered by the critic loop.")

    c1, c2, c3 = st.columns(3)
    for col, key, label in [
        (c1, "tagline", "💡 Tagline"),
        (c2, "blog",    "📰 Blog"),
        (c3, "social",  "📲 Social"),
    ]:
        with col:
            score    = r.get(f"{key}_score", 0)
            feedback = r.get(f"{key}_feedback", "")
            passed   = r.get(f"{key}_pass", True)
            verdict  = "✅ Passed" if passed else "❌ Failed"
            cls      = "critic-pass" if passed else "critic-fail"
            st.markdown(
                f'<div class="{cls}">{score_pill(score)} <strong>{label}</strong> — {verdict}'
                f'<br><span style="font-size:.82rem">{feedback}</span></div>',
                unsafe_allow_html=True,
            )

    overall = r.get("overall", "")
    if overall:
        st.markdown(f'<div class="card"><div class="card-title">Overall</div>'
                    f'<div class="card-body">{overall}</div></div>', unsafe_allow_html=True)
else:
    plain_card("🧠 Critic Evaluation", "", "Run the campaign to see the AI critic's evaluation…")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — VOICEOVER PLAYER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-header">🎙️ Voiceover Player</div>', unsafe_allow_html=True)

st.markdown('<div class="card"><div class="card-title">🎙️ Blog Narration Audio</div>', unsafe_allow_html=True)
if st.session_state.voiceover_path and Path(st.session_state.voiceover_path).exists():
    st.audio(str(st.session_state.voiceover_path), format="audio/mp3")
    if st.session_state.voiceover_script:
        st.markdown(f'<div class="script-box">📄 Narration Script:<br><br>'
                    f'{st.session_state.voiceover_script.replace(chr(10),"<br>")}</div>',
                    unsafe_allow_html=True)
elif st.session_state.voiceover_script:
    st.markdown(f'<div class="card-body"><em>Audio generation requires OPENAI_API_KEY.</em>'
                f'<br><br><div class="script-box">📄 Script (no audio):<br><br>'
                f'{st.session_state.voiceover_script.replace(chr(10),"<br>")}</div></div>',
                unsafe_allow_html=True)
else:
    st.markdown('<div class="card-body"><span class="card-placeholder">'
                'Blog narration audio will appear here after generation…</span></div>',
                unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — CHANNEL ADAPTATION PREVIEW
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-header">🔀 Channel Adaptation Preview</div>', unsafe_allow_html=True)

if st.session_state.adapted:
    a = st.session_state.adapted
    ch = a.get("channel", channel)
    st.markdown(f'<span class="channel-chip">📡 {ch}</span>', unsafe_allow_html=True)
    if a.get("error"):
        err_card(a["error"])

    al, ar = st.columns(2, gap="large")
    with al:
        st.markdown('<div class="section-header" style="font-size:.75rem">Adapted Text</div>', unsafe_allow_html=True)
        tagline_card(a.get("tagline"))
        blog_html = (a["blog"].replace("\n","<br>") if a.get("blog") else "")
        plain_card("📰 Adapted Blog", blog_html, "Adapted blog will appear here…")

    with ar:
        social_card(a.get("social"), title=f"📲 {ch} Posts")
        plain_card("🎨 Hero Image", "<em style='color:#94A3B8'>Image unchanged — adaptation only rewrites text.</em>")
        plain_card("🎬 Video",      "<em style='color:#94A3B8'>Video unchanged — adaptation only rewrites text.</em>")
else:
    plain_card("🔀 Adapted Content", "",
               "Select a channel in the sidebar and click Adapt for Channel…")

# ═══════════════════════════════════════════════════════════════════════════════
# GENERATION PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════
if generate_btn:
    if not product.strip():
        st.warning("Please enter a Product / Brand Name.", icon="⚠️"); st.stop()
    if not audience.strip():
        st.warning("Please enter a Target Audience.", icon="⚠️"); st.stop()

    for k in DEFAULTS:
        st.session_state[k] = DEFAULTS[k]

    bar    = st.progress(0)
    status = st.empty()

    def step(pct, msg):
        bar.progress(pct)
        status.markdown(f"⏳ **{msg}**")

    try:
        from text_gen   import generate_tagline, generate_blog_intro, generate_social_posts
        from image_gen  import generate_hero_image
        from video_gen  import generate_promo_video
        from critic     import run_critic_loop
        from voiceover  import generate_voiceover

        # Step 1 — tagline
        step(8, "Crafting your campaign tagline…")
        tagline = generate_tagline(product, audience, tone)
        st.session_state.tagline = tagline

        # Step 2 — blog
        step(18, "Writing the blog introduction…")
        blog = generate_blog_intro(product, audience, tone, tagline)
        st.session_state.blog_intro = blog

        # Step 3 — social posts
        step(28, "Generating social media posts…")
        social = generate_social_posts(product, audience, tone, tagline)
        st.session_state.social_posts = social

        # Step 4 — critic loop (may regenerate failed assets)
        step(40, "Running AI critic evaluation…")
        def critic_cb(msg):
            status.markdown(f"🧠 **{msg}**")
        tagline, blog, social, critic_report = run_critic_loop(
            product, audience, tone, tagline, blog, social,
            status_callback=critic_cb,
        )
        st.session_state.tagline       = tagline
        st.session_state.blog_intro    = blog
        st.session_state.social_posts  = social
        st.session_state.critic_report = critic_report

        # Step 5 — hero image
        step(52, "Generating hero image with DALL-E 3…")
        try:
            st.session_state.hero_path = str(generate_hero_image(product, audience, tone, tagline))
        except RuntimeError as e:
            st.session_state.errors.append(str(e))

        # Step 6 — voiceover (blog → script → MP3)
        step(63, "Generating blog narration voiceover…")
        vo_path, vo_script = generate_voiceover(product, tagline, blog)
        st.session_state.voiceover_path   = str(vo_path) if vo_path else None
        st.session_state.voiceover_script = vo_script

        # Step 7 — legacy ad voiceover (short script via TTS)
        step(72, "Generating ad voiceover audio…")
        try:
            from voiceover import generate_voiceover as _gv
            # reuse voiceover module with tagline-only short script
            from config import OPENAI_API_KEY as _key
            if _key:
                from openai import OpenAI as _OAI
                _c = _OAI(api_key=_key)
                short_script = f"{tagline}. Discover {product} today."
                _r = _c.audio.speech.create(model="tts-1", voice="nova",
                                            input=short_script, response_format="mp3")
                from utils import save_bytes as _sb
                _p = _sb(_r.content, "ad_voiceover", "mp3")
                st.session_state.audio_path   = str(_p)
                st.session_state.audio_script = short_script
        except Exception:
            pass

        # Step 8 — promo video
        video_info = st.empty()
        step(82, "Submitting video job to OpenRouter (Wan 2.6)…")
        def video_cb(msg):
            video_info.info(f"🎬 {msg}")
        try:
            vp = generate_promo_video(product, audience, tone, tagline,
                                      status_callback=video_cb)
            st.session_state.video_path = str(vp)
            video_info.empty()
        except RuntimeError as e:
            st.session_state.errors.append(str(e))
            video_info.empty()

        step(100, "All assets generated!")
        status.success("✅ Campaign generated successfully!")
        bar.empty()
        st.rerun()

    except RuntimeError as e:
        bar.empty(); status.empty()
        st.error(f"Generation failed: {e}", icon="🚫")
    except Exception as e:
        bar.empty(); status.empty()
        st.error(f"Unexpected error: {e}", icon="🚫")

# ═══════════════════════════════════════════════════════════════════════════════
# CHANNEL ADAPTATION PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════
if adapt_btn and st.session_state.tagline:
    bar    = st.progress(0)
    status = st.empty()

    def step(pct, msg):
        bar.progress(pct)
        status.markdown(f"⏳ **{msg}**")

    try:
        from adapter import adapt_for_channel
        step(20, f"Adapting content for {channel}…")

        def adapt_cb(msg):
            status.markdown(f"🔀 **{msg}**")

        adapted = adapt_for_channel(
            product  = product,
            audience = audience,
            channel  = channel,
            tagline  = st.session_state.tagline,
            blog     = st.session_state.blog_intro or "",
            social   = st.session_state.social_posts or {},
            status_callback=adapt_cb,
        )
        st.session_state.adapted = adapted
        step(100, f"Adaptation complete for {channel}!")
        status.success(f"✅ Adapted for {channel}!")
        bar.empty()
        st.rerun()

    except Exception as e:
        bar.empty(); status.empty()
        st.error(f"Adaptation failed: {e}", icon="🚫")
