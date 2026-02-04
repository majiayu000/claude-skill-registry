---
name: "forecast-skill"
description: "Provides real-time weather forecasts using OpenWeather API. Use when users ask about current or future weather conditions, temperature, precipitation, or weather-dependent planning for any location (e.g., 'What's the weather in Paris tomorrow?', 'Will it rain in Seattle this weekend?', 'Should I bring a jacket to Denver?')."
---

# Forecast Skill

Get real-time weather data and forecasts for any location worldwide using OpenWeather.

## Prerequisites

This skill requires an OpenWeather API key to be configured in `config.json` before uploading.

**Setup (done once before uploading the skill):**
1. Get a free API key at https://openweathermap.org/api
2. Edit `config.json` and replace `PASTE_YOUR_API_KEY_HERE` with your key
3. Ensure `api.openweathermap.org` is in your Claude environment's allowed network domains
4. Upload the skill to Claude

**Network Requirements:**
- This skill makes HTTPS requests to `api.openweathermap.org`
- Some Claude environments may require this domain to be added to allowed network lists
- Contact your administrator if you encounter connection errors

See `SETUP.txt` for detailed instructions.

## Usage

### Understanding API Limitations

**Important**: The OpenWeather free tier provides:
- Current weather for any date (today)
- 5-day forecast maximum (today + 4 future days)
- If a user asks for weather beyond 5 days, explain the limitation and suggest alternatives

### Single Location Forecast

When the user asks about weather for one location:

**Modern format (preferred)**:
```bash
python skills/get_weather.py current "<location>"          # Current weather
python skills/get_weather.py forecast "<location>" <days>  # Multi-day forecast (1-5 days)
```

**Legacy format (still supported)**:
```bash
python skills/get_weather.py "<location>" "<YYYY-MM-DD>"
```

**Important**: The script is located at `skills/get_weather.py` (not `scripts/`)

### Multi-Location Comparison

When the user asks to compare weather between locations:

**Trigger phrases:**
- "Compare weather in Paris vs London"
- "Paris or Berlin next week?"
- "Which city has better weather this week?"

**Command format**:
```bash
python skills/get_weather.py compare "<location1>" "<location2>" <days>
```

**Important**: Days parameter is limited to 1-5 due to API forecast limits.

### Activity Recommendations

When the user asks about weather suitability for specific activities:

**Trigger phrases:**
- "Is it good for skiing in Aspen this week?"
- "When should I plan a picnic in the park?"
- "What are the best days for hiking in Colorado?"
- "Should I water my garden tomorrow?"

**Supported activities:** skiing, picnic, hiking, gardening, beach, cycling, plus general outdoor activities and sports

**Flexible activity detection:** The system can analyze weather for many activities, even if not explicitly listed. It will automatically map unfamiliar activities to the most appropriate general category.

**Command format**:
```bash
python skills/get_weather.py activity "<activity_type>" "<location>" <days>
```

**Important**: Days parameter is limited to 1-5 due to API forecast limits.

### Multi-Location Comparison Commands

For location comparisons:
```bash
python skills/get_weather.py compare "<location1>" "<location2>" <days>
```

Present side-by-side comparison with recommendations for travel planning.

## Error Handling

- **missing_api_key**: "The weather service isn't configured. Please edit config.json with your OpenWeather API key before uploading this skill."
- **invalid_api_key**: "Invalid OpenWeather API key. Please check your key in config.json."
- **location_not_found**: Ask for a more specific location (e.g., "Paris, France" instead of "Paris")
- **quota_exceeded**: "The weather service has reached its daily limit. Please try again later."
- **date_not_available**: Forecast is limited to 5 days maximum. When this occurs:
  - Explain the 5-day limit to the user
  - Offer to provide available forecast data for the timeframe that is available
  - Suggest checking back closer to the desired date for extended forecasts

## Response Format

### Single Location Response
The script returns JSON with these fields:
- `location`: Resolved location name
- `date`: Date of forecast
- `temp_c`, `temp_f`: Temperature in Celsius and Fahrenheit
- `humidity`: Relative humidity percentage
- `wind_kph`: Wind speed in km/h
- `condition`: Weather description (e.g., "partly cloudy", "light rain")
- `precip_mm`: Precipitation in millimeters
- `sunrise_utc`, `sunset_utc`: Sun times in UTC ISO format

### Comparison Response
For multi-location comparisons, the script returns:
- `comparison_type`: "multi_day"
- `num_days`: Number of days compared
- `location1`/`location2`: Each containing:
  - `name`: Resolved location name
  - `forecasts`: Array of daily forecasts with temps, conditions, precipitation
- `recommendations`: Array of comparison insights and suggestions

### Activity Recommendation Response
For activity analysis, the script returns:
- `analysis_type`: "activity_recommendation"
- `activity`: Activity name (e.g., "Skiing", "Picnic")
- `overall_score`: 0-100 suitability rating
- `overall_rating`: Text rating (Excellent/Good/Fair/Poor/Not Recommended)
- `best_day`: Date and score of most suitable day
- `daily_analysis`: Array of daily scores and recommendations
- `overall_recommendation`: Summary advice for the activity period

Present this information conversationally, highlighting the most relevant details for the user's query.

## Error Handling

The script may return errors in JSON format:

- `missing_api_key`: API key not provided - ask user for their key
- `invalid_api_key`: API key is invalid - ask user to verify their key
- `location_not_found`: Location not recognized - ask for clarification (e.g., "Paris, France" instead of "Paris")
- `quota_exceeded`: API daily limit reached - inform user to try later
- `invalid_date`: Date format incorrect - use YYYY-MM-DD format
- `unknown_activity`: Activity not recognized - show supported activities list
- Network errors: Inform user the weather service is temporarily unavailable

## Examples

**User:** "What's the weather in Boulder this weekend?"
**Claude should recognize this MAY need the skill, but users get better results with:**
**User:** "Using the forecast-skill, what's the weather in Boulder this weekend?"
**Action:**
1. Extract: location="Boulder", dates=[Saturday, Sunday]
2. Call: `python skills/get_weather.py forecast Boulder 2`
3. Summarize: "This weekend in Boulder: Saturday will be sunny and 72°F, perfect for outdoor activities. Sunday looks cooler at 65°F with a chance of afternoon showers."

**User:** "Using forecast-skill, should I bring an umbrella to Tokyo tomorrow?"
**Action:**
1. Extract: location="Tokyo", date=tomorrow
2. Call: `python skills/get_weather.py forecast Tokyo 1`
3. Check precipitation and respond: "Tomorrow in Tokyo has a 70% chance of rain with 5mm expected. Definitely bring an umbrella!"

**User:** "With the forecast-skill, is this week good for skiing in Vail?"
**Action:**
1. Extract: activity="skiing", location="Vail", days=5 (limit to 5-day forecast)
2. Call: `python skills/get_weather.py activity skiing Vail 5`
3. Analyze response: "The next 5 days look excellent for skiing in Vail! Overall score: 85/100. Best conditions on Wednesday with fresh powder and temps around -2°C."

**User:** "Using forecast-skill, compare weather in Aspen this weekend vs next weekend"
**Action:**
1. Recognize next weekend exceeds 5-day limit
2. Call: `python skills/get_weather.py forecast Aspen 2` (for this weekend)
3. Respond: "I can provide this weekend's forecast for Aspen, but weather data beyond 5 days isn't available. This weekend looks great with sunny skies and 12°C. For next weekend, I'd suggest checking back in a few days for the most accurate forecast."

**User:** "Using the forecast-skill, compare weather in London vs Paris next week"
**Action:**
1. Extract: location1="Paris", location2="London", days=7
2. Call: `python skills/get_weather.py compare "Paris" "London" 7`
3. Present comparison: "Comparing Paris and London for the next week: Paris will be warmer overall (averaging 18°C vs 14°C) but has more rainy days expected (4 vs 2). London has fewer rainy days expected, making it better for outdoor activities despite cooler temperatures."

## Skill Activation Tips

**Best Practice**: Users should prefix queries with "Using the forecast-skill," or "With forecast-skill," to ensure reliable activation.

**Examples of effective prompts:**
- "Using the forecast-skill, [weather question]"
- "With forecast-skill, [weather question]"  
- "Can you use forecast-skill to [weather question]"

**Why explicit activation helps:**
- Ensures Claude uses the weather API instead of general knowledge
- Gets real-time data rather than training data
- Provides more accurate and current forecasts