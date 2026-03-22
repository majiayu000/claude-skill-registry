---
name: irail-cli
description: >
  Query Belgian railway (NMBS/SNCB) schedules via the irail CLI. Use when the user wants
  train departures, connections between stations, train compositions, or service disruptions.
  Triggered by mentions of Belgian trains, NMBS, SNCB, iRail, train schedules, or railway delays.
license: MIT
homepage: https://github.com/dedene/irail-cli
metadata:
  author: dedene
  version: "1.1.0"
  openclaw:
    requires:
      bins:
        - irail
      anyBins:
        - jq
    install:
      - kind: brew
        tap: dedene/tap
        formula: irail
        bins: [irail]
      - kind: go
        package: github.com/dedene/irail-cli/cmd/irail
        bins: [irail]
---

# irail-cli

CLI for Belgian railways (NMBS/SNCB) via [iRail API](https://api.irail.be/). No authentication required.

## Quick Start

```bash
# Station departures
irail liveboard Brugge

# Find connections
irail connections Brugge Leuven

# Check disruptions
irail disturbances
```

## Authentication

**None required.** iRail API is public and free to use.

## Core Rules

1. **Always use `--json`** when parsing output programmatically
2. **Station names are flexible** - accepts partial matches, quotes for multi-word
3. **Time format** - HH:MM (24-hour), date format YYYY-MM-DD
4. **Language options** - nl, fr, en, de (default: nl)

## Output Formats

| Flag | Format | Use case |
|------|--------|----------|
| (default) | Table | User-facing with colors |
| `--json` | JSON | Agent parsing, scripting |

Colors indicate: red = delays, yellow = platform changes.

## Workflows

### Liveboard (Departures/Arrivals)

```bash
# Departures from station
irail liveboard Brugge
irail liveboard "Brussel-Centraal"

# Arrivals instead of departures
irail liveboard Brugge --arrivals

# Specific date/time
irail liveboard Brugge --time 09:00 --date 2025-02-15

# JSON for scripting
irail liveboard Brugge --json

# Different language
irail liveboard Brugge --lang en
```

### Connections (Route Planning)

```bash
# Find routes
irail connections Brugge Leuven

# Specific departure time
irail connections Brugge Leuven --time 09:00

# Arrive by time (instead of depart at)
irail connections Brugge Leuven --time 14:00 --arrive-by

# More results
irail connections Brugge Leuven --results 10

# JSON for parsing
irail connections Brugge Leuven --json
```

### Stations

```bash
# List all stations
irail stations

# Search stations
irail stations --search bruss
irail stations --search gent

# JSON for scripting
irail stations --json
```

### Vehicle (Train Info)

```bash
# Show train information
irail vehicle IC1832

# Include all stops
irail vehicle IC1832 --stops

# JSON output
irail vehicle IC1832 --json
```

### Composition (Train Cars)

```bash
# Show train composition (seats, amenities)
irail composition S51507
irail composition IC1832

# JSON for parsing
irail composition S51507 --json
```

### Disturbances

```bash
# All current disruptions
irail disturbances

# Only planned works
irail disturbances --type planned

# Only unplanned disruptions
irail disturbances --type disturbance

# JSON for scripting
irail disturbances --json
```

## Scripting Examples

```bash
# Get next train to destination
irail connections Brugge Leuven --json | jq -r '.[0].departure'

# Find station ID
irail stations --search "brussel" --json | jq -r '.[0].id'

# Check if delays exist on liveboard
irail liveboard Brugge --json | jq '[.[] | select(.delay > 0)] | length'

# Get platform for next departure
irail liveboard Brugge --json | jq -r '.[0].platform'

# List all disruptions
irail disturbances --json | jq -r '.[].title'
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `IRAIL_LANG` | Default language (nl, fr, en, de) |
| `IRAIL_JSON` | Default to JSON output |
| `NO_COLOR` | Disable colored output |

## Language Options

| Code | Language |
|------|----------|
| `nl` | Dutch (default) |
| `fr` | French |
| `en` | English |
| `de` | German |

```bash
irail liveboard Brugge --lang fr
irail connections Brugge Leuven --lang en
```

## Command Reference

| Command | Description |
|---------|-------------|
| `liveboard` | Station departures/arrivals |
| `connections` | Route planning between stations |
| `stations` | List/search stations |
| `vehicle` | Train information and stops |
| `composition` | Train car composition |
| `disturbances` | Service disruptions |
| `completion` | Shell completions |

## Common Patterns

### Check if train is delayed

```bash
irail vehicle IC1832 --json | jq '.delay // 0'
```

### Get connection with transfers

```bash
irail connections Brugge Leuven --json | jq '.[0].vias | length'
```

### Find direct trains only

```bash
irail connections Brugge Leuven --json | jq '[.[] | select(.vias == null or (.vias | length) == 0)]'
```

## Guidelines

- No authentication needed - API is public
- Be mindful of API usage in loops - add delays between requests
- Station names are case-insensitive and support partial matching
- Delay values are in seconds (divide by 60 for minutes)


## Installation

```bash
brew install dedene/tap/irail
```
