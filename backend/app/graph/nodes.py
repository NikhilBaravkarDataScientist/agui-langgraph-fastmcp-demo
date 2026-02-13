import json
from typing import Optional

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage

from app.llm.openai import get_llm
from app.mcp.client import mcp_client


# --------------- LangChain tool wrappers (call tools server via REST) --------

@tool
def get_apod(date: Optional[str] = None) -> str:
    """Get NASA's Astronomy Picture of the Day (APOD).

    Args:
        date: Optional date in YYYY-MM-DD format. If not provided, returns today's APOD.
    """
    args = {}
    if date:
        args["date"] = date
    return json.dumps(mcp_client.call("get_apod", args))


@tool
def get_mars_rover_photos(
    sol: int = 1000, camera: str = "all", rover: str = "curiosity"
) -> str:
    """Get photos from Mars Rovers (Curiosity, Opportunity, Spirit).

    Args:
        sol: Martian sol (day) number. Default is 1000.
        camera: Camera name - FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM, PANCAM, MINITES, or 'all'.
        rover: Rover name - curiosity, opportunity, or spirit.
    """
    return json.dumps(
        mcp_client.call(
            "get_mars_rover_photos",
            {"sol": sol, "camera": camera, "rover": rover},
        )
    )


@tool
def get_neo_feed(
    start_date: Optional[str] = None, end_date: Optional[str] = None
) -> str:
    """Get Near Earth Objects (asteroids) data from NASA.

    Args:
        start_date: Optional start date in YYYY-MM-DD format.
        end_date: Optional end date in YYYY-MM-DD format (max 7 days from start_date).
    """
    args = {}
    if start_date:
        args["start_date"] = start_date
    if end_date:
        args["end_date"] = end_date
    return json.dumps(mcp_client.call("get_neo_feed", args))


@tool
def search_nasa_images(query: str, media_type: str = "image") -> str:
    """Search NASA's Image and Video Library.

    Args:
        query: Search query (e.g., 'Mars', 'Moon landing', 'Hubble', 'ISS').
        media_type: Type of media - image, video, or audio. Default is 'image'.
    """
    return json.dumps(
        mcp_client.call(
            "search_nasa_images",
            {"query": query, "media_type": media_type},
        )
    )


nasa_tools = [get_apod, get_mars_rover_photos, get_neo_feed, search_nasa_images]

# --------------- System prompt ------------------------------------------------

SYSTEM_PROMPT = (
    "You are a NASA Space Exploration Assistant with access to real NASA APIs. "
    "You have the following tools:\n"
    "- get_apod: Get the Astronomy Picture of the Day\n"
    "- get_mars_rover_photos: Fetch photos from Mars Rovers (Curiosity, Opportunity, Spirit)\n"
    "- get_neo_feed: Get Near Earth Object (asteroid) data\n"
    "- search_nasa_images: Search NASA's image and video library\n\n"
    "IMPORTANT RULES:\n"
    "1. When users ask about space topics, ALWAYS call the appropriate tool to fetch real data. "
    "Do NOT make up information.\n"
    "2. When tool results contain image URLs (img_src, url, hdurl, thumbnail), "
    "ALWAYS display them as markdown images: ![description](url)\n"
    "   Example: ![Mars Rover Photo](http://mars.jpl.nasa.gov/image.jpg)\n"
    "3. Be enthusiastic about space exploration!\n"
    "4. If the user requests a chart, include an open-json-ui code block.\n"
)

# --------------- Graph nodes --------------------------------------------------


def llm_node(state):
    """LLM node – calls the model with tools bound."""
    llm = get_llm().bind_tools(nasa_tools)
    # Prepend system prompt (not stored in conversation state)
    all_messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(all_messages)
    return {"messages": [response]}
