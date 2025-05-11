# API Calling Assistant

A Python-based AI assistant that demonstrates **OpenAI Function Calling** capabilities by integrating with external APIs. This project showcases how to use OpenAI's GPT models to intelligently call external APIs (OpenWeatherMap) based on natural language queries.

## 🌟 Features

- **OpenAI Function Calling**: Uses GPT-4 with function calling to determine when and how to call external APIs
- **Intelligent Query Processing**: Natural language understanding powered by OpenAI
- **Real-time Weather Data**: Integrates with OpenWeatherMap API through function calls
- **Error Handling**: Graceful handling of both AI and API errors
- **Command-line Interface**: Interactive terminal-based experience
- **Secure Configuration**: Environment-based API key management for both OpenAI and weather services

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
     ```
     OPENAI_API_KEY=sk-your_actual_openai_key_here
     WEATHER_API_KEY=your_actual_weather_key_here
     ```

5. **Run the assistant**
   ```bash
   python main.py
   ```

## 💬 Usage

Experience OpenAI Function Calling in action:

```
🌤️  Welcome to the OpenAI Weather Assistant!
This assistant demonstrates OpenAI Function Calling with external APIs.
Ask me about the weather in any city around the world!
Type 'help' for examples or 'quit' to exit.

Testing API connections...
✅ Openai: OpenAI API connection successful
✅ Weather Api: Weather API connection successful

🎉 All systems ready! You can start asking about weather.

🗣️  You: What's the weather like in London?
🤖 Assistant: The weather in London is currently 15°C with overcast clouds. It feels like 14°C, and the humidity is at 82%. There's a light breeze with wind speeds of 3.6 m/s from the west-southwest direction.

🗣️  You: How about Tokyo?
🤖 Assistant: In Tokyo, it's currently 22°C with clear skies! It feels like 21°C with a comfortable humidity level of 55%. The wind is gentle at 2.1 m/s, making it a lovely day in the city.

> quit
Goodbye!
```

## 🏗️ Project Structure

```
api_calling_assistant/
│
├── main.py                     # CLI interface and application entry point
├── openai_assistant.py         # OpenAI integration with function calling
├── requirements.txt            # Python dependencies (OpenAI, requests, etc.)
├── .env.example               # Environment variables template
├── .env                       # Your actual API keys (not committed)
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
└── README.md                  # This file
```

## 🔧 Configuration

The application uses environment variables for both OpenAI and weather API configuration:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your_openai_api_key_here

# OpenWeatherMap API Configuration  
WEATHER_API_KEY=your_openweathermap_api_key_here

# API Settings
API_BASE_URL=https://api.openweathermap.org/data/2.5
DEFAULT_UNITS=metric

# Application Settings
DEBUG=false
TIMEOUT=10
```

## 🤖 How It Works

This project demonstrates **OpenAI Function Calling**, where:

1. **User Query**: You ask about weather in natural language
2. **AI Processing**: GPT-4 analyzes your query and determines weather data is needed
3. **Function Call**: OpenAI automatically calls the `get_current_weather` function
4. **API Integration**: The function fetches real-time data from OpenWeatherMap
5. **AI Response**: GPT-4 formats the data into a natural, conversational response

The AI decides when to call external APIs - showcasing intelligent API orchestration!

## 🛠️ Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests (when implemented)
python -m pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines. Format code using:

```bash
# Install formatting tools
pip install black flake8

# Format code
black .

# Check style
flake8 .
```

## 📚 API Reference

### Supported Queries

The assistant understands various ways to ask about weather:

- "What's the weather in [city]?"
- "How's the weather in [city]?"
- "Tell me about the weather in [city]"
- "Weather for [city]"
- "[city] weather"

### Error Handling

The assistant handles common scenarios gracefully:

- **Invalid city names**: Suggests checking spelling
- **Network issues**: Informs about connectivity problems
- **API errors**: Provides user-friendly error messages
- **Missing API key**: Guides through configuration setup

## 🔒 Security

- API keys are stored in environment variables
- No sensitive data is logged
- Input validation prevents injection attacks
- Rate limiting respects API provider limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for providing weather data API
- Python community for excellent libraries and documentation

## 📞 Support

If you encounter any issues or have questions:

1. Check the [issues page](https://github.com/kaleemnadeem16/api_calling_assistant/issues)
2. Create a new issue with detailed information
3. Reach out via email: kaleem.nadeem@gmail.com

---

**Made with ❤️ by [kaleemnadeem16](https://github.com/kaleemnadeem16)**