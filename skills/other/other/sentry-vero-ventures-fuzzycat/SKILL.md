---
name: sentry
description: >
  Monitor and manage Sentry error tracking via CLI and REST API. List unresolved issues,
  check error rates, view stack traces, resolve issues, and manage releases.
  Use for any error monitoring or debugging task.
allowed-tools: Bash, Read, Grep, Glob
---

# Sentry CLI & REST API

Monitor FuzzyCat's error tracking via the Sentry CLI and API.

## Authentication

```bash
source <(grep -E '^(SENTRY_AUTH_TOKEN|SENTRY_ORG|SENTRY_PROJECT)=' .env.local | sed 's/^/export /')
# SENTRY_ORG=fuzzycatapp
# SENTRY_PROJECT=javascript-nextjs
# CLI auto-reads SENTRY_AUTH_TOKEN from env
```

## CLI Commands (`npx @sentry/cli`)

### Issues

```bash
# List unresolved issues (most common check)
npx @sentry/cli issues list --project $SENTRY_PROJECT -s unresolved

# List issues with details
npx @sentry/cli issues list --project $SENTRY_PROJECT -s unresolved --show-columns title,events,users,lastSeen

# Resolve an issue
npx @sentry/cli issues resolve <issue-id>
```

### Releases

```bash
# List releases
npx @sentry/cli releases list --project $SENTRY_PROJECT

# Create a release
npx @sentry/cli releases new <version> --project $SENTRY_PROJECT

# Upload source maps
npx @sentry/cli sourcemaps upload --release <version> .next/

# Finalize a release
npx @sentry/cli releases finalize <version>
```

### Source Maps

```bash
# List uploaded source maps for a release
npx @sentry/cli sourcemaps list --release <version> --project $SENTRY_PROJECT
```

## REST API

For operations the CLI doesn't cover:

```bash
SENTRY_TOKEN=$(grep SENTRY_AUTH_TOKEN .env.local | cut -d'"' -f2)
ORG="fuzzycatapp"
PROJECT="javascript-nextjs"

# List issues (with query)
curl -s "https://sentry.io/api/0/projects/$ORG/$PROJECT/issues/?query=is:unresolved" \
  -H "Authorization: Bearer $SENTRY_TOKEN" | python3 -c "
import sys,json
issues = json.load(sys.stdin)
for i in issues[:10]:
    print(f\"[{i['shortId']}] {i['title']} ({i['count']} events, last: {i['lastSeen'][:10]})\")"

# Get issue details
curl -s "https://sentry.io/api/0/issues/<issue-id>/" \
  -H "Authorization: Bearer $SENTRY_TOKEN" | python3 -m json.tool

# Get latest event for an issue
curl -s "https://sentry.io/api/0/issues/<issue-id>/events/latest/" \
  -H "Authorization: Bearer $SENTRY_TOKEN" | python3 -m json.tool

# Get project stats (error count over time)
curl -s "https://sentry.io/api/0/projects/$ORG/$PROJECT/stats/?stat=received&resolution=1d" \
  -H "Authorization: Bearer $SENTRY_TOKEN" | python3 -m json.tool

# List project environments
curl -s "https://sentry.io/api/0/projects/$ORG/$PROJECT/environments/" \
  -H "Authorization: Bearer $SENTRY_TOKEN" | python3 -m json.tool
```

## Common Tasks

```bash
# Quick health check: any new errors today?
npx @sentry/cli issues list --project javascript-nextjs -s unresolved 2>/dev/null | head -20

# Check error volume
curl -s "https://sentry.io/api/0/projects/fuzzycatapp/javascript-nextjs/stats/?stat=received&resolution=1h" \
  -H "Authorization: Bearer $SENTRY_TOKEN" | python3 -c "
import sys,json
data=json.load(sys.stdin)
for ts,count in data[-24:]:
    from datetime import datetime
    print(f\"{datetime.fromtimestamp(ts).strftime('%H:%M')}: {count} events\")"
```

## FuzzyCat-Specific

- **DSN**: Configured in `NEXT_PUBLIC_SENTRY_DSN` (client-side error reporting)
- **Key files**: `sentry.client.config.ts`, `sentry.server.config.ts`, `sentry.edge.config.ts`
- **Source maps**: Automatically uploaded during Vercel builds
- **Integrations**: Next.js, tRPC error boundary, Stripe webhook error logging
