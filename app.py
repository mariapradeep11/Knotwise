
import streamlit as st
import pandas as pd
from datetime import date, datetime
from io import BytesIO
import base64
import json
from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

st.set_page_config(
    page_title="KnotWise | AI Prenup Preparation",
    page_icon="💍",
    layout="wide",
)

# ── Theme ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0C0C0C !important;
    color: #D4CFC8 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"] { background: #0C0C0C !important; }
[data-testid="stSidebar"] {
    background: #080808 !important;
    border-right: 1px solid #141414 !important;
}

/* Nav row */
div[data-testid="stHorizontalBlock"]:first-of-type .stButton button {
    background: transparent !important; border: none !important;
    border-bottom: 1px solid #2E2E2E !important; border-radius: 0 !important;
    color: #888 !important; font-size: 0.65rem !important;
    letter-spacing: 0.06em !important; text-transform: uppercase !important;
    padding: 0.65rem 0.2rem !important; line-height: 1.6 !important;
    transition: color 0.2s, border-color 0.2s !important;
    font-family: 'Inter', sans-serif !important;
    white-space: nowrap !important;
}
div[data-testid="stHorizontalBlock"]:first-of-type .stButton button:hover {
    color: #CCC !important; border-bottom-color: #666 !important;
}

h1, h2, h3, h4 {
    font-family: 'Playfair Display', serif !important;
    color: #F0EBE3 !important; font-weight: 400 !important;
}
h1 { font-size: 2.6rem !important; line-height: 1.18 !important; }
h2 { font-size: 1.7rem !important; }
p, li { color: #999 !important; line-height: 1.75 !important; }

section[data-testid="stSidebar"] h2 { font-size: 1.4rem !important; color: #F0EBE3 !important; }
section[data-testid="stSidebar"] p { color: #AAA !important; font-size: 0.76rem !important; }

[data-testid="metric-container"] {
    background: #0A0A0A !important; border: 1px solid #161616 !important;
    border-radius: 2px !important; padding: 1.2rem 1rem !important;
}
[data-testid="stMetricLabel"] p {
    color: #666 !important; font-size: 0.58rem !important;
    letter-spacing: 0.2em !important; text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    color: #8A9E58 !important; font-size: 1.9rem !important;
}

[data-baseweb="input"] > div { background: #080808 !important; border-color: #1C1C1C !important; border-radius: 2px !important; }
/* ── Inputs & textareas ── */
[data-baseweb="input"] { background: #0E0E0E !important; border-color: #252525 !important; border-radius: 2px !important; }
[data-baseweb="input"] input { color: #E8E4DE !important; font-size: 0.9rem !important; font-family: 'Inter', sans-serif !important; background: transparent !important; }
[data-baseweb="textarea"] { background: #0E0E0E !important; border-color: #252525 !important; border-radius: 2px !important; }
[data-baseweb="textarea"] textarea { color: #E8E4DE !important; font-size: 0.9rem !important; font-family: 'Inter', sans-serif !important; background: transparent !important; caret-color: #8A9E58 !important; }
input, textarea { color: #E8E4DE !important; font-family: 'Inter', sans-serif !important; }
input::placeholder, textarea::placeholder { color: #3A3A3A !important; }

/* ── Select ── */
[data-baseweb="select"] > div { background: #0E0E0E !important; border-color: #252525 !important; border-radius: 2px !important; }
[data-baseweb="select"] [data-baseweb="select"] > div { background: #0E0E0E !important; }
div[data-baseweb="select"] > div > div { color: #E8E4DE !important; font-size: 0.9rem !important; }
[data-baseweb="menu"] { background: #141414 !important; border: 1px solid #252525 !important; border-radius: 2px !important; }
[data-baseweb="menu"] li { background: #141414 !important; color: #C8C4BE !important; font-size: 0.85rem !important; }
[data-baseweb="menu"] li:hover { background: #1C1C1C !important; color: #E8E4DE !important; }
[data-baseweb="menu"] [aria-selected="true"] { background: #1A1A1A !important; color: #8A9E58 !important; }

/* ── Number input stepper buttons — keep neutral, not olive ── */
[data-testid="stNumberInput"] button {
    background: #141414 !important; border: 1px solid #252525 !important;
    color: #888 !important; border-radius: 2px !important;
    font-size: 0.8rem !important; padding: 0.3rem 0.6rem !important;
    letter-spacing: 0 !important; text-transform: none !important;
}
[data-testid="stNumberInput"] button:hover { background: #1E1E1E !important; color: #CCC !important; }

/* ── Labels ── */
label, .stSelectbox label, .stTextInput label, .stNumberInput label, .stTextArea label {
    color: #888 !important; font-size: 0.66rem !important;
    letter-spacing: 0.1em !important; text-transform: uppercase !important;
    font-weight: 500 !important;
}
[data-testid="stCheckbox"] label span { color: #B0ACA6 !important; font-size: 0.82rem !important; }

/* ── Action buttons (outline style) ── */
.stButton > button:not([data-testid]) {
    background: transparent !important; border: 1px solid #8A9E58 !important;
    color: #8A9E58 !important; font-size: 0.68rem !important;
    letter-spacing: 0.12em !important; text-transform: uppercase !important;
    border-radius: 0 !important; padding: 0.55rem 1.4rem !important;
    font-weight: 500 !important;
}
.stButton > button {
    background: transparent !important; border: 1px solid #8A9E58 !important;
    color: #8A9E58 !important; font-size: 0.68rem !important;
    letter-spacing: 0.12em !important; text-transform: uppercase !important;
    border-radius: 0 !important; padding: 0.55rem 1.4rem !important;
    font-weight: 500 !important;
}
.stButton > button:hover { background: #8A9E58 !important; color: #050505 !important; }

/* ── Form submit — outline with olive ── */
[data-testid="stFormSubmitButton"] button {
    background: transparent !important; color: #8A9E58 !important;
    border: 1px solid #8A9E58 !important; font-weight: 600 !important;
    font-size: 0.72rem !important; letter-spacing: 0.12em !important;
    text-transform: uppercase !important; border-radius: 0 !important;
    padding: 0.65rem 2rem !important; transition: all 0.2s !important;
}
[data-testid="stFormSubmitButton"] button:hover {
    background: #8A9E58 !important; color: #F0EBE3 !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important; color: #8A9E58 !important;
    border: 1px solid #8A9E58 !important; border-radius: 0 !important;
    font-size: 0.72rem !important; letter-spacing: 0.12em !important;
    text-transform: uppercase !important; font-weight: 600 !important;
    padding: 0.65rem 2rem !important; transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: #8A9E58 !important; color: #F0EBE3 !important;
}

div[data-testid="stProgressBar"] > div > div > div {
    background: linear-gradient(90deg, #8A9E58 0%, #A8BC78 100%) !important;
}

[data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid #181818 !important; }
button[data-baseweb="tab"] {
    background: transparent !important; color: #777 !important;
    font-size: 0.66rem !important; letter-spacing: 0.1em !important;
    text-transform: uppercase !important; padding: 0.7rem 1.2rem !important;
    font-weight: 500 !important;
}
button[data-baseweb="tab"][aria-selected="true"] { color: #8A9E58 !important; border-bottom: 2px solid #8A9E58 !important; }

[data-testid="stForm"] { background: #070707 !important; border: 1px solid #131313 !important; border-radius: 2px !important; padding: 1.8rem !important; }
details { border: 1px solid #131313 !important; border-radius: 2px !important; background: #070707 !important; }
details summary { color: #8A9E58 !important; font-size: 0.7rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }
[data-testid="stAlert"] { background: #070707 !important; border-radius: 2px !important; border-left: 2px solid #8A9E58 !important; }
[data-testid="stAlert"] p { color: #888 !important; font-size: 0.76rem !important; }
hr { border-color: #131313 !important; margin: 1.5rem 0 !important; }
[data-testid="stDataFrame"] { border: 1px solid #131313 !important; border-radius: 2px !important; }
[data-testid="stFileUploadDropzone"] { background: #070707 !important; border-color: #1C1C1C !important; border-radius: 2px !important; }
code { background: #080808 !important; color: #8A9E58 !important; border-radius: 2px !important; }
pre { background: #070707 !important; border: 1px solid #131313 !important; border-radius: 2px !important; }
.stCaption p { color: #444 !important; font-size: 0.62rem !important; letter-spacing: 0.06em !important; }
.stTextArea textarea { color: #D4CFC8 !important; }
.block-container { padding: 2.5rem 2.5rem 2.5rem !important; max-width: 1200px !important; }

/* Hero containers */
.kw-hero { position: relative; width: 100%; overflow: hidden; border-radius: 2px; margin-bottom: 2rem; }
.kw-hero img { width: 100%; height: 100%; object-fit: cover; display: block; animation: kwFadeScale 1.6s cubic-bezier(0.22,1,0.36,1) both; }
.kw-hero-grad { position: absolute; inset: 0; pointer-events: none; background: linear-gradient(to bottom, rgba(12,12,12,0.05) 35%, rgba(12,12,12,0.65) 78%, #0C0C0C 100%); }
.kw-hero-col { position: relative; width: 100%; overflow: hidden; border-radius: 2px; }
.kw-hero-col img { width: 100%; height: 100%; object-fit: cover; display: block; animation: kwFadeScale 1.6s cubic-bezier(0.22,1,0.36,1) both; }
.kw-hero-col-grad { position: absolute; inset: 0; pointer-events: none; background: linear-gradient(to bottom, transparent 45%, rgba(12,12,12,0.75) 85%, #0C0C0C 100%); }

@keyframes kwFadeScale { from { opacity: 0; transform: scale(1.07); } to { opacity: 1; transform: scale(1); } }
@keyframes kwPageIn {
  0%   { opacity: 0; transform: translateY(24px); }
  100% { opacity: 1; transform: translateY(0); }
}
section.main > div { animation: kwPageIn 0.65s cubic-bezier(0.16, 1, 0.3, 1) both; }
[data-testid="stForm"], [data-testid="stVerticalBlock"] > div { animation: kwPageIn 0.55s cubic-bezier(0.16, 1, 0.3, 1) both; animation-delay: 0.04s; }

.kw-nav-active { text-align: center; padding: 0.65rem 0.2rem; border-bottom: 2px solid #8A9E58; }
.kw-nav-active-num { font-size: 0.65rem; color: #8A9E58; letter-spacing: 0.06em; font-family: 'Inter', sans-serif; text-transform: uppercase; white-space: nowrap; }
.kw-nav-active-label { font-size: 0.65rem; color: #8A9E58; margin-top: 0.1rem; font-family: 'Inter', sans-serif; white-space: nowrap; font-weight: 500; }
.kw-nav-sep { width: 100%; height: 1px; background: #111; margin: 0 0 2rem 0; }

/* AI generation box */
.kw-ai-box {
    border: 1px solid #8A9E5822;
    border-left: 3px solid #8A9E58;
    background: #0A0A08;
    padding: 1.5rem;
    border-radius: 2px;
    margin: 1rem 0;
}
.kw-lock-box {
    border: 1px solid #1E1E1E;
    background: #080808;
    padding: 1.5rem;
    border-radius: 2px;
    margin: 1rem 0;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ── Persistence ───────────────────────────────────────────────────────────
_SAVE_FILE = Path("knotwise_save.json")
_SAVE_KEYS = [
    "page", "case_created", "case",
    "partner_a", "partner_b",
    "assets_a", "assets_b",
    "debts_a", "debts_b",
    "goals_a", "goals_b",
    "uploaded_docs", "partner_invited", "invite_email",
    "ai_draft", "signoff_a", "signoff_b",
]

def save_state():
    try:
        _SAVE_FILE.write_text(
            json.dumps({k: st.session_state.get(k) for k in _SAVE_KEYS}, default=str)
        )
    except Exception:
        pass

def _load_persisted():
    if not _SAVE_FILE.exists():
        return
    try:
        saved = json.loads(_SAVE_FILE.read_text())
        for k, v in saved.items():
            if k in _SAVE_KEYS:
                st.session_state[k] = v
    except Exception:
        pass

def clear_state():
    if _SAVE_FILE.exists():
        _SAVE_FILE.unlink()
    for k in _SAVE_KEYS:
        st.session_state.pop(k, None)
    st.session_state.pop("_state_loaded", None)


# ── Session State ─────────────────────────────────────────────────────────
def init_state():
    # Load from disk once per browser session (not on every rerun)
    if "_state_loaded" not in st.session_state:
        st.session_state["_state_loaded"] = True
        _load_persisted()

    defaults = {
        "page": "welcome",
        "case_created": False, "case": {},
        "partner_a": {}, "partner_b": {},
        "assets_a": [], "assets_b": [],
        "debts_a": [], "debts_b": [],
        "goals_a": {}, "goals_b": {},
        "uploaded_docs": [], "partner_invited": False, "invite_email": "",
        "ai_draft": None,
        "signoff_a": {}, "signoff_b": {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── Navigation ────────────────────────────────────────────────────────────
STEPS = [
    ("welcome",  "Welcome"),
    ("setup",    "Case"),
    ("partner",  "Invite"),
    ("qa",       "Partner A"),
    ("qb",       "Partner B"),
    ("assets",   "Assets"),
    ("risk",     "Risk"),
    ("draft",    "Draft"),
    ("signoff",  "Signoff"),
    ("final",    "Final"),
]
STEP_KEYS = [s[0] for s in STEPS]

def step_done(key):
    return {
        "setup":   st.session_state.case_created,
        "partner": st.session_state.partner_invited,
        "qa":      bool(st.session_state.partner_a),
        "qb":      bool(st.session_state.partner_b),
        "assets":  bool(st.session_state.assets_a or st.session_state.assets_b),
        "risk":    bool(st.session_state.goals_a and st.session_state.goals_b),
        "draft":   bool(st.session_state.ai_draft),
        "signoff": bool(st.session_state.signoff_a.get("agreed") and st.session_state.signoff_b.get("agreed")),
        "final":   False,
    }.get(key, True)

def ai_ready():
    return (st.session_state.case_created and
            bool(st.session_state.partner_a) and
            bool(st.session_state.partner_b) and
            bool(st.session_state.goals_a) and
            bool(st.session_state.goals_b))

def go(key):
    st.session_state.page = key
    save_state()
    st.rerun()

def render_nav():
    current = st.session_state.page
    cols = st.columns(len(STEPS))
    for i, (col, (key, label)) in enumerate(zip(cols, STEPS)):
        is_active = (key == current)
        is_done   = step_done(key) and not is_active
        num = str(i + 1).zfill(2)
        with col:
            if is_active:
                st.markdown(
                    f'<div class="kw-nav-active">'
                    f'<div class="kw-nav-active-num">{num}</div>'
                    f'<div class="kw-nav-active-label">{label}</div>'
                    f'</div>', unsafe_allow_html=True)
            else:
                icon = "✓" if is_done else num
                if st.button(f"{icon}\n{label}", key=f"nav_{key}", use_container_width=True):
                    go(key)
    st.markdown('<div class="kw-nav-sep"></div>', unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────
def render_sidebar():
    st.sidebar.markdown(
        '<p style="font-size:0.55rem;letter-spacing:0.3em;text-transform:uppercase;color:#222;margin-bottom:0.1rem">Est. 2024</p>',
        unsafe_allow_html=True)
    st.sidebar.markdown(
        '<h2 style="font-family:\'Playfair Display\',serif;font-size:1.5rem;'
        'font-weight:400;color:#F0EBE3;margin:0 0 0.1rem 0;line-height:1.2">'
        'Knot<span style="color:#8A9E58">Wise</span></h2>',
        unsafe_allow_html=True,
    )
    st.sidebar.caption("AI Prenup Preparation Assistant")
    st.sidebar.divider()
    score, _ = completion_score()
    risk, _ = risk_level(score)
    st.sidebar.metric("Readiness", f"{score}/100")
    st.sidebar.progress(score / 100)
    st.sidebar.markdown(f'<p style="font-size:0.6rem;color:#8A9E58;letter-spacing:0.1em;margin:0.2rem 0 0.8rem 0">{risk} risk</p>', unsafe_allow_html=True)
    st.sidebar.divider()
    for label, key in [("Case Setup","setup"),("Partner Invited","partner"),("Partner A","qa"),("Partner B","qb"),("Assets & Debts","assets"),("Preferences Set","risk"),("AI Draft","draft"),("Both Signed Off","signoff")]:
        done = step_done(key)
        color = "#8A9E58" if done else "#888"
        icon  = "●" if done else "○"
        st.sidebar.markdown(f'<p style="color:{color};font-size:0.78rem;margin:0.35rem 0;letter-spacing:0.03em">{icon}&nbsp; {label}</p>', unsafe_allow_html=True)
    st.sidebar.divider()
    if st.sidebar.button("📋 Project Documentation", use_container_width=True, key="nav_ref"):
        go("ref")

    # ── Persistence status + reset ────────────────────────────────────────
    if _SAVE_FILE.exists():
        try:
            mtime = datetime.fromtimestamp(_SAVE_FILE.stat().st_mtime).strftime("%-I:%M %p")
            st.sidebar.markdown(
                f'<p style="font-size:0.58rem;color:#333;letter-spacing:0.06em;margin:0.6rem 0 0.2rem 0">'
                f'AUTO-SAVED {mtime}</p>', unsafe_allow_html=True)
        except Exception:
            pass

    if "confirm_reset" not in st.session_state:
        st.session_state.confirm_reset = False

    if not st.session_state.confirm_reset:
        if st.sidebar.button("↺ Start New Case", use_container_width=True, key="reset_btn"):
            st.session_state.confirm_reset = True
            st.rerun()
    else:
        st.sidebar.warning("This will erase all saved data.")
        c1, c2 = st.sidebar.columns(2)
        if c1.button("Erase", use_container_width=True, key="confirm_erase"):
            clear_state()
            st.rerun()
        if c2.button("Cancel", use_container_width=True, key="cancel_erase"):
            st.session_state.confirm_reset = False
            st.rerun()

    st.sidebar.caption("Academic prototype only. Not legal advice.")


# ── Image helpers ─────────────────────────────────────────────────────────
def _b64(filename):
    p = Path("images") / filename
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else None

def hero_full(filename, height="400px", pos="center 30%"):
    data = _b64(filename)
    if not data: return
    st.markdown(f'<div class="kw-hero" style="height:{height}"><img src="data:image/jpeg;base64,{data}" style="object-position:{pos}" /><div class="kw-hero-grad"></div></div>', unsafe_allow_html=True)

def hero_col(filename, height="500px", pos="center 25%"):
    data = _b64(filename)
    if not data: return
    st.markdown(f'<div class="kw-hero-col" style="height:{height}"><img src="data:image/jpeg;base64,{data}" style="object-position:{pos}" /><div class="kw-hero-col-grad"></div></div>', unsafe_allow_html=True)


# ── Core helpers ──────────────────────────────────────────────────────────
def money(v):
    try: return f"${float(v):,.2f}"
    except: return "$0.00"

def eyebrow(text):
    st.markdown(f'<p style="font-size:0.6rem;letter-spacing:0.28em;text-transform:uppercase;color:#8A9E58;margin-bottom:0.15rem">{text}</p>', unsafe_allow_html=True)

def gold_rule():
    st.markdown('<div style="width:34px;height:1px;background:#8A9E58;margin:0.4rem 0 1.3rem 0"></div>', unsafe_allow_html=True)

def li(text):
    st.markdown(f'<p style="color:#777;font-size:0.78rem;margin:0.22rem 0;line-height:1.6">— {text}</p>', unsafe_allow_html=True)

def pdf_safe(text):
    if not text: return ""
    for src, dst in [('’',"'"),('‘',"'"),('“','"'),('”','"'),('—','--'),('–','-'),('…','...'),(' ',' ')]:
        text = text.replace(src, dst)
    return text.encode('latin-1', errors='replace').decode('latin-1')


# ── Scoring & conflicts ───────────────────────────────────────────────────
def detect_conflicts():
    conflicts, a, b = [], st.session_state.goals_a, st.session_state.goals_b
    for key, label in [
        ("premarital_assets","Premarital asset treatment"),
        ("future_income","Future income treatment"),
        ("business_growth","Business growth / appreciation"),
        ("debt_responsibility","Debt responsibility"),
        ("spousal_support","Spousal support"),
        ("inheritance","Inheritance and family gifts"),
        ("home_purchase","Future home purchase"),
    ]:
        if a.get(key) and b.get(key) and a[key] != b[key]:
            conflicts.append({"Topic": label, "Partner A": a[key], "Partner B": b[key],
                "Severity": "High" if key in ("spousal_support","business_growth","premarital_assets") else "Medium",
                "Recommendation": "Discuss before attorney review."})
    return conflicts

def missing_documents():
    docs = {d["type"] for d in st.session_state.uploaded_docs}
    return [r for r in ["Government ID","Bank/Investment Statements","Debt Statements","Real Estate Documents","Business Ownership Documents","Retirement Account Statements"] if r not in docs]

def completion_score():
    score, explanation = 0, []
    checks = [
        (st.session_state.case_created,                                    10, "Case setup completed",              "Case setup missing"),
        (st.session_state.partner_invited,                                 10, "Partner invitation prepared",       "Partner invitation not prepared"),
        (bool(st.session_state.partner_a),                                 10, "Partner A questionnaire completed", "Partner A questionnaire missing"),
        (bool(st.session_state.partner_b),                                 10, "Partner B questionnaire completed", "Partner B questionnaire missing"),
        (bool(st.session_state.assets_a and st.session_state.assets_b),   15, "Both partners disclosed assets",    "Asset disclosure incomplete"),
        (bool(st.session_state.debts_a and st.session_state.debts_b),     10, "Both partners disclosed debts",     "Debt disclosure incomplete"),
        (bool(st.session_state.goals_a and st.session_state.goals_b),     15, "Both partners selected preferences","Partner preference responses incomplete"),
        (len(st.session_state.uploaded_docs) >= 2,                        10, "Supporting documents uploaded",     "Supporting documents limited or missing"),
    ]
    for cond, pts, pos, neg in checks:
        if cond: score += pts; explanation.append(f"{pos} (+{pts})")
        else: explanation.append(f"{neg} (+0)")
    conflicts = detect_conflicts()
    if not conflicts and st.session_state.goals_a and st.session_state.goals_b:
        score += 10; explanation.append("No major preference conflicts detected (+10)")
    elif conflicts:
        explanation.append(f"{len(conflicts)} preference conflict(s) detected (+0)")
    else:
        explanation.append("Conflict check pending (+0)")
    return min(score, 100), explanation

def risk_level(score):
    if score >= 80: return "Low",    "Strong preparation"
    if score >= 55: return "Medium", "Needs attorney clarification"
    return "High", "Missing key information"

def build_asset_df():
    rows = []
    for p, lst in [("Partner A", st.session_state.assets_a), ("Partner B", st.session_state.assets_b)]:
        for a in lst:
            rows.append({"Owner":p,"Type":a.get("asset_type"),"Description":a.get("description"),"Location":a.get("location"),"Value":a.get("value"),"Preference":a.get("preference")})
    return pd.DataFrame(rows)

def build_debt_df():
    rows = []
    for p, lst in [("Partner A", st.session_state.debts_a), ("Partner B", st.session_state.debts_b)]:
        for d in lst:
            rows.append({"Owner":p,"Type":d.get("debt_type"),"Description":d.get("description"),"Balance":d.get("balance"),"Preference":d.get("preference")})
    return pd.DataFrame(rows)


# ── AI: Theme detection ───────────────────────────────────────────────────
def detect_theme():
    a, b = st.session_state.goals_a, st.session_state.goals_b
    if not a or not b: return "General Prenuptial Agreement"
    protect, share, attorney = 0, 0, 0
    for key in ["premarital_assets","future_income","business_growth","debt_responsibility","spousal_support","inheritance","home_purchase"]:
        for g in [a, b]:
            v = g.get(key, "").lower()
            if any(w in v for w in ["separate","waived","own","keep"]): protect += 1
            elif any(w in v for w in ["share","shared","together"]): share += 1
            elif "attorney" in v or "discuss" in v: attorney += 1
    if protect >= share and protect >= attorney: return "Asset Protection Focus"
    if share >= protect and share >= attorney: return "Partnership & Sharing Focus"
    return "Comprehensive Attorney Review"


# ── AI: Prompt builder ────────────────────────────────────────────────────
def _fmt_assets(lst):
    if not lst: return "None disclosed."
    return "\n".join(f"  • {a.get('asset_type')} — {a.get('description')} ({a.get('location')}) valued at {money(a.get('value'))} — preference: {a.get('preference')}" for a in lst)

def _fmt_debts(lst):
    if not lst: return "None disclosed."
    return "\n".join(f"  • {d.get('debt_type')} — {d.get('description')} balance {money(d.get('balance'))} — preference: {d.get('preference')}" for d in lst)

def build_prenup_prompt():
    case = st.session_state.case
    pa, pb = st.session_state.partner_a, st.session_state.partner_b
    ga, gb = st.session_state.goals_a, st.session_state.goals_b
    theme = detect_theme()
    conflicts = detect_conflicts()
    conflict_notes = "\n".join(f"  • {c['Topic']}: Partner A prefers '{c['Partner A']}', Partner B prefers '{c['Partner B']}' — Severity: {c['Severity']}" for c in conflicts) if conflicts else "  None detected."

    return f"""You are a legal document assistant preparing a prenuptial agreement PREPARATION DRAFT for attorney review.

Fill in each section of the template below using the couple's specific information. Write in professional but readable legal language. Be specific — use real names, asset descriptions, and preferences. This is a preparation draft only, not a final legal document.

══════════════════════════════════════
COUPLE INFORMATION
══════════════════════════════════════
Case Name: {case.get('case_name', '')}
Wedding Date: {case.get('wedding_date', '')}
Current Residence: {case.get('current_residence', '')}
Future Residence: {case.get('future_residence', '')}
Jurisdictions: {case.get('jurisdictions', '')}
Agreement Theme: {theme}
Cross-border: {case.get('cross_border', False)}

PARTNER A: {pa.get('name', '')}
Citizenship: {pa.get('citizenship', '')} | Status: {pa.get('immigration_status', '')}
Annual Income: {money(pa.get('income', 0))}
Owns Business: {pa.get('owns_business', False)} | Owns Real Estate: {pa.get('owns_real_estate', False)}
Has Prior Children: {pa.get('has_children_prior', False)} | Supports Family: {pa.get('supports_family', False)}
Assets:
{_fmt_assets(st.session_state.assets_a)}
Debts:
{_fmt_debts(st.session_state.debts_a)}
Preferences:
  Premarital Assets: {ga.get('premarital_assets','')} | Future Income: {ga.get('future_income','')}
  Business Growth: {ga.get('business_growth','')} | Debt Responsibility: {ga.get('debt_responsibility','')}
  Spousal Support: {ga.get('spousal_support','')} | Inheritance: {ga.get('inheritance','')}
  Home Purchase: {ga.get('home_purchase','')}

PARTNER B: {pb.get('name', '')}
Citizenship: {pb.get('citizenship', '')} | Status: {pb.get('immigration_status', '')}
Annual Income: {money(pb.get('income', 0))}
Owns Business: {pb.get('owns_business', False)} | Owns Real Estate: {pb.get('owns_real_estate', False)}
Has Prior Children: {pb.get('has_children_prior', False)} | Supports Family: {pb.get('supports_family', False)}
Assets:
{_fmt_assets(st.session_state.assets_b)}
Debts:
{_fmt_debts(st.session_state.debts_b)}
Preferences:
  Premarital Assets: {gb.get('premarital_assets','')} | Future Income: {gb.get('future_income','')}
  Business Growth: {gb.get('business_growth','')} | Debt Responsibility: {gb.get('debt_responsibility','')}
  Spousal Support: {gb.get('spousal_support','')} | Inheritance: {gb.get('inheritance','')}
  Home Purchase: {gb.get('home_purchase','')}

PREFERENCE CONFLICTS TO ACKNOWLEDGE:
{conflict_notes}

══════════════════════════════════════
TEMPLATE — FILL IN EACH SECTION
══════════════════════════════════════
Use the couple's real names, assets, and preferences throughout. Replace every [FILL] placeholder with specific language derived from the information above. Keep each section focused. Output plain text with the section numbers and headers exactly as shown.

PRENUPTIAL AGREEMENT — PREPARATION DRAFT

This Prenuptial Agreement ("Agreement") is entered into by and between [FILL: full legal names, citizenship, and residency context] in contemplation of their forthcoming marriage on or around {case.get('wedding_date', '[date]')} in {case.get('future_residence', '[location]')}.

1. RECITALS
[FILL: 3-4 sentences establishing who the parties are, that they intend to marry, and the purpose of this agreement — reference their income levels, asset complexity, and the agreement theme "{theme}"]

2. FINANCIAL DISCLOSURE
[FILL: Confirm that both partners have voluntarily disclosed their financial positions. Reference the specific assets and debts categories disclosed. Note any cross-border complexity if applicable.]

3. SEPARATE PROPERTY — PREMARITAL ASSETS
[FILL: Using each partner's actual disclosed assets, specify what remains separate property for each party. Reference specific asset types (real estate, business interests, investments, retirement accounts). Reflect each partner's stated preference.]

4. MARITAL PROPERTY AND INCOME
[FILL: Define how income earned during the marriage will be treated based on both partners' stated preferences. Address any conflict between preferences if one exists.]

5. DEBT RESPONSIBILITY
[FILL: Address premarital debts specifically using the disclosed debt types and balances. Specify responsibility allocation based on each partner's preference. Note any shared responsibility agreements.]

6. BUSINESS INTERESTS AND APPRECIATION
[FILL: If either partner owns a business, address ownership, future appreciation, and dividends during marriage. If neither owns a business, state that this section is not currently applicable but may require review if circumstances change.]

7. REAL ESTATE
[FILL: Address existing real estate holdings and any future home purchase. Use the disclosed real estate assets and the stated home purchase preference.]

8. INHERITANCE, GIFTS, AND FAMILY TRANSFERS
[FILL: Define treatment of inheritance and family gifts based on both partners' stated preferences. Address any family support obligations if applicable.]

9. SPOUSAL SUPPORT
[FILL: Based on both partners' stated preferences, define whether spousal support is waived, limited, or reserved for future determination. If preferences conflict, acknowledge both positions and flag for attorney resolution.]

10. GOVERNING LAW AND JURISDICTION
[FILL: Reference the jurisdictions noted ({case.get('jurisdictions', '')}) and note that this agreement shall be governed accordingly. Flag any cross-border considerations.]

11. INDEPENDENT COUNSEL AND REVIEW
Both parties acknowledge this preparation draft has been generated for the purpose of organizing financial disclosures and identifying key discussion points prior to attorney engagement. Each party is advised to retain independent legal counsel before executing any final agreement. This document does not constitute legal advice.

12. SIGNATURES
This Agreement reflects the preliminary preferences and disclosures of both parties and is subject to revision following attorney review.

[END OF TEMPLATE]

Output only the filled-in document. No preamble, no closing commentary, no meta-notes. Start directly with "PRENUPTIAL AGREEMENT — PREPARATION DRAFT"."""


# ── Local draft generator (no API quota) ─────────────────────────────────
def generate_draft_locally():
    case  = st.session_state.case
    pa, pb = st.session_state.partner_a, st.session_state.partner_b
    ga, gb = st.session_state.goals_a,   st.session_state.goals_b
    theme  = detect_theme()
    conflicts = detect_conflicts()
    score, _ = completion_score()
    risk, risk_label = risk_level(score)
    missing_docs = missing_documents()

    na    = pa.get("name", "Partner A")
    nb    = pb.get("name", "Partner B")
    loc   = case.get("future_residence", case.get("current_residence", "[location]"))
    jur   = case.get("jurisdictions", loc)
    wdate = case.get("wedding_date", "[date to be confirmed]")
    now_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    def _p(goals, key):
        return goals.get(key, "Not specified")

    # ── Option clause builders ─────────────────────────────────────────────
    def income_clause():
        ap, bp = _p(ga,'future_income'), _p(gb,'future_income')
        if 'Shared' in ap and 'Shared' in bp:
            return "AGREED — Income earned by either Party during the marriage shall be treated as Marital Property."
        if 'Separate' in ap and 'Separate' in bp:
            return "AGREED — Income earned by each Party shall remain that Party's Separate Property unless deposited into a joint account or used for joint expenses."
        return f"ATTORNEY REVIEW REQUIRED — The Parties have not reached consistent agreement. {na}: {ap}. {nb}: {bp}."

    def sep_prop_clause():
        ap, bp = _p(ga,'premarital_assets'), _p(gb,'premarital_assets')
        if 'Keep separate' in ap and 'Keep separate' in bp:
            return "AGREED — All premarital property shall remain the Separate Property of the owning Party."
        if 'Share' in ap or 'Share' in bp:
            return f"ATTORNEY REVIEW REQUIRED — One or both Parties indicated a preference for sharing premarital property. {na}: {ap}. {nb}: {bp}."
        return f"ATTORNEY REVIEW REQUIRED — Premarital asset treatment requires further discussion. {na}: {ap}. {nb}: {bp}."

    def biz_clause():
        ap, bp = _p(ga,'business_growth'), _p(gb,'business_growth')
        if 'Keep separate' in ap and 'Keep separate' in bp:
            return "AGREED — All appreciation of Business Interests, including retained earnings, goodwill, and proceeds, shall remain Separate Property."
        if 'Share' in ap or 'Share' in bp:
            return f"ATTORNEY REVIEW REQUIRED — One or both Parties indicated a preference for sharing business appreciation. {na}: {ap}. {nb}: {bp}."
        return f"PASSIVE APPRECIATION SEPARATE; ACTIVE APPRECIATION REVIEWED — Passive appreciation shall remain Separate Property. Appreciation from marital labour or contribution during marriage may be subject to review. {na}: {ap}. {nb}: {bp}."

    def spousal_clause():
        ap, bp = _p(ga,'spousal_support'), _p(gb,'spousal_support')
        if 'Waived' in ap and 'Waived' in bp:
            return "AGREED — WAIVER: Each Party waives the right to seek spousal support, alimony, or maintenance from the other Party to the fullest extent permitted by applicable law."
        if 'Limited' in ap and 'Limited' in bp:
            return "AGREED — LIMITED: Spousal support may be available under limited circumstances to be defined with attorney review."
        if 'Reserved' in ap or 'Reserved' in bp:
            return "RIGHTS RESERVED — The Parties do not waive spousal support. Any claim shall be determined under applicable law at the time of separation or divorce."
        return f"ATTORNEY REVIEW REQUIRED — The Parties have not reached agreement. {na}: {ap}. {nb}: {bp}."

    def home_clause():
        ap, bp = _p(ga,'home_purchase'), _p(gb,'home_purchase')
        if 'Shared' in ap and 'Shared' in bp:
            return "AGREED — Any residence purchased jointly after marriage shall be treated as Marital Property and divided equally unless otherwise agreed."
        if 'contribution' in ap.lower() or 'contribution' in bp.lower():
            return "AGREED — Any residence purchased after marriage shall be owned according to each Party's documented financial contribution unless otherwise titled."
        return f"ATTORNEY REVIEW REQUIRED — Future home purchase terms require further discussion. {na}: {ap}. {nb}: {bp}."

    def inheritance_clause():
        ap, bp = _p(ga,'inheritance'), _p(gb,'inheritance')
        if 'Keep separate' in ap and 'Keep separate' in bp:
            return "AGREED — Inheritance and family gifts shall remain the Separate Property of the receiving Party."
        if 'Share' in ap or 'Share' in bp:
            return "PARTIALLY AGREED — Inheritance or gifts used for joint purposes may be treated as Marital Property. Documentation of intent at time of use is strongly recommended."
        return f"ATTORNEY REVIEW REQUIRED — Inheritance treatment requires further discussion. {na}: {ap}. {nb}: {bp}."

    # ── Asset/Debt formatters ──────────────────────────────────────────────
    def fmt_assets(lst, owner_name):
        if not lst:
            return f"  No premarital assets disclosed by {owner_name}."
        lines = []
        for a in lst:
            desc = a.get('description','').strip() or '[description not provided]'
            val  = money(a.get('value', 0))
            lines.append(
                f"  • {a.get('asset_type','Asset')}: {desc} "
                f"| Location: {a.get('location','') or '[not specified]'} "
                f"| Est. Value: {val} "
                f"| Preference: {a.get('preference','Separate property')}")
        return "\n".join(lines)

    def fmt_debts(lst, owner_name):
        if not lst:
            return f"  No premarital debts disclosed by {owner_name}."
        lines = []
        for d in lst:
            desc = d.get('description','').strip() or '[description not provided]'
            bal  = money(d.get('balance', 0))
            lines.append(
                f"  • {d.get('debt_type','Debt')}: {desc} "
                f"| Balance: {bal} "
                f"| Responsibility: {d.get('preference','Owner remains responsible')}")
        return "\n".join(lines)

    # ── Preference status (Schedule C) ────────────────────────────────────
    def pref_status(key):
        av, bv = ga.get(key,''), gb.get(key,'')
        if not av or not bv:                              return "Pending"
        if av == bv and 'Discuss' not in av:              return "Agreed"
        if 'Discuss' in av or 'Discuss' in bv:            return "Attorney Review Required"
        return "Conflict — Attorney Review Required"

    # ── Attorney review flags (Schedule D) ───────────────────────────────
    flags = []
    for c in conflicts:
        flags.append(
            f"Preference conflict — {c['Topic']}: {na} prefers '{c['Partner A']}'; "
            f"{nb} prefers '{c['Partner B']}' (Severity: {c['Severity']})")
    for goals, pname in [(ga, na), (gb, nb)]:
        for key, label in [('premarital_assets','Premarital Assets'),
                           ('future_income','Future Income'),
                           ('business_growth','Business Growth'),
                           ('spousal_support','Spousal Support')]:
            if 'Discuss' in goals.get(key,'') or 'attorney' in goals.get(key,'').lower():
                flag = f"{pname} requested attorney review for: {label}"
                if flag not in flags:
                    flags.append(flag)
    if case.get('cross_border'):
        flags.append(f"Cross-border assets or multiple jurisdictions identified ({jur}) — international counsel recommended")
    for has_biz, pname in [(pa.get('owns_business'), na), (pb.get('owns_business'), nb)]:
        if has_biz:
            flags.append(f"{pname} owns a business interest — professional valuation and attorney review required")
    if pa.get('has_children_prior') or pb.get('has_children_prior'):
        flags.append("One or both Parties have children from prior relationships — estate planning and support provisions should be reviewed with counsel")
    if not flags:
        flags.append("No major conflicts detected. Standard attorney review still recommended before execution.")
    flags_text = "\n".join(f"  {i+1}. {f}" for i, f in enumerate(flags))

    # ── Document checklist (Schedule E) ──────────────────────────────────
    uploaded_types = {d["type"] for d in st.session_state.uploaded_docs}
    def chk(doc_type):
        return "[x]" if doc_type in uploaded_types else "[ ]"
    cross_border_doc_line = (
        "[x] Cross-border asset documentation" if case.get("cross_border")
        else "[ ] Cross-border asset documentation (if applicable)")

    # ── Schedule C rows ───────────────────────────────────────────────────
    pref_keys = [
        ('premarital_assets',   'Premarital Assets'),
        ('future_income',       'Future Income'),
        ('business_growth',     'Business Growth'),
        ('debt_responsibility', 'Debt Responsibility'),
        ('spousal_support',     'Spousal Support'),
        ('inheritance',         'Inheritance / Gifts'),
        ('home_purchase',       'Future Home Purchase'),
    ]
    sched_c = "\n\n".join(
        f"  {label}:\n"
        f"    {na}: {ga.get(key,'—')}\n"
        f"    {nb}: {gb.get(key,'—')}\n"
        f"    Status: {pref_status(key)}"
        for key, label in pref_keys)

    # ── Pre-computed conditionals (avoids quote nesting in f-string) ──────
    cross_disclosure = (
        "This disclosure is further complicated by cross-border holdings. "
        "The Parties should obtain internationally competent counsel." if case.get("cross_border")
        else "All disclosed assets and debts are domestic.")
    re_a_line = f"  {na}: Owns real property — deed and mortgage details to be attached before execution." if pa.get("owns_real_estate") else f"  {na}: No premarital real estate disclosed."
    re_b_line = f"  {nb}: Owns real property — deed and mortgage details to be attached before execution." if pb.get("owns_real_estate") else f"  {nb}: No premarital real estate disclosed."
    biz_a_line = "Owns business or equity interest — formal disclosure and valuation to be completed with independent counsel." if pa.get("owns_business") else "No business interests disclosed."
    biz_b_line = "Owns business or equity interest — formal disclosure and valuation to be completed with independent counsel." if pb.get("owns_business") else "No business interests disclosed."
    biz_disclosed = (
        f"{na} and/or {nb} hold a business ownership or equity interest as disclosed in the Schedules."
        if pa.get("owns_business") or pb.get("owns_business")
        else "Neither Party has disclosed ownership of a business interest at the time of this draft.")
    family_support_line = (
        "One or both Parties have disclosed ongoing financial obligations to family members. "
        "Such obligations shall remain the separate responsibility of the Party who undertakes them unless otherwise agreed."
        if pa.get("supports_family") or pb.get("supports_family")
        else "Neither Party has disclosed ongoing family financial support obligations at the time of this draft.")
    children_line = (
        "One or both Parties have children from a prior relationship. "
        "Existing legal obligations to those children are not modified by this Agreement."
        if pa.get("has_children_prior") or pb.get("has_children_prior")
        else "Neither Party has disclosed children from a prior relationship at the time of this draft.")
    cross_border_jur_note = (
        f" This Agreement may implicate the laws of multiple jurisdictions given the Parties' "
        f"disclosed cross-border assets or residency ({jur}). International counsel is strongly recommended."
        if case.get("cross_border") else "")
    imm_note = (
        f"{na} — {pa.get('immigration_status','')}; {nb} — {pb.get('immigration_status','')}. "
        f"Immigration and residency statuses are noted. This Agreement does not modify obligations imposed by immigration law.")
    missing_suffix  = "y" if len(missing_docs) == 1 else "ies"
    next_step_rec   = (
        f"Resolve {len(conflicts)} preference conflict(s) with counsel before execution."
        if conflicts
        else "Both Parties should review this draft with independent legal counsel before scheduling execution.")
    pa_fam_a = "Has disclosed ongoing financial support obligations to family members." if pa.get("supports_family") else "No ongoing family financial support obligations disclosed."
    pb_fam_b = "Has disclosed ongoing financial support obligations to family members." if pb.get("supports_family") else "No ongoing family financial support obligations disclosed."
    pa_kids  = "Has children from a prior relationship. Existing legal obligations are not modified by this Agreement." if pa.get("has_children_prior") else "None disclosed."
    pb_kids  = "Has children from a prior relationship. Existing legal obligations are not modified by this Agreement." if pb.get("has_children_prior") else "None disclosed."

    # ─────────────────────────────────────────────────────────────────────
    # DOCUMENT
    # ─────────────────────────────────────────────────────────────────────
    draft = f"""PREMARITAL AGREEMENT — PREPARATION DRAFT

IMPORTANT NOTICE: This document is a template-generated draft based on questionnaire responses. It is intended for preparation and attorney review only. It should not be signed, relied upon, or treated as final until each Party has had adequate opportunity to review, disclose financial information, ask questions, and consult independent legal counsel.


PREMARITAL AGREEMENT

This Premarital Agreement ("Agreement") is made and entered into on this ___ day of ________, 20__, by and between:

{na}, a {pa.get('citizenship','')} national, residency status: {pa.get('immigration_status','')}, currently residing in {case.get('current_residence','')}, referred to in this Agreement as "Partner A,"

and

{nb}, a {pb.get('citizenship','')} national, residency status: {pb.get('immigration_status','')}, currently residing in {case.get('current_residence','')}, referred to in this Agreement as "Partner B."

Partner A and Partner B may be referred to individually as a "Party" and collectively as the "Parties."


1. RECITALS

1.1  Intent to Marry. The Parties intend to marry on or about {wdate} in {loc}.

1.2  Purpose. The Parties desire to define their respective rights and obligations regarding property, income, debts, business interests, inheritance, gifts, spousal support, and other financial matters before marriage. This Agreement reflects a theme of: "{theme}." {na} reports an approximate annual income of {money(pa.get('income',0))} and {nb} reports an approximate annual income of {money(pb.get('income',0))}.

1.3  Effective Date. This Agreement shall become effective only upon the legal marriage of the Parties.

1.4  Voluntary Agreement. Each Party enters into this Agreement voluntarily, freely, and without fraud, duress, coercion, or undue influence.

1.5  Opportunity for Legal Counsel.
     [ ] The Party has obtained independent legal counsel.
     [ ] The Party has had adequate opportunity to obtain counsel and voluntarily chooses to proceed.
     [ ] The Party requires attorney review before execution.

1.6  Financial Disclosure. Each Party acknowledges that they have provided a fair and reasonable disclosure of their assets, debts, income, and financial obligations. Disclosures are attached as Schedule A ({na}) and Schedule B ({nb}).

1.7  Adequate Time for Review. Each Party acknowledges receipt of this Agreement with sufficient time before the wedding date to review, ask questions, and consult counsel.

1.8  No Reliance on Oral Promises. Neither Party is relying on oral promises or representations not included in this Agreement.


2. DEFINITIONS

2.1  Separate Property: Property belonging solely to one Party, not subject to division upon separation, divorce, annulment, or death, except as otherwise provided herein.

2.2  Marital Property: Property the Parties agree will be jointly owned, shared, or subject to division upon separation, divorce, annulment, or death.

2.3  Premarital Property: Property owned by either Party before the marriage.

2.4  Income: Wages, salary, bonuses, commissions, dividends, distributions, business income, rental income, interest, capital gains, royalties, and other earnings.

2.5  Appreciation: Any increase in value of property, whether caused by market forces, reinvestment, labour, active management, business growth, or improvements.

2.6  Debt: Any financial obligation, including credit card debt, student loans, personal loans, mortgages, tax liabilities, and other obligations.

2.7  Business Interest: Any ownership, equity, membership, partnership, stock, options, restricted stock units, profit-sharing rights, or other economic interest in a business or professional entity.

2.8  Cross-Border Asset: Any asset, debt, business interest, real estate, inheritance interest, or financial account located outside the primary jurisdiction where the Parties reside.


3. DISCLOSURE OF ASSETS, DEBTS, AND INCOME

3.1  {na}'s assets, debts, income, business interests, and financial obligations are disclosed in Schedule A.

3.2  {nb}'s assets, debts, income, business interests, and financial obligations are disclosed in Schedule B.

3.3  Each Party represents that their disclosure is true, accurate, and complete to the best of their knowledge. {cross_disclosure}

3.4  No Hidden Assets: Each Party represents that they have not intentionally concealed any material asset, debt, income source, business interest, or financial obligation.

3.5  If either Party discovers a material omission before signing, that Party shall update their disclosure before execution.


4. SEPARATE PROPERTY — PREMARITAL ASSETS

4.1  Premarital Asset Treatment.
     {sep_prop_clause()}

4.2  All assets listed as Separate Property in Schedule A shall remain {na}'s Separate Property. All assets listed as Separate Property in Schedule B shall remain {nb}'s Separate Property.

{na}'s Disclosed Premarital Assets:
{fmt_assets(st.session_state.assets_a, na)}

{nb}'s Disclosed Premarital Assets:
{fmt_assets(st.session_state.assets_b, nb)}

4.3  If Separate Property is sold, exchanged, or converted into another asset, the resulting asset shall remain Separate Property, provided it can be traced.

4.4  Commingling: The Parties agree to use reasonable efforts to keep Separate Property separate. Deposit into joint accounts may create tracing issues and should be addressed in writing.

4.5  Tracing: A Party claiming that an asset remains Separate Property shall maintain records sufficient to trace the asset to its separate source.


5. MARITAL PROPERTY

5.1  Marital Property shall include property the Parties intentionally acquire jointly during the marriage or expressly designate as shared in writing.

5.2  Funds deposited into jointly titled bank or investment accounts shall be presumed to be Marital Property unless records clearly show otherwise.

5.3  The Parties may modify the classification of property during the marriage by written agreement signed by both Parties.


6. INCOME DURING MARRIAGE

6.1  Treatment of Earned Income.
     {income_clause()}

6.2  Bonuses, stock options, RSUs, and equity compensation shall be classified based on when they were earned, granted, or vested, subject to attorney review.

6.3  Tax refunds and liabilities shall be allocated based on source of income, filing status, and the Parties' agreement, subject to applicable law.


7. DEBTS AND LIABILITIES

7.1  Premarital debts incurred by a Party before the marriage shall remain that Party's separate responsibility, consistent with the preferences stated below.

{na}'s Disclosed Premarital Debts:
{fmt_debts(st.session_state.debts_a, na)}
     {na}'s debt responsibility preference: {_p(ga,'debt_responsibility')}.

{nb}'s Disclosed Premarital Debts:
{fmt_debts(st.session_state.debts_b, nb)}
     {nb}'s debt responsibility preference: {_p(gb,'debt_responsibility')}.

7.2  Neither Party shall incur debt in the other Party's name without express written consent.

7.3  Any joint debt incurred after the date of marriage shall be subject to shared responsibility unless the Parties agree otherwise in writing.


8. REAL ESTATE

8.1  Real estate owned by a Party before marriage shall remain that Party's Separate Property unless transferred into joint title or otherwise agreed in writing.
{re_a_line}
{re_b_line}

8.2  Mortgage payments from marital funds toward one Party's Separate Property may create reimbursement rights; the Parties should specify in writing whether such payments establish a marital interest or remain non-reimbursable.

8.3  Future Home Purchase.
     {home_clause()}

8.4  Certain jurisdictions may have special rules governing a marital residence that may limit or override provisions of this Agreement.

8.5  Any real estate located outside {jur} shall be disclosed separately and reviewed by counsel familiar with the law of that location.


9. BUSINESS INTERESTS

9.1  Business Interests Disclosed.
     {biz_disclosed}
     {na}: {biz_a_line}
     {nb}: {biz_b_line}

9.2  Business Interest Appreciation.
     {biz_clause()}

9.3  No Management Rights. This Agreement does not grant either Party management rights, voting rights, or employment rights in the other Party's business unless otherwise agreed in writing.

9.4  Future Business Interests. Business interests created during marriage shall be classified based on source of funds, labour contribution, ownership documents, and the Parties' written agreement.

9.5  If a business must be valued, the Parties may use a neutral valuation professional or another method agreed in writing.


10. RETIREMENT ACCOUNTS AND INVESTMENTS

10.1  Premarital Retirement Accounts: Retirement accounts owned before marriage shall remain the Separate Property of the owning Party, including premarital balances and traceable premarital growth.

10.2  Contributions During Marriage: Retirement contributions and their classification shall be addressed with independent counsel, as treatment varies significantly by jurisdiction.

10.3  Investment Accounts: Shall be classified based on title, source of funds, and tracing records.

10.4  Stock Options and RSUs: Shall be reviewed based on grant date, vesting date, purpose of award, and applicable law.


11. INHERITANCE, GIFTS, TRUSTS, AND FAMILY PROPERTY

11.1  Inheritance and Gifts.
      {inheritance_clause()}

11.2  Family land, ancestral property, family businesses, expected inheritance, or beneficial interests in family trusts shall remain Separate Property unless expressly transferred or shared in writing.

11.3  Trust Interests: Any trust interest, whether vested, contingent, or discretionary, shall remain the Separate Property of the beneficiary Party unless applicable law provides otherwise.

11.4  If a Party uses inheritance or family gifts toward a joint home, joint account, or shared investment, the Parties should document whether the contribution is a gift, loan, or reimbursement right.

11.5  Family Support Obligations.
      {family_support_line}


12. SPOUSAL SUPPORT

12.1  {spousal_clause()}

12.2  Career Pause or Caregiving: If one Party pauses or reduces employment to care for children, support the household, or relocate for the other Party's career, the Parties should review whether the spousal support provision remains fair and enforceable.

12.3  No provision of this Agreement shall be interpreted to require enforcement of a spousal support waiver if doing so would violate applicable law or public policy.


13. CHILDREN

13.1  Child Support Not Waived: This Agreement does not waive, limit, or predetermine child support. Child support shall be determined according to applicable law and the best interests of the child.

13.2  Child Custody: This Agreement does not make binding decisions regarding custody, decision-making responsibility, or parenting time. Such matters shall be determined according to applicable law.

13.3  {children_line}


14. ESTATE RIGHTS AND DEATH

14.1  Estate rights, including elective share and surviving spouse claims, shall be addressed with independent estate planning counsel before execution.

14.2  Beneficiary Designations: This Agreement does not automatically change beneficiary designations for life insurance, retirement accounts, bank accounts, or transfer-on-death assets. Each Party is responsible for updating their own designations.

14.3  The Parties may execute wills, trusts, powers of attorney, and healthcare directives consistent with this Agreement.


15. TAXES

15.1  The Parties may file tax returns jointly or separately as permitted by law and as they mutually determine each tax year.

15.2  Each Party shall be responsible for tax liabilities arising from their separate income or premarital tax obligations unless otherwise agreed.

15.3  Indemnification: A Party whose separate income, property, or business creates tax liability shall indemnify the other Party to the extent permitted by law.


16. CROSS-BORDER, IMMIGRATION, AND MULTI-JURISDICTION ISSUES

16.1  Jurisdictions Identified: {jur}.

16.2  Cross-Border Assets: Assets located outside the primary jurisdiction may require review by counsel familiar with the laws of that jurisdiction.{cross_border_jur_note}

16.3  Immigration and Residency: {imm_note}

16.4  Future Relocation: If the Parties relocate to another state, province, or country, they should review this Agreement with counsel to determine whether amendment is appropriate.


17. HOUSEHOLD EXPENSES AND JOINT FINANCES

17.1  Each Party may maintain separate bank, investment, and credit accounts. Nothing in this Agreement requires either Party to merge finances, retitle property, or assume the other Party's debts.

17.2  The Parties may agree to contribute to shared household expenses equally, proportionally by income, or by separate arrangement. Joint account contributions shall be used for joint purposes unless otherwise agreed.


18. DISPUTE RESOLUTION

18.1  If a dispute arises, the Parties shall first attempt to resolve it through good-faith discussion.

18.2  Before filing litigation, the Parties may attempt mediation with a qualified family-law mediator, unless emergency relief is needed.

18.3  Any unresolved dispute shall be handled in a court with proper jurisdiction in {loc}.

18.4  Nothing in this Agreement prevents either Party from seeking emergency legal relief where necessary.


19. REPRESENTATIONS AND WARRANTIES

Each Party represents and warrants that:
  • They have read this Agreement fully and understand its nature and effect.
  • They have had the opportunity to ask questions and consult independent legal counsel.
  • They are signing voluntarily, without duress, coercion, or undue influence.
  • They have provided financial disclosure to the best of their knowledge.
  • They are not relying on promises outside this Agreement.
  • They understand that certain provisions may be limited by applicable law or public policy.


20. AMENDMENT, REVOCATION, AND REVIEW

20.1  Amendment: This Agreement may be amended only by a written document signed by both Parties.

20.2  Revocation: This Agreement may be revoked only by a written document signed by both Parties.

20.3  Periodic Review: The Parties may review this Agreement after major life events, including birth of a child, relocation, business sale, inheritance, major asset purchase, or significant income change.


21. SEVERABILITY

If any provision of this Agreement is found invalid or unenforceable, the remaining provisions shall remain in effect to the fullest extent permitted by law.


22. GOVERNING LAW

22.1  This Agreement shall be governed by the laws of {jur}, unless a court determines that another law applies.

22.2  This governing-law provision may not control the treatment of real estate, family law rights, estate rights, or support obligations in another jurisdiction.


23. ENTIRE AGREEMENT

This Agreement, including all Schedules, constitutes the entire agreement between the Parties regarding the matters addressed herein. It supersedes all prior oral or written discussions and understandings.


24. INDEPENDENT COUNSEL ACKNOWLEDGMENT AND EXECUTION

Both Parties acknowledge this preparation draft has been generated by KnotWise for the purpose of organising financial disclosures and identifying key discussion points prior to attorney engagement. Each Party is strongly advised to retain independent legal counsel before executing any final agreement. This document does not constitute legal advice. KnotWise is not a law firm.

This Agreement may be signed in counterparts, each of which shall be considered an original. Electronic signatures may be accepted if permitted by applicable law. The Parties may sign before a notary public and/or witnesses as required by applicable law.


SIGNATURES

IN WITNESS WHEREOF, the Parties have executed this Premarital Agreement on the dates set forth below.

Partner A:
Signature:     _______________________________
Printed Name:  {na}
Date:          ___________________

Partner B:
Signature:     _______________________________
Printed Name:  {nb}
Date:          ___________________


NOTARY ACKNOWLEDGMENT

State/Province of ____________________
County/Region of ____________________

On this ___ day of ________, 20__, before me personally appeared {na} and {nb}, known to me or proven through satisfactory evidence to be the persons subscribed to this Agreement, and acknowledged that they executed the same voluntarily.

Notary Public: _______________________________
My Commission Expires: ______________________


CERTIFICATE OF INDEPENDENT LEGAL ADVICE — PARTNER A

I, _______________________________, a licensed attorney, certify that I have reviewed this Agreement with {na}, explained its nature and effect, discussed rights and obligations affected, and answered questions presented by the client.

Attorney Name: _______________________________
Bar Number: _______________________________
Signature: _______________________________
Date: ___________________


CERTIFICATE OF INDEPENDENT LEGAL ADVICE — PARTNER B

I, _______________________________, a licensed attorney, certify that I have reviewed this Agreement with {nb}, explained its nature and effect, discussed rights and obligations affected, and answered questions presented by the client.

Attorney Name: _______________________________
Bar Number: _______________________________
Signature: _______________________________
Date: ___________________


SCHEDULE A — PARTNER A FINANCIAL DISCLOSURE

A.1  Personal Information
     Full Name:                 {na}
     Citizenship:               {pa.get('citizenship','')}
     Immigration/Residency:     {pa.get('immigration_status','')}
     Current Residence:         {case.get('current_residence','')}
     Approximate Annual Income: {money(pa.get('income',0))}

A.2  Disclosed Assets
{fmt_assets(st.session_state.assets_a, na)}

A.3  Disclosed Debts
{fmt_debts(st.session_state.debts_a, na)}

A.4  Business Interests
     {biz_a_line}

A.5  Real Estate
     {'Owns real property — deed and mortgage details to be attached before execution.' if pa.get('owns_real_estate') else 'No premarital real estate disclosed.'}

A.6  Family Financial Obligations
     {pa_fam_a}

A.7  Prior Relationship Children
     {pa_kids}


SCHEDULE B — PARTNER B FINANCIAL DISCLOSURE

B.1  Personal Information
     Full Name:                 {nb}
     Citizenship:               {pb.get('citizenship','')}
     Immigration/Residency:     {pb.get('immigration_status','')}
     Current Residence:         {case.get('current_residence','')}
     Approximate Annual Income: {money(pb.get('income',0))}

B.2  Disclosed Assets
{fmt_assets(st.session_state.assets_b, nb)}

B.3  Disclosed Debts
{fmt_debts(st.session_state.debts_b, nb)}

B.4  Business Interests
     {biz_b_line}

B.5  Real Estate
     {'Owns real property — deed and mortgage details to be attached before execution.' if pb.get('owns_real_estate') else 'No premarital real estate disclosed.'}

B.6  Family Financial Obligations
     {pb_fam_b}

B.7  Prior Relationship Children
     {pb_kids}


SCHEDULE C — SELECTED PRENUP PREFERENCES

{sched_c}


SCHEDULE D — ATTORNEY REVIEW FLAGS

The following items require attorney attention before execution:

{flags_text}


SCHEDULE E — DOCUMENT CHECKLIST

  {chk('Government ID')} Government identification — {na}
  {chk('Government ID')} Government identification — {nb}
  {chk('Bank/Investment Statements')} Recent bank and investment account statements
  {chk('Retirement Account Statements')} Retirement account statements
  {chk('Debt Statements')} Credit card, loan, and debt statements
  {chk('Real Estate Documents')} Real estate deeds or title records
  {chk('Business Ownership Documents')} Business formation and valuation documents
  [ ] Tax returns (last 2 years)
  [ ] Pay stubs or income verification
  [ ] Trust documents (if applicable)
  [ ] Inheritance documentation (if applicable)
  {cross_border_doc_line}


SCHEDULE F — READINESS SUMMARY

  Readiness Score:       {score}/100
  Risk Level:            {risk} — {risk_label}
  Detected Conflicts:    {len(conflicts)} preference conflict(s) identified
  Missing Documents:     {len(missing_docs)} document categor{missing_suffix} not yet uploaded
  Agreement Theme:       {theme}
  Draft Generated:       {now_str}
  Recommended Next Step: {next_step_rec}

  IMPORTANT DISCLAIMER: This document is a preparation draft generated by KnotWise, an academic demonstration prototype. It is not legal advice and does not constitute a valid prenuptial agreement. Both Parties must retain independent legal counsel before executing any final agreement. KnotWise is not a law firm and does not provide legal services."""

    return draft


# ── AI: Gemini call (cached) — falls back to local draft ─────────────────
def call_gemini():
    if st.session_state.ai_draft:
        return st.session_state.ai_draft, None
    try:
        import google.generativeai as genai
        key = st.secrets.get("knotwise_gemini_key", "")
        if key:
            genai.configure(api_key=key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(build_prenup_prompt())
            st.session_state.ai_draft = response.text
            save_state()
            return response.text, None
    except Exception:
        pass
    # Fallback: fill template locally — no API quota consumed
    draft = generate_draft_locally()
    st.session_state.ai_draft = draft
    save_state()
    return draft, None


# ── PDF builder ───────────────────────────────────────────────────────────
def build_pdf_bytes():
    from fpdf import FPDF

    LM = 15   # left margin mm
    RM = 15   # right margin mm
    TM = 15   # top margin mm
    CW = 180  # content width = 210 - LM - RM

    class KWDoc(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 7.5)
            self.set_text_color(138, 158, 88)
            self.set_x(LM)
            self.cell(CW, 7, "KNOTWISE  |  PRENUPTIAL AGREEMENT PREPARATION DRAFT", align="C",
                      new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(138, 158, 88)
            self.set_line_width(0.2)
            self.line(LM, self.get_y(), LM + CW, self.get_y())
            self.ln(4)

        def footer(self):
            self.set_y(-13)
            self.set_font("Helvetica", "I", 6.5)
            self.set_text_color(160, 160, 160)
            self.set_x(LM)
            self.cell(CW, 5,
                f"PREPARATION DRAFT — FOR ATTORNEY REVIEW ONLY  |  Page {self.page_no()}  |  KnotWise Academic Prototype",
                align="C")

    pdf = KWDoc(orientation="P", unit="mm", format="A4")
    pdf.set_margins(left=LM, top=TM, right=RM)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    case  = st.session_state.case
    pa, pb = st.session_state.partner_a, st.session_state.partner_b
    sa, sb = st.session_state.signoff_a, st.session_state.signoff_b
    draft  = st.session_state.ai_draft or ""
    theme  = detect_theme()
    HW    = CW // 2  # half-width column = 90mm

    def mc(txt, h=5.5, bold=False, size=9.5, color=(25,25,25)):
        """Safe multi_cell that always starts at left margin."""
        pdf.set_x(LM)
        pdf.set_font("Helvetica", "B" if bold else "", size)
        pdf.set_text_color(*color)
        pdf.multi_cell(CW, h, pdf_safe(str(txt)))

    # ── Title block ───────────────────────────────────────────────────────
    pdf.set_x(LM)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(CW, 11, "PREMARITAL AGREEMENT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(LM)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(CW, 5, "Preparation Draft for Attorney Review  |  Not a Final Legal Document",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # ── Info box (two-column rows, explicit half-widths) ──────────────────
    pdf.set_fill_color(250, 250, 248)
    pdf.set_draw_color(180, 195, 150)
    pdf.set_line_width(0.3)
    box_y = pdf.get_y()
    pdf.rect(LM, box_y, CW, 28, style="FD")

    def box_row(label_a, val_a, label_b, val_b, row_y):
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(70, 70, 70)
        pdf.set_xy(LM + 3, row_y)
        pdf.cell(HW - 3, 5, pdf_safe(f"{label_a}: {val_a}"), border=0)
        pdf.set_xy(LM + HW + 3, row_y)
        pdf.cell(HW - 3, 5, pdf_safe(f"{label_b}: {val_b}"), border=0)

    box_row("Couple",    case.get("case_name",""),
            "Wedding",   case.get("wedding_date",""),    row_y=box_y + 4)
    box_row("Residence", case.get("future_residence",""),
            "Jurisdiction", case.get("jurisdictions",""), row_y=box_y + 11)

    pdf.set_xy(LM + 3, box_y + 18)
    pdf.set_font("Helvetica", "I", 7.5)
    pdf.set_text_color(120, 145, 70)
    pdf.cell(CW - 6, 5, pdf_safe(f"Agreement Theme: {theme}"), border=0)

    # Reset cursor below the box
    pdf.set_xy(LM, box_y + 28)
    pdf.ln(6)

    # ── Draft content ─────────────────────────────────────────────────────
    for raw_line in draft.split('\n'):
        line = pdf_safe(raw_line.strip())
        if not line:
            pdf.set_x(LM)
            pdf.ln(2.5)
            continue

        # Detect section headers:
        # "1. RECITALS", "22. GOVERNING LAW" — digit(s), ". ", rest
        # or ALL-CAPS short lines like "SIGNATURES", "SCHEDULE A —..."
        starts_numbered = (len(line) > 3 and line[0].isdigit()
                           and '. ' in line[:line.find(' ')+2 if ' ' in line else 4])
        is_all_caps    = (line.isupper() and 4 < len(line) < 90)
        is_schedule    = line.startswith("SCHEDULE ")

        if starts_numbered or is_all_caps or is_schedule:
            pdf.ln(2)
            pdf.set_x(LM)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(120, 145, 70)
            pdf.multi_cell(CW, 6, line)
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(25, 25, 25)
            pdf.set_x(LM)
            pdf.ln(1)
        else:
            pdf.set_x(LM)
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(25, 25, 25)
            pdf.multi_cell(CW, 5.5, line)

    # ── Sign-off page ─────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_x(LM)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(CW, 10, "ACKNOWLEDGMENT & SIGN-OFF", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(138, 158, 88)
    pdf.set_line_width(0.4)
    pdf.line(LM, pdf.get_y(), LM + CW, pdf.get_y())
    pdf.ln(6)

    pdf.set_x(LM)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(CW, 5.5, pdf_safe(
        "Both parties confirm they have reviewed this preparation draft, understand it is not a "
        "final legal agreement, and acknowledge it requires independent attorney review before execution."))
    pdf.ln(8)

    # Two signature columns (fixed absolute positions, cell width = 80)
    COL_W = 80
    y = pdf.get_y()
    for x_off, plabel, pdata, sdata in [
        (LM,          "PARTNER A", pa, sa),
        (LM + COL_W + 10, "PARTNER B", pb, sb),
    ]:
        pdf.set_xy(x_off, y)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(120, 145, 70)
        pdf.cell(COL_W, 6, plabel, border=0)

        pdf.set_xy(x_off, y + 8)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(COL_W, 5.5, pdf_safe(f"Name: {sdata.get('name', pdata.get('name',''))}"), border=0)

        pdf.set_xy(x_off, y + 14)
        pdf.cell(COL_W, 5.5,
                 pdf_safe(f"Acknowledged: {'Yes' if sdata.get('agreed') else 'Pending'}"), border=0)

        pdf.set_xy(x_off, y + 20)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(COL_W, 5.5,
                 pdf_safe(f"Date & Time: {sdata.get('timestamp', 'Not recorded')}"), border=0)

    sig_y = y + 38
    pdf.set_draw_color(200, 200, 200)
    pdf.set_line_width(0.3)
    pdf.line(LM,               sig_y, LM + COL_W,               sig_y)
    pdf.line(LM + COL_W + 10,  sig_y, LM + COL_W + 10 + COL_W, sig_y)
    pdf.set_y(sig_y + 2)
    pdf.set_font("Helvetica", "I", 7.5)
    pdf.set_text_color(150, 150, 150)
    pdf.set_x(LM)
    pdf.cell(COL_W, 5, pdf_safe(f"Signature — {pa.get('name','Partner A')}"), border=0)
    pdf.set_x(LM + COL_W + 10)
    pdf.cell(COL_W, 5, pdf_safe(f"Signature — {pb.get('name','Partner B')}"), border=0)
    pdf.ln(16)

    # Disclaimer
    pdf.set_x(LM)
    pdf.set_fill_color(252, 252, 250)
    pdf.set_draw_color(180, 195, 150)
    pdf.set_line_width(0.2)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(140, 130, 100)
    pdf.multi_cell(CW, 4.2, pdf_safe(
        f"IMPORTANT DISCLAIMER: This document is a preparation draft generated by KnotWise, an academic "
        f"demonstration prototype. It is not legal advice and does not constitute a valid prenuptial agreement. "
        f"Both parties must retain independent legal counsel before executing any final agreement. "
        f"KnotWise is not a law firm and does not provide legal services. "
        f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"),
        fill=True)

    return bytes(pdf.output())


# ── Email sender ──────────────────────────────────────────────────────────
def send_email_pdf(pdf_bytes, recipients):
    try:
        sender   = st.secrets.get("sender_email", "")
        password = st.secrets.get("sender_password", "")
    except Exception:
        sender, password = "", ""
    if not sender or not password:
        return False, "Email not configured. Add `sender_email` and `sender_password` to Streamlit secrets."

    case = st.session_state.case
    pa, pb = st.session_state.partner_a, st.session_state.partner_b
    msg = MIMEMultipart()
    msg["From"]    = sender
    msg["To"]      = ", ".join(recipients)
    msg["Subject"] = f"KnotWise — Prenup Preparation Draft: {case.get('case_name','')}"

    body = (f"Dear {pa.get('name','Partner A')} and {pb.get('name','Partner B')},\n\n"
            f"Please find attached your KnotWise prenuptial agreement preparation draft.\n\n"
            f"IMPORTANT: This is a preparation draft only and is not a final legal agreement. "
            f"Please review with your respective attorneys before proceeding.\n\n"
            f"Generated by KnotWise on {datetime.now().strftime('%B %d, %Y')}.\n\n"
            f"This email was sent automatically by KnotWise — Academic Prototype. Not legal advice.")
    msg.attach(MIMEText(body, "plain"))

    part = MIMEBase("application", "octet-stream")
    part.set_payload(pdf_bytes)
    encoders.encode_base64(part)
    fname = f"knotwise_prenup_{case.get('case_name','draft').replace(' ','_')}.pdf"
    part.add_header("Content-Disposition", f"attachment; filename={fname}")
    msg.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as srv:
            srv.login(sender, password)
            srv.sendmail(sender, recipients, msg.as_string())
        return True, "Email sent successfully to both partners."
    except Exception as e:
        return False, str(e)


# ── Partner form ──────────────────────────────────────────────────────────
def partner_form(label, state_key, next_page=None):
    existing = st.session_state[state_key]
    with st.form(f"{state_key}_form"):
        c1, c2 = st.columns(2)
        with c1:
            name        = st.text_input(f"{label} Name",  value=existing.get("name",""))
            citizenship = st.text_input("Citizenship",    value=existing.get("citizenship",""))
            income      = st.number_input("Approximate Annual Income ($)", min_value=0.0, step=1000.0, value=float(existing.get("income",0.0)))
        with c2:
            email  = st.text_input(f"{label} Email", value=existing.get("email",""))
            statuses = ["U.S. Citizen","Green Card / Permanent Resident","F-1","H-1B","L-1","Canadian PR","Other","Prefer not to say"]
            es = existing.get("immigration_status","")
            immigration_status = st.selectbox("Immigration / Residency Status", statuses, index=statuses.index(es) if es in statuses else 0)
            notes = st.text_area("Additional Notes", value=existing.get("notes",""), height=82)
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            owns_business    = st.checkbox("Owns a business or equity interest", value=existing.get("owns_business",False))
            owns_real_estate = st.checkbox("Owns real estate", value=existing.get("owns_real_estate",False))
        with c2:
            has_children_prior = st.checkbox("Has children from prior relationship", value=existing.get("has_children_prior",False))
            supports_family    = st.checkbox("Financially supports family members", value=existing.get("supports_family",False))
        st.markdown("---")
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.2em;text-transform:uppercase;color:#8A9E58;margin-bottom:0.8rem">Prenup Preferences</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            premarital_assets   = st.selectbox("Premarital assets",          ["Keep separate","Share after marriage","Discuss with attorney"], key=f"{state_key}_pre")
            future_income       = st.selectbox("Future income during marriage",["Shared marital property","Separate property","Discuss with attorney"], key=f"{state_key}_inc")
            business_growth     = st.selectbox("Business growth / appreciation",["Keep separate","Share appreciation","Discuss with attorney"], key=f"{state_key}_biz")
            debt_responsibility = st.selectbox("Premarital debts",             ["Each partner responsible for own debts","Shared responsibility","Discuss with attorney"], key=f"{state_key}_dbt")
        with c2:
            spousal_support = st.selectbox("Spousal support",            ["Waived","Limited","Reserved for future review","Discuss with attorney"], key=f"{state_key}_sp")
            inheritance     = st.selectbox("Inheritance and family gifts",["Keep separate","Share if used by couple","Discuss with attorney"], key=f"{state_key}_inh")
            home_purchase   = st.selectbox("Future home purchase",        ["Shared property","Based on contribution","Discuss with attorney"], key=f"{state_key}_hm")
        sb1, sb2 = st.columns(2)
        with sb1:
            submitted  = st.form_submit_button(f"Save {label} Questionnaire", use_container_width=True)
        with sb2:
            save_next = st.form_submit_button("Save & Continue →", use_container_width=True)

    if submitted or save_next:
        st.session_state[state_key] = {"name":name,"email":email,"citizenship":citizenship,"immigration_status":immigration_status,"income":income,"owns_business":owns_business,"owns_real_estate":owns_real_estate,"has_children_prior":has_children_prior,"supports_family":supports_family,"notes":notes}
        goal_key = "goals_a" if state_key == "partner_a" else "goals_b"
        st.session_state[goal_key] = {"premarital_assets":premarital_assets,"future_income":future_income,"business_growth":business_growth,"debt_responsibility":debt_responsibility,"spousal_support":spousal_support,"inheritance":inheritance,"home_purchase":home_purchase}
        save_state()
        if save_next and next_page:
            go(next_page)
        else:
            st.success(f"{label} questionnaire saved.")


# ── Render ─────────────────────────────────────────────────────────────────
render_sidebar()
render_nav()
page = st.session_state.page


# 1. WELCOME ──────────────────────────────────────────────────────────────
if page == "welcome":
    hero_full("NYC-WEDDING-PHOTOGRAPHER-1024x683.jpg", height="420px", pos="center 40%")
    eyebrow("AI Prenup Preparation")
    st.title("KnotWise")
    gold_rule()
    c1, c2 = st.columns([3, 2], gap="large")
    with c1:
        st.markdown("KnotWise helps couples complete structured prenup questionnaires, organize financial disclosures, compare partner preferences, identify conflicts, and generate an attorney-ready AI preparation draft.")
        st.markdown("---")
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.18em;text-transform:uppercase;color:#555;margin-bottom:0.6rem">End-to-end workflow</p>', unsafe_allow_html=True)
        for item in ["Couple case creation and partner invitation","Partner A & B questionnaires with financial disclosures","Asset and debt disclosure with preference tracking","Automated conflict detection between partner responses","Prenup readiness score with explainable breakdown","Gemini AI fills a structured prenup template — one call, cached","Both partners sign off digitally","Final PDF generated and delivered by email or download"]:
            li(item)
    with c2:
        score, _ = completion_score()
        st.metric("Prototype Stack", "Streamlit + Gemini")
        st.metric("Primary Value", "Lower legal prep time")
        st.metric("User Flow", "2-partner intake")
        st.metric("Current Readiness", f"{score}/100")
    st.markdown('<p style="font-size:0.62rem;color:#1E1E1E;border-top:1px solid #111;padding-top:1rem;margin-top:2rem;letter-spacing:0.04em;line-height:1.8">Academic prototype. Not legal advice. Does not replace attorney review.</p>', unsafe_allow_html=True)


# 2. CASE SETUP ────────────────────────────────────────────────────────────
elif page == "setup":
    c_img, c_head = st.columns([2, 3], gap="large")
    with c_img:
        hero_col("7d9337fdbff13df38d6ccd18b2a9ec7b.jpg", height="480px", pos="center 50%")
    with c_head:
        eyebrow("Step 01 of 09")
        st.title("Case Setup")
        gold_rule()
        st.markdown("Establish the jurisdictional context and basic case information.")
        with st.form("case_setup_form"):
            c1, c2 = st.columns(2)
            with c1:
                case_name         = st.text_input("Case / Couple Name",                 value=st.session_state.case.get("case_name",""))
                current_residence = st.text_input("Current Residence",                  value=st.session_state.case.get("current_residence",""))
                jurisdictions     = st.text_input("Jurisdictions / Countries Involved",  value=st.session_state.case.get("jurisdictions",""))
            with c2:
                saved = st.session_state.case.get("wedding_date")
                dd = date.today()
                if isinstance(saved, str):
                    try: dd = datetime.strptime(saved, "%Y-%m-%d").date()
                    except: pass
                wedding_date     = st.date_input("Expected Wedding Date", value=dd)
                future_residence = st.text_input("Expected Residence After Marriage",    value=st.session_state.case.get("future_residence",""))
                cross_border     = st.checkbox("Involves cross-border assets or multiple countries", value=st.session_state.case.get("cross_border",False))
            sb1, sb2 = st.columns(2)
            with sb1:
                submitted  = st.form_submit_button("Save Case Setup", use_container_width=True)
            with sb2:
                save_next = st.form_submit_button("Save & Continue →", use_container_width=True)
        if submitted or save_next:
            st.session_state.case = {"case_name":case_name,"wedding_date":str(wedding_date),"current_residence":current_residence,"future_residence":future_residence,"jurisdictions":jurisdictions,"cross_border":cross_border}
            st.session_state.case_created = True
            st.session_state.ai_draft = None
            save_state()
            if save_next:
                go("partner")
            else:
                st.success("Case setup saved.")


# 3. ADD PARTNER ───────────────────────────────────────────────────────────
elif page == "partner":
    c_img, c_head = st.columns([1, 2], gap="large")
    with c_img:
        hero_col("images (1).jpeg", height="520px", pos="center 35%")
    with c_head:
        eyebrow("Step 02 of 09")
        st.title("Add Partner")
        gold_rule()
        st.markdown("Prepare a partner invitation for the prenup preparation workflow.")
        st.markdown("---")
        st.markdown('<p style="font-size:0.6rem;letter-spacing:0.16em;text-transform:uppercase;color:#555;margin-bottom:0.5rem">Partner Workflow</p>', unsafe_allow_html=True)
        for i, s in enumerate(["Partner A creates the case","Partner A invites Partner B","Partner B completes a separate questionnaire","Both responses are compared","Conflicts and missing information are flagged","Gemini AI generates the prenup draft","Both partners sign off","Final PDF is delivered"],1):
            st.markdown(f'<p style="color:#555;font-size:0.76rem;margin:0.2rem 0">{i}.&nbsp; {s}</p>', unsafe_allow_html=True)
        st.markdown("---")
        with st.form("partner_invite_form"):
            c1, c2 = st.columns(2)
            with c1:
                invite_email = st.text_input("Partner Email Address", value=st.session_state.invite_email)
                partner_name = st.text_input("Partner Name", value=st.session_state.partner_b.get("name",""))
            with c2:
                access_level = st.selectbox("Partner Access Level", ["Complete questionnaire only","View shared summary after both submit","Full shared case access"])
                message = st.text_area("Invitation Message", height=88, value="Hi, I invited you to complete your section of our prenup preparation questionnaire in KnotWise.")
            sb1, sb2 = st.columns(2)
            with sb1:
                sent      = st.form_submit_button("Save Invitation", use_container_width=True)
            with sb2:
                sent_next = st.form_submit_button("Save & Continue →", use_container_width=True)
        if sent or sent_next:
            st.session_state.partner_invited = True
            st.session_state.invite_email = invite_email
            if partner_name: st.session_state.partner_b["name"] = partner_name
            save_state()
            if sent_next:
                go("qa")
            else:
                st.success("Partner invitation prepared.")
                st.code(f"To: {invite_email}\nSubject: KnotWise prenup questionnaire invitation\n\n{message}\n\nAccess Level: {access_level}", language="text")


# 4. PARTNER A ─────────────────────────────────────────────────────────────
elif page == "qa":
    c_img, c_head = st.columns([1, 2], gap="large")
    with c_img:
        hero_col("106ae0c3ff0dd68d593c41d7bf297240.jpg", height="460px", pos="center 20%")
    with c_head:
        eyebrow("Step 03 of 09")
        st.title("Partner A Questionnaire")
        gold_rule()
        st.markdown("Complete your financial profile and prenup preference selections.")
    st.markdown("---")
    partner_form("Partner A", "partner_a", next_page="qb")


# 5. PARTNER B ─────────────────────────────────────────────────────────────
elif page == "qb":
    c_img, c_head = st.columns([1, 2], gap="large")
    with c_img:
        hero_col("_MG_4725 copy.jpg", height="460px", pos="center 40%")
    with c_head:
        eyebrow("Step 04 of 09")
        st.title("Partner B Questionnaire")
        gold_rule()
        if not st.session_state.partner_invited:
            st.warning("Partner has not been invited yet. Go to 'Invite' first.")
        else:
            st.markdown("Partner invitation prepared. Complete the questionnaire below.")
    st.markdown("---")
    partner_form("Partner B", "partner_b", next_page="assets")


# 6. ASSETS & DEBTS ────────────────────────────────────────────────────────
elif page == "assets":
    hero_full("img_7973.jpg", height="360px", pos="center 15%")
    eyebrow("Step 05 of 09")
    st.title("Assets, Debts & Documents")
    gold_rule()
    tab1, tab2, tab3 = st.tabs(["Add Asset","Add Debt","Upload Documents"])
    with tab1:
        with st.form("asset_form"):
            c1, c2 = st.columns(2)
            with c1:
                owner = st.selectbox("Owner", ["Partner A","Partner B"])
                asset_type = st.selectbox("Asset Type", ["Bank Account","Investment","Retirement Account","Real Estate","Business","Vehicle","Inheritance","Other"])
                description = st.text_input("Description")
            with c2:
                location  = st.text_input("Country / State", value="United States")
                value     = st.number_input("Estimated Value ($)", min_value=0.0, step=1000.0)
                preference = st.selectbox("Preferred Treatment", ["Separate property","Shared property","Attorney review needed"])
            sub = st.form_submit_button("Add Asset")
        if sub:
            a = {"asset_type":asset_type,"description":description,"location":location,"value":value,"preference":preference}
            (st.session_state.assets_a if owner=="Partner A" else st.session_state.assets_b).append(a)
            st.session_state.ai_draft = None; save_state(); st.success("Asset added.")
        df = build_asset_df()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.caption("No assets added yet.")

    with tab2:
        with st.form("debt_form"):
            c1, c2 = st.columns(2)
            with c1:
                owner = st.selectbox("Debt Owner", ["Partner A","Partner B"])
                debt_type = st.selectbox("Debt Type", ["Student Loan","Credit Card","Mortgage","Personal Loan","Business Debt","Vehicle Loan","Other"])
                description = st.text_input("Debt Description")
            with c2:
                balance   = st.number_input("Debt Balance ($)", min_value=0.0, step=500.0)
                preference = st.selectbox("Responsibility Preference", ["Owner remains responsible","Shared responsibility","Attorney review needed"])
            sub = st.form_submit_button("Add Debt")
        if sub:
            d = {"debt_type":debt_type,"description":description,"balance":balance,"preference":preference}
            (st.session_state.debts_a if owner=="Partner A" else st.session_state.debts_b).append(d)
            st.session_state.ai_draft = None; save_state(); st.success("Debt added.")
        df = build_debt_df()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.caption("No debts added yet.")

    with tab3:
        st.caption("Files are not permanently stored. Document type and filename are recorded for demonstration purposes.")
        with st.form("doc_form"):
            c1, c2 = st.columns(2)
            with c1:
                doc_type = st.selectbox("Document Type", ["Government ID","Bank/Investment Statements","Debt Statements","Real Estate Documents","Business Ownership Documents","Retirement Account Statements","Other"])
            with c2:
                uploaded_file = st.file_uploader("Upload document", type=["png","jpg","jpeg","pdf"])
            sub = st.form_submit_button("Add Document")
        if sub:
            if uploaded_file:
                st.session_state.uploaded_docs.append({"type":doc_type,"filename":uploaded_file.name,"size":uploaded_file.size})
                save_state()
                st.success("Document metadata saved.")
            else:
                st.error("Please upload a file first.")
        if st.session_state.uploaded_docs:
            st.dataframe(pd.DataFrame(st.session_state.uploaded_docs), use_container_width=True)

    st.markdown("---")
    st.markdown(
        '<div style="display:flex;justify-content:flex-end;margin-top:0.5rem">'
        '<span style="font-size:0.62rem;color:#555;letter-spacing:0.08em;align-self:center;margin-right:1.2rem">'
        'Add assets and debts above, then continue</span></div>', unsafe_allow_html=True)
    if st.button("Continue to Risk Dashboard →"):
        go("risk")


# 7. RISK DASHBOARD ────────────────────────────────────────────────────────
elif page == "risk":
    hero_full("black-white-shot-engaged-couple.jpg", height="360px", pos="center 15%")
    eyebrow("Step 06 of 09")
    st.title("Risk Dashboard")
    gold_rule()
    score, explanation = completion_score()
    risk, label = risk_level(score)
    conflicts = detect_conflicts()
    missing   = missing_documents()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Readiness Score", f"{score}/100")
    c2.metric("Risk Level", risk)
    c3.metric("Conflicts", len(conflicts))
    c4.metric("Missing Docs", len(missing))
    st.markdown(f'<p style="font-size:0.76rem;color:#8A9E58;letter-spacing:0.08em;margin:1rem 0 0.5rem 0">{label}</p>', unsafe_allow_html=True)
    st.progress(score / 100)
    st.markdown("---")
    cl, cr = st.columns(2, gap="large")
    with cl:
        with st.expander("Score Breakdown", expanded=True):
            for item in explanation:
                color = "#8A9E58" if "(+0)" not in item else "#333"
                st.markdown(f'<p style="color:{color};font-size:0.76rem;margin:0.22rem 0">— {item}</p>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<p style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#555;margin-bottom:0.5rem">Missing Documents</p>', unsafe_allow_html=True)
        for doc in missing: st.markdown(f'<p style="color:#333;font-size:0.76rem;margin:0.2rem 0">— {doc}</p>', unsafe_allow_html=True)
        if not missing: st.success("All major document categories present.")
    with cr:
        st.markdown('<p style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#555;margin-bottom:0.5rem">Partner Preference Conflicts</p>', unsafe_allow_html=True)
        if conflicts:
            st.dataframe(pd.DataFrame(conflicts), use_container_width=True)
        else:
            st.success("No major conflicts detected.")
    a_df, d_df = build_asset_df(), build_debt_df()
    if not a_df.empty or not d_df.empty:
        st.markdown("---")
        if not a_df.empty: st.caption("Assets"); st.dataframe(a_df, use_container_width=True)
        if not d_df.empty: st.caption("Debts");  st.dataframe(d_df, use_container_width=True)

    st.markdown("---")
    if st.button("Continue to AI Draft →"):
        go("draft")


# 8. AI DRAFT ──────────────────────────────────────────────────────────────
elif page == "draft":
    c_img, c_head = st.columns([1, 2], gap="large")
    with c_img:
        hero_col("images.jpeg", height="460px", pos="center 30%")
    with c_head:
        eyebrow("Step 07 of 09")
        st.title("AI Draft Generation")
        gold_rule()
        theme = detect_theme()
        st.markdown("All captured questionnaire data is merged into a structured prenup template. The draft is generated **once** and cached — it will not re-run unless you explicitly regenerate.")
        st.markdown(f'<p style="font-size:0.72rem;color:#8A9E58;margin-top:0.8rem">Detected theme: <strong>{theme}</strong></p>', unsafe_allow_html=True)

    st.markdown("---")

    if not ai_ready():
        missing_steps = []
        if not st.session_state.case_created: missing_steps.append("Case Setup")
        if not st.session_state.partner_a: missing_steps.append("Partner A Questionnaire")
        if not st.session_state.partner_b: missing_steps.append("Partner B Questionnaire")
        if not st.session_state.goals_a or not st.session_state.goals_b: missing_steps.append("Prenup Preferences (both partners)")
        st.markdown('<div class="kw-lock-box">', unsafe_allow_html=True)
        st.markdown('<p style="color:#555;font-size:0.8rem;margin-bottom:0.6rem">Complete the following steps before generating the draft:</p>', unsafe_allow_html=True)
        for s in missing_steps:
            st.markdown(f'<p style="color:#8A9E58;font-size:0.78rem;margin:0.2rem 0">— {s}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        if not st.session_state.ai_draft:
            st.markdown('<div class="kw-ai-box">', unsafe_allow_html=True)
            st.markdown('<p style="color:#999;font-size:0.82rem;margin-bottom:1rem">All required data is captured. Click below to generate the prenup preparation draft. The result is cached — no repeat processing on reload.</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("Generate Draft", use_container_width=False):
                with st.spinner("Building your prenup draft…"):
                    draft, err = call_gemini()
                if err:
                    st.error(f"Generation failed: {err}")
                else:
                    st.success("Draft generated and cached. Scroll down to review.")
                    st.rerun()
        else:
            st.success("Draft generated and cached. Edit below or proceed to Sign Off.")
            col_dl, col_regen = st.columns([3, 1])
            with col_regen:
                if st.button("↺ Regenerate", help="Clear cache and rebuild the draft"):
                    st.session_state.ai_draft = None
                    save_state()
                    st.rerun()
            st.markdown("---")
            edited = st.text_area("Review & Edit AI Draft", value=st.session_state.ai_draft, height=600)
            if edited != st.session_state.ai_draft:
                if st.button("Save Edits"):
                    st.session_state.ai_draft = edited
                    save_state()
                    st.success("Edits saved.")


# 9. SIGN OFF ──────────────────────────────────────────────────────────────
elif page == "signoff":
    hero_full("7d9337fdbff13df38d6ccd18b2a9ec7b.jpg", height="320px", pos="center 40%")
    eyebrow("Step 08 of 09")
    st.title("Sign Off")
    gold_rule()

    if not st.session_state.ai_draft:
        st.warning("The AI draft has not been generated yet. Please complete Step 07 first.")
    else:
        st.markdown("Both partners review and acknowledge the preparation draft before the final PDF is generated.")
        st.markdown("---")
        c1, c2 = st.columns(2, gap="large")
        pa = st.session_state.partner_a
        pb = st.session_state.partner_b

        with c1:
            st.markdown('<p style="font-size:0.62rem;letter-spacing:0.2em;text-transform:uppercase;color:#8A9E58;margin-bottom:0.8rem">Partner A Acknowledgment</p>', unsafe_allow_html=True)
            with st.form("signoff_a_form"):
                sa_name  = st.text_input("Full Name", value=st.session_state.signoff_a.get("name", pa.get("name","")), key="sa_name")
                sa_agree = st.checkbox("I have reviewed this preparation draft and understand it is not a final legal document and requires attorney review before execution.", value=st.session_state.signoff_a.get("agreed", False), key="sa_agree")
                sub_a = st.form_submit_button("Confirm Partner A Sign-Off")
            if sub_a:
                if sa_agree:
                    st.session_state.signoff_a = {"name": sa_name, "agreed": True, "timestamp": datetime.now().strftime("%B %d, %Y at %I:%M %p")}
                    save_state()
                    st.success(f"Partner A sign-off recorded — {st.session_state.signoff_a['timestamp']}")
                else:
                    st.error("Please check the acknowledgment box to confirm.")
            if st.session_state.signoff_a.get("agreed"):
                st.markdown(f'<p style="color:#8A9E58;font-size:0.76rem;margin-top:0.5rem">✓ Signed off — {st.session_state.signoff_a.get("timestamp","")}</p>', unsafe_allow_html=True)

        with c2:
            st.markdown('<p style="font-size:0.62rem;letter-spacing:0.2em;text-transform:uppercase;color:#8A9E58;margin-bottom:0.8rem">Partner B Acknowledgment</p>', unsafe_allow_html=True)
            with st.form("signoff_b_form"):
                sb_name  = st.text_input("Full Name", value=st.session_state.signoff_b.get("name", pb.get("name","")), key="sb_name")
                sb_agree = st.checkbox("I have reviewed this preparation draft and understand it is not a final legal document and requires attorney review before execution.", value=st.session_state.signoff_b.get("agreed", False), key="sb_agree")
                sub_b = st.form_submit_button("Confirm Partner B Sign-Off")
            if sub_b:
                if sb_agree:
                    st.session_state.signoff_b = {"name": sb_name, "agreed": True, "timestamp": datetime.now().strftime("%B %d, %Y at %I:%M %p")}
                    save_state()
                    st.success(f"Partner B sign-off recorded — {st.session_state.signoff_b['timestamp']}")
                else:
                    st.error("Please check the acknowledgment box to confirm.")
            if st.session_state.signoff_b.get("agreed"):
                st.markdown(f'<p style="color:#8A9E58;font-size:0.76rem;margin-top:0.5rem">✓ Signed off — {st.session_state.signoff_b.get("timestamp","")}</p>', unsafe_allow_html=True)

        both_signed = st.session_state.signoff_a.get("agreed") and st.session_state.signoff_b.get("agreed")
        if both_signed:
            st.markdown("---")
            gif_data = _b64("tumblr_nhpreeIvoL1rlnjw2o1_1280.gif")
            if gif_data:
                st.markdown(
                    f'<div style="display:flex;justify-content:center;margin:1rem 0 0.5rem 0">'
                    f'<img src="data:image/gif;base64,{gif_data}" '
                    f'style="max-width:420px;width:100%;border-radius:4px;" /></div>',
                    unsafe_allow_html=True,
                )
            pa_name = st.session_state.signoff_a.get("name", "Partner A")
            pb_name = st.session_state.signoff_b.get("name", "Partner B")
            st.markdown(
                f'<div style="text-align:center;padding:2rem 1rem;">'
                f'<p style="font-size:0.65rem;letter-spacing:0.28em;text-transform:uppercase;'
                f'color:#8A9E58;margin-bottom:0.5rem">Congratulations</p>'
                f'<h2 style="font-family:\'Playfair Display\',serif;font-size:2rem;'
                f'color:#F0EBE3;font-weight:400;margin:0 0 1rem 0">'
                f'{pa_name} &amp; {pb_name}</h2>'
                f'<p style="color:#888;font-size:0.9rem;max-width:480px;margin:0 auto 1.5rem auto;line-height:1.8">'
                f'You\'ve both taken an important step toward your future together. '
                f'Your preparation draft is signed, organised, and ready for your attorney. '
                f'The hard part is done — now let the professionals take it from here.</p>'
                f'<p style="color:#555;font-size:0.72rem;letter-spacing:0.06em">'
                f'Signed {st.session_state.signoff_a.get("timestamp","")}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown("---")
            if st.button("Generate Final PDF →"):
                go("final")


# 10. FINAL PDF ────────────────────────────────────────────────────────────
elif page == "final":
    eyebrow("Step 09 of 09")
    st.title("Final PDF")
    gold_rule()

    if not st.session_state.ai_draft:
        st.warning("AI draft not generated yet. Please complete Step 07.")
    elif not (st.session_state.signoff_a.get("agreed") and st.session_state.signoff_b.get("agreed")):
        st.warning("Both partners must sign off before generating the final PDF. Please complete Step 08.")
    else:
        pa = st.session_state.partner_a
        pb = st.session_state.partner_b
        case = st.session_state.case

        st.markdown("Your preparation draft is complete and signed off by both partners. Generate the PDF below.")
        st.markdown("---")

        c1, c2 = st.columns([3, 2], gap="large")
        with c1:
            st.markdown('<p style="font-size:0.62rem;letter-spacing:0.18em;text-transform:uppercase;color:#555;margin-bottom:0.8rem">Document Summary</p>', unsafe_allow_html=True)
            for item in [
                f"Couple: {case.get('case_name','')}",
                f"Theme: {detect_theme()}",
                f"Partner A: {pa.get('name','')} — signed off {st.session_state.signoff_a.get('timestamp','')}",
                f"Partner B: {pb.get('name','')} — signed off {st.session_state.signoff_b.get('timestamp','')}",
                f"Assets disclosed: {len(st.session_state.assets_a) + len(st.session_state.assets_b)}",
                f"Debts disclosed: {len(st.session_state.debts_a) + len(st.session_state.debts_b)}",
                f"Preference conflicts: {len(detect_conflicts())}",
            ]:
                li(item)

        with c2:
            st.markdown('<p style="font-size:0.62rem;letter-spacing:0.18em;text-transform:uppercase;color:#555;margin-bottom:0.8rem">Generate & Deliver</p>', unsafe_allow_html=True)

            with st.spinner("Building PDF…"):
                try:
                    pdf_bytes = build_pdf_bytes()
                    fname = f"knotwise_prenup_{case.get('case_name','draft').replace(' ','_')}.pdf"
                    st.download_button(
                        label="Download Final PDF",
                        data=pdf_bytes,
                        file_name=fname,
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"PDF generation failed: {e}")
                    pdf_bytes = None

            st.markdown("---")
            st.markdown('<p style="font-size:0.62rem;letter-spacing:0.14em;text-transform:uppercase;color:#555;margin-bottom:0.6rem">Email to Partners</p>', unsafe_allow_html=True)

            email_a = pa.get("email","")
            email_b = pb.get("email","")
            recipients = [e for e in [email_a, email_b] if e]

            if recipients:
                st.markdown(f'<p style="color:#555;font-size:0.74rem;margin-bottom:0.6rem">Will send to: {", ".join(recipients)}</p>', unsafe_allow_html=True)
                if st.button("Send PDF by Email", use_container_width=True):
                    if pdf_bytes:
                        with st.spinner("Sending email…"):
                            ok, msg = send_email_pdf(pdf_bytes, recipients)
                        if ok: st.success(msg)
                        else:  st.error(msg)
                    else:
                        st.error("PDF must be generated first.")
            else:
                st.caption("No partner email addresses captured. Add emails in the questionnaire to enable sending.")

        st.markdown("---")
        st.markdown('<p style="font-size:0.62rem;color:#1E1E1E;letter-spacing:0.04em;line-height:1.8">This document is a preparation draft only and does not constitute a valid prenuptial agreement. Both parties should retain independent legal counsel before executing any final agreement.</p>', unsafe_allow_html=True)


# ── REFERENCE / PROJECT DOCS ──────────────────────────────────────────────
elif page == "ref":
    eyebrow("NEC Residency Weekend")
    st.title("Project Documentation")
    gold_rule()
    st.markdown("All eight deliverable tasks — from project selection through implementation — documented for academic review.")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Tasks 1 – 2  |  Selection & Requirements",
        "Tasks 3 – 4  |  Data & App Architecture",
        "Tasks 5 – 6  |  Infrastructure & Security",
        "Tasks 7 – 8  |  Testing & Implementation",
    ])

    # ── TAB 1 ─────────────────────────────────────────────────────────────
    with tab1:
        with st.expander("Task 1 — Project Selection", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Project Name:** KnotWise — AI Prenup Preparation Assistant")
                st.markdown("**Group / Team:** Group 1 / Team A")
                st.markdown("**Date:** May 2026")
                st.markdown("**Business Problem**")
                st.markdown("Prenuptial agreements are expensive and time-consuming because couples arrive at attorney consultations without organised financial disclosures, aligned preferences, or a clear understanding of what they need to discuss. KnotWise reduces preparation time, improves partner transparency, and helps attorneys receive cleaner intake packages.")
            with col2:
                st.markdown("**Team Members**")
                team_df = pd.DataFrame([
                    {"Name": "Team Member 1", "Degree Program": "[Insert]", "Role": "Project Manager / Requirements Lead"},
                    {"Name": "Team Member 2", "Degree Program": "[Insert]", "Role": "Data Architect / Database Designer"},
                    {"Name": "Team Member 3", "Degree Program": "[Insert]", "Role": "Streamlit Frontend Developer"},
                    {"Name": "Team Member 4", "Degree Program": "[Insert]", "Role": "Backend Logic / AI Drafting Lead"},
                    {"Name": "Team Member 5", "Degree Program": "[Insert]", "Role": "Security, Testing & Risk Lead"},
                ])
                st.dataframe(team_df, use_container_width=True, hide_index=True)
            st.markdown("**Proposed Application**")
            st.markdown("KnotWise is a Streamlit web app where both partners complete questionnaires, disclose assets and debts, set prenup goals, and receive an AI-generated preparation draft. Gemini 1.5 Flash fills a fixed template using captured data — one API call, cached in session. The final output is a signed PDF delivered by email or download.")

        with st.expander("Task 2 — Requirements Definition"):
            st.markdown("**Stakeholder Analysis**")
            stakeholder_df = pd.DataFrame([
                {"Stakeholder": "Partner A",          "Interest": "Complete disclosures, protect assets",    "Influence": "High"},
                {"Stakeholder": "Partner B",          "Interest": "Complete disclosures, protect assets",    "Influence": "High"},
                {"Stakeholder": "Attorney / Reviewer","Interest": "Receive clean intake package",            "Influence": "High"},
                {"Stakeholder": "Product Owner",      "Interest": "Deliver viable MVP for class",            "Influence": "High"},
                {"Stakeholder": "App Administrator",  "Interest": "Manage user data and security",           "Influence": "Medium"},
                {"Stakeholder": "Notary / Signing Svc","Interest":"Execute final agreement",                 "Influence": "Low"},
            ])
            st.dataframe(stakeholder_df, use_container_width=True, hide_index=True)

            st.markdown("**RACI Chart (abbreviated)**")
            raci_df = pd.DataFrame([
                {"Activity": "Define business problem",       "Product Owner":"A","Project Mgr":"R","Data Architect":"C","Frontend Dev":"C","Backend/AI Dev":"C","Security Lead":"C"},
                {"Activity": "Design questionnaire flow",     "Product Owner":"A","Project Mgr":"R","Data Architect":"C","Frontend Dev":"C","Backend/AI Dev":"R","Security Lead":"C"},
                {"Activity": "Build data model",              "Product Owner":"C","Project Mgr":"C","Data Architect":"R/A","Frontend Dev":"C","Backend/AI Dev":"C","Security Lead":"C"},
                {"Activity": "Build Streamlit UI",            "Product Owner":"C","Project Mgr":"C","Data Architect":"I","Frontend Dev":"R/A","Backend/AI Dev":"C","Security Lead":"C"},
                {"Activity": "Build scoring + conflict logic","Product Owner":"C","Project Mgr":"C","Data Architect":"C","Frontend Dev":"C","Backend/AI Dev":"R/A","Security Lead":"C"},
                {"Activity": "Gemini AI integration",         "Product Owner":"C","Project Mgr":"C","Data Architect":"C","Frontend Dev":"C","Backend/AI Dev":"R/A","Security Lead":"C"},
                {"Activity": "Security design",               "Product Owner":"C","Project Mgr":"C","Data Architect":"C","Frontend Dev":"C","Backend/AI Dev":"C","Security Lead":"R/A"},
                {"Activity": "Testing",                       "Product Owner":"C","Project Mgr":"C","Data Architect":"C","Frontend Dev":"R","Backend/AI Dev":"R","Security Lead":"A"},
            ])
            st.dataframe(raci_df, use_container_width=True, hide_index=True)
            st.caption("R = Responsible  A = Accountable  C = Consulted  I = Informed")

            st.markdown("**Functional Requirements**")
            for i, r in enumerate([
                "System shall allow Partner A to create a prenup preparation case",
                "System shall allow Partner A to invite Partner B to a separate questionnaire",
                "System shall collect couple info: location, wedding date, marital residence",
                "System shall collect income, assets, debts, business ownership, real estate, retirement, and inheritance per partner",
                "System shall allow each partner to select prenup goals and preferences",
                "System shall compare both partners' responses and identify conflicts",
                "System shall calculate a prenup readiness score with breakdown",
                "System shall generate a missing document checklist",
                "System shall call Gemini AI once to fill a structured prenup template and cache the result",
                "System shall allow both partners to digitally sign off with timestamps",
                "System shall generate a PDF with AI draft + sign-off blocks",
                "System shall deliver the PDF by download and optionally by email",
            ], 1):
                li(f"FR-{i:02d}: {r}")

            st.markdown("**Non-Functional Requirements**")
            for r in ["Pages load within 3 seconds for normal usage","Sensitive financial data protected via encrypted secrets management","Easy to use for non-technical users — no legal knowledge required","Clear disclaimers: AI drafts require attorney review before execution","Role concept for Partner A, Partner B, attorney reviewer, and admin","Audit-ready: questionnaire submission and draft generation timestamped","Scalable architecture to support future attorney marketplace integration","Explainable scoring logic — users see exactly why their score is what it is"]:
                li(r)

    # ── TAB 2 ─────────────────────────────────────────────────────────────
    with tab2:
        with st.expander("Task 3 — Data Architecture", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Conceptual Model — Core Entities**")
                for e in ["Couple Case","Partner Profile","Questionnaire Response","Asset","Debt","Prenup Goal","Conflict Flag","Readiness Score","AI Draft Document","Sign-Off Record","Attorney Review Request","Audit Log"]:
                    li(e)
            with col2:
                st.markdown("**Logical Model — Key Fields**")
                logical_df = pd.DataFrame([
                    {"Entity": "Couple Case",        "Key Fields": "case_id, case_name, wedding_date, state, country, status"},
                    {"Entity": "Partner Profile",    "Key Fields": "partner_id, case_id, name, email, role, citizenship, income"},
                    {"Entity": "Asset",              "Key Fields": "asset_id, partner_id, asset_type, description, value, preference"},
                    {"Entity": "Debt",               "Key Fields": "debt_id, partner_id, debt_type, balance, preference"},
                    {"Entity": "Prenup Goal",        "Key Fields": "goal_id, partner_id, goal_category, selected_preference"},
                    {"Entity": "Conflict Flag",      "Key Fields": "conflict_id, case_id, topic, severity, recommendation"},
                    {"Entity": "Readiness Score",    "Key Fields": "score_id, case_id, score_value, explanation_json"},
                    {"Entity": "AI Draft",           "Key Fields": "draft_id, case_id, draft_text, model, generated_at"},
                    {"Entity": "Sign-Off Record",    "Key Fields": "signoff_id, partner_id, name, agreed, timestamp"},
                ])
                st.dataframe(logical_df, use_container_width=True, hide_index=True)

            st.markdown("**Physical Model**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("*Prototype (current)*")
                for item in ["Streamlit session state (in-memory)","CSV export for reports","Secrets managed via Streamlit Cloud secrets.toml","Gemini API for AI draft generation"]:
                    li(item)
            with col2:
                st.markdown("*Production (future)*")
                for item in ["PostgreSQL with encrypted columns","FastAPI backend with JWT auth","AWS S3 for generated PDF storage","AWS Secrets Manager for API keys","Audit log table in PostgreSQL"]:
                    li(item)

            st.markdown("**Data Governance Plan**")
            for item in ["Data minimization: collect only what is needed for prenup preparation","Role-based access: each partner accesses only their own profile and shared case","Consent-based sharing: partner responses shared only after both submit","Data retention policy: users can request deletion of case data","Audit logging: questionnaire submission, draft generation, and sign-off recorded","Data classification: financial disclosures and preferences classified as Confidential","Data quality rules: required fields, valid currency formats, duplicate asset checks","Secure export: generated PDFs not publicly accessible without authenticated session"]:
                li(item)

            st.markdown("**Ethical & Regulatory Impact Analysis**")
            ethics_df = pd.DataFrame([
                {"Area": "Data Privacy",       "Risk": "Collection of sensitive financial and personal information","Mitigation": "Encryption, access control, clear privacy policy, data minimization"},
                {"Area": "GDPR / CCPA",        "Risk": "User may be subject to EU or California privacy law","Mitigation": "Consent capture, right to deletion, data residency disclosure"},
                {"Area": "AI Bias",            "Risk": "Gemini may produce biased or jurisdictionally inaccurate language","Mitigation": "Fixed template structure, attorney review required, disclaimers on all AI output"},
                {"Area": "AI Hallucination",   "Risk": "Model generates incorrect legal clauses","Mitigation": "Limit AI to template-filling, not free-form drafting; flag as draft only"},
                {"Area": "Unauthorized Practice","Risk":"App may be perceived as providing legal advice","Mitigation": "Prominent disclaimers on every page and in the PDF"},
                {"Area": "Human Oversight",    "Risk": "Users rely solely on AI output","Mitigation": "Attorney review gate in workflow, sign-off step, readiness score explainability"},
            ])
            st.dataframe(ethics_df, use_container_width=True, hide_index=True)

        with st.expander("Task 4 — Application Architecture"):
            st.markdown("**Application Flow**")
            st.code("User → Streamlit UI → Questionnaire Forms → Session / Data Layer\n→ Scoring Engine → Conflict Engine → Theme Detector\n→ Gemini 1.5 Flash (one call, cached) → PDF Builder\n→ Sign-Off Module → Email / Download Delivery", language="text")

            st.markdown("**Architectural Decision Records (ADR)**")
            adr_df = pd.DataFrame([
                {"ADR": "ADR-01", "Decision": "Use Streamlit for frontend", "Alternatives": "React, Flask, Django", "Trade-off": "Less customisable but 10× faster to build","Business Impact": "Working demo in 3 days","Risk": "Limited UI flexibility — acceptable for prototype"},
                {"ADR": "ADR-02", "Decision": "Rule-based scoring before AI", "Alternatives": "Fully AI-generated scoring","Trade-off": "Less flexible but fully explainable","Business Impact": "Users understand their readiness score","Risk": "Reduces hallucination and bias risk"},
                {"ADR": "ADR-03", "Decision": "Session state for prototype storage", "Alternatives": "PostgreSQL, SQLite, Firebase","Trade-off": "Simple and fast but not persistent","Business Impact": "Rapid development and demo readiness","Risk": "Production requires full database migration"},
                {"ADR": "ADR-04", "Decision": "AI fills fixed template, not free-form", "Alternatives": "Fully AI-generated prenup","Trade-off": "Less creative but predictable and safe","Business Impact": "Reduces legal and ethical risk","Risk": "Output consistency over flexibility"},
                {"ADR": "ADR-05", "Decision": "Gemini 1.5 Flash (free tier)", "Alternatives": "GPT-4, Claude, Mistral","Trade-off": "Free but rate-limited","Business Impact": "Zero API cost for class prototype","Risk": "Production would require paid tier"},
            ])
            st.dataframe(adr_df, use_container_width=True, hide_index=True)

    # ── TAB 3 ─────────────────────────────────────────────────────────────
    with tab3:
        with st.expander("Task 5 — Infrastructure Architecture", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Cloud Choice**")
                st.markdown("*Prototype:* Streamlit Community Cloud (free, GitHub-connected, zero-config deployment)")
                st.markdown("*Production:* AWS (recommended) — managed RDS, S3, Cognito, CloudWatch, WAF, and multi-AZ deployment")
                st.markdown("**Infrastructure Diagram — Prototype**")
                st.code("User Browser\n  └── Streamlit Community Cloud\n        └── app.py (Python 3.14)\n              ├── Google Gemini API (HTTPS)\n              ├── Streamlit Secrets (encrypted)\n              └── Gmail SMTP (PDF delivery)", language="text")
            with col2:
                st.markdown("**Infrastructure Diagram — Production**")
                st.code("User Browser\n  └── CloudFront CDN\n        └── ALB (Load Balancer)\n              ├── ECS Fargate (app containers)\n              │     └── FastAPI + Streamlit\n              ├── RDS PostgreSQL (Multi-AZ)\n              ├── S3 (PDF storage, encrypted)\n              ├── Cognito (Auth)\n              └── SES (Email delivery)", language="text")
                st.markdown("**Failover Strategy**")
                for item in ["Multi-AZ RDS with automated failover (<30s)","ECS Fargate auto-scaling (2–10 tasks)","CloudFront serves cached static assets during app downtime","Health checks every 30 seconds, auto-restart on failure"]:
                    li(item)

            st.markdown("**Backup & Disaster Recovery**")
            dr_df = pd.DataFrame([
                {"Item": "Database backups",     "Frequency": "Daily automated snapshots", "Retention": "30 days",  "Storage": "S3 (encrypted)"},
                {"Item": "PDF documents",        "Frequency": "On generation",             "Retention": "7 years",  "Storage": "S3 with versioning"},
                {"Item": "App config / secrets", "Frequency": "On change",                 "Retention": "Indefinite","Storage": "AWS Secrets Manager"},
                {"Item": "RTO (Recovery Time)",  "Frequency": "—",                         "Retention": "< 4 hours","Storage": "Multi-AZ auto-failover"},
                {"Item": "RPO (Recovery Point)", "Frequency": "—",                         "Retention": "< 24 hours","Storage": "Daily backup window"},
            ])
            st.dataframe(dr_df, use_container_width=True, hide_index=True)

        with st.expander("Task 6 — Security Architecture"):
            st.markdown("**Identity & Access Management**")
            for item in ["Partner A and Partner B: separate authenticated sessions in production","Attorney reviewer: read-only case access after partner consent","Admin: full case management with audit log visibility","MFA required for attorney and admin roles in production","JWT tokens with 1-hour expiry; refresh token rotation"]:
                li(item)

            st.markdown("**Security Controls Mapped to NIST / ISO 27001**")
            controls_df = pd.DataFrame([
                {"Control Area": "Access Control",     "NIST / ISO":  "NIST AC / ISO A.5, A.8", "Application Control": "Role-based access for partners, attorneys, and admins"},
                {"Control Area": "Data Protection",    "NIST / ISO":  "NIST SC / ISO A.8",      "Application Control": "Encryption at rest (AES-256) and in transit (TLS 1.3)"},
                {"Control Area": "Audit Logging",      "NIST / ISO":  "NIST AU / ISO A.8",      "Application Control": "Questionnaire submission, draft generation, sign-off timestamped"},
                {"Control Area": "Input Validation",   "NIST / ISO":  "NIST SI / ISO A.8",      "Application Control": "Server-side validation of all form fields; SQL injection N/A (no raw SQL)"},
                {"Control Area": "AI Prompt Security", "NIST / ISO":  "NIST SA / ISO A.8",      "Application Control": "Structured prompt with no user-controlled injection points"},
                {"Control Area": "Incident Response",  "NIST / ISO":  "NIST IR / ISO A.5",      "Application Control": "Playbook for data breach notification within 72 hours (GDPR)"},
                {"Control Area": "Backup & Recovery",  "NIST / ISO":  "NIST CP / ISO A.8",      "Application Control": "Daily backups, RTO 4h, RPO 24h, quarterly DR test"},
                {"Control Area": "Network Security",   "NIST / ISO":  "NIST SC / ISO A.8",      "Application Control": "WAF, private DB subnet, no public RDS endpoint, HTTPS-only"},
            ])
            st.dataframe(controls_df, use_container_width=True, hide_index=True)
            st.caption("HIPAA does not apply — KnotWise is not a healthcare application.")

            st.markdown("**Enterprise Risk Register**")
            risk_df = pd.DataFrame([
                {"#": 1, "Risk": "Users rely on AI draft as final legal advice",   "Probability": "Medium","Impact": "High",  "Mitigation": "Prominent disclaimers, attorney review gate, sign-off step", "Owner": "Product Owner"},
                {"#": 2, "Risk": "Sensitive financial data exposure",               "Probability": "Medium","Impact": "High",  "Mitigation": "Encryption, RBAC, secure secrets management",               "Owner": "Security Lead"},
                {"#": 3, "Risk": "Incorrect/incomplete AI draft language",          "Probability": "Medium","Impact": "High",  "Mitigation": "Fixed template, attorney review required, draft labelling",   "Owner": "Backend/AI Lead"},
                {"#": 4, "Risk": "Partner data shared without consent",             "Probability": "Low",   "Impact": "High",  "Mitigation": "Consent-based sharing, role-based access controls",           "Owner": "Security Lead"},
                {"#": 5, "Risk": "AI hallucination or jurisdictional inaccuracy",  "Probability": "Medium","Impact": "Medium","Mitigation": "Structured prompt, limit to template-filling, flag as draft",   "Owner": "Backend/AI Lead"},
                {"#": 6, "Risk": "Incomplete financial disclosure by partners",    "Probability": "High",  "Impact": "Medium","Mitigation": "Missing doc checklist, readiness score gate",                   "Owner": "Data Architect"},
                {"#": 7, "Risk": "Application downtime during demo",               "Probability": "Low",   "Impact": "Medium","Mitigation": "Streamlit Cloud auto-restart, GitHub-linked redeployment",     "Owner": "Infrastructure Lead"},
                {"#": 8, "Risk": "Unauthorised access to attorney/admin view",     "Probability": "Low",   "Impact": "High",  "Mitigation": "Authentication, least privilege, audit logging",               "Owner": "Security Lead"},
                {"#": 9, "Risk": "Poor user adoption due to complex forms",        "Probability": "Medium","Impact": "Medium","Mitigation": "Step-by-step flow, progress score, plain-English questions",    "Owner": "Frontend Lead"},
                {"#":10, "Risk": "Jurisdiction mismatch in generated language",    "Probability": "Medium","Impact": "High",  "Mitigation": "Collect jurisdiction data, flag cross-border cases, attorney gate","Owner": "Product Owner"},
            ])
            st.dataframe(risk_df, use_container_width=True, hide_index=True)

    # ── TAB 4 ─────────────────────────────────────────────────────────────
    with tab4:
        with st.expander("Task 7 — Testing Strategy", expanded=True):
            st.markdown("**Test Coverage Plan**")
            test_df = pd.DataFrame([
                {"Type": "Unit Testing",        "Scope": "Individual Python functions",                         "What": "completion_score(), detect_conflicts(), detect_theme(), build_prenup_prompt()", "Tool": "pytest"},
                {"Type": "Integration Testing", "Scope": "Form → session state → scoring pipeline",            "What": "Form submission updates session state; scoring uses saved responses correctly", "Tool": "pytest + streamlit testing"},
                {"Type": "System Testing",      "Scope": "Full end-to-end user journey",                       "What": "Steps 1–9: case → invite → questionnaires → assets → AI draft → sign-off → PDF", "Tool": "Manual + Playwright"},
                {"Type": "Performance Testing", "Scope": "Page load times, Gemini API latency",                "What": "All pages < 3s; Gemini call < 15s; PDF generation < 5s",                      "Tool": "Streamlit metrics + manual"},
                {"Type": "Security Testing",    "Scope": "Input validation, prompt injection, data exposure",  "What": "Form fields, AI prompt construction, secrets handling, session isolation",     "Tool": "Manual + OWASP checklist"},
                {"Type": "User Acceptance",     "Scope": "Real-world usability with test users",               "What": "Complete questionnaire, understand score, download summary, review draft",    "Tool": "Classmate testing + feedback form"},
            ])
            st.dataframe(test_df, use_container_width=True, hide_index=True)

            st.markdown("**Unit Test Examples**")
            st.code("""# Test scoring logic
def test_completion_score_empty():
    # Fresh session state → score should be 0
    assert completion_score()[0] == 0

# Test conflict detection
def test_detect_conflicts_identical_goals():
    # Same preferences → no conflicts
    goals = {"premarital_assets": "Keep separate", ...}
    assert detect_conflicts(goals, goals) == []

# Test theme detection
def test_detect_theme_protection_focus():
    goals_a = goals_b = {"premarital_assets": "Keep separate",
                          "spousal_support": "Waived", ...}
    assert detect_theme(goals_a, goals_b) == "Asset Protection Focus"
""", language="python")

        with st.expander("Task 8 — Implementation Plan"):
            st.markdown("**Resource Plan**")
            resource_df = pd.DataFrame([
                {"Resource": "Streamlit",           "Purpose": "Web application frontend",                         "Cost": "Free"},
                {"Resource": "Python 3.11+",        "Purpose": "Business logic, scoring, conflict detection",      "Cost": "Free"},
                {"Resource": "Pandas",              "Purpose": "Data processing and display",                      "Cost": "Free"},
                {"Resource": "Google Gemini Flash", "Purpose": "AI prenup draft generation",                      "Cost": "Free tier (1M tokens/day)"},
                {"Resource": "fpdf2",               "Purpose": "PDF generation",                                   "Cost": "Free"},
                {"Resource": "Streamlit Community Cloud","Purpose":"Deployment and hosting",                       "Cost": "Free"},
                {"Resource": "GitHub",              "Purpose": "Source code management and CI/CD",                 "Cost": "Free"},
                {"Resource": "Gmail SMTP",          "Purpose": "PDF email delivery to partners",                   "Cost": "Free"},
                {"Resource": "Team Members (5)",    "Purpose": "Requirements, dev, data, security, testing, demo","Cost": "N/A"},
            ])
            st.dataframe(resource_df, use_container_width=True, hide_index=True)

            st.markdown("**3-Day Sprint Timeline**")
            timeline_df = pd.DataFrame([
                {"Day": "Day 1", "Focus": "Foundation",    "Deliverables": "Project scope, requirements doc, data model, Streamlit layout, questionnaire fields, sample data"},
                {"Day": "Day 2", "Focus": "Core Build",    "Deliverables": "Partner A/B forms, scoring logic, conflict detection, risk dashboard, draft preview, security docs"},
                {"Day": "Day 3", "Focus": "AI + Delivery", "Deliverables": "Gemini integration, sign-off flow, PDF generation, email delivery, testing, risk register, presentation prep"},
            ])
            st.dataframe(timeline_df, use_container_width=True, hide_index=True)

            st.markdown("**Risk Management for Delivery**")
            for item in ["Scope control: MVP focuses on questionnaire intake, conflict detection, AI draft, sign-off, PDF — no advanced features","Daily progress checks to identify blockers early","Use Streamlit + session state to avoid complex backend setup","All AI output labelled as draft — reduces legal and ethical delivery risk","Fallback plan: if Gemini API fails, show rule-based template draft instead"]:
                li(item)
