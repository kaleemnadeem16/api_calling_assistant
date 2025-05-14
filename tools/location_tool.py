"""
Location Tool for the LangChain API Calling Assistant.

This tool provides IP-based location detection to determine
the user's approximate current location.
"""

import json
import geocoder
from langchain.tools import BaseTool


class MyLocationTool(BaseTool):
    """Tool for getting user's current location."""
    name: str = "get_my_location"
    description: str = "Get the user's current approximate location based on IP address"
    
    def _run(self) -> str:
        """Execute the location detection tool."""
        try:
            # Get location based on IP
            g = geocoder.ip('me')
            
            if g.ok:
                result = {
                    "success": True,
                    "city": g.city,
                    "region": g.state,
                    "country": g.country,
                    "coordinates": {"latitude": g.latlng[0], "longitude": g.latlng[1]},
                    "ip_address": g.ip,
                    "note": "Location determined by IP address (approximate)"
                }
            else:
                result = {
                    "success": False,
                    "error": "Could not determine location from IP address"
                }
            
            return json.dumps(result)
                
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"Location detection error: {str(e)}"
            })