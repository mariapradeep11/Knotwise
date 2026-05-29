
# KnotWise — AI Prenup Preparation Assistant

KnotWise is a Streamlit-based academic prototype that helps couples prepare for a prenuptial agreement by completing structured questionnaires, disclosing assets/debts, identifying preference conflicts, calculating a readiness score, and generating a lawyer-ready summary.

## Important Disclaimer

This project is for academic demonstration only. It is not legal advice and does not replace attorney review.

## Features

- Case setup
- Add/invite partner workflow
- Partner A questionnaire
- Partner B questionnaire
- Asset and debt disclosure
- Supporting document upload metadata
- Readiness score
- Conflict detection
- Draft preview
- Lawyer-ready summary export
- Mock attorney review upgrade page
- Requirements alignment page

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How to Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, and this `README.md`.
3. Go to Streamlit Community Cloud.
4. Connect your GitHub repository.
5. Select `app.py` as the main file.
6. Deploy.

## Suggested Demo Flow

1. Open Welcome page.
2. Create a case on Case Setup.
3. Add Partner using partner email.
4. Complete Partner A questionnaire.
5. Complete Partner B questionnaire.
6. Add sample assets, debts, and document metadata.
7. Open Risk Dashboard.
8. Show conflicts and readiness score.
9. Open Draft Preview and download lawyer-ready summary.
10. Show Attorney Review Upgrade page.

## Class Project Architecture

Prototype architecture:

User Browser → Streamlit App → Python Logic → Session State / CSV-style Data → Scoring Engine → Conflict Engine → Draft Generator → Export

Production architecture:

User Browser → Web App → API Layer → PostgreSQL Database → Secure Object Storage → AI Drafting Service → Attorney Review Portal → Monitoring and Logging
