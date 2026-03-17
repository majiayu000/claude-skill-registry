---
slug: "weather-api"
display_name: "Weather API"
description: "Fetch weather data for construction scheduling. Historical data, forecasts, and risk assessment for outdoor work."
---

# Weather API for Construction

## Overview
Weather impacts 50% of construction activities. This skill fetches weather data for scheduling, risk assessment, and productivity adjustments.

## Python Implementation

```python
import requests
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class WeatherRisk(Enum):
    """Weather risk levels for construction."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class WeatherCondition:
    """Weather condition at a point in time."""
    timestamp: datetime
    temperature: float  # Celsius
    humidity: float     # Percent
    wind_speed: float   # m/s
    precipitation: float  # mm
    conditions: str


@dataclass
class WorkabilityAssessment:
    """Assessment of weather workability."""
    date: datetime
    risk_level: WeatherRisk
    workable_hours: int
    affected_activities: List[str]
    recommendations: List[str]


class WeatherAPIClient:
    """Client for weather APIs."""

    # Free tier endpoints
    OPEN_METEO_BASE = "https://api.open-meteo.com/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def get_forecast(self, latitude: float, longitude: float,
                     days: int = 7) -> List[WeatherCondition]:
        """Get weather forecast."""
        url = f"{self.OPEN_METEO_BASE}/forecast"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation',
            'forecast_days': days
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code}")

        data = response.json()
        return self._parse_forecast(data)

    def get_historical(self, latitude: float, longitude: float,
                       start_date: str, end_date: str) -> List[WeatherCondition]:
        """Get historical weather data."""
        url = f"{self.OPEN_METEO_BASE}/archive"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'start_date': start_date,
            'end_date': end_date,
            'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation'
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code}")

        data = response.json()
        return self._parse_forecast(data)

    def _parse_forecast(self, data: Dict) -> List[WeatherCondition]:
        """Parse API response to WeatherCondition list."""
        conditions = []
        hourly = data.get('hourly', {})

        times = hourly.get('time', [])
        temps = hourly.get('temperature_2m', [])
        humidity = hourly.get('relative_humidity_2m', [])
        wind = hourly.get('wind_speed_10m', [])
        precip = hourly.get('precipitation', [])

        for i in range(len(times)):
            conditions.append(WeatherCondition(
                timestamp=datetime.fromisoformat(times[i]),
                temperature=temps[i] if i < len(temps) else 0,
                humidity=humidity[i] if i < len(humidity) else 0,
                wind_speed=wind[i] if i < len(wind) else 0,
                precipitation=precip[i] if i < len(precip) else 0,
                conditions=self._describe_conditions(
                    temps[i] if i < len(temps) else 0,
                    precip[i] if i < len(precip) else 0,
                    wind[i] if i < len(wind) else 0
                )
            ))

        return conditions

    def _describe_conditions(self, temp: float, precip: float, wind: float) -> str:
        """Generate weather description."""
        conditions = []

        if temp < 0:
            conditions.append("Freezing")
        elif temp > 35:
            conditions.append("Extreme heat")
        elif temp > 30:
            conditions.append("Hot")
        elif temp < 10:
            conditions.append("Cold")

        if precip > 10:
            conditions.append("Heavy rain")
        elif precip > 2:
            conditions.append("Rain")
        elif precip > 0:
            conditions.append("Light rain")

        if wind > 15:
            conditions.append("Strong winds")
        elif wind > 10:
            conditions.append("Windy")

        return ", ".join(conditions) if conditions else "Clear"

    def to_dataframe(self, conditions: List[WeatherCondition]) -> pd.DataFrame:
        """Convert conditions to DataFrame."""
        data = [{
            'timestamp': c.timestamp,
            'temperature': c.temperature,
            'humidity': c.humidity,
            'wind_speed': c.wind_speed,
            'precipitation': c.precipitation,
            'conditions': c.conditions
        } for c in conditions]
        return pd.DataFrame(data)


class ConstructionWeatherRisk:
    """Assess weather risk for construction activities."""

    # Activity-specific thresholds
    THRESHOLDS = {
        'concrete_pour': {
            'min_temp': 5, 'max_temp': 35,
            'max_wind': 12, 'max_precip': 0.5
        },
        'crane_work': {
            'min_temp': -10, 'max_temp': 40,
            'max_wind': 10, 'max_precip': 5
        },
        'exterior_paint': {
            'min_temp': 10, 'max_temp': 35,
            'max_wind': 8, 'max_precip': 0
        },
        'roofing': {
            'min_temp': 5, 'max_temp': 38,
            'max_wind': 12, 'max_precip': 0
        },
        'earthwork': {
            'min_temp': -5, 'max_temp': 40,
            'max_wind': 20, 'max_precip': 10
        }
    }

    def assess_workability(self, condition: WeatherCondition,
                           activities: List[str] = None) -> WorkabilityAssessment:
        """Assess workability for given conditions."""

        if activities is None:
            activities = list(self.THRESHOLDS.keys())

        affected = []
        recommendations = []

        for activity in activities:
            if activity in self.THRESHOLDS:
                thresh = self.THRESHOLDS[activity]

                reasons = []
                if condition.temperature < thresh['min_temp']:
                    reasons.append(f"Too cold ({condition.temperature}°C)")
                if condition.temperature > thresh['max_temp']:
                    reasons.append(f"Too hot ({condition.temperature}°C)")
                if condition.wind_speed > thresh['max_wind']:
                    reasons.append(f"High wind ({condition.wind_speed} m/s)")
                if condition.precipitation > thresh['max_precip']:
                    reasons.append(f"Precipitation ({condition.precipitation} mm)")

                if reasons:
                    affected.append(activity)
                    recommendations.append(f"{activity}: " + ", ".join(reasons))

        # Determine overall risk level
        if len(affected) >= len(activities) * 0.8:
            risk = WeatherRisk.CRITICAL
            workable = 0
        elif len(affected) >= len(activities) * 0.5:
            risk = WeatherRisk.HIGH
            workable = 4
        elif len(affected) > 0:
            risk = WeatherRisk.MODERATE
            workable = 6
        else:
            risk = WeatherRisk.LOW
            workable = 8

        return WorkabilityAssessment(
            date=condition.timestamp,
            risk_level=risk,
            workable_hours=workable,
            affected_activities=affected,
            recommendations=recommendations
        )

    def weekly_forecast_risk(self, conditions: List[WeatherCondition],
                             activities: List[str] = None) -> pd.DataFrame:
        """Assess risk for week of weather data."""

        # Group by date
        daily_conditions = {}
        for c in conditions:
            date = c.timestamp.date()
            if date not in daily_conditions:
                daily_conditions[date] = []
            daily_conditions[date].append(c)

        assessments = []
        for date, day_conditions in daily_conditions.items():
            # Use midday condition as representative
            midday = [c for c in day_conditions
                      if 10 <= c.timestamp.hour <= 16]
            representative = midday[len(midday)//2] if midday else day_conditions[0]

            assessment = self.assess_workability(representative, activities)
            assessments.append({
                'date': date,
                'risk_level': assessment.risk_level.value,
                'workable_hours': assessment.workable_hours,
                'affected_count': len(assessment.affected_activities)
            })

        return pd.DataFrame(assessments)
```

## Quick Start

```python
# Initialize client
weather = WeatherAPIClient()

# Get forecast for site
conditions = weather.get_forecast(latitude=52.52, longitude=13.41, days=7)
df = weather.to_dataframe(conditions)
print(df.head())

# Assess construction risk
risk = ConstructionWeatherRisk()
weekly_risk = risk.weekly_forecast_risk(conditions)
print(weekly_risk)
```

## Common Use Cases

### 1. Schedule Planning
```python
conditions = weather.get_forecast(52.52, 13.41, days=14)
risk = ConstructionWeatherRisk()

# Check concrete pour window
for c in conditions:
    assessment = risk.assess_workability(c, ['concrete_pour'])
    if assessment.risk_level == WeatherRisk.LOW:
        print(f"Good for concrete: {c.timestamp}")
```

### 2. Historical Analysis
```python
historical = weather.get_historical(52.52, 13.41, '2024-01-01', '2024-03-31')
df = weather.to_dataframe(historical)

# Count rain days
rain_days = df[df['precipitation'] > 2]['timestamp'].dt.date.nunique()
print(f"Rain days in Q1: {rain_days}")
```

## Resources
- **DDC Book**: Chapter 2.2 - Open Data Integration
- **Open-Meteo API**: https://open-meteo.com/
