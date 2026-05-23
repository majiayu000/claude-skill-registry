---
name: sentry
description: >-
  Analyze Sentry error monitoring data through read-only API queries to inspect
  issues, summarize production errors, retrieve event details, and assess
  application health. Uses a bundled Python script for deterministic API calls
  with pagination, retry logic, and automatic PII redaction. Trigger when the
  user asks to investigate Sentry issues, list recent errors, check issue
  frequency, retrieve event stack traces, or summarize error trends for a
  project. Requires SENTRY_AUTH_TOKEN environment variable with read-only
  scopes.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - analyzer
    - observability
    - sentry
    - error-monitoring
    - production
  provenance:
    upstream_source: "sentry"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T15:55:22+00:00"
    generator_version: "1.0.0"
    intent_confidence: 0.58
---

# Sentry Issue Analyzer

Perform read-only analysis of Sentry error monitoring data to inspect issues, retrieve events, and assess production application health through the Sentry API.

## Overview

This skill queries the Sentry API to analyze production error data. It is designed for developers and SREs who need to investigate issues, understand error trends, and triage production incidents without leaving their development environment.

**What it analyzes:**
- Open and unresolved issues across projects and environments
- Individual issue details including frequency, first/last seen timestamps, and affected users
- Event-level data including culprit, environment, release, and request context
- Error trends over configurable time windows (1h to 90d)

**What it reports:**
- Ranked issue lists with title, short ID, status, frequency, and recency
- Issue detail breakdowns with metadata, tags, and assignment status
- Event timelines with timestamps, environments, and release versions
- Triage recommendations based on frequency, recency, and user impact

**Security constraints:**
- All API calls are read-only (GET requests only)
- PII (emails, IP addresses) is automatically redacted in output
- Auth tokens are never echoed or logged
- Stack trace entries are excluded by default (opt-in with `--include-entries`)

## Authentication Setup

Before running any commands, the user must have a valid `SENTRY_AUTH_TOKEN`. If the token is not set:

1. Direct the user to create one at: `https://sentry.io/settings/account/api/auth-tokens/`
2. Required scopes: `project:read`, `event:read`, `org:read`
3. Set the environment variable:
   ```bash
   export SENTRY_AUTH_TOKEN="sntrys_..."
   ```
4. Optionally set defaults:
   ```bash
   export SENTRY_ORG="my-org"
   export SENTRY_PROJECT="my-project"
   export SENTRY_BASE_URL="https://sentry.io"  # or self-hosted URL
   ```

Never ask the user to paste the token directly in chat. Ask them to set it as an environment variable and confirm when ready.

## Analysis Checklist

### Issue Triage

- [ ] List unresolved issues sorted by most recent occurrence
- [ ] Identify high-frequency issues (count > 100 in 24h)
- [ ] Check issue age (first_seen) to distinguish new regressions from chronic problems
- [ ] Review assigned vs unassigned issues for ownership gaps
- [ ] Compare issue counts across environments (prod vs staging)

### Event Investigation

- [ ] Retrieve latest events for a specific issue
- [ ] Check event distribution across releases to identify regression sources
- [ ] Review event context (browser, OS, URL) for pattern detection
- [ ] Examine culprit field to locate the failing code path
- [ ] Optionally inspect stack trace entries for root cause analysis

### Health Assessment

- [ ] Count total unresolved issues per project
- [ ] Identify issues with rapidly increasing event counts
- [ ] Check for issues affecting multiple environments
- [ ] Review issues by tag to find systemic patterns (e.g., same browser, same endpoint)

## Metrics

### Issue Severity

| Metric | Description | Low | Medium | High | Critical |
|--------|-------------|-----|--------|------|----------|
| Event count (24h) | Events in last 24 hours | < 10 | 10-100 | 100-1000 | > 1000 |
| User impact | Unique users affected | < 5 | 5-50 | 50-500 | > 500 |
| Issue age | Time since first_seen | > 30d | 7-30d | 1-7d | < 1d (new) |
| Recurrence | Times issue re-opened | 0 | 1 | 2-3 | > 3 |

### Response Targets

| Priority | Response Time | Resolution Target |
|----------|---------------|-------------------|
| Critical | Immediate | 4 hours |
| High | 1 hour | 24 hours |
| Medium | 4 hours | 1 week |
| Low | Next sprint | Best effort |

## Workflow

### Step 1: Verify authentication

Confirm `SENTRY_AUTH_TOKEN` is set and org/project are configured:

```bash
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." 2>/dev/null && pwd || echo "$HOME/.claude/skills/sentry")"
python3 "$SKILL_DIR/scripts/sentry_api.py" \
  list-issues \
  --org "$SENTRY_ORG" \
  --project "$SENTRY_PROJECT" \
  --limit 1
```

If this fails, guide the user through authentication setup.

### Step 2: List recent issues

```bash
python3 "$SKILL_DIR/scripts/sentry_api.py" \
  list-issues \
  --org "$SENTRY_ORG" \
  --project "$SENTRY_PROJECT" \
  --environment prod \
  --time-range 24h \
  --limit 25 \
  --query "is:unresolved"
```

### Step 3: Investigate a specific issue

Resolve a short ID (e.g., `PROJ-123`) to a numeric issue ID:

```bash
python3 "$SKILL_DIR/scripts/sentry_api.py" \
  list-issues \
  --org "$SENTRY_ORG" \
  --project "$SENTRY_PROJECT" \
  --query "PROJ-123" \
  --limit 1
```

Then get full details:

```bash
python3 "$SKILL_DIR/scripts/sentry_api.py" \
  issue-detail \
  1234567890
```

### Step 4: Examine events

List recent events for an issue:

```bash
python3 "$SKILL_DIR/scripts/sentry_api.py" \
  issue-events \
  1234567890 \
  --limit 10
```

Get a single event's detail:

```bash
python3 "$SKILL_DIR/scripts/sentry_api.py" \
  event-detail \
  --org "$SENTRY_ORG" \
  --project "$SENTRY_PROJECT" \
  abcdef1234567890
```

Add `--include-entries` only when the user explicitly requests stack trace data.

### Step 5: Synthesize findings

After gathering data, present a structured analysis:
- Summarize the top issues by severity and frequency
- Identify patterns (same culprit, same release, same environment)
- Recommend triage priorities based on the metrics table above
- Suggest next steps (assign owner, link to code, escalate)

## Report Format

### Summary

```
Sentry Analysis Report
======================
Organization: {org}
Project: {project}
Time Window: {time_range}
Environment: {environment}
Generated: {timestamp}

Overview:
  Total unresolved issues: {count}
  New issues (< 24h): {count}
  High-frequency issues (> 100 events): {count}

Top Issues:
  1. {title} ({short_id}) - {count} events, last seen {last_seen}
  2. {title} ({short_id}) - {count} events, last seen {last_seen}
  3. {title} ({short_id}) - {count} events, last seen {last_seen}
```

### Detailed Issue Report

```
Issue: {title}
Short ID: {short_id}
Status: {status}
First Seen: {first_seen}
Last Seen: {last_seen}
Events (24h): {count}
Users Affected: {user_count}
Assigned To: {assignee or "Unassigned"}
Culprit: {culprit}
Tags: {top_tags}

Recent Events:
  - {timestamp} | {environment} | {release} | {culprit}
  - {timestamp} | {environment} | {release} | {culprit}

Recommendation: {priority_level} - {suggested_action}
```

## API Reference

All endpoints are read-only (GET). The bundled script handles authentication, pagination, and error retry.

| Command | Endpoint | Required Params |
|---------|----------|-----------------|
| `list-issues` | `/api/0/projects/{org}/{project}/issues/` | org, project |
| `issue-detail` | `/api/0/issues/{issue_id}/` | issue_id |
| `issue-events` | `/api/0/issues/{issue_id}/events/` | issue_id |
| `event-detail` | `/api/0/projects/{org}/{project}/events/{event_id}/` | org, project, event_id |

### Default Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--time-range` | `24h` | Stats period (e.g., 1h, 24h, 7d, 14d, 30d, 90d) |
| `--environment` | `prod` | Target environment |
| `--limit` | `20` | Max results (capped at 50) |
| `--query` | empty | Sentry search query (e.g., `is:unresolved`, `assigned:me`) |

## Examples

### Example 1: Production incident triage

```
User: What are the top issues in production for the last 24 hours?
Assistant: Let me query Sentry for recent production issues.

[Runs list-issues with --time-range 24h --environment prod --limit 10]

Sentry Analysis Report
======================
Project: my-project | Environment: prod | Window: 24h

Top 5 Unresolved Issues:
1. TypeError: Cannot read property 'id' of undefined (PROJ-847)
   - 342 events | 89 users | Last seen: 12 min ago
   - Culprit: app/api/handlers/order.py

2. ConnectionError: Redis connection refused (PROJ-901)
   - 156 events | N/A | Last seen: 3 min ago
   - Culprit: app/cache/redis_client.py

3. ValidationError: Invalid email format (PROJ-512)
   - 87 events | 43 users | Last seen: 1h ago
   - Culprit: app/forms/registration.py

Recommendations:
- PROJ-847: Critical - investigate the undefined 'id' in order handler
- PROJ-901: High - check Redis connectivity, possible infrastructure issue
- PROJ-512: Medium - add input sanitization to registration form
```

### Example 2: Specific issue investigation

```
User: Investigate PROJ-847 in more detail.
Assistant: Resolving PROJ-847 to get the full issue details...

[Runs list-issues with --query "PROJ-847" then issue-detail and issue-events]

Issue Detail: TypeError: Cannot read property 'id' of undefined
================================================================
Status: unresolved
First Seen: 2026-02-03T14:22:00Z (new regression)
Last Seen: 2026-02-04T15:43:00Z
Events (24h): 342
Users Affected: 89
Release: v2.4.1 (deployed yesterday)

Recent Events (last 5):
  - 15:43 | prod | v2.4.1 | app/api/handlers/order.py
  - 15:41 | prod | v2.4.1 | app/api/handlers/order.py
  - 15:38 | prod | v2.4.1 | app/api/handlers/order.py

Analysis:
- This is a new regression introduced in v2.4.1 (deployed yesterday)
- All events come from the same code path in order.py
- 89 unique users affected suggests it hits a common flow
- Recommendation: Roll back v2.4.1 or hotfix the order handler
```

## Interpretation Guide

### Issue Status

| Status | Meaning | Action |
|--------|---------|--------|
| `unresolved` | Active, needs attention | Triage and assign |
| `resolved` | Fixed, monitoring | Verify no recurrence |
| `ignored` | Deliberately suppressed | Review periodically |
| `muted` | Temporarily silenced | Will auto-unmute |

### Time Range Selection

| Window | Use Case |
|--------|----------|
| `1h` | Active incident investigation |
| `24h` | Daily triage (default) |
| `7d` | Weekly review |
| `14d` | Sprint retrospective |
| `30d` | Monthly health check |
| `90d` | Quarterly trend analysis |

### Output Rules

- Always order issues by most recent occurrence
- Show title, short_id, status, event count, last_seen, and culprit
- Redact PII (emails, IPs) automatically via the bundled script
- Never print raw auth tokens or full stack traces unless explicitly requested
- If no results found, state explicitly: "No issues found matching the query"
