import streamlit as st
import copy
import time
import requests
import os

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
#  CSS INJECTION  — Streamlit 1.40+ compatible
#  We load style.css as a raw string and inject via st.html()
# ─────────────────────────────────────────────────────────────────────────────
_css_path = os.path.join(os.path.dirname(__file__), "style.css")
with open(_css_path) as _f:
    _css = _f.read()

st.html(f"""
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{_css}

/* ── Component styles ─────────────────────────────────────────────────── */
.pulse-nav {{
  display:flex; align-items:center; justify-content:space-between;
  padding:28px 0 24px; border-bottom:1px solid #D4CFC6; margin-bottom:40px;
}}
.pulse-logo-mark {{
  font-family:'EB Garamond',serif; font-size:28px; font-weight:700;
  color:#1A3D1A; letter-spacing:-0.02em;
}}
.pulse-logo-sub {{
  font-size:11px; font-weight:600; letter-spacing:0.12em;
  text-transform:uppercase; color:#8A8880; margin-top:2px;
}}
.nav-links {{ display:flex; gap:32px; align-items:center; }}
.nav-link {{ font-size:13px; color:#5A5A55; font-weight:500; }}
.nav-status {{
  display:inline-flex; align-items:center; gap:7px; font-size:12px;
  font-weight:600; background:#E8F0E8; border:1px solid #C2D4C2;
  color:#1A3D1A; padding:5px 14px; border-radius:20px;
}}
.nav-offline {{
  display:inline-flex; align-items:center; gap:7px; font-size:12px;
  font-weight:600; background:#FFF3CD; border:1px solid #FFEBA8;
  color:#856404; padding:5px 14px; border-radius:20px;
}}
.nav-dot {{
  width:7px; height:7px; border-radius:50%;
  animation:blink 2s infinite; display:inline-block;
}}
@keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}

.hero-label {{
  font-size:11px; font-weight:700; letter-spacing:0.15em;
  text-transform:uppercase; color:#1A3D1A; margin-bottom:12px;
  display:flex; align-items:center; gap:10px;
}}
.hero-label::before {{
  content:''; display:block; width:28px; height:1px; background:#1A3D1A;
}}
.hero-headline {{
  font-family:'EB Garamond',serif; font-size:54px; font-weight:500;
  color:#0F0F0E; line-height:1.08; letter-spacing:-0.025em; margin-bottom:20px;
}}
.hero-headline em {{ font-style:italic; color:#1A3D1A; }}
.hero-sub {{ font-size:16px; color:#6B6B66; line-height:1.6; max-width:560px; }}

.eyebrow {{
  font-size:10px; font-weight:700; letter-spacing:0.15em;
  text-transform:uppercase; color:#8A8880; margin-bottom:10px;
}}
.divider {{ border:none; border-top:1px solid #D4CFC6; margin:28px 0; }}

.case-strip {{
  display:flex; align-items:center; gap:16px; padding:10px 0;
  margin-bottom:32px; border-bottom:1px solid #D4CFC6; font-size:12px; color:#8A8880;
}}
.case-id {{
  font-family:'JetBrains Mono',monospace; font-size:11px; color:#1A3D1A;
  background:#E8F0E8; padding:2px 8px; border-radius:4px;
}}
.case-strip-dot {{ color:#D4CFC6; }}
.case-strip-right {{ margin-left:auto; color:#1A3D1A; font-weight:600; font-size:11px; }}

.rec-card {{
  background:#FFFFFF; border:1px solid #C2D4C2; border-radius:12px;
  padding:28px; margin-bottom:24px; box-shadow:0 2px 12px rgba(26,61,26,.06);
}}
.rec-action {{
  font-family:'EB Garamond',serif; font-size:28px; font-weight:600;
  color:#0F0F0E; line-height:1.15; margin-bottom:12px;
}}
.badge-high {{
  display:inline-flex; align-items:center; gap:6px; background:#E8F0E8;
  border:1px solid #A8C4A8; color:#1A3D1A; padding:4px 12px;
  border-radius:20px; font-size:11px; font-weight:700;
}}
.badge-low {{
  display:inline-flex; align-items:center; gap:6px; background:#FDF8EE;
  border:1px solid #E6C870; color:#8A6A00; padding:4px 12px;
  border-radius:20px; font-size:11px; font-weight:700;
}}
.badge-dot {{
  width:6px; height:6px; border-radius:50%; display:inline-block;
}}
.conf-row {{
  display:flex; justify-content:space-between; font-size:10px;
  color:#8A8880; margin-bottom:4px; margin-top:14px;
}}
.conf-track {{
  background:#EDE9E3; border-radius:4px; height:6px; overflow:hidden;
}}
.conf-fill {{ height:100%; border-radius:4px; }}

.pcvl-grid {{
  display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:16px 0;
}}
.pcvl-tile {{
  background:#FFFFFF; border:1px solid #D4CFC6; border-radius:10px;
  padding:16px 12px 12px; text-align:center;
  transition:border-color .18s,transform .18s;
}}
.pcvl-tile:hover {{ border-color:#1A3D1A; transform:translateY(-2px); }}
.pcvl-tile-hi {{ border-color:#C2D4C2; background:#F0F7F0; }}
.pcvl-label {{
  font-size:9px; font-weight:700; letter-spacing:0.15em;
  text-transform:uppercase; color:#8A8880; margin-bottom:6px;
}}
.pcvl-value {{
  font-family:'EB Garamond',serif; font-size:32px;
  font-weight:600; line-height:1;
}}
.pcvl-sub {{ font-size:9px; color:#8A8880; margin-top:4px; }}

.ev-wrap {{
  background:#FFFFFF; border:1px solid #D4CFC6; border-radius:8px;
  padding:14px 16px; margin-bottom:10px;
}}
.ev-row {{
  display:flex; align-items:center; justify-content:space-between;
}}
.ev-source {{
  background:#E8F0E8; border:1px solid #A8C4A8; color:#1A3D1A;
  font-size:10px; font-weight:700; padding:3px 9px; border-radius:4px;
}}
.ev-score {{ font-size:11px; color:#8A8880; font-family:'JetBrains Mono',monospace; }}
.ev-bar-track {{
  height:3px; background:#EDE9E3; border-radius:2px;
  margin-top:8px; overflow:hidden;
}}
.ev-bar-fill {{ height:100%; border-radius:2px; background:#1A3D1A; }}

.expl-quote {{
  border-left:3px solid #1A3D1A; padding:14px 18px; background:#F0EDE8;
  border-radius:0 8px 8px 0; font-size:14px; color:#2A2A25;
  line-height:1.65; margin:16px 0;
}}
.lever-pill {{
  display:inline-flex; align-items:center; gap:6px; background:#F0EDE8;
  border:1px solid #D4CFC6; color:#3A3A35; border-radius:6px;
  padding:6px 12px; font-size:12px; font-weight:500; margin-top:10px;
}}

.mem-diff {{
  background:#EDF5F0; border:1px solid #A8C4B0; border-radius:10px;
  padding:16px 20px; margin-bottom:28px; font-size:13px;
  color:#2A4A30; line-height:1.6;
}}

.banner-ok {{
  background:#E8F0E8; border:1px solid #A8C4A8; border-radius:10px;
  padding:20px 24px; margin-top:16px; display:flex;
  align-items:flex-start; gap:16px;
}}
.banner-no {{
  background:#FDECEA; border:1px solid #F0BABA; border-radius:10px;
  padding:20px 24px; margin-top:16px; display:flex;
  align-items:flex-start; gap:16px;
}}
.banner-title {{
  font-family:'EB Garamond',serif; font-size:18px; font-weight:600;
}}
.banner-sub {{ font-size:12px; color:#6B6B66; margin-top:3px; line-height:1.5; }}

.chip {{
  display:inline-flex; align-items:center; gap:5px; padding:3px 10px;
  border-radius:4px; font-size:10px; font-weight:700;
  letter-spacing:0.08em; text-transform:uppercase;
}}
.chip-pending  {{ background:#FDF8EE; border:1px solid #E6C870; color:#8A6A00; }}
.chip-approved {{ background:#E8F0E8; border:1px solid #A8C4A8; color:#1A3D1A; }}
.chip-rejected {{ background:#FDECEA; border:1px solid #F0BABA; color:#B03020; }}
.chip-editing  {{ background:#F0EAF8; border:1px solid #C8A8E0; color:#6030A0; }}

.sb-row {{
  display:flex; justify-content:space-between; align-items:center;
  padding:7px 0; border-bottom:1px solid #254B25; font-size:12px;
}}
.sb-head {{
  font-size:10px; font-weight:700; letter-spacing:0.12em;
  text-transform:uppercase; color:#A8C4A8; margin:24px 0 10px;
  padding-bottom:6px; border-bottom:1px solid #254B25;
}}
.health-track {{
  background:#254B25; border-radius:3px; height:4px;
  margin-top:6px; overflow:hidden;
}}
.health-fill {{ height:100%; border-radius:3px; }}

/* Agent tree */
.node-header {{
  padding-top:4px; margin-bottom:8px;
}}
.node-name {{
  font-family:'EB Garamond',serif; font-size:19px;
  font-weight:600; color:#0F0F0E;
}}
.node-role {{ font-size:11px; color:#8A8880; font-weight:500; }}
.node-thought {{
  background:#FFFFFF; border:1px solid #D4CFC6; border-radius:12px;
  padding:16px 20px; margin-bottom:12px;
  box-shadow:0 2px 8px rgba(0,0,0,.015);
}}
.node-thought-lbl {{
  font-size:9px; font-weight:700; letter-spacing:0.12em;
  text-transform:uppercase; color:#8A8880; margin-bottom:6px;
}}
.node-thought-txt {{ font-size:13px; color:#4A4A45; line-height:1.65; }}
.out-card {{
  background:#FDFDFB; border:1px solid #D4CFC6;
  border-radius:8px; padding:14px 18px; margin-bottom:12px;
}}
.out-title {{
  font-size:9px; font-weight:700; letter-spacing:0.12em;
  text-transform:uppercase; color:#1A3D1A; margin-bottom:8px;
}}
.out-row {{
  display:flex; justify-content:space-between;
  padding:5px 0; border-bottom:1px solid #EAE6DF; font-size:12.5px;
}}
.out-row-k {{ color:#8A8880; }}
.out-row-v {{ font-weight:600; color:#0F0F0E; }}
.assumption-tag {{
  display:inline-flex; align-items:center; gap:6px; background:#FDF8EE;
  border:1px solid #E6C870; color:#7A5800; border-radius:5px;
  padding:3px 10px; font-size:11px; font-weight:600;
  margin-right:5px; margin-bottom:4px;
}}
.pill-route {{
  background:#E8F0E8; border:1px solid #A8C4A8; padding:4px 12px;
  border-radius:20px; font-size:11px; font-weight:600; color:#1A3D1A;
}}
.pill-hitl {{
  background:#F0EDE8; border:1px solid #D4CFC6; padding:4px 12px;
  border-radius:20px; font-size:11px; font-weight:600; color:#3A3A35;
}}
.pill-score {{
  background:#FFFFFF; border:1px solid #D4CFC6; padding:6px 12px;
  border-radius:8px; font-size:12px; display:inline-flex; gap:6px;
}}

.assume-box {{
  background:#FFFDF5; border:1px solid #E6C870; border-radius:10px;
  padding:18px 20px; margin:4px 0 12px;
}}
.assume-box-title {{
  font-size:10px; font-weight:700; letter-spacing:0.12em;
  text-transform:uppercase; color:#8A6A00; margin-bottom:14px;
}}

.cmp-before {{
  background:#FDF3F3; border:1px solid #F0BABA;
  border-radius:10px; padding:20px;
}}
.cmp-after {{
  background:#F0F7F0; border:1px solid #A8C4A8;
  border-radius:10px; padding:20px;
}}
.cmp-label {{
  font-size:9px; font-weight:700; letter-spacing:0.12em;
  text-transform:uppercase; margin-bottom:8px;
}}
.cmp-action {{
  font-family:'EB Garamond',serif; font-size:18px; font-weight:600;
}}

</style>
""")

# ─────────────────────────────────────────────────────────────────────────────
#  API CLIENT
# ─────────────────────────────────────────────────────────────────────────────
BACKEND = "http://localhost:8000"

def api_health() -> bool:
    try:
        r = requests.get(f"{BACKEND}/health", timeout=1.5)
        return r.status_code == 200
    except Exception:
        return False

def api_process(raw_input: str) -> dict:
    r = requests.post(f"{BACKEND}/process", json={"raw_input": raw_input}, timeout=30)
    r.raise_for_status()
    return r.json()

def api_resume(thread_id: str, decision: str, edit_payload: dict = None) -> dict:
    body = {"thread_id": thread_id, "decision": decision}
    if edit_payload:
        body["edit_payload"] = edit_payload
    r = requests.post(f"{BACKEND}/resume", json=body, timeout=30)
    r.raise_for_status()
    return r.json()

# ─────────────────────────────────────────────────────────────────────────────
#  DEMO PRESETS  — raw CRM text only, no fake response data
# ─────────────────────────────────────────────────────────────────────────────
PRESETS = {
    "🔴  ACME Corp — Churn Risk": (
        "ACME Corp's lead CSM reports that usage of key dashboards has dropped 40% in the last "
        "30 days. The primary champion VP of Product left the company last week, and they are "
        "currently on an annual contract renewing in 90 days. Need immediate playbook action."
    ),
    "🟢  Globex Inc — Expansion": (
        "Globex Inc has added 50 new seats this month, hitting 98% utilization. "
        "The new Director of Customer Experience expressed interest in our premium analytics add-on. "
        "They are currently on a self-serve monthly plan."
    ),
    "🟡  Initech Co — Low Confidence": (
        "Initech Co shows fluctuating API usage. A junior support ticket mentions they might be "
        "migrating to a competitor, but the customer contact hasn't responded. No executive "
        "sponsor listed."
    ),
}
PRESET_KEYS = list(PRESETS.keys())

# ─────────────────────────────────────────────────────────────────────────────
#  AGENT NODE DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────
AGENT_NODES = [
    {"agent": "Planner",        "icon": "🧭", "role": "Orchestration Planner"},
    {"agent": "Ingestion",      "icon": "📥", "role": "Data Ingestion Agent"},
    {"agent": "Retrieval",      "icon": "🔍", "role": "Knowledge Retrieval Agent"},
    {"agent": "Reasoning",      "icon": "⚖️",  "role": "Reasoning & Scoring Agent"},
    {"agent": "Explainability", "icon": "💬", "role": "Explainability Agent"},
    {"agent": "HITL Gate",      "icon": "🛑", "role": "Human-in-the-Loop Interrupt"},
]

def get_node_thought(agent: str, plan_trace: list) -> str:
    for line in (plan_trace or []):
        if isinstance(line, str) and line.strip().startswith(agent):
            parts = line.split(":", 1)
            if len(parts) == 2:
                return parts[1].strip()
    return f"{agent} completed its step."

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def _defaults():
    defaults = {
        "preset":       PRESET_KEYS[0],
        "stage":        "input",
        "api_data":     None,
        "thread_id":    None,
        "original_rec": None,
        "node_edits":   {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_defaults()

def reset():
    for k in ["stage", "api_data", "thread_id", "original_rec", "node_edits"]:
        if k in st.session_state:
            del st.session_state[k]
    _defaults()

# ─────────────────────────────────────────────────────────────────────────────
#  NAVIGATION BAR
# ─────────────────────────────────────────────────────────────────────────────
online = api_health()
if online:
    status_badge = '<span class="nav-status"><span class="nav-dot" style="background:#1A3D1A;"></span>Backend Connected</span>'
else:
    status_badge = '<span class="nav-offline"><span class="nav-dot" style="background:#856404;"></span>Backend Offline</span>'

st.html(f"""
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
    {status_badge}
  </div>
</div>
""")

if not online:
    st.warning("⚠️ FastAPI backend is offline. Start it: `uvicorn api.main:app --port 8000`")

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.html('<div style="font-family:\'EB Garamond\',serif;font-size:20px;font-weight:600;color:#FFFFFF;margin-bottom:4px;">Case Runner</div>')
    st.html('<div style="font-size:11px;color:#A8C4A8;margin-bottom:16px;">Select a demo scenario</div>')

    sel = st.selectbox("Preset", PRESET_KEYS,
                       index=PRESET_KEYS.index(st.session_state.preset),
                       label_visibility="collapsed")
    if sel != st.session_state.preset:
        st.session_state.preset = sel
        reset()
        st.rerun()

    data = st.session_state.api_data
    st.html('<div class="sb-head">Account Profile</div>')
    if data:
        profile = data.get("customer_profile") or {}
        health = profile.get("health_score", 50)
        if isinstance(health, str):
            try: health = int(str(health).split("/")[0].strip())
            except: health = 50
        health = max(0, min(100, int(health)))
        hc = "#3FB950" if health >= 75 else "#D4A017" if health >= 50 else "#F85149"
        rows_html = ""
        show = {
            "Company":  profile.get("company_name", "—"),
            "Segment":  profile.get("segment", "—"),
            "Contract": profile.get("contract_type", "—"),
            "Users":    str(profile.get("active_users", "—")),
            "Health":   f"{health}/100",
        }
        for k, v in show.items():
            color = hc if k == "Health" else "#FFFFFF"
            rows_html += f'<div class="sb-row"><span style="color:#A8C4A8;font-size:11px;">{k}</span><span style="color:{color};font-weight:600;font-size:12px;">{v}</span></div>'
        st.html(f'{rows_html}<div class="health-track"><div class="health-fill" style="width:{health}%;background:{hc};"></div></div>')
    else:
        st.html('<div style="font-size:11px;color:#A8C4A8;font-style:italic;">No case loaded yet.</div>')

    stage_labels = {
        "input":    ("chip-pending",  "Awaiting Input"),
        "review":   ("chip-pending",  "Pending Review"),
        "edited":   ("chip-editing",  "Re-evaluated"),
        "approved": ("chip-approved", "Approved"),
        "rejected": ("chip-rejected", "Rejected"),
    }
    cls, lbl = stage_labels.get(st.session_state.stage, ("chip-pending", "—"))
    st.html(f'<div class="sb-head">Flow State</div><span class="chip {cls}">{lbl}</span>')

# ─────────────────────────────────────────────────────────────────────────────
#  STAGE: INPUT
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.stage == "input":
    st.html("""
    <div style="margin-bottom:48px;">
      <div class="hero-label">Customer Intelligence</div>
      <div class="hero-headline">What is the <em>next best action</em><br>for this account?</div>
      <div class="hero-sub">
        Paste a CRM note, support transcript, or engagement signal.
        The orchestration layer routes it through specialised agents
        and returns a fully reasoned recommendation.
      </div>
    </div>
    """)

    raw = st.text_area(
        "Signal",
        value=PRESETS[st.session_state.preset],
        height=148,
        label_visibility="collapsed",
        placeholder="Paste CRM note, support ticket, or engagement signal…",
    )

    c1, c2 = st.columns([2, 6])
    with c1:
        go = st.button("⚡  Analyse Case", type="primary",
                       use_container_width=True, disabled=not online)
    with c2:
        st.html('<div style="padding-top:10px;font-size:12px;color:#8A8880;">Calls <code style="color:#1A3D1A;background:#E8F0E8;padding:2px 7px;border-radius:4px;font-family:\'JetBrains Mono\',monospace;">POST /process</code></div>')

    if go:
        with st.spinner("Running orchestration pipeline…"):
            try:
                result = api_process(raw)
                st.session_state.api_data  = result
                st.session_state.thread_id = result.get("thread_id")
                st.session_state.stage     = "review"
                st.rerun()
            except Exception as e:
                st.error(f"Backend error: {e}")

# ─────────────────────────────────────────────────────────────────────────────
#  STAGES: REVIEW / EDITED / APPROVED / REJECTED
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.stage in ("review", "edited", "approved", "rejected"):
    data    = st.session_state.api_data or {}
    rec     = data.get("recommendation") or {}
    conf    = float(rec.get("confidence", 1.0))
    profile = data.get("customer_profile") or {}
    assump  = data.get("assumptions") or {}
    evid    = data.get("retrieved_evidence") or []
    expl    = data.get("explanation") or "No explanation generated."
    trace   = data.get("plan_trace") or []
    tid     = st.session_state.thread_id or data.get("thread_id", "—")
    company = profile.get("company_name", "Unknown Account")
    arr_raw = profile.get("contract_value", "N/A")
    arr_str = f"${arr_raw:,}" if isinstance(arr_raw, (int, float)) else str(arr_raw)

    # Case strip
    st.html(f"""
    <div class="case-strip">
      <span class="case-id">{tid}</span>
      <span class="case-strip-dot">·</span>
      <span>{company}</span>
      <span class="case-strip-dot">·</span>
      <span>{arr_str}</span>
      <span class="case-strip-right">Awaiting CSM decision</span>
    </div>
    """)

    left, right = st.columns([5, 3], gap="large")

    # ── LEFT: Agent Thinking Tree ──────────────────────────────────────────
    with left:
        st.html('<div class="eyebrow">Reasoning Trace</div>')
        st.html('<div style="font-family:\'EB Garamond\',serif;font-size:24px;font-weight:600;color:#0F0F0E;margin-bottom:4px;">How the agents reasoned</div>')
        st.html('<div style="font-size:13px;color:#6B6B66;margin-bottom:24px;">Real-time execution trace from the backend orchestration graph.</div>')

        total = len(AGENT_NODES)

        for idx, node_def in enumerate(AGENT_NODES):
            agent    = node_def["agent"]
            icon     = node_def["icon"]
            role     = node_def["role"]
            is_last  = idx == total - 1
            is_hitl  = agent == "HITL Gate"
            circle_bg = "#0F2A0F" if is_hitl else "#1A3D1A"

            thought = get_node_thought(agent, trace)

            col_rail, col_content = st.columns([1, 12], gap="small")

            with col_rail:
                line_seg = "" if is_last else '<div style="width:2px;flex:1;min-height:40px;background:linear-gradient(to bottom,#1A3D1A,#C2D4C2);margin:4px auto;"></div>'
                st.html(f"""
                <div style="display:flex;flex-direction:column;align-items:center;height:100%;">
                  <div style="width:36px;height:36px;border-radius:50%;background:{circle_bg};
                              display:flex;align-items:center;justify-content:center;font-size:16px;
                              flex-shrink:0;">{icon}</div>
                  {line_seg}
                </div>
                """)

            with col_content:
                # Agent name + role (static strings — safe)
                st.html(f"""
                <div class="node-header">
                  <div class="node-name">{agent}</div>
                  <div class="node-role">{role}</div>
                </div>
                """)

                # Thought card — thought text rendered via st.write (escaped)
                st.html('<div class="node-thought"><div class="node-thought-lbl">💭 Internal Thought</div><div class="node-thought-txt">')
                st.write(thought)   # ← st.write escapes all special chars
                st.html('</div></div>')

                # ── Structured output per agent type ──────────────────────
                if agent == "Planner":
                    route_pills = " ➜ ".join([
                        f'<span class="pill-route">{s}</span>' if s != "HITL Gate"
                        else f'<span class="pill-hitl">{s}</span>'
                        for s in ["Ingestion","Retrieval","Reasoning","Explainability","HITL Gate"]
                    ])
                    st.html(f'<div class="out-card"><div class="out-title">Routing Decision</div><div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;">{route_pills}</div></div>')

                elif agent == "Ingestion":
                    fields = {
                        "Company":    profile.get("company_name"),
                        "Segment":    profile.get("segment"),
                        "Contract":   profile.get("contract_type"),
                        "Churn Risk": profile.get("churn_risk"),
                        "Health":     profile.get("health_score"),
                        "Users":      profile.get("active_users"),
                        "Licenses":   profile.get("license_count"),
                    }
                    rows = "".join(
                        f'<div class="out-row"><span class="out-row-k">{k}</span><span class="out-row-v">{v}</span></div>'
                        for k, v in fields.items() if v not in (None, "", "—")
                    )
                    st.html(f'<div class="out-card"><div class="out-title">Extracted Profile</div>{rows}</div>')

                    if assump:
                        tags = "".join(
                            f'<span class="assumption-tag">⚠ Inferred: {k.replace("_"," ").title()}</span>'
                            for k in assump
                        )
                        st.html(f'<div style="margin:8px 0;">{tags}</div>')

                elif agent == "Retrieval":
                    if evid:
                        ev_rows = "".join(
                            f'<div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid #EAE6DF;">'
                            f'<span style="font-size:12px;color:#2A2A25;">{ev.get("source","Unknown")}</span>'
                            f'<span class="ev-source">Relevance: {float(ev.get("score", ev.get("original_score", 0))):.2f}</span>'
                            f'</div>'
                            for ev in evid
                        )
                        st.html(f'<div class="out-card"><div class="out-title">Retrieved Chunks</div>{ev_rows}</div>')
                    else:
                        st.html('<div class="out-card"><div class="out-title">Retrieved Chunks</div><div style="font-size:12px;color:#8A8880;font-style:italic;">No chunks retrieved.</div></div>')

                elif agent == "Reasoning":
                    p   = float(rec.get("propensity", 0.0))
                    cv  = float(rec.get("context", 0.0))
                    v   = float(rec.get("value", 0.0))
                    pri = float(rec.get("priority", p * cv * v * 10))
                    st.html(f"""
                    <div class="out-card">
                      <div class="out-title">PCVL Scores</div>
                      <div style="display:flex;flex-wrap:wrap;gap:8px;">
                        <span class="pill-score"><span style="color:#8A8880;">Propensity</span><strong style="color:#1A3D1A;">{p:.2f}</strong></span>
                        <span class="pill-score"><span style="color:#8A8880;">Context</span><strong style="color:#1A4060;">{cv:.2f}</strong></span>
                        <span class="pill-score"><span style="color:#8A8880;">Value</span><strong style="color:#5A3080;">{v:.2f}</strong></span>
                        <span style="background:#E8F0E8;border:1px solid #A8C4A8;padding:6px 12px;border-radius:8px;font-size:12px;display:inline-flex;gap:6px;">
                          <span style="color:#1A3D1A;">Priority</span><strong style="color:#1A3D1A;">{pri:.2f}</strong>
                        </span>
                      </div>
                    </div>
                    """)

                elif agent == "Explainability":
                    st.html('<div class="out-card"><div class="out-title">Rationale Draft</div>')
                    st.write(expl)   # ← escaped
                    st.html('</div>')

                elif agent == "HITL Gate":
                    if conf < 0.5:
                        st.warning("⚠️ **Execution blocked.** Confidence below 0.50. Correct flagged assumptions first.")
                    else:
                        st.info("⏸️ **Execution paused.** Awaiting CSM decision.")

                # ── Assumption editor — only for Ingestion ─────────────────
                if agent == "Ingestion" and assump and st.session_state.stage in ("review", "edited"):
                    edit_key = "open_Ingestion"
                    if edit_key not in st.session_state.node_edits:
                        st.session_state.node_edits[edit_key] = False

                    btn_lbl = "▼ Correct inferred assumptions" if not st.session_state.node_edits[edit_key] else "▲ Close"
                    if st.button(btn_lbl, key="toggle_ingestion"):
                        st.session_state.node_edits[edit_key] = not st.session_state.node_edits[edit_key]
                        st.rerun()

                    if st.session_state.node_edits[edit_key]:
                        st.html('<div class="assume-box"><div class="assume-box-title">✏ Correct Inferred Assumptions</div></div>')

                        edited_vals = {}
                        for field_name, reason in assump.items():
                            display = field_name.replace("_", " ").title()
                            st.markdown(f"**{display}**")
                            st.caption(str(reason))
                            fl = field_name.lower()
                            if "segment" in fl:
                                edited_vals[field_name] = st.selectbox(display, ["Enterprise","Mid-Market","SMB"], key=f"ed_{field_name}", label_visibility="collapsed")
                            elif "contract" in fl:
                                edited_vals[field_name] = st.selectbox(display, ["Annual","Monthly","Multi-year"], key=f"ed_{field_name}", label_visibility="collapsed")
                            elif "churn" in fl:
                                edited_vals[field_name] = st.radio(display, ["High","Medium","Low"], horizontal=True, key=f"ed_{field_name}", label_visibility="collapsed")
                            elif "health" in fl:
                                edited_vals[field_name] = st.slider(display, 0, 100, int(profile.get("health_score", 50)), key=f"ed_{field_name}", label_visibility="collapsed")
                            else:
                                edited_vals[field_name] = st.text_input(display, value=str(profile.get(field_name, "")), key=f"ed_{field_name}", label_visibility="collapsed")
                            st.write("")

                        cs, cc, _ = st.columns([3, 2, 4])
                        with cs:
                            if st.button("🔄 Re-evaluate", type="primary", key="submit_ingestion"):
                                st.session_state.original_rec = copy.deepcopy(rec)
                                with st.spinner("Re-routing via Reasoning → Explainability…"):
                                    try:
                                        result = api_resume(tid, "edit", edited_vals)
                                        updated = dict(st.session_state.api_data)
                                        updated["customer_profile"] = result.get("customer_profile", profile)
                                        updated["assumptions"]      = result.get("assumptions", {})
                                        updated["explanation"]      = result.get("explanation", expl)
                                        updated["plan_trace"]       = result.get("plan_trace", trace)
                                        updated["recommendation"]   = result.get("corrected_recommendation", rec)
                                        st.session_state.api_data = updated
                                        st.session_state.node_edits[edit_key] = False
                                        st.session_state.stage = "edited"
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Resume error: {e}")
                        with cc:
                            if st.button("Cancel", key="cancel_ingestion"):
                                st.session_state.node_edits[edit_key] = False
                                st.rerun()

            st.html('<hr style="border:none;border-top:1px solid #D4CFC6;margin:20px 0;">')

        # Before/After after edit
        if st.session_state.stage == "edited" and st.session_state.original_rec:
            orig  = st.session_state.original_rec
            p_new = float(rec.get("propensity",0)) * float(rec.get("context",0)) * float(rec.get("value",0)) * 10
            p_old = float(orig.get("priority", float(orig.get("propensity",0)) * float(orig.get("context",0)) * float(orig.get("value",0)) * 10))
            st.html('<div class="eyebrow">Edit Result</div>')
            st.html('<div style="font-family:\'EB Garamond\',serif;font-size:22px;font-weight:600;color:#0F0F0E;margin-bottom:12px;">Before vs After</div>')
            ca, cb = st.columns(2, gap="medium")
            with ca:
                st.html(f'<div class="cmp-before"><div class="cmp-label" style="color:#C0392B;">Before Edit</div><div class="cmp-action" style="color:#C0392B;">{orig.get("action","—")}</div><div style="font-size:12px;color:#6B6B66;margin-top:8px;line-height:1.8;">Confidence <strong style="color:#C0392B">{float(orig.get("confidence",0)):.2f}</strong><br>Priority <strong style="color:#C0392B">{p_old:.2f}</strong></div></div>')
            with cb:
                st.html(f'<div class="cmp-after"><div class="cmp-label" style="color:#1A3D1A;">After Edit</div><div class="cmp-action" style="color:#1A3D1A;">{rec.get("action","—")}</div><div style="font-size:12px;color:#6B6B66;margin-top:8px;line-height:1.8;">Confidence <strong style="color:#1A3D1A">{conf:.2f}</strong><br>Priority <strong style="color:#1A3D1A">{p_new:.2f}</strong></div></div>')

    # ── RIGHT: Recommendation Card ──────────────────────────────────────────
    with right:
        p   = float(rec.get("propensity", 0.0))
        cv  = float(rec.get("context", 0.0))
        v   = float(rec.get("value", 0.0))
        pri = float(rec.get("priority", p * cv * v * 10))
        mc  = "#1A3D1A" if conf >= 0.5 else "#D4A017"
        pct = conf * 100

        if conf >= 0.5:
            badge_html = f'<span class="badge-high"><span class="badge-dot" style="background:#1A3D1A;"></span>High Confidence · {conf:.2f}</span>'
        else:
            badge_html = f'<span class="badge-low"><span class="badge-dot" style="background:#D4A017;"></span>Low Confidence · {conf:.2f} — Human Review Required</span>'

        st.html(f"""
        <div class="rec-card">
          <div class="eyebrow">Recommended Action</div>
          <div class="rec-action">{rec.get("action","No recommendation generated")}</div>
          {badge_html}
          <div class="conf-row"><span>CONFIDENCE</span><span>{pct:.0f}%</span></div>
          <div class="conf-track"><div class="conf-fill" style="width:{pct}%;background:{mc};"></div></div>
        </div>
        """)

        st.html('<div class="eyebrow">PCVL Scoring</div>')
        st.html(f"""
        <div class="pcvl-grid">
          <div class="pcvl-tile"><div class="pcvl-label">Propensity</div><div class="pcvl-value" style="color:#1A3D1A;">{p:.2f}</div><div class="pcvl-sub">likelihood</div></div>
          <div class="pcvl-tile"><div class="pcvl-label">Context</div><div class="pcvl-value" style="color:#1A4060;">{cv:.2f}</div><div class="pcvl-sub">relevance</div></div>
          <div class="pcvl-tile"><div class="pcvl-label">Value</div><div class="pcvl-value" style="color:#5A3080;">{v:.2f}</div><div class="pcvl-sub">account LTV</div></div>
          <div class="pcvl-tile pcvl-tile-hi"><div class="pcvl-label">Priority</div><div class="pcvl-value" style="color:#0F0F0E;">{pri:.2f}</div><div class="pcvl-sub">P×C×V×L</div></div>
        </div>
        """)

        # Explanation — st.write inside a container so text is safe
        st.html('<div class="expl-quote">')
        st.write(expl)
        st.html('</div>')

        levers = rec.get("levers")
        if levers:
            st.html(f'<div class="lever-pill">⚙ {levers}</div>')

        st.html('<hr style="border:none;border-top:1px solid #D4CFC6;margin:24px 0;">')

        st.html('<div class="eyebrow">Retrieved Evidence</div>')
        if evid:
            for ev in evid:
                score  = float(ev.get("score", ev.get("original_score", 0.0)))
                source = ev.get("source", "Unknown")
                text   = ev.get("text", "")
                pct_ev = int(min(score, 1.0) * 100)
                st.html(f'<div class="ev-wrap"><div class="ev-row"><span class="ev-source">{source}</span><span class="ev-score">{score:.2f}</span></div><div class="ev-bar-track"><div class="ev-bar-fill" style="width:{pct_ev}%;"></div></div></div>')
                # Render text safely
                st.write(f'*"{text}"*')
        else:
            st.html('<div style="font-size:12px;color:#8A8880;font-style:italic;">No evidence chunks retrieved.</div>')

        st.html('<hr style="border:none;border-top:1px solid #D4CFC6;margin:24px 0;">')

        # HITL Gate buttons
        if st.session_state.stage in ("review", "edited"):
            st.html('<div class="eyebrow" style="margin-bottom:10px;">CSM Decision — HITL Gate</div>')
            b1, b2, b3 = st.columns(3, gap="small")
            with b1:
                if st.button("✅  Approve", type="primary", use_container_width=True):
                    with st.spinner("Submitting…"):
                        try:    api_resume(tid, "approve")
                        except: pass
                    st.session_state.stage = "approved"
                    st.rerun()
            with b2:
                if st.button("✏️  Edit", use_container_width=True):
                    st.session_state.node_edits["open_Ingestion"] = True
                    st.rerun()
            with b3:
                if st.button("❌  Reject", use_container_width=True):
                    with st.spinner("Submitting…"):
                        try:    api_resume(tid, "reject")
                        except: pass
                    st.session_state.stage = "rejected"
                    st.rerun()

        if st.session_state.stage == "approved":
            st.html(f"""
            <div class="banner-ok">
              <div style="font-size:26px;">🎉</div>
              <div>
                <div class="banner-title" style="color:#1A3D1A;">Action Approved</div>
                <div class="banner-sub">Outbound trigger fired: <em>{rec.get("action","—")}</em>.<br>Decision logged to memory.</div>
              </div>
            </div>
            """)
            st.write("")
            if st.button("→  New case"):
                reset(); st.rerun()

        elif st.session_state.stage == "rejected":
            st.html(f"""
            <div class="banner-no">
              <div style="font-size:26px;">🚫</div>
              <div>
                <div class="banner-title" style="color:#B03020;">Action Rejected</div>
                <div class="banner-sub">CSM override recorded. Will inform future cases.</div>
              </div>
            </div>
            """)
            st.write("")
            if st.button("→  New case"):
                reset(); st.rerun()
