---
name: terra-data
description: Terra API health data retrieval and management. Use when fetching activity, sleep, body, daily, nutrition, menstruation, or athlete data from wearables.
---

# Terra Data Retrieval

Fetch and manage health data from 150+ wearable devices via Terra API.

## Data Types Overview

| Type | Description | Update Frequency |
|------|-------------|------------------|
| **Activity** | Workout sessions with metrics | Per workout completion |
| **Sleep** | Sleep stages, duration, HRV | Per sleep session |
| **Body** | Weight, body composition, glucose | Multiple times/day |
| **Daily** | Aggregated daily summaries | Multiple times/day |
| **Nutrition** | Meals, macros, calories | Per meal logged |
| **Menstruation** | Cycle tracking, symptoms | Per update |
| **Athlete** | User profile, demographics | On change |

## Quick Start

```python
from terra import Terra
from datetime import datetime, timedelta

client = Terra(
    dev_id=os.environ["TERRA_DEV_ID"],
    api_key=os.environ["TERRA_API_KEY"]
)

# Get last 7 days of activity data
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

response = client.activity.get(
    user_id="terra_user_abc123",
    start_date=start_date,
    end_date=end_date
)

for activity in response.data:
    print(f"{activity.metadata.type}: {activity.calories_data.total_burned_calories} cal")
```

## Operations

### `get-activity`
Retrieve completed workout sessions.

```python
def get_activity(
    client: Terra,
    user_id: str,
    start_date: datetime,
    end_date: datetime,
    to_webhook: bool = False
) -> list:
    """
    Get activity/workout data.

    Returns sessions with:
    - Duration, calories burned
    - Heart rate (avg, max, min, samples)
    - Distance, steps, floors
    - GPS position/polyline
    - Power, cadence (cycling)
    """
    response = client.activity.get(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        to_webhook=to_webhook  # True for async processing
    )

    return response.data
```

**Sample Activity Response**:
```json
{
  "data": [{
    "metadata": {
      "start_time": "2025-12-05T07:00:00Z",
      "end_time": "2025-12-05T08:00:00Z",
      "type": "running"
    },
    "calories_data": {
      "total_burned_calories": 450,
      "net_activity_calories": 350
    },
    "heart_rate_data": {
      "summary": { "avg_hr_bpm": 145, "max_hr_bpm": 175 }
    },
    "distance_data": { "distance_meters": 8500 },
    "movement_data": { "steps_count": 8500 }
  }]
}
```

### `get-sleep`
Retrieve sleep sessions with stages.

```python
def get_sleep(
    client: Terra,
    user_id: str,
    start_date: datetime,
    end_date: datetime
) -> list:
    """
    Get sleep data.

    Returns sessions with:
    - Sleep stages (deep, light, REM, awake)
    - Duration in bed vs asleep
    - Sleep efficiency
    - HRV, respiratory rate
    - Temperature deviation
    """
    response = client.sleep.get(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )

    return response.data
```

**Sample Sleep Response**:
```json
{
  "data": [{
    "metadata": {
      "start_time": "2025-12-04T22:30:00Z",
      "end_time": "2025-12-05T06:30:00Z"
    },
    "sleep_durations_data": {
      "duration_in_bed_seconds": 28800,
      "duration_asleep_seconds": 26400,
      "sleep_efficiency": 0.92
    },
    "asleep": {
      "duration_deep_sleep_state_seconds": 5400,
      "duration_light_sleep_state_seconds": 14400,
      "duration_REM_sleep_state_seconds": 6600
    },
    "awake": {
      "num_wakeup_events": 2,
      "sleep_latency_seconds": 600
    },
    "heart_rate_data": {
      "summary": { "resting_hr_bpm": 52 }
    }
  }]
}
```

### `get-daily`
Retrieve aggregated daily summaries.

```python
def get_daily(
    client: Terra,
    user_id: str,
    start_date: datetime,
    end_date: datetime
) -> list:
    """
    Get daily aggregated data.

    Returns summaries with:
    - Steps, calories, distance
    - Active minutes, floors
    - Resting heart rate, HRV
    - Recovery scores
    - Stress data

    Note: Sent multiple times/day - always OVERWRITE previous data.
    """
    response = client.daily.get(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )

    return response.data
```

**Sample Daily Response**:
```json
{
  "data": [{
    "metadata": {
      "start_time": "2025-12-05T00:00:00Z",
      "end_time": "2025-12-05T23:59:59Z"
    },
    "calories_data": {
      "total_burned_calories": 2400,
      "BMR_calories": 1600,
      "net_activity_calories": 800
    },
    "movement_data": {
      "steps_count": 10500,
      "floors_climbed": 12
    },
    "heart_rate_data": {
      "summary": { "resting_hr_bpm": 58 }
    },
    "scores": {
      "recovery": { "score": 82 },
      "activity": { "score": 75 },
      "sleep": { "score": 88 }
    }
  }]
}
```

### `get-body`
Retrieve body metrics and biometrics.

```python
def get_body(
    client: Terra,
    user_id: str,
    start_date: datetime,
    end_date: datetime
) -> list:
    """
    Get body metrics data.

    Returns measurements including:
    - Weight, height, BMI
    - Body fat %, muscle mass
    - Blood glucose (CGM)
    - Blood pressure
    - Temperature
    - SpO2

    Note: Sent multiple times/day - always OVERWRITE previous data.
    """
    response = client.body.get(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )

    return response.data
```

**Sample Body Response**:
```json
{
  "data": [{
    "metadata": {
      "start_time": "2025-12-05T00:00:00Z",
      "end_time": "2025-12-05T23:59:59Z"
    },
    "body_metrics": {
      "weight_kg": 75.5,
      "height_cm": 178,
      "BMI": 23.8,
      "body_fat_percentage": 18.5
    },
    "blood_glucose_data": {
      "blood_glucose_samples": [
        { "glucose_mg_per_dL": 95, "timestamp": "2025-12-05T07:00:00Z" },
        { "glucose_mg_per_dL": 120, "timestamp": "2025-12-05T08:30:00Z" }
      ]
    },
    "blood_pressure_data": {
      "systolic_bp_mmHg": 120,
      "diastolic_bp_mmHg": 80
    }
  }]
}
```

### `get-nutrition`
Retrieve nutrition and meal data.

```python
def get_nutrition(
    client: Terra,
    user_id: str,
    start_date: datetime,
    end_date: datetime
) -> list:
    """
    Get nutrition data.

    Returns meal logs with:
    - Calories, macros (protein, carbs, fat)
    - Micronutrients
    - Individual food items
    - Meal timestamps
    """
    response = client.nutrition.get(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )

    return response.data
```

**Sample Nutrition Response**:
```json
{
  "data": [{
    "metadata": {
      "start_time": "2025-12-05T00:00:00Z",
      "end_time": "2025-12-05T23:59:59Z"
    },
    "summary": {
      "macros": {
        "calories": 2200,
        "protein_g": 120,
        "carbohydrates_g": 250,
        "fat_g": 70,
        "fiber_g": 30
      }
    },
    "meals": [
      {
        "name": "Breakfast",
        "timestamp": "2025-12-05T08:00:00Z",
        "macros": { "calories": 450, "protein_g": 25 }
      }
    ]
  }]
}
```

### `get-menstruation`
Retrieve menstrual cycle data.

```python
def get_menstruation(
    client: Terra,
    user_id: str,
    start_date: datetime,
    end_date: datetime
) -> list:
    """
    Get menstruation/cycle data.

    Returns tracking data including:
    - Cycle phase, day in cycle
    - Flow level, symptoms
    - Predictions
    """
    response = client.menstruation.get(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )

    return response.data
```

### `get-athlete`
Retrieve user profile information.

```python
def get_athlete(
    client: Terra,
    user_id: str
) -> dict:
    """
    Get user profile/athlete data.

    Returns profile including:
    - Name, email (if available)
    - Date of birth, age
    - Sex, gender
    - Location
    - Connected devices
    """
    response = client.athlete.get(user_id=user_id)
    return response.data
```

## Bulk Data Retrieval

### Get All Data Types

```python
async def get_all_user_data(
    client: Terra,
    user_id: str,
    start_date: datetime,
    end_date: datetime
) -> dict:
    """Fetch all data types for a user."""

    return {
        "activity": client.activity.get(user_id, start_date, end_date).data,
        "sleep": client.sleep.get(user_id, start_date, end_date).data,
        "daily": client.daily.get(user_id, start_date, end_date).data,
        "body": client.body.get(user_id, start_date, end_date).data,
        "nutrition": client.nutrition.get(user_id, start_date, end_date).data,
    }
```

### Historical Backfill

```python
def backfill_user_data(
    client: Terra,
    user_id: str,
    days_back: int = 90
) -> dict:
    """
    Backfill historical data for newly connected user.

    Note: Requests >28 days are processed asynchronously
    and results sent via webhook.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    # For requests >28 days, use to_webhook=True
    if days_back > 28:
        # Async - results via webhook
        client.activity.get(user_id, start_date, end_date, to_webhook=True)
        client.sleep.get(user_id, start_date, end_date, to_webhook=True)
        client.daily.get(user_id, start_date, end_date, to_webhook=True)
        return {"status": "processing", "message": "Results via webhook"}
    else:
        # Sync - immediate response
        return get_all_user_data(client, user_id, start_date, end_date)
```

## Provider Historical Data Limits

| Provider | Max Historical Data |
|----------|---------------------|
| Garmin | 5 years |
| Fitbit | 10 years |
| Oura | 3 years |
| WHOOP | 2 years |
| Polar | 30 days |
| COROS | 3 months |
| Withings | 2 years |

## Data Normalization

Terra normalizes all provider data into consistent schemas:

### Unique Identifiers
- **Activity/Sleep**: `start_time` + `end_time` = unique session
- **Daily/Body/Nutrition**: Date-based, OVERWRITE on updates

### Update Strategy

```python
def handle_data_update(data_type: str, payload: dict):
    """Handle incoming data with proper update strategy."""

    unique_key = f"{payload['user']['user_id']}:{payload['metadata']['start_time']}:{payload['metadata']['end_time']}"

    if data_type in ["daily", "body", "nutrition"]:
        # OVERWRITE - these update multiple times per day
        db.upsert(unique_key, payload)
    else:
        # INSERT OR IGNORE - sessions are unique
        db.insert_if_not_exists(unique_key, payload)
```

## Writing Data (Limited Providers)

Some providers support writing data back:

```python
# Post activity to Wahoo
client.activity.post(
    user_id="terra_user_abc123",
    data={
        "type": "cycling",
        "start_time": "2025-12-05T10:00:00Z",
        "end_time": "2025-12-05T11:00:00Z",
        "calories": 500,
        "distance_meters": 25000
    }
)

# Post nutrition to Fitbit
client.nutrition.post(
    user_id="terra_user_abc123",
    data={
        "meals": [{
            "name": "Lunch",
            "calories": 650,
            "protein_g": 35
        }]
    }
)

# Post planned workout to Apple Health
client.planned_workout.post(
    user_id="terra_user_abc123",
    data={
        "name": "5K Training",
        "type": "running",
        "phases": [
            {"type": "warmup", "duration_seconds": 300},
            {"type": "interval", "duration_seconds": 600}
        ]
    }
)
```

## Database Schema

```sql
-- Activity sessions
CREATE TABLE terra_activities (
    id SERIAL PRIMARY KEY,
    terra_user_id VARCHAR(255),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    activity_type VARCHAR(50),
    calories INTEGER,
    distance_meters FLOAT,
    avg_heart_rate INTEGER,
    data JSONB,
    UNIQUE(terra_user_id, start_time, end_time)
);

-- Daily summaries (UPSERT)
CREATE TABLE terra_daily (
    id SERIAL PRIMARY KEY,
    terra_user_id VARCHAR(255),
    date DATE,
    steps INTEGER,
    calories INTEGER,
    distance_meters FLOAT,
    resting_heart_rate INTEGER,
    data JSONB,
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(terra_user_id, date)
);
```

## Related Skills

- **terra-auth**: Authentication setup
- **terra-connections**: Connect users
- **terra-webhooks**: Real-time data delivery
- **terra-sdk**: SDK integration
