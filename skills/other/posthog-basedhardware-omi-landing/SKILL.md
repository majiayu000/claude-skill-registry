---
name: posthog
description: Query PostHog for product analytics, create insights, dashboards, and track AI referral traffic. Auto-activates when user asks about analytics, user behavior, funnels, retention, AI traffic, or dashboards. Trigger words: "check posthog", "create insight", "analytics", "user behavior", "AI traffic", "dashboard", "funnel", "retention"
allowed-tools: Bash, Read
---

# PostHog Analytics Skill

Query and manage PostHog product analytics for Mediar applications.

## Configuration

**Host:** `https://eu.i.posthog.com`
**Project Key (SDK):** `phc_NFSaZUao49XckpqaeyB3lIEKrFXhhXbKaI81jqZ8yn9`

**Personal API Key:** Required for API operations. Read `POSTHOG_API_KEY` from `.env.local`

### Getting a Personal API Key

1. Go to https://eu.posthog.com/settings/user-api-keys
2. Click "Create personal API key"
3. Name it (e.g., "claude-code")
4. Select scopes: `insight:read`, `insight:write`, `dashboard:read`, `dashboard:write`, `query:read`
5. Add to `.env.local`: `POSTHOG_API_KEY=phx_xxx...`

---

## PowerShell Queries (Windows)

Use PowerShell for all queries to avoid bash escaping issues.

### Get Project ID

```powershell
powershell -Command "
$token = (Get-Content .env.local | Where-Object { $_ -match '^POSTHOG_API_KEY=' }) -replace 'POSTHOG_API_KEY=', '' -replace '\"', ''
$headers = @{ 'Authorization' = \"Bearer $token\" }
$response = Invoke-RestMethod -Uri 'https://eu.i.posthog.com/api/projects/' -Headers $headers
$response.results | ForEach-Object { Write-Host \"[$($_.id)] $($_.name)\" }
"
```

### List All Insights

```powershell
powershell -Command "
$token = (Get-Content .env.local | Where-Object { $_ -match '^POSTHOG_API_KEY=' }) -replace 'POSTHOG_API_KEY=', '' -replace '\"', ''
$headers = @{ 'Authorization' = \"Bearer $token\" }
$projectId = 'YOUR_PROJECT_ID'  # Get from above query
$response = Invoke-RestMethod -Uri \"https://eu.i.posthog.com/api/projects/$projectId/insights/?limit=20\" -Headers $headers
$response.results | ForEach-Object {
    Write-Host \"[$($_.id)] $($_.name)\"
    Write-Host \"  Type: $($_.filters.insight) | Created: $($_.created_at)\"
}
"
```

### List All Dashboards

```powershell
powershell -Command "
$token = (Get-Content .env.local | Where-Object { $_ -match '^POSTHOG_API_KEY=' }) -replace 'POSTHOG_API_KEY=', '' -replace '\"', ''
$headers = @{ 'Authorization' = \"Bearer $token\" }
$projectId = 'YOUR_PROJECT_ID'
$response = Invoke-RestMethod -Uri \"https://eu.i.posthog.com/api/projects/$projectId/dashboards/\" -Headers $headers
$response.results | ForEach-Object {
    Write-Host \"[$($_.id)] $($_.name)\"
    Write-Host \"  Tiles: $($_.tiles.Count) | Created: $($_.created_at)\"
}
"
```

---

## Create Insights

### Create AI Referral Traffic Insight

```powershell
powershell -Command "
$token = (Get-Content .env.local | Where-Object { $_ -match '^POSTHOG_API_KEY=' }) -replace 'POSTHOG_API_KEY=', '' -replace '\"', ''
$headers = @{
    'Authorization' = \"Bearer $token\"
    'Content-Type' = 'application/json'
}
$projectId = 'YOUR_PROJECT_ID'
$body = @{
    name = 'AI Referral Traffic'
    filters = @{
        insight = 'TRENDS'
        events = @(@{ id = '`$pageview'; type = 'events' })
        properties = @{
            type = 'OR'
            values = @(
                @{ key = '`$referrer'; value = 'chatgpt.com'; operator = 'icontains'; type = 'event' }
                @{ key = '`$referrer'; value = 'claude.ai'; operator = 'icontains'; type = 'event' }
                @{ key = '`$referrer'; value = 'perplexity.ai'; operator = 'icontains'; type = 'event' }
                @{ key = '`$referrer'; value = 'gemini.google.com'; operator = 'icontains'; type = 'event' }
            )
        }
        date_from = '-30d'
    }
} | ConvertTo-Json -Depth 10
$response = Invoke-RestMethod -Uri \"https://eu.i.posthog.com/api/projects/$projectId/insights/\" -Method POST -Headers $headers -Body $body
Write-Host \"Created insight: $($response.id) - $($response.name)\"
"
```

### Create Pageviews by Page Insight

```powershell
powershell -Command "
$token = (Get-Content .env.local | Where-Object { $_ -match '^POSTHOG_API_KEY=' }) -replace 'POSTHOG_API_KEY=', '' -replace '\"', ''
$headers = @{
    'Authorization' = \"Bearer $token\"
    'Content-Type' = 'application/json'
}
$projectId = 'YOUR_PROJECT_ID'
$body = @{
    name = 'Top Pages'
    filters = @{
        insight = 'TRENDS'
        events = @(@{ id = '`$pageview'; type = 'events' })
        breakdown = '`$pathname'
        breakdown_type = 'event'
        date_from = '-7d'
    }
} | ConvertTo-Json -Depth 10
$response = Invoke-RestMethod -Uri \"https://eu.i.posthog.com/api/projects/$projectId/insights/\" -Method POST -Headers $headers -Body $body
Write-Host \"Created insight: $($response.id) - $($response.name)\"
"
```

### Create User Funnel Insight

```powershell
powershell -Command "
$token = (Get-Content .env.local | Where-Object { $_ -match '^POSTHOG_API_KEY=' }) -replace 'POSTHOG_API_KEY=', '' -replace '\"', ''
$headers = @{
    'Authorization' = \"Bearer $token\"
    'Content-Type' = 'application/json'
}
$projectId = 'YOUR_PROJECT_ID'
$body = @{
    name = 'Signup Funnel'
    filters = @{
        insight = 'FUNNELS'
        events = @(
            @{ id = '`$pageview'; type = 'events'; name = 'Visit' }
            @{ id = 'signup_started'; type = 'events'; name = 'Start Signup' }
            @{ id = 'signup_completed'; type = 'events'; name = 'Complete Signup' }
        )
        date_from = '-30d'
    }
} | ConvertTo-Json -Depth 10
$response = Invoke-RestMethod -Uri \"https://eu.i.posthog.com/api/projects/$projectId/insights/\" -Method POST -Headers $headers -Body $body
Write-Host \"Created funnel: $($response.id) - $($response.name)\"
"
```

---

## Dashboard Operations

### Create Dashboard

```powershell
powershell -Command "
$token = (Get-Content .env.local | Where-Object { $_ -match '^POSTHOG_API_KEY=' }) -replace 'POSTHOG_API_KEY=', '' -replace '\"', ''
$headers = @{
    'Authorization' = \"Bearer $token\"
    'Content-Type' = 'application/json'
}
$projectId = 'YOUR_PROJECT_ID'
$body = @{
    name = 'AI Traffic Dashboard'
    description = 'Track traffic from AI assistants (ChatGPT, Claude, Perplexity)'
} | ConvertTo-Json
$response = Invoke-RestMethod -Uri \"https://eu.i.posthog.com/api/projects/$projectId/dashboards/\" -Method POST -Headers $headers -Body $body
Write-Host \"Created dashboard: $($response.id) - $($response.name)\"
"
```

### Add Insight to Dashboard

```powershell
powershell -Command "
$token = (Get-Content .env.local | Where-Object { $_ -match '^POSTHOG_API_KEY=' }) -replace 'POSTHOG_API_KEY=', '' -replace '\"', ''
$headers = @{
    'Authorization' = \"Bearer $token\"
    'Content-Type' = 'application/json'
}
$projectId = 'YOUR_PROJECT_ID'
$dashboardId = 'YOUR_DASHBOARD_ID'
$insightId = 'YOUR_INSIGHT_ID'
$body = @{
    tiles = @(@{ insight = $insightId })
} | ConvertTo-Json -Depth 5
$response = Invoke-RestMethod -Uri \"https://eu.i.posthog.com/api/projects/$projectId/dashboards/$dashboardId/\" -Method PATCH -Headers $headers -Body $body
Write-Host \"Added insight to dashboard: $($response.name)\"
"
```

---

## Query Events (HogQL)

### Query Recent Events

```powershell
powershell -Command "
$token = (Get-Content .env.local | Where-Object { $_ -match '^POSTHOG_API_KEY=' }) -replace 'POSTHOG_API_KEY=', '' -replace '\"', ''
$headers = @{
    'Authorization' = \"Bearer $token\"
    'Content-Type' = 'application/json'
}
$projectId = 'YOUR_PROJECT_ID'
$body = @{
    query = @{
        kind = 'HogQLQuery'
        query = 'SELECT event, properties.`$referrer` as referrer, count() as count FROM events WHERE timestamp > now() - INTERVAL 7 DAY GROUP BY event, referrer ORDER BY count DESC LIMIT 20'
    }
} | ConvertTo-Json -Depth 5
$response = Invoke-RestMethod -Uri \"https://eu.i.posthog.com/api/projects/$projectId/query/\" -Method POST -Headers $headers -Body $body
$response.results | ForEach-Object { Write-Host $_ }
"
```

### Query AI Bot Referrals

```powershell
powershell -Command "
$token = (Get-Content .env.local | Where-Object { $_ -match '^POSTHOG_API_KEY=' }) -replace 'POSTHOG_API_KEY=', '' -replace '\"', ''
$headers = @{
    'Authorization' = \"Bearer $token\"
    'Content-Type' = 'application/json'
}
$projectId = 'YOUR_PROJECT_ID'
$body = @{
    query = @{
        kind = 'HogQLQuery'
        query = @'
SELECT
    CASE
        WHEN properties.`$referrer` LIKE '%chatgpt%' OR properties.`$referrer` LIKE '%openai%' THEN 'ChatGPT'
        WHEN properties.`$referrer` LIKE '%claude.ai%' THEN 'Claude'
        WHEN properties.`$referrer` LIKE '%perplexity%' THEN 'Perplexity'
        WHEN properties.`$referrer` LIKE '%gemini%' THEN 'Gemini'
        ELSE 'Other AI'
    END as ai_source,
    count() as visits,
    uniq(distinct_id) as unique_users
FROM events
WHERE event = '$pageview'
    AND (
        properties.`$referrer` LIKE '%chatgpt%'
        OR properties.`$referrer` LIKE '%openai%'
        OR properties.`$referrer` LIKE '%claude.ai%'
        OR properties.`$referrer` LIKE '%perplexity%'
        OR properties.`$referrer` LIKE '%gemini%'
    )
    AND timestamp > now() - INTERVAL 30 DAY
GROUP BY ai_source
ORDER BY visits DESC
'@
    }
} | ConvertTo-Json -Depth 5
$response = Invoke-RestMethod -Uri \"https://eu.i.posthog.com/api/projects/$projectId/query/\" -Method POST -Headers $headers -Body $body
$response.results | ForEach-Object { Write-Host \"$($_[0]): $($_[1]) visits, $($_[2]) unique users\" }
"
```

---

## Get Insight Data

### Get Insight Results

```powershell
powershell -Command "
$token = (Get-Content .env.local | Where-Object { $_ -match '^POSTHOG_API_KEY=' }) -replace 'POSTHOG_API_KEY=', '' -replace '\"', ''
$headers = @{ 'Authorization' = \"Bearer $token\" }
$projectId = 'YOUR_PROJECT_ID'
$insightId = 'YOUR_INSIGHT_ID'
$response = Invoke-RestMethod -Uri \"https://eu.i.posthog.com/api/projects/$projectId/insights/$insightId/\" -Headers $headers
Write-Host \"Insight: $($response.name)\"
Write-Host \"Last refresh: $($response.last_refresh)\"
$response.result | ConvertTo-Json -Depth 5
"
```

---

## Useful Filters

### Event Properties
- `$pageview` - Page view event
- `$autocapture` - Auto-captured clicks
- `$referrer` - Referring URL
- `$pathname` - Page path
- `$current_url` - Full URL
- `$browser` - Browser name
- `$os` - Operating system
- `$device_type` - desktop/mobile/tablet

### Filter Operators
- `exact` - Exact match
- `icontains` - Case-insensitive contains
- `regex` - Regular expression
- `is_set` - Property exists
- `is_not_set` - Property doesn't exist
- `gt`, `lt`, `gte`, `lte` - Comparisons

### Insight Types
- `TRENDS` - Time series charts
- `FUNNELS` - Conversion funnels
- `RETENTION` - User retention
- `PATHS` - User journey paths
- `STICKINESS` - Feature stickiness
- `LIFECYCLE` - User lifecycle

---

## Rate Limits

- Analytics endpoints: 240/min, 1200/hour
- Query endpoint: 2400/hour

---

## AI Crawler User Agents (for server-side tracking)

These crawlers won't show in PostHog (JS-based), but you can track them server-side:

```
GPTBot, ChatGPT-User, ClaudeBot, Claude-Web, PerplexityBot,
Google-Extended, Applebot-Extended, CCBot, anthropic-ai
```

To track these, add server-side events in Next.js middleware or API routes.

---

## Important Notes

1. **API Key required:** Personal API key needed (not the public project key)
2. **EU Region:** Mediar uses `eu.i.posthog.com` (not `app.posthog.com`)
3. **Project ID:** Get from `/api/projects/` endpoint first
4. **HogQL:** Use for complex queries not supported by filters
5. **AI traffic:** Client-side PostHog tracks referrals, not crawler bots
6. **Rate limits:** 240 requests/min for analytics endpoints
