---
name: weather-impact-analysis
description: "Analyze weather data impact on construction schedules. Predict weather delays, optimize work scheduling based on forecasts, and calculate weather-related risk factors for project planning."
---

# Weather Impact Analysis

## Overview

This skill implements weather data analysis for construction project management. Integrate weather forecasts, historical data, and activity sensitivity to predict delays and optimize scheduling.

**Capabilities:**
- Weather forecast integration
- Activity weather sensitivity mapping
- Delay prediction and quantification
- Schedule optimization based on weather
- Historical weather impact analysis
- Risk factor calculation

## Quick Start

```python
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum
import requests

class WeatherCondition(Enum):
    CLEAR = "clear"
    CLOUDY = "cloudy"
    RAIN = "rain"
    HEAVY_RAIN = "heavy_rain"
    SNOW = "snow"
    FROST = "frost"
    HIGH_WIND = "high_wind"
    EXTREME_HEAT = "extreme_heat"
    EXTREME_COLD = "extreme_cold"

@dataclass
class WeatherDay:
    date: date
    condition: WeatherCondition
    temp_high: float
    temp_low: float
    precipitation_mm: float
    wind_speed_kmh: float
    humidity_pct: float

@dataclass
class ActivitySensitivity:
    activity_type: str
    min_temp: float
    max_temp: float
    max_wind: float
    max_precipitation: float
    can_work_in_rain: bool

def check_work_day(weather: WeatherDay, activity: ActivitySensitivity) -> Dict:
    """Check if work is possible for given weather and activity"""
    can_work = True
    reasons = []

    if weather.temp_low < activity.min_temp:
        can_work = False
        reasons.append(f"Temperature too low: {weather.temp_low}°C < {activity.min_temp}°C")

    if weather.temp_high > activity.max_temp:
        can_work = False
        reasons.append(f"Temperature too high: {weather.temp_high}°C > {activity.max_temp}°C")

    if weather.wind_speed_kmh > activity.max_wind:
        can_work = False
        reasons.append(f"Wind too strong: {weather.wind_speed_kmh} km/h > {activity.max_wind} km/h")

    if weather.precipitation_mm > activity.max_precipitation and not activity.can_work_in_rain:
        can_work = False
        reasons.append(f"Precipitation: {weather.precipitation_mm}mm")

    return {
        'date': weather.date,
        'can_work': can_work,
        'reasons': reasons,
        'productivity_factor': 1.0 if can_work else 0.0
    }

# Example
concrete_work = ActivitySensitivity(
    activity_type="concrete_placement",
    min_temp=5,
    max_temp=35,
    max_wind=40,
    max_precipitation=2,
    can_work_in_rain=False
)

today_weather = WeatherDay(
    date=date.today(),
    condition=WeatherCondition.RAIN,
    temp_high=15,
    temp_low=8,
    precipitation_mm=10,
    wind_speed_kmh=20,
    humidity_pct=80
)

result = check_work_day(today_weather, concrete_work)
print(f"Can work: {result['can_work']}, Reasons: {result['reasons']}")
```

## Comprehensive Weather Analysis System

### Weather Data Integration

```python
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional, Tuple
from enum import Enum
import requests
import json

class WeatherSeverity(Enum):
    NORMAL = 1
    CAUTION = 2
    WARNING = 3
    SEVERE = 4
    EXTREME = 5

@dataclass
class HourlyWeather:
    datetime: datetime
    temperature: float
    feels_like: float
    humidity: float
    wind_speed: float
    wind_direction: float
    precipitation: float
    precipitation_probability: float
    condition: WeatherCondition
    visibility: float
    uv_index: float

@dataclass
class DailyForecast:
    date: date
    temp_high: float
    temp_low: float
    sunrise: datetime
    sunset: datetime
    precipitation_total: float
    precipitation_probability: float
    primary_condition: WeatherCondition
    hourly: List[HourlyWeather] = field(default_factory=list)
    severity: WeatherSeverity = WeatherSeverity.NORMAL

class WeatherDataService:
    """Weather data integration service"""

    def __init__(self, api_key: str = None, provider: str = "openweathermap"):
        self.api_key = api_key
        self.provider = provider
        self.cache: Dict[str, Dict] = {}
        self.cache_duration = timedelta(hours=1)

    def get_forecast(self, latitude: float, longitude: float,
                    days: int = 14) -> List[DailyForecast]:
        """Get weather forecast for location"""
        cache_key = f"{latitude},{longitude}"

        if cache_key in self.cache:
            cached = self.cache[cache_key]
            if datetime.now() - cached['timestamp'] < self.cache_duration:
                return cached['data']

        if self.provider == "openweathermap":
            forecast = self._fetch_openweathermap(latitude, longitude, days)
        else:
            forecast = self._generate_sample_forecast(days)

        self.cache[cache_key] = {
            'timestamp': datetime.now(),
            'data': forecast
        }

        return forecast

    def _fetch_openweathermap(self, lat: float, lon: float,
                              days: int) -> List[DailyForecast]:
        """Fetch from OpenWeatherMap API"""
        url = f"https://api.openweathermap.org/data/2.5/forecast"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
            return self._parse_openweathermap(data)
        except Exception as e:
            print(f"Weather API error: {e}")
            return self._generate_sample_forecast(days)

    def _parse_openweathermap(self, data: Dict) -> List[DailyForecast]:
        """Parse OpenWeatherMap response"""
        forecasts = []
        daily_data = {}

        for item in data.get('list', []):
            dt = datetime.fromtimestamp(item['dt'])
            day = dt.date()

            if day not in daily_data:
                daily_data[day] = {
                    'temps': [],
                    'precipitation': 0,
                    'conditions': [],
                    'hourly': []
                }

            daily_data[day]['temps'].append(item['main']['temp'])
            daily_data[day]['precipitation'] += item.get('rain', {}).get('3h', 0)

            condition = self._map_condition(item['weather'][0]['main'])
            daily_data[day]['conditions'].append(condition)

            daily_data[day]['hourly'].append(HourlyWeather(
                datetime=dt,
                temperature=item['main']['temp'],
                feels_like=item['main']['feels_like'],
                humidity=item['main']['humidity'],
                wind_speed=item['wind']['speed'] * 3.6,  # m/s to km/h
                wind_direction=item['wind'].get('deg', 0),
                precipitation=item.get('rain', {}).get('3h', 0),
                precipitation_probability=item.get('pop', 0) * 100,
                condition=condition,
                visibility=item.get('visibility', 10000) / 1000,
                uv_index=0
            ))

        for day, data in daily_data.items():
            primary_condition = max(set(data['conditions']), key=data['conditions'].count)

            forecasts.append(DailyForecast(
                date=day,
                temp_high=max(data['temps']),
                temp_low=min(data['temps']),
                sunrise=datetime.combine(day, datetime.min.time().replace(hour=6)),
                sunset=datetime.combine(day, datetime.min.time().replace(hour=18)),
                precipitation_total=data['precipitation'],
                precipitation_probability=max(h.precipitation_probability for h in data['hourly']),
                primary_condition=primary_condition,
                hourly=data['hourly'],
                severity=self._calculate_severity(primary_condition, data)
            ))

        return sorted(forecasts, key=lambda x: x.date)

    def _map_condition(self, condition_str: str) -> WeatherCondition:
        """Map API condition to enum"""
        mapping = {
            'Clear': WeatherCondition.CLEAR,
            'Clouds': WeatherCondition.CLOUDY,
            'Rain': WeatherCondition.RAIN,
            'Drizzle': WeatherCondition.RAIN,
            'Thunderstorm': WeatherCondition.HEAVY_RAIN,
            'Snow': WeatherCondition.SNOW,
            'Mist': WeatherCondition.CLOUDY,
            'Fog': WeatherCondition.CLOUDY
        }
        return mapping.get(condition_str, WeatherCondition.CLEAR)

    def _calculate_severity(self, condition: WeatherCondition,
                           data: Dict) -> WeatherSeverity:
        """Calculate weather severity"""
        max_temp = max(data['temps'])
        min_temp = min(data['temps'])
        precip = data['precipitation']

        if condition in [WeatherCondition.HEAVY_RAIN, WeatherCondition.SNOW]:
            if precip > 50:
                return WeatherSeverity.EXTREME
            elif precip > 25:
                return WeatherSeverity.SEVERE

        if max_temp > 40 or min_temp < -15:
            return WeatherSeverity.SEVERE

        if max_temp > 35 or min_temp < -5:
            return WeatherSeverity.WARNING

        if condition == WeatherCondition.RAIN:
            return WeatherSeverity.CAUTION

        return WeatherSeverity.NORMAL

    def _generate_sample_forecast(self, days: int) -> List[DailyForecast]:
        """Generate sample forecast for testing"""
        import random
        forecasts = []

        for i in range(days):
            day = date.today() + timedelta(days=i)
            temp_base = 15 + random.uniform(-5, 10)
            condition = random.choice(list(WeatherCondition))

            forecasts.append(DailyForecast(
                date=day,
                temp_high=temp_base + random.uniform(3, 8),
                temp_low=temp_base - random.uniform(3, 8),
                sunrise=datetime.combine(day, datetime.min.time().replace(hour=6)),
                sunset=datetime.combine(day, datetime.min.time().replace(hour=18)),
                precipitation_total=random.uniform(0, 20) if condition == WeatherCondition.RAIN else 0,
                precipitation_probability=random.uniform(0, 100) if condition == WeatherCondition.RAIN else 10,
                primary_condition=condition,
                severity=WeatherSeverity.NORMAL
            ))

        return forecasts
```

### Activity Weather Sensitivity

```python
@dataclass
class WeatherThresholds:
    min_temp: float = -10
    max_temp: float = 45
    max_wind: float = 50
    max_precipitation: float = 50
    max_snow_depth: float = 20
    min_visibility: float = 0.5  # km

@dataclass
class ConstructionActivity:
    activity_id: str
    activity_name: str
    category: str
    thresholds: WeatherThresholds
    indoor: bool = False
    rain_sensitive: bool = True
    frost_sensitive: bool = False
    productivity_factors: Dict[WeatherCondition, float] = field(default_factory=dict)

    def __post_init__(self):
        if not self.productivity_factors:
            self.productivity_factors = {
                WeatherCondition.CLEAR: 1.0,
                WeatherCondition.CLOUDY: 0.95,
                WeatherCondition.RAIN: 0.3 if self.rain_sensitive else 0.8,
                WeatherCondition.HEAVY_RAIN: 0.0 if self.rain_sensitive else 0.5,
                WeatherCondition.SNOW: 0.2,
                WeatherCondition.FROST: 0.5 if self.frost_sensitive else 0.8,
                WeatherCondition.HIGH_WIND: 0.3,
                WeatherCondition.EXTREME_HEAT: 0.6,
                WeatherCondition.EXTREME_COLD: 0.4
            }

class ActivityWeatherAnalyzer:
    """Analyze weather impact on construction activities"""

    # Default activity definitions
    ACTIVITY_TEMPLATES = {
        'concrete_placement': ConstructionActivity(
            activity_id='ACT-001',
            activity_name='Concrete Placement',
            category='structural',
            thresholds=WeatherThresholds(min_temp=5, max_temp=35, max_precipitation=2, max_wind=40),
            rain_sensitive=True,
            frost_sensitive=True
        ),
        'steel_erection': ConstructionActivity(
            activity_id='ACT-002',
            activity_name='Steel Erection',
            category='structural',
            thresholds=WeatherThresholds(max_wind=35, max_precipitation=10),
            rain_sensitive=False
        ),
        'roofing': ConstructionActivity(
            activity_id='ACT-003',
            activity_name='Roofing',
            category='envelope',
            thresholds=WeatherThresholds(min_temp=0, max_precipitation=0, max_wind=30),
            rain_sensitive=True
        ),
        'excavation': ConstructionActivity(
            activity_id='ACT-004',
            activity_name='Excavation',
            category='earthwork',
            thresholds=WeatherThresholds(min_temp=-5, max_precipitation=25),
            rain_sensitive=True,
            frost_sensitive=True
        ),
        'painting_exterior': ConstructionActivity(
            activity_id='ACT-005',
            activity_name='Exterior Painting',
            category='finishing',
            thresholds=WeatherThresholds(min_temp=10, max_temp=35, max_precipitation=0, max_wind=25),
            rain_sensitive=True
        ),
        'masonry': ConstructionActivity(
            activity_id='ACT-006',
            activity_name='Masonry Work',
            category='structural',
            thresholds=WeatherThresholds(min_temp=5, max_temp=32, max_precipitation=5),
            rain_sensitive=True,
            frost_sensitive=True
        ),
        'crane_operations': ConstructionActivity(
            activity_id='ACT-007',
            activity_name='Crane Operations',
            category='equipment',
            thresholds=WeatherThresholds(max_wind=30, min_visibility=1.0),
            rain_sensitive=False
        ),
        'electrical_exterior': ConstructionActivity(
            activity_id='ACT-008',
            activity_name='Exterior Electrical',
            category='MEP',
            thresholds=WeatherThresholds(max_precipitation=0),
            rain_sensitive=True
        ),
        'interior_work': ConstructionActivity(
            activity_id='ACT-009',
            activity_name='Interior Work',
            category='finishing',
            thresholds=WeatherThresholds(),
            indoor=True,
            rain_sensitive=False
        )
    }

    def __init__(self):
        self.activities = dict(self.ACTIVITY_TEMPLATES)

    def add_activity(self, activity: ConstructionActivity):
        """Add custom activity"""
        self.activities[activity.activity_id] = activity

    def analyze_day(self, weather: DailyForecast,
                   activities: List[str]) -> Dict[str, Dict]:
        """Analyze weather impact for specific day and activities"""
        results = {}

        for activity_id in activities:
            activity = self.activities.get(activity_id)
            if not activity:
                continue

            impact = self._calculate_impact(weather, activity)
            results[activity_id] = impact

        return results

    def _calculate_impact(self, weather: DailyForecast,
                         activity: ConstructionActivity) -> Dict:
        """Calculate weather impact on activity"""
        if activity.indoor:
            return {
                'can_work': True,
                'productivity': 1.0,
                'issues': [],
                'recommendations': []
            }

        issues = []
        productivity = 1.0

        # Temperature check
        if weather.temp_low < activity.thresholds.min_temp:
            issues.append(f"Low temperature: {weather.temp_low}°C")
            if activity.frost_sensitive:
                productivity *= 0.0
            else:
                productivity *= 0.5

        if weather.temp_high > activity.thresholds.max_temp:
            issues.append(f"High temperature: {weather.temp_high}°C")
            productivity *= 0.6

        # Precipitation check
        if weather.precipitation_total > activity.thresholds.max_precipitation:
            issues.append(f"Precipitation: {weather.precipitation_total}mm")
            if activity.rain_sensitive:
                productivity *= 0.0
            else:
                productivity *= 0.7

        # Condition-based productivity
        condition_factor = activity.productivity_factors.get(
            weather.primary_condition, 1.0
        )
        productivity *= condition_factor

        # Generate recommendations
        recommendations = []
        if productivity < 0.5 and productivity > 0:
            recommendations.append("Consider rescheduling to more favorable day")
        if weather.temp_low < activity.thresholds.min_temp + 5:
            recommendations.append("Plan for cold weather precautions")
        if weather.precipitation_probability > 50:
            recommendations.append("Have rain contingency plan ready")

        can_work = productivity > 0

        return {
            'activity_name': activity.activity_name,
            'can_work': can_work,
            'productivity': round(productivity, 2),
            'issues': issues,
            'recommendations': recommendations,
            'weather_condition': weather.primary_condition.value,
            'temperature_range': f"{weather.temp_low}°C - {weather.temp_high}°C"
        }

    def find_optimal_days(self, forecast: List[DailyForecast],
                         activity_id: str,
                         min_productivity: float = 0.8) -> List[date]:
        """Find optimal days for an activity"""
        activity = self.activities.get(activity_id)
        if not activity:
            return []

        optimal = []
        for day in forecast:
            impact = self._calculate_impact(day, activity)
            if impact['productivity'] >= min_productivity:
                optimal.append(day.date)

        return optimal
```

### Schedule Weather Integration

```python
from datetime import date, timedelta
from typing import List, Dict
import pandas as pd

@dataclass
class ScheduledActivity:
    activity_id: str
    activity_name: str
    activity_type: str  # Maps to ACTIVITY_TEMPLATES
    planned_start: date
    planned_end: date
    duration_days: int
    is_critical: bool = False

class ScheduleWeatherOptimizer:
    """Optimize construction schedule based on weather"""

    def __init__(self, weather_service: WeatherDataService,
                 activity_analyzer: ActivityWeatherAnalyzer):
        self.weather = weather_service
        self.analyzer = activity_analyzer

    def analyze_schedule(self, schedule: List[ScheduledActivity],
                        location: Tuple[float, float]) -> Dict:
        """Analyze schedule against weather forecast"""
        forecast = self.weather.get_forecast(location[0], location[1])
        forecast_dict = {f.date: f for f in forecast}

        analysis = {
            'activities': [],
            'weather_delays': 0,
            'risk_days': [],
            'recommendations': []
        }

        for activity in schedule:
            activity_analysis = self._analyze_activity(
                activity, forecast_dict
            )
            analysis['activities'].append(activity_analysis)

            if activity_analysis['expected_delay'] > 0:
                analysis['weather_delays'] += activity_analysis['expected_delay']

            analysis['risk_days'].extend(activity_analysis['risk_days'])

        # Generate overall recommendations
        if analysis['weather_delays'] > 5:
            analysis['recommendations'].append(
                f"Schedule shows {analysis['weather_delays']} potential weather delay days. "
                "Consider buffer time or alternative scheduling."
            )

        return analysis

    def _analyze_activity(self, activity: ScheduledActivity,
                         forecast: Dict[date, DailyForecast]) -> Dict:
        """Analyze single activity against weather"""
        result = {
            'activity_id': activity.activity_id,
            'activity_name': activity.activity_name,
            'planned_start': activity.planned_start,
            'planned_end': activity.planned_end,
            'day_analysis': [],
            'risk_days': [],
            'expected_delay': 0,
            'avg_productivity': 1.0
        }

        current_date = activity.planned_start
        productivities = []
        delay_days = 0

        while current_date <= activity.planned_end:
            if current_date in forecast:
                weather = forecast[current_date]
                impact = self.analyzer._calculate_impact(
                    weather,
                    self.analyzer.activities.get(activity.activity_type,
                        self.analyzer.ACTIVITY_TEMPLATES.get('interior_work'))
                )

                productivities.append(impact['productivity'])

                day_info = {
                    'date': current_date,
                    'can_work': impact['can_work'],
                    'productivity': impact['productivity'],
                    'weather': weather.primary_condition.value
                }
                result['day_analysis'].append(day_info)

                if not impact['can_work']:
                    delay_days += 1
                    result['risk_days'].append({
                        'date': current_date,
                        'activity': activity.activity_name,
                        'reason': weather.primary_condition.value
                    })
                elif impact['productivity'] < 0.7:
                    delay_days += (1 - impact['productivity'])

            current_date += timedelta(days=1)

        result['expected_delay'] = round(delay_days)
        result['avg_productivity'] = sum(productivities) / len(productivities) if productivities else 1.0

        return result

    def suggest_reschedule(self, activity: ScheduledActivity,
                          location: Tuple[float, float],
                          flexibility_days: int = 7) -> Optional[date]:
        """Suggest better start date for activity"""
        forecast = self.weather.get_forecast(location[0], location[1])

        best_start = None
        best_avg_productivity = 0

        for offset in range(-flexibility_days, flexibility_days + 1):
            test_start = activity.planned_start + timedelta(days=offset)
            test_end = test_start + timedelta(days=activity.duration_days - 1)

            productivities = []
            for f in forecast:
                if test_start <= f.date <= test_end:
                    act_template = self.analyzer.activities.get(activity.activity_type)
                    if act_template:
                        impact = self.analyzer._calculate_impact(f, act_template)
                        productivities.append(impact['productivity'])

            if productivities:
                avg = sum(productivities) / len(productivities)
                if avg > best_avg_productivity:
                    best_avg_productivity = avg
                    best_start = test_start

        if best_start and best_start != activity.planned_start:
            return best_start
        return None

    def generate_weather_report(self, schedule: List[ScheduledActivity],
                               location: Tuple[float, float],
                               output_path: str) -> str:
        """Generate weather impact report"""
        analysis = self.analyze_schedule(schedule, location)

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary = pd.DataFrame([{
                'Total Activities': len(schedule),
                'Weather Delay Days': analysis['weather_delays'],
                'High Risk Days': len(analysis['risk_days']),
                'Recommendations': len(analysis['recommendations'])
            }])
            summary.to_excel(writer, sheet_name='Summary', index=False)

            # Activity details
            activity_data = []
            for act in analysis['activities']:
                activity_data.append({
                    'Activity': act['activity_name'],
                    'Start': act['planned_start'],
                    'End': act['planned_end'],
                    'Avg Productivity': f"{act['avg_productivity']:.0%}",
                    'Expected Delay': f"{act['expected_delay']} days"
                })
            pd.DataFrame(activity_data).to_excel(writer, sheet_name='Activities', index=False)

            # Risk days
            if analysis['risk_days']:
                pd.DataFrame(analysis['risk_days']).to_excel(
                    writer, sheet_name='Risk_Days', index=False
                )

        return output_path
```

## Quick Reference

| Activity Type | Min Temp | Max Precip | Max Wind | Rain Sensitive |
|---------------|----------|------------|----------|----------------|
| Concrete | 5°C | 2mm | 40 km/h | Yes |
| Steel Erection | -10°C | 10mm | 35 km/h | No |
| Roofing | 0°C | 0mm | 30 km/h | Yes |
| Excavation | -5°C | 25mm | 50 km/h | Partial |
| Exterior Painting | 10°C | 0mm | 25 km/h | Yes |
| Masonry | 5°C | 5mm | 40 km/h | Yes |
| Crane Operations | -15°C | 20mm | 30 km/h | No |

## Resources

- **OpenWeatherMap API**: https://openweathermap.org/api
- **Weather Underground**: https://www.wunderground.com/weather/api
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `4d-simulation` for schedule visualization
- See `risk-assessment-ml` for weather risk prediction
- See `site-logistics-optimization` for delivery scheduling
