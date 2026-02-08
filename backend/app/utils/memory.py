from collections import defaultdict

MEMORY = defaultdict(list)


def get_messages(session_id: str):
    return MEMORY[session_id]


def save_message(session_id: str, role: str, content: str):
    MEMORY[session_id].append((role, content))
