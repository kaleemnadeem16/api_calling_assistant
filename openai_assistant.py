"""
OpenAI-powered assistant with function calling capabilities for weather data.

This module demonstrates OpenAI's function calling feature by integrating
with external APIs based on user queries processed by GPT models.
"""

import os
import json
from typing import Dict, List, Optional, Any
from openai import OpenAI
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()


class OpenAIAssistant:
    """OpenAI-powered assistant with function calling capabilities."""
    
    def __init__(self):
        """Initialize the OpenAI assistant with API credentials and function definitions."""
        self.openai_client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        self.base_url = os.getenv('API_BASE_URL', 'https://api.openweathermap.org/data/2.5')
        self.default_units = os.getenv('DEFAULT_UNITS', 'metric')
        self.timeout = int(os.getenv('TIMEOUT', '10'))
        
        # Validate configuration
        if not self.openai_client.api_key:
            raise ValueError("OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file.")
        
        if not self.weather_api_key:
            raise ValueError("Weather API key not configured. Please set WEATHER_API_KEY in your .env file.")
        
        # Define available functions for OpenAI
        self.functions = [
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
                    "content": """You are a helpful weather assistant. You can provide current weather information for any city worldwide. 
                    
When users ask about weather, use the get_current_weather function to fetch real-time data. 
Always provide helpful, conversational responses with the weather information.

If users ask about things other than weather, politely explain that you specialize in weather information."""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
            
            # Make the initial request with function calling
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",  # Available in May 2024
                messages=messages,
                functions=self.functions,
                function_call="auto",
                temperature=0.7,
                max_tokens=500
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
            
            # Execute the function
            if function_name == "get_current_weather":
                function_result = self._get_current_weather(**function_args)
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
                model="gpt-4-turbo-preview",
                messages=messages,
                temperature=0.7,
                max_tokens=300
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
    
    def test_connection(self) -> Dict:
        """
        Test both OpenAI and weather API connections.
        
        Returns:
            Dict: Connection test results
        """
        results = {
            "openai": {"success": False, "message": ""},
            "weather_api": {"success": False, "message": ""}
        }
        
        # Test OpenAI connection
        try:
            test_response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            results["openai"] = {
                "success": True,
                "message": "OpenAI API connection successful"
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
        
        return results


# Example usage and testing
if __name__ == "__main__":
    try:
        assistant = OpenAIAssistant()
        
        print("OpenAI Weather Assistant Test")
        print("=" * 40)
        
        # Test connections
        print("Testing API connections...")
        test_results = assistant.test_connection()
        
        for api, result in test_results.items():
            status = "✓" if result["success"] else "✗"
            print(f"{status} {api.replace('_', ' ').title()}: {result['message']}")
        
        print("\nTesting weather queries...")
        
        # Test some queries
        test_queries = [
            "What's the weather in London?",
            "How's the weather in Tokyo today?",
            "Tell me about the weather in New York",
        ]
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            response = assistant.process_user_query(query)
            print(f"Response: {response}")
            
    except Exception as e:
        print(f"Error initializing assistant: {e}")
        print("Please check your .env configuration.")