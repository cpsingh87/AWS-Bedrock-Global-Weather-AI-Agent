# Global Weather AI Agent

An **agentic AI**–based weather agent that uses **Claude (AWS Bedrock)** and **OpenWeatherMap** to get weather for any location in the world. You can enter city names, countries, or natural-language descriptions (e.g. "capital of France", "city near Eiffel Tower"). The agent orchestrates multiple steps—location interpretation, geocoding, and weather summarization—using an LLM and external APIs.

## Workflow

<img width="687" height="311" alt="Workflow" src="https://github.com/user-attachments/assets/a7d2a869-aab2-4120-b425-a85dfeb0ce5e" />

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

<img width="1381" height="560" alt="weather_agent_Screenshot_1" src="https://github.com/user-attachments/assets/83c403b0-8569-47b0-8144-66961a17108d" />

<img width="1073" height="692" alt="weather_agent_Screenshot_2" src="https://github.com/user-attachments/assets/3889f77f-ad87-4093-a79f-137aacad12e1" />


## License

Use and modify as you like.
