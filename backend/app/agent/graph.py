import json
import re
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from ..llm_provider import get_llm, get_local_llm
from .prompts import TRANSLATOR_PROMPT, REVIEWER_PROMPT, STYLE_ALIGN_PROMPT
from ..services.nmt_service import NMTService

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

def clean_translation_response(text: str, original_text: str) -> str:
    """Helper to clean introductory commentary and unauthorized bold/italic formatting from LLM response."""
    cleaned = text.strip()
    
    # 1. Remove code blocks if the LLM wrapped the output in one
    cleaned = re.sub(r"^```(?:[a-zA-Z]+)?\n", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\n```$", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip()
    
    # 2. Remove typical introductory prefixes (case-insensitive)
    intro_patterns = [
        r"^here is the (polished|finalized|final)?\s*(vietnamese)?\s*translation:\s*",
        r"^here is the finalized\s*(vietnamese)?\s*sentence:\s*",
        r"^polished translation:\s*",
        r"^vietnamese translation:\s*",
        r"^sure, here is the translation:\s*",
        r"^bản dịch:\s*",
        r"^dưới đây là bản dịch:\s*"
    ]
    for pattern in intro_patterns:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    
    cleaned = cleaned.strip()
    
    # Also handle cases where there's an intro sentence on the first line ending with colon, followed by empty space/newline
    # e.g. "Here is the polished Vietnamese translation:"
    first_line_match = re.match(r"^([^\n]+):(\s*\n+)", cleaned)
    if first_line_match:
        line_content = first_line_match.group(1).lower()
        if "translation" in line_content or "polished" in line_content or "here is" in line_content or "vietnamese" in line_content:
            cleaned = cleaned[first_line_match.end():].strip()
            
    # 3. Handle bold asterisks.
    # If the original text does not contain '**', but the translation does, we should remove them.
    if "**" not in original_text:
        cleaned = cleaned.replace("**", "")
        
    # 4. Handle italic/other asterisks.
    if "*" not in original_text:
        cleaned = cleaned.replace("*", "")
        
    return cleaned.strip()

# 1. Translator Node
def translator_node(state: AgentState) -> Dict[str, Any]:
    original = state["original_text"]
    context = state["context_window"]
    glossary = state["glossary_context"]
    few_shot = state.get("few_shot_context", "")
    attempts = state.get("review_attempts", 0)
    
    # Check if this is the first attempt (Round 0)
    # Use offline NMT Service for fast and lightweight draft translation
    if attempts == 0:
        draft_translation = NMTService.translate(original)
        return {"translator_output": draft_translation}
        
    # If this is a re-translation after review feedback (attempts > 0)
    # We need reasoning capability to fix errors based on feedback, so we call local LLM (or fallback)
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
    cleaned = clean_translation_response(response.content, original)
    return {"translator_output": cleaned}

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
    if "suggested_correction" in review_data and review_data["suggested_correction"]:
        review_data["suggested_correction"] = clean_translation_response(
            review_data["suggested_correction"], original
        )
    
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

    llm = get_llm(temperature=0.1)
    
    prompt = STYLE_ALIGN_PROMPT.format(
        original_text=original,
        translated_text=translation
    )
    
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    cleaned = clean_translation_response(response.content, original)
    return {"final_output": cleaned}

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
