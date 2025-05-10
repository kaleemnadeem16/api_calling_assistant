"""
Main application entry point for the OpenAI API Calling Assistant.

This module provides the command-line interface for an AI assistant that
demonstrates OpenAI's function calling capabilities with external APIs.
"""

import sys
import os
from openai_assistant import OpenAIAssistant


class WeatherChatBot:
    """Main application class for the OpenAI-powered weather assistant."""
    
    def __init__(self):
        """Initialize the chat bot with OpenAI assistant."""
        try:
            self.assistant = OpenAIAssistant()
            self.is_running = False
            
        except ValueError as e:
            print(f"Configuration Error: {e}")
            print("\nPlease ensure you have:")
            print("1. Copied .env.example to .env")
            print("2. Added your OpenAI API key to OPENAI_API_KEY in the .env file")
            print("3. Added your OpenWeatherMap API key to WEATHER_API_KEY in the .env file")
            print("4. Installed required dependencies: pip install -r requirements.txt")
            sys.exit(1)
        except Exception as e:
            print(f"Initialization Error: {e}")
            sys.exit(1)
    
    def start(self):
        """Start the interactive command-line interface."""
        self.is_running = True
        
        # Display welcome message
        print("🌤️  Welcome to the OpenAI Weather Assistant!")
        print("This assistant demonstrates OpenAI Function Calling with external APIs.")
        print("Ask me about the weather in any city around the world!")
        print("Type 'help' for examples or 'quit' to exit.\n")
        
        # Test API connections
        print("Testing API connections...")
        connection_tests = self.assistant.test_connection()
        
        all_connected = True
        for api, result in connection_tests.items():
            status = "✅" if result["success"] else "❌"
            print(f"{status} {api.replace('_', ' ').title()}: {result['message']}")
            if not result["success"]:
                all_connected = False
        
        if not all_connected:
            print("\n⚠️  Some connections failed. The assistant may not work properly.")
            print("Please check your API keys and internet connection.\n")
        else:
            print("\n🎉 All systems ready! You can start asking about weather.\n")
        
        # Main interaction loop
        while self.is_running:
            try:
                self._handle_user_interaction()
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print("Please try again or type 'quit' to exit.")
        
        print("Thank you for using the OpenAI Weather Assistant! 🌟")
    
    def _handle_user_interaction(self):
        """Handle a single user interaction cycle."""
        # Get user input
        user_input = input("🗣️  You: ").strip()
        
        if not user_input:
            return
        
        # Check for special commands
        if self._handle_special_commands(user_input):
            return
        
        # Process with OpenAI assistant
        print("🤖 Assistant: ", end="", flush=True)
        response = self.assistant.process_user_query(user_input)
        print(response)
        print()  # Add spacing between interactions
    
    def _handle_special_commands(self, user_input: str) -> bool:
        """
        Handle special commands like help, quit, etc.
        
        Args:
            user_input (str): User input to check for special commands
            
        Returns:
            bool: True if a special command was handled
        """
        input_lower = user_input.lower().strip()
        
        if input_lower in ['quit', 'exit', 'q', 'bye']:
            self.is_running = False
            return True
        
        elif input_lower in ['help', 'h', '?']:
            self._show_help()
            return True
        
        elif input_lower in ['test', 'test connection', 'status']:
            self._test_connections()
            return True
        
        elif input_lower in ['info', 'about']:
            self._show_info()
            return True
        
        return False
    
    def _show_help(self):
        """Display help information with examples."""
        help_text = """
🔧 OpenAI Weather Assistant Help

This assistant uses OpenAI's GPT-4 with function calling to fetch weather data.
You can ask about weather in natural language!

Example queries:
• "What's the weather like in London?"
• "How's the weather in New York today?"
• "Tell me about the weather in Tokyo"
• "Is it raining in Paris?"
• "What's the temperature in Sydney?"
• "Weather forecast for Berlin"

Special commands:
• 'help' or 'h' - Show this help message
• 'test' - Test API connections
• 'info' - Show technical information
• 'quit' or 'q' - Exit the assistant

💡 Tip: You can ask about weather in any way that feels natural to you!
The AI will understand your intent and call the appropriate weather API.
        """
        print(help_text)
    
    def _test_connections(self):
        """Test and display API connection status."""
        print("🔍 Testing API connections...\n")
        
        results = self.assistant.test_connection()
        
        for api, result in results.items():
            status = "✅ Connected" if result["success"] else "❌ Failed"
            print(f"{api.replace('_', ' ').title()}: {status}")
            print(f"   Message: {result['message']}\n")
    
    def _show_info(self):
        """Display technical information about the assistant."""
        info_text = """
🤖 OpenAI Weather Assistant - Technical Info

This assistant demonstrates:
• OpenAI Function Calling - AI decides when to call external APIs
• GPT-4 Turbo integration for natural language understanding  
• Weather API integration through function calls
• Real-time weather data from OpenWeatherMap

Architecture:
1. User asks a question in natural language
2. OpenAI GPT-4 processes the query and decides if weather data is needed
3. If needed, GPT-4 calls the get_current_weather function
4. The function fetches real-time data from OpenWeatherMap API
5. GPT-4 formats the data into a natural, conversational response

This showcases the power of AI-driven API orchestration!
        """
        print(info_text)
    
    def process_single_query(self, query: str) -> str:
        """
        Process a single query and return the response.
        
        This method is useful for programmatic access or testing.
        
        Args:
            query (str): User query to process
            
        Returns:
            str: Assistant's response
        """
        try:
            return self.assistant.process_user_query(query)
        except Exception as e:
            return f"An error occurred while processing your query: {str(e)}"


def main():
    """Main entry point for the application."""
    try:
        chatbot = WeatherChatBot()
        chatbot.start()
    except Exception as e:
        print(f"Failed to start the OpenAI Weather Assistant: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()