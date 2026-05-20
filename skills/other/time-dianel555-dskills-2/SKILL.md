---
name: time
description: |
  Time and timezone utilities for getting current time and converting between timezones. Use when: (1) Getting current time in any timezone, (2) Converting time between different timezones, (3) Working with IANA timezone names, (4) Scheduling across timezones, (5) Time-sensitive operations. Triggers: "what time is it", "current time", "convert time", "timezone", "time in [city]".
---

# Time

Time and timezone conversion utilities. Standalone CLI only (no MCP dependency).

## Execution Methods

Run `scripts/time_cli.py` via Bash:

```bash
# Prerequisites: pip install pytz (or use Python 3.9+ with zoneinfo)

# Get current time in a timezone
python scripts/time_cli.py get --timezone "Asia/Shanghai"
python scripts/time_cli.py get --timezone "America/New_York"
python scripts/time_cli.py get  # Uses system timezone

# Convert time between timezones
python scripts/time_cli.py convert \
  --time "16:30" \
  --from "America/New_York" \
  --to "Asia/Tokyo"

# List available timezones
python scripts/time_cli.py list [--filter "Asia"]
```

## Tool Capability Matrix

| Tool | Parameters | Output |
|------|------------|--------|
| `get_current_time` | `timezone` (required, IANA name) | `{timezone, datetime, is_dst}` |
| `convert_time` | `source_timezone`, `time` (HH:MM), `target_timezone` | `{source, target, time_difference}` |

## Common IANA Timezone Names

| Region | Timezone |
|--------|----------|
| China | `Asia/Shanghai` |
| Japan | `Asia/Tokyo` |
| Korea | `Asia/Seoul` |
| US East | `America/New_York` |
| US West | `America/Los_Angeles` |
| UK | `Europe/London` |
| Germany | `Europe/Berlin` |
| France | `Europe/Paris` |
| Australia | `Australia/Sydney` |
| UTC | `UTC` |

## Workflow

### Getting Current Time
1. Identify target timezone (use IANA name)
2. Call `get_current_time` with timezone parameter
3. Response includes ISO 8601 datetime and DST status

### Converting Time
1. Identify source timezone and time (24-hour format HH:MM)
2. Identify target timezone
3. Call `convert_time` with all parameters
4. Response includes both times and time difference

## Output Format

### get_current_time Response
```json
{
  "timezone": "Asia/Shanghai",
  "datetime": "2024-01-01T21:00:00+08:00",
  "is_dst": false
}
```

### convert_time Response
```json
{
  "source": {
    "timezone": "America/New_York",
    "datetime": "2024-01-01T16:30:00-05:00",
    "is_dst": false
  },
  "target": {
    "timezone": "Asia/Tokyo",
    "datetime": "2024-01-02T06:30:00+09:00",
    "is_dst": false
  },
  "time_difference": "+14.0h"
}
```

## Error Handling

| Error | Recovery |
|-------|----------|
| Invalid timezone | Check IANA timezone name spelling |
| Invalid time format | Use 24-hour format HH:MM |
| MCP unavailable | Fall back to CLI script |

## Anti-Patterns

| Prohibited | Correct |
|------------|---------|
| Use city names directly | Use IANA timezone names (e.g., `Asia/Tokyo` not `Tokyo`) |
| Use 12-hour format | Use 24-hour format (e.g., `16:30` not `4:30 PM`) |
| Assume timezone | Always specify timezone explicitly |
