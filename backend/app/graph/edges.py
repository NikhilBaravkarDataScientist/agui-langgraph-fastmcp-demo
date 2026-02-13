from langchain_core.messages import AIMessage


def route(state):
    """Route to tools node when the LLM wants to call a tool."""
    messages = state.get("messages", [])
    if not messages:
        return "__end__"
    last = messages[-1]
    if isinstance(last, AIMessage) and getattr(last, "tool_calls", None):
        return "tools"
    return "__end__"
