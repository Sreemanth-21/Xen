import os
import math
from datetime import datetime, timezone
from typing import Any, List
from agents.graph import PulseState

# Mock Database of Knowledge Base Playbooks/Articles
MOCK_KB = [
    {
        "text": "Playbook: Seat Contraction and License Utilization Recovery. When license utilization falls below 70%, schedule an expansion review, offer free admin training, and align on customer goals. Value: High priority expansion/retention tactic.",
        "source": "kb_seat_contraction_v2.md",
        "timestamp": "2026-06-26T12:00:00Z"  # 1 day ago
    },
    {
        "text": "Playbook: Churn Prevention for Payment Failures. If a customer experience credit card expiry or billing issues, notify billing contact, grant 14-day grace period, and send automated warning alerts.",
        "source": "kb_billing_failure.md",
        "timestamp": "2026-06-15T09:00:00Z"  # 12 days ago
    },
    {
        "text": "Playbook: Annual Contract Renewal Guide. Engage enterprise customers 90 days before renewal. Present ROI dashboard, usage trends, and discuss multi-year expansion options.",
        "source": "kb_enterprise_renewal.md",
        "timestamp": "2026-03-01T10:00:00Z"  # ~118 days ago (old playbook)
    },
    {
        "text": "Playbook: Inactive Admin/Key Sponsor Churn Rescue. When the main admin or executive sponsor leaves the company, immediately engage the executive buyer, identify new admin candidates, and conduct a new onboarding session.",
        "source": "kb_sponsor_change.md",
        "timestamp": "2026-06-25T15:30:00Z"  # 2 days ago
    },
    {
        "text": "Playbook: High Churn Risk Mitigations. Implement executive check-ins, custom CSM support, and customer success reviews for high-risk accounts.",
        "source": "kb_high_risk_remedy.md",
        "timestamp": "2025-12-01T08:00:00Z"  # Over 200 days ago
    }
]

def retrieve(query: str, top_k: int = 3) -> List[dict]:
    """
    Teammate B will replace this function with the actual interface to Chroma DB.
    We stub it here with a keyword search over the mock database.
    """
    print(f"Retrieving from Chroma with query: '{query}' and top_k: {top_k}")
    query_words = set(query.lower().split())
    results = []
    
    for item in MOCK_KB:
        text = item["text"].lower()
        # Calculate a simple Jaccard-like overlap score for stub purposes
        text_words = set(text.split())
        overlap = len(query_words.intersection(text_words))
        score = float(overlap) / float(max(len(query_words), 1))
        
        # Add basic base score plus mock similarity
        base_score = 0.3 + (score * 0.7)
        results.append({
            "text": item["text"],
            "source": item["source"],
            "score": base_score,
            "timestamp": item["timestamp"]
        })
        
    # Sort by initial similarity score
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:top_k]

def retrieval_node(state: PulseState) -> dict[str, Any]:
    print("--- RUNNING KNOWLEDGE RETRIEVAL AGENT ---")
    raw_input = state.get("raw_input", "")
    customer_profile = state.get("customer_profile", {})
    plan_trace = state.get("plan_trace", [])
    
    # Check if we received a broadening signal from the planner
    has_broaden_signal = False
    if plan_trace:
        last_log = plan_trace[-1]
        if "broadening retrieval query" in last_log.lower():
            has_broaden_signal = True
            
    # Formulate search query
    if has_broaden_signal:
        # A broader query to get general churn and expansion policies
        search_query = "customer success playbooks retention expansion churn contraction renewal"
        top_k = 4
    else:
        # Generate targeted query from raw input and customer profile
        company = customer_profile.get("company_name", "")
        churn_risk = customer_profile.get("churn_risk", "Medium")
        # Extract keywords or issues from raw input
        search_query = f"{churn_risk} churn risk {raw_input[:100]}"
        top_k = 3
        
    # Call the retrieval interface
    raw_results = retrieve(search_query, top_k=top_k)
    
    # Apply recency weighting post-retrieval (Time-Decay)
    # reference time = 2026-06-27T13:47:31Z (as provided in metadata)
    ref_time = datetime(2026, 6, 27, 13, 47, 31, tzinfo=timezone.utc)
    
    decayed_results = []
    for chunk in raw_results:
        timestamp_str = chunk.get("timestamp")
        orig_score = chunk["score"]
        
        try:
            chunk_time = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            age_days = (ref_time - chunk_time).days
            if age_days < 0:
                age_days = 0
        except Exception:
            age_days = 30  # fallback age of 30 days if timestamp parsing fails
            
        # Time-decay multiplier formula: exp(-lambda * age_days)
        # lambda = 0.02 means 10 days = ~0.82 multiplier, 100 days = ~0.13 multiplier
        decay_factor = math.exp(-0.02 * age_days)
        decayed_score = orig_score * decay_factor
        
        decayed_chunk = {
            "text": chunk["text"],
            "source": chunk["source"],
            "score": round(decayed_score, 4),
            "original_score": round(orig_score, 4),
            "timestamp": timestamp_str,
            "age_days": age_days,
            "decay_factor": round(decay_factor, 4)
        }
        decayed_results.append(decayed_chunk)
        
    # Re-rank based on decayed scores
    reranked_results = sorted(decayed_results, key=lambda x: x["score"], reverse=True)
    
    print(f"Retrieved {len(reranked_results)} items. Best decayed score: {reranked_results[0]['score'] if reranked_results else 0.0}")
    
    return {
        "retrieved_evidence": reranked_results
    }
