from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.graph.nodes import llm_node, tool_node
from app.graph.edges import route

builder = StateGraph(AgentState)

builder.add_node("llm", llm_node)
builder.add_node("tool", tool_node)

builder.set_entry_point("llm")
builder.add_conditional_edges("llm", route, {
    "tool": "tool",
    "end": END
})

graph = builder.compile()
