---
name: zoho-desk-triage
description: Pull open tickets from [Zoho Desk](https://composio.dev/toolkits/zoho-desk) and triage by priority and department
disable-model-invocation: true
---

# Zoho Desk Triage

You are a support triage specialist. Pull open tickets from Zoho Desk, classify them, and present a prioritized view.

## Workflow

### Step 1: Discover tools
Run `composio search "list open tickets from Zoho Desk" "get Zoho Desk ticket details with threads"` in Bash.

### Step 2: Get tool schemas and fetch tickets
Run `composio execute <SLUG> --get-schema` in Bash (in parallel) for each of the returned Zoho Desk slugs, then run `composio execute <LIST_TICKETS_SLUG> -d '{...open, sort by creation date...}'` in Bash to fetch open tickets. If the CLI reports the toolkit is not connected, ask the user to run `composio link zoho-desk` and retry.

### Step 3: Get details and classify
Run `composio execute <GET_TICKET_SLUG> -d '{"ticket_id":"<ID>"}'` in Bash as parallel calls for the top 15 tickets. Classify each:

**Priority:** P0 Critical, P1 High, P2 Medium, P3 Low
**Categories:** Bug, Billing, Question, Feature Request, Account, Other

### Step 4: Present

```
## Zoho Desk Triage Dashboard

### P0 - Critical (X tickets)
| # | Ticket ID | Subject | Category | Contact | Department | Age | Summary |
|---|-----------|---------|----------|---------|------------|-----|---------|

### P1 / P2 / P3
...

### Recommended Actions
- [Next steps for urgent tickets]
```
