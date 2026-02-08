def route(state):
    last = state["messages"][-1][1]
    if "tool" in last.lower():
        return "tool"
    return "end"
