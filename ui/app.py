import streamlit as st
import copy
import json
import os
import requests

st.set_page_config(
    page_title="Pulse — Customer Success Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

_css_path = os.path.join(os.path.dirname(__file__), "style.css")
with open(_css_path) as _f:
    _css = _f.read()

st.html(f"""
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{_css}

/* ── NAV ──────────────────────────────────────────────────────────────────── */
.pulse-nav {{
  display:flex; align-items:center; justify-content:space-between;
  padding:24px 0 22px; border-bottom:1px solid #DDD9D0; margin-bottom:40px;
}}
.pulse-logo-wrap {{ display:flex; align-items:center; gap:11px; }}
.pulse-logo-icon {{
  width:34px; height:34px; border-radius:9px;
  background:linear-gradient(145deg,#1A3D1A,#0F2A0F);
  display:flex; align-items:center; justify-content:center;
  font-size:17px; box-shadow:0 2px 8px rgba(26,61,26,.3);
}}
.pulse-logo-mark {{
  font-family:'EB Garamond',serif; font-size:24px; font-weight:700;
  color:#1A3D1A; letter-spacing:-0.02em;
}}
.pulse-logo-sub {{
  font-size:10px; font-weight:600; letter-spacing:0.14em;
  text-transform:uppercase; color:#9A9690; margin-top:1px;
}}
.nav-links {{ display:flex; gap:28px; align-items:center; }}
.nav-link {{ font-size:13px; color:#7A7A72; font-weight:500; }}
.nav-status {{
  display:inline-flex; align-items:center; gap:7px; font-size:11px;
  font-weight:700; background:#EAF2EA; border:1px solid #B8D4B8;
  color:#1A4A1A; padding:5px 14px; border-radius:20px; letter-spacing:0.01em;
}}
.nav-offline {{
  display:inline-flex; align-items:center; gap:7px; font-size:11px;
  font-weight:700; background:#FFF8E6; border:1px solid #E8D080;
  color:#7A5C00; padding:5px 14px; border-radius:20px;
}}
.nav-dot {{
  width:6px; height:6px; border-radius:50%;
  animation:blink 2s infinite; display:inline-block;
}}
@keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}

/* ── TYPOGRAPHY HELPERS ───────────────────────────────────────────────────── */
.eyebrow {{
  font-size:9px; font-weight:700; letter-spacing:0.18em;
  text-transform:uppercase; color:#6A8A6A; margin-bottom:8px;
}}
.section-title {{
  font-family:'EB Garamond',serif; font-size:22px; font-weight:600;
  color:#0F0F0E; margin-bottom:4px; line-height:1.2;
}}
.section-sub {{ font-size:13px; color:#7A7A72; margin-bottom:20px; line-height:1.6; }}

/* ── HERO ─────────────────────────────────────────────────────────────────── */
.hero-wrap {{ padding:48px 0 36px; }}
.hero-label {{
  font-size:10px; font-weight:700; letter-spacing:0.18em;
  text-transform:uppercase; color:#1A3D1A; margin-bottom:14px;
  display:flex; align-items:center; gap:10px;
}}
.hero-label::before {{ content:''; display:block; width:24px; height:1px; background:#1A3D1A; }}
.hero-headline {{
  font-family:'EB Garamond',serif; font-size:52px; font-weight:500;
  color:#0A0A0A; line-height:1.07; letter-spacing:-0.025em; margin-bottom:18px;
}}
.hero-headline em {{ font-style:italic; color:#1A3D1A; }}
.hero-sub {{ font-size:16px; color:#6A6A62; line-height:1.7; max-width:520px; }}

/* ── CASE STRIP ───────────────────────────────────────────────────────────── */
.case-strip {{
  display:flex; align-items:center; gap:12px; padding:12px 18px;
  margin-bottom:28px; background:#FFFFFF;
  border:1px solid #DDD9D0; border-radius:12px;
  font-size:12px; color:#8A8880;
  box-shadow:0 1px 4px rgba(0,0,0,.04);
}}
.case-id {{
  font-family:'JetBrains Mono',monospace; font-size:11px; color:#1A3D1A;
  background:#EAF2EA; border:1px solid #B8D4B8; padding:2px 9px; border-radius:5px;
}}
.case-dot {{ color:#D4CFC6; }}
.case-company {{ color:#1A1A18; font-weight:600; font-size:13px; }}
.case-right {{ margin-left:auto; }}
.case-badge {{
  font-size:10px; font-weight:700; letter-spacing:0.08em; text-transform:uppercase;
  color:#8A6A00; background:#FFF8E6; border:1px solid #E8D080;
  padding:3px 10px; border-radius:5px;
}}

/* ── AGENT CARD ───────────────────────────────────────────────────────────── */
.agent-card {{
  background:#FFFFFF; border:1px solid #E4E0D8; border-radius:14px;
  padding:22px 24px; margin-bottom:14px;
  box-shadow:0 2px 8px rgba(0,0,0,.04);
  transition: border-color .2s, box-shadow .2s;
}}
.agent-card:hover {{
  border-color:#C2D4C2;
  box-shadow:0 4px 16px rgba(26,61,26,.08);
}}
.agent-header {{ display:flex; align-items:center; gap:14px; margin-bottom:14px; }}
.agent-icon-wrap {{
  width:42px; height:42px; border-radius:12px; flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
  font-size:18px; background:#EAF2EA; border:1px solid #C2D4C2;
}}
.agent-icon-hitl {{
  background:#FDF2F2; border:1px solid #E8C4C4;
}}
.agent-name {{
  font-family:'EB Garamond',serif; font-size:19px; font-weight:600; color:#0F0F0E;
}}
.agent-role {{ font-size:11px; color:#9A9690; font-weight:500; margin-top:1px; }}

/* ── THOUGHT BOX ──────────────────────────────────────────────────────────── */
.thought-box {{
  background:#F8F6F2; border:1px solid #EAE6DE; border-radius:10px;
  padding:14px 16px; margin-bottom:12px;
}}
.thought-label {{
  font-size:8px; font-weight:700; letter-spacing:0.18em;
  text-transform:uppercase; color:#9A9690; margin-bottom:6px;
  display:flex; align-items:center; gap:6px;
}}
.thought-label::before {{ content:''; display:block; width:14px; height:1px; background:#C4C0B8; }}
.thought-text {{ font-size:13px; color:#4A4A45; line-height:1.75; }}

/* ── DATA CARD ────────────────────────────────────────────────────────────── */
.data-card {{
  background:#FDFBF8; border:1px solid #EAE6DE; border-radius:10px;
  padding:14px 16px; margin-top:4px;
}}
.data-card-title {{
  font-size:8px; font-weight:700; letter-spacing:0.18em;
  text-transform:uppercase; color:#1A3D1A; margin-bottom:10px;
}}
.data-row {{
  display:flex; justify-content:space-between; align-items:center;
  padding:8px 0; border-bottom:1px solid #F0EDE6; font-size:13px;
}}
.data-row:last-child {{ border-bottom:none; padding-bottom:0; }}
.data-key {{ color:#8A8880; font-size:12px; white-space:nowrap; }}
.data-val {{ font-weight:600; color:#1A1A18; text-align:right; }}

/* ── ASSUMPTION TAGS ──────────────────────────────────────────────────────── */
.assumption-tag {{
  display:inline-flex; align-items:center; gap:5px;
  background:#FFF8E6; border:1px solid #E8D080;
  color:#7A5C00; border-radius:6px;
  padding:4px 10px; font-size:11px; font-weight:600;
  margin-right:6px; margin-bottom:5px;
}}

/* ── ROUTE PILLS ──────────────────────────────────────────────────────────── */
.pill-agent {{
  background:#EAF2EA; border:1px solid #B8D4B8;
  padding:4px 12px; border-radius:20px;
  font-size:11px; font-weight:600; color:#1A3D1A;
}}
.pill-hitl {{
  background:#FDF2F2; border:1px solid #E8C4C4;
  padding:4px 12px; border-radius:20px;
  font-size:11px; font-weight:600; color:#C03030;
}}
.pill-arrow {{ color:#C4C0B8; font-size:13px; margin:0 2px; }}

/* ── SCORE PILLS ──────────────────────────────────────────────────────────── */
.score-pill {{
  display:inline-flex; align-items:center; gap:7px;
  background:#FFFFFF; border:1px solid #DDD9D0;
  padding:7px 13px; border-radius:8px; font-size:12px;
}}
.score-key {{ color:#8A8880; }}
.score-val {{ font-weight:700; font-family:'JetBrains Mono',monospace; }}

/* ── ASSUMPTION EDITOR ────────────────────────────────────────────────────── */
.assume-box {{
  background:#FFFCF0; border:1px solid #E8D080; border-radius:12px;
  padding:18px 20px; margin:8px 0 12px;
}}
.assume-box-title {{
  font-size:9px; font-weight:700; letter-spacing:0.16em;
  text-transform:uppercase; color:#8A6A00; margin-bottom:14px;
}}

/* ── BEFORE/AFTER ─────────────────────────────────────────────────────────── */
.cmp-before {{
  background:#FEF6F6; border:1px solid #EDBCBC; border-radius:12px; padding:20px;
}}
.cmp-after {{
  background:#F2F9F2; border:1px solid #B8D4B8; border-radius:12px; padding:20px;
}}
.cmp-label {{ font-size:9px; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; margin-bottom:8px; }}
.cmp-action {{ font-family:'EB Garamond',serif; font-size:20px; font-weight:600; line-height:1.2; }}

/* ── REC CARD (right panel) ───────────────────────────────────────────────── */
.rec-card {{
  background:#FFFFFF; border:1px solid #B8D4B8; border-radius:16px;
  padding:28px; margin-bottom:20px;
  box-shadow:0 4px 20px rgba(26,61,26,.08), 0 1px 0 rgba(255,255,255,.8) inset;
}}
.rec-eyebrow {{
  font-size:9px; font-weight:700; letter-spacing:0.18em;
  text-transform:uppercase; color:#6A8A6A; margin-bottom:10px;
}}
.rec-action {{
  font-family:'EB Garamond',serif; font-size:26px; font-weight:600;
  color:#0A0A0A; line-height:1.2; margin-bottom:16px;
}}
.conf-badge-high {{
  display:inline-flex; align-items:center; gap:7px;
  background:#EAF2EA; border:1px solid #A8C8A8; color:#1A4A1A;
  padding:5px 14px; border-radius:20px; font-size:11px; font-weight:700; margin-bottom:16px;
}}
.conf-badge-low {{
  display:inline-flex; align-items:center; gap:7px;
  background:#FFF8E6; border:1px solid #E8D080; color:#7A5C00;
  padding:5px 14px; border-radius:20px; font-size:11px; font-weight:700; margin-bottom:16px;
}}
.conf-badge-dot {{ width:6px; height:6px; border-radius:50%; display:inline-block; }}
.conf-track-row {{
  display:flex; justify-content:space-between;
  font-size:9px; font-weight:700; letter-spacing:0.1em;
  text-transform:uppercase; color:#9A9690; margin-bottom:6px; margin-top:4px;
}}
.conf-track {{ background:#EDE9E2; border-radius:6px; height:7px; overflow:hidden; }}
.conf-fill {{ height:100%; border-radius:6px; }}

/* ── PCVL GRID ────────────────────────────────────────────────────────────── */
.pcvl-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:16px 0; }}
.pcvl-tile {{
  background:#FDFBF8; border:1px solid #DDD9D0; border-radius:12px;
  padding:16px 12px; text-align:center;
  transition: border-color .18s, box-shadow .18s, transform .18s;
}}
.pcvl-tile:hover {{
  border-color:#A8C4A8; transform:translateY(-2px);
  box-shadow:0 4px 12px rgba(26,61,26,.08);
}}
.pcvl-tile-priority {{ border-color:#B8D4B8 !important; background:#F2F9F2; }}
.pcvl-label {{
  font-size:8px; font-weight:700; letter-spacing:0.16em;
  text-transform:uppercase; color:#9A9690; margin-bottom:6px;
}}
.pcvl-value {{
  font-family:'EB Garamond',serif; font-size:28px; font-weight:600; line-height:1.1; margin-bottom:4px;
}}
.pcvl-sub {{ font-size:9px; color:#9A9690; }}

/* ── EXPLANATION ──────────────────────────────────────────────────────────── */
.expl-block {{
  background:#F8F6F2; border-left:3px solid #1A3D1A;
  border-radius:0 10px 10px 0; padding:16px 18px; margin:16px 0;
  font-size:13px; color:#3A3A35; line-height:1.8;
}}

/* ── LEVERS ───────────────────────────────────────────────────────────────── */
.levers-pill {{
  display:inline-flex; align-items:center; gap:7px;
  background:#F8F6F2; border:1px solid #DDD9D0; border-radius:8px;
  padding:7px 14px; font-size:12px; color:#5A5A55; margin-top:4px;
}}

/* ── EVIDENCE CARDS ───────────────────────────────────────────────────────── */
.ev-card {{
  background:#FDFBF8; border:1px solid #EAE6DE; border-radius:10px;
  padding:14px 16px; margin-bottom:10px;
}}
.ev-header {{ display:flex; align-items:center; justify-content:space-between; margin-bottom:8px; }}
.ev-source {{
  font-family:'JetBrains Mono',monospace; font-size:11px; color:#1A3D1A;
  background:#EAF2EA; border:1px solid #B8D4B8; padding:3px 9px; border-radius:5px;
}}
.ev-score {{ font-family:'JetBrains Mono',monospace; font-size:11px; color:#9A9690; }}
.ev-bar {{ height:3px; background:#EDE9E2; border-radius:2px; margin-bottom:8px; overflow:hidden; }}
.ev-bar-fill {{ height:100%; background:#1A3D1A; border-radius:2px; }}
.ev-text {{ font-size:12px; color:#7A7A72; line-height:1.65; font-style:italic; }}

/* ── MEMORY DIFF ──────────────────────────────────────────────────────────── */
.mem-card {{
  background:#F2F9F4; border:1px solid #C4D8C8; border-radius:10px;
  padding:14px 16px; margin-bottom:10px;
}}
.mem-header {{ display:flex; align-items:center; justify-content:space-between; margin-bottom:6px; }}
.mem-action {{ font-size:13px; font-weight:600; color:#1A1A18; }}
.mem-approved {{ font-size:10px; font-weight:700; color:#1A4A1A; text-transform:uppercase; letter-spacing:0.1em; }}
.mem-rejected {{ font-size:10px; font-weight:700; color:#8A2020; text-transform:uppercase; letter-spacing:0.1em; }}
.mem-other {{ font-size:10px; font-weight:700; color:#7A5C00; text-transform:uppercase; letter-spacing:0.1em; }}
.mem-summary {{ font-size:12px; color:#4A6A50; line-height:1.65; margin-bottom:5px; }}
.mem-ts {{ font-size:10px; color:#9A9690; }}

/* ── HITL SECTION ─────────────────────────────────────────────────────────── */
.hitl-section {{
  background:#FFFFFF; border:1px solid #DDD9D0; border-radius:14px;
  padding:20px; margin-top:8px;
  box-shadow:0 2px 8px rgba(0,0,0,.04);
}}
.hitl-title {{
  font-size:9px; font-weight:700; letter-spacing:0.18em;
  text-transform:uppercase; color:#6A8A6A; margin-bottom:14px;
}}

/* ── OUTCOME BANNERS ──────────────────────────────────────────────────────── */
.banner-ok {{
  background:#EAF2EA; border:1px solid #A8C8A8; border-radius:14px;
  padding:22px; margin-top:16px; display:flex; align-items:flex-start; gap:16px;
}}
.banner-no {{
  background:#FEF2F2; border:1px solid #E8C0C0; border-radius:14px;
  padding:22px; margin-top:16px; display:flex; align-items:flex-start; gap:16px;
}}
.banner-title {{ font-family:'EB Garamond',serif; font-size:20px; font-weight:600; }}
.banner-sub {{ font-size:12px; color:#7A7A72; margin-top:4px; line-height:1.6; }}

/* ── CHIPS ────────────────────────────────────────────────────────────────── */
.chip {{
  display:inline-flex; align-items:center; gap:5px; padding:4px 11px;
  border-radius:6px; font-size:10px; font-weight:700;
  letter-spacing:0.08em; text-transform:uppercase;
}}
.chip-pending  {{ background:#FFF8E6; border:1px solid #E8D080; color:#7A5C00; }}
.chip-approved {{ background:#EAF2EA; border:1px solid #A8C8A8; color:#1A4A1A; }}
.chip-rejected {{ background:#FEF2F2; border:1px solid #E8C0C0; color:#8A2020; }}
.chip-editing  {{ background:#F4EEFF; border:1px solid #C8A8E8; color:#5A2A8A; }}

/* ── SIDEBAR ROWS ─────────────────────────────────────────────────────────── */
.sb-row {{
  display:flex; justify-content:space-between; align-items:center;
  padding:8px 0; border-bottom:1px solid #1E2E1E; font-size:12px;
}}
.sb-head {{
  font-size:9px; font-weight:700; letter-spacing:0.14em;
  text-transform:uppercase; color:#6A8A6A; margin:20px 0 8px;
  padding-bottom:6px; border-bottom:1px solid #1E2E1E;
}}
.health-track {{ background:#1E2E1E; border-radius:4px; height:4px; margin-top:8px; overflow:hidden; }}
.health-fill {{ height:100%; border-radius:4px; }}

/* ── DIVIDER ──────────────────────────────────────────────────────────────── */
.divider {{ border:none; border-top:1px solid #EAE6DE; margin:20px 0; }}
</style>
""")

# ─── API CLIENT ────────────────────────────────────────────────────────────────
BACKEND = "http://localhost:8000"

def api_health() -> bool:
    try:
        r = requests.get(f"{BACKEND}/health", timeout=1.5)
        return r.status_code == 200
    except Exception:
        return False

def api_process(raw_input: str, case_id: str = None) -> dict:
    body = {"raw_input": raw_input}
    if case_id:
        body["case_id"] = case_id
    r = requests.post(f"{BACKEND}/process", json=body, timeout=60)
    r.raise_for_status()
    return r.json()

def api_resume(thread_id: str, decision: str, edit_payload: dict = None) -> dict:
    body = {"thread_id": thread_id, "decision": decision}
    if edit_payload:
        body["edit_payload"] = edit_payload
    r = requests.post(f"{BACKEND}/resume", json=body, timeout=30)
    r.raise_for_status()
    return r.json()

def api_memory_diff(company_name: str) -> list:
    try:
        r = requests.get(f"{BACKEND}/memory_diff", params={"company_name": company_name}, timeout=10)
        if r.status_code == 200:
            return r.json().get("results", [])
    except Exception:
        pass
    return []

# ─── SCENARIO LOADER ───────────────────────────────────────────────────────────
_SCENARIO_DIR   = os.path.join(os.path.dirname(__file__), "..", "data", "scenarios")
_SCENARIO_FILES = [
    "scenario_1_churn.json", "scenario_2_expansion.json",
    "scenario_3_ambiguous.json", "scenario_4_apexlogistics_followup.json",
    "scenario_5_novaretail_enterprise.json",
]
_RISK_ICONS = {"High": "🔴", "Low": "🟢", "Medium": "🟡"}

def _load_scenarios() -> dict:
    result = {}
    for fname in _SCENARIO_FILES:
        fpath = os.path.join(_SCENARIO_DIR, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            sc = json.load(f)
        gt   = sc.get("ground_truth_assumptions", {})
        risk = gt.get("churn_risk", "Medium")
        label = f"{_RISK_ICONS.get(risk,'⚪')}  {sc['customer_name']} — {risk} Risk"
        result[label] = sc
    return result

SCENARIOS   = _load_scenarios()
PRESET_KEYS = list(SCENARIOS.keys())

# ─── AGENT NODES ───────────────────────────────────────────────────────────────
AGENT_NODES = [
    {"agent": "Planner",        "icon": "🧭", "role": "Orchestration Planner"},
    {"agent": "Ingestion",      "icon": "📥", "role": "Data Ingestion Agent"},
    {"agent": "Retrieval",      "icon": "🔍", "role": "Knowledge Retrieval Agent"},
    {"agent": "Reasoning",      "icon": "⚖️",  "role": "Reasoning & Scoring Agent"},
    {"agent": "Explainability", "icon": "💬", "role": "Explainability Agent"},
    {"agent": "HITL Gate",      "icon": "🛑", "role": "Human-in-the-Loop Interrupt"},
]

def get_node_thought(agent, plan_trace, profile=None, rec=None, evid=None):
    profile = profile or {}; rec = rec or {}; evid = evid or []
    if agent == "Planner":
        for line in reversed(plan_trace or []):
            if isinstance(line, str) and "routing to execute" in line.lower():
                return "All agents completed successfully. Routing to the HITL Gate — pausing for CSM review before any action is executed."
            if isinstance(line, str) and "planner" in line.lower():
                return line.split(":", 1)[-1].strip() if ":" in line else line
        return "Inspected the incoming case and determined the best agent routing sequence."
    elif agent == "Ingestion":
        company = profile.get("company_name","the account"); churn = profile.get("churn_risk","unknown")
        health = profile.get("health_score","—"); users = profile.get("active_users","—"); licenses = profile.get("license_count","—")
        return (f"Parsed the raw CRM note and extracted a structured profile for {company}. "
                f"Identified churn risk as {churn} with a health score of {health}/100. "
                f"Active usage is {users} out of {licenses} licensed seats.")
    elif agent == "Retrieval":
        if evid:
            top = evid[0]
            return (f"Queried the knowledge base using the customer's risk profile and contract details. "
                    f"Retrieved {len(evid)} relevant playbook(s) after applying time-decay re-ranking. "
                    f"Top match: {top.get('source','—')} (score: {float(top.get('score',0)):.4f}).")
        return "Queried the knowledge base but found no matching playbooks. Evidence is sparse — confidence will be reduced."
    elif agent == "Reasoning":
        action = rec.get("action","—"); conf = float(rec.get("confidence",0)); priority = float(rec.get("priority",0))
        conf_lbl = "high" if conf >= 0.6 else "moderate" if conf >= 0.4 else "low"
        return (f"Computed PCVL scores using the extracted profile and retrieved evidence. "
                f"Selected action: '{action}' with a priority score of {priority:.4f}. "
                f"Confidence is {conf_lbl} ({conf:.2f}) — "
                + ("ready for CSM approval." if conf >= 0.5 else "human judgment is recommended before acting."))
    elif agent == "Explainability":
        action = rec.get("action","the recommended action")
        return (f"Generated a human-readable rationale for '{action}', "
                f"citing the most relevant retrieved playbook evidence. "
                f"Flagged any low-confidence signals for CSM awareness.")
    elif agent == "HITL Gate":
        conf = float(rec.get("confidence",1.0))
        if conf < 0.5:
            return (f"Execution blocked. Confidence is low ({conf:.2f}). "
                    f"Please review the flagged assumptions and correct any inferred fields before proceeding.")
        return "Pipeline complete. Execution paused at the human checkpoint — approve, edit, or reject below."
    return f"{agent} completed its step."

def parse_actual_route(plan_trace):
    order = ["Planner","Ingestion","Retrieval","Reasoning","Explainability","HITL Gate"]
    seen  = {"Planner"}
    for line in (plan_trace or []):
        lower = line.lower()
        if "ingestion"      in lower: seen.add("Ingestion")
        if "retrieval"      in lower: seen.add("Retrieval")
        if "reasoning"      in lower: seen.add("Reasoning")
        if "explainability" in lower: seen.add("Explainability")
        if "execute" in lower or "pausing" in lower: seen.add("HITL Gate")
    if "Explainability" in seen: seen.add("Reasoning")
    return [a for a in order if a in seen]

# ─── SESSION STATE ──────────────────────────────────────────────────────────────
def _defaults():
    for k, v in {"preset": PRESET_KEYS[0] if PRESET_KEYS else "", "stage": "input",
                 "api_data": None, "thread_id": None, "original_rec": None, "node_edits": {}}.items():
        if k not in st.session_state: st.session_state[k] = v

_defaults()

def reset():
    for k in ["stage","api_data","thread_id","original_rec","node_edits"]:
        if k in st.session_state: del st.session_state[k]
    _defaults()

# ─── NAV BAR ────────────────────────────────────────────────────────────────────
online = api_health()
status_html = (
    '<span class="nav-status"><span class="nav-dot" style="background:#2A7A2A;"></span>Backend Connected</span>'
    if online else
    '<span class="nav-offline"><span class="nav-dot" style="background:#C4A020;"></span>Backend Offline</span>'
)
st.html(f"""
<div class="pulse-nav">
  <div class="pulse-logo-wrap">
    <div class="pulse-logo-icon">⚡</div>
    <div>
      <div class="pulse-logo-mark">Pulse</div>
      <div class="pulse-logo-sub">Customer Success Intelligence</div>
    </div>
  </div>
  <div class="nav-links">
    <span class="nav-link">Cases</span>
    <span class="nav-link">Playbooks</span>
    <span class="nav-link">Memory</span>
    <span class="nav-link">Settings</span>
    {status_html}
  </div>
</div>
""")
if not online:
    st.warning("⚠️ FastAPI backend is offline — run: `uvicorn api.main:app --port 8000`")

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.html('<div style="font-family:\'EB Garamond\',serif;font-size:21px;font-weight:600;color:#D8D4CC;margin-bottom:2px;letter-spacing:-0.01em;">Case Runner</div>')
    st.html('<div style="font-size:9px;color:#5A8A5A;text-transform:uppercase;letter-spacing:.16em;font-weight:700;margin-bottom:14px;">Select a scenario</div>')
    if PRESET_KEYS:
        sel = st.selectbox("Preset", PRESET_KEYS,
                           index=PRESET_KEYS.index(st.session_state.preset) if st.session_state.preset in PRESET_KEYS else 0,
                           label_visibility="collapsed")
        if sel != st.session_state.preset:
            st.session_state.preset = sel; reset(); st.rerun()

    data = st.session_state.api_data
    st.html('<div class="sb-head">Account Profile</div>')
    if data:
        profile = data.get("customer_profile") or {}
        health  = profile.get("health_score", 50)
        try: health = max(0, min(100, int(float(str(health).split("/")[0].strip()))))
        except: health = 50
        hc = "#3FB950" if health >= 75 else "#D4A017" if health >= 50 else "#F85149"
        rows = ""
        for k, v in {"Company": profile.get("company_name","—"), "Segment": profile.get("segment","—"),
                     "Contract": profile.get("contract_type","—"),
                     "Active Users": str(profile.get("active_users","—")), "Health": f"{health}/100"}.items():
            c = hc if k == "Health" else "#D8D4CC"
            rows += f'<div class="sb-row"><span style="color:#5A8A5A;font-size:11px;">{k}</span><span style="color:{c};font-weight:600;font-size:12px;">{v}</span></div>'
        st.html(f'{rows}<div class="health-track" style="margin-top:10px;"><div class="health-fill" style="width:{health}%;background:{hc};"></div></div>')
    else:
        st.html('<div style="font-size:11px;color:#3A5A3A;font-style:italic;padding:8px 0;">No case loaded yet.</div>')

    st.html('<div class="sb-head">Flow State</div>')
    stage_map = {"input":("chip-pending","Awaiting Input"),"review":("chip-pending","Pending Review"),
                 "edited":("chip-editing","Re-evaluated"),"approved":("chip-approved","Approved"),
                 "rejected":("chip-rejected","Rejected")}
    cls, lbl = stage_map.get(st.session_state.stage, ("chip-pending","—"))
    st.html(f'<span class="chip {cls}">{lbl}</span>')

# ─── STAGE: INPUT ────────────────────────────────────────────────────────────────
if st.session_state.stage == "input":
    st.html("""
    <div class="hero-wrap">
      <div class="hero-label">Customer Intelligence Platform</div>
      <div class="hero-headline">What is the <em>next best action</em><br>for this account?</div>
      <div class="hero-sub">
        Paste a CRM note, support transcript, or engagement signal.
        The multi-agent orchestration layer routes it through specialised agents
        and returns a fully reasoned, evidence-backed recommendation.
      </div>
    </div>
    """)
    sc          = SCENARIOS.get(st.session_state.preset, {})
    default_txt = sc.get("raw_text", "")
    scenario_id = sc.get("scenario_id", None)
    raw = st.text_area("Signal", value=default_txt, height=160,
                       label_visibility="collapsed",
                       placeholder="Paste CRM note, support ticket, or engagement signal…")
    c1, c2 = st.columns([2, 7])
    with c1:
        go = st.button("⚡  Analyse Case", type="primary", use_container_width=True, disabled=not online)
    with c2:
        st.html('<div style="padding-top:12px;font-size:11px;color:#8A8880;">Calls <code style="color:#1A3D1A;background:#EAF2EA;padding:2px 7px;border-radius:4px;font-family:\'JetBrains Mono\',monospace;font-size:11px;">POST /process</code> → LangGraph pipeline</div>')
    if go:
        with st.spinner("Running multi-agent orchestration pipeline…"):
            try:
                result = api_process(raw, case_id=scenario_id)
                st.session_state.api_data  = result
                st.session_state.thread_id = result.get("thread_id")
                st.session_state.stage     = "review"
                st.rerun()
            except Exception as e:
                st.error(f"Backend error: {e}")

# ─── STAGE: REVIEW / EDITED / APPROVED / REJECTED ──────────────────────────────
elif st.session_state.stage in ("review","edited","approved","rejected"):
    data    = st.session_state.api_data or {}
    rec     = data.get("recommendation") or {}
    conf    = float(rec.get("confidence", 0.5))
    profile = data.get("customer_profile") or {}
    assump  = data.get("assumptions") or {}
    evid    = data.get("retrieved_evidence") or []
    expl    = data.get("explanation") or "No explanation generated."
    trace   = data.get("plan_trace") or []
    tid     = st.session_state.thread_id or data.get("thread_id","—")
    company = profile.get("company_name","Unknown Account")
    arr_raw = profile.get("contract_value","N/A")
    arr_str = f"${arr_raw:,}" if isinstance(arr_raw,(int,float)) else str(arr_raw)
    actual_route = parse_actual_route(trace)
    churn  = profile.get("churn_risk","—")
    risk_c = {"High":"#C03030","Medium":"#8A6A00","Low":"#1A4A1A"}.get(churn,"#6A6A62")

    st.html(f"""
    <div class="case-strip">
      <span class="case-id">{tid}</span>
      <span class="case-dot">·</span>
      <span class="case-company">{company}</span>
      <span class="case-dot">·</span>
      <span style="color:#8A8880;">{arr_str}</span>
      <span class="case-dot">·</span>
      <span style="font-size:12px;color:{risk_c};font-weight:700;">{churn} Risk</span>
      <div class="case-right"><span class="case-badge">⏸ Awaiting CSM Decision</span></div>
    </div>
    """)

    left, right = st.columns([12, 9], gap="large")

    # ── LEFT ──────────────────────────────────────────────────────────────────
    with left:
        st.html('<div class="eyebrow">Agent Reasoning Trace</div>')
        st.html('<div class="section-title">How the agents reasoned</div>')
        st.html('<div class="section-sub">Live execution trace from the LangGraph orchestration pipeline.</div>')

        nodes_to_render = [n for n in AGENT_NODES if n["agent"] in actual_route]

        for node_def in nodes_to_render:
            agent   = node_def["agent"]
            icon    = node_def["icon"]
            role    = node_def["role"]
            is_hitl = agent == "HITL Gate"
            icon_cls = "agent-icon-hitl" if is_hitl else "agent-icon-wrap"
            thought = get_node_thought(agent, trace, profile=profile, rec=rec, evid=evid)

            st.html(f"""
            <div class="agent-card">
              <div class="agent-header">
                <div class="agent-icon-wrap {icon_cls}" style="{'background:#FDF2F2;border:1px solid #E8C4C4;' if is_hitl else ''}">{icon}</div>
                <div>
                  <div class="agent-name">{agent}</div>
                  <div class="agent-role">{role}</div>
                </div>
              </div>
              <div class="thought-box">
                <div class="thought-label">Internal Thought</div>
                <div class="thought-text">{thought}</div>
              </div>
            """)

            if agent == "Planner":
                pills = ""
                for i, s in enumerate(actual_route):
                    if i > 0: pills += '<span class="pill-arrow"> → </span>'
                    pills += f'<span class="{"pill-hitl" if s=="HITL Gate" else "pill-agent"}">{s}</span>'
                st.html(f'<div class="data-card"><div class="data-card-title">Actual Routing Sequence</div><div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:4px;">{pills}</div></div>')

            elif agent == "Ingestion":
                churn_c = {"High":"#C03030","Medium":"#8A6A00","Low":"#1A4A1A"}
                fields  = {"Company": profile.get("company_name"), "Segment": profile.get("segment"),
                           "Contract": profile.get("contract_type"), "Churn Risk": profile.get("churn_risk"),
                           "Health Score": profile.get("health_score"),
                           "Active Users": profile.get("active_users"), "Licenses": profile.get("license_count")}
                rows = ""
                for k, v_val in fields.items():
                    if v_val in (None,"","—"): continue
                    color = churn_c.get(str(v_val),"#1A1A18") if k == "Churn Risk" else "#1A1A18"
                    rows += f'<div class="data-row"><span class="data-key">{k}</span><span class="data-val" style="color:{color};">{v_val}</span></div>'
                st.html(f'<div class="data-card"><div class="data-card-title">Extracted Profile</div>{rows}</div>')
                if assump:
                    tags = "".join(f'<span class="assumption-tag">⚠ {k.replace("_"," ").title()}</span>' for k in assump)
                    st.html(f'<div style="margin-top:10px;line-height:2.4;">{tags}</div>')

            elif agent == "Retrieval":
                if evid:
                    rows = "".join(
                        f'<div class="data-row">'
                        f'<span class="data-key" style="font-family:\'JetBrains Mono\',monospace;font-size:11px;">{ev.get("source","—")}</span>'
                        f'<span class="data-val" style="font-family:\'JetBrains Mono\',monospace;font-size:11px;color:#1A3D1A;">score: {float(ev.get("score",0)):.4f}</span>'
                        f'</div>'
                        for ev in evid
                    )
                    st.html(f'<div class="data-card"><div class="data-card-title">Retrieved & Time-Decayed Chunks</div>{rows}</div>')
                else:
                    st.html('<div class="data-card"><div class="data-card-title">Retrieved Chunks</div><div style="font-size:12px;color:#9A9690;font-style:italic;">No chunks retrieved.</div></div>')

            elif agent == "Reasoning":
                p, cv, v, lv, pri = (float(rec.get(k,0)) for k in ("propensity","context","value","levers","priority"))
                pills_html = (
                    f'<span class="score-pill"><span class="score-key">Propensity</span><span class="score-val" style="color:#1A4A1A;">{p:.4f}</span></span>'
                    f'<span class="score-pill"><span class="score-key">Context</span><span class="score-val" style="color:#1A3A5A;">{cv:.4f}</span></span>'
                    f'<span class="score-pill"><span class="score-key">Value</span><span class="score-val" style="color:#4A1A6A;">{v:.4f}</span></span>'
                    f'<span class="score-pill"><span class="score-key">Levers</span><span class="score-val" style="color:#5A3A1A;">{lv:.4f}</span></span>'
                    f'<span class="score-pill" style="background:#EAF2EA;border-color:#B8D4B8;"><span class="score-key">Priority</span><span class="score-val" style="color:#1A3D1A;">{pri:.4f}</span></span>'
                )
                st.html(f'<div class="data-card"><div class="data-card-title">PCVL Scores</div><div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:4px;">{pills_html}</div></div>')

            elif agent == "Explainability":
                st.html('<div class="data-card"><div class="data-card-title">Rationale Draft</div>')
                st.write(expl)
                st.html('</div>')

            elif agent == "HITL Gate":
                if conf < 0.5:
                    st.warning(f"⚠️ **Low confidence ({conf:.2f}).** Correct flagged assumptions before approving.")
                else:
                    st.info("⏸️ **Execution paused.** Awaiting CSM decision.")

            st.html('</div>')  # close agent-card

            # Assumption editor under Ingestion
            if agent == "Ingestion" and assump and st.session_state.stage in ("review","edited"):
                edit_key = "open_Ingestion"
                if edit_key not in st.session_state.node_edits:
                    st.session_state.node_edits[edit_key] = False
                btn_lbl = "▼ Correct inferred assumptions" if not st.session_state.node_edits[edit_key] else "▲ Close editor"
                if st.button(btn_lbl, key="toggle_ingestion"):
                    st.session_state.node_edits[edit_key] = not st.session_state.node_edits[edit_key]; st.rerun()
                if st.session_state.node_edits[edit_key]:
                    st.html('<div class="assume-box"><div class="assume-box-title">✏ Correct Inferred Assumptions</div></div>')
                    edited_vals = {}
                    for field_name, reason in assump.items():
                        display = field_name.replace("_"," ").title()
                        st.markdown(f"**{display}**"); st.caption(str(reason))
                        fl = field_name.lower()
                        if   "segment"  in fl: edited_vals[field_name] = st.selectbox(display,["Enterprise","Mid-Market","SMB"],key=f"ed_{field_name}",label_visibility="collapsed")
                        elif "contract" in fl: edited_vals[field_name] = st.selectbox(display,["Annual","Monthly","Multi-year"],key=f"ed_{field_name}",label_visibility="collapsed")
                        elif "churn"    in fl: edited_vals[field_name] = st.radio(display,["High","Medium","Low"],horizontal=True,key=f"ed_{field_name}",label_visibility="collapsed")
                        elif "health"   in fl: edited_vals[field_name] = st.slider(display,0,100,int(profile.get("health_score",50)),key=f"ed_{field_name}",label_visibility="collapsed")
                        else: edited_vals[field_name] = st.text_input(display,value=str(profile.get(field_name,"")),key=f"ed_{field_name}",label_visibility="collapsed")
                        st.write("")
                    cs, cc, _ = st.columns([3,2,4])
                    with cs:
                        if st.button("🔄 Re-evaluate", type="primary", key="submit_ingestion"):
                            st.session_state.original_rec = copy.deepcopy(rec)
                            with st.spinner("Re-routing via Reasoning → Explainability…"):
                                try:
                                    result = api_resume(tid, "edit", edited_vals)
                                    updated = dict(st.session_state.api_data)
                                    updated.update({"customer_profile": result.get("customer_profile",profile),
                                                    "assumptions": result.get("assumptions",{}),
                                                    "explanation": result.get("explanation",expl),
                                                    "plan_trace": result.get("plan_trace",trace),
                                                    "recommendation": result.get("corrected_recommendation",rec)})
                                    st.session_state.api_data = updated
                                    st.session_state.node_edits[edit_key] = False
                                    st.session_state.stage = "edited"; st.rerun()
                                except Exception as e:
                                    st.error(f"Resume error: {e}")
                    with cc:
                        if st.button("Cancel", key="cancel_ingestion"):
                            st.session_state.node_edits[edit_key] = False; st.rerun()

        # Before/After
        if st.session_state.stage == "edited" and st.session_state.original_rec:
            orig  = st.session_state.original_rec
            p_new = float(rec.get("priority",0)); p_old = float(orig.get("priority",0))
            st.html('<div style="margin-top:24px;"><div class="eyebrow">Edit Result</div><div class="section-title" style="margin-bottom:16px;">Before vs After Re-evaluation</div></div>')
            ca, cb = st.columns(2, gap="medium")
            with ca:
                st.html(f'<div class="cmp-before"><div class="cmp-label" style="color:#8A2020;">Before Edit</div><div class="cmp-action" style="color:#8A2020;">{orig.get("action","—")}</div><div style="font-size:12px;color:#7A7A72;margin-top:10px;line-height:1.9;">Confidence&nbsp;<strong style="color:#8A2020;">{float(orig.get("confidence",0)):.4f}</strong><br>Priority&nbsp;<strong style="color:#8A2020;">{p_old:.4f}</strong></div></div>')
            with cb:
                st.html(f'<div class="cmp-after"><div class="cmp-label" style="color:#1A4A1A;">After Edit</div><div class="cmp-action" style="color:#1A4A1A;">{rec.get("action","—")}</div><div style="font-size:12px;color:#7A7A72;margin-top:10px;line-height:1.9;">Confidence&nbsp;<strong style="color:#1A4A1A;">{conf:.4f}</strong><br>Priority&nbsp;<strong style="color:#1A4A1A;">{p_new:.4f}</strong></div></div>')

    # ── RIGHT PANEL ────────────────────────────────────────────────────────────
    with right:
        p, cv, v, lv, pri = (float(rec.get(k,0)) for k in ("propensity","context","value","levers","priority"))
        mc  = "#1A3D1A" if conf >= 0.5 else "#C4A020"
        pct = conf * 100

        badge_html = (
            f'<span class="conf-badge-high"><span class="conf-badge-dot" style="background:#2A7A2A;"></span>High Confidence · {conf:.2f}</span>'
            if conf >= 0.5 else
            f'<span class="conf-badge-low"><span class="conf-badge-dot" style="background:#C4A020;"></span>Low Confidence · {conf:.2f} — Review Required</span>'
        )

        st.html(f"""
        <div class="rec-card">
          <div class="rec-eyebrow">Recommended Action</div>
          <div class="rec-action">{rec.get("action","No recommendation generated")}</div>
          {badge_html}
          <div class="conf-track-row"><span>Confidence</span><span>{pct:.0f}%</span></div>
          <div class="conf-track"><div class="conf-fill" style="width:{pct}%;background:{mc};"></div></div>
        </div>
        """)

        st.html(f"""
        <div class="eyebrow" style="margin-bottom:10px;">PCVL Scoring Matrix</div>
        <div class="pcvl-grid">
          <div class="pcvl-tile">
            <div class="pcvl-label">Propensity</div>
            <div class="pcvl-value" style="color:#1A4A1A;">{p:.2f}</div>
            <div class="pcvl-sub">action likelihood</div>
          </div>
          <div class="pcvl-tile">
            <div class="pcvl-label">Context</div>
            <div class="pcvl-value" style="color:#1A3A5A;">{cv:.2f}</div>
            <div class="pcvl-sub">evidence strength</div>
          </div>
          <div class="pcvl-tile">
            <div class="pcvl-label">Value</div>
            <div class="pcvl-value" style="color:#4A1A6A;">{v:.2f}</div>
            <div class="pcvl-sub">account LTV</div>
          </div>
          <div class="pcvl-tile pcvl-tile-priority">
            <div class="pcvl-label">Priority Score</div>
            <div class="pcvl-value" style="color:#0F2A0F;">{pri:.4f}</div>
            <div class="pcvl-sub">P × C × V × L</div>
          </div>
        </div>
        """)

        if lv > 0:
            lbl = "High playbook coverage" if lv >= 0.7 else "Partial playbook coverage"
            st.html(f'<div class="levers-pill">⚙&nbsp; Levers: {lv:.2f} — {lbl}</div>')

        st.html('<div class="divider"></div>')

        st.html('<div class="eyebrow">AI Rationale</div>')
        st.html('<div class="expl-block">')
        st.write(expl)
        st.html('</div>')

        st.html('<div class="divider"></div>')

        st.html('<div class="eyebrow">Retrieved Playbook Evidence</div>')
        if evid:
            for ev in evid:
                score  = float(ev.get("score",0))
                source = ev.get("source","Unknown")
                text   = ev.get("text","")
                bar_w  = int(min(score * 250, 100))
                st.html(f"""
                <div class="ev-card">
                  <div class="ev-header">
                    <span class="ev-source">{source}</span>
                    <span class="ev-score">{score:.4f}</span>
                  </div>
                  <div class="ev-bar"><div class="ev-bar-fill" style="width:{bar_w}%;"></div></div>
                  <div class="ev-text">"{text[:180]}{"…" if len(text)>180 else ""}"</div>
                </div>
                """)
        else:
            st.html('<div style="font-size:12px;color:#9A9690;font-style:italic;padding:8px 0;">No evidence chunks retrieved.</div>')

        st.html('<div class="divider"></div>')

        st.html('<div class="eyebrow">Memory — Similar Past Decisions</div>')
        mem_results = api_memory_diff(company)
        if mem_results:
            for m in mem_results[:3]:
                past_action   = m.get("action","—")
                past_decision = m.get("human_decision","—")
                past_summary  = m.get("summary","")
                past_ts       = m.get("timestamp","")[:10] if m.get("timestamp") else "—"
                dec_cls = "mem-approved" if past_decision=="approved" else "mem-rejected" if past_decision=="rejected" else "mem-other"
                st.html(f"""
                <div class="mem-card">
                  <div class="mem-header">
                    <span class="mem-action">{past_action}</span>
                    <span class="{dec_cls}">{past_decision}</span>
                  </div>
                  <div class="mem-summary">{past_summary}</div>
                  <div class="mem-ts">{past_ts}</div>
                </div>
                """)
        else:
            st.html('<div style="font-size:12px;color:#9A9690;font-style:italic;padding:8px 0;">No past decisions yet — approve a case to build memory.</div>')

        st.html('<div class="divider"></div>')

        if st.session_state.stage in ("review","edited"):
            st.html('<div class="hitl-section"><div class="hitl-title">CSM Decision — Human-in-the-Loop Gate</div></div>')
            b1, b2, b3 = st.columns(3, gap="small")
            with b1:
                if st.button("✅  Approve", type="primary", use_container_width=True):
                    with st.spinner("Submitting…"):
                        try: api_resume(tid, "approve")
                        except: pass
                    st.session_state.stage = "approved"; st.rerun()
            with b2:
                if st.button("✏️  Edit", use_container_width=True):
                    st.session_state.node_edits["open_Ingestion"] = True; st.rerun()
            with b3:
                if st.button("❌  Reject", use_container_width=True):
                    with st.spinner("Submitting…"):
                        try: api_resume(tid, "reject")
                        except: pass
                    st.session_state.stage = "rejected"; st.rerun()

        if st.session_state.stage == "approved":
            st.html(f"""
            <div class="banner-ok">
              <div style="font-size:28px;">✅</div>
              <div>
                <div class="banner-title" style="color:#1A4A1A;">Action Approved</div>
                <div class="banner-sub">Decision logged to interaction memory. Case closed.<br>
                <em style="color:#2A5A2A;">{rec.get("action","—")}</em></div>
              </div>
            </div>
            """)
            st.write("")
            if st.button("→  New Case", type="primary"):
                reset(); st.rerun()

        elif st.session_state.stage == "rejected":
            st.html(f"""
            <div class="banner-no">
              <div style="font-size:28px;">🚫</div>
              <div>
                <div class="banner-title" style="color:#8A2020;">Action Rejected</div>
                <div class="banner-sub">CSM override recorded. Will inform future recommendations.</div>
              </div>
            </div>
            """)
            st.write("")
            if st.button("→  New Case", type="primary"):
                reset(); st.rerun()
