from app.llm.openai import llm
from app.mcp.client import mcp_client
from app.llm.openai import get_llm

def llm_node(state):
    llm = get_llm()
    response = llm.invoke(state["messages"])
    return {
        "messages": state["messages"] + [("assistant", response.content)]
    }

def tool_node(state):
    last = state["messages"][-1][1]
    result = mcp_client.call("echo", {"text": last})
    return {"tool_result": result}
