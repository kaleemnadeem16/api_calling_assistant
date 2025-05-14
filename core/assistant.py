"""
LangChain Tool Assistant - Main Assistant Class

This module contains the core LangChain-powered assistant that orchestrates
multiple tools for weather, time, and location services.
"""

import os
from typing import Dict, List, Optional, Any
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseMessage
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# Import tools
from tools import WeatherTool, TimeTool, MyLocationTool, LocationInfoTool

# Load environment variables
load_dotenv()


class LangChainToolAssistant:
    """LangChain-powered assistant with multiple tool calling capabilities."""
    
    def __init__(self):
        """Initialize the assistant with API credentials and tools."""
        # Load configuration from environment
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4.1-nano')
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
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file.")
        
        if not self.weather_api_key:
            raise ValueError("Weather API key not configured. Please set WEATHER_API_KEY in your .env file.")
        
        # Initialize LangChain components
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            openai_api_key=self.openai_api_key
        )
        
        # Initialize tools
        self.tools = self._build_tools()
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant that can access multiple tools to provide information.
            
You have access to the following tools:
- Weather information for any city
- Current time and timezone information
- Location detection and information

Always use the appropriate tool when the user asks for specific information. Be conversational and helpful.
When using tools, provide context about what you're doing and explain the results clearly.

Current capabilities:
- Weather: Get current weather for any city worldwide
- Time: Get current time, optionally with timezone conversion
- Location: Detect user's location or get info about specific locations

If the user asks about something you can't do with your tools, politely explain what you can help with instead."""),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
        
        # Create agent
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Create agent executor with conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=self.debug,
            handle_parsing_errors=True,
            max_iterations=3
        )
    
    def _build_tools(self) -> List[BaseTool]:
        """Build the list of available tools based on enabled features."""
        tools = [WeatherTool()]
        
        if self.enable_time_functions:
            tools.append(TimeTool())
        
        if self.enable_location_functions:
            tools.extend([MyLocationTool(), LocationInfoTool()])
        
        return tools
    
    def chat(self, user_input: str, conversation_history: Optional[List[BaseMessage]] = None) -> Dict[str, Any]:
        """
        Process user input and return response using LangChain agent.
        
        Args:
            user_input: The user's message/query
            conversation_history: Optional conversation context
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            if self.debug:
                print(f"\n=== Processing User Input ===")
                print(f"Input: {user_input}")
                print(f"Available tools: {[tool.name for tool in self.tools]}")
            
            # Execute the agent
            result = self.agent_executor.invoke({"input": user_input})
            
            response = {
                "success": True,
                "response": result["output"],
                "tools_used": [],  # LangChain handles this internally
                "metadata": {
                    "model": self.model,
                    "temperature": self.temperature,
                    "tools_available": [tool.name for tool in self.tools]
                }
            }
            
            if self.debug:
                print(f"\n=== Agent Response ===")
                print(f"Response: {response['response']}")
            
            return response
            
        except Exception as e:
            error_response = {
                "success": False,
                "error": f"Assistant error: {str(e)}",
                "response": "I encountered an error while processing your request. Please try again or rephrase your question.",
                "tools_used": [],
                "metadata": {
                    "model": self.model,
                    "error_type": type(e).__name__
                }
            }
            
            if self.debug:
                print(f"\n=== Error ===")
                print(f"Error: {str(e)}")
                import traceback
                traceback.print_exc()
            
            return error_response
    
    def get_available_capabilities(self) -> Dict[str, Any]:
        """Get information about available capabilities."""
        capabilities = {
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "enabled": True
                }
                for tool in self.tools
            ],
            "model_info": {
                "model": self.model,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            },
            "features": {
                "weather": True,
                "time_functions": self.enable_time_functions,
                "location_functions": self.enable_location_functions
            }
        }
        
        return capabilities