---
name: healthkit-cli
description: Seed and verify HealthKit data in running Expo apps using the apple-health CLI
---

Use `bunx apple-health` to interact with HealthKit through a running Expo app's devtools connection.

## Prerequisites

The app must have the devtools hook enabled:

```tsx
import { useHealthKitDevTools } from "apple-health/dev-tools";

export default function App() {
  useHealthKitDevTools();
  // ...
}
```

Verify connection:

```bash
bunx apple-health status
```

## Seeding Data

### Quick Start

Use batch mode for efficient bulk writes. Create NDJSON data and pipe to the CLI:

```bash
cat << 'EOF' | bunx apple-health batch
{"kind":"quantity","type":"heartRate","value":72,"start":"today 8am"}
{"kind":"quantity","type":"stepCount","value":8500,"start":"yesterday","duration":"1d"}
{"kind":"category","type":"sleepAnalysis","value":4,"start":"-8h","duration":"2h"}
{"kind":"workout","activityType":"running","start":"-2h","duration":"45m","energy":450}
EOF
```

### Sample Types

**Quantity samples** (measurements with values):

```json
{"kind":"quantity","type":"heartRate","value":72,"start":"today 8am"}
{"kind":"quantity","type":"stepCount","value":10000,"start":"yesterday","duration":"1d"}
{"kind":"quantity","type":"dietaryCaffeine","value":150,"start":"today 7am"}
{"kind":"quantity","type":"activeEnergyBurned","value":350,"start":"today","duration":"1d"}
{"kind":"quantity","type":"bodyMass","value":75,"unit":"kg","start":"today 7am"}
```

**Category samples** (events/states with enum values):

```json
{"kind":"category","type":"sleepAnalysis","value":3,"start":"-7h","duration":"6h"}
{"kind":"category","type":"headache","value":2,"start":"today 2pm"}
{"kind":"category","type":"mindfulSession","value":0,"start":"-1h","duration":"15m"}
```

**Workouts**:

```json
{"kind":"workout","activityType":"running","start":"-1h","duration":"30m","energy":300,"distance":5000}
{"kind":"workout","activityType":"cycling","start":"today 7am","duration":"1h","energy":500,"distance":25000}
{"kind":"workout","activityType":"yoga","start":"yesterday 6am","duration":"45m","energy":150}
```

### Sleep Values

| Value | Meaning            |
| ----- | ------------------ |
| 0     | In Bed             |
| 2     | Awake              |
| 3     | Core Sleep (light) |
| 4     | Deep Sleep         |
| 5     | REM Sleep          |

Realistic sleep pattern example:

```json
{"kind":"category","type":"sleepAnalysis","value":0,"start":"-8h","duration":"8h"}
{"kind":"category","type":"sleepAnalysis","value":3,"start":"-7h45m","duration":"45m"}
{"kind":"category","type":"sleepAnalysis","value":4,"start":"-7h","duration":"1h"}
{"kind":"category","type":"sleepAnalysis","value":5,"start":"-6h","duration":"30m"}
{"kind":"category","type":"sleepAnalysis","value":3,"start":"-5h30m","duration":"2h"}
{"kind":"category","type":"sleepAnalysis","value":5,"start":"-3h30m","duration":"45m"}
{"kind":"category","type":"sleepAnalysis","value":3,"start":"-2h45m","duration":"2h"}
```

### Symptom Values

| Value | Meaning     |
| ----- | ----------- |
| 0     | Not Present |
| 1     | Mild        |
| 2     | Moderate    |
| 3     | Severe      |

### Date Formats

| Format           | Example                | Description           |
| ---------------- | ---------------------- | --------------------- |
| `now`            | `"start":"now"`        | Current time          |
| `today`          | `"start":"today"`      | Start of today        |
| `yesterday`      | `"start":"yesterday"`  | Start of yesterday    |
| Relative days    | `"start":"-1d"`        | 1 day ago             |
| Relative hours   | `"start":"-2h"`        | 2 hours ago           |
| Relative minutes | `"start":"-30m"`       | 30 minutes ago        |
| Day + time       | `"start":"today 8am"`  | Today at 8:00 AM      |
| ISO8601          | `"start":"2026-01-04T08:00:00Z"` | Exact timestamp |

Duration uses same format: `"duration":"1h30m"`, `"duration":"1d"`, etc.

## Data Profiles

Reference values for realistic data generation:

### Healthy Active Person

- Resting HR: 55-65 bpm
- Steps: 8,000-12,000/day
- Sleep: 7-8 hours, good quality
- Workouts: 4-5x/week
- Water: 2-3L/day

### Sedentary Office Worker

- Resting HR: 70-80 bpm
- Steps: 2,000-4,000/day
- Sleep: 5-6 hours, fragmented
- Workouts: 0-1x/week
- Caffeine: 300-500mg/day

### Elite Athlete

- Resting HR: 45-55 bpm
- Steps: 15,000-25,000/day
- Sleep: 8-9 hours, high quality
- Workouts: 10-14x/week (doubles)

### Stressed Individual

- Resting HR: 80-95 bpm
- Steps: 2,000-3,500/day
- Sleep: 4-5 hours, poor quality
- Symptoms: headaches, fatigue
- Caffeine: 400-600mg/day

## Verifying Data

### Query Samples

```bash
# Query recent samples
bunx apple-health query quantity heartRate --limit 10
bunx apple-health query category sleepAnalysis --limit 5
bunx apple-health query workouts --limit 5

# With date range
bunx apple-health query quantity stepCount --start "-7d" --end "now" --limit 100
```

### Get Statistics

```bash
# Single stat
bunx apple-health stats stepCount

# With aggregations
bunx apple-health stats heartRate --aggregations "discreteAverage,discreteMin,discreteMax"

# Time-bucketed (daily, weekly, etc.)
bunx apple-health stats stepCount --interval day --start "-7d"
bunx apple-health stats heartRate --interval hour --start "today"
```

### JSON Output

Add `--json` flag for machine-readable output:

```bash
bunx apple-health query quantity heartRate --limit 5 --json
bunx apple-health stats stepCount --interval day --start "-7d" --json
```

## Individual Writes

For single samples without batch mode:

```bash
# Quantity samples
bunx apple-health write quantity heartRate 72
bunx apple-health write quantity heartRate 85 --start "today 8am"
bunx apple-health write quantity stepCount 5000 --start "yesterday" --duration "1d"

# Category samples
bunx apple-health write category sleepAnalysis 3 --start "-8h" --duration "7h"
bunx apple-health write category headache 2 --start "-2h"

# Workouts
bunx apple-health write workout running
bunx apple-health write workout cycling --start "today 7am" --duration "1h" --energy 450 --distance 25000
```

## Deleting Test Data

```bash
# Delete specific type within time range
bunx apple-health delete stepCount --start "-30d" --end "now"
bunx apple-health delete heartRate --start "-30d" --end "now"
```

## Authorization

Check and request permissions before writing:

```bash
# Check authorization status
bunx apple-health auth status stepCount heartRate

# Request authorization
bunx apple-health auth request --read "stepCount,heartRate" --write "stepCount,heartRate"
```

## Available Types

List all available types:

```bash
bunx apple-health types

# Filter by category
bunx apple-health types --category Vitals
bunx apple-health types --category Nutrition
```

Common quantity types:
- Body: `bodyMass`, `height`, `bodyFatPercentage`, `bodyMassIndex`
- Fitness: `stepCount`, `distanceWalkingRunning`, `activeEnergyBurned`, `flightsClimbed`
- Vitals: `heartRate`, `restingHeartRate`, `bloodPressureSystolic`, `oxygenSaturation`
- Nutrition: `dietaryCaffeine`, `dietaryWater`, `dietaryEnergyConsumed`, `dietaryProtein`

Common category types:
- Sleep: `sleepAnalysis`
- Symptoms: `headache`, `fatigue`, `nausea`, `dizziness`
- Mindfulness: `mindfulSession`

Workout types: `running`, `walking`, `cycling`, `swimming`, `yoga`, `hiking`, `highIntensityIntervalTraining`, `traditionalStrengthTraining`, and 70+ more.

## Tips for Realistic Data

1. **Include variations**: Not every day should have identical values
2. **Consider correlations**: Poor sleep → higher resting HR, lower step count
3. **Use appropriate ranges**: Elite athletes have lower resting HR than sedentary individuals
4. **Add realistic patterns**: Heart rate higher during workouts, lower during sleep
5. **Distribute over time**: Use relative time formats to spread data across days

## Interactive Mode

For exploratory testing, use the REPL:

```bash
bunx apple-health repl
```

```
apple-health> write quantity heartRate 72
apple-health> query quantity heartRate 5
apple-health> stats stepCount day
apple-health> exit
```
