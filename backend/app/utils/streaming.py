import logging

logger = logging.getLogger(__name__)


async def stream_graph(graph, state):
    """Stream events from the LangGraph computation"""
    try:
        async for event in graph.astream_events(state, version="v2"):
            try:
                if event["event"] == "on_llm_stream":
                    chunk = event.get("data", {}).get("chunk")
                    if chunk and hasattr(chunk, "content") and chunk.content:
                        yield {
                            "type": "token",
                            "content": chunk.content
                        }
                elif event["event"] == "on_chain_end":
                    data = event.get("data", {})
                    output = data.get("output")

                    if output and isinstance(output, dict) and "messages" in output:
                        # Keep the latest graph state so the caller can persist it.
                        state["messages"] = output["messages"]
                        
                elif event["event"] == "on_tool_start":
                    tool_name = event.get("name", "unknown")
                    tool_input = event.get("data", {}).get("input")
                    yield {
                        "type": "tool_start",
                        "tool": tool_name,
                        "args": tool_input
                    }
                elif event["event"] == "on_tool_end":
                    tool_name = event.get("name", "unknown")
                    tool_output = event.get("data", {}).get("output")
                    yield {
                        "type": "tool_end",
                        "tool": tool_name,
                        "result": tool_output
                    }
            except Exception as e:
                logger.error(f"Error processing graph event: {e}", exc_info=True)
                continue

        # Yield any buffered tool events from state
        for tool_event in state.get("events", []):
            yield tool_event

        state["events"] = []

    except Exception as e:
        logger.error(f"Error streaming from graph: {e}", exc_info=True)
        yield {
            "type": "error",
            "content": "An error occurred while processing your request"
        }
