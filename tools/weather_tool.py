"""
Weather Tool for the LangChain API Calling Assistant.

This tool provides current weather information for cities worldwide
using the OpenWeatherMap API.
"""

import os
import json
import requests
from typing import Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel
from .schemas import WeatherInput


class WeatherTool(BaseTool):
    """Tool for getting current weather information."""
    name: str = "get_current_weather"
    description: str = "Get the current weather information for a specific city"
    args_schema: Type[BaseModel] = WeatherInput
    
    def _run(self, city: str, country: Optional[str] = None, units: Optional[str] = None) -> str:
        """Execute the weather tool."""
        try:
            weather_api_key = os.getenv('WEATHER_API_KEY')
            base_url = os.getenv('API_BASE_URL', 'https://api.openweathermap.org/data/2.5')
            timeout = int(os.getenv('TIMEOUT', '10'))
            
            # Prepare query parameter
            query = city
            if country:
                query = f"{city},{country}"
            
            # Use provided units or default
            units = units or "metric"
            
            # Prepare request parameters
            params = {
                'q': query,
                'appid': weather_api_key,
                'units': units
            }
            
            # Make API request
            response = requests.get(
                f"{base_url}/weather",
                params=params,
                timeout=timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Format the response for the agent
                result = {
                    "success": True,
                    "city": data.get("name"),
                    "country": data.get("sys", {}).get("country"),
                    "temperature": data.get("main", {}).get("temp"),
                    "feels_like": data.get("main", {}).get("feels_like"),
                    "humidity": data.get("main", {}).get("humidity"),
                    "pressure": data.get("main", {}).get("pressure"),
                    "description": data.get("weather", [{}])[0].get("description"),
                    "wind_speed": data.get("wind", {}).get("speed"),
                    "units": units
                }
                
                return json.dumps(result)
            else:
                error_data = response.json() if response.content else {}
                return json.dumps({
                    "success": False,
                    "error": f"Weather API error: {error_data.get('message', 'Unknown error')}"
                })
                
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"Weather lookup failed: {str(e)}"
            })