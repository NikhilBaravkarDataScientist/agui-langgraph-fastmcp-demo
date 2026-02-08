async def stream_graph(graph, state):
    async for event in graph.astream_events(state, version="v2"):
        if event["event"] == "on_llm_stream":
            yield {
                "type": "token",
                "content": event["data"]["chunk"].content
            }
