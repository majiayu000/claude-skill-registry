---
name: garmer
description: Extract health and fitness data from Garmin Connect including activities, sleep, heart rate, stress, steps, and body composition. Use when the user asks about their Garmin data, fitness metrics, sleep analysis, or health insights.
license: MIT
compatibility: Requires Python 3.10+, pip/uv for installation. Requires Garmin Connect account credentials for authentication.
metadata:
  author: MoltBot Team
  version: "0.1.0"
  moltbot:
    emoji: "⌚"
    primaryEnv: "GARMER_TOKEN_DIR"
    requires:
      bins:
        - garmer
    install:
      - id: uv
        kind: uv
        package: garmer
        bins:
          - garmer
        label: Install garmer (uv)
      - id: pip
        kind: pip
        package: garmer
        bins:
          - garmer
        label: Install garmer (pip)
---

# Garmer - Garmin Data Extraction Skill

This skill enables extraction of health and fitness data from Garmin Connect for analysis and insights.

## Prerequisites

1. A Garmin Connect account with health data
2. The `garmer` CLI tool installed (see installation options in metadata)

## Authentication (One-Time Setup)

Before using garmer, authenticate with Garmin Connect:

```bash
garmer login
```

This will prompt for your Garmin Connect email and password. Tokens are saved to `~/.garmer/garmin_tokens` for future use.

To check authentication status:

```bash
garmer status
```

## Available Commands

### Daily Summary

Get today's health summary (steps, calories, heart rate, stress):

```bash
garmer summary
# For a specific date:
garmer summary --date 2025-01-15
# Include last night's sleep data:
garmer summary --with-sleep
garmer summary -s
# JSON output for programmatic use:
garmer summary --json
# Combine flags:
garmer summary --date 2025-01-15 --with-sleep --json
```

### Sleep Data

Get sleep analysis (duration, phases, score, HRV):

```bash
garmer sleep
# For a specific date:
garmer sleep --date 2025-01-15
```

### Activities

List recent fitness activities:

```bash
garmer activities
# Limit number of results:
garmer activities --limit 5
# Filter by specific date:
garmer activities --date 2025-01-15
# JSON output for programmatic use:
garmer activities --json
```

### Activity Detail

Get detailed information for a single activity:

```bash
# Latest activity:
garmer activity
# Specific activity by ID:
garmer activity 12345678
# Include lap data:
garmer activity --laps
# Include heart rate zone data:
garmer activity --zones
# JSON output:
garmer activity --json
# Combine flags:
garmer activity 12345678 --laps --zones --json
```

### Health Snapshot

Get comprehensive health data for a day:

```bash
garmer snapshot
# For a specific date:
garmer snapshot --date 2025-01-15
# As JSON for programmatic use:
garmer snapshot --json
```

### Export Data

Export multiple days of data to JSON:

```bash
# Last 7 days (default)
garmer export

# Custom date range
garmer export --start-date 2025-01-01 --end-date 2025-01-31 --output my_data.json

# Last N days
garmer export --days 14
```

### Utility Commands

```bash
# Update garmer to latest version (git pull):
garmer update

# Show version information:
garmer version
```

## Python API Usage

For more complex data processing, use the Python API:

```python
from garmer import GarminClient
from datetime import date, timedelta

# Use saved tokens
client = GarminClient.from_saved_tokens()

# Or login with credentials
client = GarminClient.from_credentials(email="user@example.com", password="pass")
```

### User Profile

```python
# Get user profile
profile = client.get_user_profile()
print(f"User: {profile.display_name}")

# Get registered devices
devices = client.get_user_devices()
```

### Daily Summary

```python
# Get daily summary (defaults to today)
summary = client.get_daily_summary()
print(f"Steps: {summary.total_steps}")

# Get for specific date
summary = client.get_daily_summary(date(2025, 1, 15))

# Get weekly summary
weekly = client.get_weekly_summary()
```

### Sleep Data

```python
# Get sleep data (defaults to today)
sleep = client.get_sleep()
print(f"Sleep: {sleep.total_sleep_hours:.1f} hours")

# Get last night's sleep
sleep = client.get_last_night_sleep()

# Get sleep for date range
sleep_data = client.get_sleep_range(
    start_date=date(2025, 1, 1),
    end_date=date(2025, 1, 7)
)
```

### Activities

```python
# Get recent activities
activities = client.get_recent_activities(limit=5)
for activity in activities:
    print(f"{activity.activity_name}: {activity.distance_km:.1f} km")

# Get activities with filters
activities = client.get_activities(
    start_date=date(2025, 1, 1),
    end_date=date(2025, 1, 31),
    activity_type="running",
    limit=20
)

# Get single activity by ID
activity = client.get_activity(12345678)
```

### Heart Rate

```python
# Get heart rate data for a day
hr = client.get_heart_rate()
print(f"Resting HR: {hr.resting_heart_rate} bpm")

# Get just resting heart rate
resting_hr = client.get_resting_heart_rate(date(2025, 1, 15))
```

### Stress & Body Battery

```python
# Get stress data
stress = client.get_stress()
print(f"Avg stress: {stress.avg_stress_level}")

# Get body battery data
battery = client.get_body_battery()
```

### Steps

```python
# Get detailed step data
steps = client.get_steps()
print(f"Total: {steps.total_steps}, Goal: {steps.step_goal}")

# Get just total steps
total = client.get_total_steps(date(2025, 1, 15))
```

### Body Composition

```python
# Get latest weight
weight = client.get_latest_weight()
print(f"Weight: {weight.weight_kg} kg")

# Get weight for specific date
weight = client.get_weight(date(2025, 1, 15))

# Get full body composition
body = client.get_body_composition()
```

### Hydration & Respiration

```python
# Get hydration data
hydration = client.get_hydration()
print(f"Intake: {hydration.total_intake_ml} ml")

# Get respiration data
resp = client.get_respiration()
print(f"Avg breathing: {resp.avg_waking_respiration} breaths/min")
```

### Comprehensive Reports

```python
# Get health snapshot (all metrics for a day)
snapshot = client.get_health_snapshot()
# Returns: daily_summary, sleep, heart_rate, stress, steps, hydration, respiration

# Get weekly health report with trends
report = client.get_weekly_health_report()
# Returns: activities summary, sleep stats, steps stats, HR trends, stress trends

# Export data for date range
data = client.export_data(
    start_date=date(2025, 1, 1),
    end_date=date(2025, 1, 31),
    include_activities=True,
    include_sleep=True,
    include_daily=True
)
```

## Common Workflows

### Health Check Query

When a user asks "How did I sleep?" or "What's my health summary?":

```bash
garmer snapshot --json
```

### Activity Analysis

When a user asks about workouts or exercise:

```bash
garmer activities --limit 10
```

### Trend Analysis

When analyzing health trends over time:

```bash
garmer export --days 30 --output health_data.json
```

Then process the JSON file with Python for analysis.

## Data Types Available

- **Activities**: Running, cycling, swimming, strength training, etc.
- **Sleep**: Duration, phases (deep, light, REM), score, HRV
- **Heart Rate**: Resting HR, samples, zones
- **Stress**: Stress levels, body battery
- **Steps**: Total steps, distance, floors
- **Body Composition**: Weight, body fat, muscle mass
- **Hydration**: Water intake tracking
- **Respiration**: Breathing rate data

## Error Handling

If not authenticated:

```
Not logged in. Use 'garmer login' first.
```

If session expired, re-authenticate:

```bash
garmer login
```

## Environment Variables

- `GARMER_TOKEN_DIR`: Custom directory for token storage
- `GARMER_LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)
- `GARMER_CACHE_ENABLED`: Enable/disable data caching (true/false)

## References

For detailed API documentation and MoltBot integration examples, see `references/REFERENCE.md`.
