---
name: cron-expression-builder
description: Build and validate cron expressions from natural language. Convert between human-readable schedules and cron syntax with next run preview.
---

# Cron Expression Builder

Build, parse, and validate cron expressions with natural language conversion and run time preview.

## Features

- **Natural Language**: Convert descriptions to cron expressions
- **Cron Parser**: Parse cron to human-readable format
- **Validation**: Validate cron syntax
- **Next Runs**: Preview upcoming execution times
- **Presets**: Common scheduling patterns
- **Both Formats**: 5-field (standard) and 6-field (with seconds)

## Quick Start

```python
from cron_builder import CronBuilder

builder = CronBuilder()

# Build from natural language
cron = builder.from_text("every day at 3:30 PM")
print(cron)  # 30 15 * * *

# Parse to human-readable
description = builder.describe("0 */2 * * *")
print(description)  # "Every 2 hours"

# Get next run times
runs = builder.next_runs("30 15 * * *", count=5)
for run in runs:
    print(run)
```

## CLI Usage

```bash
# Build from text
python cron_builder.py --from-text "every monday at 9am"

# Describe a cron expression
python cron_builder.py --describe "0 9 * * 1"

# Validate expression
python cron_builder.py --validate "0 9 * * 1"

# Get next 10 runs
python cron_builder.py --next "0 9 * * 1" --count 10

# List preset schedules
python cron_builder.py --presets

# Use preset
python cron_builder.py --preset daily_midnight

# Interactive builder
python cron_builder.py --interactive
```

## API Reference

### CronBuilder Class

```python
class CronBuilder:
    def __init__(self, with_seconds: bool = False)

    # Building
    def from_text(self, text: str) -> str
    def build(self, minute: str = "*", hour: str = "*",
             day: str = "*", month: str = "*",
             weekday: str = "*") -> str

    # Parsing
    def describe(self, expression: str) -> str
    def parse(self, expression: str) -> dict

    # Validation
    def validate(self, expression: str) -> dict
    def is_valid(self, expression: str) -> bool

    # Execution times
    def next_runs(self, expression: str, count: int = 5,
                 from_date: datetime = None) -> list
    def matches(self, expression: str, dt: datetime) -> bool

    # Presets
    def get_preset(self, name: str) -> str
    def list_presets(self) -> dict
```

## Cron Expression Format

### 5-Field Format (Standard)

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sun=0)
│ │ │ │ │
* * * * *
```

### 6-Field Format (With Seconds)

```
┌───────────── second (0-59)
│ ┌───────────── minute (0-59)
│ │ ┌───────────── hour (0-23)
│ │ │ ┌───────────── day of month (1-31)
│ │ │ │ ┌───────────── month (1-12)
│ │ │ │ │ ┌───────────── day of week (0-6)
│ │ │ │ │ │
* * * * * *
```

## Natural Language Conversion

### Supported Patterns

```python
# Time-based
builder.from_text("every minute")        # * * * * *
builder.from_text("every 5 minutes")     # */5 * * * *
builder.from_text("every hour")          # 0 * * * *
builder.from_text("every 2 hours")       # 0 */2 * * *

# Daily
builder.from_text("every day at noon")   # 0 12 * * *
builder.from_text("daily at 3pm")        # 0 15 * * *
builder.from_text("at 3:30 PM every day")# 30 15 * * *

# Weekly
builder.from_text("every monday")        # 0 0 * * 1
builder.from_text("weekdays at 9am")     # 0 9 * * 1-5
builder.from_text("every friday at 5pm") # 0 17 * * 5

# Monthly
builder.from_text("first of every month")# 0 0 1 * *
builder.from_text("15th of each month")  # 0 0 15 * *
builder.from_text("last day of month")   # 0 0 L * *

# Special
builder.from_text("every sunday at midnight") # 0 0 * * 0
builder.from_text("twice daily")         # 0 0,12 * * *
```

## Presets

Built-in common schedules:

| Preset | Cron | Description |
|--------|------|-------------|
| `every_minute` | `* * * * *` | Every minute |
| `every_5_minutes` | `*/5 * * * *` | Every 5 minutes |
| `every_15_minutes` | `*/15 * * * *` | Every 15 minutes |
| `every_30_minutes` | `*/30 * * * *` | Every 30 minutes |
| `hourly` | `0 * * * *` | Every hour |
| `daily_midnight` | `0 0 * * *` | Daily at midnight |
| `daily_noon` | `0 12 * * *` | Daily at noon |
| `weekly_sunday` | `0 0 * * 0` | Weekly on Sunday |
| `weekly_monday` | `0 0 * * 1` | Weekly on Monday |
| `monthly` | `0 0 1 * *` | First of month |
| `quarterly` | `0 0 1 1,4,7,10 *` | First day of quarter |
| `yearly` | `0 0 1 1 *` | January 1st |

```python
cron = builder.get_preset("daily_noon")
# "0 12 * * *"
```

## Cron Description

Convert cron to human-readable:

```python
builder.describe("30 15 * * 1-5")
# "At 3:30 PM, Monday through Friday"

builder.describe("0 */6 * * *")
# "Every 6 hours"

builder.describe("0 9 15 * *")
# "At 9:00 AM on day 15 of every month"
```

## Validation

```python
result = builder.validate("0 9 * * 1")

# Returns:
{
    "valid": True,
    "expression": "0 9 * * 1",
    "fields": {
        "minute": "0",
        "hour": "9",
        "day_of_month": "*",
        "month": "*",
        "day_of_week": "1"
    },
    "description": "At 9:00 AM, only on Monday"
}

# Invalid expression
result = builder.validate("60 25 * * *")
# Returns:
{
    "valid": False,
    "error": "Invalid minute: 60 (must be 0-59)"
}
```

## Next Run Times

Preview upcoming executions:

```python
runs = builder.next_runs("0 9 * * 1", count=5)

# Returns:
[
    "2024-01-15 09:00:00",  # Next Monday
    "2024-01-22 09:00:00",
    "2024-01-29 09:00:00",
    "2024-02-05 09:00:00",
    "2024-02-12 09:00:00"
]
```

### Check Specific Time

```python
from datetime import datetime

# Does this cron run at this time?
matches = builder.matches("0 9 * * 1", datetime(2024, 1, 15, 9, 0))
# True (Monday at 9 AM)
```

## Manual Building

Build expression field by field:

```python
# Every Monday at 9:30 AM
cron = builder.build(
    minute="30",
    hour="9",
    day="*",
    month="*",
    weekday="1"
)
# "30 9 * * 1"

# Every 15 minutes during business hours on weekdays
cron = builder.build(
    minute="*/15",
    hour="9-17",
    day="*",
    month="*",
    weekday="1-5"
)
# "*/15 9-17 * * 1-5"
```

## Example Workflows

### Schedule Builder

```python
builder = CronBuilder()

# Create schedule from user input
schedule_text = "every weekday at 8:30 AM"
cron = builder.from_text(schedule_text)

# Validate and preview
if builder.is_valid(cron):
    print(f"Cron: {cron}")
    print(f"Description: {builder.describe(cron)}")
    print("\nNext 5 runs:")
    for run in builder.next_runs(cron, count=5):
        print(f"  {run}")
```

### Job Scheduler Integration

```python
# Define schedules for different jobs
jobs = {
    "backup": builder.get_preset("daily_midnight"),
    "reports": builder.from_text("every monday at 8am"),
    "cleanup": builder.from_text("first sunday of month at 2am")
}

for job_name, cron in jobs.items():
    print(f"{job_name}: {cron}")
    print(f"  Next run: {builder.next_runs(cron, count=1)[0]}")
```

## Dependencies

- croniter>=1.4.0 (for next run calculations)
