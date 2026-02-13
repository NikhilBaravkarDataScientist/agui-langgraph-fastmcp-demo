from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    session_id: str
    messages: Annotated[list, add_messages]
    events: list
