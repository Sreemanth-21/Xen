import os
from datetime import datetime, timezone
from typing import Any, List
import chromadb
from agents.graph import PulseState

def memory_update_node(state: PulseState) -> dict[str, Any]:
    print("--- RUNNING MEMORY UPDATE AGENT ---")
    
    # 1. Read input state variables
    case_id = state.get("case_id", "unknown_case")
    customer_profile = state.get("customer_profile", {})
    recommendation = state.get("recommendation", {})
    status = state.get("status", "executed")
    
    company_name = customer_profile.get("company_name", "Unknown Company")
    churn_risk = customer_profile.get("churn_risk", "Unknown")
    segment = customer_profile.get("segment", "Unknown")
    action = recommendation.get("action", "No action")
    priority = float(recommendation.get("priority", 0.0))
    confidence = float(recommendation.get("confidence", 0.0))
    
    # 2. Build natural-language summary string — must include segment and churn_risk
    # so that find_similar_past_cases() queries (which use those fields) can match against
    # embedded text in this record during similarity search.
    summary_text = (
        f"For {company_name}, a {segment} customer with {churn_risk} churn risk, "
        f"the recommended action '{action}' was {status} by human reviewer. "
        f"Priority score: {priority:.4f}, confidence score: {confidence:.4f}."
    )
    
    # 3. Resolve absolute path to Chroma DB store
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    chroma_db_path = os.path.join(workspace_root, "chroma_store")
    
    print(f"Connecting to ChromaDB at: {chroma_db_path}")
    client = chromadb.PersistentClient(path=chroma_db_path)
    collection = client.get_or_create_collection(name="interaction_history")
    
    # 4. Prepare metadata and perform upsert using case_id as ID to overwrite duplicates
    metadata = {
        "case_id": case_id,
        "action": action,
        "decision": status,
        "priority": priority,
        "confidence": confidence,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    print(f"Writing history record for case: {case_id}")
    collection.upsert(
        ids=[case_id],
        documents=[summary_text],
        metadatas=[metadata]
    )
    
    print(f"Memory update confirmed: '{summary_text}' successfully saved.")
    
    # Return executed status to signal workflow termination
    return {
        "status": "executed"
    }

def find_similar_past_cases(customer_profile: dict, k: int = 3) -> List[dict]:
    # 1. Resolve absolute path to Chroma DB store
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    chroma_db_path = os.path.join(workspace_root, "chroma_store")
    
    client = chromadb.PersistentClient(path=chroma_db_path)
    
    collections = client.list_collections()
    col_names = [col.name for col in collections]
    
    if "interaction_history" not in col_names:
        print("Warning: 'interaction_history' collection does not exist in Chroma DB.")
        return []
        
    collection = client.get_collection(name="interaction_history")
    count = collection.count()
    
    if count == 0:
        print("Warning: 'interaction_history' collection is empty.")
        return []
        
    # 2. Build short query string from customer_profile
    company_name = customer_profile.get("company_name", "Unknown Company")
    churn_risk = customer_profile.get("churn_risk", "Medium")
    segment = customer_profile.get("segment", "Mid-Market")
    
    query_str = f"{company_name} - {segment} customer, {churn_risk} churn risk"
    
    # 3. Query interaction_history
    n_results = min(k, count)
    results = collection.query(
        query_texts=[query_str],
        n_results=n_results
    )
    
    past_cases = []
    if results and "documents" in results and results["documents"]:
        documents = results["documents"][0]
        metadatas = results["metadatas"][0] if "metadatas" in results and results["metadatas"] else []
        
        for i in range(len(documents)):
            text = documents[i]
            meta = metadatas[i] if i < len(metadatas) else {}
            
            past_cases.append({
                "case_id": meta.get("case_id"),
                "action": meta.get("action"),
                "decision": meta.get("decision"),
                "priority": meta.get("priority"),
                "confidence": meta.get("confidence"),
                "timestamp": meta.get("timestamp"),
                "summary_text": text
            })
            
    return past_cases

if __name__ == "__main__":
    print("=== TESTING MEMORY UPDATE STANDALONE (TEST DATA) ===")
    
    # 1. Clear previous test collection if we want a clean execution, or just overwrite
    # Build fake completed cases
    fake_state_1 = {
        "case_id": "test_case_001_churn",
        "customer_profile": {
            "company_name": "ApexLogistics",
            "churn_risk": "High",
            "segment": "Mid-Market"
        },
        "recommendation": {
            "action": "Schedule retention call",
            "priority": 0.85,
            "confidence": 0.90
        },
        "status": "approved"
    }
    
    fake_state_2 = {
        "case_id": "test_case_002_expansion",
        "customer_profile": {
            "company_name": "CloudScale Solutions",
            "churn_risk": "Low",
            "segment": "Enterprise"
        },
        "recommendation": {
            "action": "Propose upsell",
            "priority": 0.72,
            "confidence": 0.95
        },
        "status": "approved"
    }
    
    fake_state_3 = {
        "case_id": "test_case_003_rejected",
        "customer_profile": {
            "company_name": "NovaRetail",
            "churn_risk": "Medium",
            "segment": "SMB"
        },
        "recommendation": {
            "action": "Trigger churn intervention playbook",
            "priority": 0.40,
            "confidence": 0.35
        },
        "status": "rejected"
    }
    
    # Run states through node
    print("\n[TEST DATA] Running fake completed cases through memory_update_node...")
    memory_update_node(fake_state_1)
    memory_update_node(fake_state_2)
    memory_update_node(fake_state_3)
    
    # 2. Run retrieval using find_similar_past_cases
    test_query_profile = {
        "company_name": "ApexLogistics",
        "churn_risk": "High",
        "segment": "Mid-Market"
    }
    
    print(f"\n[TEST DATA] Querying similar past cases for profile: {test_query_profile}")
    matches = find_similar_past_cases(test_query_profile, k=2)
    
    print("\n[TEST DATA] Retrieved Matches:")
    import pprint
    pprint.pprint(matches)
