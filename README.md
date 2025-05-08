# API Calling Assistant

A Python-based AI assistant that fetches real-time weather data from external APIs and presents it in a conversational format.

## 🌟 Features

- **Natural Language Processing**: Ask weather questions in plain English
- **Real-time Weather Data**: Powered by OpenWeatherMap API
- **Error Handling**: Graceful handling of network issues and invalid inputs
- **Command-line Interface**: Simple terminal-based interaction
- **Secure Configuration**: Environment-based API key management

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
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

3. **Configure environment**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your OpenWeatherMap API key
   # API_KEY=your_openweathermap_api_key_here
   ```

4. **Run the assistant**
   ```bash
   python main.py
   ```

## 💬 Usage

Once running, you can ask weather questions in natural language:

```
Welcome to the API Calling Assistant!
Type 'quit' to exit.

> What's the weather in London?
It's currently 20.5°C with clear sky in London. Humidity is 65%.

> How's the weather in New York?
It's currently 18.2°C with scattered clouds in New York. Humidity is 72%.

> Tell me about Tokyo weather
It's currently 25.1°C with light rain in Tokyo. Humidity is 80%.

> quit
Goodbye!
```

## 🏗️ Project Structure

```
api_calling_assistant/
│
├── main.py                  # Entry point and CLI interface
├── api_handler.py           # OpenWeatherMap API integration
├── parser.py                # Natural language query processing
├── formatter.py             # Response formatting and presentation
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔧 Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and customize:

```env
# OpenWeatherMap API Configuration
API_KEY=your_api_key_here
API_BASE_URL=https://api.openweathermap.org/data/2.5
DEFAULT_UNITS=metric

# Application Settings
DEBUG=false
TIMEOUT=10
```

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