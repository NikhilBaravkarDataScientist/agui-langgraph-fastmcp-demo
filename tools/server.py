from fastapi import FastAPI
from fastmcp import FastMCP
from pydantic import BaseModel
from typing import Optional
import uvicorn

from tools import (
    get_apod as _get_apod,
    get_mars_rover_photos as _get_mars_rover_photos,
    get_neo_feed as _get_neo_feed,
    search_nasa_images as _search_nasa_images,
    search_docs as _search_docs,
)

# --- FastAPI REST server (used by backend) ---

app = FastAPI(title="NASA Tools Server")

TOOL_REGISTRY = {
    "get_apod": _get_apod,
    "get_mars_rover_photos": _get_mars_rover_photos,
    "get_neo_feed": _get_neo_feed,
    "search_nasa_images": _search_nasa_images,
    "search_docs": _search_docs,
}


class ToolCallRequest(BaseModel):
    tool: str
    args: dict = {}


@app.post("/call")
async def call_tool(request: ToolCallRequest):
    func = TOOL_REGISTRY.get(request.tool)
    if not func:
        return {"error": f"Unknown tool: {request.tool}"}
    try:
        result = func(**request.args)
        return result
    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
async def health():
    return {"status": "ok", "tools": list(TOOL_REGISTRY.keys())}


# --- FastMCP server (kept for MCP protocol compatibility) ---

mcp = FastMCP("NASA Space Exploration Tools")


@mcp.tool()
def get_apod(date: Optional[str] = None) -> dict:
    """Get NASA's Astronomy Picture of the Day (APOD)

    Args:
        date: Optional date in YYYY-MM-DD format. If not provided, returns today's APOD
    """
    return _get_apod(date)


@mcp.tool()
def get_mars_rover_photos(
    sol: int = 1000, camera: str = "all", rover: str = "curiosity"
) -> dict:
    """Get photos from Mars Rovers (Curiosity, Opportunity, Spirit)

    Args:
        sol: Martian sol (day) number. Default is 1000
        camera: Camera name (FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM, PANCAM, MINITES, all)
        rover: Rover name (curiosity, opportunity, spirit)
    """
    return _get_mars_rover_photos(sol, camera, rover)


@mcp.tool()
def get_neo_feed(
    start_date: Optional[str] = None, end_date: Optional[str] = None
) -> dict:
    """Get Near Earth Objects (NEO) - asteroids data

    Args:
        start_date: Optional start date in YYYY-MM-DD format
        end_date: Optional end date in YYYY-MM-DD format (max 7 days from start_date)
    """
    return _get_neo_feed(start_date, end_date)


@mcp.tool()
def search_nasa_images(query: str, media_type: str = "image") -> dict:
    """Search NASA's Image and Video Library

    Args:
        query: Search query (e.g., "Mars", "Moon landing", "Hubble", "ISS")
        media_type: Type of media (image, video, audio)
    """
    return _search_nasa_images(query, media_type)


@mcp.tool()
def search_docs(query: str) -> str:
    """Search internal docs - legacy function"""
    return _search_docs(query)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
