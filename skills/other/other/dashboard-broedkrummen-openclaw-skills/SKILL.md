---
name: Dashboard
slug: dashboard
version: 1.0.1
description: Build custom dashboards from any data source with local hosting and visual QA loops.
changelog: User-driven data source model, explicit credential handling
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Data Storage

```
~/dashboard/
├── registry.json           # Dashboard index
├── {name}/
│   ├── config.json         # Layout, widgets
│   ├── data.json           # Current data
│   └── index.html          # Dashboard page
```

Create on first use: `mkdir -p ~/dashboard`

## Scope

This skill:
- ✅ Generates static HTML dashboards
- ✅ Creates fetch scripts user can run
- ✅ Stores dashboards in ~/dashboard/

**User-driven model:**
- User specifies data sources
- User provides API credentials via environment
- User runs fetch scripts (cron or manual)
- Skill generates HTML and fetch scripts

This skill does NOT:
- ❌ Access credentials without user providing them
- ❌ Run automated fetches (user's cron runs scripts)
- ❌ Scrape services without user consent

## Quick Reference

| Topic | File |
|-------|------|
| Data source patterns | `sources.md` |
| Visual design rules | `design.md` |
| Widget templates | `widgets.md` |

## Core Rules

### 1. User Provides Data
When creating a dashboard:
```
User: "Dashboard for my Stripe revenue"
Agent: "I'll create a fetch script. Set STRIPE_API_KEY 
        in your environment, then run the script."
→ Generates: ~/dashboard/stripe/fetch.sh
→ User adds to cron: */15 * * * * ~/dashboard/stripe/fetch.sh
```

### 2. Architecture
```
[User's Cron] → [fetch.sh] → [data.json] → [index.html]
                    ↓
              Uses $API_KEY from env
```

Agent generates scripts. User runs them.

### 3. Fetch Script Template
```bash
#!/bin/bash
# Requires: STRIPE_API_KEY in environment
curl -s -u "$STRIPE_API_KEY:" \
  https://api.stripe.com/v1/balance \
  | jq '.' > ~/dashboard/stripe/data.json
```

### 4. Visual QA (Before Delivery)
- Open in browser, take screenshot
- Check: no overlap, readable fonts (≥14px), good contrast
- If issues → fix → repeat
- Only deliver after visual validation

### 5. Design Defaults
| Element | Value |
|---------|-------|
| Background | `#0f172a` (dark) / `#f8fafc` (light) |
| Text | `#e2e8f0` (dark) / `#1e293b` (light) |
| Spacing | 16px, 24px, 32px |
| Corners | 8px |
| KPI | 48-72px number, 14px label |

### 6. Security
- Credentials via env vars, never in files
- Dashboards on `127.0.0.1` by default
- No PII in displayed data
- User adds auth if exposing to network
