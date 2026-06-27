import os
import json
import math
from typing import Any, List
from groq import Groq
from dotenv import load_dotenv
from agents.graph import PulseState

# Load environment variables
load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def reasoning_node(state: PulseState) -> dict[str, Any]:
    print("--- RUNNING REASONING & ARBITRATION AGENT ---")
    customer_profile = state.get("customer_profile", {})
    retrieved_evidence = state.get("retrieved_evidence", [])
    raw_input = state.get("raw_input", "")
    
    client = get_groq_client()
    if not client:
        # Fallback Mock in case GROQ_API_KEY is not configured
        print("Mocking Reasoning LLM call due to missing Groq API Key.")
        # Create dummy candidates
        candidates = [
            {
                "action": "Initiate License Utilization Recovery Playbook",
                "propensity": 8.0,
                "context": 9.0,
                "value": 7.5,
                "levers": 8.5,
                "confidence": 0.85,
                "source_file": "kb_seat_contraction_v2.md"
            },
            {
                "action": "Trigger High-risk Executive Check-in",
                "propensity": 7.0,
                "context": 8.0,
                "value": 9.0,
                "levers": 6.0,
                "confidence": 0.80,
                "source_file": "kb_high_risk_remedy.md"
            }
        ]
    else:
        # Construct prompt for LLM to get candidates and scores
        system_prompt = (
            "You are the Reasoning & Arbitration Agent for Xen, a B2B SaaS Customer Success Next Best Action platform.\n"
            "Analyze the customer profile and the retrieved playbook evidence to suggest the best Next Best Actions (between 1 and 3 candidates).\n"
            "For each candidate action, you must output raw scores from 0.0 to 10.0 for four components:\n"
            "1. Propensity: Likelihood of customer accepting or responding to the action.\n"
            "2. Context: Raw relevance of this action given their current profile and CRM notes.\n"
            "3. Value: Impact/revenue value of this action.\n"
            "4. Levers: Ease of execution or feasibility for the CSM.\n"
            "Also specify 'source_file' matching one of the retrieved evidence sources, and 'confidence' (0.0 to 1.0).\n\n"
            "IMPORTANT: Do NOT compute the priority score yourself. The priority score will be computed programmatically in code.\n\n"
            "You must return a JSON object with the following format:\n"
            "{\n"
            "  \"candidates\": [\n"
            "    {\n"
            "      \"action\": \"Action description\",\n"
            "      \"propensity\": number,\n"
            "      \"context\": number,\n"
            "      \"value\": number,\n"
            "      \"levers\": number,\n"
            "      \"confidence\": number,\n"
            "      \"source_file\": \"filename.md\"\n"
            "    }\n"
            "  ]\n"
            "}"
        )
        
        evidence_text = "\n".join([
            f"- File: {c.get('source')} | Text: {c.get('text')}"
            for c in retrieved_evidence
        ])
        
        user_prompt = (
            f"Customer Profile:\n{json.dumps(customer_profile, indent=2)}\n\n"
            f"Raw CRM Note:\n{raw_input}\n\n"
            f"Retrieved Evidence Playbooks:\n{evidence_text}\n"
        )
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            result_text = completion.choices[0].message.content
            data = json.loads(result_text)
            candidates = data.get("candidates", [])
        except Exception as e:
            print(f"Error calling Groq API in Reasoning: {e}")
            raise e

    # Process and compute Priority in code
    processed_candidates = []
    for cand in candidates:
        action_name = cand.get("action", "Unknown Action")
        prop = float(cand.get("propensity", 5.0))
        raw_context = float(cand.get("context", 5.0))
        val = float(cand.get("value", 5.0))
        levs = float(cand.get("levers", 5.0))
        conf = float(cand.get("confidence", 0.5))
        source = cand.get("source_file", "")
        
        # Apply time-decay to Context specifically
        # We find the matching chunk age in retrieved_evidence
        age_days = 30  # default fallback
        for chunk in retrieved_evidence:
            if chunk.get("source") == source:
                age_days = chunk.get("age_days", 30)
                break
                
        # Time-decay factor: exp(-0.02 * age_days)
        context_decay_factor = math.exp(-0.02 * age_days)
        decayed_context = raw_context * context_decay_factor
        
        # Compute Priority = Propensity * Context (decayed) * Value * Levers
        priority = prop * decayed_context * val * levs
        
        processed_candidates.append({
            "action": action_name,
            "propensity": round(prop, 2),
            "context": round(decayed_context, 2),
            "raw_context": round(raw_context, 2),
            "value": round(val, 2),
            "levers": round(levs, 2),
            "priority": round(priority, 2),
            "confidence": round(conf, 2),
            "source_file": source,
            "age_days": age_days,
            "decay_factor": round(context_decay_factor, 4)
        })
        
    # Sort candidates by Priority descending
    ranked_candidates = sorted(processed_candidates, key=lambda x: x["priority"], reverse=True)
    
    # Selected top action to populate recommendation
    if ranked_candidates:
        top_cand = ranked_candidates[0]
        recommendation = {
            "action": top_cand["action"],
            "propensity": top_cand["propensity"],
            "context": top_cand["context"],
            "value": top_cand["value"],
            "levers": top_cand["levers"],
            "priority": top_cand["priority"],
            "confidence": top_cand["confidence"],
            "candidates": ranked_candidates  # keep all candidates for potential UI list
        }
    else:
        recommendation = {
            "action": "No action recommended",
            "propensity": 0.0,
            "context": 0.0,
            "value": 0.0,
            "levers": 0.0,
            "priority": 0.0,
            "confidence": 0.0,
            "candidates": []
        }
        
    print(f"Reasoning completed. Selected: '{recommendation['action']}' with Priority: {recommendation['priority']}")
    
    return {
        "recommendation": recommendation
    }
