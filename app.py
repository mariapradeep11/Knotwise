
import streamlit as st
import pandas as pd
from datetime import date, datetime
from io import BytesIO
import base64
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
@keyframes kwPageIn { from { opacity: 0; transform: translateY(7px); } to { opacity: 1; transform: translateY(0); } }
section.main > div { animation: kwPageIn 0.4s ease-out both; }

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


# ── Session State ─────────────────────────────────────────────────────────
def init_state():
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


# ── AI: Gemini call (cached) ──────────────────────────────────────────────
def call_gemini():
    if st.session_state.ai_draft:
        return st.session_state.ai_draft, None
    try:
        import google.generativeai as genai
        key = st.secrets.get("knotwise_gemini_key", "")
        if not key:
            return None, "API key not configured. Add `knotwise_gemini_key` to Streamlit secrets."
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(build_prenup_prompt())
        st.session_state.ai_draft = response.text
        return response.text, None
    except Exception as e:
        return None, str(e)


# ── PDF builder ───────────────────────────────────────────────────────────
def build_pdf_bytes():
    from fpdf import FPDF

    class KWDoc(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 7.5)
            self.set_text_color(138, 158, 88)
            self.cell(0, 7, "KNOTWISE  |  PRENUPTIAL AGREEMENT PREPARATION DRAFT", align="C")
            self.ln(1)
            self.set_draw_color(138, 158, 88)
            self.set_line_width(0.2)
            self.line(15, self.get_y(), 195, self.get_y())
            self.ln(5)

        def footer(self):
            self.set_y(-13)
            self.set_font("Helvetica", "I", 6.5)
            self.set_text_color(160, 160, 160)
            self.cell(0, 5, f"PREPARATION DRAFT — FOR ATTORNEY REVIEW ONLY  |  Page {self.page_no()}  |  KnotWise Academic Prototype", align="C")

    pdf = KWDoc(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    case  = st.session_state.case
    pa, pb = st.session_state.partner_a, st.session_state.partner_b
    sa, sb = st.session_state.signoff_a, st.session_state.signoff_b
    draft  = st.session_state.ai_draft or ""
    theme  = detect_theme()

    # Title block
    pdf.set_font("Helvetica", "B", 17)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 12, "PRENUPTIAL AGREEMENT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 5, "Preparation Draft for Attorney Review  |  Not a Final Legal Document", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # Info box
    pdf.set_fill_color(250, 250, 248)
    pdf.set_draw_color(180, 195, 150)
    pdf.set_line_width(0.3)
    box_y = pdf.get_y()
    pdf.rect(15, box_y, 180, 26, style="FD")
    pdf.set_xy(20, box_y + 4)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(70, 70, 70)
    pdf.cell(88, 5, pdf_safe(f"Couple: {case.get('case_name','')}"), new_x="RIGHT", new_y="TOP")
    pdf.cell(88, 5, pdf_safe(f"Wedding Date: {case.get('wedding_date','')}"))
    pdf.set_x(20); pdf.ln(6)
    pdf.cell(88, 5, pdf_safe(f"Residence: {case.get('future_residence','')}"), new_x="RIGHT", new_y="TOP")
    pdf.cell(88, 5, pdf_safe(f"Jurisdiction: {case.get('jurisdictions','')}"))
    pdf.set_x(20); pdf.ln(6)
    pdf.set_font("Helvetica", "I", 7.5)
    pdf.set_text_color(120, 145, 70)
    pdf.cell(0, 5, pdf_safe(f"Agreement Theme: {theme}"))
    pdf.ln(10)

    # AI Draft content
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(25, 25, 25)

    for line in draft.split('\n'):
        line = pdf_safe(line.strip())
        if not line:
            pdf.ln(2.5)
            continue
        # Section headers: starts with digit and dot, or all caps short line
        is_header = (len(line) > 2 and line[0].isdigit() and '. ' in line[:5]) or (line.isupper() and len(line) < 80)
        if is_header:
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(120, 145, 70)
            pdf.multi_cell(0, 6, line)
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(25, 25, 25)
            pdf.ln(1)
        else:
            pdf.multi_cell(0, 5.5, line)

    # Sign-off page
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, "ACKNOWLEDGMENT & SIGN-OFF", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(138, 158, 88)
    pdf.set_line_width(0.4)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(6)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 5.5, pdf_safe(
        "Both parties confirm they have reviewed this preparation draft, understand it is not a final legal agreement, "
        "and acknowledge it requires independent attorney review before execution."))
    pdf.ln(8)

    # Two signature columns
    y = pdf.get_y()
    for x_off, partner_label, partner_data, signoff_data in [
        (15, "PARTNER A", pa, sa), (110, "PARTNER B", pb, sb)
    ]:
        pdf.set_xy(x_off, y)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(120, 145, 70)
        pdf.cell(80, 6, partner_label)
        pdf.set_xy(x_off, y + 8)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(80, 5.5, pdf_safe(f"Name: {signoff_data.get('name', partner_data.get('name',''))}"))
        pdf.set_xy(x_off, y + 14)
        pdf.cell(80, 5.5, pdf_safe(f"Acknowledged: {'Yes' if signoff_data.get('agreed') else 'Pending'}"))
        pdf.set_xy(x_off, y + 20)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(80, 5.5, pdf_safe(f"Date & Time: {signoff_data.get('timestamp', 'Not recorded')}"))

    pdf.set_y(y + 32)
    pdf.set_draw_color(200, 200, 200)
    pdf.set_line_width(0.3)
    sig_y = pdf.get_y() + 18
    pdf.line(15, sig_y, 90, sig_y)
    pdf.line(110, sig_y, 185, sig_y)
    pdf.set_y(sig_y + 2)
    pdf.set_font("Helvetica", "I", 7.5)
    pdf.set_text_color(150, 150, 150)
    pdf.set_x(15); pdf.cell(80, 5, pdf_safe(f"Signature — {pa.get('name','Partner A')}"), new_x="RIGHT", new_y="TOP")
    pdf.set_x(110); pdf.cell(80, 5, pdf_safe(f"Signature — {pb.get('name','Partner B')}"))
    pdf.ln(16)

    # Disclaimer box
    pdf.set_fill_color(252, 252, 250)
    pdf.set_draw_color(180, 195, 150)
    pdf.set_line_width(0.2)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(140, 130, 100)
    pdf.multi_cell(0, 4.2, pdf_safe(
        f"IMPORTANT DISCLAIMER: This document is a preparation draft generated by KnotWise, an academic demonstration prototype. "
        f"It is not legal advice and does not constitute a valid prenuptial agreement. Both parties must retain independent legal counsel "
        f"before executing any final agreement. KnotWise is not a law firm and does not provide legal services. "
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
def partner_form(label, state_key):
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
        submitted = st.form_submit_button(f"Save {label} Questionnaire")

    if submitted:
        st.session_state[state_key] = {"name":name,"email":email,"citizenship":citizenship,"immigration_status":immigration_status,"income":income,"owns_business":owns_business,"owns_real_estate":owns_real_estate,"has_children_prior":has_children_prior,"supports_family":supports_family,"notes":notes}
        goal_key = "goals_a" if state_key == "partner_a" else "goals_b"
        st.session_state[goal_key] = {"premarital_assets":premarital_assets,"future_income":future_income,"business_growth":business_growth,"debt_responsibility":debt_responsibility,"spousal_support":spousal_support,"inheritance":inheritance,"home_purchase":home_purchase}
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
            submitted = st.form_submit_button("Save Case Setup")
        if submitted:
            st.session_state.case = {"case_name":case_name,"wedding_date":str(wedding_date),"current_residence":current_residence,"future_residence":future_residence,"jurisdictions":jurisdictions,"cross_border":cross_border}
            st.session_state.case_created = True
            st.session_state.ai_draft = None  # reset draft if case changes
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
            sent = st.form_submit_button("Prepare Partner Invitation")
        if sent:
            st.session_state.partner_invited = True
            st.session_state.invite_email = invite_email
            if partner_name: st.session_state.partner_b["name"] = partner_name
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
    partner_form("Partner A", "partner_a")


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
    partner_form("Partner B", "partner_b")


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
            st.session_state.ai_draft = None; st.success("Asset added.")
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
            st.session_state.ai_draft = None; st.success("Debt added.")
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
                st.success("Document metadata saved.")
            else:
                st.error("Please upload a file first.")
        if st.session_state.uploaded_docs:
            st.dataframe(pd.DataFrame(st.session_state.uploaded_docs), use_container_width=True)


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
        st.markdown(f"Gemini AI will fill the prenup template using all captured questionnaire data. The AI runs **once** and the result is cached — it will not re-run unless you explicitly regenerate.")
        st.markdown(f'<p style="font-size:0.72rem;color:#8A9E58;margin-top:0.8rem">Detected theme: <strong>{theme}</strong></p>', unsafe_allow_html=True)

    st.markdown("---")

    if not ai_ready():
        missing_steps = []
        if not st.session_state.case_created: missing_steps.append("Case Setup")
        if not st.session_state.partner_a: missing_steps.append("Partner A Questionnaire")
        if not st.session_state.partner_b: missing_steps.append("Partner B Questionnaire")
        if not st.session_state.goals_a or not st.session_state.goals_b: missing_steps.append("Prenup Preferences (both partners)")
        st.markdown('<div class="kw-lock-box">', unsafe_allow_html=True)
        st.markdown('<p style="color:#555;font-size:0.8rem;margin-bottom:0.6rem">Complete the following steps before generating the AI draft:</p>', unsafe_allow_html=True)
        for s in missing_steps:
            st.markdown(f'<p style="color:#8A9E58;font-size:0.78rem;margin:0.2rem 0">— {s}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        if not st.session_state.ai_draft:
            st.markdown('<div class="kw-ai-box">', unsafe_allow_html=True)
            st.markdown('<p style="color:#999;font-size:0.82rem;margin-bottom:1rem">All required data is captured. Click below to generate your AI prenup draft. This will make <strong style="color:#8A9E58">one API call</strong> to Google Gemini and cache the result.</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("Generate AI Draft", use_container_width=False):
                with st.spinner("Gemini is drafting your prenup…"):
                    draft, err = call_gemini()
                if err:
                    st.error(f"Generation failed: {err}")
                else:
                    st.success("Draft generated and cached. Scroll down to review.")
                    st.rerun()
        else:
            st.success("AI draft generated and cached. Edit or proceed to Sign Off.")
            col_dl, col_regen = st.columns([3, 1])
            with col_regen:
                if st.button("↺ Regenerate", help="This will make another API call"):
                    st.session_state.ai_draft = None
                    st.rerun()
            st.markdown("---")
            edited = st.text_area("Review & Edit AI Draft", value=st.session_state.ai_draft, height=600)
            if edited != st.session_state.ai_draft:
                if st.button("Save Edits"):
                    st.session_state.ai_draft = edited
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
