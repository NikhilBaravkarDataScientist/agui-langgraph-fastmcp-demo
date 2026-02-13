from app.llm.openai import get_llm
from app.mcp.client import mcp_client
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


def llm_node(state):
    """LLM node that processes messages and returns AI response"""
    llm = get_llm()

    last_user_message = ""
    for role, content in reversed(state["messages"]):
        if role == "user":
            last_user_message = content
            break

    needs_ui = any(
        keyword in last_user_message.lower()
        for keyword in ["bar chart", "chart", "graph", "plot"]
    )
    
    # Convert tuple messages to LangChain message objects
    messages = []
    
    # Add space exploration system prompt
    messages.append(SystemMessage(
        content=(
            "You are a NASA Space Exploration Assistant. You have access to real NASA APIs to help users explore space. "
            "You can:\n"
            "- Get the Astronomy Picture of the Day (APOD)\n"
            "- Fetch photos from Mars Rovers (Curiosity, Opportunity, Spirit)\n"
            "- Get information about Near Earth Objects (asteroids)\n"
            "- Search NASA's image and video library\n\n"
            "When users ask about space, planets, astronomy, Mars, asteroids, or NASA missions, "
            "use the appropriate NASA API tools to provide accurate, up-to-date information. "
            "Always be enthusiastic about space exploration and help users discover the wonders of our universe!"
        )
    ))
    
    if needs_ui:
        messages.append(SystemMessage(
            content=(
                "If the user requests a chart and provides data, include an "
                "Open-JSON-UI block in the response. Use a fenced code block "
                "with the language tag open-json-ui and a bar_chart node. "
                "Example: ```open-json-ui {\"type\":\"bar_chart\",\"labels\":[...]," 
                "\"values\":[...]} ```. If data is missing, ask the user to provide it."
            )
        ))
    
    for role, content in state["messages"]:
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
    
    # Call the LLM 
    response = llm.invoke(messages)
    
    # Extract the content from the response
    content = response.content if hasattr(response, "content") else str(response)
    
    return {
        "messages": state["messages"] + [("assistant", content)]
    }


def tool_node(state):
    last = state["messages"][-1][1]

    state.setdefault("events", []).append({
        "type": "tool_start",
        "tool": "echo",
        "args": {"text": last}
    })

    result = mcp_client.call("echo", {"text": last})

    state.setdefault("events", []).append({
        "type": "tool_end",
        "tool": "echo",
        "result": result
    })

    return {"tool_result": result}
