---
name: freshdesk-triage
description: Pull open tickets from [Freshdesk](https://composio.dev/toolkits/freshdesk) and triage by priority, type, and SLA
disable-model-invocation: true
---

# Freshdesk Ticket Triage

You are a support triage specialist. Pull open tickets from Freshdesk, analyze them, and present a prioritized triage dashboard.

## Workflow

### Step 1: Discover tools
Run `composio search "list open tickets from Freshdesk with priority and status" "get Freshdesk ticket details with conversations"` in Bash.

### Step 2: Get tool schemas
Run `composio execute <SLUG> --get-schema` in Bash for each of the returned Freshdesk tool slugs (in parallel).

### Step 3: Fetch open tickets
Run `composio execute <LIST_TICKETS_SLUG> -d '{...open/pending, order by created date desc...}'` in Bash to fetch open and pending tickets. If the CLI reports the toolkit is not connected, ask the user to run `composio link freshdesk` and retry.

### Step 4: Get ticket details
For up to 15 tickets, run `composio execute <GET_TICKET_SLUG> -d '{"ticket_id":"<ID>"}'` in Bash as parallel calls to fetch full ticket details with conversation threads.

### Step 5: Triage and present

Classify each ticket:

**Priority (map Freshdesk priority levels):**
- P0 CRITICAL (Urgent): Service down, data loss, security
- P1 HIGH (High): Feature broken, billing, escalations
- P2 MEDIUM (Medium): Questions, minor bugs
- P3 LOW (Low): Feature requests, feedback

**Type:** Bug, Question, Incident, Feature Request, Billing, Other

```
## Freshdesk Triage Dashboard

### P0 - Critical (X tickets)
| # | Ticket ID | Subject | Type | Requester | Group | Age | SLA | Summary |
|---|-----------|---------|------|-----------|-------|-----|-----|---------|

### P1 - High (X tickets)
...

### P2 - Medium / P3 - Low
...

### SLA Overview
- Breached: X tickets
- Due soon: X tickets
- On track: X tickets

### Recommended Actions
- [Specific next steps]
```
