---
name: check-live-stations
description: Analyze live weather station integrations, validate data sources, and identify spots missing live conditions
---

# Check Live Stations Skill

Analyze live weather data sources in FetchCurrentConditions strategies and cross-reference with spots.json to identify coverage and issues.

## Instructions

Perform the following analysis and report all findings.

### 1. Discover All Strategies

Scan `src/main/java/com/github/pwittchen/varun/service/live/strategy/` for all `FetchCurrentConditionsStrategy*.java` files.

For each strategy, extract:
- Class name
- Windguru ID(s) it handles (from `canProcess()` method or ID constants/maps)
- Data source URL(s)
- Data format (JSON, plain text, HTML scraping)
- Provider name (from class comments or URL domain)

### 2. Load Spots Data

Read `src/main/resources/spots.json` and extract:
- Spot name
- Country
- Windguru ID (from `windguruUrl`, extract numeric ID)
- Fallback Windguru ID if present (from `windguruFallbackUrl`)

### 3. Cross-Reference Coverage

For each spot in spots.json:
1. Determine if any strategy can process its Windguru ID
2. Mark spots as "has live data" or "no live data"

### 4. Test Live Data Sources

For each unique data source URL found in strategies:
1. Attempt to fetch the URL using curl (with 10s timeout)
2. Check HTTP response code
3. Verify response contains expected data markers (non-empty, valid format)

### 5. Analyze Strategy Patterns

For each strategy, document:
- Parsing method (regex, JSON, HTML table extraction)
- Fields extracted (wind speed, gusts, direction, temperature, timestamp)
- Unit conversions performed (m/s to knots, etc.)
- Error handling approach

## Output Format

Generate a report in this format:

```
## Live Weather Stations Analysis Report

### Summary
- Total strategies: X
- Total spots: Y
- Spots with live data: Z (W%)
- Spots without live data: N

### Strategy Inventory

| Strategy Class | Provider | WG IDs | Data URL | Format |
|----------------|----------|--------|----------|--------|
| ...            | ...      | ...    | ...      | ...    |

### Coverage by Country

| Country | Total Spots | With Live Data | Without Live Data |
|---------|-------------|----------------|-------------------|
| Poland  | X           | Y              | Z                 |
| ...     | ...         | ...            | ...               |

### Spots WITH Live Data Integration

| Spot Name | Country | WG ID | Strategy | Data Source |
|-----------|---------|-------|----------|-------------|
| ...       | ...     | ...   | ...      | ...         |

### Spots WITHOUT Live Data Integration

These spots only have forecast data and could benefit from live weather station integration:

| Spot Name | Country | WG ID | Potential Sources |
|-----------|---------|-------|-------------------|
| ...       | ...     | ...   | (suggest if known) |

### Data Source Health Check

| URL | Status | Response Time | Notes |
|-----|--------|---------------|-------|
| ... | OK/FAIL| Xms           | ...   |

### Issues Found

#### Critical (data sources unreachable)
- [Strategy] URL not responding: url

#### Warnings (potential improvements)
- [Spot] Could add live data from nearby station
- [Strategy] Missing gust data extraction

### Recommendations

1. Priority spots for live data integration (high-traffic locations)
2. Nearby stations that could be leveraged
3. Strategy improvements or consolidation opportunities
```

## Execution Steps

1. Use `Glob` to find all strategy files in the strategy directory
2. Use `Read` to analyze each strategy file
3. Use `Read` to load spots.json
4. Use `Bash` with `curl` to test each data source URL
5. Cross-reference and generate the report
6. Provide actionable recommendations

## Notes

- Windguru IDs are extracted from URLs like `https://www.windguru.cz/500760` -> `500760`
- Some spots use `windguruFallbackUrl` when `windguruUrl` is empty (generated IDs)
- Strategies may handle multiple spots (e.g., WiatrKadynyStations handles 4 spots)
- Data sources may be temporarily offline; distinguish between transient and permanent failures
