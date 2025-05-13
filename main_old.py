"""
Main application entry point for the Multi-Tool OpenAI Assistant.

This module provides the command-line interface for an AI assistant that
demonstrates OpenAI's function calling capabilities with multiple external APIs.
"""

import sys
import os
from openai_assistant import MultiToolAssistant


class MultiToolChatBot:
    """Main application class for the multi-tool OpenAI assistant."""
    
    def __init__(self):
        """Initialize the chat bot with OpenAI assistant."""
        try:
            self.assistant = MultiToolAssistant()
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
        config = self.assistant.get_config_info()
        print("🤖 Welcome to the Multi-Tool OpenAI Assistant!")
        print("This assistant demonstrates OpenAI Function Calling with multiple APIs.")
        print(f"Model: {config['openai_model']} | Functions: {config['total_functions']} available")
        print("\nI can help you with:")
        print("🌤️  Weather information for any city")
        if config['enabled_functions']['time']:
            print("⏰ Current time and timezone information")
        if config['enabled_functions']['location']:
            print("📍 Location detection and geographic information")
        print("\nType 'help' for examples or 'quit' to exit.\n")
        
        # Test API connections
        print("Testing API connections...")
        connection_tests = self.assistant.test_connection()
        
        all_connected = True
        for service, result in connection_tests.items():
            if service != "configuration":
                status = "✅" if result["success"] else "❌"
                print(f"{status} {service.replace('_', ' ').title()}: {result['message']}")
                if not result["success"]:
                    all_connected = False
        
        if not all_connected:
            print("\n⚠️  Some connections failed. Some features may not work properly.")
            print("Please check your API keys and internet connection.\n")
        else:
            print("\n🎉 All systems ready! You can start asking questions.\n")
        
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
        
        print("Thank you for using the Multi-Tool OpenAI Assistant! 🌟")
    
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
        
        elif input_lower in ['info', 'about', 'config', 'configuration']:
            self._show_config()
            return True
        
        return False
    
    def _show_help(self):
        """Display help information with examples."""
        config = self.assistant.get_config_info()
        
        help_text = f"""
🔧 Multi-Tool OpenAI Assistant Help

This assistant uses OpenAI's {config['openai_model']} with function calling to access multiple services.
You can ask questions in natural language!

🌤️ Weather queries:
• "What's the weather like in London?"
• "How's the weather in New York today?"
• "Is it raining in Paris?"
• "What's the temperature in Tokyo?"
"""

        if config['enabled_functions']['time']:
            help_text += """
⏰ Time & timezone queries:
• "What time is it?"
• "What time is it in London?"
• "What's the current date?"
• "What timezone is New York in?"
"""

        if config['enabled_functions']['location']:
            help_text += """
📍 Location queries:
• "Where am I?"
• "What's my current location?"
• "Tell me about Paris, France"
• "What are the coordinates of Tokyo?"
"""

        help_text += """
🔗 Combined queries:
• "What's the weather like where I am?"
• "What time is it in London and what's the weather there?"

Special commands:
• 'help' or 'h' - Show this help message
• 'test' - Test API connections
• 'config' - Show current configuration
• 'quit' or 'q' - Exit the assistant

💡 Tip: Ask questions naturally! The AI will determine which tools to use.
        """
        print(help_text)
    
    def _test_connections(self):
        """Test and display API connection status."""
        print("🔍 Testing API connections...\n")
        
        results = self.assistant.test_connection()
        
        for service, result in results.items():
            if service != "configuration":
                status = "✅ Connected" if result["success"] else "❌ Failed"
                print(f"{service.replace('_', ' ').title()}: {status}")
                print(f"   Message: {result['message']}\n")
        
        # Show configuration
        config = results.get("configuration", {})
        print("Current Configuration:")
        print(f"   Model: {config.get('model', 'Unknown')}")
        print(f"   Temperature: {config.get('temperature', 'Unknown')}")
        print(f"   Max Tokens: {config.get('max_tokens', 'Unknown')}")
        print(f"   Functions Available: {config.get('functions_enabled', 'Unknown')}")
    
    def _show_config(self):
        """Display current configuration."""
        config = self.assistant.get_config_info()
        
        print("🔧 Current Configuration:")
        print(f"   OpenAI Model: {config['openai_model']}")
        print(f"   Temperature: {config['temperature']}")
        print(f"   Max Tokens: {config['max_tokens']}")
        print(f"   Weather Units: {config['weather_units']}")
        print(f"   Timeout: {config['timeout']}s")
        print(f"   Debug Mode: {'On' if config['debug_mode'] else 'Off'}")
        print()
        print("🔧 Enabled Functions:")
        for func_type, enabled in config['enabled_functions'].items():
            status = "✅ Enabled" if enabled else "❌ Disabled"
            print(f"   {func_type.title()}: {status}")
        print(f"\nTotal Functions Available: {config['total_functions']}")
        print("\n💡 You can modify these settings in your .env file!")
    
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
        chatbot = MultiToolChatBot()
        chatbot.start()
    except Exception as e:
        print(f"Failed to start the Multi-Tool OpenAI Assistant: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()