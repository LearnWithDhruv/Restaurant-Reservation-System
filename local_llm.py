# local_llm.py

def process_input(user_input):
    """Placeholder for LLM processing. Delegates to tool_registry."""
    from agents.tool_registry import detect_intent
    return detect_intent(user_input)