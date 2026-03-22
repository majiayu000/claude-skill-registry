---
name: posthog
description: >
  Query PostHog analytics via REST API. Check event ingestion, view feature flags,
  inspect user sessions, query trends, and manage experiments. Use for any analytics,
  feature flag, or user behavior task.
allowed-tools: Bash, Read, Grep, Glob
---

# PostHog REST API

Query FuzzyCat's analytics and feature flags via the PostHog API.

## Authentication

```bash
POSTHOG_KEY=$(grep NEXT_PUBLIC_POSTHOG_KEY .env.local | cut -d'"' -f2)
POSTHOG_HOST=$(grep NEXT_PUBLIC_POSTHOG_HOST .env.local | cut -d'"' -f2)
# Note: NEXT_PUBLIC_POSTHOG_KEY is a project API key (phc_...), sufficient for most queries
# For admin operations, you'd need a personal API key from PostHog settings
```

## Common Commands

### Events

```bash
# Recent events (check ingestion is working)
curl -s "$POSTHOG_HOST/api/event/?limit=10" \
  -H "Authorization: Bearer $POSTHOG_KEY" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for e in d.get('results',[])[:10]:
    print(f\"{e['timestamp'][:19]} | {e['event']} | {e.get('properties',{}).get('\$current_url','')}\")
"

# Filter events by type
curl -s "$POSTHOG_HOST/api/event/?event=\$pageview&limit=10" \
  -H "Authorization: Bearer $POSTHOG_KEY" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for e in d.get('results',[]):
    url = e.get('properties',{}).get('\$current_url','')
    print(f\"{e['timestamp'][:19]} | {url}\")
"

# Custom events (e.g., enrollment, payment)
curl -s "$POSTHOG_HOST/api/event/?event=enrollment_started&limit=10" \
  -H "Authorization: Bearer $POSTHOG_KEY" | python3 -m json.tool
```

### Persons (Users)

```bash
# List persons
curl -s "$POSTHOG_HOST/api/persons/?limit=10" \
  -H "Authorization: Bearer $POSTHOG_KEY" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for p in d.get('results',[]):
    props = p.get('properties',{})
    print(f\"{p['id'][:8]}... | {props.get('email','N/A')} | {props.get('\$os','')}\")
"

# Search person by email
curl -s "$POSTHOG_HOST/api/persons/?search=user@example.com" \
  -H "Authorization: Bearer $POSTHOG_KEY" | python3 -m json.tool
```

### Feature Flags

```bash
# List feature flags
curl -s "$POSTHOG_HOST/api/feature_flag/" \
  -H "Authorization: Bearer $POSTHOG_KEY" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for f in d.get('results',[]):
    print(f\"{f['key']} | Active: {f['active']} | Rollout: {f.get('rollout_percentage', 'N/A')}%\")
"

# Get specific flag
curl -s "$POSTHOG_HOST/api/feature_flag/?key=flag-name" \
  -H "Authorization: Bearer $POSTHOG_KEY" | python3 -m json.tool

# Evaluate flags for a user
curl -s -X POST "$POSTHOG_HOST/decide/?v=3" \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$POSTHOG_KEY\",
    \"distinct_id\": \"user-id-here\"
  }" | python3 -m json.tool
```

### Insights / Trends

```bash
# Get saved insights
curl -s "$POSTHOG_HOST/api/insight/?limit=10" \
  -H "Authorization: Bearer $POSTHOG_KEY" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for i in d.get('results',[]):
    print(f\"{i['id']} | {i['name']} | {i.get('filters',{}).get('insight','TRENDS')}\")
"

# Query a trend (pageviews last 7 days)
curl -s -X POST "$POSTHOG_HOST/api/insight/trend/" \
  -H "Authorization: Bearer $POSTHOG_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [{"id": "$pageview", "type": "events"}],
    "date_from": "-7d",
    "interval": "day"
  }' | python3 -m json.tool
```

### Dashboards

```bash
# List dashboards
curl -s "$POSTHOG_HOST/api/dashboard/" \
  -H "Authorization: Bearer $POSTHOG_KEY" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for dash in d.get('results',[]):
    print(f\"{dash['id']} | {dash['name']} | Tiles: {len(dash.get('tiles',[]))}\")
"
```

## FuzzyCat-Specific

- **Project key**: `phc_Q8tll1S5mEFbvsbVG79E7N4adHA5ENdIlHjKo4HZAeo`
- **Host**: `https://us.i.posthog.com`
- **Key files**: `lib/posthog/client.ts`, `lib/posthog/server.ts`, `components/providers/posthog-provider.tsx`
- **Tracked events**: Page views, enrollment flow steps, payment events, clinic dashboard usage
- **Web analytics**: PostHog replaces Google Analytics for privacy-friendly tracking
