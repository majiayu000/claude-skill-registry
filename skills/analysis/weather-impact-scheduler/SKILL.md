---
name: "weather-impact-scheduler"
description: "Analyze weather impact on construction schedule. Predict delays and adjust activities based on forecast."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "📅", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Weather Impact Scheduler

## Technical Implementation

```python
import pandas as pd
from datetime import date, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class WeatherCondition(Enum):
    CLEAR = "clear"
    CLOUDY = "cloudy"
    RAIN = "rain"
    HEAVY_RAIN = "heavy_rain"
    SNOW = "snow"
    WIND = "wind"
    EXTREME_HEAT = "extreme_heat"
    EXTREME_COLD = "extreme_cold"


class ActivitySensitivity(Enum):
    HIGH = "high"      # Concrete, painting, roofing
    MEDIUM = "medium"  # Excavation, masonry
    LOW = "low"        # Indoor work


@dataclass
class WeatherForecast:
    forecast_date: date
    condition: WeatherCondition
    high_temp: float
    low_temp: float
    precipitation_mm: float
    wind_speed_kmh: float


@dataclass
class ScheduleActivity:
    activity_id: str
    name: str
    start_date: date
    end_date: date
    sensitivity: ActivitySensitivity
    outdoor: bool
    can_work_in_rain: bool = False
    min_temp: float = 5.0
    max_temp: float = 35.0
    max_wind: float = 50.0


@dataclass
class WeatherImpact:
    activity_id: str
    impact_date: date
    reason: str
    delay_hours: float
    recommendation: str


class WeatherImpactScheduler:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.activities: Dict[str, ScheduleActivity] = {}
        self.forecasts: Dict[date, WeatherForecast] = {}
        self.impacts: List[WeatherImpact] = []

    def add_activity(self, activity_id: str, name: str, start_date: date,
                    end_date: date, sensitivity: ActivitySensitivity,
                    outdoor: bool = True, can_work_in_rain: bool = False) -> ScheduleActivity:
        activity = ScheduleActivity(
            activity_id=activity_id,
            name=name,
            start_date=start_date,
            end_date=end_date,
            sensitivity=sensitivity,
            outdoor=outdoor,
            can_work_in_rain=can_work_in_rain
        )
        self.activities[activity_id] = activity
        return activity

    def add_forecast(self, forecast_date: date, condition: WeatherCondition,
                    high_temp: float, low_temp: float,
                    precipitation_mm: float = 0, wind_speed_kmh: float = 0):
        forecast = WeatherForecast(
            forecast_date=forecast_date,
            condition=condition,
            high_temp=high_temp,
            low_temp=low_temp,
            precipitation_mm=precipitation_mm,
            wind_speed_kmh=wind_speed_kmh
        )
        self.forecasts[forecast_date] = forecast

    def analyze_impacts(self) -> List[WeatherImpact]:
        self.impacts = []

        for activity in self.activities.values():
            if not activity.outdoor:
                continue

            current = activity.start_date
            while current <= activity.end_date:
                forecast = self.forecasts.get(current)
                if forecast:
                    impact = self._check_impact(activity, forecast)
                    if impact:
                        self.impacts.append(impact)
                current += timedelta(days=1)

        return self.impacts

    def _check_impact(self, activity: ScheduleActivity,
                     forecast: WeatherForecast) -> Optional[WeatherImpact]:
        reasons = []
        delay_hours = 0

        # Check precipitation
        if forecast.condition in [WeatherCondition.RAIN, WeatherCondition.HEAVY_RAIN]:
            if not activity.can_work_in_rain:
                if activity.sensitivity == ActivitySensitivity.HIGH:
                    reasons.append("Rain - high sensitivity activity")
                    delay_hours = 8
                else:
                    reasons.append("Rain delays")
                    delay_hours = 4

        # Check temperature
        if forecast.low_temp < activity.min_temp:
            reasons.append(f"Too cold ({forecast.low_temp}°C)")
            delay_hours = max(delay_hours, 8 if activity.sensitivity == ActivitySensitivity.HIGH else 4)

        if forecast.high_temp > activity.max_temp:
            reasons.append(f"Too hot ({forecast.high_temp}°C)")
            delay_hours = max(delay_hours, 4)

        # Check wind
        if forecast.wind_speed_kmh > activity.max_wind:
            reasons.append(f"High wind ({forecast.wind_speed_kmh} km/h)")
            delay_hours = max(delay_hours, 8)

        if reasons:
            return WeatherImpact(
                activity_id=activity.activity_id,
                impact_date=forecast.forecast_date,
                reason="; ".join(reasons),
                delay_hours=delay_hours,
                recommendation=self._get_recommendation(activity, forecast)
            )
        return None

    def _get_recommendation(self, activity: ScheduleActivity,
                           forecast: WeatherForecast) -> str:
        if forecast.condition in [WeatherCondition.RAIN, WeatherCondition.HEAVY_RAIN]:
            return "Reschedule or plan indoor work"
        if forecast.low_temp < activity.min_temp:
            return "Use heating blankets or delay start"
        if forecast.high_temp > activity.max_temp:
            return "Start early, plan heat breaks"
        if forecast.wind_speed_kmh > activity.max_wind:
            return "Secure materials, delay crane work"
        return "Monitor conditions"

    def get_total_delay_forecast(self) -> Dict[str, Any]:
        total_hours = sum(i.delay_hours for i in self.impacts)
        by_activity = {}
        for impact in self.impacts:
            act = impact.activity_id
            by_activity[act] = by_activity.get(act, 0) + impact.delay_hours

        return {
            'total_impact_hours': total_hours,
            'total_impact_days': round(total_hours / 8, 1),
            'affected_activities': len(by_activity),
            'by_activity': by_activity,
            'impact_count': len(self.impacts)
        }

    def export_analysis(self, output_path: str):
        data = [{
            'Activity': i.activity_id,
            'Date': i.impact_date,
            'Reason': i.reason,
            'Delay Hours': i.delay_hours,
            'Recommendation': i.recommendation
        } for i in self.impacts]
        pd.DataFrame(data).to_excel(output_path, index=False)
```

## Quick Start

```python
scheduler = WeatherImpactScheduler("Office Tower")

# Add activities
scheduler.add_activity("CONC-001", "Pour Slab L3", date(2024, 3, 15),
                      date(2024, 3, 20), ActivitySensitivity.HIGH, outdoor=True)

# Add forecasts
scheduler.add_forecast(date(2024, 3, 17), WeatherCondition.RAIN, 15, 8, 25, 20)

# Analyze
impacts = scheduler.analyze_impacts()
summary = scheduler.get_total_delay_forecast()
print(f"Projected delay: {summary['total_impact_days']} days")
```

## Resources
- **DDC Book**: Chapter 3.3 - Schedule Management
