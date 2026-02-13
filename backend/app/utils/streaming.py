import json
import logging
from langchain_core.callbacks import AsyncCallbackHandler

logger = logging.getLogger(__name__)


class WebSocketStreamingHandler(AsyncCallbackHandler):
    """Callback handler that streams LLM tokens and tool events to a WebSocket."""

    def __init__(self, websocket):
        super().__init__()
        self.websocket = websocket
        self._tool_runs: dict = {}  # run_id -> tool_name

    # ---- LLM token streaming -------------------------------------------------

    async def on_llm_new_token(self, token: str, **kwargs):
        """Forward each generated token to the frontend."""
        if token:
            try:
                await self.websocket.send_json(
                    {"type": "token", "content": token}
                )
            except Exception as e:
                logger.error(f"Error streaming token: {e}")

    # ---- Tool lifecycle ------------------------------------------------------

    async def on_tool_start(self, serialized, input_str, *, run_id, **kwargs):
        tool_name = serialized.get("name", "unknown")
        self._tool_runs[run_id] = tool_name
        try:
            args = input_str
            if isinstance(input_str, str):
                try:
                    args = json.loads(input_str)
                except (json.JSONDecodeError, TypeError):
                    pass
            await self.websocket.send_json(
                {"type": "tool_start", "tool": tool_name, "args": args}
            )
        except Exception as e:
            logger.error(f"Error sending tool_start: {e}")

    async def on_tool_end(self, output, *, run_id, **kwargs):
        tool_name = self._tool_runs.pop(run_id, "unknown")
        try:
            result = str(output) if output else ""
            await self.websocket.send_json(
                {"type": "tool_end", "tool": tool_name, "result": result}
            )
        except Exception as e:
            logger.error(f"Error sending tool_end: {e}")
