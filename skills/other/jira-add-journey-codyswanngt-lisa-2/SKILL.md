---
name: jira-add-journey
description: "Add a Validation Journey section to an existing JIRA ticket by reading the ticket description, understanding the feature, and generating the journey steps and assertions."
---

# Add Validation Journey to Existing JIRA Ticket

Read an existing JIRA ticket, understand the feature or fix it describes, analyze the codebase to determine the verification approach, and append a Validation Journey section to the ticket description.

## Arguments

`$ARGUMENTS`: `<TICKET_ID>`

- `TICKET_ID` (required): JIRA ticket key (e.g., `PROJ-123`)

## Prerequisites

- `JIRA_API_TOKEN` environment variable set
- `jira-cli` configured (`~/.config/.jira/.config.yml`)

## Workflow

### Step 1: Read the Ticket

Use the Atlassian MCP or jira-cli to read the full ticket details:

```bash
jira issue view <TICKET_ID>
```

Extract: title, description, acceptance criteria, components, labels, linked tickets.

### Step 2: Check for Existing Journey

Run the parser to see if a Validation Journey already exists:

```bash
python3 .claude/skills/jira-journey/scripts/parse-plan.py <TICKET_ID> 2>&1
```

If the parser succeeds and returns steps, the ticket already has a journey. Report this to the user and stop.

### Step 3: Analyze the Feature

Based on the ticket description and acceptance criteria, determine the appropriate verification approach. Stack-specific overrides provide the analysis logic.

### Step 4: Draft the Validation Journey

Compose the journey following the Validation Journey format with: Prerequisites, Steps (with evidence markers), and Assertions.

### Step 5: Present to User for Approval

Display the drafted Validation Journey to the user and ask for confirmation before appending it to the ticket.

### Step 6: Append to Ticket Description

After user approval, use the JIRA REST API to append the Validation Journey to the existing ticket description.

### Step 7: Verify

Run the parser again to confirm the journey was added correctly:

```bash
python3 .claude/skills/jira-journey/scripts/parse-plan.py <TICKET_ID>
```
