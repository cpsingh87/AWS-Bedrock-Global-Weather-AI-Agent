# ============================================================
# GLOBAL WEATHER AGENT (Claude + OpenWeatherMap)
# Supports ALL countries, cities, states, and vague descriptions
# ============================================================

import boto3
import json
import os
from urllib.parse import quote
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------
# Load .env from script directory if present (optional)
_script_dir = os.path.dirname(os.path.abspath(__file__))
_env_path = os.path.join(_script_dir, ".env")
if os.path.isfile(_env_path):
    with open(_env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                key, value = key.strip(), value.strip().strip('"').strip("'")
                if key:
                    os.environ.setdefault(key, value)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not OPENWEATHER_API_KEY:
    raise ValueError(
        "OPENWEATHER_API_KEY is missing. Copy .env.example to .env and add your key, "
        "or set the OPENWEATHER_API_KEY environment variable."
    )

# ------------------------------------------------------------
# CLAUDE CALL
# ------------------------------------------------------------
def call_claude_sonnet(prompt):
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-west-2'
    )

    try:
        response = bedrock.converse(
            modelId='us.anthropic.claude-sonnet-4-5-20250929-v1:0',
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": 2000, "temperature": 0.7}
        )

        return True, response['output']['message']['content'][0]['text']

    except Exception as e:
        return False, f"Error calling Claude: {str(e)}"

# ------------------------------------------------------------
# HTTP FETCH
# ------------------------------------------------------------
def fetch_url(url, timeout=30):
    try:
        with urlopen(url, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
        return True, body
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return False, body or f"HTTP {e.code}: {e.reason}"
    except (URLError, OSError) as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

# ------------------------------------------------------------
# STEP 1: CLAUDE INTERPRETS LOCATION
# ------------------------------------------------------------
def interpret_location_with_claude(location):
    prompt = f"""
You are a world geography expert.

The user provided this location description:
"{location}"

Your task:
1. Interpret the location
2. Return ONLY the best matching real-world place name
3. Do NOT include explanations

Examples:
"city near Eiffel Tower" → "Paris, France"
"capital of Punjab" → "Chandigarh, India"
"largest city in Italy" → "Rome, Italy"
"village near Amritsar airport" → "Amritsar, Punjab, India"

Now return the interpreted location:
"""

    success, response = call_claude_sonnet(prompt)
    return success, response.strip()

# ------------------------------------------------------------
# STEP 2: GEOCODING (GLOBAL)
# ------------------------------------------------------------
def geocode_location(location):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={quote(location)}&limit=1&appid={OPENWEATHER_API_KEY}"
    success, response = fetch_url(url)
    if not success:
        return False, response

    try:
        data = json.loads(response)
        if len(data) == 0:
            return False, "No matching location found."

        lat = data[0]['lat']
        lon = data[0]['lon']
        return True, (lat, lon)

    except Exception as e:
        return False, f"Error parsing geocoding response: {str(e)}"

# ------------------------------------------------------------
# STEP 3: FETCH GLOBAL WEATHER
# ------------------------------------------------------------
def fetch_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    return fetch_url(url)

# ------------------------------------------------------------
# STEP 4: CLAUDE SUMMARIZES WEATHER
# ------------------------------------------------------------
def process_weather_response(raw_json, location):
    prompt = f"""
You are a weather information specialist.

I have global weather forecast data from OpenWeatherMap for:
"{location}"

Raw API Response:
{raw_json}

Create a clear, helpful summary including:
1. Brief intro with the location
2. Current conditions and today's forecast
3. Next 2–3 days outlook (temperature, precipitation, wind)
4. Any notable weather patterns or alerts
5. Format it for easy reading
"""

    success, response = call_claude_sonnet(prompt)
    return success, response

# ------------------------------------------------------------
# MAIN AGENT LOOP
# ------------------------------------------------------------
def run_weather_agent():
    print("Welcome to the Global Weather AI Agent")
    print("This agent uses Claude and OpenWeatherMap to get weather anywhere in the world.")
    print("=" * 60)

    while True:
        location = input("\nEnter a location or description (or 'quit'): ").strip()

        if location.lower() in ['quit', 'exit', 'q']:
            print("Exiting Global Weather Agent.")
            break

        if not location:
            print("Please enter a valid location.")
            continue

        print(f"\nStarting weather analysis for '{location}'...")
        print("-" * 40)

        # Step 1: Interpret location
        print("Step 1: Interpreting location with Claude...")
        success, interpreted = interpret_location_with_claude(location)

        if not success:
            print(f"Failed to interpret location: {interpreted}")
            continue

        print(f"Interpreted as: {interpreted}")

        # Step 2: Geocode
        print("\nStep 2: Geocoding location...")
        success, coords = geocode_location(interpreted)

        if not success:
            print(f"Geocoding failed: {coords}")
            continue

        lat, lon = coords
        print(f"Coordinates: {lat}, {lon}")

        # Step 3: Fetch weather
        print("\nStep 3: Fetching global weather data...")
        success, weather_json = fetch_weather(lat, lon)

        if not success:
            print(f"Failed to fetch weather: {weather_json}")
            continue

        print(f"Received {len(weather_json)} characters of weather data")

        # Step 4: Summarize
        print("\nStep 4: AI Summary Phase...")
        success, summary = process_weather_response(weather_json, interpreted)

        if not success:
            print(f"Failed to summarize weather: {summary}")
            continue

        print("\nWeather Forecast")
        print("=" * 60)
        print(summary)
        print("=" * 60)

        print(f"\nWeather analysis complete for '{interpreted}'.")

# ------------------------------------------------------------
# RUN AGENT
# ------------------------------------------------------------
if __name__ == "__main__":
    run_weather_agent()
