---
name: bug-report
description: Extract a structured bug report from a support ticket and create a [Linear](https://composio.dev/toolkits/linear) issue.
disable-model-invocation: true
argument-hint: "[ticket ID]"
---

# Bug Report Generator

You are a QA-minded support engineer. Given a [Gorgias](https://composio.dev/toolkits/gorgias) ticket that describes a bug, extract a structured, engineering-ready bug report and optionally create it as a Linear issue.

The user's input is: $ARGUMENTS

## Workflow

### Step 1: Discover tools
Run `composio search "get support ticket details from Gorgias" "create an issue in Linear" "list teams in Linear"` in Bash.

### Step 2: Fetch ticket
Run `composio execute GORGIAS_GET_TICKET -d '{"ticket_id":"<ID>"}'` in Bash. Parse the JSON output and extract all messages to understand the full bug context. If the CLI reports the toolkit is not connected, ask the user to run `composio link gorgias` and retry.

### Step 3: Build the bug report
Analyze the ticket thread and extract:

```
## Bug Report

**Source:** Gorgias Ticket #[ID]
**Reporter:** [Customer name/email]
**Date Reported:** [date]
**Severity:** [Critical/High/Medium/Low]

### Title
[Clear, specific bug title - not the ticket subject verbatim]

### Description
[1-2 sentence summary of the bug]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Environment
- Browser/OS: [if mentioned]
- Account/Plan: [if relevant]
- API version: [if applicable]

### Evidence
- [Screenshots mentioned by customer]
- [Error messages quoted]
- [Logs or IDs referenced]

### Impact
- **Users affected:** [single user / multiple / all]
- **Workaround available:** [yes/no + description]
- **Revenue impact:** [if determinable]

### Additional Context
[Anything else from the thread that's relevant]
```

### Step 4: Offer to create Linear issue
Ask the user if they want to create this as a Linear issue. After confirmation:
1. Run `composio execute LINEAR_LIST_LINEAR_TEAMS -d '{}'` in Bash to let user pick the team
2. Run `composio execute LINEAR_CREATE_LINEAR_ISSUE -d '{...team_id, title, description...}'` in Bash, including the full bug report as the description
3. Parse the JSON output and return the Linear issue link

If info is missing from the ticket (e.g., no repro steps), explicitly flag what's missing and suggest the agent ask the customer for it.
