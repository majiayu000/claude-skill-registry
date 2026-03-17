---
name: get-dates
description: Resolve target date from argument and return all date formats needed for planning rituals.
disable-model-invocation: true
allowed-tools: Bash
---

# Get Dates

This sub-skill resolves a target date from user arguments and returns all date-related fields needed by planning rituals.

## Input

The `$ARGUMENTS` variable contains the raw date argument:
- `(empty)` → today
- `today` → today
- `tomorrow` → tomorrow
- `monday`, `tuesday`, etc. → next occurrence (including today if matches)
- `next monday`, `next tuesday`, etc. → next occurrence after today
- `YYYY-MM-DD` → specific date

## Instructions

1. Parse `$ARGUMENTS` to determine the target date

2. Use macOS `date` commands to resolve relative dates:

   ```bash
   # For "tomorrow"
   date -v+1d +"%Y-%m-%d"

   # For next weekday (e.g., "monday")
   # Calculate days until next occurrence
   ```

3. Calculate all date fields for the resolved target date:

   ```bash
   # Day of week
   date -j -f "%Y-%m-%d" "$TARGET_DATE" +"%A"

   # ISO week number
   date -j -f "%Y-%m-%d" "$TARGET_DATE" +"%Y-W%V"

   # Month
   date -j -f "%Y-%m-%d" "$TARGET_DATE" +"%Y-%m"

   # Quarter
   # Q1: Jan-Mar, Q2: Apr-Jun, Q3: Jul-Sep, Q4: Oct-Dec
   ```

4. Determine relationship to today:
   - `is_today`: target date equals current date
   - `is_future`: target date is after current date
   - `is_past`: target date is before current date

## Output

Return structured JSON:

```json
{
  "target_date": "2026-02-15",
  "day_name": "Sunday",
  "day_short": "Sun",
  "week": "2026-W07",
  "month": "2026-02",
  "month_name": "February",
  "quarter": "2026-Q1",
  "year": "2026",
  "is_today": false,
  "is_future": true,
  "is_past": false,
  "days_from_today": 1
}
```

## Error Cases

- **Invalid date format**: Return error with valid format examples
- **Past date**: Allow but set `is_past: true` for caller to handle

## Example Resolutions

| Input | Target Date | Notes |
|-------|-------------|-------|
| `(empty)` | 2026-02-14 | Today |
| `today` | 2026-02-14 | Today |
| `tomorrow` | 2026-02-15 | +1 day |
| `monday` | 2026-02-16 | Next Monday (including today if Monday) |
| `next monday` | 2026-02-16 | Next Monday (always future) |
| `2026-02-20` | 2026-02-20 | Specific date |

---

## Week Resolution (for weekly rituals)

When `scope=week` is passed in arguments or the input contains an ISO week format:

### Week Input Formats
- `(empty)` → current week
- `last week` → previous week
- `YYYY-Www` → specific ISO week (e.g., 2026-W07)

### Week Calculations

```bash
# Get current ISO week
date +"%G-W%V"

# Get week start (Monday) from ISO week
# Use: date command with week calculation

# Get week end (Sunday) from ISO week
# week_end = week_start + 6 days
```

### Extended Output for Weekly Scope

When resolving weeks, include these additional fields:

```json
{
  "target_date": "2026-02-14",
  "day_name": "Saturday",
  "day_short": "Sat",
  "week": "2026-W07",
  "week_start": "2026-02-09",
  "week_end": "2026-02-15",
  "is_current_week": true,
  "is_past_week": false,
  "month": "2026-02",
  "month_name": "February",
  "quarter": "2026-Q1",
  "year": "2026",
  "is_today": false,
  "is_future": true,
  "is_past": false,
  "days_from_today": 1
}
```

### Week Resolution Examples

| Input | Target Week | Week Start | Week End |
|-------|-------------|------------|----------|
| `(empty)` scope=week | 2026-W07 | 2026-02-09 | 2026-02-15 |
| `last week` | 2026-W06 | 2026-02-02 | 2026-02-08 |
| `2026-W05` | 2026-W05 | 2026-01-26 | 2026-02-01 |

### Week Resolution Logic

1. If input matches `YYYY-Www` pattern → use directly
2. If input is `last week` → current week minus 1
3. If `scope=week` with empty input → current week
4. Calculate `week_start` as the Monday of that week
5. Calculate `week_end` as the Sunday of that week
