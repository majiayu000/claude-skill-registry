---
name: hevy
description: Comprehensive fitness tracking integration with Hevy app. Use when needing to track workouts, analyze exercise progress, get fitness statistics, create/manage routines, or query workout history. Supports JSON output for structured analysis. Requires Hevy Pro subscription for API access.
---

# Hevy Fitness Tracking

Integrate with Hevy app for comprehensive fitness tracking, workout analysis, and progress monitoring.

## Prerequisites

- **Hevy Pro subscription** (required for API access)
- **API key** from [Hevy Developer Settings](https://hevy.com/settings?developer)

## Quick Start

### 1. Install hevycli

```bash
./scripts/install_hevycli.sh
```

### 2. Configure API Key

```bash
./scripts/configure_api.sh YOUR_API_KEY
```

### 3. Test Installation

```bash
hevycli workout count --output json
```

## Core Operations

### Workout Tracking

**List recent workouts:**

```bash
hevycli workout list --since 2026-02-01 --output json
```

**Get specific workout details:**

```bash
hevycli workout get <workout-id> --output json
```

**Get workout count:**

```bash
hevycli workout count --output json
```

### Progress Analysis

**Track exercise progression:**

```bash
hevycli stats progress "Bench Press" --output json
hevycli stats progress "Squat" --metric 1rm --output json
```

**Get workout summaries:**

```bash
hevycli stats summary --period month --output json
hevycli stats summary --period week --output json
```

**View personal records:**

```bash
hevycli stats records --output json
hevycli stats records --exercise "Bench Press" --output json
```

### Exercise Management

**Search for exercises:**

```bash
hevycli exercise search "bench" --output json
```

**List exercise templates:**

```bash
hevycli exercise list --output json
```

### Routine Management

**List routines:**

```bash
hevycli routine list --output json
```

**Get routine details:**

```bash
hevycli routine get <routine-id> --output json
```

## Convenience Scripts

### Recent Activity Analysis

```bash
# Last 7 days of workouts
./scripts/get_recent_workouts.sh 7 json

# Last 30 days
./scripts/get_recent_workouts.sh 30 json
```

### Progress Tracking

```bash
# Weight progression
./scripts/track_progress.sh "Bench Press" weight json

# Estimated 1RM progression  
./scripts/track_progress.sh "Deadlift" 1rm json
```

### Statistics Overview

```bash
# Monthly stats with records
./scripts/get_stats.sh month json

# Weekly overview
./scripts/get_stats.sh week json
```

## Integration Patterns

### Body Status Tracking

**Daily workout summary:**

```bash
# Check if workout completed today
TODAY=$(date +%Y-%m-%d)
hevycli workout list --since $TODAY --output json | jq '.[] | {title, duration_minutes: (.end_time | fromdate) - (.start_time | fromdate) | . / 60}'
```

**Weekly volume analysis:**

```bash
WEEK_AGO=$(date -d '7 days ago' +%Y-%m-%d)
hevycli workout list --since $WEEK_AGO --output json | jq 'map(.exercises[].sets | map(.weight_kg * .reps) | add) | add'
```

**Progress toward goals:**

```bash
# Track specific lift PRs
hevycli stats records --exercise "Bench Press" --output json | jq '.records[0].weight_kg'
```

### RPG Integration

Each workout can be treated as a quest with XP based on:

- **Volume:** Total weight lifted
- **Duration:** Time spent training  
- **Consistency:** Streak tracking via workout frequency
- **Progress:** PRs and strength gains

**XP Calculation Example:**

```bash
# Get today's workout volume for XP calculation
hevycli workout list --since $(date +%Y-%m-%d) --output json | \
jq '[.[].exercises[].sets[] | (.weight_kg // 0) * (.reps // 0)] | add // 0'
```

## Data Formats

All commands support `--output json` for structured agent consumption. See `references/data_structures.md` for complete JSON schema examples.

### Key Fields

- **Workouts:** id, title, start_time, end_time, exercises, notes
- **Exercises:** title, muscle_groups, sets (weight_kg, reps, rpe)
- **Stats:** total_workouts, total_volume_kg, average_duration_minutes
- **Records:** exercise, weight_kg, reps, date, estimated_1rm_kg

## Configuration

Config file location: `~/.hevycli/config.yaml`

**Recommended agent settings:**

```yaml
api:
  key: "your-api-key"
display:
  output_format: json
  color: false
  units: metric
```

## Troubleshooting

### API Issues

- **401 Unauthorized:** Check API key and Hevy Pro subscription
- **Rate Limiting:** Hevy API has rate limits - space out requests
- **Network Errors:** Check internet connection

### Installation Issues

- **Binary not found:** Ensure `~/.local/bin` is in PATH
- **Permission errors:** Make scripts executable: `chmod +x scripts/*.sh`

## References

- **Command Reference:** `references/api_commands.md` - Complete CLI command guide
- **Data Structures:** `references/data_structures.md` - JSON schemas and examples
- **Hevy API Docs:** https://api.hevyapp.com/docs/
- **Hevy App:** https://www.hevyapp.com/

## Security Notes

- API key stored in `~/.hevycli/config.yaml` or env variable HEVY_API_KEY
- Ensure proper file permissions (600) on config file
- Never commit API keys to version control
- API key provides read/write access to all Hevy data