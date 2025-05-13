#!/usr/bin/env python3
"""
LangChain API Calling Assistant - Main CLI Interface

A command-line interface for demonstrating LangChain's tool calling capabilities
with multiple external APIs including weather, time, and location services.
"""

import os
import sys
import json
from typing import Dict, Any, List

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openai_assistant import LangChainToolAssistant
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def print_banner():
    """Print the application banner."""
    print("=" * 60)
    print("   LangChain API Calling Assistant")
    print("   Demonstrating Tool Calling with Multiple APIs")
    print("=" * 60)
    print()


def print_help():
    """Print help information."""
    help_text = """
Available Commands:
  help, h, ?           - Show this help message
  quit, exit, q        - Exit the application
  clear, cls           - Clear the screen
  config, settings     - Show current configuration
  capabilities, caps   - Show available tools and capabilities
  test                 - Run connection tests
  
Usage Examples:
  "What's the weather in Tokyo?"
  "What time is it in New York?"
  "Where am I?"
  "Tell me about the weather where I am"
  "What's the current time?"
  "Get location info for Paris, France"

Features:
  - Weather information for any city worldwide
  - Current time with timezone support
  - Location detection and information lookup
  - Conversational interface with context awareness
  - Powered by LangChain's tool calling framework
"""
    print(help_text)


def format_response(response: Dict[str, Any]) -> str:
    """Format the assistant response for display."""
    if not response.get("success", False):
        return f"❌ Error: {response.get('error', 'Unknown error occurred')}"
    
    output = f"🤖 {response.get('response', 'No response')}"
    
    # Add debug information if available
    if response.get("tools_used"):
        tools_info = []
        for tool in response["tools_used"]:
            tools_info.append(f"  • {tool.get('function', 'Unknown tool')}")
        
        if tools_info:
            output += f"\n\n🔧 Tools used:\n" + "\n".join(tools_info)
    
    return output


def handle_command(command: str, assistant: LangChainToolAssistant) -> bool:
    """
    Handle special commands. Returns True if command was handled, False otherwise.
    """
    command = command.lower().strip()
    
    if command in ['help', 'h', '?']:
        print_help()
        return True
    
    elif command in ['quit', 'exit', 'q']:
        print("👋 Goodbye!")
        return True
    
    elif command in ['clear', 'cls']:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        return True
    
    elif command in ['config', 'settings']:
        try:
            capabilities = assistant.get_available_capabilities()
            print("\n📋 Current Configuration:")
            print(f"  Model: {capabilities['model_info']['model']}")
            print(f"  Temperature: {capabilities['model_info']['temperature']}")
            print(f"  Max Tokens: {capabilities['model_info']['max_tokens']}")
            print(f"  Available Tools: {len(capabilities['tools'])}")
            print("\n🔧 Feature Flags:")
            for feature, enabled in capabilities['features'].items():
                status = "✓" if enabled else "✗"
                print(f"  {status} {feature.replace('_', ' ').title()}")
        except Exception as e:
            print(f"❌ Error getting configuration: {e}")
        return True
    
    elif command in ['capabilities', 'caps']:
        try:
            capabilities = assistant.get_available_capabilities()
            print("\n🛠️  Available Tools:")
            for tool in capabilities['tools']:
                print(f"  • {tool['name']}: {tool['description']}")
            
            print(f"\n📊 Total Tools: {len(capabilities['tools'])}")
        except Exception as e:
            print(f"❌ Error getting capabilities: {e}")
        return True
    
    elif command == 'test':
        print("\n🧪 Testing LangChain tool calling...")
        test_queries = [
            "What's the weather in London?",
            "What time is it?",
        ]
        
        for query in test_queries:
            print(f"\nTesting: {query}")
            try:
                response = assistant.chat(query)
                if response.get("success"):
                    print(f"✓ Success: {response['response'][:100]}...")
                else:
                    print(f"✗ Failed: {response.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"✗ Error: {e}")
        return True
    
    return False


def main():
    """Main application loop."""
    try:
        # Initialize the assistant
        print("🚀 Initializing LangChain Tool Assistant...")
        assistant = LangChainToolAssistant()
        
        # Clear screen and show banner
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        
        # Show initial information
        capabilities = assistant.get_available_capabilities()
        print(f"✅ Assistant initialized successfully!")
        print(f"📋 Model: {capabilities['model_info']['model']}")
        print(f"🔧 Tools available: {len(capabilities['tools'])}")
        print(f"\nType 'help' for usage instructions or 'quit' to exit.\n")
        
        # Conversation history for context
        conversation_history = []
        
        # Main conversation loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if handle_command(user_input, assistant):
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        break
                    continue
                
                # Process with assistant
                print("🤔 Thinking...")
                response = assistant.chat(user_input, conversation_history)
                
                # Display response
                print(format_response(response))
                print()
                
                # Update conversation history
                conversation_history.append({
                    "role": "user",
                    "content": user_input
                })
                
                if response.get("success"):
                    conversation_history.append({
                        "role": "assistant", 
                        "content": response.get("response", "")
                    })
                
                # Keep conversation history manageable
                if len(conversation_history) > 10:
                    conversation_history = conversation_history[-8:]
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An unexpected error occurred: {e}")
                print("Please try again or type 'quit' to exit.\n")
    
    except Exception as e:
        print(f"❌ Failed to initialize assistant: {e}")
        print("\n💡 Troubleshooting:")
        print("  1. Check your .env file configuration")
        print("  2. Ensure you have valid API keys")
        print("  3. Check your internet connection")
        print("  4. Install required dependencies: pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()