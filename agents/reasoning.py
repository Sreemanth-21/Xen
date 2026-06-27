import os
import math
from typing import Any, List
from agents.graph import PulseState

def reasoning_node(state: PulseState) -> dict[str, Any]:
    print("--- RUNNING REASONING & ARBITRATION AGENT ---")
    
    # 1. Read input state variables
    customer_profile = state.get("customer_profile", {})
    retrieved_evidence = state.get("retrieved_evidence", [])
    assumptions = state.get("assumptions", {})
    
    churn_risk = customer_profile.get("churn_risk", "Medium")
    health_score = float(customer_profile.get("health_score", 50.0))
    contract_value = customer_profile.get("contract_value")
    
    # 2. Compute Propensity (0-1)
    # Propensity indicates the customer's likelihood to respond/accept the action.
    # We map the categorical churn_risk to base scores: High=0.85, Medium=0.5, Low=0.2.
    # We then nudge these using the health score as a secondary signal:
    # - For High/Medium churn risk: lower health score boosts churn propensity (worse health).
    # - For Low churn risk (expansion-leaning): higher health score boosts expansion propensity.
    if churn_risk in ["High", "Medium"]:
        base_propensity = 0.85 if churn_risk == "High" else 0.5
        # Nudge: health score below 50 boosts propensity; above 50 lowers it. Max nudge is +/- 0.15.
        nudge = (50.0 - health_score) / 50.0 * 0.15
        propensity = max(0.0, min(1.0, base_propensity + nudge))
    else:  # Low
        # Expansion case: high health score blends to higher propensity
        base_propensity = 0.2
        propensity = 0.6 * base_propensity + 0.4 * (health_score / 100.0)
        
    # 3. Compute Context (0-1)
    # The average score of time-decayed retrieved playbooks.
    # Fallback to 0.1 if evidence is empty to prevent zero-out issues.
    if retrieved_evidence:
        scores = [float(e.get("score", 0.0)) for e in retrieved_evidence]
        context = sum(scores) / len(scores)
    else:
        context = 0.1
        
    # 4. Compute Value (0-1)
    # Normalized against a ceiling of $200,000, capped at 1.0.
    # Fallback to 0.3 if contract_value is null.
    if contract_value is None:
        value = 0.3
    else:
        value = min(1.0, float(contract_value) / 200000.0)
        
    # 5. Compute Levers (0-1)
    # Presence of a usable playbook (contains substring "playbook" in source/text case-insensitive).
    has_playbook = False
    for e in retrieved_evidence:
        text = e.get("text", "").lower()
        source = e.get("source", "").lower()
        if "playbook" in text or "playbook" in source:
            has_playbook = True
            break
    levers = 0.8 if has_playbook else 0.4
    
    # 6. Compute Priority Score (P * C * V * L)
    priority = propensity * context * value * levers
    
    # 7. Select Action
    # Map churn_risk + health_score signals to meaningful CSM actions
    active_users   = customer_profile.get("active_users")
    license_count  = customer_profile.get("license_count")

    # Compute utilisation ratio if both values are available
    if active_users and license_count and int(license_count) > 0:
        utilisation = float(active_users) / float(license_count)
    else:
        utilisation = None

    if churn_risk == "High":
        action = "Schedule retention call"
    elif churn_risk == "Low" and health_score >= 80:
        if utilisation is not None and utilisation >= 0.90:
            action = "Propose upsell"
        else:
            action = "Propose upsell"
    elif churn_risk == "Medium":
        # Medium risk — differentiate by adoption signal
        if utilisation is not None and utilisation < 0.60:
            action = "Launch adoption recovery playbook"
        elif health_score < 50:
            action = "Schedule check-in and health review"
        else:
            action = "Send proactive success resources"
    else:
        # Low churn but health not strong enough for upsell
        action = "Send proactive success resources"
        
    # 8. Compute Confidence Score (0-1)
    # Base confidence scales with context strength
    base_confidence = 0.4 + 0.6 * context

    # Deductions — only penalise fields that materially affect the action decision
    deduction = 0.0

    # Contract type inferred — affects renewal/discount logic
    if "contract_type" in assumptions:
        deduction += 0.10

    # Health score inferred — affects propensity nudge
    if "health_score" in assumptions:
        deduction += 0.10

    # Each additional inferred field adds a small penalty
    for key in assumptions:
        if key not in ["contract_type", "health_score"]:
            deduction += 0.05

    # Thin evidence penalty — but only if truly empty
    if not retrieved_evidence:
        deduction += 0.20
    elif context <= 0.10:
        deduction += 0.10

    # Null contract value — minor penalty, doesn't affect action selection
    if contract_value is None:
        deduction += 0.05

    # Floor at 0.25 so real LLM output is never presented as completely worthless
    confidence = max(0.25, min(1.0, base_confidence - deduction))
    
    print(f"Computed reasoning - Priority: {priority:.4f}, Confidence: {confidence:.4f}, Action: '{action}'")
    
    # 9. Return structured recommendation dictionary
    return {
        "recommendation": {
            "action": action,
            "propensity": round(propensity, 4),
            "context": round(context, 4),
            "value": round(value, 4),
            "levers": round(levers, 4),
            "priority": round(priority, 4),
            "confidence": round(confidence, 4)
        }
    }

if __name__ == "__main__":
    # Test blocks representing different scenarios
    state_churn = {
        "customer_profile": {
            "company_name": "ApexLogistics",
            "contract_value": 45000,
            "contract_type": "Annual",
            "health_score": 35,
            "segment": "Mid-Market",
            "churn_risk": "High",
            "license_count": 100,
            "active_users": 38
        },
        "retrieved_evidence": [
            {"text": "Playbook: Seat Contraction Recovery...", "source": "kb_001", "score": 0.3842},
            {"text": "Playbook: Churn Prevention...", "source": "kb_002", "score": 0.2405}
        ],
        "assumptions": {}
    }
    
    state_expansion = {
        "customer_profile": {
            "company_name": "CloudScale Solutions",
            "contract_value": 60000,
            "contract_type": "Annual",
            "health_score": 95,
            "segment": "Mid-Market",
            "churn_risk": "Low",
            "license_count": 100,
            "active_users": 98
        },
        "retrieved_evidence": [
            {"text": "Playbook: Expansion Trigger...", "source": "kb_006", "score": 0.521},
            {"text": "Playbook: Upsell to Enterprise...", "source": "kb_007", "score": 0.381}
        ],
        "assumptions": {}
    }
    
    state_ambiguous = {
        "customer_profile": {
            "company_name": "NovaRetail",
            "contract_value": 36000,
            "contract_type": "Annual",
            "health_score": 55,
            "segment": "Mid-Market",
            "churn_risk": "Medium",
            "license_count": 80,
            "active_users": 42
        },
        "retrieved_evidence": [],  # no strong evidence
        "assumptions": {
            "contract_type": "Inferred Monthly contract based on billing notes."
        }
    }
    
    print("=== TESTING REASONING NODE STANDALONE ===")
    
    print("\n--- CHURN CASE ---")
    rec_churn = reasoning_node(state_churn)
    import pprint
    pprint.pprint(rec_churn)
    
    print("\n--- EXPANSION CASE ---")
    rec_exp = reasoning_node(state_expansion)
    pprint.pprint(rec_exp)
    
    print("\n--- AMBIGUOUS CASE ---")
    rec_amb = reasoning_node(state_ambiguous)
    pprint.pprint(rec_amb)
