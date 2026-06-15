import json
import re
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from ..llm_provider import get_llm, get_local_llm
from .prompts import TRANSLATOR_PROMPT, REVIEWER_PROMPT, STYLE_ALIGN_PROMPT

class AgentState(TypedDict):
    original_text: str
    context_window: str
    glossary_context: str
    few_shot_context: str
    translator_output: str
    reviewer_output: Dict[str, Any]
    review_attempts: int
    final_output: str

def clean_json_response(text: str) -> Dict[str, Any]:
    """Helper to clean and parse JSON response from LLM."""
    cleaned = text.strip()
    # Remove code blocks if present
    cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"```$", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip()
    try:
        return json.loads(cleaned)
    except Exception as e:
        # Fallback in case of failure
        return {
            "is_passed": True,  # Fallback to true to avoid infinite loops
            "feedback": f"Failed to parse JSON: {str(e)}",
            "suggested_correction": text
        }

# 1. Translator Node
def translator_node(state: AgentState) -> Dict[str, Any]:
    original = state["original_text"]
    context = state["context_window"]
    glossary = state["glossary_context"]
    few_shot = state.get("few_shot_context", "")
    attempts = state.get("review_attempts", 0)
    
    llm = get_local_llm(temperature=0.3)
    
    # If this is a re-translation after review feedback
    feedback_context = ""
    if attempts > 0 and "reviewer_output" in state:
        fb = state["reviewer_output"].get("feedback", "")
        suggested = state["reviewer_output"].get("suggested_correction", "")
        feedback_context = (
            f"\n\n[REVIEW FEEDBACK FROM PREVIOUS ATTEMPT]\n"
            f"The reviewer failed your previous translation with this feedback: '{fb}'.\n"
            f"Suggested correction: '{suggested}'.\n"
            f"Please revise your translation to correct these issues."
        )

    system_prompt = TRANSLATOR_PROMPT.format(
        glossary_context=glossary,
        few_shot_context=few_shot
    )
    
    user_prompt = (
        f"{context}"
        f"{feedback_context}"
    )
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = llm.invoke(messages)
    return {"translator_output": response.content.strip()}

# 2. Reviewer Node
def reviewer_node(state: AgentState) -> Dict[str, Any]:
    original = state["original_text"]
    translation = state["translator_output"]
    glossary = state["glossary_context"]
    context = state["context_window"]
    attempts = state.get("review_attempts", 0)
    
    llm = get_llm(temperature=0.2)
    
    prompt = REVIEWER_PROMPT.format(
        original_text=original,
        translated_text=translation,
        glossary_context=glossary,
        context_window=context
    )
    
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    review_data = clean_json_response(response.content)
    
    return {
        "reviewer_output": review_data,
        "review_attempts": attempts + 1
    }

# 3. Style Node
def style_align_node(state: AgentState) -> Dict[str, Any]:
    original = state["original_text"]
    # If passed, use translator's translation. Otherwise, use reviewer's suggested correction.
    rev_out = state.get("reviewer_output", {})
    translation = state["translator_output"]
    if rev_out and not rev_out.get("is_passed", False):
        translation = rev_out.get("suggested_correction") or translation

    llm = get_local_llm(temperature=0.1)
    
    prompt = STYLE_ALIGN_PROMPT.format(
        original_text=original,
        translated_text=translation
    )
    
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    return {"final_output": response.content.strip()}

# 4. Conditional Edge router
def router_edge(state: AgentState) -> str:
    rev_out = state.get("reviewer_output", {})
    attempts = state.get("review_attempts", 0)
    
    # If passed OR we hit max attempts (3), proceed to Style alignment
    if rev_out.get("is_passed", False) or attempts >= 3:
        return "style"
    else:
        return "translate"

# Define the workflow graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("translate", translator_node)
workflow.add_node("review", reviewer_node)
workflow.add_node("style", style_align_node)

# Set Entry Point
workflow.set_entry_point("translate")

# Add Edges
workflow.add_edge("translate", "review")

workflow.add_conditional_edges(
    "review",
    router_edge,
    {
        "translate": "translate",
        "style": "style"
    }
)

workflow.add_edge("style", END)

# Compile Graph
translation_agent = workflow.compile()
