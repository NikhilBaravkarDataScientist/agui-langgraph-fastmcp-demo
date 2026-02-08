from uuid import uuid4
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.graph.graph import graph
from app.utils.memory import get_messages, save_message
from app.utils.streaming import stream_graph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AGUI Backend", description="Agentic AI with LangGraph and FastMCP")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.websocket("/ws/chat")
async def chat(ws: WebSocket):
    """WebSocket endpoint for chat interactions"""
    await ws.accept()
    session_id = str(uuid4())
    logger.info(f"New chat session: {session_id}")
    
    state = {
        "session_id": session_id,
        "messages": get_messages(session_id),
        "events": []
    }

    try:
        while True:
            data = await ws.receive_text()
            logger.info(f"Session {session_id}: Received message: {data[:50]}...")
            
            # Save user message
            save_message(session_id, "user", data)
            state["messages"] = get_messages(session_id)
            before_count = len(state["messages"])

            # Stream graph events
            try:
                async for event in stream_graph(graph, state):
                    await ws.send_json(event)
            except Exception as e:
                logger.error(f"Error streaming graph for session {session_id}: {e}")
                await ws.send_json({
                    "type": "error",
                    "content": "An error occurred while processing your request"
                })

            # Save assistant messages and send any that weren't already streamed
            updated_messages = state.get("messages", [])
            if len(updated_messages) > before_count:
                for role, content in updated_messages[before_count:]:
                    save_message(session_id, role, content)
                    # Send the full response as a token if it's from assistant
                    if role == "assistant":
                        logger.info(f"Session {session_id}: Sending assistant response")
                        await ws.send_json({
                            "type": "message_complete",
                            "content": content
                        })
                    
    except WebSocketDisconnect:
        logger.info(f"Session {session_id}: Client disconnected")
    except Exception as e:
        logger.error(f"Session {session_id}: WebSocket error: {e}", exc_info=True)
