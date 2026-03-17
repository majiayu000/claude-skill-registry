---
name: astro-aso
description: Query local Astro Mac app database for ASO insights. Use when the user asks about keyword rankings, historical ranking data, trend analysis, competitor keywords, app ratings, keyword opportunities, or ASO health metrics.
---

# Astro ASO Skill

Query your local Astro Mac app database for App Store Optimization insights.

## When to Use

Invoke this skill when the user asks about:

- Keyword rankings and tracking
- Historical ranking data and trends
- Competitor analysis for keywords
- App ratings and reviews data
- Keyword opportunities and recommendations
- ASO health analysis
- Ranking predictions and anomalies

## Prerequisites

- Astro Mac app installed: https://astro.app
- App must have data (tracked apps/keywords)

## Usage

Run commands via the bundled script:

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs <command> '<json-params>'
```

## Available Commands

### list_apps

List all tracked apps in Astro.

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs list_apps '{}'
```

---

### search_rankings

Search keyword rankings for apps.

| Param   | Type   | Required | Description               |
| ------- | ------ | -------- | ------------------------- |
| keyword | string | YES      | Keyword to search         |
| store   | string | no       | Filter by store (ios/mac) |
| appName | string | no       | Filter by app name        |
| appId   | string | no       | Filter by app ID          |

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs search_rankings '{"keyword": "photo editor"}'
```

---

### historical_rankings

Get historical ranking data for a keyword.

| Param    | Type   | Required | Description                   |
| -------- | ------ | -------- | ----------------------------- |
| keyword  | string | YES      | Keyword to track              |
| appName  | string | no       | Filter by app name            |
| appId    | string | no       | Filter by app ID              |
| daysBack | number | no       | Days of history (default: 30) |
| store    | string | no       | Filter by store               |

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs historical_rankings '{"keyword": "photo editor", "daysBack": 90}'
```

---

### app_keywords

Get all tracked keywords for an app.

| Param   | Type   | Required | Description       |
| ------- | ------ | -------- | ----------------- |
| appName | string | no\*     | App name to query |
| appId   | string | no\*     | App ID to query   |
| store   | string | no       | Filter by store   |

\*One of appName or appId required

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs app_keywords '{"appName": "My App"}'
```

---

### keyword_trends

Analyze keyword ranking trends over time.

| Param   | Type   | Required | Description                          |
| ------- | ------ | -------- | ------------------------------------ |
| keyword | string | YES      | Keyword to analyze                   |
| appName | string | no       | Filter by app name                   |
| appId   | string | no       | Filter by app ID                     |
| period  | string | no       | week/month/year/all (default: month) |
| store   | string | no       | Filter by store                      |

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs keyword_trends '{"keyword": "photo editor", "period": "month"}'
```

---

### compare_rankings

Compare rankings between two dates.

| Param   | Type   | Required | Description              |
| ------- | ------ | -------- | ------------------------ |
| keyword | string | YES      | Keyword to compare       |
| date1   | string | YES      | First date (ISO format)  |
| date2   | string | YES      | Second date (ISO format) |
| appName | string | no       | Filter by app name       |
| appId   | string | no       | Filter by app ID         |
| store   | string | no       | Filter by store          |

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs compare_rankings '{"keyword": "photo editor", "date1": "2024-01-01", "date2": "2024-02-01"}'
```

---

### app_ratings

Get app ratings and review data.

| Param    | Type   | Required | Description                   |
| -------- | ------ | -------- | ----------------------------- |
| appName  | string | no\*     | App name to query             |
| appId    | string | no\*     | App ID to query               |
| store    | string | no       | Filter by store               |
| daysBack | number | no       | Days of history (default: 30) |

\*One of appName or appId required

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs app_ratings '{"appName": "My App", "daysBack": 60}'
```

---

### keyword_competitors

Find competing apps ranking for a keyword.

| Param   | Type   | Required | Description               |
| ------- | ------ | -------- | ------------------------- |
| keyword | string | YES      | Keyword to analyze        |
| store   | string | no       | Filter by store           |
| limit   | number | no       | Max results (default: 10) |

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs keyword_competitors '{"keyword": "photo editor", "limit": 20}'
```

---

### keyword_recommendations

Get recommended keywords based on existing ones.

| Param   | Type   | Required | Description               |
| ------- | ------ | -------- | ------------------------- |
| keyword | string | YES      | Base keyword              |
| appName | string | no       | Filter by app name        |
| appId   | string | no       | Filter by app ID          |
| store   | string | no       | Filter by store           |
| limit   | number | no       | Max results (default: 10) |

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs keyword_recommendations '{"keyword": "photo"}'
```

---

### competitive_landscape

Analyze competitive position for an app.

| Param   | Type   | Required | Description                   |
| ------- | ------ | -------- | ----------------------------- |
| appName | string | no\*     | App name to analyze           |
| appId   | string | no\*     | App ID to analyze             |
| store   | string | no       | Filter by store               |
| limit   | number | no       | Max competitors (default: 10) |

\*One of appName or appId required

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs competitive_landscape '{"appName": "My App"}'
```

---

### keyword_opportunities

Find keyword opportunities (low difficulty, high popularity).

| Param         | Type   | Required | Description          |
| ------------- | ------ | -------- | -------------------- |
| appName       | string | no\*     | App name to analyze  |
| appId         | string | no\*     | App ID to analyze    |
| store         | string | no       | Filter by store      |
| minPopularity | number | no       | Min popularity score |
| maxDifficulty | number | no       | Max difficulty score |

\*One of appName or appId required

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs keyword_opportunities '{"appName": "My App", "maxDifficulty": 30}'
```

---

### ranking_anomalies

Detect sudden ranking changes and anomalies.

| Param     | Type   | Required | Description                    |
| --------- | ------ | -------- | ------------------------------ |
| appName   | string | no\*     | App name to analyze            |
| appId     | string | no\*     | App ID to analyze              |
| daysBack  | number | no       | Days to analyze (default: 7)   |
| threshold | number | no       | Change threshold (default: 10) |
| store     | string | no       | Filter by store                |

\*One of appName or appId required

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs ranking_anomalies '{"appName": "My App", "threshold": 15}'
```

---

### ranking_predictions

Predict future rankings based on trends.

| Param       | Type   | Required | Description                  |
| ----------- | ------ | -------- | ---------------------------- |
| keyword     | string | YES      | Keyword to predict           |
| appName     | string | no       | Filter by app name           |
| appId       | string | no       | Filter by app ID             |
| store       | string | no       | Filter by store              |
| daysForward | number | no       | Days to predict (default: 7) |

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs ranking_predictions '{"keyword": "photo editor", "daysForward": 14}'
```

---

### low_competition_keywords

Find keywords with low competition.

| Param         | Type   | Required | Description                  |
| ------------- | ------ | -------- | ---------------------------- |
| store         | string | no       | Filter by store              |
| maxDifficulty | number | no       | Max difficulty (default: 30) |
| minPopularity | number | no       | Min popularity (default: 20) |
| limit         | number | no       | Max results (default: 20)    |

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs low_competition_keywords '{"maxDifficulty": 25, "minPopularity": 30}'
```

---

### analyze_aso_health

Get overall ASO health analysis for an app.

| Param   | Type   | Required | Description         |
| ------- | ------ | -------- | ------------------- |
| appName | string | no\*     | App name to analyze |
| appId   | string | no\*     | App ID to analyze   |
| store   | string | no       | Filter by store     |

\*One of appName or appId required

```bash
node .claude/skills/astro-aso/scripts/astro-query.mjs analyze_aso_health '{"appName": "My App"}'
```

## Output Format

All commands return JSON with either:

- `{ "success": true, "data": ... }` on success
- `{ "success": false, "error": "..." }` on failure

## Example Workflow

1. List all tracked apps:

   ```bash
   node .claude/skills/astro-aso/scripts/astro-query.mjs list_apps '{}'
   ```

2. Get keywords for a specific app:

   ```bash
   node .claude/skills/astro-aso/scripts/astro-query.mjs app_keywords '{"appName": "My App"}'
   ```

3. Analyze keyword trends:

   ```bash
   node .claude/skills/astro-aso/scripts/astro-query.mjs keyword_trends '{"keyword": "productivity", "period": "month"}'
   ```

4. Find opportunities:
   ```bash
   node .claude/skills/astro-aso/scripts/astro-query.mjs keyword_opportunities '{"appName": "My App", "maxDifficulty": 40}'
   ```
