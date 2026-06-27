"""
Memory Update Agent — writes the CSM's Approve/Edit/Reject decision
to the interaction_history Chroma collection so the Memory Diff panel
can surface relevant past decisions on future cases.
"""

import os
import uuid
from datetime import datetime, timezone
from typing import Any
from agents.graph import PulseState


def memory_update_node(state: PulseState) -> dict[str, Any]:
    print("--- RUNNING MEMORY UPDATE AGENT ---")

    human_decision  = state.get("human_decision") or {}
    recommendation  = state.get("recommendation") or {}
    customer_profile = state.get("customer_profile") or {}

    decision        = human_decision.get("decision", "unknown")
    action          = recommendation.get("action", "unknown")
    company_name    = customer_profile.get("company_name", "Unknown")
    confidence      = recommendation.get("confidence", 0.0)
    priority        = recommendation.get("priority", 0.0)
    timestamp       = datetime.now(timezone.utc).isoformat()
    doc_id          = f"interaction-{uuid.uuid4().hex[:10]}"

    # Human-readable outcome mapping
    outcome_map = {
        "approve": "Action executed",
        "reject":  "Action overridden by CSM",
        "edit":    "Assumptions corrected, action re-evaluated",
    }
    outcome = outcome_map.get(decision, "Unknown outcome")

    # Document text for semantic search (used by memory_diff queries)
    document_text = (
        f"Company: {company_name}. "
        f"Recommended action: {action}. "
        f"CSM decision: {decision}. "
        f"Outcome: {outcome}."
    )

    metadata = {
        "company_name":   company_name,
        "action":         action,
        "human_decision": decision,
        "outcome":        outcome,
        "confidence":     str(round(float(confidence), 4)),
        "priority":       str(round(float(priority), 4)),
        "timestamp":      timestamp,
    }

    try:
        import chromadb
        script_dir     = os.path.dirname(os.path.abspath(__file__))
        workspace_root = os.path.dirname(script_dir)
        chroma_db_path = os.path.join(workspace_root, "chroma_store")

        client     = chromadb.PersistentClient(path=chroma_db_path)
        collection = client.get_or_create_collection(name="interaction_history")

        collection.add(
            ids=[doc_id],
            documents=[document_text],
            metadatas=[metadata],
        )
        print(f"Memory Update: Saved interaction '{doc_id}' for '{company_name}' — decision={decision}")
    except Exception as e:
        print(f"Memory Update: Failed to write to Chroma. Error: {e}")

    return {"status": "executed"}
