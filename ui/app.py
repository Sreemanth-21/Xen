import streamlit as st
import copy
import time

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pulse — Customer Success Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  DESIGN SYSTEM  (XL Ventures-inspired: cream bg · forest green · serif)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
/* ── Reset ─────────────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { font-family: 'Inter', sans-serif; background: #F5F3EF; color: #1A1A1A; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2.5rem 3rem !important; max-width: 1440px !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #EDE9E3; }
::-webkit-scrollbar-thumb { background: #1A3D1A; border-radius: 3px; }

/* ── Brand Header ──────────────────────────────────────────────────────────── */
.pulse-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 28px 0 24px;
    border-bottom: 1px solid #D4CFC6;
    margin-bottom: 40px;
}
.pulse-logo-mark {
    font-family: 'EB Garamond', serif;
    font-size: 28px;
    font-weight: 700;
    color: #1A3D1A;
    letter-spacing: -0.02em;
}
.pulse-logo-sub {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8A8880;
    margin-top: 2px;
}
.nav-links { display: flex; gap: 32px; align-items: center; }
.nav-link {
    font-size: 13px;
    color: #5A5A55;
    text-decoration: none;
    font-weight: 500;
    letter-spacing: 0.01em;
}
.nav-status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 12px;
    font-weight: 600;
    color: #1A3D1A;
    background: #E8F0E8;
    border: 1px solid #C2D4C2;
    padding: 5px 14px;
    border-radius: 20px;
    letter-spacing: 0.04em;
}
.nav-status-dot {
    width: 7px;
    height: 7px;
    background: #1A3D1A;
    border-radius: 50%;
    animation: blink 2s infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Page Hero ─────────────────────────────────────────────────────────────── */
.page-hero {
    margin-bottom: 48px;
}
.page-hero-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #1A3D1A;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.page-hero-label::before {
    content: '';
    display: block;
    width: 28px;
    height: 1px;
    background: #1A3D1A;
}
.page-hero-headline {
    font-family: 'EB Garamond', serif;
    font-size: 56px;
    font-weight: 500;
    color: #0F0F0E;
    line-height: 1.08;
    letter-spacing: -0.025em;
    margin-bottom: 20px;
}
.page-hero-headline em {
    font-style: italic;
    color: #1A3D1A;
}
.page-hero-sub {
    font-size: 16px;
    color: #6B6B66;
    line-height: 1.6;
    max-width: 560px;
}

/* ── Section Labels ────────────────────────────────────────────────────────── */
.section-eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8A8880;
    margin-bottom: 10px;
}
.section-heading {
    font-family: 'EB Garamond', serif;
    font-size: 24px;
    font-weight: 600;
    color: #0F0F0E;
    margin-bottom: 4px;
}
hr.rule {
    border: none;
    border-top: 1px solid #D4CFC6;
    margin: 28px 0;
}

/* ── Input Area ────────────────────────────────────────────────────────────── */
.input-card {
    background: #FFFFFF;
    border: 1px solid #D4CFC6;
    border-radius: 12px;
    padding: 28px 28px 20px;
    margin-bottom: 32px;
}
.input-card:focus-within {
    border-color: #1A3D1A;
    box-shadow: 0 0 0 3px rgba(26,61,26,0.06);
}
textarea {
    background: transparent !important;
    border: none !important;
    color: #1A1A1A !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    resize: none !important;
    padding: 0 !important;
}
textarea:focus { box-shadow: none !important; }

/* ── Primary Button ────────────────────────────────────────────────────────── */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    transition: all 0.18s ease !important;
    letter-spacing: 0.01em !important;
}
.stButton > button[kind="primary"] {
    background: #1A3D1A !important;
    color: #F5F3EF !important;
    border: 1px solid #1A3D1A !important;
    box-shadow: 0 2px 8px rgba(26,61,26,0.2) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #0F2A0F !important;
    box-shadow: 0 4px 14px rgba(26,61,26,0.3) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:not([kind="primary"]) {
    background: #FFFFFF !important;
    color: #1A1A1A !important;
    border: 1px solid #D4CFC6 !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: #F0EDE8 !important;
    border-color: #1A3D1A !important;
    transform: translateY(-1px) !important;
}

/* ── Confidence Badge ──────────────────────────────────────────────────────── */
.badge-high {
    display: inline-flex; align-items: center; gap: 6px;
    background: #E8F0E8; border: 1px solid #A8C4A8;
    color: #1A3D1A; padding: 4px 12px;
    border-radius: 20px; font-size: 11px; font-weight: 700;
    letter-spacing: 0.04em;
}
.badge-low {
    display: inline-flex; align-items: center; gap: 6px;
    background: #FDF8EE; border: 1px solid #E6C870;
    color: #8A6A00; padding: 4px 12px;
    border-radius: 20px; font-size: 11px; font-weight: 700;
    letter-spacing: 0.04em;
}
.badge-dot-green { width:6px; height:6px; border-radius:50%; background:#1A3D1A; display:inline-block; }
.badge-dot-amber { width:6px; height:6px; border-radius:50%; background:#D4A017; display:inline-block; }

/* ── PCVL Tiles ────────────────────────────────────────────────────────────── */
.pcvl-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin: 20px 0; }
.pcvl-tile {
    background: #FFFFFF;
    border: 1px solid #D4CFC6;
    border-radius: 10px;
    padding: 18px 14px 14px;
    text-align: center;
    transition: border-color 0.18s, transform 0.18s;
}
.pcvl-tile:hover { border-color: #1A3D1A; transform: translateY(-2px); }
.pcvl-tile-label { font-size: 9px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: #8A8880; margin-bottom: 8px; }
.pcvl-tile-value { font-family: 'EB Garamond', serif; font-size: 34px; font-weight: 600; line-height: 1; }
.pcvl-g { color: #1A3D1A; }
.pcvl-b { color: #1A4060; }
.pcvl-p { color: #5A3080; }
.pcvl-k { color: #0F0F0E; }
.pcvl-tile-sub { font-size: 9px; color: #8A8880; margin-top: 4px; }

/* ── Confidence Meter ──────────────────────────────────────────────────────── */
.conf-track {
    background: #EDE9E3;
    border-radius: 4px;
    height: 6px;
    overflow: hidden;
    margin: 6px 0 0;
}
.conf-fill { height: 100%; border-radius: 4px; transition: width 0.8s ease; }

/* ── Explanation Quote ─────────────────────────────────────────────────────── */
.explanation-quote {
    border-left: 3px solid #1A3D1A;
    padding: 14px 18px;
    background: #F0EDE8;
    border-radius: 0 8px 8px 0;
    font-size: 14px;
    color: #2A2A25;
    line-height: 1.65;
    font-style: italic;
    margin: 16px 0;
}

/* ── Levers ────────────────────────────────────────────────────────────────── */
.lever-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #F0EDE8;
    border: 1px solid #D4CFC6;
    color: #3A3A35;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 500;
    margin-top: 10px;
}

/* ── Memory Diff ───────────────────────────────────────────────────────────── */
.memory-diff {
    background: #EDF5F0;
    border: 1px solid #A8C4B0;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 28px;
    font-size: 13px;
    color: #2A4A30;
    line-height: 1.6;
}
.memory-diff-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #1A3D1A;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Agent Thinking Tree ───────────────────────────────────────────────────── */
.agent-tree-wrap { margin-bottom: 40px; }

.agent-node {
    display: flex;
    gap: 0;
    margin-bottom: 0;
}
.agent-node-rail {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 44px;
    flex-shrink: 0;
}
.agent-node-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 2px solid #1A3D1A;
    background: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
    z-index: 1;
    transition: background 0.2s;
}
.agent-node-circle.active { background: #1A3D1A; }
.agent-node-circle.final  { background: #0F2A0F; border-color: #0F2A0F; }
.agent-node-line {
    width: 2px;
    flex: 1;
    min-height: 16px;
    background: linear-gradient(to bottom, #1A3D1A, #C2D4C2);
}

.agent-node-content {
    flex: 1;
    padding: 0 0 28px 16px;
}
.agent-node-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
    padding-top: 6px;
}
.agent-node-name {
    font-family: 'EB Garamond', serif;
    font-size: 19px;
    font-weight: 600;
    color: #0F0F0E;
}
.agent-node-role {
    font-size: 11px;
    color: #8A8880;
    font-weight: 500;
}
.agent-thought-box {
    background: #FFFFFF;
    border: 1px solid #D4CFC6;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 10px;
    font-size: 13px;
    color: #3A3A35;
    line-height: 1.6;
}
.agent-thought-label {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8A8880;
    margin-bottom: 6px;
}
.agent-output-box {
    background: #F0EDE8;
    border: 1px solid #D4CFC6;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    font-family: 'JetBrains Mono', monospace;
    color: #1A3D1A;
    margin-bottom: 10px;
    line-height: 1.5;
}
.agent-assumption-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #FDF8EE;
    border: 1px solid #E6C870;
    color: #7A5800;
    border-radius: 5px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
    margin-right: 6px;
    margin-bottom: 6px;
}

/* ── Before/After Cards ────────────────────────────────────────────────────── */
.cmp-before {
    background: #FDF3F3;
    border: 1px solid #F0BABA;
    border-radius: 10px;
    padding: 20px;
}
.cmp-after {
    background: #F0F7F0;
    border: 1px solid #A8C4A8;
    border-radius: 10px;
    padding: 20px;
}
.cmp-label {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.cmp-before .cmp-label { color: #C0392B; }
.cmp-after  .cmp-label { color: #1A3D1A; }
.cmp-action { font-family: 'EB Garamond', serif; font-size: 18px; font-weight: 600; }
.cmp-before .cmp-action { color: #C0392B; }
.cmp-after  .cmp-action { color: #1A3D1A; }
.cmp-stats { font-size: 12px; color: #6B6B66; margin-top: 8px; line-height: 1.8; }

/* ── Recommendation Card ───────────────────────────────────────────────────── */
.rec-card {
    background: #FFFFFF;
    border: 1px solid #C2D4C2;
    border-radius: 12px;
    padding: 28px;
    margin-bottom: 24px;
    box-shadow: 0 2px 12px rgba(26,61,26,0.06);
}

/* ── Evidence Cards ────────────────────────────────────────────────────────── */
.ev-card {
    background: #FFFFFF;
    border: 1px solid #D4CFC6;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 10px;
    transition: border-color 0.18s;
}
.ev-card:hover { border-color: #1A3D1A; }
.ev-text { font-size: 13px; color: #2A2A25; line-height: 1.55; margin-bottom: 10px; }
.ev-footer { display: flex; align-items: center; justify-content: space-between; }
.ev-source {
    background: #E8F0E8;
    border: 1px solid #A8C4A8;
    color: #1A3D1A;
    font-size: 10px;
    font-weight: 700;
    padding: 3px 9px;
    border-radius: 4px;
    letter-spacing: 0.04em;
}
.ev-score-bar { display: flex; align-items: center; gap: 8px; }
.ev-score-track { width: 52px; height: 3px; background: #EDE9E3; border-radius: 2px; overflow: hidden; }
.ev-score-fill { height: 100%; background: #1A3D1A; border-radius: 2px; }
.ev-score-num { font-size: 10px; color: #8A8880; font-family: 'JetBrains Mono', monospace; }

/* ── Status Chips ──────────────────────────────────────────────────────────── */
.chip { display:inline-flex; align-items:center; gap:5px; padding:3px 10px; border-radius:4px; font-size:10px; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; }
.chip-pending  { background:#FDF8EE; border:1px solid #E6C870; color:#8A6A00; }
.chip-approved { background:#E8F0E8; border:1px solid #A8C4A8; color:#1A3D1A; }
.chip-rejected { background:#FDECEA; border:1px solid #F0BABA; color:#B03020; }
.chip-editing  { background:#F0EAF8; border:1px solid #C8A8E0; color:#6030A0; }

/* ── HITL Banners ──────────────────────────────────────────────────────────── */
.banner {
    border-radius: 10px;
    padding: 20px 24px;
    margin-top: 16px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
}
.banner-approved { background: #E8F0E8; border: 1px solid #A8C4A8; }
.banner-rejected { background: #FDECEA; border: 1px solid #F0BABA; }
.banner-icon { font-size: 26px; }
.banner-title { font-family: 'EB Garamond', serif; font-size: 18px; font-weight: 600; }
.banner-approved .banner-title { color: #1A3D1A; }
.banner-rejected .banner-title { color: #B03020; }
.banner-sub { font-size: 12px; color: #6B6B66; margin-top: 3px; line-height: 1.5; }

/* ── Case strip ────────────────────────────────────────────────────────────── */
.case-strip {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 10px 0;
    margin-bottom: 32px;
    border-bottom: 1px solid #D4CFC6;
    font-size: 12px;
    color: #8A8880;
}
.case-strip code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #1A3D1A;
    background: #E8F0E8;
    padding: 2px 8px;
    border-radius: 4px;
}
.case-strip-sep { color: #D4CFC6; }

/* ── Sidebar ───────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #D4CFC6 !important;
}
[data-testid="stSidebar"] > div { padding: 1.5rem 1.25rem; }
.sb-section { font-size: 10px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #8A8880; margin: 20px 0 10px; padding-bottom: 6px; border-bottom: 1px solid #EDE9E3; }
.sb-stat { display: flex; justify-content: space-between; align-items: center; padding: 7px 0; border-bottom: 1px solid #F0EDE8; }
.sb-stat-label { font-size: 11px; color: #8A8880; }
.sb-stat-value { font-size: 12px; font-weight: 600; color: #1A1A1A; }
.health-track { background: #EDE9E3; border-radius: 3px; height: 4px; margin-top: 6px; overflow: hidden; }
.health-fill { height: 100%; border-radius: 3px; }

/* ── Selectbox / Input ─────────────────────────────────────────────────────── */
[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border-color: #D4CFC6 !important;
    color: #1A1A1A !important;
    border-radius: 8px !important;
}
[data-baseweb="select"] > div:focus-within { border-color: #1A3D1A !important; }
.stTextInput > div > input {
    background: #FFFFFF !important;
    border: 1px solid #D4CFC6 !important;
    border-radius: 6px !important;
    color: #1A1A1A !important;
    font-size: 13px !important;
}
.stTextInput > div > input:focus { border-color: #1A3D1A !important; box-shadow: 0 0 0 3px rgba(26,61,26,0.06) !important; }
.stRadio label { font-size: 13px !important; color: #3A3A35 !important; }

/* Expander */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #D4CFC6 !important;
    border-radius: 8px !important;
    margin-bottom: 10px !important;
}
[data-testid="stExpander"]:hover { border-color: #1A3D1A !important; }

/* Spinner */
.stSpinner > div { border-top-color: #1A3D1A !important; }

/* Selectbox label */
.stSelectbox > label, .stTextArea > label, .stTextInput > label, .stRadio > label > div > p {
    color: #5A5A55 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SCENARIO DATA  (enriched with agent_thoughts tree)
# ─────────────────────────────────────────────────────────────────────────────
SCENARIOS = {
    "🔴  ACME Corp — Churn Risk": {
        "case_id": "PULSE-2024-ACME-101",
        "raw_input": (
            "ACME Corp's lead CSM reports that usage of key dashboards has dropped 40% in the last "
            "30 days. The primary champion VP of Product left the company last week, and they are "
            "currently on an annual contract renewing in 90 days. Need immediate playbook action."
        ),
        "customer_profile": {
            "name": "ACME Corp", "contract_type": "Enterprise (Annual)",
            "contract_value": "$120,000 ARR", "tenure_months": 18,
            "active_users": 45, "health_score": 42,
        },
        "assumptions": {
            "contract_type": {
                "value": "Enterprise (Annual)",
                "description": "Inferred from company domain and seat count patterns. Not confirmed in CRM.",
                "agent": "Ingestion",
                "type": "select",
                "options": ["Enterprise (Annual)", "Enterprise (Monthly)", "Self-Serve (Monthly)", "SMB"],
            },
            "renewing_in_90_days": {
                "value": "Yes",
                "description": "Assumed based on calendar-year sync. No explicit renewal date in CRM.",
                "agent": "Ingestion",
                "type": "radio",
                "options": ["Yes", "No"],
            },
        },
        "retrieved_evidence": [
            {
                "text": "Enterprise clients with usage drops >30% and VP transitions should receive an Executive Business Review (EBR) within 7 days.",
                "source": "Churn Prevention Playbook v2.4",
                "score": 0.89,
            },
            {
                "text": "ACME Corp usage logs show login counts went from 110/week to 65/week over the past 30 days.",
                "source": "Telemetry Database",
                "score": 0.82,
            },
        ],
        "recommendation": {
            "action": "Schedule Executive Business Review (EBR)",
            "propensity": 0.85, "context": 0.78, "value": 0.90,
            "levers": "Add 3-month trial of Premium Support & schedule VP-level meeting.",
            "priority": 5.97, "confidence": 0.88,
        },
        "explanation": (
            "The model recommends scheduling an Executive Business Review (EBR) with ACME Corp immediately. "
            "Evidence from the Churn Prevention Playbook v2.4 indicates that enterprise clients experiencing "
            "usage drops exceeding 30% alongside executive champion departures require an EBR within 7 days. "
            "Telemetry confirms a 40% dashboard login drop. Confidence is 0.88 — strong signal."
        ),
        "agent_thoughts": [
            {
                "agent": "Planner", "icon": "🧭", "role": "Orchestration Planner",
                "thought": "I received a raw CRM signal and assessed what information is missing. I determined the optimal agent routing: Ingestion first (to parse structured profile data), then Retrieval (to find matching playbooks), then Reasoning (to score recommendations), then Explainability (to generate the rationale).",
                "output": "Routing sequence: Ingestion → Retrieval → Reasoning → Explainability → [HITL Gate]",
                "assumptions_keys": [],
                "status": "complete",
            },
            {
                "agent": "Ingestion", "icon": "📥", "role": "Data Ingestion Agent",
                "thought": "I parsed the CRM note and extracted a structured customer profile. I identified 2 fields that are absent from the CRM record and had to infer them from contextual signals. These assumptions are flagged for human review.",
                "output": "Profile extracted: ACME Corp · 45 active users · Health score: 42/100 · 18-month tenure\n⚠ 2 assumptions flagged: contract_type, renewing_in_90_days",
                "assumptions_keys": ["contract_type", "renewing_in_90_days"],
                "status": "complete",
            },
            {
                "agent": "Retrieval", "icon": "🔍", "role": "Knowledge Retrieval Agent",
                "thought": "I queried the Chroma vector store with the enriched customer profile as the retrieval context. I found 2 highly relevant playbook chunks from the knowledge base. Both exceeded the relevance threshold of 0.75.",
                "output": "Retrieved 2 chunks · Top score: 0.89 · Source: Churn Prevention Playbook v2.4",
                "assumptions_keys": [],
                "status": "complete",
            },
            {
                "agent": "Reasoning", "icon": "⚖️", "role": "Reasoning & Scoring Agent",
                "thought": "I computed the PCVL priority score using the customer profile and evidence. The high propensity (0.85) is driven by the usage drop and champion departure. Context (0.78) reflects time-critical renewal window. Value (0.90) reflects $120K ARR at risk. The final priority score is 5.97.",
                "output": "Priority = P(0.85) × C(0.78) × V(0.90) × L(10) = 5.97\nRecommended action: Schedule Executive Business Review (EBR)",
                "assumptions_keys": [],
                "status": "complete",
            },
            {
                "agent": "Explainability", "icon": "💬", "role": "Explainability Agent",
                "thought": "I composed a human-readable rationale for the CSM by combining the recommendation, evidence citations, and confidence level. Confidence (0.88) is high enough that no low-confidence warning is needed. I cited both the playbook and telemetry sources explicitly.",
                "output": "Explanation generated · Confidence: 0.88 · No warning flags triggered",
                "assumptions_keys": [],
                "status": "complete",
            },
            {
                "agent": "HITL Gate", "icon": "🛑", "role": "Human-in-the-Loop Interrupt",
                "thought": "Execution is paused. The orchestration layer has completed its analysis. Control is now with the CSM. The recommended action will not be executed until a human decision (Approve, Edit, or Reject) is submitted.",
                "output": "Status: pending_review · Awaiting CSM decision",
                "assumptions_keys": [],
                "status": "waiting",
            },
        ],
        "memory_diff": {
            "past_recommendation": "Send Automated Churn Survey Email",
            "human_correction": "Schedule Executive Business Review (EBR)",
            "context": "Similar case found (ACME Corp, 6 months ago, relevance 0.87). CSM override recorded.",
        },
    },

    "🟢  Globex Inc — Expansion": {
        "case_id": "PULSE-2024-GLOBEX-202",
        "raw_input": (
            "Globex Inc has added 50 new seats this month, hitting 98% utilization. "
            "The new Director of Customer Experience expressed interest in our premium analytics add-on. "
            "They are currently on a self-serve monthly plan."
        ),
        "customer_profile": {
            "name": "Globex Inc", "contract_type": "Self-Serve (Monthly)",
            "contract_value": "$15,000 ARR", "tenure_months": 6,
            "active_users": 150, "health_score": 92,
        },
        "assumptions": {
            "contract_type": {
                "value": "Self-Serve (Monthly)",
                "description": "Inferred from subscription tier metadata. Not explicitly confirmed.",
                "agent": "Ingestion",
                "type": "select",
                "options": ["Self-Serve (Monthly)", "Enterprise (Monthly)", "Enterprise (Annual)", "SMB"],
            },
        },
        "retrieved_evidence": [
            {
                "text": "Accounts with seat utilization >90% and positive champion feedback should be pitched the Enterprise Upgrade Plan.",
                "source": "Account Expansion Playbook",
                "score": 0.94,
            },
        ],
        "recommendation": {
            "action": "Propose Enterprise Upgrade Plan",
            "propensity": 0.92, "context": 0.80, "value": 0.75,
            "levers": "Offer 15% discount on 2-year contract lock-in.",
            "priority": 6.62, "confidence": 0.94,
        },
        "explanation": (
            "The model recommends proposing an Enterprise Upgrade Plan to Globex Inc. "
            "According to the Account Expansion Playbook (relevance 0.94), accounts exceeding 90% seat "
            "utilization with positive champion signals are prime expansion candidates. "
            "With 150 active users at 98% utilization and a new champion engaged, all signals point "
            "to high-propensity expansion. Confidence: 0.94."
        ),
        "agent_thoughts": [
            {
                "agent": "Planner", "icon": "🧭", "role": "Orchestration Planner",
                "thought": "I detected a strong expansion signal in the input: seat utilization near capacity and a new champion expressing interest. I routed to Ingestion to structure the account data, then Retrieval for expansion playbooks, then Reasoning to compute the priority score.",
                "output": "Routing sequence: Ingestion → Retrieval → Reasoning → Explainability → [HITL Gate]",
                "assumptions_keys": [], "status": "complete",
            },
            {
                "agent": "Ingestion", "icon": "📥", "role": "Data Ingestion Agent",
                "thought": "I parsed the engagement signal and extracted the customer profile. I found 1 field that required inference: the contract type was not explicitly stated in the input and was inferred from subscription tier metadata.",
                "output": "Profile extracted: Globex Inc · 150 active users · Health score: 92/100\n⚠ 1 assumption flagged: contract_type",
                "assumptions_keys": ["contract_type"], "status": "complete",
            },
            {
                "agent": "Retrieval", "icon": "🔍", "role": "Knowledge Retrieval Agent",
                "thought": "I found a highly relevant expansion playbook chunk with a relevance score of 0.94 — above our high-confidence threshold of 0.90. This strongly supports the enterprise upgrade recommendation.",
                "output": "Retrieved 1 chunk · Score: 0.94 · Source: Account Expansion Playbook",
                "assumptions_keys": [], "status": "complete",
            },
            {
                "agent": "Reasoning", "icon": "⚖️", "role": "Reasoning & Scoring Agent",
                "thought": "I computed the PCVL priority score. Very high propensity (0.92) driven by 98% seat utilization and new champion. Moderate value score (0.75) given current low ARR — but expansion would dramatically increase LTV. Priority score: 6.62.",
                "output": "Priority = P(0.92) × C(0.80) × V(0.75) × L(12) = 6.62\nRecommended: Propose Enterprise Upgrade Plan",
                "assumptions_keys": [], "status": "complete",
            },
            {
                "agent": "Explainability", "icon": "💬", "role": "Explainability Agent",
                "thought": "I generated the rationale citing the Account Expansion Playbook. Confidence (0.94) is very high — no uncertainty warnings needed. The explanation is clear and direct for the CSM to act on.",
                "output": "Explanation generated · Confidence: 0.94 · No warnings triggered",
                "assumptions_keys": [], "status": "complete",
            },
            {
                "agent": "HITL Gate", "icon": "🛑", "role": "Human-in-the-Loop Interrupt",
                "thought": "Orchestration complete. CSM approval required before triggering the enterprise upgrade outreach sequence. High confidence but human oversight is mandatory.",
                "output": "Status: pending_review · Awaiting CSM decision",
                "assumptions_keys": [], "status": "waiting",
            },
        ],
        "memory_diff": None,
    },

    "🟡  Initech Co — Low Confidence": {
        "case_id": "PULSE-2024-INITECH-303",
        "raw_input": (
            "Initech Co shows fluctuating API usage. A junior support ticket mentions they might be "
            "migrating to a competitor, but the customer contact hasn't responded. No executive "
            "sponsor listed."
        ),
        "customer_profile": {
            "name": "Initech Co", "contract_type": "Enterprise",
            "contract_value": "$50,000 ARR", "tenure_months": 12,
            "active_users": 12, "health_score": 60,
        },
        "assumptions": {
            "contract_type": {
                "value": "Enterprise",
                "description": "Assumed Enterprise based on historical ticket priority. No contract data in CRM.",
                "agent": "Ingestion",
                "type": "select",
                "options": ["Enterprise (Annual)", "Enterprise (Monthly)", "Self-Serve (Monthly)", "SMB"],
            },
            "decision_maker_active": {
                "value": "No",
                "description": "Inferred inactive because no executive sponsor is listed in CRM. Unverified.",
                "agent": "Ingestion",
                "type": "radio",
                "options": ["Yes", "No"],
            },
        },
        "retrieved_evidence": [
            {
                "text": "If customer migration is suspected but unconfirmed, schedule High-Touch Outreach. Do not automate emails.",
                "source": "Competitor Defeat Playbook",
                "score": 0.65,
            },
        ],
        "recommendation": {
            "action": "Trigger High-Touch Outreach Call",
            "propensity": 0.45, "context": 0.65, "value": 0.40,
            "levers": "No discount. Assign senior CSM to call directly.",
            "priority": 1.17, "confidence": 0.35,
        },
        "explanation": (
            "The model recommends a High-Touch Outreach Call for Initech Co. "
            "Low confidence (0.35) — recommend human judgment over automation. "
            "The Competitor Defeat Playbook (relevance 0.65) advises against automated outreach when "
            "migration is suspected but unconfirmed. Two key profile fields (contract_type, decision_maker_active) "
            "remain unverified assumptions, significantly reducing model certainty."
        ),
        "agent_thoughts": [
            {
                "agent": "Planner", "icon": "🧭", "role": "Orchestration Planner",
                "thought": "The input signal is ambiguous — potential competitor migration mentioned but unconfirmed, no executive contact identified. I routed conservatively: Ingestion to extract what we know, Retrieval to find competitor-defeat playbooks, Reasoning to assess whether we have enough signal to recommend action confidently.",
                "output": "Routing sequence: Ingestion → Retrieval → Reasoning → Explainability → [HITL Gate]",
                "assumptions_keys": [], "status": "complete",
            },
            {
                "agent": "Ingestion", "icon": "📥", "role": "Data Ingestion Agent",
                "thought": "I extracted limited profile data — only 12 active users and no executive sponsor listed. I had to infer 2 critical fields that are absent from the CRM: contract_type and decision_maker_active. These are high-uncertainty inferences that need human correction.",
                "output": "Sparse profile: Initech Co · 12 active users · Health: 60/100\n⚠ 2 assumptions flagged (HIGH UNCERTAINTY): contract_type, decision_maker_active",
                "assumptions_keys": ["contract_type", "decision_maker_active"], "status": "complete",
            },
            {
                "agent": "Retrieval", "icon": "🔍", "role": "Knowledge Retrieval Agent",
                "thought": "I found 1 relevant playbook chunk with a relevance score of 0.65 — below our high-confidence threshold of 0.80. The match is directionally correct but weak. This contributes to the overall low confidence in the recommendation.",
                "output": "Retrieved 1 chunk · Score: 0.65 (weak) · Source: Competitor Defeat Playbook",
                "assumptions_keys": [], "status": "complete",
            },
            {
                "agent": "Reasoning", "icon": "⚖️", "role": "Reasoning & Scoring Agent",
                "thought": "PCVL scoring returned weak numbers across all dimensions. Low propensity (0.45) because migration signal is unconfirmed. Low value score (0.40) because decision-maker is assumed inactive. Priority score of 1.17 is the lowest of all processed cases. Model confidence: 0.35 — well below the human-review threshold.",
                "output": "Priority = P(0.45) × C(0.65) × V(0.40) × L(10) = 1.17\n⚠ Confidence: 0.35 — below threshold · Human judgment strongly recommended",
                "assumptions_keys": [], "status": "complete",
            },
            {
                "agent": "Explainability", "icon": "💬", "role": "Explainability Agent",
                "thought": "I detected that confidence (0.35) is below the 0.5 threshold. Per protocol, I appended a mandatory human-judgment warning to the explanation. The rationale cites the Competitor Defeat Playbook but explicitly flags that two key assumptions are unverified.",
                "output": "Explanation generated · ⚠ LOW CONFIDENCE WARNING inserted · Unverified assumptions cited",
                "assumptions_keys": [], "status": "complete",
            },
            {
                "agent": "HITL Gate", "icon": "🛑", "role": "Human-in-the-Loop Interrupt",
                "thought": "Execution halted — low confidence case. This recommendation MUST NOT be auto-executed. CSM intervention is required. Correction of the 2 flagged assumptions in the Ingestion node will significantly improve model certainty.",
                "output": "Status: pending_review · ⚠ Low confidence — human decision mandatory",
                "assumptions_keys": [], "status": "waiting",
            },
        ],
        "memory_diff": None,
    },
}

SCENARIO_KEYS = list(SCENARIOS.keys())

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "scenario_name" not in st.session_state:
    st.session_state.scenario_name = SCENARIO_KEYS[0]
if "case_data" not in st.session_state:
    st.session_state.case_data = copy.deepcopy(SCENARIOS[st.session_state.scenario_name])
if "stage" not in st.session_state:
    st.session_state.stage = "input"
if "original_rec" not in st.session_state:
    st.session_state.original_rec = None
if "node_edit_open" not in st.session_state:
    st.session_state.node_edit_open = {}   # {agent_name: bool}


def load_scenario(name: str):
    st.session_state.scenario_name = name
    st.session_state.case_data = copy.deepcopy(SCENARIOS[name])
    st.session_state.stage = "input"
    st.session_state.original_rec = None
    st.session_state.node_edit_open = {}


# ─────────────────────────────────────────────────────────────────────────────
#  NAVIGATION HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="pulse-nav">
  <div>
    <div class="pulse-logo-mark">Pulse</div>
    <div class="pulse-logo-sub">Customer Success Intelligence</div>
  </div>
  <div class="nav-links">
    <span class="nav-link">Cases</span>
    <span class="nav-link">Playbooks</span>
    <span class="nav-link">Memory</span>
    <span class="nav-link">Settings</span>
    <span class="nav-status"><span class="nav-status-dot"></span>Agent Online</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:EB Garamond,serif; font-size:20px; font-weight:600; color:#1A3D1A; margin-bottom:4px;">Case Runner</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px; color:#8A8880; margin-bottom:16px;">Select a scenario to analyse</div>', unsafe_allow_html=True)

    selected = st.selectbox(
        "Scenario",
        options=SCENARIO_KEYS,
        index=SCENARIO_KEYS.index(st.session_state.scenario_name),
        label_visibility="collapsed",
    )
    if selected != st.session_state.scenario_name:
        load_scenario(selected)
        st.rerun()

    profile = st.session_state.case_data["customer_profile"]
    health  = profile.get("health_score", 50)
    h_color = "#1A3D1A" if health >= 75 else "#D4A017" if health >= 50 else "#C0392B"

    st.markdown('<div class="sb-section">Active Account</div>', unsafe_allow_html=True)
    for label, val in [
        ("Account",   profile["name"]),
        ("ARR",       profile["contract_value"]),
        ("Contract",  profile["contract_type"]),
        ("Tenure",    f"{profile['tenure_months']} months"),
        ("Users",     str(profile["active_users"])),
    ]:
        st.markdown(f'<div class="sb-stat"><span class="sb-stat-label">{label}</span><span class="sb-stat-value">{val}</span></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding: 8px 0 4px;">
        <div class="sb-stat">
            <span class="sb-stat-label">Health Score</span>
            <span class="sb-stat-value" style="color:{h_color};">{health}/100</span>
        </div>
        <div class="health-track">
            <div class="health-fill" style="width:{health}%; background:{h_color};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    stage_map = {
        "input":     ("chip-pending",  "Awaiting Input"),
        "review":    ("chip-pending",  "Pending Review"),
        "edit_mode": ("chip-editing",  "Editing Node"),
        "edited":    ("chip-editing",  "Re-evaluated"),
        "approved":  ("chip-approved", "Approved"),
        "rejected":  ("chip-rejected", "Rejected"),
    }
    cls, lbl = stage_map.get(st.session_state.stage, ("chip-pending", "Unknown"))
    st.markdown('<div class="sb-section">Flow State</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="chip {cls}">{lbl}</span>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  STAGE 1 — INPUT
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.stage == "input":
    # Hero
    st.markdown("""
    <div class="page-hero">
        <div class="page-hero-label">Customer Intelligence</div>
        <div class="page-hero-headline">What is the <em>next best action</em><br>for this account?</div>
        <div class="page-hero-sub">
            Paste a CRM note, support transcript, or engagement signal.
            The AI orchestration layer will route it through specialised agents and surface a
            recommended action with full reasoning transparency.
        </div>
    </div>
    """, unsafe_allow_html=True)

    raw = st.text_area(
        "Signal",
        value=st.session_state.case_data["raw_input"],
        height=148,
        placeholder="Paste CRM note, support ticket, or engagement signal…",
        label_visibility="collapsed",
    )

    c1, c2 = st.columns([2, 6])
    with c1:
        go = st.button("⚡  Analyse Case", type="primary", use_container_width=True)
    with c2:
        st.markdown(
            '<div style="padding-top:10px; font-size:12px; color:#8A8880;">'
            'Routes through <code style="color:#1A3D1A; background:#E8F0E8; padding:2px 7px; border-radius:4px;">POST /process</code>'
            ' — LangGraph orchestration · Chroma retrieval · Groq reasoning</div>',
            unsafe_allow_html=True,
        )

    if go:
        st.session_state.case_data["raw_input"] = raw
        with st.spinner("Running orchestration pipeline…"):
            time.sleep(1.4)
        st.session_state.stage = "review"
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
#  STAGE 2+ — REVIEW / EDIT / APPROVE / REJECT
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.stage in ["review", "approved", "rejected", "edit_mode", "edited"]:
    case = st.session_state.case_data
    rec  = case["recommendation"]
    conf = rec["confidence"]

    # Case identity strip
    st.markdown(f"""
    <div class="case-strip">
        <code>{case['case_id']}</code>
        <span class="case-strip-sep">·</span>
        <span>{case['customer_profile']['name']}</span>
        <span class="case-strip-sep">·</span>
        <span>{case['customer_profile']['contract_value']}</span>
        <span class="case-strip-sep">·</span>
        <span style="margin-left:auto; color:#1A3D1A; font-weight:600;">Awaiting CSM decision</span>
    </div>
    """, unsafe_allow_html=True)

    # Memory Diff
    mem = case.get("memory_diff")
    if mem:
        st.markdown(f"""
        <div class="memory-diff">
            <div class="memory-diff-label">⟳ Memory Diff — Similar Past Interaction</div>
            Previously recommended <strong>"{mem['past_recommendation']}"</strong> —
            the CSM corrected it to <strong>"{mem['human_correction']}"</strong>.
            <span style="color:#5A7A5A; font-size:12px; display:block; margin-top:4px;">{mem['context']}</span>
        </div>
        """, unsafe_allow_html=True)

    left, right = st.columns([5, 3], gap="large")

    # ── LEFT — Agent Thinking Tree ─────────────────────────────────────────
    with left:
        st.markdown("""
        <div style="margin-bottom:20px;">
            <div class="section-eyebrow">Reasoning Trace</div>
            <div class="section-heading">How the agents reasoned</div>
            <div style="font-size:13px; color:#6B6B66; margin-top:4px;">
                Each node shows what the agent thought, what it produced, and any assumptions you can correct.
            </div>
        </div>
        """, unsafe_allow_html=True)

        all_assumptions = case.get("assumptions", {})
        agent_thoughts  = case.get("agent_thoughts", [])
        total_nodes     = len(agent_thoughts)

        for idx, node in enumerate(agent_thoughts):
            is_last    = (idx == total_nodes - 1)
            is_waiting = node["status"] == "waiting"
            circle_cls = "final" if is_waiting else "active" if not is_last else "active"
            node_assumptions = {k: v for k, v in all_assumptions.items() if k in node["assumptions_keys"]}
            has_assumptions  = bool(node_assumptions)
            edit_key         = f"edit_open_{node['agent']}"

            if edit_key not in st.session_state.node_edit_open:
                st.session_state.node_edit_open[edit_key] = False

            # ── Node HTML ───────────────────────────────────────────────────
            line_html = "" if is_last else '<div class="agent-node-line"></div>'
            circle_bg  = "#1A3D1A" if not is_waiting else "#0F2A0F"
            circle_icon = node["icon"]

            st.markdown(f"""
            <div class="agent-node">
              <div class="agent-node-rail">
                <div class="agent-node-circle" style="background:{circle_bg}; border-color:{circle_bg};">
                    <span style="font-size:14px;">{circle_icon}</span>
                </div>
                {line_html}
              </div>
              <div class="agent-node-content">
                <div class="agent-node-header">
                    <div>
                        <div class="agent-node-name">{node['agent']}</div>
                        <div class="agent-node-role">{node['role']}</div>
                    </div>
                </div>
                <div class="agent-thought-box">
                    <div class="agent-thought-label">💭 Internal Reasoning</div>
                    {node['thought']}
                </div>
                <div class="agent-output-box">{node['output']}</div>
            """, unsafe_allow_html=True)

            # Assumption tags
            if has_assumptions:
                tags_html = "".join([
                    f'<span class="agent-assumption-tag">⚠ {k.replace("_"," ")}</span>'
                    for k in node_assumptions.keys()
                ])
                st.markdown(f'<div style="margin-bottom:8px;">{tags_html}</div>', unsafe_allow_html=True)

            st.markdown("</div></div>", unsafe_allow_html=True)

            # Inline assumption editor per node
            if has_assumptions and st.session_state.stage in ["review", "edited"]:
                toggle_label = "▼ Correct assumptions" if not st.session_state.node_edit_open[edit_key] else "▲ Close editor"
                col_t, _ = st.columns([2, 5])
                with col_t:
                    if st.button(toggle_label, key=f"toggle_{node['agent']}"):
                        st.session_state.node_edit_open[edit_key] = not st.session_state.node_edit_open[edit_key]
                        st.rerun()

                if st.session_state.node_edit_open[edit_key]:
                    st.markdown(f"""
                    <div style="margin: 0 0 8px 44px; background:#FFFDF5; border:1px solid #E6C870;
                                border-radius:10px; padding:18px 20px;">
                        <div style="font-size:10px; font-weight:700; letter-spacing:0.12em;
                                    text-transform:uppercase; color:#8A6A00; margin-bottom:14px;">
                            ✏ Edit {node['agent']} Assumptions
                        </div>
                    """, unsafe_allow_html=True)

                    edited_vals = {}
                    for k, meta in node_assumptions.items():
                        st.markdown(f"""
                        <div style="font-size:11px; color:#6B6B66; margin-bottom:6px;">
                            <b style="color:#0F0F0E;">{k.replace('_',' ').title()}</b>
                            — {meta['description']}
                        </div>
                        """, unsafe_allow_html=True)

                        if meta["type"] == "select":
                            edited_vals[k] = st.selectbox(
                                f"Value for {k}",
                                options=meta["options"],
                                index=meta["options"].index(meta["value"]) if meta["value"] in meta["options"] else 0,
                                key=f"val_{node['agent']}_{k}",
                                label_visibility="collapsed",
                            )
                        elif meta["type"] == "radio":
                            edited_vals[k] = st.radio(
                                f"Value for {k}",
                                options=meta["options"],
                                index=meta["options"].index(meta["value"]) if meta["value"] in meta["options"] else 0,
                                key=f"val_{node['agent']}_{k}",
                                horizontal=True,
                                label_visibility="collapsed",
                            )
                        else:
                            edited_vals[k] = st.text_input(
                                f"Value for {k}",
                                value=meta["value"],
                                key=f"val_{node['agent']}_{k}",
                                label_visibility="collapsed",
                            )

                    st.markdown("</div>", unsafe_allow_html=True)
                    st.write("")

                    col_s, col_c, _ = st.columns([2, 2, 4])
                    with col_s:
                        if st.button(f"🔄 Resubmit via {node['agent']}", type="primary", key=f"submit_{node['agent']}"):
                            st.session_state.original_rec = copy.deepcopy(rec)

                            # Apply edits to profile and assumptions
                            for k, v in edited_vals.items():
                                st.session_state.case_data["customer_profile"][k] = v
                                if k in st.session_state.case_data["assumptions"]:
                                    del st.session_state.case_data["assumptions"][k]
                                # Also remove from agent_thoughts assumptions_keys
                                for n in st.session_state.case_data["agent_thoughts"]:
                                    if k in n["assumptions_keys"]:
                                        n["assumptions_keys"].remove(k)

                            with st.spinner(f"Re-routing from {node['agent']} → Reasoning → Explainability…"):
                                time.sleep(1.0)

                            # Mock recalculation
                            r = st.session_state.case_data["recommendation"]
                            if "ACME" in st.session_state.scenario_name:
                                r["action"]     = "Propose Enterprise Upgrade Plan"
                                r["propensity"] = 0.95
                                r["context"]    = 0.85
                                r["confidence"] = 0.95
                                r["priority"]   = 7.26
                                st.session_state.case_data["explanation"] = (
                                    "Following human correction confirming the Enterprise contract and 90-day renewal, "
                                    "the Reasoning Agent recomputed PCVL. New recommendation: Propose Enterprise Upgrade "
                                    "Plan with a 15% promotional incentive. Confidence elevated to 0.95."
                                )
                                # Update HITL Gate node thought
                                for n in st.session_state.case_data["agent_thoughts"]:
                                    if n["agent"] == "Reasoning":
                                        n["output"] = "Priority = P(0.95) × C(0.85) × V(0.90) × L(10) = 7.26\nRe-recommended: Propose Enterprise Upgrade Plan"
                                    if n["agent"] == "Explainability":
                                        n["output"] = "Re-generated explanation · Confidence: 0.95 · No warnings"
                            else:
                                r["confidence"] = min(r["confidence"] + 0.15, 1.0)
                                r["propensity"] = min(r["propensity"] + 0.10, 1.0)
                                st.session_state.case_data["explanation"] = (
                                    "Recommendation updated following correction of flagged assumptions. "
                                    "Confidence improved with verified profile data."
                                )

                            st.session_state.node_edit_open[edit_key] = False
                            st.session_state.stage = "edited"
                            st.rerun()

                    with col_c:
                        if st.button("Cancel", key=f"cancel_{node['agent']}"):
                            st.session_state.node_edit_open[edit_key] = False
                            st.rerun()

            st.markdown('<hr class="rule">', unsafe_allow_html=True)

        # Before / After comparison
        if st.session_state.stage == "edited" and st.session_state.original_rec:
            orig = st.session_state.original_rec
            priority_new = rec["propensity"] * rec["context"] * rec["value"] * 10
            st.markdown("""
            <div style="margin: 8px 0 16px;">
                <div class="section-eyebrow">Edit Result</div>
                <div class="section-heading">Before vs After</div>
            </div>
            """, unsafe_allow_html=True)
            ca, cb = st.columns(2, gap="medium")
            with ca:
                st.markdown(f"""
                <div class="cmp-before">
                    <div class="cmp-label">Before Edit</div>
                    <div class="cmp-action">{orig['action']}</div>
                    <div class="cmp-stats">
                        Confidence &nbsp;<strong style="color:#C0392B">{orig['confidence']:.2f}</strong><br>
                        Priority &nbsp;<strong style="color:#C0392B">{orig['priority']:.2f}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with cb:
                st.markdown(f"""
                <div class="cmp-after">
                    <div class="cmp-label">After Edit</div>
                    <div class="cmp-action">{rec['action']}</div>
                    <div class="cmp-stats">
                        Confidence &nbsp;<strong style="color:#1A3D1A">{rec['confidence']:.2f}</strong><br>
                        Priority &nbsp;<strong style="color:#1A3D1A">{priority_new:.2f}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.write("")

    # ── RIGHT — Recommendation + Actions ─────────────────────────────────
    with right:
        priority_val = rec["propensity"] * rec["context"] * rec["value"] * 10

        if conf >= 0.5:
            badge_html  = f'<span class="badge-high"><span class="badge-dot-green"></span>High Confidence · {conf:.2f}</span>'
            meter_color = "#1A3D1A"
        else:
            badge_html  = f'<span class="badge-low"><span class="badge-dot-amber"></span>Low Confidence · {conf:.2f} — Human Review Required</span>'
            meter_color = "#D4A017"

        st.markdown(f"""
        <div class="rec-card">
            <div class="section-eyebrow" style="margin-bottom:6px;">Recommended Action</div>
            <div style="font-family:'EB Garamond',serif; font-size:28px; font-weight:600;
                        color:#0F0F0E; line-height:1.15; margin-bottom:12px;">
                {rec['action']}
            </div>
            {badge_html}

            <!-- Confidence Meter -->
            <div style="margin-top:14px; margin-bottom:4px;">
                <div style="display:flex; justify-content:space-between; font-size:10px; color:#8A8880; margin-bottom:4px;">
                    <span>CONFIDENCE</span><span>{conf*100:.0f}%</span>
                </div>
                <div class="conf-track">
                    <div class="conf-fill" style="width:{conf*100}%; background:{meter_color};"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # PCVL Tiles
        st.markdown('<div class="section-eyebrow">PCVL Scoring — Visible Math</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="pcvl-row">
            <div class="pcvl-tile">
                <div class="pcvl-tile-label">Propensity</div>
                <div class="pcvl-tile-value pcvl-g">{rec['propensity']:.2f}</div>
                <div class="pcvl-tile-sub">likelihood</div>
            </div>
            <div class="pcvl-tile">
                <div class="pcvl-tile-label">Context</div>
                <div class="pcvl-tile-value pcvl-b">{rec['context']:.2f}</div>
                <div class="pcvl-tile-sub">relevance</div>
            </div>
            <div class="pcvl-tile">
                <div class="pcvl-tile-label">Value</div>
                <div class="pcvl-tile-value pcvl-p">{rec['value']:.2f}</div>
                <div class="pcvl-tile-sub">account LTV</div>
            </div>
            <div class="pcvl-tile" style="border-color:#C2D4C2; background:#F0F7F0;">
                <div class="pcvl-tile-label">Priority</div>
                <div class="pcvl-tile-value pcvl-k">{priority_val:.2f}</div>
                <div class="pcvl-tile-sub">P×C×V×L</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Explanation
        st.markdown(f'<div class="explanation-quote">"{case["explanation"]}"</div>', unsafe_allow_html=True)

        # Levers
        st.markdown(f'<div class="lever-pill">⚙ {rec["levers"]}</div>', unsafe_allow_html=True)

        st.markdown('<hr class="rule">', unsafe_allow_html=True)

        # Evidence
        st.markdown('<div class="section-eyebrow">Retrieved Evidence</div>', unsafe_allow_html=True)
        for ev in case.get("retrieved_evidence", []):
            pct = int(ev["score"] * 100)
            st.markdown(f"""
            <div class="ev-card">
                <div class="ev-text">"{ev['text']}"</div>
                <div class="ev-footer">
                    <span class="ev-source">{ev['source']}</span>
                    <div class="ev-score-bar">
                        <div class="ev-score-track">
                            <div class="ev-score-fill" style="width:{pct}%;"></div>
                        </div>
                        <span class="ev-score-num">{ev['score']:.2f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<hr class="rule">', unsafe_allow_html=True)

        # HITL Action Buttons
        if st.session_state.stage in ["review", "edited"]:
            st.markdown('<div class="section-eyebrow" style="margin-bottom:10px;">CSM Decision — HITL Gate</div>', unsafe_allow_html=True)
            b1, b2, b3 = st.columns(3, gap="small")
            with b1:
                if st.button("✅  Approve", type="primary", use_container_width=True):
                    st.session_state.stage = "approved"
                    st.rerun()
            with b2:
                if st.button("✏️  Edit Node", use_container_width=True):
                    # Scroll user to the first node with assumptions
                    has_any = any(
                        n.get("assumptions_keys") for n in case.get("agent_thoughts", [])
                    )
                    if has_any:
                        for n in case.get("agent_thoughts", []):
                            if n.get("assumptions_keys"):
                                k = f"edit_open_{n['agent']}"
                                st.session_state.node_edit_open[k] = True
                                break
                    st.rerun()
            with b3:
                if st.button("❌  Reject", use_container_width=True):
                    st.session_state.stage = "rejected"
                    st.rerun()

        # Approved Banner
        if st.session_state.stage == "approved":
            st.markdown(f"""
            <div class="banner banner-approved">
                <div class="banner-icon">🎉</div>
                <div>
                    <div class="banner-title">Action Approved</div>
                    <div class="banner-sub">
                        Outbound trigger fired: <em>{rec['action']}</em>.
                        Decision logged to memory — will influence future similarity-based retrieval.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            if st.button("→  Analyse another case"):
                load_scenario(st.session_state.scenario_name)
                st.rerun()

        # Rejected Banner
        elif st.session_state.stage == "rejected":
            st.markdown(f"""
            <div class="banner banner-rejected">
                <div class="banner-icon">🚫</div>
                <div>
                    <div class="banner-title">Action Rejected</div>
                    <div class="banner-sub">
                        CSM override recorded and logged. This rejection will be stored in memory
                        and will inform future recommendations for similar cases.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            if st.button("→  Analyse another case"):
                load_scenario(st.session_state.scenario_name)
                st.rerun()
