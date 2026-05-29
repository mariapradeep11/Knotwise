
import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

# ----------------------------
# KnotWise - Streamlit MVP
# ----------------------------
# This prototype is for an academic/class project.
# It is not legal advice and does not replace attorney review.

st.set_page_config(
    page_title="KnotWise | AI Prenup Preparation Assistant",
    page_icon="💍",
    layout="wide",
)

# ----------------------------
# Session State Initialization
# ----------------------------
def init_state():
    defaults = {
        "case_created": False,
        "case": {},
        "partner_a": {},
        "partner_b": {},
        "assets_a": [],
        "assets_b": [],
        "debts_a": [],
        "debts_b": [],
        "goals_a": {},
        "goals_b": {},
        "uploaded_docs": [],
        "partner_invited": False,
        "invite_email": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# ----------------------------
# Helper Functions
# ----------------------------
def money(value):
    try:
        return f"${float(value):,.2f}"
    except Exception:
        return "$0.00"

def completion_score():
    score = 0
    explanation = []

    if st.session_state.case_created:
        score += 10
        explanation.append("Case setup completed (+10)")
    else:
        explanation.append("Case setup missing (+0)")

    if st.session_state.partner_invited:
        score += 10
        explanation.append("Partner invitation prepared (+10)")
    else:
        explanation.append("Partner invitation not prepared (+0)")

    if st.session_state.partner_a:
        score += 10
        explanation.append("Partner A questionnaire completed (+10)")
    else:
        explanation.append("Partner A questionnaire missing (+0)")

    if st.session_state.partner_b:
        score += 10
        explanation.append("Partner B questionnaire completed (+10)")
    else:
        explanation.append("Partner B questionnaire missing (+0)")

    if len(st.session_state.assets_a) > 0 and len(st.session_state.assets_b) > 0:
        score += 15
        explanation.append("Both partners disclosed assets (+15)")
    else:
        explanation.append("Asset disclosure incomplete (+0)")

    if len(st.session_state.debts_a) > 0 and len(st.session_state.debts_b) > 0:
        score += 10
        explanation.append("Both partners disclosed debts (+10)")
    else:
        explanation.append("Debt disclosure incomplete (+0)")

    if st.session_state.goals_a and st.session_state.goals_b:
        score += 15
        explanation.append("Both partners selected prenup preferences (+15)")
    else:
        explanation.append("Partner preference responses incomplete (+0)")

    conflicts = detect_conflicts()
    if len(conflicts) == 0 and st.session_state.goals_a and st.session_state.goals_b:
        score += 10
        explanation.append("No major preference conflicts detected (+10)")
    elif len(conflicts) > 0:
        explanation.append(f"{len(conflicts)} preference conflict(s) detected (+0)")
    else:
        explanation.append("Conflict check pending (+0)")

    docs = st.session_state.uploaded_docs
    if len(docs) >= 2:
        score += 10
        explanation.append("Supporting documents uploaded (+10)")
    else:
        explanation.append("Supporting documents are limited or missing (+0)")

    return min(score, 100), explanation

def risk_level(score):
    if score >= 80:
        return "Low", "✅ Strong preparation"
    elif score >= 55:
        return "Medium", "⚠️ Needs attorney clarification"
    return "High", "🚨 Missing key information"

def detect_conflicts():
    conflicts = []
    a = st.session_state.goals_a
    b = st.session_state.goals_b

    checks = [
        ("premarital_assets", "Premarital asset treatment"),
        ("future_income", "Future income treatment"),
        ("business_growth", "Business growth/appreciation"),
        ("debt_responsibility", "Debt responsibility"),
        ("spousal_support", "Spousal support"),
        ("inheritance", "Inheritance and family gifts"),
        ("home_purchase", "Future home purchase"),
    ]

    for key, label in checks:
        if a.get(key) and b.get(key) and a.get(key) != b.get(key):
            conflicts.append({
                "Topic": label,
                "Partner A Preference": a.get(key),
                "Partner B Preference": b.get(key),
                "Severity": "High" if key in ["spousal_support", "business_growth", "premarital_assets"] else "Medium",
                "Recommendation": "Discuss before attorney review and document both expectations clearly."
            })

    return conflicts

def missing_documents():
    docs = [d["type"] for d in st.session_state.uploaded_docs]
    required = [
        "Government ID",
        "Bank/Investment Statements",
        "Debt Statements",
        "Real Estate Documents",
        "Business Ownership Documents",
        "Retirement Account Statements",
    ]

    missing = []
    for item in required:
        if item not in docs:
            missing.append(item)
    return missing

def build_asset_df():
    rows = []
    for p, assets in [("Partner A", st.session_state.assets_a), ("Partner B", st.session_state.assets_b)]:
        for asset in assets:
            rows.append({
                "Owner": p,
                "Asset Type": asset.get("asset_type"),
                "Description": asset.get("description"),
                "Country/State": asset.get("location"),
                "Estimated Value": asset.get("value"),
                "Preference": asset.get("preference"),
            })
    return pd.DataFrame(rows)

def build_debt_df():
    rows = []
    for p, debts in [("Partner A", st.session_state.debts_a), ("Partner B", st.session_state.debts_b)]:
        for debt in debts:
            rows.append({
                "Owner": p,
                "Debt Type": debt.get("debt_type"),
                "Description": debt.get("description"),
                "Balance": debt.get("balance"),
                "Responsibility Preference": debt.get("preference"),
            })
    return pd.DataFrame(rows)

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

    summary = []
    summary.append("# KnotWise Lawyer-Ready Prenup Preparation Summary")
    summary.append("")
    summary.append("## Important Disclaimer")
    summary.append("This document is an AI-assisted preparation summary for academic demonstration purposes. It is not legal advice and should be reviewed by a licensed attorney before use.")
    summary.append("")
    summary.append("## Case Overview")
    summary.append(f"- Couple/Case Name: {case.get('case_name', 'Not provided')}")
    summary.append(f"- Expected Wedding Date: {case.get('wedding_date', 'Not provided')}")
    summary.append(f"- Current Residence: {case.get('current_residence', 'Not provided')}")
    summary.append(f"- Expected Residence After Marriage: {case.get('future_residence', 'Not provided')}")
    summary.append(f"- Jurisdictions/Countries Involved: {case.get('jurisdictions', 'Not provided')}")
    summary.append("")
    summary.append("## Partner Profiles")
    summary.append(f"### Partner A")
    summary.append(f"- Name: {pa.get('name', 'Not provided')}")
    summary.append(f"- Citizenship: {pa.get('citizenship', 'Not provided')}")
    summary.append(f"- Immigration/Residency Status: {pa.get('immigration_status', 'Not provided')}")
    summary.append(f"- Annual Income: {money(pa.get('income', 0))}")
    summary.append("")
    summary.append(f"### Partner B")
    summary.append(f"- Name: {pb.get('name', 'Not provided')}")
    summary.append(f"- Citizenship: {pb.get('citizenship', 'Not provided')}")
    summary.append(f"- Immigration/Residency Status: {pb.get('immigration_status', 'Not provided')}")
    summary.append(f"- Annual Income: {money(pb.get('income', 0))}")
    summary.append("")
    summary.append("## Readiness Score")
    summary.append(f"- Score: {score}/100")
    summary.append(f"- Risk Level: {risk} - {label}")
    summary.append("")
    summary.append("### Score Explanation")
    for line in explanation:
        summary.append(f"- {line}")
    summary.append("")

    summary.append("## Missing Documents")
    if missing:
        for item in missing:
            summary.append(f"- {item}")
    else:
        summary.append("- No major missing documents identified.")
    summary.append("")

    summary.append("## Partner Preference Conflicts")
    if conflicts:
        for c in conflicts:
            summary.append(f"- {c['Topic']}: Partner A selected '{c['Partner A Preference']}', while Partner B selected '{c['Partner B Preference']}'. Severity: {c['Severity']}.")
    else:
        summary.append("- No major conflicts detected based on submitted preferences.")
    summary.append("")

    summary.append("## Asset Disclosure Summary")
    if not asset_df.empty:
        for _, row in asset_df.iterrows():
            summary.append(f"- {row['Owner']} | {row['Asset Type']} | {row['Description']} | {row['Country/State']} | {money(row['Estimated Value'])} | Preference: {row['Preference']}")
    else:
        summary.append("- No assets disclosed.")
    summary.append("")

    summary.append("## Debt Disclosure Summary")
    if not debt_df.empty:
        for _, row in debt_df.iterrows():
            summary.append(f"- {row['Owner']} | {row['Debt Type']} | {row['Description']} | Balance: {money(row['Balance'])} | Preference: {row['Responsibility Preference']}")
    else:
        summary.append("- No debts disclosed.")
    summary.append("")

    summary.append("## Attorney Discussion Questions")
    summary.append("- Are all premarital assets fully disclosed and properly valued?")
    summary.append("- Should future appreciation of premarital property remain separate or become marital property?")
    summary.append("- How should business ownership and business growth during marriage be treated?")
    summary.append("- How should debts incurred before and during marriage be handled?")
    summary.append("- Should spousal support be waived, limited, or reserved for future determination?")
    summary.append("- Are there cross-border assets, immigration issues, or family obligations that require special review?")
    summary.append("")
    summary.append("## Draft Preview")
    summary.append(generate_draft_preview())

    return "\n".join(summary)

def generate_draft_preview():
    case = st.session_state.case
    pa = st.session_state.partner_a
    pb = st.session_state.partner_b

    partner_a_name = pa.get("name", "Partner A")
    partner_b_name = pb.get("name", "Partner B")
    wedding_date = case.get("wedding_date", "[Wedding Date]")
    residence = case.get("future_residence", "[Future Residence]")

    return f"""
This draft preview is generated from the questionnaire responses and is intended for attorney review only.

1. Background  
{partner_a_name} and {partner_b_name} are planning to marry on or around {wedding_date}. The couple expects to reside in {residence}. Each partner has provided preliminary financial disclosures and preferences regarding separate property, marital property, debts, income, and future financial responsibilities.

2. Separate Property  
Property owned by either partner before marriage may be identified as separate property, subject to attorney review and complete disclosure schedules.

3. Marital Property  
The couple should determine whether income, assets, or appreciation earned during marriage will be treated as shared marital property or separately owned property.

4. Debts  
Each partner should disclose all premarital debts. The agreement may specify whether premarital debts remain the responsibility of the partner who incurred them.

5. Business Ownership  
Any business interests disclosed by either partner should be separately reviewed to determine whether ownership, future growth, dividends, or appreciation will remain separate or be shared.

6. Inheritance and Family Gifts  
The couple should clarify whether inheritance, gifts, and family property will remain separate property.

7. Spousal Support  
The couple should discuss whether spousal support will be waived, limited, or reserved for attorney review based on future circumstances.

8. Attorney Review  
This draft preview must be reviewed by qualified counsel before execution. Each partner should have adequate time to review and ask questions before signing.
"""

def downloadable_text(text):
    return BytesIO(text.encode("utf-8"))

# ----------------------------
# Sidebar Navigation
# ----------------------------
st.sidebar.title("💍 KnotWise")
st.sidebar.caption("AI Prenup Preparation Assistant")

page = st.sidebar.radio(
    "Navigate",
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
)

st.sidebar.divider()
st.sidebar.warning("Academic prototype only. Not legal advice.")

# ----------------------------
# Page 1 - Welcome
# ----------------------------
if page == "1. Welcome":
    st.title("KnotWise: AI Prenup Preparation Assistant")
    st.subheader("Collaborative prenup preparation before attorney review")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        KnotWise helps couples complete structured prenup questionnaires, organize financial disclosures,
        compare partner preferences, identify conflicts, and generate an attorney-ready preparation summary.
        """)
        st.info("""
        This prototype is designed for a class project. It demonstrates application architecture,
        partner collaboration, data collection, risk scoring, and document preparation workflows.
        """)

        st.markdown("### MVP Features")
        st.markdown("""
        - Create a couple case
        - Add/invite a partner
        - Complete Partner A and Partner B questionnaires
        - Add assets, debts, and supporting document types
        - Detect preference conflicts
        - Calculate prenup readiness score
        - Generate an AI-style draft preview
        - Mock premium attorney review upgrade
        """)

    with col2:
        st.metric("Prototype Stack", "Streamlit + Python")
        st.metric("Primary Value", "Lower legal prep time")
        st.metric("User Flow", "2-partner intake")

# ----------------------------
# Page 2 - Case Setup
# ----------------------------
elif page == "2. Case Setup":
    st.title("Case Setup")

    with st.form("case_setup_form"):
        case_name = st.text_input("Case/Couple Name", value=st.session_state.case.get("case_name", "Maria & Partner Prenup Prep"))
        wedding_date = st.date_input("Expected Wedding Date", value=st.session_state.case.get("wedding_date", date.today()))
        current_residence = st.text_input("Current Residence", value=st.session_state.case.get("current_residence", "Florida, USA"))
        future_residence = st.text_input("Expected Residence After Marriage", value=st.session_state.case.get("future_residence", "Florida, USA"))
        jurisdictions = st.text_input(
            "Jurisdictions/Countries Involved",
            value=st.session_state.case.get("jurisdictions", "United States")
        )
        cross_border = st.checkbox("This case involves cross-border assets, immigration, or multiple countries", value=st.session_state.case.get("cross_border", False))

        submitted = st.form_submit_button("Save Case Setup")

    if submitted:
        st.session_state.case = {
            "case_name": case_name,
            "wedding_date": str(wedding_date),
            "current_residence": current_residence,
            "future_residence": future_residence,
            "jurisdictions": jurisdictions,
            "cross_border": cross_border,
        }
        st.session_state.case_created = True
        st.success("Case setup saved successfully.")

    if st.session_state.case_created:
        st.json(st.session_state.case)

# ----------------------------
# Page 3 - Add Partner
# ----------------------------
elif page == "3. Add Partner":
    st.title("Add Partner")
    st.write("This page demonstrates the required option to add or invite a partner into the prenup preparation workflow.")

    with st.form("partner_invite_form"):
        invite_email = st.text_input("Partner Email Address", value=st.session_state.invite_email)
        partner_name = st.text_input("Partner Name", value=st.session_state.partner_b.get("name", ""))
        access_level = st.selectbox(
            "Partner Access Level",
            ["Complete questionnaire only", "View shared summary after both submit", "Full shared case access"]
        )
        message = st.text_area(
            "Invitation Message",
            value="Hi, I invited you to complete your section of our prenup preparation questionnaire in KnotWise."
        )
        sent = st.form_submit_button("Prepare Partner Invitation")

    if sent:
        st.session_state.partner_invited = True
        st.session_state.invite_email = invite_email
        if partner_name:
            st.session_state.partner_b["name"] = partner_name
        st.success("Partner invitation prepared. In a production app, this would send an email invitation link.")
        st.code(f"""
To: {invite_email}

Subject: Invitation to complete KnotWise prenup questionnaire

{message}

Access Level: {access_level}
        """, language="text")

    st.markdown("### Partner Workflow")
    st.markdown("""
    1. Partner A creates the case.
    2. Partner A invites Partner B.
    3. Partner B completes a separate questionnaire.
    4. Both responses are compared.
    5. Conflicts and missing information are flagged.
    6. A lawyer-ready summary is generated.
    """)

# ----------------------------
# Reusable Partner Form
# ----------------------------
def partner_form(label, state_key):
    existing = st.session_state[state_key]
    with st.form(f"{state_key}_form"):
        name = st.text_input(f"{label} Name", value=existing.get("name", ""))
        email = st.text_input(f"{label} Email", value=existing.get("email", ""))
        citizenship = st.text_input("Citizenship", value=existing.get("citizenship", ""))
        immigration_status = st.selectbox(
            "Immigration / Residency Status",
            ["U.S. Citizen", "Green Card / Permanent Resident", "F-1", "H-1B", "L-1", "Canadian PR", "Other", "Prefer not to say"],
            index=0 if not existing.get("immigration_status") else ["U.S. Citizen", "Green Card / Permanent Resident", "F-1", "H-1B", "L-1", "Canadian PR", "Other", "Prefer not to say"].index(existing.get("immigration_status"))
        )
        income = st.number_input("Approximate Annual Income", min_value=0.0, step=1000.0, value=float(existing.get("income", 0.0)))
        owns_business = st.checkbox("Owns a business or equity interest", value=existing.get("owns_business", False))
        owns_real_estate = st.checkbox("Owns real estate", value=existing.get("owns_real_estate", False))
        has_children_prior = st.checkbox("Has children from prior relationship", value=existing.get("has_children_prior", False))
        supports_family = st.checkbox("Financially supports family members", value=existing.get("supports_family", False))
        notes = st.text_area("Additional Notes", value=existing.get("notes", ""))

        st.markdown("### Prenup Preferences")
        premarital_assets = st.selectbox(
            "Premarital assets should be treated as:",
            ["Keep separate", "Share after marriage", "Discuss with attorney"],
            key=f"{state_key}_premarital_assets"
        )
        future_income = st.selectbox(
            "Future income during marriage should be treated as:",
            ["Shared marital property", "Separate property", "Discuss with attorney"],
            key=f"{state_key}_future_income"
        )
        business_growth = st.selectbox(
            "Business growth/appreciation during marriage should be:",
            ["Keep separate", "Share appreciation", "Discuss with attorney"],
            key=f"{state_key}_business_growth"
        )
        debt_responsibility = st.selectbox(
            "Premarital debts should be:",
            ["Each partner responsible for own debts", "Shared responsibility", "Discuss with attorney"],
            key=f"{state_key}_debt_responsibility"
        )
        spousal_support = st.selectbox(
            "Spousal support should be:",
            ["Waived", "Limited", "Reserved for future review", "Discuss with attorney"],
            key=f"{state_key}_spousal_support"
        )
        inheritance = st.selectbox(
            "Inheritance and family gifts should be:",
            ["Keep separate", "Share if used by couple", "Discuss with attorney"],
            key=f"{state_key}_inheritance"
        )
        home_purchase = st.selectbox(
            "Future home purchase should be:",
            ["Shared property", "Based on contribution", "Discuss with attorney"],
            key=f"{state_key}_home_purchase"
        )

        submitted = st.form_submit_button(f"Save {label} Questionnaire")

    if submitted:
        st.session_state[state_key] = {
            "name": name,
            "email": email,
            "citizenship": citizenship,
            "immigration_status": immigration_status,
            "income": income,
            "owns_business": owns_business,
            "owns_real_estate": owns_real_estate,
            "has_children_prior": has_children_prior,
            "supports_family": supports_family,
            "notes": notes,
        }
        goal_key = "goals_a" if state_key == "partner_a" else "goals_b"
        st.session_state[goal_key] = {
            "premarital_assets": premarital_assets,
            "future_income": future_income,
            "business_growth": business_growth,
            "debt_responsibility": debt_responsibility,
            "spousal_support": spousal_support,
            "inheritance": inheritance,
            "home_purchase": home_purchase,
        }
        st.success(f"{label} questionnaire saved.")

# ----------------------------
# Partner A Page
# ----------------------------
elif page == "4. Partner A Questionnaire":
    st.title("Partner A Questionnaire")
    partner_form("Partner A", "partner_a")

# ----------------------------
# Partner B Page
# ----------------------------
elif page == "5. Partner B Questionnaire":
    st.title("Partner B Questionnaire")
    if not st.session_state.partner_invited:
        st.warning("Partner has not been added/invited yet. Go to 'Add Partner' first for the intended workflow.")
    partner_form("Partner B", "partner_b")

# ----------------------------
# Assets & Debts Page
# ----------------------------
elif page == "6. Assets & Debts":
    st.title("Assets, Debts, and Supporting Documents")

    tab1, tab2, tab3 = st.tabs(["Add Asset", "Add Debt", "Upload Document Metadata"])

    with tab1:
        st.subheader("Add Asset")
        with st.form("asset_form"):
            owner = st.selectbox("Owner", ["Partner A", "Partner B"])
            asset_type = st.selectbox("Asset Type", ["Bank Account", "Investment", "Retirement Account", "Real Estate", "Business", "Vehicle", "Inheritance", "Other"])
            description = st.text_input("Description")
            location = st.text_input("Country/State", value="United States")
            value = st.number_input("Estimated Value", min_value=0.0, step=1000.0)
            preference = st.selectbox("Preferred Treatment", ["Separate property", "Shared property", "Attorney review needed"])
            submitted = st.form_submit_button("Add Asset")

        if submitted:
            asset = {
                "asset_type": asset_type,
                "description": description,
                "location": location,
                "value": value,
                "preference": preference,
            }
            if owner == "Partner A":
                st.session_state.assets_a.append(asset)
            else:
                st.session_state.assets_b.append(asset)
            st.success("Asset added.")

        asset_df = build_asset_df()
        if not asset_df.empty:
            st.dataframe(asset_df, use_container_width=True)
        else:
            st.info("No assets added yet.")

    with tab2:
        st.subheader("Add Debt")
        with st.form("debt_form"):
            owner = st.selectbox("Debt Owner", ["Partner A", "Partner B"])
            debt_type = st.selectbox("Debt Type", ["Student Loan", "Credit Card", "Mortgage", "Personal Loan", "Business Debt", "Vehicle Loan", "Other"])
            description = st.text_input("Debt Description")
            balance = st.number_input("Debt Balance", min_value=0.0, step=500.0)
            preference = st.selectbox("Responsibility Preference", ["Owner remains responsible", "Shared responsibility", "Attorney review needed"])
            submitted = st.form_submit_button("Add Debt")

        if submitted:
            debt = {
                "debt_type": debt_type,
                "description": description,
                "balance": balance,
                "preference": preference,
            }
            if owner == "Partner A":
                st.session_state.debts_a.append(debt)
            else:
                st.session_state.debts_b.append(debt)
            st.success("Debt added.")

        debt_df = build_debt_df()
        if not debt_df.empty:
            st.dataframe(debt_df, use_container_width=True)
        else:
            st.info("No debts added yet.")

    with tab3:
        st.subheader("Supporting Document Upload")
        st.caption("For this class prototype, files are not permanently stored. The app records document type and uploaded filename for demo purposes.")

        with st.form("doc_form"):
            doc_type = st.selectbox(
                "Document Type",
                [
                    "Government ID",
                    "Bank/Investment Statements",
                    "Debt Statements",
                    "Real Estate Documents",
                    "Business Ownership Documents",
                    "Retirement Account Statements",
                    "Other",
                ]
            )
            uploaded_file = st.file_uploader("Upload document/image/PDF", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=False)
            submitted = st.form_submit_button("Add Document Metadata")

        if submitted:
            if uploaded_file is not None:
                st.session_state.uploaded_docs.append({
                    "type": doc_type,
                    "filename": uploaded_file.name,
                    "size": uploaded_file.size,
                })
                st.success("Document metadata added.")
            else:
                st.error("Please upload a file before adding document metadata.")

        if st.session_state.uploaded_docs:
            st.dataframe(pd.DataFrame(st.session_state.uploaded_docs), use_container_width=True)
        else:
            st.info("No document metadata added yet.")

# ----------------------------
# Risk Dashboard
# ----------------------------
elif page == "7. Risk Dashboard":
    st.title("Risk Dashboard and Readiness Score")

    score, explanation = completion_score()
    risk, label = risk_level(score)

    col1, col2, col3 = st.columns(3)
    col1.metric("Readiness Score", f"{score}/100")
    col2.metric("Risk Level", risk)
    col3.metric("Conflicts", len(detect_conflicts()))

    st.progress(score / 100)
    st.subheader(label)

    with st.expander("Score Explanation", expanded=True):
        for item in explanation:
            st.write(f"- {item}")

    st.subheader("Detected Partner Preference Conflicts")
    conflicts = detect_conflicts()
    if conflicts:
        st.dataframe(pd.DataFrame(conflicts), use_container_width=True)
    else:
        st.success("No major conflicts detected based on current responses.")

    st.subheader("Missing Document Checklist")
    missing = missing_documents()
    if missing:
        for doc in missing:
            st.warning(f"Missing: {doc}")
    else:
        st.success("All major supporting document categories are present.")

    st.subheader("Financial Disclosure Overview")
    asset_df = build_asset_df()
    debt_df = build_debt_df()

    if not asset_df.empty:
        st.markdown("#### Assets")
        st.dataframe(asset_df, use_container_width=True)

    if not debt_df.empty:
        st.markdown("#### Debts")
        st.dataframe(debt_df, use_container_width=True)

# ----------------------------
# Draft Preview
# ----------------------------
elif page == "8. Draft Preview":
    st.title("AI-Assisted Draft Preview")

    st.warning("This is a draft preview for attorney review only. It is not a final legal document.")

    draft = generate_draft_preview()
    st.text_area("Draft Preview", value=draft, height=500)

    summary_text = generate_summary_text()
    st.download_button(
        label="Download Lawyer-Ready Summary (.md)",
        data=downloadable_text(summary_text),
        file_name="knotwise_lawyer_ready_summary.md",
        mime="text/markdown",
    )

# ----------------------------
# Attorney Upgrade Page
# ----------------------------
elif page == "9. Attorney Review Upgrade":
    st.title("Premium Attorney Review Upgrade")
    st.write("This page is a mock premium workflow for the class project.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Basic Draft Package")
        st.write("$49 - $99")
        st.write("- Full questionnaire summary")
        st.write("- Draft preview")
        st.write("- Missing document checklist")
        st.write("- Conflict report")

    with col2:
        st.subheader("Attorney Review")
        st.write("$499 - $1,500+")
        st.write("- Attorney reviews draft")
        st.write("- Revisions included")
        st.write("- Jurisdiction-specific feedback")
        st.write("- Signing guidance")

    with col3:
        st.subheader("Concierge Package")
        st.write("$2,000+")
        st.write("- Two-attorney coordination")
        st.write("- Partner-specific review")
        st.write("- Notary/signing workflow")
        st.write("- Final execution checklist")

    st.info("Production version could integrate payments, attorney marketplace, e-signature, and notarization providers.")

# ----------------------------
# Requirements View
# ----------------------------
elif page == "10. Project Requirements View":
    st.title("Project Requirements Alignment")

    st.markdown("""
    ## Business Problem
    Prenup preparation can be expensive and inefficient because couples often lack organized disclosures,
    aligned preferences, and complete documentation before meeting attorneys.

    ## Functional Requirements Covered
    - Create case
    - Add partner
    - Partner A and Partner B questionnaires
    - Asset/debt disclosure
    - Supporting document upload metadata
    - Conflict detection
    - Readiness score
    - Draft preview
    - Lawyer-ready summary export
    - Mock attorney review upgrade

    ## Non-Functional Requirements Covered
    - Usability through Streamlit
    - Explainable scoring
    - Privacy-oriented design
    - Role concept for partners and attorney
    - Exportable report
    - Future scalable architecture

    ## Data Architecture
    Main entities:
    - Couple Case
    - Partner Profile
    - Assets
    - Debts
    - Prenup Goals
    - Uploaded Documents
    - Conflict Flags
    - Readiness Score
    - Draft Summary

    ## Application Architecture
    User → Streamlit UI → Forms → Session/Data Layer → Scoring Engine → Conflict Engine → Draft Generator → Export/Attorney Review

    ## Security Architecture
    Prototype demonstrates privacy concepts. Production should include authentication, role-based access,
    encryption, audit logs, secure document storage, and consent-based sharing.

    ## Testing Strategy
    - Unit test scoring logic
    - Unit test conflict detection
    - Form validation testing
    - End-to-end workflow testing
    - Security testing for role access in production
    """)
