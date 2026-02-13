from fastmcp import FastMCP
from typing import Optional

mcp = FastMCP("NASA Space Exploration Tools")

@mcp.tool()
def get_apod(date: Optional[str] = None) -> dict:
    """
    Get NASA's Astronomy Picture of the Day (APOD)
    
    Args:
        date: Optional date in YYYY-MM-DD format. If not provided, returns today's APOD
        
    Returns:
        Dictionary with APOD data including title, explanation, image URL, and more
    """
    from tools import get_apod as get_apod_func
    return get_apod_func(date)

@mcp.tool()
def get_mars_rover_photos(sol: int = 1000, camera: str = "all", rover: str = "curiosity") -> dict:
    """
    Get photos from Mars Rovers (Curiosity, Opportunity, Spirit)
    
    Args:
        sol: Martian sol (day) number. Default is 1000
        camera: Camera name - options: FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM, PANCAM, MINITES, all. Default is 'all'
        rover: Rover name - options: curiosity, opportunity, spirit. Default is 'curiosity'
        
    Returns:
        Dictionary with Mars Rover photos
    """
    from tools import get_mars_rover_photos as get_photos_func
    return get_photos_func(sol, camera, rover)

@mcp.tool()
def get_neo_feed(start_date: Optional[str] = None, end_date: Optional[str] = None) -> dict:
    """
    Get Near Earth Objects (NEO) - asteroids data
    
    Args:
        start_date: Optional start date in YYYY-MM-DD format
        end_date: Optional end date in YYYY-MM-DD format (max 7 days from start_date)
        
    Returns:
        Dictionary with NEO data including potentially hazardous asteroids
    """
    from tools import get_neo_feed as get_neo_func
    return get_neo_func(start_date, end_date)

@mcp.tool()
def search_nasa_images(query: str, media_type: str = "image") -> dict:
    """
    Search NASA's Image and Video Library
    
    Args:
        query: Search query (e.g., "Mars", "Moon landing", "Hubble", "ISS")
        media_type: Type of media - options: image, video, audio. Default is 'image'
        
    Returns:
        Dictionary with search results from NASA's media library
    """
    from tools import search_nasa_images as search_func
    return search_func(query, media_type)

@mcp.tool()
def search_docs(query: str) -> str:
    """Search internal docs - legacy function"""
    from tools import search_docs as search_func
    return search_func(query)

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=9000)
