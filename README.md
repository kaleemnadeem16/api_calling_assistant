# LangChain API Calling Assistant

A small command-line assistant that shows LangChain tool calling. You ask in plain English; an OpenAI model decides which tool to call (weather, time, your location, or details about a place), calls it, and answers from the result. Several tools can be chained in one question, for example "weather where I am".

**Status:** Stable. Small, single-purpose reference implementation of tool calling; no further features planned.

## Tools

| Tool | What it does | Source |
|---|---|---|
| WeatherTool | Current weather for a city | OpenWeatherMap |
| TimeTool | Current time, with timezone support | `pytz` |
| MyLocationTool | Approximate location from your IP | `geocoder` |
| LocationInfoTool | Details about a named place | See `tools/location_info_tool.py` |

Flow: user query -> LangChain tool-calling agent (with conversation buffer memory) -> tool selection -> tool execution -> reply.

## Quick start

Requires Python 3.9+, an OpenAI API key and a free OpenWeatherMap key.

```bash
git clone https://github.com/kaleemnadeem16/api_calling_assistant.git
cd api_calling_assistant
pip install -r requirements.txt
cp .env.example .env     # set OPENAI_API_KEY and WEATHER_API_KEY
python main.py
```

## Example

Illustrative conversation (not a recorded run):

```
You: What's the weather like where I am?
Assistant: Let me detect your location first... You're in <city>. The current weather there is ...
```

## Configuration

Set in `.env` (see `.env.example`).

| Variable | Default | Required |
|---|---|---|
| `OPENAI_API_KEY` | none | yes |
| `WEATHER_API_KEY` | none | yes |
| `OPENAI_MODEL` | `gpt-4.1-nano` | no |
| `OPENAI_TEMPERATURE` | `0.7` | no |
| `OPENAI_MAX_TOKENS` | `500` | no |
| `API_BASE_URL` | OpenWeatherMap | no |
| `DEFAULT_UNITS` | `metric` | no |
| `ENABLE_TIME_FUNCTIONS`, `ENABLE_LOCATION_FUNCTIONS` | `true` | no |
| `DEBUG`, `TIMEOUT` | `false`, `10` s | no |

The model must support tool calling.

## Project layout

```
main.py             CLI
core/assistant.py   LangChain agent and memory
tools/              weather, time, location tools and their input schemas
test_assistant.py   tests (run as a script)
```

## Tests

```bash
python test_assistant.py
```

Covers initialisation, capabilities, a basic conversation, tool calling and error handling.

## Troubleshooting

- **"API key not configured":** set `OPENAI_API_KEY` and `WEATHER_API_KEY` in `.env`.
- **`ModuleNotFoundError: langchain`:** run `pip install -r requirements.txt` in the active environment.
- **Wrong location:** location comes from your IP address and is approximate; VPNs and corporate networks distort it. Ask about a named city instead.

## Limitations

- Needs two API keys and network access; there is no offline mode.
- IP-based location is approximate.
- Weather comes from one provider only.

## License

MIT, see [LICENSE](LICENSE).
