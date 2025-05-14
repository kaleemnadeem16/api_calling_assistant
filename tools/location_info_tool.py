"""
Location Info Tool for the LangChain API Calling Assistant.

This tool provides detailed information about specific locations
using geocoding services.
"""

import json
import geocoder
from typing import Type
from langchain.tools import BaseTool
from pydantic import BaseModel
from .schemas import LocationInput


class LocationInfoTool(BaseTool):
    """Tool for getting detailed location information."""
    name: str = "get_location_info"
    description: str = "Get detailed information about a specific location (coordinates, country, etc.)"
    args_schema: Type[BaseModel] = LocationInput
    
    def _run(self, location: str) -> str:
        """Execute the location info tool."""
        try:
            # Use geocoder to get detailed location info
            g = geocoder.osm(location)
            
            if g.ok:
                result = {
                    "success": True,
                    "address": g.address,
                    "city": g.city,
                    "state": g.state,
                    "country": g.country,
                    "postal_code": g.postal,
                    "coordinates": {
                        "latitude": g.latlng[0],
                        "longitude": g.latlng[1]
                    }
                }
            else:
                result = {
                    "success": False,
                    "error": f"Could not find detailed information for: {location}"
                }
            
            return json.dumps(result)
                
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"Location info error: {str(e)}"
            })