from fastapi import FastAPI, WebSocket
from app.graph.graph import graph
print("LangGraph compiled OK")

from app.utils.streaming import stream_graph

app = FastAPI()

@app.websocket("/ws/chat")
async def chat(ws: WebSocket):
    await ws.accept()
    state = {"messages": []}

    while True:
        data = await ws.receive_text()
        state["messages"].append(("user", data))

        async for event in stream_graph(graph, state):
            await ws.send_json(event)
