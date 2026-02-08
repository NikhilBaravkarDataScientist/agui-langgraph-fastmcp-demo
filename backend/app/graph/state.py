from typing import TypedDict, List, Tuple, Any

class AgentState(TypedDict):
    messages: List[Tuple[str, str]]
    tool_result: Any
