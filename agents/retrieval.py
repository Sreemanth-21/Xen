import os
import math
from datetime import datetime, timezone
from typing import Any, List
import chromadb
from agents.graph import PulseState

def retrieval_node(state: PulseState) -> dict[str, Any]:
    print("--- RUNNING KNOWLEDGE RETRIEVAL AGENT ---")
    
    # 1. Read customer profile from state
    profile = state.get("customer_profile", {})
    company_name = profile.get("company_name", "Unknown Company")
    churn_risk = profile.get("churn_risk", "Medium")
    segment = profile.get("segment", "Mid-Market")
    contract_type = profile.get("contract_type", "Annual")
    
    # 2. Build query string
    query_str = f"{segment} customer, {churn_risk} churn risk, {contract_type} contract"
    print(f"Retrieving from Chroma with query: '{query_str}'")
    
    # 3. Resolve absolute path to Chroma DB store
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    chroma_db_path = os.path.join(workspace_root, "chroma_store")
    
    retrieved_docs = []
    
    try:
        client = chromadb.PersistentClient(path=chroma_db_path)
        
        # Check collections to avoid errors if database is not set up
        collections = client.list_collections()
        col_names = [col.name for col in collections]
        
        if "knowledge_base" not in col_names:
            print("Warning: 'knowledge_base' collection does not exist in Chroma DB.")
        else:
            collection = client.get_collection(name="knowledge_base")
            count = collection.count()
            
            if count == 0:
                print("Warning: 'knowledge_base' collection is empty.")
            else:
                # Query for top 6 similar documents
                n_results = min(6, count)
                results = collection.query(
                    query_texts=[query_str],
                    n_results=n_results
                )
                
                # Parse query results
                if results and "documents" in results and results["documents"]:
                    documents = results["documents"][0]
                    metadatas = results["metadatas"][0] if "metadatas" in results and results["metadatas"] else []
                    distances = results["distances"][0] if "distances" in results and results["distances"] else []
                    ids = results["ids"][0] if "ids" in results and results["ids"] else []
                    
                    for i in range(len(documents)):
                        text = documents[i]
                        meta = metadatas[i] if i < len(metadatas) else {}
                        dist = distances[i] if i < len(distances) else 0.0
                        doc_id = ids[i] if i < len(ids) else f"kb_{i}"
                        
                        # Convert L2 distance to similarity score
                        similarity_score = 1.0 / (1.0 + dist)
                        timestamp_str = meta.get("timestamp", "")
                        
                        retrieved_docs.append({
                            "text": text,
                            "source": doc_id,
                            "similarity_score": similarity_score,
                            "timestamp": timestamp_str
                        })
    except Exception as e:
        print(f"Warning: Failed to query Chroma DB. Error: {e}")
        
    print(f"Found {len(retrieved_docs)} raw matching documents in Chroma.")
    
    # 4. Apply time-decay re-ranking
    # Reference time is the current time in UTC
    ref_time = datetime.now(timezone.utc)
    
    decayed_results = []
    for doc in retrieved_docs:
        timestamp_str = doc["timestamp"]
        similarity_score = doc["similarity_score"]
        
        age_in_days = 30  # default fallback if timestamp parsing fails
        if timestamp_str:
            try:
                # Replace 'Z' with UTC offset for python compatibility
                doc_time = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                age_in_days = (ref_time - doc_time).days
                if age_in_days < 0:
                    age_in_days = 0
            except Exception as pe:
                print(f"Error parsing timestamp '{timestamp_str}': {pe}")
                
        # Time-decay re-ranking score formula: decayed_score = similarity_score * exp(-0.01 * age_in_days)
        decay_factor = math.exp(-0.01 * age_in_days)
        decayed_score = similarity_score * decay_factor
        
        decayed_results.append({
            "text": doc["text"],
            "source": doc["source"],
            "score": round(decayed_score, 4)
        })
        
    # Sort by decayed score descending
    decayed_results.sort(key=lambda x: x["score"], reverse=True)
    
    # Keep top 4
    final_evidence = decayed_results[:4]
    
    if len(final_evidence) < 4:
        print(f"Warning: Only {len(final_evidence)} evidence documents retrieved (fewer than the requested 4).")
        
    print(f"Retrieved {len(final_evidence)} evidence documents after time-decay re-ranking.")
    
    return {
        "retrieved_evidence": final_evidence
    }

if __name__ == "__main__":
    # Test block with a sample customer profile
    fake_state = {
        "customer_profile": {
            "company_name": "ApexLogistics",
            "contract_value": 45000,
            "contract_type": "Annual",
            "health_score": 35,
            "segment": "Mid-Market",
            "churn_risk": "High",
            "license_count": 100,
            "active_users": 38
        }
    }
    
    print("=== TESTING RETRIEVAL NODE STANDALONE ===")
    result = retrieval_node(fake_state)
    print("\nResult:")
    import pprint
    pprint.pprint(result)
