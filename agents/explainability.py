"""
Explainability Agent — owned by Teammate C (Member 3)

Responsibilities:
- Takes recommendation dict + retrieved_evidence from PulseState
- Makes a Groq LLM call to produce a human-readable `explanation` string
- Cites specific evidence snippets by source
- Explicitly flags low confidence (< 0.5) with a warning

This node is called by the LangGraph orchestration. Do NOT import this
directly from the UI — always go through the FastAPI /process endpoint.
"""

import os
from typing import Any
from dotenv import load_dotenv

load_dotenv()

# Lazy import to avoid hard crash if groq is not installed yet
try:
    from groq import Groq
    _groq_available = True
except ImportError:
    _groq_available = False

# Import PulseState contract from graph (within agents package)
from agents.graph import PulseState


def _build_prompt(recommendation: dict, retrieved_evidence: list[dict], guidance: str = None) -> str:
    """
    Constructs the LLM prompt from the recommendation, evidence, and human guidance.
    """
    action = recommendation.get("action", "N/A")
    propensity = recommendation.get("propensity", 0.0)
    context_score = recommendation.get("context", 0.0)
    value = recommendation.get("value", 0.0)
    levers = recommendation.get("levers", "N/A")
    priority = recommendation.get("priority", 0.0)
    confidence = recommendation.get("confidence", 0.0)

    # Format evidence snippets
    evidence_lines = []
    for i, ev in enumerate(retrieved_evidence or []):
        source = ev.get("source", "Unknown Source")
        text = ev.get("text", "")
        score = ev.get("score", 0.0)
        evidence_lines.append(f"  [{i+1}] Source: \"{source}\" (relevance {score:.2f})\n       Snippet: \"{text}\"")

    evidence_block = "\n".join(evidence_lines) if evidence_lines else "  No evidence retrieved."

    # Low-confidence flag instruction
    confidence_instruction = ""
    if confidence < 0.5:
        confidence_instruction = (
            "\n\nIMPORTANT: The confidence score is LOW (below 0.5). "
            "Your explanation MUST include a clear warning such as: "
            "'Low confidence — recommend human judgment over automation.' "
            "Do NOT present this recommendation with the same certainty as a high-confidence case."
        )

    prompt = f"""You are an AI explainability agent for a B2B SaaS Customer Success platform called Pulse.
Your job is to produce a concise, professional, human-readable explanation for a Customer Success Manager (CSM).

The AI system has produced the following recommendation:
- Recommended Action: {action}
- Propensity Score: {propensity:.2f}
- Context Relevance Score: {context_score:.2f}
- Account Value Score: {value:.2f}
- Action Levers: {levers}
- Computed Priority Score: {priority:.2f}
- Confidence: {confidence:.2f}{confidence_instruction}

The following evidence was retrieved to support this recommendation:
{evidence_block}

Write a 2–4 sentence explanation that:
1. States the recommended action plainly and directly.
2. Cites at least one specific evidence snippet by source name (e.g., "According to [Source Name]...").
3. Briefly references the key signals driving the recommendation (e.g., usage drop, champion departure).
4. If confidence is below 0.5, includes the phrase "Low confidence — recommend human judgment over automation."
5. Do NOT re-state basic account profile facts (such as company segment, contract type, contract value, or active user count) that are already visible in the sidebar UI. Focus strictly on the reasoning, evidence citations, and key risk signals.
"""
    if guidance:
        prompt += f"\n\nNote: The user provided the following guidance override: \"{guidance}\". Integrate this guidance into your explanation and explain how the recommendation was adjusted in response to this human feedback."

    return prompt.strip()


def explainability_node(state: PulseState) -> dict[str, Any]:
    """
    LangGraph node: generates a human-readable explanation using the Groq LLM.
    Falls back to a rule-based explanation if Groq is unavailable.
    """
    print("--- RUNNING EXPLAINABILITY AGENT (Teammate C) ---")

    recommendation = state.get("recommendation", {})
    retrieved_evidence = state.get("retrieved_evidence", [])
    confidence = recommendation.get("confidence", 1.0)
    customer_profile = state.get("customer_profile", {})
    guidance = customer_profile.get("guidance_override")

    # ---- Attempt Groq LLM call ----
    api_key = os.getenv("GROQ_API_KEY")

    if _groq_available and api_key and api_key != "your_groq_api_key_here":
        try:
            client = Groq(api_key=api_key)
            prompt = _build_prompt(recommendation, retrieved_evidence, guidance=guidance)

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a precise, professional AI explainability agent for a B2B SaaS "
                            "Customer Success platform. Always be concise, evidence-backed, and honest "
                            "about uncertainty."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=300,
            )

            explanation = chat_completion.choices[0].message.content.strip()
            print(f"Explainability Agent: Groq explanation generated successfully.")
            return {"explanation": explanation}

        except Exception as e:
            print(f"Explainability Agent: Groq call failed ({e}), falling back to rule-based explanation.")

    # ---- Rule-based fallback (no API key or Groq unavailable) ----
    explanation = _rule_based_explanation(recommendation, retrieved_evidence, guidance=guidance)
    return {"explanation": explanation}


def _rule_based_explanation(recommendation: dict, retrieved_evidence: list[dict], guidance: str = None) -> str:
    """
    Fallback explanation builder using rule-based logic. Used when Groq is unavailable.
    """
    action = recommendation.get("action", "the recommended action")
    confidence = recommendation.get("confidence", 1.0)
    levers = recommendation.get("levers", "")

    # Pick the top evidence source
    top_source = None
    top_snippet = None
    if retrieved_evidence:
        top_ev = max(retrieved_evidence, key=lambda x: x.get("score", 0))
        top_source = top_ev.get("source", "retrieved playbooks")
        top_snippet = top_ev.get("text", "")

    parts = [f"The system recommends: {action}."]

    if top_source and top_snippet:
        # Cite the top evidence
        parts.append(f"This is supported by evidence from \"{top_source}\": \"{top_snippet[:120]}...\"")

    if levers:
        parts.append(f"Suggested action levers include: {levers}.")

    if confidence < 0.5:
        parts.append(
            f"Low confidence ({confidence:.2f}) — recommend human judgment over automation. "
            "Key assumptions in the customer profile were inferred and have not been verified."
        )
    else:
        parts.append(
            f"This recommendation has a confidence score of {confidence:.2f}, indicating reliable signal strength."
        )

    if guidance:
        parts.append(f"Adjusted recommendation in response to CSM guidance: \"{guidance}\".")

    return " ".join(parts)
