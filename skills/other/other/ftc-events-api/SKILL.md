---
name: ftc-events-api
description: >-
  Integrate with the official FIRST Tech Challenge Events API in FTC Metrics.
  Use when fetching events, teams, matches, scores, rankings, or troubleshooting
  FTC API authentication and responses.
license: MIT
compatibility: [Claude Code]
metadata:
  author: ftcmetrics
  version: "1.0.0"
  category: api
---

# FTC Events API Integration

The FTC Events API provides official data for FIRST Tech Challenge competitions. FTC Metrics uses this to fetch events, teams, match schedules, scores, and rankings.

## Quick Start

### Prerequisites

1. Register for API credentials at https://ftc-events.firstinspires.org/services/API
2. Add credentials to `.env`:
   ```bash
   FTC_API_USERNAME=your_username
   FTC_API_TOKEN=your_token
   ```

### Basic Usage

```typescript
import { getFTCApi } from "@ftcmetrics/api/lib/ftc-api";

const api = getFTCApi();

// Get all events for current season
const { events } = await api.getEvents();

// Get teams at an event
const { teams } = await api.getEventTeams("USNCCRR");

// Get match scores
const { matchScores } = await api.getScores("USNCCRR", "qual");
```

## API Reference

| Method | Description |
|--------|-------------|
| `getEvents()` | List all events for current season |
| `getEvent(code)` | Get specific event details |
| `getEventTeams(code)` | Get teams registered at event |
| `getTeam(number)` | Get team info by number |
| `getSchedule(code, level)` | Get match schedule |
| `getMatches(code, level)` | Get match results |
| `getScores(code, level)` | Get detailed match scores |
| `getRankings(code)` | Get team rankings at event |
| `getTeamEvents(number)` | Get events a team is registered for |

### Tournament Levels

- `"qual"` - Qualification matches (default)
- `"playoff"` - Elimination matches

## Response Types

### FTCEvent
```typescript
interface FTCEvent {
  eventCode: string;
  name: string;
  venue: string;
  city: string;
  stateProv: string;
  country: string;
  dateStart: string;
  dateEnd: string;
  type: string;
  timezone: string;
}
```

### FTCMatchScore
```typescript
interface FTCMatchScore {
  matchLevel: string;
  matchNumber: number;
  alliances: {
    alliance: "Red" | "Blue";
    totalPoints: number;
    autoPoints: number;
    dcPoints: number;
    endgamePoints: number;
    penaltyPointsCommitted: number;
    team1: number;
    team2: number;
  }[];
}
```

## Authentication

The API uses HTTP Basic Auth with base64-encoded credentials:

```typescript
private getAuthHeader(): string {
  const credentials = Buffer.from(`${username}:${token}`).toString("base64");
  return `Basic ${credentials}`;
}
```

## Common Patterns

### Fetch Event with All Data

```typescript
async function getFullEventData(eventCode: string) {
  const api = getFTCApi();

  const [eventData, teams, schedule, scores, rankings] = await Promise.all([
    api.getEvent(eventCode),
    api.getEventTeams(eventCode),
    api.getSchedule(eventCode, "qual"),
    api.getScores(eventCode, "qual"),
    api.getRankings(eventCode),
  ]);

  return { eventData, teams, schedule, scores, rankings };
}
```

### Handle Missing Scores

```typescript
// Matches may not have scores yet (scheduled but not played)
const { matchScores } = await api.getScores(eventCode, "qual");

const completedMatches = matchScores.filter(
  (match) => match.alliances[0].totalPoints > 0
);
```

## Anti-Patterns

- ❌ Hardcoding credentials in source code
- ❌ Not handling API errors (always check response.ok)
- ❌ Fetching all events when you only need one (use eventCode filter)
- ❌ Ignoring rate limits (add delays between bulk requests)

## Common Errors

### "FTC API credentials not configured"

Ensure `FTC_API_USERNAME` and `FTC_API_TOKEN` are set in your `.env` file.

### 401 Unauthorized

Credentials are invalid. Verify at https://ftc-events.firstinspires.org/services/API

### 404 Not Found

Event code doesn't exist or season is wrong. Current season is 2025 (DECODE).

## Current Season

The API client is configured for the **2025 DECODE** season:

```typescript
const CURRENT_SEASON = 2025;
```

## References

- [FTC Events API Documentation](https://ftc-api.firstinspires.org/)
- [Register for API Access](https://ftc-events.firstinspires.org/services/API)
- [API Implementation](packages/api/src/lib/ftc-api.ts)
