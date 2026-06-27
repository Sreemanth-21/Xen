import os
import json
import re
from typing import Any
from groq import Groq
from dotenv import load_dotenv
from agents.graph import PulseState

# Load environment variables
load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Warning: GROQ_API_KEY environment variable is not set. Using dummy client/mock.")
        return None
    return Groq(api_key=api_key)

def ingestion_node(state: PulseState) -> dict[str, Any]:
    print("--- RUNNING INGESTION & CONTEXT AGENT ---")
    raw_input = state.get("raw_input", "")
    
    client = get_groq_client()
    if not client:
        # Fallback Mock in case GROQ_API_KEY is not configured
        print("Mocking Ingestion LLM call due to missing Groq API Key.")
        # Perform basic regex extraction for company name
        company_match = re.search(r"(?:company|for|at)\s+([A-Z][a-zA-Z0-9_]+)", raw_input)
        company_name = company_match.group(1) if company_match else "Acme Corp"
        
        # Make default profile & assumptions
        profile = {
            "company_name": company_name,
            "contract_value": 50000,
            "contract_type": "Annual",
            "health_score": 75,
            "segment": "Mid-Market",
            "churn_risk": "Medium",
            "license_count": 100,
            "active_users": 60
        }
        assumptions = {
            "contract_type": "Inferred Annual based on typical SaaS contract templates.",
            "health_score": "Inferred 75 based on neutral CRM tone.",
            "segment": "Inferred Mid-Market from customer size."
        }
        return {
            "customer_profile": profile,
            "assumptions": assumptions
        }

    # Prompt Groq Llama 3.3 70B
    system_prompt = (
        "You are the Ingestion and Context Agent for Xen, a B2B SaaS Customer Success Next Best Action platform.\n"
        "Your task is to parse raw CRM notes, interaction transcripts, or emails and extract a structured customer profile.\n"
        "If some fields are not explicitly stated, you must infer them based on the context and record them under 'assumptions' with a clear key-value structure.\n\n"
        "You must return a JSON object with the following fields:\n"
        "{\n"
        "  \"customer_profile\": {\n"
        "    \"company_name\": \"string (name of the company)\",\n"
        "    \"contract_value\": number (annual or total contract value if available, default to null if completely unknown)\",\n"
        "    \"contract_type\": \"string (Annual, Monthly, Multi-year, etc.)\",\n"
        "    \"health_score\": number (customer health score 0-100)\",\n"
        "    \"segment\": \"string (Enterprise, Mid-Market, SMB)\",\n"
        "    \"churn_risk\": \"string (High, Medium, Low)\",\n"
        "    \"license_count\": number,\n"
        "    \"active_users\": number\n"
        "  },\n"
        "  \"assumptions\": {\n"
        "    \"field_name_1\": \"Why this value was assumed/inferred\",\n"
        "    \"field_name_2\": \"Why this value was assumed/inferred\"\n"
        "  }\n"
        "}"
    )

    user_prompt = f"Raw CRM Input:\n\"\"\"\n{raw_input}\n\"\"\""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        result_text = completion.choices[0].message.content
        data = json.loads(result_text)
        
        profile = data.get("customer_profile", {})
        assumptions = data.get("assumptions", {})
        
        # Ensure company name is present
        if not profile.get("company_name"):
            profile["company_name"] = "Unknown Company"
            assumptions["company_name"] = "Inferred 'Unknown Company' because no name was found in raw input."
            
        return {
            "customer_profile": profile,
            "assumptions": assumptions
        }
    except Exception as e:
        print(f"Error calling Groq API in Ingestion: {e}")
        raise e
