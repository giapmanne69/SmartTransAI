from typing import List, Dict, Any

def format_glossary_for_prompt(glossary_matches: List[Dict[str, Any]]) -> str:
    """
    Format list of glossary matches into a readable string for system prompt injection.
    """
    if not glossary_matches:
        return "None. Use standard academic translations."
        
    lines = []
    for item in glossary_matches:
        lines.append(f"- '{item['source_term']}' -> '{item['target_term']}' (Notes: {item.get('notes') or 'N/A'})")
    return "\n".join(lines)
