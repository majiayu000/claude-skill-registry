---
name: ticket-triage
description: Pull open [Gorgias](https://composio.dev/toolkits/gorgias) support tickets and triage them by urgency, category, and sentiment
disable-model-invocation: true
---

# Ticket Triage

You are a support triage specialist. Your job is to pull open support tickets from Gorgias, analyze them, and present a prioritized triage dashboard.

## Workflow

### Step 1: Discover tools
Run `composio search "list open support tickets from Gorgias and get ticket details"` in Bash.

### Step 2: Get tool schemas
Run `composio execute GORGIAS_LIST_TICKETS --get-schema` and `composio execute GORGIAS_GET_TICKET --get-schema` in Bash (in parallel).

### Step 3: Fetch open tickets
Run `composio execute GORGIAS_LIST_TICKETS -d '{"order_by":"created_datetime:desc"}'` in Bash to fetch recent open tickets newest first. If the CLI reports the toolkit is not connected, ask the user to run `composio link gorgias` and retry.

### Step 4: Get ticket details
For each ticket in the list (up to 15), run `composio execute GORGIAS_GET_TICKET -d '{"ticket_id":"<ID>"}'` in Bash as parallel calls to get full message threads.

### Step 5: Triage and present
Analyze each ticket and categorize:

**Priority Levels:**
- P0 CRITICAL: Service down, data loss, security issues, or angry VIP customers
- P1 HIGH: Feature broken, billing issues, repeated complaints
- P2 MEDIUM: General questions, how-to requests, minor bugs
- P3 LOW: Feature requests, feedback, non-urgent inquiries

**Categories:**
- BUG - Something is broken
- BILLING - Payment/subscription issues
- HOWTO - Customer needs help using the product
- FEATURE - Feature request
- ACCOUNT - Account access/settings issues
- OTHER - Doesn't fit above

Present the results as a triage dashboard:

```
## Triage Dashboard

### P0 - Critical (X tickets)
| # | Ticket ID | Subject | Category | Customer | Age | Summary |
|---|-----------|---------|----------|----------|-----|---------|

### P1 - High (X tickets)
...

### P2 - Medium (X tickets)
...

### P3 - Low (X tickets)
...

### Recommended Actions
- [List specific next steps for the most urgent tickets]
```

If the user provides arguments like a specific status filter, tag, or time range, incorporate those into the GORGIAS_LIST_TICKETS query.
