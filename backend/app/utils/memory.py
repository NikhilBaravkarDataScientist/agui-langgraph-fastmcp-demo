from collections import defaultdict

MEMORY = defaultdict(list)


def get_messages(session_id: str) -> list:
    """Return the full conversation history (list of LangChain BaseMessage)."""
    return list(MEMORY[session_id])


def save_messages(session_id: str, messages: list):
    """Overwrite conversation history with the complete message list."""
    MEMORY[session_id] = list(messages)
