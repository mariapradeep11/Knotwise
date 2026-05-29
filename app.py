
import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO
import base64
from pathlib import Path

st.set_page_config(
    page_title="KnotWise | AI Prenup Preparation",
    page_icon="💍",
    layout="wide",
)

# ── Theme & Animations ────────────────────────────────────────────────────
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

/* ── Nav row ── */
div[data-testid="stHorizontalBlock"]:first-of-type .stButton button {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid #191919 !important;
    border-radius: 0 !important;
    color: #2A2A2A !important;
    font-size: 0.58rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.55rem 0.1rem !important;
    line-height: 1.9 !important;
    transition: color 0.18s, border-color 0.18s !important;
    font-family: 'Inter', sans-serif !important;
}
div[data-testid="stHorizontalBlock"]:first-of-type .stButton button:hover {
    color: #777 !important;
    border-bottom-color: #444 !important;
}

/* ── Typography ── */
h1, h2, h3, h4 {
    font-family: 'Playfair Display', serif !important;
    color: #F0EBE3 !important;
    font-weight: 400 !important;
}
h1 { font-size: 2.6rem !important; line-height: 1.18 !important; }
h2 { font-size: 1.7rem !important; }
p, li { color: #666 !important; line-height: 1.75 !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] h2 { font-size: 1.4rem !important; color: #F0EBE3 !important; }
section[data-testid="stSidebar"] p { color: #2E2E2E !important; font-size: 0.68rem !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: #0A0A0A !important; border: 1px solid #161616 !important;
    border-radius: 2px !important; padding: 1.2rem 1rem !important;
}
[data-testid="stMetricLabel"] p {
    color: #333 !important; font-size: 0.58rem !important;
    letter-spacing: 0.2em !important; text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    color: #C9A84C !important; font-size: 1.9rem !important;
}

/* ── Inputs ── */
[data-baseweb="input"] > div { background: #080808 !important; border-color: #1C1C1C !important; border-radius: 2px !important; }
[data-baseweb="textarea"] { background: #080808 !important; border-color: #1C1C1C !important; border-radius: 2px !important; }
input, textarea { color: #D4CFC8 !important; font-family: 'Inter', sans-serif !important; }
[data-baseweb="select"] > div { background: #080808 !important; border-color: #1C1C1C !important; border-radius: 2px !important; color: #D4CFC8 !important; }
[data-baseweb="menu"] { background: #111 !important; border: 1px solid #1E1E1E !important; }
[data-baseweb="menu"] li { background: #111 !important; color: #D4CFC8 !important; }
[data-baseweb="menu"] li:hover { background: #181818 !important; }
label, .stSelectbox label, .stTextInput label, .stNumberInput label, .stTextArea label {
    color: #3A3A3A !important; font-size: 0.64rem !important;
    letter-spacing: 0.1em !important; text-transform: uppercase !important;
}
[data-testid="stCheckbox"] label span { color: #666 !important; font-size: 0.76rem !important; }

/* ── Buttons (non-nav) ── */
.stButton > button {
    background: transparent !important; border: 1px solid #C9A84C !important;
    color: #C9A84C !important; font-size: 0.65rem !important;
    letter-spacing: 0.14em !important; text-transform: uppercase !important;
    border-radius: 0 !important; padding: 0.5rem 1.4rem !important;
}
.stButton > button:hover { background: #C9A84C !important; color: #0C0C0C !important; }
[data-testid="stFormSubmitButton"] button {
    background: #C9A84C !important; color: #0C0C0C !important;
    border: none !important; font-weight: 600 !important;
    font-size: 0.65rem !important; letter-spacing: 0.14em !important;
    text-transform: uppercase !important; border-radius: 0 !important;
}
.stDownloadButton > button {
    background: transparent !important; border: 1px solid #C9A84C !important;
    color: #C9A84C !important; border-radius: 0 !important;
    font-size: 0.65rem !important; letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}
.stDownloadButton > button:hover { background: #C9A84C !important; color: #0C0C0C !important; }

/* ── Progress ── */
div[data-testid="stProgressBar"] > div > div > div {
    background: linear-gradient(90deg, #C9A84C 0%, #E8C96A 100%) !important;
}

/* ── Tabs ── */
[data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid #181818 !important; }
button[data-baseweb="tab"] {
    background: transparent !important; color: #2A2A2A !important;
    font-size: 0.64rem !important; letter-spacing: 0.14em !important;
    text-transform: uppercase !important; padding: 0.7rem 1.2rem !important;
}
button[data-baseweb="tab"][aria-selected="true"] { color: #C9A84C !important; border-bottom: 2px solid #C9A84C !important; }

/* ── Form ── */
[data-testid="stForm"] { background: #070707 !important; border: 1px solid #131313 !important; border-radius: 2px !important; padding: 1.8rem !important; }

/* ── Expander ── */
details { border: 1px solid #131313 !important; border-radius: 2px !important; background: #070707 !important; }
details summary { color: #C9A84C !important; font-size: 0.7rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }

/* ── Alerts ── */
[data-testid="stAlert"] { background: #070707 !important; border-radius: 2px !important; border-left: 2px solid #C9A84C !important; }
[data-testid="stAlert"] p { color: #666 !important; font-size: 0.76rem !important; }

/* ── Misc ── */
hr { border-color: #131313 !important; margin: 1.5rem 0 !important; }
[data-testid="stDataFrame"] { border: 1px solid #131313 !important; border-radius: 2px !important; }
[data-testid="stFileUploadDropzone"] { background: #070707 !important; border-color: #1C1C1C !important; border-radius: 2px !important; }
code { background: #080808 !important; color: #C9A84C !important; border-radius: 2px !important; }
pre { background: #070707 !important; border: 1px solid #131313 !important; border-radius: 2px !important; }
.stCaption p { color: #222 !important; font-size: 0.62rem !important; letter-spacing: 0.06em !important; }
.block-container { padding: 0 2.5rem 2.5rem !important; max-width: 1200px !important; }

/* ── Hero image containers ── */
.kw-hero {
    position: relative; width: 100%; overflow: hidden;
    border-radius: 2px; margin-bottom: 2rem;
}
.kw-hero img {
    width: 100%; height: 100%; object-fit: cover; display: block;
    animation: kwFadeScale 1.6s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.kw-hero-grad {
    position: absolute; inset: 0; pointer-events: none;
    background: linear-gradient(to bottom, rgba(12,12,12,0.05) 35%, rgba(12,12,12,0.65) 78%, #0C0C0C 100%);
}

.kw-hero-col {
    position: relative; width: 100%; overflow: hidden; border-radius: 2px;
}
.kw-hero-col img {
    width: 100%; height: 100%; object-fit: cover; display: block;
    animation: kwFadeScale 1.6s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.kw-hero-col-grad {
    position: absolute; inset: 0; pointer-events: none;
    background: linear-gradient(to bottom, transparent 45%, rgba(12,12,12,0.75) 85%, #0C0C0C 100%);
}

/* ── Animations ── */
@keyframes kwFadeScale {
    from { opacity: 0; transform: scale(1.07); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes kwPageIn {
    from { opacity: 0; transform: translateY(7px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Page-level fade-in (targets the block container inner div) */
section.main > div { animation: kwPageIn 0.4s ease-out both; }

/* ── Nav active chip ── */
.kw-nav-active {
    text-align: center;
    padding: 0.55rem 0.1rem;
    border-bottom: 1px solid #C9A84C;
}
.kw-nav-active-num {
    font-size: 0.58rem; color: #C9A84C;
    letter-spacing: 0.14em; font-family: 'Inter', sans-serif;
    text-transform: uppercase;
}
.kw-nav-active-label {
    font-size: 0.62rem; color: #C9A84C;
    margin-top: 0.12rem; font-family: 'Inter', sans-serif;
}

/* ── Nav separator ── */
.kw-nav-sep { width: 100%; height: 1px; background: #111; margin: 0 0 2rem 0; }
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
    ("assets",   "Financials"),
    ("risk",     "Dashboard"),
    ("draft",    "Draft"),
    ("attorney", "Attorney"),
    ("ref",      "Reference"),
]
STEP_KEYS = [s[0] for s in STEPS]

def step_done(key):
    return {
        "setup":    st.session_state.case_created,
        "partner":  st.session_state.partner_invited,
        "qa":       bool(st.session_state.partner_a),
        "qb":       bool(st.session_state.partner_b),
        "assets":   bool(st.session_state.assets_a or st.session_state.assets_b),
        "risk":     bool(st.session_state.goals_a and st.session_state.goals_b),
        "draft":    bool(st.session_state.partner_a and st.session_state.partner_b),
    }.get(key, True)

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
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                icon = "✓" if is_done else num
                if st.button(f"{icon}\n{label}", key=f"nav_{key}", use_container_width=True):
                    go(key)
    st.markdown('<div class="kw-nav-sep"></div>', unsafe_allow_html=True)


# ── Sidebar: Status Panel ─────────────────────────────────────────────────
def render_sidebar():
    st.sidebar.markdown(
        '<p style="font-size:0.55rem;letter-spacing:0.3em;text-transform:uppercase;color:#222;margin-bottom:0.1rem">Est. 2024</p>',
        unsafe_allow_html=True,
    )
    st.sidebar.title("KnotWise")
    st.sidebar.caption("AI Prenup Preparation Assistant")
    st.sidebar.divider()

    score, _ = completion_score()
    risk, _ = risk_level(score)
    st.sidebar.metric("Readiness", f"{score}/100")
    st.sidebar.progress(score / 100)
    st.sidebar.markdown('<p style="font-size:0.6rem;color:#C9A84C;letter-spacing:0.1em;margin:0.2rem 0 0.8rem 0">' + risk + ' risk</p>', unsafe_allow_html=True)

    st.sidebar.divider()
    status_items = [
        ("Case Setup",       "setup"),
        ("Partner Invited",  "partner"),
        ("Partner A",        "qa"),
        ("Partner B",        "qb"),
        ("Assets & Debts",   "assets"),
        ("Preferences Set",  "risk"),
    ]
    for label, key in status_items:
        done = step_done(key)
        color = "#C9A84C" if done else "#1E1E1E"
        icon  = "●" if done else "○"
        st.sidebar.markdown(
            f'<p style="color:{color};font-size:0.68rem;margin:0.3rem 0;letter-spacing:0.04em">{icon}&nbsp; {label}</p>',
            unsafe_allow_html=True,
        )
    st.sidebar.divider()
    st.sidebar.caption("Academic prototype only. Not legal advice.")


# ── Image Helpers ─────────────────────────────────────────────────────────
def _b64(filename):
    p = Path("images") / filename
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else None

def hero_full(filename, height="400px", pos="center 30%"):
    data = _b64(filename)
    if not data:
        return
    st.markdown(
        f'<div class="kw-hero" style="height:{height}">'
        f'<img src="data:image/jpeg;base64,{data}" style="object-position:{pos}" />'
        f'<div class="kw-hero-grad"></div></div>',
        unsafe_allow_html=True,
    )

def hero_col(filename, height="500px", pos="center 25%"):
    data = _b64(filename)
    if not data:
        return
    st.markdown(
        f'<div class="kw-hero-col" style="height:{height}">'
        f'<img src="data:image/jpeg;base64,{data}" style="object-position:{pos}" />'
        f'<div class="kw-hero-col-grad"></div></div>',
        unsafe_allow_html=True,
    )


# ── Helper Functions ──────────────────────────────────────────────────────
def money(v):
    try:
        return f"${float(v):,.2f}"
    except Exception:
        return "$0.00"

def completion_score():
    score = 0
    explanation = []

    checks = [
        (st.session_state.case_created,          10, "Case setup completed",                    "Case setup missing"),
        (st.session_state.partner_invited,        10, "Partner invitation prepared",             "Partner invitation not prepared"),
        (bool(st.session_state.partner_a),        10, "Partner A questionnaire completed",       "Partner A questionnaire missing"),
        (bool(st.session_state.partner_b),        10, "Partner B questionnaire completed",       "Partner B questionnaire missing"),
        (bool(st.session_state.assets_a and st.session_state.assets_b), 15, "Both partners disclosed assets", "Asset disclosure incomplete"),
        (bool(st.session_state.debts_a and st.session_state.debts_b),   10, "Both partners disclosed debts",  "Debt disclosure incomplete"),
        (bool(st.session_state.goals_a and st.session_state.goals_b),   15, "Both partners selected preferences", "Partner preference responses incomplete"),
        (len(st.session_state.uploaded_docs) >= 2, 10, "Supporting documents uploaded",          "Supporting documents limited or missing"),
    ]
    for condition, pts, pos_msg, neg_msg in checks:
        if condition:
            score += pts
            explanation.append(f"{pos_msg} (+{pts})")
        else:
            explanation.append(f"{neg_msg} (+0)")

    conflicts = detect_conflicts()
    if len(conflicts) == 0 and st.session_state.goals_a and st.session_state.goals_b:
        score += 10
        explanation.append("No major preference conflicts detected (+10)")
    elif len(conflicts) > 0:
        explanation.append(f"{len(conflicts)} preference conflict(s) detected (+0)")
    else:
        explanation.append("Conflict check pending (+0)")

    return min(score, 100), explanation

def risk_level(score):
    if score >= 80: return "Low",    "Strong preparation"
    if score >= 55: return "Medium", "Needs attorney clarification"
    return "High", "Missing key information"

def detect_conflicts():
    conflicts, a, b = [], st.session_state.goals_a, st.session_state.goals_b
    for key, label in [
        ("premarital_assets", "Premarital asset treatment"),
        ("future_income",     "Future income treatment"),
        ("business_growth",   "Business growth / appreciation"),
        ("debt_responsibility","Debt responsibility"),
        ("spousal_support",   "Spousal support"),
        ("inheritance",       "Inheritance and family gifts"),
        ("home_purchase",     "Future home purchase"),
    ]:
        if a.get(key) and b.get(key) and a[key] != b[key]:
            conflicts.append({
                "Topic":          label,
                "Partner A":      a[key],
                "Partner B":      b[key],
                "Severity":       "High" if key in ("spousal_support", "business_growth", "premarital_assets") else "Medium",
                "Recommendation": "Discuss before attorney review.",
            })
    return conflicts

def missing_documents():
    docs = {d["type"] for d in st.session_state.uploaded_docs}
    required = ["Government ID", "Bank/Investment Statements", "Debt Statements",
                "Real Estate Documents", "Business Ownership Documents", "Retirement Account Statements"]
    return [r for r in required if r not in docs]

def build_asset_df():
    rows = []
    for p, lst in [("Partner A", st.session_state.assets_a), ("Partner B", st.session_state.assets_b)]:
        for a in lst:
            rows.append({"Owner": p, "Type": a.get("asset_type"), "Description": a.get("description"),
                         "Location": a.get("location"), "Value": a.get("value"), "Preference": a.get("preference")})
    return pd.DataFrame(rows)

def build_debt_df():
    rows = []
    for p, lst in [("Partner A", st.session_state.debts_a), ("Partner B", st.session_state.debts_b)]:
        for d in lst:
            rows.append({"Owner": p, "Type": d.get("debt_type"), "Description": d.get("description"),
                         "Balance": d.get("balance"), "Preference": d.get("preference")})
    return pd.DataFrame(rows)

def generate_draft_preview():
    case = st.session_state.case
    pa, pb = st.session_state.partner_a, st.session_state.partner_b
    a_name = pa.get("name", "Partner A")
    b_name = pb.get("name", "Partner B")
    wedding_date = case.get("wedding_date", "[Wedding Date]")
    residence    = case.get("future_residence", "[Future Residence]")
    return f"""PRENUPTIAL AGREEMENT — PREPARATION DRAFT
For Attorney Review Only — Not a Final Legal Document
{'─' * 60}

1. BACKGROUND
{a_name} and {b_name} are planning to marry on or around {wedding_date}. The couple expects to reside in {residence}. Each partner has provided preliminary financial disclosures and preferences regarding separate property, marital property, debts, income, and future financial responsibilities.

2. SEPARATE PROPERTY
Property owned by either partner before marriage may be identified as separate property, subject to attorney review and complete disclosure schedules.

3. MARITAL PROPERTY
The couple should determine whether income, assets, or appreciation earned during marriage will be treated as shared marital property or separately owned property.

4. DEBTS
Each partner should disclose all premarital debts. The agreement may specify whether premarital debts remain the responsibility of the partner who incurred them.

5. BUSINESS OWNERSHIP
Any business interests disclosed by either partner should be separately reviewed to determine whether ownership, future growth, dividends, or appreciation will remain separate or be shared.

6. INHERITANCE AND FAMILY GIFTS
The couple should clarify whether inheritance, gifts, and family property will remain separate property.

7. SPOUSAL SUPPORT
The couple should discuss whether spousal support will be waived, limited, or reserved for attorney review based on future circumstances.

8. ATTORNEY REVIEW
This draft preview must be reviewed by qualified counsel before execution. Each partner should have adequate time to review and ask questions before signing.
"""

def generate_summary_text():
    score, explanation = completion_score()
    risk, label = risk_level(score)
    conflicts, missing = detect_conflicts(), missing_documents()
    asset_df, debt_df = build_asset_df(), build_debt_df()
    case, pa, pb = st.session_state.case, st.session_state.partner_a, st.session_state.partner_b

    lines = [
        "# KnotWise — Attorney-Ready Prenup Preparation Summary", "",
        "## Important Disclaimer",
        "This document is an AI-assisted preparation summary for academic demonstration purposes. It is not legal advice and should be reviewed by a licensed attorney before use.", "",
        "## Case Overview",
        f"- Couple/Case Name: {case.get('case_name', 'Not provided')}",
        f"- Expected Wedding Date: {case.get('wedding_date', 'Not provided')}",
        f"- Current Residence: {case.get('current_residence', 'Not provided')}",
        f"- Expected Residence After Marriage: {case.get('future_residence', 'Not provided')}",
        f"- Jurisdictions/Countries Involved: {case.get('jurisdictions', 'Not provided')}", "",
        "## Partner Profiles",
        f"### Partner A: {pa.get('name', 'Not provided')}",
        f"- Citizenship: {pa.get('citizenship', 'Not provided')}",
        f"- Status: {pa.get('immigration_status', 'Not provided')}",
        f"- Annual Income: {money(pa.get('income', 0))}", "",
        f"### Partner B: {pb.get('name', 'Not provided')}",
        f"- Citizenship: {pb.get('citizenship', 'Not provided')}",
        f"- Status: {pb.get('immigration_status', 'Not provided')}",
        f"- Annual Income: {money(pb.get('income', 0))}", "",
        f"## Readiness Score: {score}/100 — {risk} — {label}",
    ] + [f"- {e}" for e in explanation] + ["", "## Missing Documents"] + \
        [f"- {i}" for i in (missing or ["No major missing documents identified."])] + \
        ["", "## Partner Preference Conflicts"] + \
        ([f"- {c['Topic']}: Partner A: '{c['Partner A']}' | Partner B: '{c['Partner B']}' | Severity: {c['Severity']}" for c in conflicts]
         if conflicts else ["- No major conflicts detected."]) + \
        ["", "## Asset Disclosure"] + \
        ([f"- {r['Owner']} | {r['Type']} | {r['Description']} | {r['Location']} | {money(r['Value'])} | {r['Preference']}"
          for _, r in asset_df.iterrows()] if not asset_df.empty else ["- No assets disclosed."]) + \
        ["", "## Debt Disclosure"] + \
        ([f"- {r['Owner']} | {r['Type']} | {r['Description']} | Balance: {money(r['Balance'])} | {r['Preference']}"
          for _, r in debt_df.iterrows()] if not debt_df.empty else ["- No debts disclosed."]) + \
        ["", "## Attorney Discussion Questions",
         "- Are all premarital assets fully disclosed and properly valued?",
         "- Should future appreciation of premarital property remain separate or become marital property?",
         "- How should business ownership and growth during marriage be treated?",
         "- How should debts incurred before and during marriage be handled?",
         "- Should spousal support be waived, limited, or reserved for future determination?",
         "- Are there cross-border assets, immigration issues, or family obligations requiring special review?",
         "", "## Draft Preview", generate_draft_preview()]
    return "\n".join(lines)

def downloadable_text(text):
    return BytesIO(text.encode("utf-8"))


# ── Partner Form ──────────────────────────────────────────────────────────
def partner_form(label, state_key):
    existing = st.session_state[state_key]
    with st.form(f"{state_key}_form"):
        col1, col2 = st.columns(2)
        with col1:
            name  = st.text_input(f"{label} Name",  value=existing.get("name", ""))
            citizenship = st.text_input("Citizenship", value=existing.get("citizenship", ""))
            income = st.number_input("Approximate Annual Income ($)", min_value=0.0, step=1000.0, value=float(existing.get("income", 0.0)))
        with col2:
            email = st.text_input(f"{label} Email", value=existing.get("email", ""))
            statuses = ["U.S. Citizen", "Green Card / Permanent Resident", "F-1", "H-1B", "L-1", "Canadian PR", "Other", "Prefer not to say"]
            existing_status = existing.get("immigration_status", "")
            idx = statuses.index(existing_status) if existing_status in statuses else 0
            immigration_status = st.selectbox("Immigration / Residency Status", statuses, index=idx)
            notes = st.text_area("Additional Notes", value=existing.get("notes", ""), height=82)
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            owns_business    = st.checkbox("Owns a business or equity interest", value=existing.get("owns_business", False))
            owns_real_estate = st.checkbox("Owns real estate", value=existing.get("owns_real_estate", False))
        with c2:
            has_children_prior = st.checkbox("Has children from prior relationship", value=existing.get("has_children_prior", False))
            supports_family    = st.checkbox("Financially supports family members",  value=existing.get("supports_family", False))
        st.markdown("---")
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.2em;text-transform:uppercase;color:#C9A84C;margin-bottom:0.8rem">Prenup Preferences</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            premarital_assets   = st.selectbox("Premarital assets",          ["Keep separate", "Share after marriage", "Discuss with attorney"], key=f"{state_key}_pre")
            future_income       = st.selectbox("Future income during marriage", ["Shared marital property", "Separate property", "Discuss with attorney"], key=f"{state_key}_inc")
            business_growth     = st.selectbox("Business growth / appreciation", ["Keep separate", "Share appreciation", "Discuss with attorney"], key=f"{state_key}_biz")
            debt_responsibility = st.selectbox("Premarital debts",            ["Each partner responsible for own debts", "Shared responsibility", "Discuss with attorney"], key=f"{state_key}_dbt")
        with c2:
            spousal_support = st.selectbox("Spousal support", ["Waived", "Limited", "Reserved for future review", "Discuss with attorney"], key=f"{state_key}_sp")
            inheritance     = st.selectbox("Inheritance and family gifts",    ["Keep separate", "Share if used by couple", "Discuss with attorney"], key=f"{state_key}_inh")
            home_purchase   = st.selectbox("Future home purchase",            ["Shared property", "Based on contribution", "Discuss with attorney"], key=f"{state_key}_hm")
        submitted = st.form_submit_button(f"Save {label} Questionnaire")

    if submitted:
        st.session_state[state_key] = {
            "name": name, "email": email, "citizenship": citizenship,
            "immigration_status": immigration_status, "income": income,
            "owns_business": owns_business, "owns_real_estate": owns_real_estate,
            "has_children_prior": has_children_prior, "supports_family": supports_family,
            "notes": notes,
        }
        goal_key = "goals_a" if state_key == "partner_a" else "goals_b"
        st.session_state[goal_key] = {
            "premarital_assets": premarital_assets, "future_income": future_income,
            "business_growth": business_growth, "debt_responsibility": debt_responsibility,
            "spousal_support": spousal_support, "inheritance": inheritance,
            "home_purchase": home_purchase,
        }
        st.success(f"{label} questionnaire saved.")


# ── UI helpers ────────────────────────────────────────────────────────────
def eyebrow(text):
    st.markdown(f'<p style="font-size:0.6rem;letter-spacing:0.28em;text-transform:uppercase;color:#C9A84C;margin-bottom:0.15rem">{text}</p>', unsafe_allow_html=True)

def gold_rule():
    st.markdown('<div style="width:34px;height:1px;background:#C9A84C;margin:0.4rem 0 1.3rem 0"></div>', unsafe_allow_html=True)

def li(text):
    st.markdown(f'<p style="color:#2E2E2E;font-size:0.78rem;margin:0.22rem 0;line-height:1.6">— {text}</p>', unsafe_allow_html=True)


# ── Render ────────────────────────────────────────────────────────────────
render_sidebar()
render_nav()
page = st.session_state.page


# ── 1. WELCOME ────────────────────────────────────────────────────────────
if page == "welcome":
    hero_full("NYC-WEDDING-PHOTOGRAPHER-1024x683.jpg", height="420px", pos="center 40%")
    eyebrow("AI Prenup Preparation")
    st.title("KnotWise")
    gold_rule()
    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        st.markdown("KnotWise helps couples complete structured prenup questionnaires, organize financial disclosures, compare partner preferences, identify conflicts, and generate an attorney-ready preparation summary.")
        st.markdown("---")
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.18em;text-transform:uppercase;color:#333;margin-bottom:0.6rem">What this prototype covers</p>', unsafe_allow_html=True)
        for item in [
            "Couple case creation and partner invitation workflow",
            "Partner A and B questionnaires with financial disclosures",
            "Asset and debt disclosure with preference tracking",
            "Automated conflict detection between partner responses",
            "Prenup readiness score with explainable breakdown",
            "AI-assisted draft preview and attorney-ready export",
            "Mock premium attorney review upgrade",
        ]:
            li(item)
    with col2:
        score, _ = completion_score()
        st.metric("Prototype Stack", "Streamlit + Python")
        st.metric("Primary Value", "Lower legal prep time")
        st.metric("User Flow", "2-partner intake")
        st.metric("Current Readiness", f"{score}/100")
    st.markdown('<p style="font-size:0.62rem;color:#1E1E1E;border-top:1px solid #111;padding-top:1rem;margin-top:2rem;letter-spacing:0.04em;line-height:1.8">This prototype is designed for a class project and is not legal advice. It does not replace attorney review.</p>', unsafe_allow_html=True)


# ── 2. CASE SETUP ─────────────────────────────────────────────────────────
elif page == "setup":
    col_img, col_head = st.columns([2, 3], gap="large")
    with col_img:
        hero_col("7d9337fdbff13df38d6ccd18b2a9ec7b.jpg", height="480px", pos="center 50%")
    with col_head:
        eyebrow("Step 01 of 07")
        st.title("Case Setup")
        gold_rule()
        st.markdown("Establish the jurisdictional context and basic case information for your prenup preparation.")

        with st.form("case_setup_form"):
            c1, c2 = st.columns(2)
            with c1:
                case_name         = st.text_input("Case / Couple Name",                value=st.session_state.case.get("case_name", ""))
                current_residence = st.text_input("Current Residence",                 value=st.session_state.case.get("current_residence", ""))
                jurisdictions     = st.text_input("Jurisdictions / Countries Involved", value=st.session_state.case.get("jurisdictions", ""))
            with c2:
                saved_date   = st.session_state.case.get("wedding_date")
                default_date = date.today()
                if isinstance(saved_date, str):
                    try:
                        from datetime import datetime
                        default_date = datetime.strptime(saved_date, "%Y-%m-%d").date()
                    except Exception:
                        pass
                wedding_date      = st.date_input("Expected Wedding Date", value=default_date)
                future_residence  = st.text_input("Expected Residence After Marriage",  value=st.session_state.case.get("future_residence", ""))
                cross_border      = st.checkbox("Involves cross-border assets, immigration, or multiple countries", value=st.session_state.case.get("cross_border", False))
            submitted = st.form_submit_button("Save Case Setup")

        if submitted:
            st.session_state.case = {
                "case_name": case_name, "wedding_date": str(wedding_date),
                "current_residence": current_residence, "future_residence": future_residence,
                "jurisdictions": jurisdictions, "cross_border": cross_border,
            }
            st.session_state.case_created = True
            st.success("Case setup saved.")

        if st.session_state.case_created:
            st.markdown("---")
            st.markdown('<p style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#333;margin-bottom:0.4rem">Current Case</p>', unsafe_allow_html=True)
            st.json(st.session_state.case)


# ── 3. ADD PARTNER ────────────────────────────────────────────────────────
elif page == "partner":
    col_img, col_head = st.columns([1, 2], gap="large")
    with col_img:
        hero_col("images (1).jpeg", height="520px", pos="center 35%")
    with col_head:
        eyebrow("Step 02 of 07")
        st.title("Add Partner")
        gold_rule()
        st.markdown("Prepare a partner invitation for the prenup preparation workflow.")
        st.markdown("---")
        st.markdown('<p style="font-size:0.6rem;letter-spacing:0.16em;text-transform:uppercase;color:#333;margin-bottom:0.5rem">Partner Workflow</p>', unsafe_allow_html=True)
        for i, step in enumerate(["Partner A creates the case", "Partner A invites Partner B", "Partner B completes a separate questionnaire", "Both responses are compared", "Conflicts and missing information are flagged", "A lawyer-ready summary is generated"], 1):
            st.markdown(f'<p style="color:#2A2A2A;font-size:0.76rem;margin:0.2rem 0">{i}.&nbsp; {step}</p>', unsafe_allow_html=True)

        st.markdown("---")
        with st.form("partner_invite_form"):
            c1, c2 = st.columns(2)
            with c1:
                invite_email = st.text_input("Partner Email Address", value=st.session_state.invite_email)
                partner_name = st.text_input("Partner Name",          value=st.session_state.partner_b.get("name", ""))
            with c2:
                access_level = st.selectbox("Partner Access Level", ["Complete questionnaire only", "View shared summary after both submit", "Full shared case access"])
                message = st.text_area("Invitation Message", height=88, value="Hi, I invited you to complete your section of our prenup preparation questionnaire in KnotWise.")
            sent = st.form_submit_button("Prepare Partner Invitation")

        if sent:
            st.session_state.partner_invited = True
            st.session_state.invite_email = invite_email
            if partner_name:
                st.session_state.partner_b["name"] = partner_name
            st.success("Partner invitation prepared. In production, this would send an email invitation link.")
            st.code(f"To: {invite_email}\nSubject: Invitation to complete KnotWise prenup questionnaire\n\n{message}\n\nAccess Level: {access_level}", language="text")


# ── 4. PARTNER A ──────────────────────────────────────────────────────────
elif page == "qa":
    col_img, col_head = st.columns([1, 2], gap="large")
    with col_img:
        hero_col("106ae0c3ff0dd68d593c41d7bf297240.jpg", height="460px", pos="center 20%")
    with col_head:
        eyebrow("Step 03 of 07")
        st.title("Partner A Questionnaire")
        gold_rule()
        st.markdown("Complete your financial profile and prenup preference selections.")

    st.markdown("---")
    partner_form("Partner A", "partner_a")


# ── 5. PARTNER B ──────────────────────────────────────────────────────────
elif page == "qb":
    col_img, col_head = st.columns([1, 2], gap="large")
    with col_img:
        hero_col("_MG_4725 copy.jpg", height="460px", pos="center 40%")
    with col_head:
        eyebrow("Step 04 of 07")
        st.title("Partner B Questionnaire")
        gold_rule()
        if not st.session_state.partner_invited:
            st.warning("Partner has not been invited yet. Go to 'Invite' first for the intended workflow.")
        else:
            st.markdown("Partner invitation prepared. Complete the questionnaire below.")

    st.markdown("---")
    partner_form("Partner B", "partner_b")


# ── 6. ASSETS & DEBTS ─────────────────────────────────────────────────────
elif page == "assets":
    hero_full("img_7973.jpg", height="360px", pos="center 15%")
    eyebrow("Step 05 of 07")
    st.title("Assets, Debts & Documents")
    gold_rule()

    tab1, tab2, tab3 = st.tabs(["Add Asset", "Add Debt", "Upload Documents"])

    with tab1:
        with st.form("asset_form"):
            c1, c2 = st.columns(2)
            with c1:
                owner      = st.selectbox("Owner",      ["Partner A", "Partner B"])
                asset_type = st.selectbox("Asset Type", ["Bank Account", "Investment", "Retirement Account", "Real Estate", "Business", "Vehicle", "Inheritance", "Other"])
                description = st.text_input("Description")
            with c2:
                location   = st.text_input("Country / State", value="United States")
                value      = st.number_input("Estimated Value ($)", min_value=0.0, step=1000.0)
                preference = st.selectbox("Preferred Treatment", ["Separate property", "Shared property", "Attorney review needed"])
            submitted = st.form_submit_button("Add Asset")
        if submitted:
            a = {"asset_type": asset_type, "description": description, "location": location, "value": value, "preference": preference}
            (st.session_state.assets_a if owner == "Partner A" else st.session_state.assets_b).append(a)
            st.success("Asset added.")
        df = build_asset_df()
        st.dataframe(df, use_container_width=True) if not df.empty else st.caption("No assets added yet.")

    with tab2:
        with st.form("debt_form"):
            c1, c2 = st.columns(2)
            with c1:
                owner     = st.selectbox("Debt Owner", ["Partner A", "Partner B"])
                debt_type = st.selectbox("Debt Type",  ["Student Loan", "Credit Card", "Mortgage", "Personal Loan", "Business Debt", "Vehicle Loan", "Other"])
                description = st.text_input("Debt Description")
            with c2:
                balance    = st.number_input("Debt Balance ($)", min_value=0.0, step=500.0)
                preference = st.selectbox("Responsibility Preference", ["Owner remains responsible", "Shared responsibility", "Attorney review needed"])
            submitted = st.form_submit_button("Add Debt")
        if submitted:
            d = {"debt_type": debt_type, "description": description, "balance": balance, "preference": preference}
            (st.session_state.debts_a if owner == "Partner A" else st.session_state.debts_b).append(d)
            st.success("Debt added.")
        df = build_debt_df()
        st.dataframe(df, use_container_width=True) if not df.empty else st.caption("No debts added yet.")

    with tab3:
        st.caption("Files are not permanently stored. Document type and filename are recorded for demonstration purposes.")
        with st.form("doc_form"):
            c1, c2 = st.columns(2)
            with c1:
                doc_type = st.selectbox("Document Type", ["Government ID", "Bank/Investment Statements", "Debt Statements", "Real Estate Documents", "Business Ownership Documents", "Retirement Account Statements", "Other"])
            with c2:
                uploaded_file = st.file_uploader("Upload document", type=["png", "jpg", "jpeg", "pdf"])
            submitted = st.form_submit_button("Add Document")
        if submitted:
            if uploaded_file:
                st.session_state.uploaded_docs.append({"type": doc_type, "filename": uploaded_file.name, "size": uploaded_file.size})
                st.success("Document metadata saved.")
            else:
                st.error("Please upload a file before submitting.")
        if st.session_state.uploaded_docs:
            st.dataframe(pd.DataFrame(st.session_state.uploaded_docs), use_container_width=True)
        else:
            st.caption("No documents added yet.")


# ── 7. RISK DASHBOARD ─────────────────────────────────────────────────────
elif page == "risk":
    hero_full("black-white-shot-engaged-couple.jpg", height="360px", pos="center 15%")
    eyebrow("Step 06 of 07")
    st.title("Risk Dashboard")
    gold_rule()

    score, explanation = completion_score()
    risk, label = risk_level(score)
    conflicts   = detect_conflicts()
    missing     = missing_documents()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Readiness Score", f"{score}/100")
    c2.metric("Risk Level",      risk)
    c3.metric("Conflicts",       len(conflicts))
    c4.metric("Missing Docs",    len(missing))

    st.markdown(f'<p style="font-size:0.76rem;color:#C9A84C;letter-spacing:0.08em;margin:1rem 0 0.5rem 0">{label}</p>', unsafe_allow_html=True)
    st.progress(score / 100)
    st.markdown("---")

    col_l, col_r = st.columns(2, gap="large")
    with col_l:
        with st.expander("Score Breakdown", expanded=True):
            for item in explanation:
                color = "#C9A84C" if "(+0)" not in item else "#222"
                st.markdown(f'<p style="color:{color};font-size:0.76rem;margin:0.22rem 0">— {item}</p>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<p style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#333;margin-bottom:0.5rem">Missing Documents</p>', unsafe_allow_html=True)
        if missing:
            for doc in missing:
                st.markdown(f'<p style="color:#222;font-size:0.76rem;margin:0.2rem 0">— {doc}</p>', unsafe_allow_html=True)
        else:
            st.success("All major document categories present.")
    with col_r:
        st.markdown('<p style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#333;margin-bottom:0.5rem">Partner Preference Conflicts</p>', unsafe_allow_html=True)
        if conflicts:
            st.dataframe(pd.DataFrame(conflicts), use_container_width=True)
        else:
            st.success("No major conflicts detected based on current responses.")

    asset_df, debt_df = build_asset_df(), build_debt_df()
    if not asset_df.empty or not debt_df.empty:
        st.markdown("---")
        st.markdown('<p style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#333;margin-bottom:0.5rem">Financial Disclosure Overview</p>', unsafe_allow_html=True)
        if not asset_df.empty:
            st.caption("Assets")
            st.dataframe(asset_df, use_container_width=True)
        if not debt_df.empty:
            st.caption("Debts")
            st.dataframe(debt_df, use_container_width=True)


# ── 8. DRAFT PREVIEW ─────────────────────────────────────────────────────
elif page == "draft":
    col_img, col_head = st.columns([1, 2], gap="large")
    with col_img:
        hero_col("images.jpeg", height="460px", pos="center 30%")
    with col_head:
        eyebrow("Step 07 of 07")
        st.title("Draft Preview")
        gold_rule()
        st.markdown("AI-assisted preparation draft for attorney review only. This is not a final legal document.")
        st.markdown("---")
        summary_text = generate_summary_text()
        st.download_button(
            label="Download Attorney-Ready Summary (.md)",
            data=downloadable_text(summary_text),
            file_name="knotwise_attorney_summary.md",
            mime="text/markdown",
        )
    st.markdown("---")
    st.text_area("Draft Preview", value=generate_draft_preview(), height=500)


# ── 9. ATTORNEY REVIEW ────────────────────────────────────────────────────
elif page == "attorney":
    col_img, col_head = st.columns([2, 3], gap="large")
    with col_img:
        hero_col("7d9337fdbff13df38d6ccd18b2a9ec7b.jpg", height="440px", pos="center 50%")
    with col_head:
        eyebrow("Premium")
        st.title("Attorney Review Upgrade")
        gold_rule()
        st.markdown("Connect your completed preparation package with a licensed attorney for final review, jurisdiction-specific feedback, and execution support.")

    st.markdown("---")
    c1, c2, c3 = st.columns(3, gap="large")
    for col, tier, price, items in [
        (c1, "Preparation Package", "$49–$99",      ["Complete questionnaire summary", "Draft preview", "Missing document checklist", "Conflict report"]),
        (c2, "Attorney Review",     "$499–$1,500",   ["Attorney reviews draft", "Revisions included", "Jurisdiction-specific feedback", "Signing guidance"]),
        (c3, "Concierge Package",   "$2,000+",       ["Two-attorney coordination", "Partner-specific review", "Notary and signing workflow", "Final execution checklist"]),
    ]:
        with col:
            st.markdown(f'<p style="font-size:0.6rem;letter-spacing:0.2em;text-transform:uppercase;color:#333;margin-bottom:0.3rem">{tier}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-family:\'Playfair Display\',serif;font-size:1.8rem;color:#C9A84C;margin:0.2rem 0 1rem 0">{price}</p>', unsafe_allow_html=True)
            for item in items:
                li(item)
    st.markdown("---")
    st.caption("Production version could integrate payments, attorney marketplace, e-signature, and notarization providers.")


# ── 10. REFERENCE ─────────────────────────────────────────────────────────
elif page == "ref":
    eyebrow("Academic Reference")
    st.title("Project Requirements Alignment")
    gold_rule()
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<p style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#333;margin-bottom:0.5rem">Business Problem</p>', unsafe_allow_html=True)
        st.markdown("Prenup preparation is expensive and inefficient because couples enter the legal process without organized disclosures, aligned preferences, or complete documentation before meeting attorneys.")
        st.markdown("---")
        st.markdown('<p style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#333;margin-bottom:0.5rem">Functional Requirements</p>', unsafe_allow_html=True)
        for item in ["Create case and invite partner", "Partner A and B questionnaires", "Asset and debt disclosure", "Supporting document upload metadata", "Conflict detection between partner preferences", "Prenup readiness score with breakdown", "Draft preview generation", "Lawyer-ready summary export", "Mock attorney review upgrade"]:
            li(item)
        st.markdown("---")
        st.markdown('<p style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#333;margin-bottom:0.5rem">Data Entities</p>', unsafe_allow_html=True)
        for item in ["Couple Case", "Partner Profile", "Assets", "Debts", "Prenup Goals", "Uploaded Documents", "Conflict Flags", "Readiness Score", "Draft Summary"]:
            li(item)
    with c2:
        st.markdown('<p style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#333;margin-bottom:0.5rem">Application Architecture</p>', unsafe_allow_html=True)
        st.code("User\n→ Streamlit UI\n→ Questionnaire Forms\n→ Session / Data Layer\n→ Scoring Engine\n→ Conflict Engine\n→ Draft Generator\n→ Export / Attorney Review", language="text")
        st.markdown("---")
        st.markdown('<p style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#333;margin-bottom:0.5rem">Non-Functional Requirements</p>', unsafe_allow_html=True)
        for item in ["Pages load within 3 seconds", "Sensitive financial information protected", "Easy to use for non-technical users", "Clear disclaimers: drafts require attorney review", "Role-based access: Partner A, B, attorney, admin", "Audit logs for key actions", "Explainable scoring logic", "Scalable for attorney marketplace integration"]:
            li(item)
