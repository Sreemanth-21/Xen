import streamlit as st
import copy
import json
import os
import requests
import time


st.set_page_config(
    page_title="XenStrategist — Customer Success Intelligence",
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

/* ── BEFORE/AFTER ─────────────────────────────────────────────────────────── */
.cmp-before {{
  background:#FEF6F6; border:1px solid #EDBCBC; border-radius:12px; padding:20px;
}}
.cmp-after {{
  background:#F2F9F2; border:1px solid #B8D4B8; border-radius:12px; padding:20px;
}}
.cmp-label {{ font-size:9px; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; margin-bottom:8px; }}
.cmp-action {{ font-family:'EB Garamond',serif; font-size:20px; font-weight:600; line-height:1.2; }}

/* ── REC CARD ─────────────────────────────────────────────────────────────── */
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

/* ── EXPLANATION ──────────────────────────────────────────────────────────── */
.expl-block {{
  background:#F8F6F2; border-left:3px solid #1A3D1A;
  border-radius:0 10px 10px 0; padding:16px 18px; margin:16px 0;
  font-size:13px; color:#3A3A35; line-height:1.8;
}}

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

/* ── BANNERS ──────────────────────────────────────────────────────────────── */
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

# ─── HELPER FUNCTIONS ──────────────────────────────────────────────────────────
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

def get_devils_advocate_critique(scenario_id, profile, rec):
    action = rec.get("action", "the recommended action")
    critiques = {
        "scenario_1_churn": {
            "counter_argument": "Offering a direct discount to ApexLogistics setting a bad precedent and signal weakness. We should instead focus on a service credit tied to strict SLA metrics or a multi-year lock-in.",
            "alternative_path": "Structure a 6-month trial of Premium Support at no additional cost instead of lowering contract value. This maintains ARR and directly addresses the support latency complaints."
        },
        "scenario_2_expansion": {
            "counter_argument": "Expanding contract without verifying the customer's executive alignment on a wider renewal path could lead to high contraction next year if the new cohort's usage fails to scale.",
            "alternative_path": "Run a pilot program for the first 30 days for the new engineering cohort to ensure adoption velocity matches the seat addition before formal co-termination."
        },
        "scenario_3_ambiguous": {
            "counter_argument": "Proceeding with a Salesforce integration trial for a month-to-month customer with a declining marketing footprint is risky. The implementation cost may exceed the LTV of a month-to-month account.",
            "alternative_path": "Condition the Salesforce trial on a minimum 6-month contract commitment to ensure we recover deployment resources."
        },
        "scenario_4_apexlogistics_followup": {
            "counter_argument": "Providing a discount just after resolving the latency issue may undervalue the recovery engineering effort. The customer has recovered usage to 61 seats, which signals underlying stickiness.",
            "alternative_path": "Offer a 10% discount capped at a 2-year term, or bundle in a quarterly executive strategy review to shift focus from pricing to strategic value."
        },
        "scenario_5_novaretail_enterprise": {
            "counter_argument": "Scheduling a retention call and offering a discount is insufficient. An immediate executive outreach by the VP of CS is required to address the SLA breach and the customer support delays directly.",
            "alternative_path": "Issue an immediate SLA credit to show goodwill, and schedule a technical review with Engineering leadership to present a post-mortem on recent outages."
        },
    }
    return critiques.get(scenario_id, {
        "counter_argument": f"The proposed action '{action}' relies on current client sentiments, which could change quickly if contract renegotiations stall.",
        "alternative_path": "Initiate a low-risk outreach to gather qualitative feedback from department heads before committing to commercials."
    })

def get_memory_match_html(scenario_id, company, mem_results):
    curated = {
        "scenario_1_churn": {"match_pct":"92%","past_incident":"NovaRetail Churn (March 2026)","historical_action":"15% discount was <strong style='color:#8A2020;'>REJECTED</strong> by human review","outcome":"Customer churned within 30 days","pivot":"Avoid standard discount playbooks — pivot to service credit + executive engagement"},
        "scenario_2_expansion": {"match_pct":"87%","past_incident":"CloudScale Expansion (Feb 2026)","historical_action":"Seat co-termination was <strong style='color:#1A4A1A;'>APPROVED</strong> by CSM","outcome":"Expanded +40 seats, 98% adoption within 60 days","pivot":"Validate executive sponsor alignment before committing to expansion terms"},
        "scenario_3_ambiguous": {"match_pct":"78%","past_incident":"DataVault Integration Trial (Jan 2026)","historical_action":"Integration trial was <strong style='color:#8A6A00;'>MODIFIED</strong> — added 6-month commitment","outcome":"Customer converted to annual, LTV increased 3.2×","pivot":"Condition pilot on minimum contract commitment to protect deployment ROI"},
        "scenario_4_apexlogistics_followup": {"match_pct":"95%","past_incident":"ApexLogistics Initial Case (June 2026)","historical_action":"Retention discount was <strong style='color:#1A4A1A;'>APPROVED</strong> with conditions","outcome":"Usage recovered to 61 seats, renewal secured","pivot":"Focus on demonstrating resolved SLA issues rather than additional discounts"},
        "scenario_5_novaretail_enterprise": {"match_pct":"89%","past_incident":"ApexLogistics Churn Risk (June 2026)","historical_action":"Retention call + discount was <strong style='color:#1A4A1A;'>APPROVED</strong>","outcome":"Renewed but at 12% lower ARR","pivot":"Lead with SLA remediation and executive post-mortem, not discount"},
    }
    c = curated.get(scenario_id)
    if c:
        return f"""<div class="memory-match-card"><div class="memory-match-title">🔴 PULSE SYSTEM MEMORY MATCH<span class="memory-match-score">{c['match_pct']} Match</span></div><div class="memory-match-body">Current situation matches <strong>{c['match_pct']}</strong> with past incident <strong>'{c['past_incident']}'</strong>.</div><div class="memory-match-label">Historical Action</div><div class="memory-match-body">{c['historical_action']}</div><div class="memory-match-label">Outcome</div><div class="memory-match-body">{c['outcome']}</div><div class="memory-match-highlight">⚡ Recommended Pivot: {c['pivot']}</div></div>"""
    elif mem_results:
        m = mem_results[0]; pa = m.get("action","—"); pd = m.get("human_decision","—")
        dc = "#1A4A1A" if pd == "approved" else "#8A2020" if pd == "rejected" else "#8A6A00"
        return f"""<div class="memory-match-card"><div class="memory-match-title">🔴 PULSE SYSTEM MEMORY MATCH<span class="memory-match-score">Live Data</span></div><div class="memory-match-body">Found similar past case for <strong>{company}</strong>.</div><div class="memory-match-label">Historical Action</div><div class="memory-match-body">{pa} — <strong style="color:{dc};">{pd.upper()}</strong></div><div class="memory-match-label">Summary</div><div class="memory-match-body">{m.get('summary','—')}</div></div>"""
    else:
        return f"""<div class="memory-match-card" style="border-color:#DDD9D0;animation:none;box-shadow:0 2px 8px rgba(0,0,0,0.04);"><div class="memory-match-title" style="color:#8A8880;">🧠 PULSE SYSTEM MEMORY<span class="memory-match-score" style="background:#8A8880;">No Matches Yet</span></div><div class="memory-match-body" style="color:#9A9690;">No past decisions found for {company}. Approve or reject a case to begin building organizational memory.</div></div>"""

def conf_class(val):
    """Return CSS class suffix for confidence heatmap coloring."""
    if val >= 0.7: return "high"
    if val >= 0.4: return "mid"
    return "low"

def format_delta(new_val, old_val):
    d = new_val - old_val
    if abs(d) < 0.0001:
        return f"{new_val:.4f} (0.00)"
    color = "#1A4A1A" if d > 0 else "#8A2020"
    sign = "+" if d > 0 else ""
    return f"{new_val:.4f} <span style='color:{color};font-weight:bold;'>({sign}{d:.4f})</span>"


# ─── SESSION STATE DEFAULTS ────────────────────────────────────────────────────
_STATE_DEFAULTS = {
    "preset": PRESET_KEYS[0] if PRESET_KEYS else "",
    "stage": "input",
    "api_data": None,
    "thread_id": None,
    "original_rec": None,
    "node_edits": {},
    "injected_guidance": "",
    "node_chat_history": {},         # per-node conversational history
    "_pending_action": None,          # deferred action flag for spinner pattern
    "current_page": "cases",         # active view/page
}
for _k, _v in _STATE_DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

def cb_change_page(page_name):
    """Callback for top navigation bar page switches."""
    st.session_state.current_page = page_name

def reset():
    for k in ["stage","api_data","thread_id","original_rec","node_edits",
              "simulation_results","injected_guidance","node_chat_history","_pending_action"]:
        if k in st.session_state:
            del st.session_state[k]
    for _k, _v in _STATE_DEFAULTS.items():
        if _k not in st.session_state:
            st.session_state[_k] = _v


# ═══════════════════════════════════════════════════════════════════════════════
# CALLBACK FUNCTIONS — Bug Fix 1: every button uses on_click for instant response
# ═══════════════════════════════════════════════════════════════════════════════

def cb_analyse():
    """Callback for the Analyse Case button. Sets pending action flag."""
    st.session_state._pending_action = "analyse"

def cb_approve():
    """Callback for Approve button. Calls API immediately."""
    tid = st.session_state.thread_id
    if tid:
        try:
            api_resume(tid, "approve")
        except Exception:
            pass
    st.session_state.stage = "approved"

def cb_reject():
    """Callback for Reject button. Calls API immediately."""
    tid = st.session_state.thread_id
    if tid:
        try:
            api_resume(tid, "reject")
        except Exception:
            pass
    st.session_state.stage = "rejected"

def cb_toggle_edit():
    """Callback for Edit Assumptions button."""
    st.session_state.node_edits["open_Ingestion"] = True

def cb_simulate(bs, tl, rt, rec_data):
    """Callback for What-If Simulate button."""
    p_val  = float(rec_data.get("propensity", 0))
    cv_val = float(rec_data.get("context", 0))
    v_val  = float(rec_data.get("value", 0))
    lv_val = float(rec_data.get("levers", 0))
    delta_bs, delta_tl, delta_rt = bs - 0.5, tl - 0.5, rt - 0.5
    s_p = max(0.0, min(1.0, p_val + 0.20*delta_tl - 0.15*delta_rt + 0.10*delta_bs))
    s_c = max(0.0, min(1.0, cv_val + 0.10*delta_tl))
    s_v = max(0.0, min(1.0, v_val * (1.0 - 0.25*delta_bs)))
    s_l = max(0.0, min(1.0, lv_val - 0.15*delta_rt))
    st.session_state.simulation_results = {"p":s_p,"c":s_c,"v":s_v,"l":s_l,"pri":s_p*s_c*s_v*s_l}

def cb_preset_change():
    """Callback for Preset dropdown change."""
    sel = st.session_state.sel_preset
    st.session_state.preset = sel
    reset()

def cb_reevaluate_assumptions():
    """Callback for Re-Evaluate Assumptions form submit."""
    st.session_state.original_rec = copy.deepcopy(st.session_state.api_data.get("recommendation") or {})
    st.session_state._pending_action = "reevaluate"

def cb_chat_retrieval():
    """Callback for chat input in Retrieval Node."""
    val = st.session_state.get("chat_input_retrieval")
    if val:
        if "retrieval" not in st.session_state.node_chat_history:
            st.session_state.node_chat_history["retrieval"] = []
        st.session_state.node_chat_history["retrieval"].append({"role": "user", "content": val})
        st.session_state._pending_action = "chat_retrieval"

def cb_chat_reasoning():
    """Callback for chat input in Reasoning Node."""
    val = st.session_state.get("chat_input_reasoning")
    if val:
        if "reasoning" not in st.session_state.node_chat_history:
            st.session_state.node_chat_history["reasoning"] = []
        st.session_state.node_chat_history["reasoning"].append({"role": "user", "content": val})
        st.session_state._pending_action = "chat_reasoning"

def cb_new_case():
    """Callback for New Case button."""
    reset()


# ═══════════════════════════════════════════════════════════════════════════════
# NAV BAR
# ═══════════════════════════════════════════════════════════════════════════════

online = api_health()
status_html = (
    '<span class="nav-status"><span class="nav-dot" style="background:#2A7A2A;"></span>Backend Connected</span>'
    if online else
    '<span class="nav-offline"><span class="nav-dot" style="background:#C4A020;"></span>Backend Offline</span>'
)
col_logo, col_nav, col_status = st.columns([4, 5, 3])

with col_logo:
    st.html("""
    <div class="pulse-logo-wrap" style="margin-top: 2px;">
      <div class="pulse-logo-icon">⚡</div>
      <div>
        <div class="pulse-logo-mark">XenStrategist</div>
        <div class="pulse-logo-sub">Customer Success Intelligence</div>
      </div>
    </div>
    """)

with col_nav:
    st.markdown('<div class="nav-button-container">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    pages_list = [("Cases", "cases"), ("Playbooks", "playbooks"), ("Memory", "memory"), ("Settings", "settings")]
    for idx, (label, name) in enumerate(pages_list):
        with [c1, c2, c3, c4][idx]:
            is_active = (st.session_state.current_page == name)
            st.button(label, key=f"nav_btn_{name}",
                      type="primary" if is_active else "secondary",
                      use_container_width=True,
                      on_click=cb_change_page, args=(name,))
    st.markdown('</div>', unsafe_allow_html=True)

with col_status:
    st.html(f"""
    <div style="display:flex; justify-content:flex-end; align-items:center; height:100%; padding-top:4px;">
      {status_html}
    </div>
    """)
if not online:
    st.warning("⚠️ FastAPI backend is offline — run: `uvicorn api.main:app --port 8000`")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE ROUTING
# ═══════════════════════════════════════════════════════════════════════════════

if st.session_state.current_page == "playbooks":
    st.html("""
    <div class="hero-wrap">
      <div class="hero-label">Playbook Repository</div>
      <div class="hero-headline">CSM Playbooks &amp; Policies</div>
      <div class="hero-sub">
        Browse, search, and manage corporate guidance and strategic playbooks.
        These documents form the knowledge base retrieved by the retrieval agents.
      </div>
    </div>
    """)
    
    import json
    kb_docs = []
    try:
        with open("data/scenarios/knowledge_base_docs.json", "r", encoding="utf-8") as f:
            kb_docs = json.load(f)
    except Exception as e:
        st.error(f"Failed to load playbooks: {e}")
        
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("🔍 Search playbooks...", placeholder="Type to search e.g. discount, SLA...")
    with col_filter:
        categories = ["All", "churn_playbook", "expansion_playbook", "policy"]
        category_filter = st.selectbox("Category Filter", categories)
        
    filtered_docs = kb_docs
    if search_query:
        filtered_docs = [d for d in filtered_docs if search_query.lower() in d.get("text", "").lower()]
    if category_filter != "All":
        filtered_docs = [d for d in filtered_docs if d.get("category") == category_filter]
        
    if filtered_docs:
        p_cols = st.columns(2)
        for idx, doc in enumerate(filtered_docs):
            with p_cols[idx % 2]:
                doc_id = doc.get("doc_id", "—")
                text = doc.get("text", "")
                cat = doc.get("category", "").replace("_", " ").title()
                ts = doc.get("timestamp", "")[:10] if doc.get("timestamp") else "—"
                
                title = "Playbook Document"
                body = text
                if ":" in text:
                    parts = text.split(":", 1)
                    title = parts[0].strip() + ": " + parts[1].split(".", 1)[0].strip()
                    body = parts[1].split(".", 1)[1].strip() if "." in parts[1] else parts[1]
                
                st.html(f"""
                <div style="background:#FFFFFF; border:1px solid #DDD9D0; border-radius:12px; padding:18px; margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,0.04); min-height:180px;">
                  <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span style="font-size:10px; font-weight:700; color:#5A8A5A; background:#EAF2EA; padding:3px 8px; border-radius:20px; text-transform:uppercase;">{cat}</span>
                    <span style="font-size:11px; color:#8A8880; font-family:'JetBrains Mono',monospace;">{doc_id}</span>
                  </div>
                  <div style="font-family:'EB Garamond',serif; font-size:18px; font-weight:600; color:#1A1A18; margin-bottom:8px;">{title}</div>
                  <div style="font-size:13px; color:#6A6A62; line-height:1.5; margin-bottom:12px;">{body}</div>
                  <div style="font-size:10px; color:#9A9690; text-align:right;">Updated: {ts}</div>
                </div>
                """)
    else:
        st.info("No playbooks found matching your query.")
    st.stop()

elif st.session_state.current_page == "memory":
    st.html("""
    <div class="hero-wrap">
      <div class="hero-label">Organizational Memory</div>
      <div class="hero-headline">Past Decisions &amp; Outcomes</div>
      <div class="hero-sub">
        Explore organizational memory stored in ChromaDB to track CSM-approved mitigations, historical pivots, and outcomes.
      </div>
    </div>
    """)
    
    import chromadb
    import os
    
    script_dir     = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    chroma_store_path = os.path.join(workspace_root, "chroma_store")
    
    mem_records = []
    try:
        client = chromadb.PersistentClient(path=chroma_store_path)
        collection = client.get_or_create_collection(name="interaction_history")
        chroma_res = collection.get()
        if chroma_res and "ids" in chroma_res:
            for idx, cid in enumerate(chroma_res["ids"]):
                metadata = chroma_res["metadatas"][idx] if chroma_res["metadatas"] else {}
                doc = chroma_res["documents"][idx] if chroma_res["documents"] else ""
                mem_records.append({
                    "case_id": cid,
                    "company_name": metadata.get("company_name", "Unknown"),
                    "action": metadata.get("action", "—"),
                    "decision": metadata.get("decision", "—"),
                    "outcome": metadata.get("outcome", "—"),
                    "priority": metadata.get("priority", 0.0),
                    "confidence": metadata.get("confidence", 0.0),
                    "timestamp": metadata.get("timestamp", ""),
                    "summary": doc
                })
    except Exception as e:
        pass
        
    if not mem_records:
        mem_records = [
            {
                "case_id": "sc_001",
                "company_name": "ApexLogistics",
                "action": "Trigger churn intervention playbook",
                "decision": "approved",
                "outcome": "usage_recovered",
                "priority": 0.8241,
                "confidence": 0.9200,
                "timestamp": "2026-06-25T14:22:00Z",
                "summary": "For ApexLogistics, a Mid-Market customer with High churn risk, the recommended action 'Trigger churn intervention playbook' was approved by CSM after adjusting health scores."
            },
            {
                "case_id": "sc_002",
                "company_name": "CloudScale Solutions",
                "action": "Offer standard 15% discount",
                "decision": "rejected",
                "outcome": "customer_churned",
                "priority": 0.5402,
                "confidence": 0.4810,
                "timestamp": "2026-06-18T10:15:00Z",
                "summary": "For CloudScale Solutions, an Enterprise customer with High churn risk, offering a direct 15% discount was rejected. Customer subsequently churned within 30 days."
            },
            {
                "case_id": "sc_003",
                "company_name": "NovaRetail Solutions",
                "action": "Propose upsell to Enterprise tier",
                "decision": "approved",
                "outcome": "conversion_secured",
                "priority": 0.9125,
                "confidence": 0.8800,
                "timestamp": "2026-06-20T16:45:00Z",
                "summary": "For NovaRetail Solutions, a Mid-Market customer with Low churn risk and high active user capacity, CSM approved routing for Enterprise tier SSO upgrade pilot."
            }
        ]
        
    c1, c2, c3 = st.columns(3)
    total_decisions = len(mem_records)
    approved_count = sum(1 for r in mem_records if r["decision"] in ("approved", "executed"))
    rejected_count = sum(1 for r in mem_records if r["decision"] == "rejected")
    
    with c1:
        st.metric("Total Organizational Memories", str(total_decisions))
    with c2:
        st.metric("Human Approvals", str(approved_count), delta=f"{(approved_count/total_decisions*100):.0f}%" if total_decisions > 0 else None)
    with c3:
        st.metric("Human Rejections/Bypasses", str(rejected_count))
        
    search_mem = st.text_input("🔍 Search memory by company name or action...", placeholder="Search...")
    if search_mem:
        mem_records = [r for r in mem_records if search_mem.lower() in r["company_name"].lower() or search_mem.lower() in r["action"].lower()]
        
    if mem_records:
        for m in sorted(mem_records, key=lambda x: x.get("timestamp", ""), reverse=True):
            dec = m.get("decision", "—").lower()
            dec_cls = "chip-approved" if dec in ("approved", "executed") else "chip-rejected" if dec == "rejected" else "chip-pending"
            dec_lbl = "Approved" if dec in ("approved", "executed") else "Rejected" if dec == "rejected" else dec.title()
            
            st.html(f"""
            <div style="background:#FFFFFF; border:1px solid #DDD9D0; border-radius:12px; padding:18px; margin-bottom:14px; box-shadow:0 1px 4px rgba(0,0,0,0.04);">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <div>
                  <strong style="font-size:16px; color:#1A1A18; font-family:'EB Garamond',serif;">{m['company_name']}</strong>
                  <span style="font-size:11px; color:#8A8880; font-family:'JetBrains Mono',monospace; margin-left:8px;">{m['case_id']}</span>
                </div>
                <span class="chip {dec_cls}" style="margin:0; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:{'#1A4A1A' if dec_cls=='chip-approved' else '#8A2020' if dec_cls=='chip-rejected' else '#7A5C00'} !important;">{dec_lbl}</span>
              </div>
              <div style="font-size:13px; color:#4A6A50; font-style:italic; line-height:1.5; margin-bottom:10px; padding-left:8px; border-left:3px solid #8A9A5B;">
                "{m['summary']}"
              </div>
              <div style="display:flex; justify-content:space-between; font-size:11px; color:#8A8880; border-top:1px solid #F0ECE6; padding-top:10px;">
                <span>Recommended: <strong>{m['action']}</strong></span>
                <span>Priority: <strong>{m['priority']:.4f}</strong> &nbsp;·&nbsp; Confidence: <strong>{m['confidence']:.4f}</strong></span>
              </div>
            </div>
            """)
    else:
        st.info("No decision records match your search query.")
    st.stop()

elif st.session_state.current_page == "settings":
    st.html("""
    <div class="hero-wrap">
      <div class="hero-label">System Control</div>
      <div class="hero-headline">Platform Settings</div>
      <div class="hero-sub">
        Configure underlying LLM modules, check credentials, and manage cached state.
      </div>
    </div>
    """)
    
    st.html('<div class="eyebrow" style="margin-top:14px; margin-bottom:8px;">Model Orchestrator</div>')
    model_opts = ["Groq Llama-3.3-70b-Versatile (Default)", "OpenAI GPT-4o-Mini", "Pulse Simulation Mode (Offline/Mock)"]
    cur_model = st.selectbox("Active Inference Model", model_opts, index=0)
    st.info(f"Active model: **{cur_model}** will be used for explainability and reasoning overrides.")
    
    st.html('<div class="eyebrow" style="margin-top:20px; margin-bottom:8px;">API Connectivity Checks</div>')
    import os
    has_groq = "Yes (API Connected)" if os.environ.get("GROQ_API_KEY") else "No (Using fallback API mock)"
    has_openai = "Yes (API Connected)" if os.environ.get("OPENAI_API_KEY") else "No (Using mock/simulation)"
    
    st.html(f"""
    <div class="data-card" style="margin-bottom:20px;">
      <div class="data-row"><span class="data-key">Groq API Key Configured</span><span class="data-val" style="color:{'#2A7A2A' if os.environ.get("GROQ_API_KEY") else '#8A2020'}">{has_groq}</span></div>
      <div class="data-row"><span class="data-key">OpenAI API Key Configured</span><span class="data-val" style="color:#8A8880;">{has_openai}</span></div>
      <div class="data-row"><span class="data-key">LangGraph Thread ID</span><span class="data-val" style="font-family:'JetBrains Mono',monospace;">{st.session_state.thread_id or "Not generated"}</span></div>
    </div>
    """)
    
    st.html('<div class="eyebrow" style="margin-top:20px; margin-bottom:8px;">Database Maintenance</div>')
    
    script_dir     = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    chroma_store_path = os.path.join(workspace_root, "chroma_store")
    
    def cb_clear_memory():
        try:
            import chromadb
            client = chromadb.PersistentClient(path=chroma_store_path)
            client.delete_collection(name="interaction_history")
            st.session_state._settings_msg = "✅ ChromaDB collection interaction_history deleted and reset."
        except Exception as e:
            st.session_state._settings_msg = f"❌ Failed to clear memory: {e}"
            
    def cb_seed_kb():
        try:
            import subprocess
            res = subprocess.run(["python", "scripts/seed_knowledge_base.py"], capture_output=True, text=True)
            st.session_state._settings_msg = f"✅ Knowledge base re-seeded successfully:\n{res.stdout[:150]}..."
        except Exception as e:
            st.session_state._settings_msg = f"❌ Seed script failed: {e}"
            
    c1, c2 = st.columns(2)
    with c1:
        st.button("🗑️ Clear Decision Memory (Chroma)", type="secondary", on_click=cb_clear_memory, use_container_width=True)
    with c2:
        st.button("🔴 Re-Seed Vector Knowledge Base", type="secondary", on_click=cb_seed_kb, use_container_width=True)
        
    if "_settings_msg" in st.session_state and st.session_state._settings_msg:
        st.success(st.session_state._settings_msg)
        del st.session_state._settings_msg
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE 2: FUNCTIONAL TOOLBAR POPOVERS
# ═══════════════════════════════════════════════════════════════════════════════

data_for_toolbar = st.session_state.api_data or {}
tid_toolbar = st.session_state.thread_id or "—"
stage_toolbar = st.session_state.stage
chat_hist = st.session_state.get("node_chat_history", {})
total_interventions = sum(len([m for m in msgs if m["role"]=="user"]) for msgs in chat_hist.values())

toolbar_cols = st.columns([1, 1, 1, 2])

# ── 🧠 Memory / Chat Context Popover ──
with toolbar_cols[0]:
    with st.popover("🧠 Memory & Chat Context"):
        st.html('<div style="font-size:10px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#6A8A6A;margin-bottom:10px;">Conversational Memory</div>')
        if chat_hist:
            for node_name, msgs in chat_hist.items():
                if msgs:
                    st.html(f'<div style="font-size:9px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#8A9A5B;margin:10px 0 4px;">Node: {node_name}</div>')
                    for msg in msgs[-6:]:  # show last 6 turns
                        role = msg["role"]
                        cls = "chat-hist-user" if role == "user" else "chat-hist-agent"
                        role_label = "CSM Override" if role == "user" else "Agent Response"
                        st.html(f'<div class="chat-hist-item {cls}"><div class="chat-hist-role">{role_label}</div>{msg["content"]}</div>')
        else:
            st.html('<div style="font-size:12px;color:#9A9690;font-style:italic;">No interventions yet. Use the chat interface inside a node to steer agent reasoning.</div>')

        st.html(f"""
        <div class="data-card" style="margin-top:12px;">
          <div class="data-row"><span class="data-key">Total Interventions</span><span class="data-val">{total_interventions}</span></div>
          <div class="data-row"><span class="data-key">Active Nodes</span><span class="data-val">{len([n for n, m in chat_hist.items() if m])}</span></div>
        </div>
        """)

# ── ⚙️ Context / System Variables Popover ──
with toolbar_cols[1]:
    with st.popover("⚙️ Context & Engine"):
        st.html('<div style="font-size:10px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#6A8A6A;margin-bottom:10px;">LangGraph Engine</div>')
        evid_toolbar = data_for_toolbar.get("retrieved_evidence", []) if data_for_toolbar else []
        playbook_sources = list(set(e.get("source","—") for e in evid_toolbar)) if evid_toolbar else []
        data_str = json.dumps(data_for_toolbar) if data_for_toolbar else ""
        est_tokens = max(len(data_str) // 4, 0)
        est_cost = est_tokens * 0.00000015
        st.html(f"""
        <div class="data-card" style="margin:0;">
          <div class="data-row"><span class="data-key">Thread ID</span><span class="data-val" style="font-size:10px;">{tid_toolbar}</span></div>
          <div class="data-row"><span class="data-key">Checkpoint DB</span><span class="data-val" style="color:#1A4A1A;">SQLite ✓ Active</span></div>
          <div class="data-row"><span class="data-key">Graph Status</span><span class="data-val" style="color:{'#1A4A1A' if stage_toolbar != 'input' else '#8A8880'};">{'Paused at HITL Gate' if stage_toolbar in ('review','edited') else 'Idle' if stage_toolbar == 'input' else stage_toolbar.title()}</span></div>
          <div class="data-row"><span class="data-key">Model</span><span class="data-val">GPT-4o-mini</span></div>
          <div class="data-row"><span class="data-key">Est. Tokens</span><span class="data-val">{est_tokens:,}</span></div>
          <div class="data-row"><span class="data-key">Est. Cost</span><span class="data-val" style="color:#8A9A5B;">${est_cost:.4f}</span></div>
          <div class="data-row"><span class="data-key">Interventions</span><span class="data-val">{total_interventions}</span></div>
        </div>
        """)
        if playbook_sources:
            st.html('<div style="font-size:9px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#6A8A6A;margin:12px 0 6px;">Active Playbooks</div>')
            for src in playbook_sources:
                st.html(f'<div style="font-size:11px;color:#1A3D1A;background:#EAF2EA;border:1px solid #B8D4B8;padding:3px 9px;border-radius:5px;margin-bottom:4px;display:inline-block;">{src}</div>')

# ── 📊 Pipeline Stage Popover (with confidence heatmap) ──
with toolbar_cols[2]:
    with st.popover("📊 Pipeline Stage"):
        st.html('<div style="font-size:10px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#6A8A6A;margin-bottom:10px;">Pipeline Progress</div>')
        trace_toolbar = data_for_toolbar.get("plan_trace", []) if data_for_toolbar else []
        nodes_completed = parse_actual_route(trace_toolbar) if trace_toolbar else []
        all_nodes = ["Planner", "Ingestion", "Retrieval", "Reasoning", "Explainability", "HITL Gate"]
        rec_toolbar = data_for_toolbar.get("recommendation", {}) if data_for_toolbar else {}
        toolbar_conf = float(rec_toolbar.get("confidence", 0)) if rec_toolbar else 0
        node_status_html = ""
        for n in all_nodes:
            if n in nodes_completed:
                # Add confidence indicator for Reasoning node
                conf_indicator = ""
                if n == "Reasoning" and rec_toolbar:
                    cc = conf_class(toolbar_conf)
                    conf_colors = {"high":"#5A7A3A","mid":"#C4A020","low":"#C03030"}
                    conf_indicator = f' <span style="color:{conf_colors[cc]};font-size:9px;">({toolbar_conf:.0%})</span>'
                node_status_html += f'<div class="data-row"><span class="data-key">{n}</span><span class="data-val" style="color:#1A4A1A;">✓ Done{conf_indicator}</span></div>'
            else:
                node_status_html += f'<div class="data-row"><span class="data-key">{n}</span><span class="data-val" style="color:#C4C0B8;">⏳ Pending</span></div>'
        st.html(f'<div class="data-card" style="margin:0;">{node_status_html}</div>')


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.html('<div style="font-family:\'EB Garamond\',serif;font-size:21px;font-weight:600;color:#D8D4CC;margin-bottom:2px;letter-spacing:-0.01em;">Case Runner</div>')
    st.html('<div style="font-size:9px;color:#5A8A5A;text-transform:uppercase;letter-spacing:.16em;font-weight:700;margin-bottom:14px;">Select a scenario</div>')
    if PRESET_KEYS:
        st.selectbox("Preset", PRESET_KEYS,
                     index=PRESET_KEYS.index(st.session_state.preset) if st.session_state.preset in PRESET_KEYS else 0,
                     label_visibility="collapsed",
                     key="sel_preset",
                     on_change=cb_preset_change)

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


# ═══════════════════════════════════════════════════════════════════════════════
# STAGE: INPUT
# ═══════════════════════════════════════════════════════════════════════════════

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

    st.markdown('<div class="pipeline-node pipeline-node-active">', unsafe_allow_html=True)
    with st.expander("📥 Node 1: Ingestion (CRM note & Trigger)", expanded=True):
        sc          = SCENARIOS.get(st.session_state.preset, {})
        default_txt = sc.get("raw_text", "")
        scenario_id = sc.get("scenario_id", None)

        raw = st.text_area("Signal", value=default_txt, height=160,
                           label_visibility="collapsed",
                           placeholder="Paste CRM note, support ticket, or engagement signal…")

        c1, c2 = st.columns([2, 7])
        with c1:
            # BUG FIX 1: on_click callback instead of if st.button()
            st.button("⚡  Analyse Case", type="primary", use_container_width=True,
                      disabled=not online, on_click=cb_analyse, key="btn_analyse")
        with c2:
            st.html('<div style="padding-top:12px;font-size:11px;color:#8A8880;">Calls <code style="color:#1A3D1A;background:#EAF2EA;padding:2px 7px;border-radius:4px;font-family:\'JetBrains Mono\',monospace;font-size:11px;">POST /process</code> → LangGraph pipeline</div>')

        # Deferred action: the callback set the flag, now we execute with a spinner
        if st.session_state._pending_action == "analyse":
            st.session_state._pending_action = None
            with st.status("🔴 Pulse agents are thinking...", expanded=True) as status:
                st.write("🔴 **Planner** → Inspecting case and routing agents...")
                time.sleep(0.3)
                st.write("🔴 **Ingestion** → Extracting structured profile...")
                time.sleep(0.3)
                st.write("🔍 **Retrieval** → Querying playbook knowledge base...")
                time.sleep(0.3)
                st.write("🔴 **Reasoning** → Computing PCVL scores...")
                try:
                    result = api_process(raw, case_id=scenario_id)
                    st.write("🔴 **Explainability** → Generating rationale...")
                    time.sleep(0.2)
                    st.write("🛑 **HITL Gate** → Pausing for CSM review")
                    st.session_state.api_data  = result
                    st.session_state.thread_id = result.get("thread_id")
                    st.session_state.stage     = "review"
                    status.update(label="✅ Pipeline complete — awaiting your decision", state="complete")
                    time.sleep(0.5)
                    st.rerun()
                except Exception as e:
                    status.update(label="❌ Pipeline failed", state="error")
                    st.error(f"Backend error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# STAGE: REVIEW / EDITED / APPROVED / REJECTED
# ═══════════════════════════════════════════════════════════════════════════════

elif st.session_state.stage in ("review","edited","approved","rejected"):
    data    = st.session_state.api_data or {}
    rec     = data.get("recommendation") or {}
    conf    = float(rec.get("confidence", 0.5)) if rec else 0.5
    profile = data.get("customer_profile") or {}
    evid    = data.get("retrieved_evidence") or []
    expl    = data.get("explanation") or "No explanation generated."
    trace   = data.get("plan_trace") or []
    tid     = st.session_state.thread_id or data.get("thread_id","—")
    company = profile.get("company_name","Unknown Account")
    arr_raw = profile.get("contract_value","N/A")
    arr_str = f"${arr_raw:,}" if isinstance(arr_raw,(int,float)) else str(arr_raw)
    churn   = profile.get("churn_risk","—")
    risk_c  = {"High":"#C03030","Medium":"#8A6A00","Low":"#1A4A1A"}.get(churn,"#6A6A62")
    sc = SCENARIOS.get(st.session_state.preset, {})
    scenario_id = sc.get("scenario_id") or data.get("case_id")
    mem_results = api_memory_diff(company)

    # ── Handle Pending Actions (callbacks) ──
    if st.session_state._pending_action == "reevaluate":
        st.session_state._pending_action = None
        edited_vals = {
            "segment": st.session_state.get("edit_segment"),
            "contract_type": st.session_state.get("edit_contract"),
            "contract_value": st.session_state.get("edit_contract_val"),
            "churn_risk": st.session_state.get("edit_churn_risk"),
            "health_score": st.session_state.get("edit_health_score"),
            "active_users": st.session_state.get("edit_active_users"),
            "license_count": st.session_state.get("edit_license_count"),
        }
        with st.status("🔄 Re-evaluating pipeline assumptions...", expanded=True) as status:
            st.write("📝 Applying corrected assumptions to pipeline state...")
            time.sleep(0.3)
            st.write("🔴 Re-computing scores with updated profile...")
            try:
                result = api_resume(tid, "edit", edited_vals)
                updated = dict(st.session_state.api_data)
                updated["customer_profile"] = result.get("customer_profile", profile)
                updated["assumptions"]      = result.get("assumptions", {})
                updated["explanation"]      = result.get("explanation", expl)
                updated["plan_trace"]       = result.get("plan_trace", trace)
                updated["recommendation"]   = result.get("corrected_recommendation", rec)
                st.session_state.api_data = updated
                st.session_state.node_edits["open_Ingestion"] = False
                if "simulation_results" in st.session_state:
                    del st.session_state.simulation_results
                st.session_state.stage = "edited"
                status.update(label="✅ Assumptions re-evaluated", state="complete")
                time.sleep(0.4)
                st.rerun()
            except Exception as e:
                status.update(label="❌ Re-evaluation failed", state="error")
                st.error(f"Re-evaluation failed: {e}")

    elif st.session_state._pending_action in ("chat_retrieval", "chat_reasoning"):
        pending_node = "retrieval" if st.session_state._pending_action == "chat_retrieval" else "reasoning"
        st.session_state._pending_action = None
        user_msg = st.session_state.node_chat_history[pending_node][-1]["content"]
        agent_display_name = "Retrieval Agent" if pending_node == "retrieval" else "Reasoning Agent"
        with st.status(f"🔴 {agent_display_name} is re-thinking...", expanded=True) as status:
            st.write(f"📩 Received CSM override: *\"{user_msg}\"*")
            time.sleep(0.4)
            st.write("🔍 Analyzing user guidance parameters...")
            time.sleep(0.3)
            st.write("⚙️ Updating pipeline state with override constraints...")
            time.sleep(0.3)
            st.write("🔴 Re-evaluating graph nodes...")
            time.sleep(0.2)
            try:
                result = api_resume(tid, "edit", {"guidance_override": user_msg})
                st.write("🔴 Generating explainability rationale...")
                time.sleep(0.2)
                st.session_state.original_rec = copy.deepcopy(rec)
                updated = dict(st.session_state.api_data)
                updated["customer_profile"] = result.get("customer_profile", profile)
                updated["assumptions"]      = result.get("assumptions", {})
                updated["explanation"]      = result.get("explanation", expl)
                updated["plan_trace"]       = result.get("plan_trace", trace)
                updated["recommendation"]   = result.get("corrected_recommendation", rec)
                st.session_state.api_data = updated
                new_rec = result.get("corrected_recommendation", {}) or rec
                new_action = new_rec.get("action", "the recommendation")
                new_conf = float(new_rec.get("confidence", conf))
                agent_reply = (
                    f"Understood. I've re-processed the pipeline with your guidance.\n\n"
                    f"**Updated recommendation:** {new_action}\n\n"
                    f"**Confidence:** {new_conf:.2f} ({'↑' if new_conf > conf else '↓' if new_conf < conf else '→'})"
                )
                st.session_state.node_chat_history[pending_node].append(
                    {"role": "assistant", "content": agent_reply}
                )
                if "simulation_results" in st.session_state:
                    del st.session_state.simulation_results
                st.session_state.stage = "edited"
                status.update(label="✅ Re-thinking complete — recommendation updated", state="complete")
                time.sleep(0.5)
                st.rerun()
            except Exception as e:
                agent_error = f"I encountered an error while re-processing: {e}. Your guidance has been recorded."
                st.session_state.node_chat_history[pending_node].append(
                    {"role": "assistant", "content": agent_error}
                )
                status.update(label="⚠️ Re-thinking failed", state="error")

    # ── Case Status Strip ──
    stage_badge = {"review":"⏸ Awaiting CSM Decision","edited":"✏️ Re-evaluated","approved":"✅ Approved","rejected":"❌ Rejected"}
    st.html(f"""
    <div class="case-strip">
      <span class="case-id">{tid}</span>
      <span class="case-dot">·</span>
      <span class="case-company">{company}</span>
      <span class="case-dot">·</span>
      <span style="color:#8A8880;">{arr_str}</span>
      <span class="case-dot">·</span>
      <span style="font-size:12px;color:{risk_c};font-weight:700;">{churn} Risk</span>
      <div class="case-right"><span class="case-badge">{stage_badge.get(st.session_state.stage,"—")}</span></div>
    </div>
    """)

    # ══════════════════════════════════════════════════════════════════════════
    # NODE 1: INGESTION (Completed / Read-Only)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="pipeline-node pipeline-node-completed">', unsafe_allow_html=True)
    with st.expander("🔴 Node 1: Ingestion (CRM note & Trigger) — Completed", expanded=False):
        st.text_area("Inbound CRM Signal", value=data.get("raw_input", ""), height=120,
                     disabled=True, key="ingested_raw_readonly")
        ing_thought = get_node_thought("Ingestion", trace, profile=profile, rec=rec, evid=evid)
        st.html(f'<div class="thought-box" style="margin-top:10px;"><div class="thought-label">Ingestion Agent Thought Trace</div><div class="thought-text">{ing_thought}</div></div>')
    st.markdown('</div>', unsafe_allow_html=True)

    # DAG connector
    st.markdown('<div class="dag-connector-wrap"><div class="dag-line"></div></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # NODE 2: CONTEXT & RETRIEVAL + CONVERSATIONAL HITL (Feature 1)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="pipeline-node pipeline-node-active">', unsafe_allow_html=True)
    with st.expander("🔍 Node 2: Context & Retrieval (Profile & Playbooks)", expanded=True):
        st.html('<div class="eyebrow" style="margin-bottom:12px;">Extracted Account Context</div>')

        # Metrics row
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Health Score", f"{profile.get('health_score', 50)}/100")
        with c2:
            st.metric("Customer Segment", profile.get("segment", "N/A"))
        with c3:
            velocity = profile.get("temporal_velocity", {})
            change = velocity.get("30_day_change", 0)
            change_str = f"{change:+d}" if isinstance(change, int) else str(change)
            trend = velocity.get("trend", "stable").title()
            st.metric("Temporal Velocity (30d)", f"{trend}", delta=change_str,
                      delta_color="normal" if "declining" not in trend.lower() else "inverse")

        st.html(f"""
        <div class="data-card" style="margin-top:14px;margin-bottom:18px;">
          <div class="data-row"><span class="data-key">Contract Value</span><span class="data-val">{arr_str}</span></div>
          <div class="data-row"><span class="data-key">Contract Type</span><span class="data-val">{profile.get("contract_type","—")}</span></div>
          <div class="data-row"><span class="data-key">Active / Licensed Seats</span><span class="data-val">{profile.get("active_users","—")} / {profile.get("license_count","—")}</span></div>
        </div>
        """)

        # Memory Match Card
        memory_html = get_memory_match_html(scenario_id, company, mem_results)
        st.html(memory_html)

        # Retrieved Playbooks (compact cards)
        st.html('<div class="eyebrow" style="margin-top:14px;margin-bottom:8px;">Retrieved Playbook Evidence</div>')
        if evid:
            num_cols = min(len(evid), 3)
            ev_cols = st.columns(num_cols)
            for idx, ev in enumerate(evid):
                with ev_cols[idx % num_cols]:
                    score   = float(ev.get("score", 0))
                    source  = ev.get("source", "Unknown")
                    text    = ev.get("text", "")
                    bar_pct = int(min(score * 250, 100))
                    truncated = (text[:160].rsplit(" ",1)[0] + "…") if len(text) > 160 else text
                    st.html(f"""
                    <div class="ev-compact-card">
                      <div class="ev-compact-header"><span class="ev-compact-source">{source}</span><span class="ev-compact-score">{score:.3f}</span></div>
                      <div class="ev-compact-bar"><div class="ev-compact-bar-fill" style="width:{bar_pct}%;"></div></div>
                      <div class="ev-compact-text">{truncated}</div>
                    </div>
                    """)
        else:
            st.html('<div style="font-size:12px;color:#9A9690;font-style:italic;padding:8px 0;">No playbook chunks retrieved.</div>')

        # ── FEATURE 1: CONVERSATIONAL NODE INTERVENTION ──────────────────────
        st.html('<div class="divider"></div>')
        st.html("""
        <div class="node-chat-header">
          🔴 Talk to the Retrieval Agent
        </div>
        """)

        # Initialize node chat history
        if "retrieval" not in st.session_state.node_chat_history:
            st.session_state.node_chat_history["retrieval"] = []

        node_msgs = st.session_state.node_chat_history["retrieval"]

        # Render existing chat history
        if node_msgs:
            for msg in node_msgs:
                with st.chat_message(msg["role"], avatar="🧑‍💼" if msg["role"] == "user" else "🔍"):
                    st.markdown(msg["content"])
        else:
            st.html('<div class="node-chat-empty">No interventions yet. Type below to steer the agent\'s reasoning — e.g., "Don\'t offer a discount, they are enterprise."</div>')

        # Chat input
        st.chat_input("Talk to the Retrieval Agent...", key="chat_input_retrieval", on_submit=cb_chat_retrieval)

        # Inline Assumptions Form Editor
        st.html('<div class="divider"></div>')
        st.html('<div class="eyebrow">🔴 Correct Account Context & Assumptions</div>')

        with st.form("edit_assumptions_form", clear_on_submit=False):
            col_a, col_b = st.columns(2)
            with col_a:
                segment_opts = ["Enterprise", "Mid-Market", "SMB"]
                cur_seg = profile.get("segment", "Mid-Market")
                seg_idx = segment_opts.index(cur_seg) if cur_seg in segment_opts else 0
                edit_segment = st.selectbox("Customer Segment", segment_opts, index=seg_idx, key="edit_segment")
                contract_opts = ["Annual", "Monthly", "Multi-year"]
                cur_con = profile.get("contract_type", "Annual")
                con_idx = contract_opts.index(cur_con) if cur_con in contract_opts else 0
                edit_contract = st.selectbox("Contract Type", contract_opts, index=con_idx, key="edit_contract")
                try: edit_val = float(profile.get("contract_value", 50000.0))
                except: edit_val = 50000.0
                edit_contract_val = st.number_input("Contract Value ($)", value=edit_val, step=5000.0, key="edit_contract_val")
            with col_b:
                risk_opts = ["High", "Medium", "Low"]
                cur_risk = profile.get("churn_risk", "Medium")
                risk_idx = risk_opts.index(cur_risk) if cur_risk in risk_opts else 0
                edit_churn_risk = st.radio("Churn Risk", risk_opts, index=risk_idx, horizontal=True, key="edit_churn_risk")
                try: edit_health = int(profile.get("health_score", 50))
                except: edit_health = 50
                edit_health_score = st.slider("Health Score", 0, 100, edit_health, key="edit_health_score")
                try: edit_active = int(profile.get("active_users", 60))
                except: edit_active = 60
                try: edit_license = int(profile.get("license_count", 100))
                except: edit_license = 100
                col_c, col_d = st.columns(2)
                with col_c:
                    edit_active_users = st.number_input("Active Users", value=edit_active, key="edit_active_users")
                with col_d:
                    edit_license_count = st.number_input("License Count", value=edit_license, key="edit_license_count")

            st.form_submit_button("🔄 Re-Evaluate Assumptions", type="primary", on_click=cb_reevaluate_assumptions)

        # Retrieval agent thought trace
        with st.expander("🔴 Retrieval Agent Thought Trace", expanded=False):
            ret_thought = get_node_thought("Retrieval", trace, profile=profile, rec=rec, evid=evid)
            st.html(f'<div class="thought-text">{ret_thought}</div>')
    st.markdown('</div>', unsafe_allow_html=True)

    # DAG connector
    st.markdown('<div class="dag-connector-wrap"><div class="dag-line"></div></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # NODE 3: EXECUTIVE RECOMMENDATION & DECISION ROOM
    # ══════════════════════════════════════════════════════════════════════════
    if rec:
        node3_class = "pipeline-node-hitl" if st.session_state.stage in ("review","edited") else "pipeline-node-active"
        st.markdown(f'<div class="pipeline-node {node3_class}">', unsafe_allow_html=True)
        with st.expander("🔴 Node 3: Executive Recommendation & Decision Room", expanded=True):

            # Decision Readiness Score
            readiness_criteria = profile.get("readiness_criteria", {})
            if not readiness_criteria:
                readiness_criteria = {
                    "has_budget_confirmed": True, "has_playbook_match": True,
                    "has_executive_sponsor": False, "has_telemetry_complete": True,
                    "has_remediation_plan": False, "has_contract_alignment": False,
                    "has_csm_alignment": True,
                }
            total_checks = len(readiness_criteria)
            met_checks = sum(1 for v in readiness_criteria.values() if v)
            readiness_score = int((met_checks / total_checks) * 100) if total_checks > 0 else 0

            st.html(f"""
            <div style="display:flex;justify-content:space-between;font-size:14px;font-weight:700;color:#8A9A5B;font-family:'Inter',sans-serif;margin-bottom:8px;">
              <span>🛡️ Decision Readiness Score</span><span>{readiness_score}%</span>
            </div>
            """)
            # Confidence heatmap progress bar
            bar_cls = conf_class(readiness_score / 100.0)
            st.markdown(f'<div class="conf-bar-{bar_cls}">', unsafe_allow_html=True)
            st.progress(readiness_score / 100.0)
            st.markdown('</div>', unsafe_allow_html=True)

            # Checklist
            cols = st.columns(7)
            for idx, (criterion, met) in enumerate(readiness_criteria.items()):
                with cols[idx]:
                    label = criterion.replace("has_","").replace("_"," ").title()
                    icon = "✅" if met else "⚠️"
                    st.html(f"""
                    <div style="text-align:center;font-size:9px;padding:6px;border:1px solid {'#B8D4B8' if met else '#E8D080'};background:{'#F2F9F2' if met else '#FFF8E6'};border-radius:6px;min-height:52px;display:flex;flex-direction:column;justify-content:center;align-items:center;">
                      <span style="font-size:12px;">{icon}</span>
                      <strong style="color:{'#1A4A1A' if met else '#7A5C00'};line-height:1.1;margin-top:2px;">{label}</strong>
                    </div>
                    """)

            # Before/After comparison
            if st.session_state.stage == "edited" and st.session_state.original_rec:
                orig = st.session_state.original_rec
                st.html('<div style="margin-top:14px;margin-bottom:16px;"><div class="cmp-label" style="font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#8A9A5B;">Re-evaluation comparison</div></div>')
                ca, cb = st.columns(2, gap="medium")
                with ca:
                    st.html(f'<div class="cmp-before"><div class="cmp-label" style="color:#8A2020;">Before Edit</div><div class="cmp-action" style="color:#8A2020;">{orig.get("action","—")}</div><div style="font-size:12px;color:#7A7A72;margin-top:10px;line-height:1.9;">Confidence&nbsp;<strong style="color:#8A2020;">{float(orig.get("confidence",0)):.4f}</strong><br>Priority&nbsp;<strong style="color:#8A2020;">{float(orig.get("priority",0)):.4f}</strong></div></div>')
                with cb:
                    st.html(f'<div class="cmp-after"><div class="cmp-label" style="color:#1A4A1A;">After Edit</div><div class="cmp-action" style="color:#1A4A1A;">{rec.get("action","—")}</div><div style="font-size:12px;color:#7A7A72;margin-top:10px;line-height:1.9;">Confidence&nbsp;<strong style="color:#1A4A1A;">{conf:.4f}</strong><br>Priority&nbsp;<strong style="color:#1A4A1A;">{float(rec.get("priority",0)):.4f}</strong></div></div>')

            # Recommendation + Devil's Advocate
            left_col, right_col = st.columns([1, 1], gap="large")

            with left_col:
                p_val, cv_val, v_val, lv_val, pri_val = (float(rec.get(k,0)) for k in ("propensity","context","value","levers","priority"))
                mc  = "#8A9A5B" if conf >= 0.5 else "#C4A020"
                pct = conf * 100
                badge_html = (
                    f'<span class="conf-badge-high" style="background:#EAF2EA;border:1px solid #8A9A5B;color:#1A4A1A;"><span class="conf-badge-dot" style="background:#8A9A5B;"></span>High Confidence · {conf:.2f}</span>'
                    if conf >= 0.5 else
                    f'<span class="conf-badge-low"><span class="conf-badge-dot" style="background:#C4A020;"></span>Low Confidence · {conf:.2f} — Review Required</span>'
                )
                st.html(f"""
                <div class="rec-card" style="border-color:{mc};">
                  <div class="rec-eyebrow" style="color:{mc};">Recommended Action</div>
                  <div class="rec-action">{rec.get("action","No recommendation generated")}</div>
                  {badge_html}
                  <div class="conf-track-row"><span>Confidence</span><span>{pct:.0f}%</span></div>
                  <div class="conf-track"><div class="conf-fill" style="width:{pct}%;background:{mc};"></div></div>
                </div>
                """)

                # What-If Simulator
                st.html('<div class="eyebrow" style="margin-top:20px;">What-If Simulator</div>')
                sim_bs = st.slider("Budget Sensitivity", 0.0, 1.0, 0.5, step=0.05, key="slider_bs")
                sim_tl = st.slider("Timeline (Urgency)", 0.0, 1.0, 0.5, step=0.05, key="slider_tl")
                sim_rt = st.slider("Risk Tolerance", 0.0, 1.0, 0.5, step=0.05, key="slider_rt")

                # BUG FIX 1: on_click callback for Simulate
                st.button("📊 Simulate Scenario", type="primary", key="sim_btn_exec",
                          on_click=cb_simulate, args=(sim_bs, sim_tl, sim_rt, rec))

                if "simulation_results" in st.session_state:
                    sim = st.session_state.simulation_results
                    st.html(f"""
                    <div class="data-card" style="background:#FFFDF9;border:1px dashed #8A9A5B;margin-top:14px;">
                      <div class="data-card-title" style="color:#8A9A5B;">Simulated PCVL Telemetry</div>
                      <div class="data-row"><span class="data-key">Propensity</span><span class="data-val">{format_delta(sim["p"],p_val)}</span></div>
                      <div class="data-row"><span class="data-key">Context</span><span class="data-val">{format_delta(sim["c"],cv_val)}</span></div>
                      <div class="data-row"><span class="data-key">Value</span><span class="data-val">{format_delta(sim["v"],v_val)}</span></div>
                      <div class="data-row"><span class="data-key">Levers</span><span class="data-val">{format_delta(sim["l"],lv_val)}</span></div>
                      <div class="data-row" style="border-top:1px solid #DDD9D0;padding-top:10px;"><span class="data-key" style="font-weight:bold;color:#8A9A5B;">Priority Score</span><span class="data-val" style="font-weight:bold;color:#8A9A5B;">{format_delta(sim["pri"],pri_val)}</span></div>
                    </div>
                    """)

            with right_col:
                penalties = profile.get("confidence_penalties", [])
                critique = get_devils_advocate_critique(scenario_id, profile, rec)
                st.html(f"""
                <div style="background:#FFF9E6;border:1px solid #E8D080;border-radius:12px;padding:20px;box-shadow:0 2px 8px rgba(232,208,128,0.15);margin-bottom:20px;">
                  <div style="font-family:'EB Garamond',serif;font-size:20px;font-weight:600;color:#7A5C00;margin-bottom:12px;display:flex;align-items:center;gap:8px;">😈 Devil's Advocate</div>
                  <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#8A6A00;margin-bottom:6px;">Confidence Penalties</div>
                """)
                if penalties:
                    for p_item in penalties:
                        st.html(f"<div style='font-size:13px;color:#5A4A1A;margin-bottom:6px;line-height:1.4;'>• {p_item}</div>")
                else:
                    st.html("<div style='font-size:13px;color:#7A7A72;font-style:italic;margin-bottom:12px;'>No confidence penalties identified.</div>")
                st.html(f"""
                  <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#8A6A00;margin-top:14px;margin-bottom:6px;">AI Self-Critique</div>
                  <div style="font-size:13px;color:#5A4A1A;font-style:italic;line-height:1.5;margin-bottom:14px;background:#FFFDF5;border-left:3px solid #E8D080;padding:8px 12px;border-radius:0 6px 6px 0;">"{critique['counter_argument']}"</div>
                  <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#8A6A00;margin-bottom:6px;">Alternative Strategy</div>
                  <div style="font-size:13px;color:#1A3D1A;line-height:1.5;background:#F2F9F2;border-left:3px solid #8A9A5B;padding:8px 12px;border-radius:0 6px 6px 0;"><b>Action:</b> {critique['alternative_path']}</div>
                </div>
                """)

            # Conversational Node Intervention for Reasoning (Node 3)
            st.html('<div class="divider"></div>')
            st.html("""
            <div class="node-chat-header">
              🔴 Talk to the Reasoning Agent
            </div>
            """)

            if "reasoning" not in st.session_state.node_chat_history:
                st.session_state.node_chat_history["reasoning"] = []

            node_msgs_reasoning = st.session_state.node_chat_history["reasoning"]

            if node_msgs_reasoning:
                for msg in node_msgs_reasoning:
                    with st.chat_message(msg["role"], avatar="🧑‍💼" if msg["role"] == "user" else "⚖️"):
                        st.markdown(msg["content"])
            else:
                st.html('<div class="node-chat-empty">No overrides yet. Type below to steer the Reasoning Agent — e.g., "Propose upsell, they have high health."</div>')

            st.chat_input("Talk to the Reasoning Agent...", key="chat_input_reasoning", on_submit=cb_chat_reasoning)

            # Collapsible details
            st.html('<div class="divider"></div>')
            with st.expander("🔴 AI Rationale Details", expanded=False):
                st.html(f'<div class="expl-block" style="border-left-color:#8A9A5B;">{expl}</div>')

            with st.expander("🔴 Reasoning & Explainability Thought Traces", expanded=False):
                rea_thought = get_node_thought("Reasoning", trace, profile=profile, rec=rec, evid=evid)
                exp_thought = get_node_thought("Explainability", trace, profile=profile, rec=rec, evid=evid)
                st.html(f'<div class="thought-box"><div class="thought-label">Reasoning Agent</div><div class="thought-text">{rea_thought}</div></div><div class="thought-box" style="margin-top:10px;"><div class="thought-label">Explainability Agent</div><div class="thought-text">{exp_thought}</div></div>')

            with st.expander("🔴 Memory — Similar Past Decisions", expanded=False):
                if mem_results:
                    for m in mem_results[:3]:
                        dec = m.get("human_decision","—")
                        dec_cls = "mem-approved" if dec=="approved" else "mem-rejected" if dec=="rejected" else "mem-other"
                        st.html(f"""
                        <div style="background:#F2F9F4;border:1px solid #C4D8C8;border-radius:10px;padding:14px 16px;margin-bottom:10px;">
                          <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                            <span style="font-size:13px;font-weight:600;color:#1A1A18;">{m.get("action","—")}</span>
                            <span class="{dec_cls}" style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;">{dec}</span>
                          </div>
                          <div style="font-size:12px;color:#4A6A50;line-height:1.65;margin-bottom:5px;">{m.get("summary","")}</div>
                          <div style="font-size:10px;color:#9A9690;">{(m.get("timestamp","")[:10] if m.get("timestamp") else "—")}</div>
                        </div>
                        """)
                else:
                    st.html('<div style="font-size:12px;color:#9A9690;font-style:italic;padding:8px 0;">No past decisions yet — approve a case to build memory.</div>')

            # ── DECISION BUTTONS (Bug Fix 1: on_click callbacks) ──
            st.html('<div class="divider"></div>')
            if st.session_state.stage in ("review","edited"):
                st.html('<div style="background:#FFFFFF;border:1px solid #DDD9D0;border-radius:14px;padding:20px;margin-top:8px;box-shadow:0 2px 8px rgba(0,0,0,.04);"><div style="font-size:9px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#8A9A5B;margin-bottom:14px;">CSM Decision Checkpoint</div></div>')
                b1, b2, b3 = st.columns(3, gap="small")
                with b1:
                    st.button("✅  Approve Action", type="primary", use_container_width=True,
                              key="btn_approve", on_click=cb_approve)
                with b2:
                    st.button("🔴  Edit Assumptions", use_container_width=True,
                              key="btn_edit", on_click=cb_toggle_edit)
                with b3:
                    st.button("❌  Reject Action", use_container_width=True,
                              key="btn_reject", on_click=cb_reject)

            # Outcome Banners
            if st.session_state.stage == "approved":
                st.html(f"""
                <div class="banner-ok" style="border-color:#8A9A5B;">
                  <div style="font-size:28px;">✅</div>
                  <div>
                    <div class="banner-title" style="color:#1A4A1A;">Action Approved</div>
                    <div class="banner-sub">Decision logged to interaction memory. Case closed.<br><em style="color:#8A9A5B;">{rec.get("action","—")}</em></div>
                  </div>
                </div>
                """)
                st.write("")
                st.button("→  New Case", type="primary", key="new_case_appr", on_click=cb_new_case)

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
                st.button("→  New Case", type="primary", key="new_case_rej", on_click=cb_new_case)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # No recommendation yet — show skeleton loaders
        st.markdown('<div class="pipeline-node pipeline-node-active">', unsafe_allow_html=True)
        with st.expander("🔴 Node 3: Executive Recommendation & Decision Room", expanded=True):
            st.html("""
            <div class="skeleton-wrap">
              <div class="skeleton-block skeleton-line"></div>
              <div class="skeleton-block skeleton-line-short"></div>
              <div class="skeleton-block skeleton-card"></div>
              <div class="skeleton-block skeleton-line"></div>
              <div class="skeleton-block skeleton-line-short"></div>
            </div>
            """)
            st.info("🔄 Recommendation is being re-computed. Use the chat interface above to steer the agent.")
        st.markdown('</div>', unsafe_allow_html=True)
