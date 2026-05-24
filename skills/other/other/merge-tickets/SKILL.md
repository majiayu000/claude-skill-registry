---
name: merge-tickets
description: Find and flag duplicate or related [Gorgias](https://composio.dev/toolkits/gorgias) tickets that should be merged
disable-model-invocation: true
---

# Duplicate Ticket Finder

You are a ticket deduplication specialist. Scan recent Gorgias tickets to find duplicates or closely related tickets from the same customer or about the same issue.

## Workflow

### Step 1: Discover tools
Run `composio search "list recent support tickets from Gorgias" "get ticket details from Gorgias"` in Bash.

### Step 2: Fetch recent tickets
Run `composio execute GORGIAS_LIST_TICKETS -d '{...limit 50-100, open/pending...}'` in Bash to fetch the last 50-100 open/pending tickets. If the CLI reports the toolkit is not connected, ask the user to run `composio link gorgias` and retry.

### Step 3: Get details for comparison
For each ticket, extract:
- Customer email
- Subject line
- First message content
- Tags
- Creation date

Run `composio execute GORGIAS_GET_TICKET -d '{"ticket_id":"<ID>"}'` in Bash (in parallel) for tickets where the list doesn't provide enough detail.

### Step 4: Detect duplicates
Apply these matching heuristics:

**Strong match (likely duplicate):**
- Same customer email + similar subject (>70% overlap)
- Same customer email + same tags + created within 24h
- Different customers but near-identical subject + message body

**Weak match (possibly related):**
- Same customer email + different but related subjects
- Different customers + same rare error message or product area
- Tickets referencing the same order/account ID

### Step 5: Present findings

```
## Duplicate Ticket Analysis

### Strong Matches (likely duplicates)
#### Group 1
| Ticket | Customer | Subject | Created | Status |
|--------|----------|---------|---------|--------|
| #123 | user@co.com | "Login broken" | 2h ago | Open |
| #119 | user@co.com | "Can't log in" | 5h ago | Open |
**Similarity:** Same customer, same issue (login), 3h apart
**Recommendation:** Merge #123 into #119 (keep older as primary)

#### Group 2
...

### Weak Matches (possibly related)
| Tickets | Reason | Recommendation |
|---------|--------|----------------|

### Stats
- Tickets scanned: X
- Duplicate groups found: X
- Estimated duplicates: X
- Potential time saved by merging: ~Xh
```

Note: This skill identifies duplicates but does NOT auto-merge. Present findings for agent review.
