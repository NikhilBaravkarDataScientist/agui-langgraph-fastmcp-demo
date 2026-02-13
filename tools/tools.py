import os
import requests
from typing import Dict, Any, Optional


def get_nasa_api_key() -> str:
    """Get NASA API key from environment variable"""
    api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
    return api_key


def get_apod(date: Optional[str] = None) -> Dict[str, Any]:
    """
    Get NASA's Astronomy Picture of the Day
    
    Args:
        date: Date in YYYY-MM-DD format. If None, returns today's APOD
        
    Returns:
        Dictionary containing APOD data including title, explanation, url, and media type
    """
    api_key = get_nasa_api_key()
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key}
    
    if date:
        params["date"] = date
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "title": data.get("title", ""),
            "explanation": data.get("explanation", ""),
            "url": data.get("url", ""),
            "hdurl": data.get("hdurl", ""),
            "media_type": data.get("media_type", "image"),
            "date": data.get("date", "")
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_mars_rover_photos(sol: int = 1000, camera: str = "all", rover: str = "curiosity") -> Dict[str, Any]:
    """
    Get photos from Mars Rovers
    
    Args:
        sol: Martian sol (day) number
        camera: Camera name (FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM, PANCAM, MINITES, all)
        rover: Rover name (curiosity, opportunity, spirit)
        
    Returns:
        Dictionary containing photos from the Mars Rover
    """
    api_key = get_nasa_api_key()
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos"
    params = {
        "api_key": api_key,
        "sol": sol,
        "page": 1
    }
    
    if camera != "all":
        params["camera"] = camera
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        photos = data.get("photos", [])
        
        # Limit to first 5 photos to keep response manageable
        limited_photos = photos[:5]
        
        return {
            "success": True,
            "rover": rover,
            "sol": sol,
            "total_photos": len(photos),
            "photos": [
                {
                    "id": photo.get("id"),
                    "img_src": photo.get("img_src"),
                    "camera": photo.get("camera", {}).get("full_name", ""),
                    "earth_date": photo.get("earth_date", "")
                }
                for photo in limited_photos
            ]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_neo_feed(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Get Near Earth Objects (asteroids) data
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format (max 7 days from start_date)
        
    Returns:
        Dictionary containing NEO data
    """
    api_key = get_nasa_api_key()
    url = "https://api.nasa.gov/neo/rest/v1/feed"
    params = {"api_key": api_key}
    
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Parse and summarize NEO data
        total_count = data.get("element_count", 0)
        neo_data = []
        
        near_earth_objects = data.get("near_earth_objects", {})
        for date, objects in list(near_earth_objects.items())[:3]:  # Limit to 3 days
            for obj in objects[:3]:  # Limit to 3 objects per day
                neo_data.append({
                    "name": obj.get("name", ""),
                    "date": date,
                    "is_potentially_hazardous": obj.get("is_potentially_hazardous_asteroid", False),
                    "estimated_diameter_km": obj.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_max", 0),
                    "close_approach_data": obj.get("close_approach_data", [{}])[0].get("miss_distance", {}).get("kilometers", "N/A")
                })
        
        return {
            "success": True,
            "total_count": total_count,
            "neo_objects": neo_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def search_nasa_images(query: str, media_type: str = "image") -> Dict[str, Any]:
    """
    Search NASA's Image and Video Library
    
    Args:
        query: Search query
        media_type: Type of media (image, video, audio)
        
    Returns:
        Dictionary containing search results
    """
    url = "https://images-api.nasa.gov/search"
    params = {
        "q": query,
        "media_type": media_type
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        items = data.get("collection", {}).get("items", [])
        
        # Limit to first 5 results
        limited_items = items[:5]
        
        results = []
        for item in limited_items:
            item_data = item.get("data", [{}])[0]
            links = item.get("links", [{}])
            
            results.append({
                "title": item_data.get("title", ""),
                "description": item_data.get("description", "")[:200] + "..." if len(item_data.get("description", "")) > 200 else item_data.get("description", ""),
                "nasa_id": item_data.get("nasa_id", ""),
                "date_created": item_data.get("date_created", ""),
                "media_type": item_data.get("media_type", ""),
                "thumbnail": links[0].get("href", "") if links else ""
            })
        
        return {
            "success": True,
            "query": query,
            "total_hits": data.get("collection", {}).get("metadata", {}).get("total_hits", 0),
            "results": results
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def search_docs(query: str):
    """Legacy search docs function - kept for backward compatibility"""
    return f"Results for: {query}"
