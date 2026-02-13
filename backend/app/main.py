from uuid import uuid4
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage, AIMessage

from app.graph.graph import graph
from app.utils.memory import get_messages, save_messages
from app.utils.streaming import WebSocketStreamingHandler

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

    try:
        while True:
            data = await ws.receive_text()
            logger.info(f"Session {session_id}: Received: {data[:50]}...")

            # Build state: history + new user message
            history = get_messages(session_id)
            user_msg = HumanMessage(content=data)

            state = {
                "session_id": session_id,
                "messages": history + [user_msg],
                "events": [],
            }

            handler = WebSocketStreamingHandler(ws)

            try:
                result = await graph.ainvoke(
                    state,
                    config={"callbacks": [handler], "recursion_limit": 25},
                )

                # Persist full conversation (including tool messages)
                save_messages(session_id, result["messages"])

                # Send the final assistant reply
                for msg in reversed(result["messages"]):
                    if (
                        isinstance(msg, AIMessage)
                        and msg.content
                        and not getattr(msg, "tool_calls", None)
                    ):
                        await ws.send_json(
                            {"type": "message_complete", "content": msg.content}
                        )
                        break

            except Exception as e:
                logger.error(
                    f"Error in graph for session {session_id}: {e}", exc_info=True
                )
                await ws.send_json(
                    {
                        "type": "error",
                        "content": "An error occurred while processing your request",
                    }
                )

    except WebSocketDisconnect:
        logger.info(f"Session {session_id}: Client disconnected")
    except Exception as e:
        logger.error(f"Session {session_id}: WebSocket error: {e}", exc_info=True)
