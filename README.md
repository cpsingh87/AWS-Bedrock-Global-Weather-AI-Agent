# Global Weather AI Agent

An interactive weather agent that uses **Claude (AWS Bedrock)** and **OpenWeatherMap** to get weather for any location in the world. You can enter city names, countries, or natural-language descriptions (e.g. "capital of France", "city near Eiffel Tower").

## Prerequisites

- **Python 3.7+**
- **OpenWeatherMap API key** — [Get one free](https://openweathermap.org/api)
- **AWS account** with access to **Bedrock** (Claude) — for location interpretation and weather summaries

## Setup (no code changes required)

1. **Clone the repo** (or download the project).

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   - Copy `.env.example` to `.env`
   - Edit `.env` and set `OPENWEATHER_API_KEY` to your OpenWeather API key
   - For Claude: configure AWS credentials (e.g. run `aws configure`, or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`)

4. **Run the agent:**
   ```bash
   python weather_agent.py
   ```
   On some systems you may need `python3` instead of `python`.

## Usage

- Enter a location or description when prompted (e.g. `London`, `Tokyo`, `capital of India`).
- Type `quit`, `exit`, or `q` to exit.

## License

Use and modify as you like.
