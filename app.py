
import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

st.set_page_config(
    page_title="KnotWise | AI Prenup Preparation",
    page_icon="💍",
    layout="wide",
)

# ── Premium Dark Theme ────────────────────────────────────────────────────
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
    background: #090909 !important;
    border-right: 1px solid #1A1A1A !important;
}

h1, h2, h3, h4 {
    font-family: 'Playfair Display', serif !important;
    color: #F0EBE3 !important;
    font-weight: 400 !important;
}
h1 { font-size: 2.7rem !important; line-height: 1.18 !important; }
h2 { font-size: 1.75rem !important; }
h3 { font-size: 1.1rem !important; }

p, li { color: #888 !important; line-height: 1.75 !important; }

/* Sidebar */
section[data-testid="stSidebar"] h2 {
    font-size: 1.5rem !important; color: #F0EBE3 !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] small {
    color: #555 !important; font-size: 0.72rem !important; letter-spacing: 0.06em;
}
.stRadio > div { gap: 0.15rem !important; }
.stRadio label {
    font-size: 0.7rem !important; letter-spacing: 0.1em !important;
    color: #444 !important; text-transform: uppercase !important;
    padding: 0.4rem 0.2rem !important;
}
.stRadio [data-testid="stMarkdownContainer"] p { color: #555 !important; }

/* Metrics */
[data-testid="metric-container"] {
    background: #101010 !important;
    border: 1px solid #1C1C1C !important;
    border-radius: 2px !important;
    padding: 1.3rem 1.1rem !important;
}
[data-testid="stMetricLabel"] p {
    color: #444 !important; font-size: 0.62rem !important;
    letter-spacing: 0.18em !important; text-transform: uppercase !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    color: #C9A84C !important; font-size: 2rem !important;
}

/* Inputs */
[data-baseweb="input"] > div {
    background: #0E0E0E !important; border-color: #222 !important; border-radius: 2px !important;
}
[data-baseweb="textarea"] {
    background: #0E0E0E !important; border-color: #222 !important; border-radius: 2px !important;
}
input, textarea { color: #D4CFC8 !important; font-family: 'Inter', sans-serif !important; }
[data-baseweb="select"] > div {
    background: #0E0E0E !important; border-color: #222 !important;
    border-radius: 2px !important; color: #D4CFC8 !important;
}
[data-baseweb="menu"] { background: #161616 !important; border: 1px solid #252525 !important; }
[data-baseweb="menu"] li { background: #161616 !important; color: #D4CFC8 !important; }
[data-baseweb="menu"] li:hover { background: #1E1E1E !important; }

/* Labels */
label, .stSelectbox label, .stTextInput label,
.stNumberInput label, .stTextArea label {
    color: #555 !important; font-size: 0.68rem !important;
    letter-spacing: 0.1em !important; text-transform: uppercase !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stCheckbox"] label span { color: #888 !important; font-size: 0.78rem !important; }

/* Buttons */
.stButton > button {
    background: transparent !important; border: 1px solid #C9A84C !important;
    color: #C9A84C !important; font-family: 'Inter', sans-serif !important;
    font-size: 0.68rem !important; letter-spacing: 0.15em !important;
    text-transform: uppercase !important; border-radius: 0 !important;
    padding: 0.55rem 1.6rem !important; transition: all 0.2s !important;
}
.stButton > button:hover { background: #C9A84C !important; color: #0C0C0C !important; }
[data-testid="stFormSubmitButton"] button {
    background: #C9A84C !important; color: #0C0C0C !important;
    border: none !important; font-weight: 600 !important;
    font-size: 0.68rem !important; letter-spacing: 0.15em !important;
    text-transform: uppercase !important; border-radius: 0 !important;
    padding: 0.6rem 2rem !important;
}
.stDownloadButton > button {
    background: transparent !important; border: 1px solid #C9A84C !important;
    color: #C9A84C !important; border-radius: 0 !important;
    font-size: 0.68rem !important; letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}
.stDownloadButton > button:hover { background: #C9A84C !important; color: #0C0C0C !important; }

/* Progress */
div[data-testid="stProgressBar"] > div > div > div {
    background: linear-gradient(90deg, #C9A84C 0%, #E8C96A 100%) !important;
}

/* Tabs */
[data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid #1C1C1C !important; }
button[data-baseweb="tab"] {
    background: transparent !important; color: #3A3A3A !important;
    font-size: 0.68rem !important; letter-spacing: 0.14em !important;
    text-transform: uppercase !important; padding: 0.8rem 1.5rem !important;
    font-family: 'Inter', sans-serif !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #C9A84C !important; border-bottom: 2px solid #C9A84C !important;
}

/* Form container */
[data-testid="stForm"] {
    background: #0A0A0A !important; border: 1px solid #181818 !important;
    border-radius: 2px !important; padding: 2rem 1.8rem !important;
}

/* Expander */
details { border: 1px solid #181818 !important; border-radius: 2px !important; background: #0A0A0A !important; }
details summary { color: #C9A84C !important; font-family: 'Inter', sans-serif !important; font-size: 0.75rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }

/* Alerts */
[data-testid="stAlert"] {
    background: #0A0A0A !important; border-radius: 2px !important;
    border-left: 2px solid #C9A84C !important;
}
[data-testid="stAlert"] p { color: #888 !important; font-size: 0.8rem !important; }

/* Divider */
hr { border-color: #181818 !important; margin: 1.8rem 0 !important; }

/* Dataframe */
[data-testid="stDataFrame"] { border: 1px solid #181818 !important; border-radius: 2px !important; }

/* File uploader */
[data-testid="stFileUploadDropzone"] { background: #0A0A0A !important; border-color: #222 !important; border-radius: 2px !important; }

/* Code */
code { background: #111 !important; color: #C9A84C !important; border-radius: 2px !important; }
pre { background: #0A0A0A !important; border: 1px solid #1A1A1A !important; border-radius: 2px !important; }

/* Caption */
.stCaption p { color: #383838 !important; font-size: 0.65rem !important; letter-spacing: 0.08em !important; }

/* Image */
[data-testid="stImage"] img { border-radius: 2px !important; }

/* Block container */
.block-container { padding: 2rem 2.5rem !important; max-width: 1200px !important; }
</style>
""", unsafe_allow_html=True)


# ── Session State ─────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "case_created": False, "case": {},
        "partner_a": {}, "partner_b": {},
        "assets_a": [], "assets_b": [],
        "debts_a": [], "debts_b": [],
        "goals_a": {}, "goals_b": {},
        "uploaded_docs": [], "partner_invited": False, "invite_email": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()


# ── Helper Functions ──────────────────────────────────────────────────────
def money(value):
    try:
        return f"${float(value):,.2f}"
    except Exception:
        return "$0.00"

def completion_score():
    score = 0
    explanation = []

    if st.session_state.case_created:
        score += 10; explanation.append("Case setup completed (+10)")
    else:
        explanation.append("Case setup missing (+0)")

    if st.session_state.partner_invited:
        score += 10; explanation.append("Partner invitation prepared (+10)")
    else:
        explanation.append("Partner invitation not prepared (+0)")

    if st.session_state.partner_a:
        score += 10; explanation.append("Partner A questionnaire completed (+10)")
    else:
        explanation.append("Partner A questionnaire missing (+0)")

    if st.session_state.partner_b:
        score += 10; explanation.append("Partner B questionnaire completed (+10)")
    else:
        explanation.append("Partner B questionnaire missing (+0)")

    if len(st.session_state.assets_a) > 0 and len(st.session_state.assets_b) > 0:
        score += 15; explanation.append("Both partners disclosed assets (+15)")
    else:
        explanation.append("Asset disclosure incomplete (+0)")

    if len(st.session_state.debts_a) > 0 and len(st.session_state.debts_b) > 0:
        score += 10; explanation.append("Both partners disclosed debts (+10)")
    else:
        explanation.append("Debt disclosure incomplete (+0)")

    if st.session_state.goals_a and st.session_state.goals_b:
        score += 15; explanation.append("Both partners selected prenup preferences (+15)")
    else:
        explanation.append("Partner preference responses incomplete (+0)")

    conflicts = detect_conflicts()
    if len(conflicts) == 0 and st.session_state.goals_a and st.session_state.goals_b:
        score += 10; explanation.append("No major preference conflicts detected (+10)")
    elif len(conflicts) > 0:
        explanation.append(f"{len(conflicts)} preference conflict(s) detected (+0)")
    else:
        explanation.append("Conflict check pending (+0)")

    docs = st.session_state.uploaded_docs
    if len(docs) >= 2:
        score += 10; explanation.append("Supporting documents uploaded (+10)")
    else:
        explanation.append("Supporting documents limited or missing (+0)")

    return min(score, 100), explanation

def risk_level(score):
    if score >= 80:
        return "Low", "Strong preparation"
    elif score >= 55:
        return "Medium", "Needs attorney clarification"
    return "High", "Missing key information"

def detect_conflicts():
    conflicts = []
    a = st.session_state.goals_a
    b = st.session_state.goals_b
    checks = [
        ("premarital_assets", "Premarital asset treatment"),
        ("future_income", "Future income treatment"),
        ("business_growth", "Business growth / appreciation"),
        ("debt_responsibility", "Debt responsibility"),
        ("spousal_support", "Spousal support"),
        ("inheritance", "Inheritance and family gifts"),
        ("home_purchase", "Future home purchase"),
    ]
    for key, label in checks:
        if a.get(key) and b.get(key) and a.get(key) != b.get(key):
            conflicts.append({
                "Topic": label,
                "Partner A": a.get(key),
                "Partner B": b.get(key),
                "Severity": "High" if key in ["spousal_support", "business_growth", "premarital_assets"] else "Medium",
                "Recommendation": "Discuss before attorney review.",
            })
    return conflicts

def missing_documents():
    docs = [d["type"] for d in st.session_state.uploaded_docs]
    required = [
        "Government ID", "Bank/Investment Statements", "Debt Statements",
        "Real Estate Documents", "Business Ownership Documents", "Retirement Account Statements",
    ]
    return [item for item in required if item not in docs]

def build_asset_df():
    rows = []
    for p, assets in [("Partner A", st.session_state.assets_a), ("Partner B", st.session_state.assets_b)]:
        for asset in assets:
            rows.append({
                "Owner": p, "Type": asset.get("asset_type"),
                "Description": asset.get("description"), "Location": asset.get("location"),
                "Value": asset.get("value"), "Preference": asset.get("preference"),
            })
    return pd.DataFrame(rows)

def build_debt_df():
    rows = []
    for p, debts in [("Partner A", st.session_state.debts_a), ("Partner B", st.session_state.debts_b)]:
        for debt in debts:
            rows.append({
                "Owner": p, "Type": debt.get("debt_type"),
                "Description": debt.get("description"),
                "Balance": debt.get("balance"), "Preference": debt.get("preference"),
            })
    return pd.DataFrame(rows)

def generate_draft_preview():
    case = st.session_state.case
    pa = st.session_state.partner_a
    pb = st.session_state.partner_b
    a_name = pa.get("name", "Partner A")
    b_name = pb.get("name", "Partner B")
    wedding_date = case.get("wedding_date", "[Wedding Date]")
    residence = case.get("future_residence", "[Future Residence]")

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
    conflicts = detect_conflicts()
    missing = missing_documents()
    asset_df = build_asset_df()
    debt_df = build_debt_df()
    case = st.session_state.case
    pa = st.session_state.partner_a
    pb = st.session_state.partner_b

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
    ]
    for line in explanation:
        lines.append(f"- {line}")
    lines += ["", "## Missing Documents"]
    for item in (missing if missing else ["No major missing documents identified."]):
        lines.append(f"- {item}")
    lines += ["", "## Partner Preference Conflicts"]
    if conflicts:
        for c in conflicts:
            lines.append(f"- {c['Topic']}: Partner A: '{c['Partner A']}' | Partner B: '{c['Partner B']}' | Severity: {c['Severity']}")
    else:
        lines.append("- No major conflicts detected.")
    lines += ["", "## Asset Disclosure"]
    if not asset_df.empty:
        for _, row in asset_df.iterrows():
            lines.append(f"- {row['Owner']} | {row['Type']} | {row['Description']} | {row['Location']} | {money(row['Value'])} | {row['Preference']}")
    else:
        lines.append("- No assets disclosed.")
    lines += ["", "## Debt Disclosure"]
    if not debt_df.empty:
        for _, row in debt_df.iterrows():
            lines.append(f"- {row['Owner']} | {row['Type']} | {row['Description']} | Balance: {money(row['Balance'])} | {row['Preference']}")
    else:
        lines.append("- No debts disclosed.")
    lines += [
        "", "## Attorney Discussion Questions",
        "- Are all premarital assets fully disclosed and properly valued?",
        "- Should future appreciation of premarital property remain separate or become marital property?",
        "- How should business ownership and growth during marriage be treated?",
        "- How should debts incurred before and during marriage be handled?",
        "- Should spousal support be waived, limited, or reserved for future determination?",
        "- Are there cross-border assets, immigration issues, or family obligations requiring special review?",
        "", "## Draft Preview", generate_draft_preview(),
    ]
    return "\n".join(lines)

def downloadable_text(text):
    return BytesIO(text.encode("utf-8"))


# ── Partner Form ──────────────────────────────────────────────────────────
def partner_form(label, state_key):
    existing = st.session_state[state_key]
    with st.form(f"{state_key}_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(f"{label} Name", value=existing.get("name", ""))
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
        col_a, col_b = st.columns(2)
        with col_a:
            owns_business = st.checkbox("Owns a business or equity interest", value=existing.get("owns_business", False))
            owns_real_estate = st.checkbox("Owns real estate", value=existing.get("owns_real_estate", False))
        with col_b:
            has_children_prior = st.checkbox("Has children from prior relationship", value=existing.get("has_children_prior", False))
            supports_family = st.checkbox("Financially supports family members", value=existing.get("supports_family", False))

        st.markdown("---")
        st.markdown('<p style="font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;color:#C9A84C;margin-bottom:1rem">Prenup Preferences</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            premarital_assets = st.selectbox("Premarital assets", ["Keep separate", "Share after marriage", "Discuss with attorney"], key=f"{state_key}_premarital_assets")
            future_income = st.selectbox("Future income during marriage", ["Shared marital property", "Separate property", "Discuss with attorney"], key=f"{state_key}_future_income")
            business_growth = st.selectbox("Business growth / appreciation", ["Keep separate", "Share appreciation", "Discuss with attorney"], key=f"{state_key}_business_growth")
            debt_responsibility = st.selectbox("Premarital debts", ["Each partner responsible for own debts", "Shared responsibility", "Discuss with attorney"], key=f"{state_key}_debt_responsibility")
        with col2:
            spousal_support = st.selectbox("Spousal support", ["Waived", "Limited", "Reserved for future review", "Discuss with attorney"], key=f"{state_key}_spousal_support")
            inheritance = st.selectbox("Inheritance and family gifts", ["Keep separate", "Share if used by couple", "Discuss with attorney"], key=f"{state_key}_inheritance")
            home_purchase = st.selectbox("Future home purchase", ["Shared property", "Based on contribution", "Discuss with attorney"], key=f"{state_key}_home_purchase")

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


# ── Sidebar ────────────────────────────────────────────────────────────────
st.sidebar.markdown(
    '<p style="font-size:0.58rem;letter-spacing:0.3em;text-transform:uppercase;color:#333;margin-bottom:0.1rem">Est. 2024</p>',
    unsafe_allow_html=True,
)
st.sidebar.title("KnotWise")
st.sidebar.caption("AI Prenup Preparation Assistant")
st.sidebar.divider()

page = st.sidebar.radio(
    "",
    [
        "1. Welcome",
        "2. Case Setup",
        "3. Add Partner",
        "4. Partner A Questionnaire",
        "5. Partner B Questionnaire",
        "6. Assets & Debts",
        "7. Risk Dashboard",
        "8. Draft Preview",
        "9. Attorney Review Upgrade",
        "10. Project Requirements View",
    ],
    label_visibility="collapsed",
)

st.sidebar.divider()
st.sidebar.caption("Academic prototype only. Not legal advice.")


# ── Shared UI helpers ─────────────────────────────────────────────────────
def eyebrow(text):
    st.markdown(
        f'<p style="font-size:0.62rem;letter-spacing:0.28em;text-transform:uppercase;color:#C9A84C;margin-bottom:0.2rem">{text}</p>',
        unsafe_allow_html=True,
    )

def gold_rule():
    st.markdown('<div style="width:36px;height:1px;background:#C9A84C;margin:0.5rem 0 1.4rem 0"></div>', unsafe_allow_html=True)

def list_item(text):
    st.markdown(f'<p style="color:#444;font-size:0.8rem;margin:0.25rem 0;line-height:1.6">— {text}</p>', unsafe_allow_html=True)


# ── Pages ──────────────────────────────────────────────────────────────────

# 1. WELCOME
if page == "1. Welcome":
    st.image("images/NYC-WEDDING-PHOTOGRAPHER-1024x683.jpg", use_container_width=True)

    eyebrow("AI Prenup Preparation")
    st.title("KnotWise")
    gold_rule()

    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        st.markdown(
            "KnotWise helps couples complete structured prenup questionnaires, organize financial disclosures, "
            "compare partner preferences, identify conflicts, and generate an attorney-ready preparation summary."
        )
        st.markdown("---")
        st.markdown('<p style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#555;margin-bottom:0.8rem">What this prototype covers</p>', unsafe_allow_html=True)
        for item in [
            "Couple case creation and partner invitation workflow",
            "Partner A and B questionnaires with financial disclosures",
            "Asset and debt disclosure with preference tracking",
            "Automated conflict detection between partner responses",
            "Prenup readiness score with explainable breakdown",
            "AI-assisted draft preview and attorney-ready export",
            "Mock premium attorney review upgrade",
        ]:
            list_item(item)

    with col2:
        score, _ = completion_score()
        st.metric("Prototype Stack", "Streamlit + Python")
        st.metric("Primary Value", "Lower legal prep time")
        st.metric("User Flow", "2-partner intake")
        st.metric("Current Readiness", f"{score}/100")

    st.markdown(
        '<p style="font-size:0.65rem;color:#2A2A2A;border-top:1px solid #181818;padding-top:1rem;margin-top:2rem;letter-spacing:0.04em;line-height:1.8">'
        'This prototype is designed for a class project and is not legal advice. It does not replace attorney review.</p>',
        unsafe_allow_html=True,
    )


# 2. CASE SETUP
elif page == "2. Case Setup":
    col_img, col_head = st.columns([2, 3], gap="large")
    with col_img:
        st.image("images/7d9337fdbff13df38d6ccd18b2a9ec7b.jpg", use_container_width=True)
    with col_head:
        eyebrow("Step 01 of 07")
        st.title("Case Setup")
        gold_rule()
        st.markdown("Establish the jurisdictional context and basic case information for your prenup preparation.")

    st.markdown("---")

    with st.form("case_setup_form"):
        col1, col2 = st.columns(2)
        with col1:
            case_name = st.text_input("Case / Couple Name", value=st.session_state.case.get("case_name", ""))
            current_residence = st.text_input("Current Residence", value=st.session_state.case.get("current_residence", ""))
            jurisdictions = st.text_input("Jurisdictions / Countries Involved", value=st.session_state.case.get("jurisdictions", ""))
        with col2:
            saved_date = st.session_state.case.get("wedding_date")
            default_date = date.today()
            if isinstance(saved_date, str):
                try:
                    from datetime import datetime
                    default_date = datetime.strptime(saved_date, "%Y-%m-%d").date()
                except Exception:
                    pass
            wedding_date = st.date_input("Expected Wedding Date", value=default_date)
            future_residence = st.text_input("Expected Residence After Marriage", value=st.session_state.case.get("future_residence", ""))
            cross_border = st.checkbox("Involves cross-border assets, immigration, or multiple countries", value=st.session_state.case.get("cross_border", False))
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
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.15em;text-transform:uppercase;color:#444;margin-bottom:0.5rem">Current Case</p>', unsafe_allow_html=True)
        st.json(st.session_state.case)


# 3. ADD PARTNER
elif page == "3. Add Partner":
    col_img, col_head = st.columns([1, 2], gap="large")
    with col_img:
        st.image("images/images (1).jpeg", use_container_width=True)
    with col_head:
        eyebrow("Step 02 of 07")
        st.title("Add Partner")
        gold_rule()
        st.markdown("Prepare a partner invitation for the prenup preparation workflow.")
        st.markdown("---")
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.15em;text-transform:uppercase;color:#444;margin-bottom:0.6rem">Partner Workflow</p>', unsafe_allow_html=True)
        for i, step in enumerate([
            "Partner A creates the case",
            "Partner A invites Partner B",
            "Partner B completes a separate questionnaire",
            "Both responses are compared",
            "Conflicts and missing information are flagged",
            "A lawyer-ready summary is generated",
        ], 1):
            st.markdown(f'<p style="color:#333;font-size:0.78rem;margin:0.2rem 0">{i}.  {step}</p>', unsafe_allow_html=True)

    st.markdown("---")

    with st.form("partner_invite_form"):
        col1, col2 = st.columns(2)
        with col1:
            invite_email = st.text_input("Partner Email Address", value=st.session_state.invite_email)
            partner_name = st.text_input("Partner Name", value=st.session_state.partner_b.get("name", ""))
        with col2:
            access_level = st.selectbox("Partner Access Level", [
                "Complete questionnaire only",
                "View shared summary after both submit",
                "Full shared case access",
            ])
            message = st.text_area("Invitation Message", height=100,
                value="Hi, I invited you to complete your section of our prenup preparation questionnaire in KnotWise.")
        sent = st.form_submit_button("Prepare Partner Invitation")

    if sent:
        st.session_state.partner_invited = True
        st.session_state.invite_email = invite_email
        if partner_name:
            st.session_state.partner_b["name"] = partner_name
        st.success("Partner invitation prepared. In production, this would send an email invitation link.")
        st.code(f"To: {invite_email}\nSubject: Invitation to complete KnotWise prenup questionnaire\n\n{message}\n\nAccess Level: {access_level}", language="text")


# 4. PARTNER A QUESTIONNAIRE
elif page == "4. Partner A Questionnaire":
    col_img, col_head = st.columns([1, 2], gap="large")
    with col_img:
        st.image("images/106ae0c3ff0dd68d593c41d7bf297240.jpg", use_container_width=True)
    with col_head:
        eyebrow("Step 03 of 07")
        st.title("Partner A Questionnaire")
        gold_rule()
        st.markdown("Complete your financial profile and prenup preference selections.")

    st.markdown("---")
    partner_form("Partner A", "partner_a")


# 5. PARTNER B QUESTIONNAIRE
elif page == "5. Partner B Questionnaire":
    col_img, col_head = st.columns([1, 2], gap="large")
    with col_img:
        st.image("images/_MG_4725 copy.jpg", use_container_width=True)
    with col_head:
        eyebrow("Step 04 of 07")
        st.title("Partner B Questionnaire")
        gold_rule()
        if not st.session_state.partner_invited:
            st.warning("Partner has not been invited yet. Go to 'Add Partner' first for the intended workflow.")
        else:
            st.markdown("Partner invitation prepared. Complete the questionnaire below.")

    st.markdown("---")
    partner_form("Partner B", "partner_b")


# 6. ASSETS & DEBTS
elif page == "6. Assets & Debts":
    st.image("images/img_7973.jpg", use_container_width=True)
    eyebrow("Step 05 of 07")
    st.title("Assets, Debts & Documents")
    gold_rule()

    tab1, tab2, tab3 = st.tabs(["Add Asset", "Add Debt", "Upload Documents"])

    with tab1:
        with st.form("asset_form"):
            col1, col2 = st.columns(2)
            with col1:
                owner = st.selectbox("Owner", ["Partner A", "Partner B"])
                asset_type = st.selectbox("Asset Type", ["Bank Account", "Investment", "Retirement Account", "Real Estate", "Business", "Vehicle", "Inheritance", "Other"])
                description = st.text_input("Description")
            with col2:
                location = st.text_input("Country / State", value="United States")
                value = st.number_input("Estimated Value ($)", min_value=0.0, step=1000.0)
                preference = st.selectbox("Preferred Treatment", ["Separate property", "Shared property", "Attorney review needed"])
            submitted = st.form_submit_button("Add Asset")

        if submitted:
            asset = {"asset_type": asset_type, "description": description, "location": location, "value": value, "preference": preference}
            (st.session_state.assets_a if owner == "Partner A" else st.session_state.assets_b).append(asset)
            st.success("Asset added.")

        asset_df = build_asset_df()
        if not asset_df.empty:
            st.dataframe(asset_df, use_container_width=True)
        else:
            st.caption("No assets added yet.")

    with tab2:
        with st.form("debt_form"):
            col1, col2 = st.columns(2)
            with col1:
                owner = st.selectbox("Debt Owner", ["Partner A", "Partner B"])
                debt_type = st.selectbox("Debt Type", ["Student Loan", "Credit Card", "Mortgage", "Personal Loan", "Business Debt", "Vehicle Loan", "Other"])
                description = st.text_input("Debt Description")
            with col2:
                balance = st.number_input("Debt Balance ($)", min_value=0.0, step=500.0)
                preference = st.selectbox("Responsibility Preference", ["Owner remains responsible", "Shared responsibility", "Attorney review needed"])
            submitted = st.form_submit_button("Add Debt")

        if submitted:
            debt = {"debt_type": debt_type, "description": description, "balance": balance, "preference": preference}
            (st.session_state.debts_a if owner == "Partner A" else st.session_state.debts_b).append(debt)
            st.success("Debt added.")

        debt_df = build_debt_df()
        if not debt_df.empty:
            st.dataframe(debt_df, use_container_width=True)
        else:
            st.caption("No debts added yet.")

    with tab3:
        st.caption("Files are not permanently stored. Document type and filename are recorded for demonstration purposes.")
        with st.form("doc_form"):
            col1, col2 = st.columns(2)
            with col1:
                doc_type = st.selectbox("Document Type", [
                    "Government ID", "Bank/Investment Statements", "Debt Statements",
                    "Real Estate Documents", "Business Ownership Documents",
                    "Retirement Account Statements", "Other",
                ])
            with col2:
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


# 7. RISK DASHBOARD
elif page == "7. Risk Dashboard":
    st.image("images/black-white-shot-engaged-couple.jpg", use_container_width=True)
    eyebrow("Step 06 of 07")
    st.title("Risk Dashboard")
    gold_rule()

    score, explanation = completion_score()
    risk, label = risk_level(score)
    conflicts = detect_conflicts()
    missing = missing_documents()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Readiness Score", f"{score}/100")
    col2.metric("Risk Level", risk)
    col3.metric("Conflicts", len(conflicts))
    col4.metric("Missing Docs", len(missing))

    st.markdown("---")
    st.markdown(f'<p style="font-size:0.78rem;color:#C9A84C;letter-spacing:0.08em;margin-bottom:0.6rem">{label}</p>', unsafe_allow_html=True)
    st.progress(score / 100)

    st.markdown("---")

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        with st.expander("Score Breakdown", expanded=True):
            for item in explanation:
                color = "#C9A84C" if "(+0)" not in item else "#2E2E2E"
                st.markdown(f'<p style="color:{color};font-size:0.78rem;margin:0.25rem 0;line-height:1.6">— {item}</p>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.15em;text-transform:uppercase;color:#444;margin-bottom:0.6rem">Missing Documents</p>', unsafe_allow_html=True)
        if missing:
            for doc in missing:
                st.markdown(f'<p style="color:#333;font-size:0.78rem;margin:0.2rem 0">— {doc}</p>', unsafe_allow_html=True)
        else:
            st.success("All major document categories present.")

    with col_right:
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.15em;text-transform:uppercase;color:#444;margin-bottom:0.6rem">Partner Preference Conflicts</p>', unsafe_allow_html=True)
        if conflicts:
            st.dataframe(pd.DataFrame(conflicts), use_container_width=True)
        else:
            st.success("No major conflicts detected based on current responses.")

    asset_df = build_asset_df()
    debt_df = build_debt_df()
    if not asset_df.empty or not debt_df.empty:
        st.markdown("---")
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.15em;text-transform:uppercase;color:#444;margin-bottom:0.6rem">Financial Disclosure Overview</p>', unsafe_allow_html=True)
        if not asset_df.empty:
            st.caption("Assets")
            st.dataframe(asset_df, use_container_width=True)
        if not debt_df.empty:
            st.caption("Debts")
            st.dataframe(debt_df, use_container_width=True)


# 8. DRAFT PREVIEW
elif page == "8. Draft Preview":
    col_img, col_head = st.columns([1, 2], gap="large")
    with col_img:
        st.image("images/images.jpeg", use_container_width=True)
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
    draft = generate_draft_preview()
    st.text_area("Draft Preview", value=draft, height=500)


# 9. ATTORNEY REVIEW UPGRADE
elif page == "9. Attorney Review Upgrade":
    col_img, col_head = st.columns([2, 3], gap="large")
    with col_img:
        st.image("images/7d9337fdbff13df38d6ccd18b2a9ec7b.jpg", use_container_width=True)
    with col_head:
        eyebrow("Premium")
        st.title("Attorney Review Upgrade")
        gold_rule()
        st.markdown(
            "Connect your completed preparation package with a licensed attorney "
            "for final review, jurisdiction-specific feedback, and execution support."
        )

    st.markdown("---")

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.2em;text-transform:uppercase;color:#444;margin-bottom:0.4rem">Preparation Package</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-family:\'Playfair Display\',serif;font-size:1.8rem;color:#C9A84C;margin:0.2rem 0 1rem 0">$49–$99</p>', unsafe_allow_html=True)
        for item in ["Complete questionnaire summary", "Draft preview", "Missing document checklist", "Conflict report"]:
            list_item(item)

    with col2:
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.2em;text-transform:uppercase;color:#444;margin-bottom:0.4rem">Attorney Review</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-family:\'Playfair Display\',serif;font-size:1.8rem;color:#C9A84C;margin:0.2rem 0 1rem 0">$499–$1,500</p>', unsafe_allow_html=True)
        for item in ["Attorney reviews draft", "Revisions included", "Jurisdiction-specific feedback", "Signing guidance"]:
            list_item(item)

    with col3:
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.2em;text-transform:uppercase;color:#444;margin-bottom:0.4rem">Concierge Package</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-family:\'Playfair Display\',serif;font-size:1.8rem;color:#C9A84C;margin:0.2rem 0 1rem 0">$2,000+</p>', unsafe_allow_html=True)
        for item in ["Two-attorney coordination", "Partner-specific review", "Notary and signing workflow", "Final execution checklist"]:
            list_item(item)

    st.markdown("---")
    st.caption("Production version could integrate payments, attorney marketplace, e-signature, and notarization providers.")


# 10. PROJECT REQUIREMENTS VIEW
elif page == "10. Project Requirements View":
    eyebrow("Academic Reference")
    st.title("Project Requirements Alignment")
    gold_rule()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.15em;text-transform:uppercase;color:#444;margin-bottom:0.6rem">Business Problem</p>', unsafe_allow_html=True)
        st.markdown(
            "Prenup preparation is expensive and inefficient because couples enter the legal process "
            "without organized disclosures, aligned preferences, or complete documentation before meeting attorneys."
        )
        st.markdown("---")
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.15em;text-transform:uppercase;color:#444;margin-bottom:0.6rem">Functional Requirements Covered</p>', unsafe_allow_html=True)
        for item in [
            "Create case and invite partner",
            "Partner A and B questionnaires",
            "Asset and debt disclosure",
            "Supporting document upload metadata",
            "Conflict detection between partner preferences",
            "Prenup readiness score with breakdown",
            "Draft preview generation",
            "Lawyer-ready summary export",
            "Mock attorney review upgrade",
        ]:
            list_item(item)

        st.markdown("---")
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.15em;text-transform:uppercase;color:#444;margin-bottom:0.6rem">Data Entities</p>', unsafe_allow_html=True)
        for item in ["Couple Case", "Partner Profile", "Assets", "Debts", "Prenup Goals", "Uploaded Documents", "Conflict Flags", "Readiness Score", "Draft Summary"]:
            list_item(item)

    with col2:
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.15em;text-transform:uppercase;color:#444;margin-bottom:0.6rem">Application Architecture</p>', unsafe_allow_html=True)
        st.code(
            "User\n→ Streamlit UI\n→ Questionnaire Forms\n→ Session / Data Layer\n"
            "→ Scoring Engine\n→ Conflict Engine\n→ Draft Generator\n→ Export / Attorney Review",
            language="text",
        )
        st.markdown("---")
        st.markdown('<p style="font-size:0.62rem;letter-spacing:0.15em;text-transform:uppercase;color:#444;margin-bottom:0.6rem">Non-Functional Requirements</p>', unsafe_allow_html=True)
        for item in [
            "Pages load within 3 seconds for normal usage",
            "Sensitive financial information is protected",
            "Easy to use for non-technical users",
            "Clear disclaimers: drafts require attorney review",
            "Role-based access: Partner A, B, attorney, admin",
            "Audit logs for questionnaire submission and draft generation",
            "Explainable scoring logic",
            "Scalable for future attorney marketplace integration",
        ]:
            list_item(item)
