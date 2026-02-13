from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from app.graph.state import AgentState
from app.graph.nodes import llm_node, nasa_tools
from app.graph.edges import route

builder = StateGraph(AgentState)

builder.add_node("llm", llm_node)
builder.add_node("tools", ToolNode(nasa_tools))

builder.set_entry_point("llm")
builder.add_conditional_edges("llm", route, {
    "tools": "tools",
    "__end__": END,
})
builder.add_edge("tools", "llm")   # loop back so the LLM can read tool results

graph = builder.compile()
