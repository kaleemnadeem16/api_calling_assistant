# LangChain API Calling Assistant

A Python-based AI assistant that demonstrates **LangChain Tool Calling** capabilities by integrating with multiple external APIs. This project showcases how to use LangChain agents with OpenAI models to intelligently call external tools and services based on natural language queries.

## 🌟 Features

- **LangChain Tool Calling**: Uses LangChain agents with OpenAI models to determine when and how to call external tools
- **Multi-Tool Integration**: Weather data, time services, and location detection through intelligent tool selection
- **Intelligent Query Processing**: Natural language understanding powered by OpenAI via LangChain
- **Real-time Data**: Integrates with OpenWeatherMap API, timezone services, and location APIs
- **Agent-based Architecture**: LangChain agent orchestration for complex multi-tool workflows
- **Error Handling**: Graceful handling of both AI and API errors
- **Command-line Interface**: Interactive terminal-based experience
- **Secure Configuration**: Environment-based API key management for all services

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key (from [platform.openai.com](https://platform.openai.com/api-keys))
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org/api))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kaleemnadeem16/api_calling_assistant.git
   cd api_calling_assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your API keys**
   
   **OpenAI API Key:**
   - Visit [platform.openai.com](https://platform.openai.com/api-keys)
   - Sign up or log in to your OpenAI account
   - Create a new API key
   - Copy the key (starts with 'sk-')
   
   **OpenWeatherMap API Key:**
   - Visit [openweathermap.org](https://openweathermap.org/api)
   - Sign up for a free account
   - Go to "API keys" section
   - Copy your API key

4. **Configure environment**
   - Open the `.env` file in the project root
   - Replace the placeholder values with your actual API keys:
   
   ```env
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo
   OPENAI_TEMPERATURE=0.7
   OPENAI_MAX_TOKENS=500
   
   # Weather API Configuration
   WEATHER_API_KEY=your_openweathermap_api_key_here
   API_BASE_URL=https://api.openweathermap.org/data/2.5
   DEFAULT_UNITS=metric
   
   # Feature Flags
   ENABLE_TIME_FUNCTIONS=true
   ENABLE_LOCATION_FUNCTIONS=true
   
   # Debug and Development
   DEBUG=false
   TIMEOUT=10
   ```

5. **Run the assistant**
   ```bash
   python main.py
   ```

## 🛠️ Usage Examples

### Weather Queries
```
You: What's the weather like in London?
🤖: The current weather in London, UK is partly cloudy with a temperature of 15°C...

You: Is it raining in Tokyo?
🤖: Let me check the current weather in Tokyo... No, it's currently clear with 22°C...
```

### Time and Location Queries
```
You: What time is it?
🤖: The current time is 2024-01-15 14:30:25 (Local timezone)...

You: Where am I?
🤖: Based on your IP address, you appear to be in New York, NY, United States...

You: What's the weather like where I am?
🤖: Let me detect your location first... You're in New York, NY. The current weather there is...
```

### Complex Multi-Tool Queries
```
You: I'm planning to go outside. Can you tell me the weather where I am and what time it is?
🤖: I'll help you with that! Let me check your location, the weather, and current time...
```

## 🏗️ Architecture

### LangChain Integration
- **Agent Executor**: Orchestrates tool selection and execution
- **OpenAI Tools Agent**: Uses OpenAI models for decision making
- **Custom Tools**: Weather, time, and location tools built with LangChain BaseTool
- **Memory Management**: Conversation buffer for context awareness

### Available Tools

1. **WeatherTool**: Get current weather information for any city
2. **TimeTool**: Get current time with timezone support
3. **MyLocationTool**: Detect user's current location via IP
4. **LocationInfoTool**: Get detailed information about specific locations

### Tool Calling Flow
```
User Query → LangChain Agent → Tool Selection → Tool Execution → Response Generation
```

## 📁 Project Structure

```
api_calling_assistant/
├── main.py                    # Main CLI application
├── openai_assistant.py        # LangChain assistant with tool definitions
├── test_assistant.py          # Comprehensive test suite
├── requirements.txt           # Python dependencies
├── .env.example              # Environment configuration template
├── .env                      # Your actual environment configuration
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
├── README.md               # This file
└── docs/                   # Documentation (local only)
    ├── project_overview.md
    ├── development_rules.md
    └── architecture.md
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | - | Yes |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-3.5-turbo` | No |
| `OPENAI_TEMPERATURE` | Model temperature (0-1) | `0.7` | No |
| `OPENAI_MAX_TOKENS` | Maximum response tokens | `500` | No |
| `WEATHER_API_KEY` | OpenWeatherMap API key | - | Yes |
| `API_BASE_URL` | Weather API base URL | OpenWeatherMap | No |
| `DEFAULT_UNITS` | Temperature units | `metric` | No |
| `ENABLE_TIME_FUNCTIONS` | Enable time tools | `true` | No |
| `ENABLE_LOCATION_FUNCTIONS` | Enable location tools | `true` | No |
| `DEBUG` | Enable debug mode | `false` | No |
| `TIMEOUT` | API timeout seconds | `10` | No |

### Model Options
- `gpt-3.5-turbo` (recommended for cost efficiency)
- `gpt-4` (for enhanced capabilities)
- `gpt-4-turbo-preview` (latest features)

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_assistant.py
```

The test suite includes:
- Initialization tests
- Tool calling functionality
- Error handling
- Response formatting
- LangChain agent behavior

## 🐛 Troubleshooting

### Common Issues

1. **"OpenAI API key not configured"**
   - Ensure `OPENAI_API_KEY` is set in your `.env` file
   - Verify the key is valid and has credits

2. **"Weather API key not configured"**
   - Ensure `WEATHER_API_KEY` is set in your `.env` file
   - Verify the key is active on OpenWeatherMap

3. **"ModuleNotFoundError: No module named 'langchain'"**
   - Run `pip install -r requirements.txt`
   - Ensure you're using the correct Python environment

4. **Tool calling not working**
   - Check your OpenAI API key has access to function calling
   - Verify the model supports tool calling (gpt-3.5-turbo or gpt-4)
   - Enable debug mode: `DEBUG=true` in `.env`

5. **Location detection issues**
   - Location detection uses IP geolocation (approximate)
   - May not work accurately with VPNs or corporate networks
   - Try specific location queries instead

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and test thoroughly
4. Commit with clear messages: `git commit -m "Add: new feature description"`
5. Push to your fork: `git push origin feature/your-feature`
6. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain** for the excellent tool calling framework
- **OpenAI** for the powerful GPT models and function calling capabilities
- **OpenWeatherMap** for providing free weather data API
- **Python Community** for the amazing ecosystem of libraries

## 🔗 Links

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Project Repository](https://github.com/kaleemnadeem16/api_calling_assistant)

---

**Happy Coding! 🚀**

*This project demonstrates the power of LangChain's tool calling capabilities for building intelligent, multi-service AI assistants.*