---
name: start-ticket
description: Initialize work on a Jira ticket. Creates a new branch with conventional commit prefix based on the ticket type. Use when starting work on a new ticket.
---

# Start Ticket

Initialize work on a Jira ticket by looking up the ticket details and creating an appropriately named branch.

## Usage

```
/start-ticket AB-123
```

## Instructions

### 1. Look Up the Jira Ticket

Use the `/jira-ticket` skill or the Jira MCP tools directly to fetch the ticket details:

```
mcp__jira__jira_get with:
  path: /rest/api/3/issue/{ticketNumber}
  jq: "{key: key, summary: fields.summary, type: fields.issuetype.name}"
```

### 2. Determine the Branch Prefix

Map the Jira issue type to a conventional commit prefix:

| Issue Type | Branch Prefix |
|------------|---------------|
| Story | `feat` |
| Task | `feat` |
| Bug | `fix` |
| Spike | `chore` |
| Sub-task | inherit from parent, or `feat` |
| Improvement | `feat` |
| Technical Debt | `refactor` |
| Documentation | `docs` |
| Default | `feat` |

### 3. Generate Branch Name

Format: `{prefix}/{TICKET-NUMBER}-{kebab-case-summary}`

Rules:
- Convert summary to kebab-case (lowercase, hyphens instead of spaces)
- Remove special characters except hyphens
- Truncate to reasonable length (max ~50 chars for the summary portion)
- Keep the ticket number uppercase

Example: For ticket `AB-123` with summary "Sanitize Input":
```
feat/AB-123-sanitize-input
```

### 4. Create the Branch

```bash
# Ensure we're on main and up to date
git checkout main
git pull origin main

# Create and switch to new branch
git checkout -b {branch-name}
```

### 5. Confirm to User

Output the created branch name and ticket summary so the user knows they're ready to start work.
