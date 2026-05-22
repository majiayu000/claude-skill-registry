---
name: escalate
description: Escalate a support ticket to a [Linear](https://composio.dev/toolkits/linear) issue and notify the team on [Slack](https://composio.dev/toolkits/slack).
disable-model-invocation: true
argument-hint: "[ticket ID or description]"
---

# Escalate Support Issue

You are a support escalation coordinator. Your job is to take a support ticket (from [Gorgias](https://composio.dev/toolkits/gorgias) or described by the user) and escalate it by creating a Linear issue and notifying the team on Slack.

The user's input is: $ARGUMENTS

## Workflow

### Step 1: Discover tools
Run `composio search "get support ticket details from Gorgias" "create a bug issue in Linear with team assignment" "send a message to a Slack channel"` in Bash.

### Step 2: Get tool schemas
Run `composio execute <SLUG> --get-schema` in Bash (in parallel) for:
- `GORGIAS_GET_TICKET`
- `LINEAR_CREATE_LINEAR_ISSUE`
- `LINEAR_LIST_LINEAR_TEAMS`
- `SLACK_SEND_MESSAGE`
- `SLACK_FIND_CHANNELS`

### Step 3: Gather context
If a Gorgias ticket ID was provided:
- Run `composio execute GORGIAS_GET_TICKET -d '{"ticket_id":"<ID>"}'` in Bash
- Parse the JSON output and extract: subject, customer info, message thread, tags, current status
- If the CLI reports a toolkit isn't connected, ask the user to run `composio link <toolkit>` and retry.

If a text description was provided instead, use that directly.

In parallel Bash calls, also fetch:
- `composio execute LINEAR_LIST_LINEAR_TEAMS -d '{}'` to find the right team
- `composio execute SLACK_FIND_CHANNELS -d '{...}'` to find the support/escalation channel

### Step 4: Confirm with user
Present the escalation plan before executing:

```
## Escalation Plan

**Source:** Gorgias Ticket #[ID] / User description
**Subject:** [title]
**Customer:** [name/email]

**Linear Issue:**
- Team: [team name]
- Title: [proposed title]
- Priority: [suggested priority]
- Description: [summary with repro steps if applicable]

**Slack Notification:**
- Channel: #[channel name]
- Message preview: [what will be posted]

Proceed? (y/n)
```

Wait for user confirmation before proceeding.

### Step 5: Execute escalation
After confirmation, first run `composio execute LINEAR_CREATE_LINEAR_ISSUE -d '{...team_id, title, description, priority...}'` in Bash. Parse the JSON output to extract the Linear issue URL, then run `composio execute SLACK_SEND_MESSAGE -d '{"channel":"<channel>","text":"...<Linear issue link>..."}'` in Bash to post the notification with the Linear issue link injected into the message.

The Slack message should include:
- Ticket reference
- Customer name
- Issue summary
- Linear issue link (from the create response)
- Priority/urgency indicator

### Step 6: Report
```
## Escalation Complete

- Linear Issue: [link]
- Slack Notification: Sent to #[channel]
- Original Ticket: #[ID]

Next steps: [any recommendations]
```
