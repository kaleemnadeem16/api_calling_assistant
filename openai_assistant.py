"""
OpenAI-powered assistant with multiple function calling capabilities.

This module demonstrates OpenAI's function calling feature by integrating
with multiple external APIs and services based on user queries processed by GPT models.
"""

import os
import json
import datetime
import requests
import geocoder
from typing import Dict, List, Optional, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class MultiToolAssistant:
    """OpenAI-powered assistant with multiple tool/function calling capabilities."""
    
    def __init__(self):
        """Initialize the assistant with API credentials and function definitions."""
        # Load configuration from environment
        self.openai_client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '500'))
        
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        self.base_url = os.getenv('API_BASE_URL', 'https://api.openweathermap.org/data/2.5')
        self.default_units = os.getenv('DEFAULT_UNITS', 'metric')
        self.timeout = int(os.getenv('TIMEOUT', '10'))
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'
        
        # Feature flags
        self.enable_time_functions = os.getenv('ENABLE_TIME_FUNCTIONS', 'true').lower() == 'true'
        self.enable_location_functions = os.getenv('ENABLE_LOCATION_FUNCTIONS', 'true').lower() == 'true'
        
        # Validate configuration
        if not self.openai_client.api_key:
            raise ValueError("OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file.")
        
        if not self.weather_api_key:
            raise ValueError("Weather API key not configured. Please set WEATHER_API_KEY in your .env file.")
        
        # Define available functions for OpenAI
        self.functions = self._build_function_definitions()
    
    def _build_function_definitions(self) -> List[Dict]:
        """Build function definitions based on enabled features."""
        functions = [
            {
                "name": "get_current_weather",
                "description": "Get the current weather information for a specific city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The city name, e.g., London, New York, Tokyo"
                        },
                        "country": {
                            "type": "string",
                            "description": "Optional country code for more specific results, e.g., US, UK, JP"
                        },
                        "units": {
                            "type": "string",
                            "enum": ["metric", "imperial", "standard"],
                            "description": "Temperature units to use (metric for Celsius, imperial for Fahrenheit)"
                        }
                    },
                    "required": ["city"]
                }
            }
        ]
        
        if self.enable_time_functions:
            functions.extend([
                {
                    "name": "get_current_time",
                    "description": "Get the current date and time",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "timezone": {
                                "type": "string",
                                "description": "Optional timezone (e.g., 'UTC', 'US/Eastern', 'Europe/London')"
                            },
                            "format": {
                                "type": "string",
                                "enum": ["full", "date", "time", "timestamp"],
                                "description": "Format of the time output"
                            }
                        },
                        "required": []
                    }
                },
                {
                    "name": "get_timezone_info",
                    "description": "Get timezone information for a specific city or location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City name or location to get timezone for"
                            }
                        },
                        "required": ["location"]
                    }
                }
            ])
        
        if self.enable_location_functions:
            functions.extend([
                {
                    "name": "get_my_location",
                    "description": "Get the user's current approximate location based on IP address",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                },
                {
                    "name": "get_location_info",
                    "description": "Get detailed information about a specific location (coordinates, country, etc.)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City name or address to get information for"
                            }
                        },
                        "required": ["location"]
                    }
                }
            ])
        
        return functions
    
    def process_user_query(self, user_input: str) -> str:
        """
        Process user input using OpenAI with function calling capabilities.
        
        Args:
            user_input (str): User's natural language query
            
        Returns:
            str: Formatted response from the assistant
        """
        try:
            # Create the initial conversation with function calling
            messages = [
                {
                    "role": "system",
                    "content": f"""You are a helpful multi-tool assistant. You have access to several functions:

WEATHER: Use get_current_weather to provide weather information for any city.
{'TIME: Use get_current_time and get_timezone_info for time-related queries.' if self.enable_time_functions else ''}
{'LOCATION: Use get_my_location and get_location_info for location-related queries.' if self.enable_location_functions else ''}

When users ask questions, determine which tool(s) would be most helpful and use them appropriately.
Always provide helpful, conversational responses. If users ask about something you can't help with, 
politely explain your capabilities.

Current model: {self.model}
Available functions: {', '.join([f['name'] for f in self.functions])}"""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
            
            if self.debug:
                print(f"Using model: {self.model}")
                print(f"Temperature: {self.temperature}")
                print(f"Max tokens: {self.max_tokens}")
            
            # Make the initial request with function calling
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                functions=self.functions,
                function_call="auto",
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            message = response.choices[0].message
            
            # Check if OpenAI wants to call a function
            if message.function_call:
                return self._handle_function_call(message, messages)
            else:
                # Direct response without function call
                return message.content
                
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."
    
    def _handle_function_call(self, message: Any, messages: List[Dict]) -> str:
        """
        Handle function call from OpenAI and return the final response.
        
        Args:
            message: OpenAI message with function call
            messages: Conversation history
            
        Returns:
            str: Final assistant response
        """
        try:
            function_name = message.function_call.name
            function_args = json.loads(message.function_call.arguments)
            
            if self.debug:
                print(f"Calling function: {function_name}")
                print(f"Arguments: {function_args}")
            
            # Execute the appropriate function
            if function_name == "get_current_weather":
                function_result = self._get_current_weather(**function_args)
            elif function_name == "get_current_time":
                function_result = self._get_current_time(**function_args)
            elif function_name == "get_timezone_info":
                function_result = self._get_timezone_info(**function_args)
            elif function_name == "get_my_location":
                function_result = self._get_my_location()
            elif function_name == "get_location_info":
                function_result = self._get_location_info(**function_args)
            else:
                function_result = {"error": f"Unknown function: {function_name}"}
            
            # Add the assistant's function call to the conversation
            messages.append({
                "role": "assistant",
                "content": None,
                "function_call": {
                    "name": function_name,
                    "arguments": message.function_call.arguments
                }
            })
            
            # Add the function result to the conversation
            messages.append({
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_result)
            })
            
            # Get the final response from OpenAI
            final_response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return final_response.choices[0].message.content
            
        except Exception as e:
            return f"I had trouble processing that request: {str(e)}. Please try again."
    
    def _get_current_weather(self, city: str, country: Optional[str] = None, units: Optional[str] = None) -> Dict:
        """
        Function that gets called by OpenAI to fetch weather data.
        
        Args:
            city (str): City name
            country (Optional[str]): Country code
            units (Optional[str]): Temperature units
            
        Returns:
            Dict: Weather data or error information
        """
        try:
            # Prepare query parameter
            query = city
            if country:
                query = f"{city},{country}"
            
            # Use provided units or default
            units = units or self.default_units
            
            # Prepare request parameters
            params = {
                'q': query,
                'appid': self.weather_api_key,
                'units': units
            }
            
            # Make API request
            response = requests.get(
                f"{self.base_url}/weather",
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Format the data for OpenAI to use
                return {
                    "success": True,
                    "city": data.get("name"),
                    "country": data.get("sys", {}).get("country"),
                    "temperature": data.get("main", {}).get("temp"),
                    "feels_like": data.get("main", {}).get("feels_like"),
                    "humidity": data.get("main", {}).get("humidity"),
                    "pressure": data.get("main", {}).get("pressure"),
                    "description": data.get("weather", [{}])[0].get("description"),
                    "wind_speed": data.get("wind", {}).get("speed"),
                    "visibility": data.get("visibility"),
                    "units": units
                }
            else:
                error_data = response.json() if response.content else {}
                return {
                    "success": False,
                    "error": f"Weather API error: {error_data.get('message', 'Unknown error')}",
                    "status_code": response.status_code
                }
                
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Unable to connect to weather service. Please check your internet connection."
            }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Weather service request timed out. Please try again."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def _get_current_time(self, timezone: Optional[str] = None, format: str = "full") -> Dict:
        """
        Get current time information.
        
        Args:
            timezone (Optional[str]): Timezone to use
            format (str): Format of output
            
        Returns:
            Dict: Time information
        """
        try:
            import pytz
            
            # Get current time
            if timezone:
                try:
                    tz = pytz.timezone(timezone)
                    current_time = datetime.datetime.now(tz)
                except pytz.exceptions.UnknownTimeZoneError:
                    # Fallback to UTC if timezone is invalid
                    current_time = datetime.datetime.utcnow()
                    timezone = "UTC (fallback - invalid timezone provided)"
            else:
                current_time = datetime.datetime.now()
                timezone = "Local"
            
            # Format based on request
            if format == "date":
                formatted_time = current_time.strftime("%Y-%m-%d")
            elif format == "time":
                formatted_time = current_time.strftime("%H:%M:%S")
            elif format == "timestamp":
                formatted_time = current_time.isoformat()
            else:  # full
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            
            return {
                "success": True,
                "current_time": formatted_time,
                "timezone": timezone,
                "day_of_week": current_time.strftime("%A"),
                "unix_timestamp": int(current_time.timestamp())
            }
            
        except ImportError:
            # Fallback if pytz is not available
            current_time = datetime.datetime.now()
            return {
                "success": True,
                "current_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "timezone": "Local (pytz not available)",
                "day_of_week": current_time.strftime("%A"),
                "unix_timestamp": int(current_time.timestamp())
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Time error: {str(e)}"
            }
    
    def _get_timezone_info(self, location: str) -> Dict:
        """
        Get timezone information for a location.
        
        Args:
            location (str): Location to get timezone for
            
        Returns:
            Dict: Timezone information
        """
        try:
            # Use geocoder to get location info
            g = geocoder.osm(location)
            
            if g.ok:
                # Try to get timezone from coordinates (basic approximation)
                lat, lng = g.latlng
                
                # Simple timezone estimation based on longitude
                # This is a rough approximation - in production, use a proper timezone API
                utc_offset = int(lng / 15)  # Rough estimation
                
                return {
                    "success": True,
                    "location": g.address,
                    "coordinates": {"latitude": lat, "longitude": lng},
                    "estimated_utc_offset": utc_offset,
                    "note": "This is a rough timezone estimation based on longitude"
                }
            else:
                return {
                    "success": False,
                    "error": f"Could not find location: {location}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Timezone lookup error: {str(e)}"
            }
    
    def _get_my_location(self) -> Dict:
        """
        Get user's current location based on IP address.
        
        Returns:
            Dict: Location information
        """
        try:
            # Get location based on IP
            g = geocoder.ip('me')
            
            if g.ok:
                return {
                    "success": True,
                    "city": g.city,
                    "region": g.state,
                    "country": g.country,
                    "coordinates": {"latitude": g.latlng[0], "longitude": g.latlng[1]},
                    "ip_address": g.ip,
                    "note": "Location determined by IP address (approximate)"
                }
            else:
                return {
                    "success": False,
                    "error": "Could not determine location from IP address"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Location detection error: {str(e)}"
            }
    
    def _get_location_info(self, location: str) -> Dict:
        """
        Get detailed information about a specific location.
        
        Args:
            location (str): Location to get information for
            
        Returns:
            Dict: Location information
        """
        try:
            # Use geocoder to get detailed location info
            g = geocoder.osm(location)
            
            if g.ok:
                return {
                    "success": True,
                    "address": g.address,
                    "city": g.city,
                    "state": g.state,
                    "country": g.country,
                    "postal_code": g.postal,
                    "coordinates": {
                        "latitude": g.latlng[0],
                        "longitude": g.latlng[1]
                    },
                    "bbox": g.bbox  # Bounding box
                }
            else:
                return {
                    "success": False,
                    "error": f"Could not find detailed information for: {location}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Location info error: {str(e)}"
            }
    
    def test_connection(self) -> Dict:
        """
        Test all API connections and function availability.
        
        Returns:
            Dict: Connection test results
        """
        results = {
            "openai": {"success": False, "message": ""},
            "weather_api": {"success": False, "message": ""},
            "location_services": {"success": False, "message": ""},
            "configuration": {
                "model": self.model,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "functions_enabled": len(self.functions)
            }
        }
        
        # Test OpenAI connection
        try:
            test_response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            results["openai"] = {
                "success": True,
                "message": f"OpenAI API connection successful (model: {self.model})"
            }
        except Exception as e:
            results["openai"] = {
                "success": False,
                "message": f"OpenAI API connection failed: {str(e)}"
            }
        
        # Test Weather API connection
        try:
            weather_result = self._get_current_weather("London")
            if weather_result.get("success"):
                results["weather_api"] = {
                    "success": True,
                    "message": "Weather API connection successful"
                }
            else:
                results["weather_api"] = {
                    "success": False,
                    "message": f"Weather API connection failed: {weather_result.get('error')}"
                }
        except Exception as e:
            results["weather_api"] = {
                "success": False,
                "message": f"Weather API connection failed: {str(e)}"
            }
        
        # Test location services
        try:
            location_result = self._get_my_location()
            if location_result.get("success"):
                results["location_services"] = {
                    "success": True,
                    "message": "Location services working"
                }
            else:
                results["location_services"] = {
                    "success": False,
                    "message": f"Location services failed: {location_result.get('error')}"
                }
        except Exception as e:
            results["location_services"] = {
                "success": False,
                "message": f"Location services failed: {str(e)}"
            }
        
        return results
    
    def get_config_info(self) -> Dict:
        """
        Get current configuration information.
        
        Returns:
            Dict: Configuration details
        """
        return {
            "openai_model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "weather_units": self.default_units,
            "timeout": self.timeout,
            "debug_mode": self.debug,
            "enabled_functions": {
                "weather": True,
                "time": self.enable_time_functions,
                "location": self.enable_location_functions
            },
            "total_functions": len(self.functions)
        }


# Example usage and testing
if __name__ == "__main__":
    try:
        assistant = MultiToolAssistant()
        
        print("Multi-Tool OpenAI Assistant Test")
        print("=" * 40)
        
        # Show configuration
        config = assistant.get_config_info()
        print(f"Model: {config['openai_model']}")
        print(f"Temperature: {config['temperature']}")
        print(f"Enabled functions: {config['total_functions']}")
        print()
        
        # Test connections
        print("Testing API connections...")
        test_results = assistant.test_connection()
        
        for service, result in test_results.items():
            if service != "configuration":
                status = "✓" if result["success"] else "✗"
                print(f"{status} {service.replace('_', ' ').title()}: {result['message']}")
        
        print("\nTesting multi-tool queries...")
        
        # Test various types of queries
        test_queries = [
            "What's the weather in London?",
            "What time is it?",
            "Where am I?",
            "What's the weather like where I am?",
        ]
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            response = assistant.process_user_query(query)
            print(f"Response: {response}")
            
    except Exception as e:
        print(f"Error initializing assistant: {e}")
        print("Please check your .env configuration.")