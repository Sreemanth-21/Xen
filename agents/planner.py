from typing import Any
from agents.graph import PulseState

def route_from_planner(state: PulseState) -> str:
    status = state.get("status", "pending")
    customer_profile = state.get("customer_profile", {})
    retrieved_evidence = state.get("retrieved_evidence", [])
    recommendation = state.get("recommendation", {})
    explanation = state.get("explanation", "")
    plan_trace = state.get("plan_trace", [])
    
    # 1. Edit flow routing
    if status == "edited":
        # Check if explainability was just run in the edit flow
        if plan_trace and "Planner (Edit): Routed to Explainability" in plan_trace[-1]:
            return "execute"
        return "explainability"

    # 2. Normal flow routing
    if not customer_profile or not customer_profile.get("company_name"):
        return "ingestion"

    if not retrieved_evidence:
        return "retrieval"

    # Dynamic check: What if evidence is weak?
    has_broadened = any("broadening retrieval query" in t for t in plan_trace)
    if retrieved_evidence and not has_broadened:
        scores = [chunk.get("score", 0.0) for chunk in retrieved_evidence]
        avg_score = sum(scores) / len(scores) if scores else 0.0
        if avg_score < 0.4 or len(retrieved_evidence) <= 1:
            return "retrieval"

    if not recommendation or not recommendation.get("action"):
        return "reasoning"

    if not explanation:
        return "explainability"

    return "execute"

def planner_node(state: PulseState) -> dict[str, Any]:
    print("--- RUNNING PLANNER AGENT ---")
    plan_trace = list(state.get("plan_trace", []))
    status = state.get("status", "pending")
    customer_profile = state.get("customer_profile", {})
    retrieved_evidence = state.get("retrieved_evidence", [])
    recommendation = state.get("recommendation", {})
    explanation = state.get("explanation", "")
    
    # First, evaluate what the next node will be to write the correct log
    next_node = route_from_planner(state)
    
    if status == "edited":
        if next_node == "execute":
            msg = "Planner (Edit): Routing to Execute node because edited recommendation and explanation are complete."
        else:
            msg = "Planner (Edit): Routed to Explainability Agent because corrected recommendation was generated and needs a revised explanation."
    else:
        if next_node == "ingestion":
            msg = "Planner: Routing to Ingestion Agent because customer profile is empty. We need to parse raw input."
        elif next_node == "retrieval":
            # Distinguish between first retrieval and broadening
            has_broadened = any("broadening retrieval query" in t for t in plan_trace)
            if retrieved_evidence and not has_broadened:
                scores = [chunk.get("score", 0.0) for chunk in retrieved_evidence]
                avg_score = sum(scores) / len(scores) if scores else 0.0
                msg = f"Planner: Evidence weak ({len(retrieved_evidence)} chunks, avg score {avg_score:.2f}) — broadening retrieval query."
            else:
                msg = "Planner: Routing to Retrieval Agent because customer profile is parsed but no knowledge has been retrieved."
        elif next_node == "reasoning":
            msg = "Planner: Routing to Reasoning Agent because customer profile and retrieved evidence are loaded."
        elif next_node == "explainability":
            msg = "Planner: Routing to Explainability Agent because recommendation is generated. We need to write human rationale."
        else:
            msg = "Planner: Routing to Execute node because recommendation and explanation are complete. Pausing for human review."
            
    plan_trace.append(msg)
    return {
        "plan_trace": plan_trace
    }
