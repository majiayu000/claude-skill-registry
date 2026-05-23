---
name: auto-tag
description: Automatically analyze and tag untagged [Gorgias](https://composio.dev/toolkits/gorgias) tickets based on content.
disable-model-invocation: true
argument-hint: "[ticket ID or 'batch']"
---

# Auto-Tag Tickets

You are a ticket classification engine. Analyze untagged or under-tagged Gorgias tickets, determine the correct tags based on content, and suggest (or apply) them.

The user's input is: $ARGUMENTS

## Workflow

### Step 1: Discover tools
Run `composio search "list tickets from Gorgias filtered by tags" "get ticket details from Gorgias" "list all available ticket tags in Gorgias"` in Bash.

### Step 2: Get available tags
Run `composio execute GORGIAS_LIST_TICKET_TAGS -d '{}'` in Bash to get the full set of tags configured in the system. If the CLI reports the toolkit is not connected, ask the user to run `composio link gorgias` and retry.

### Step 3: Fetch tickets
- If a specific ticket ID was given: run `composio execute GORGIAS_GET_TICKET -d '{"ticket_id":"<ID>"}'` in Bash
- If "batch" or no argument: run `composio execute GORGIAS_LIST_TICKETS -d '{...filter for untagged...}'` in Bash

### Step 4: Classify each ticket
For each ticket, read the subject + message body and determine:
- **Primary tag** (the main topic)
- **Secondary tags** (additional relevant labels)
- **Confidence** (High/Medium/Low)

Classification categories to consider:
- Product area (billing, auth, integrations, API, UI, mobile, etc.)
- Issue type (bug, question, feature-request, complaint, praise)
- Urgency indicators (outage, blocking, data-loss)
- Customer segment (enterprise, startup, free-tier)

### Step 5: Present recommendations

```
## Auto-Tag Results

### Available Tags in System
[list them]

### Tagging Recommendations
| Ticket ID | Subject | Recommended Tags | Confidence | Reasoning |
|-----------|---------|-----------------|------------|-----------|
| #123 | "Can't login" | auth, bug | High | Customer reports 403 error on login |
| ... | | | | |

### Summary
- Tickets analyzed: X
- High confidence: X
- Medium confidence: X (review recommended)
- Low confidence: X (manual review needed)
```

Ask the user if they'd like to apply any of the suggested tags. Do NOT apply tags without explicit confirmation.
