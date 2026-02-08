from typing import TypedDict, List, Tuple, Any


class AgentState(TypedDict):
    session_id: str
    messages: List[Tuple[str, str]]
    tool_result: Any
    events: list
