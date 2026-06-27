import sys
import os
import uuid
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Add workspace directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.graph import graph
from langgraph.types import Command

app = FastAPI(
    title="Xen Orchestration API",
    description="FastAPI backend for Xen Next Best Action Customer Success platform"
)

class ProcessRequest(BaseModel):
    case_id: Optional[str] = None
    raw_input: str

class ResumeRequest(BaseModel):
    thread_id: str
    decision: str  # "approve" | "edit" | "reject"
    edit_payload: Optional[Dict[str, Any]] = None

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/process")
def process_case(request: ProcessRequest):
    """
    Starts a new case process. Parses the CRM notes, retrieves playbooks,
    calculates recommendations, and pauses before action execution.
    """
    thread_id = request.case_id or f"case-{uuid.uuid4().hex[:8]}"
    config = {"configurable": {"thread_id": thread_id}}
    
    # Establish initial state matching PulseState contract
    initial_state = {
        "case_id": thread_id,
        "raw_input": request.raw_input,
        "customer_profile": {},
        "assumptions": {},
        "retrieved_evidence": [],
        "recommendation": {},
        "explanation": "",
        "plan_trace": [],
        "status": "new",
        "human_decision": None
    }
    
    try:
        # Run graph until it interrupts before execute_node
        list(graph.stream(initial_state, config))
        
        # Get the interrupted state
        state = graph.get_state(config)
        
        # Ensure status reflects pending review (planner updates it)
        state_values = dict(state.values)
        if "execute" in state.next:
            state_values["status"] = "pending_review"
            # Update state with this status officially
            graph.update_state(config, {"status": "pending_review"}, as_node="planner")
            
        return {
            "thread_id": thread_id,
            "status": state_values.get("status"),
            "customer_profile": state_values.get("customer_profile"),
            "assumptions": state_values.get("assumptions"),
            "recommendation": state_values.get("recommendation"),
            "explanation": state_values.get("explanation"),
            "plan_trace": state_values.get("plan_trace"),
            "retrieved_evidence": state_values.get("retrieved_evidence")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting case: {str(e)}")

@app.post("/resume")
def resume_case(request: ResumeRequest):
    """
    Resumes a case from the paused state.
    Supports approving, rejecting, or editing assumptions to trigger re-reasoning.
    """
    if request.decision not in ["approve", "edit", "reject"]:
        raise HTTPException(status_code=400, detail="Decision must be 'approve', 'edit', or 'reject'")
        
    config = {"configurable": {"thread_id": request.thread_id}}
    state_before = graph.get_state(config)
    
    if not state_before.next or "execute" not in state_before.next:
        raise HTTPException(
            status_code=400,
            detail=f"Thread '{request.thread_id}' is not in a state awaiting human decision. Current next: {state_before.next}"
        )
        
    original_recommendation = state_before.values.get("recommendation")
    
    # Prepare decision payload
    decision_payload = {
        "decision": request.decision,
        "edit_payload": request.edit_payload
    }
    
    try:
        # 1. Update state first, attributing it to planner to preserve execution pointer
        graph.update_state(config, {"human_decision": decision_payload}, as_node="planner")
        
        # 2. Resume thread using Command
        list(graph.stream(Command(resume=decision_payload), config))
        
        # 3. Retrieve state after resumption
        state_after = graph.get_state(config)
        state_values = state_after.values
        
        response = {
            "thread_id": request.thread_id,
            "status": state_values.get("status"),
            "customer_profile": state_values.get("customer_profile"),
            "assumptions": state_values.get("assumptions"),
            "explanation": state_values.get("explanation"),
            "plan_trace": state_values.get("plan_trace")
        }
        
        if request.decision == "edit":
            response["original_recommendation"] = original_recommendation
            response["corrected_recommendation"] = state_values.get("recommendation")
        else:
            response["recommendation"] = state_values.get("recommendation")
            
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resuming case: {str(e)}")
