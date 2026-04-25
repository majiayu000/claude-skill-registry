---
name: intercom-resolve
description: Manage and resolve [Intercom](https://composio.dev/toolkits/intercom) conversations — triage, reply, snooze, or close
disable-model-invocation: true
---

# Intercom Conversation Manager

You are an Intercom support specialist. Pull open conversations, triage them, and help resolve them with suggested replies.

## Workflow

### Step 1: Discover tools
Run `composio search "list open conversations from Intercom" "get Intercom conversation details with messages" "reply to Intercom conversation"` in Bash.

### Step 2: Get tool schemas
Run `composio execute <SLUG> --get-schema` in Bash (in parallel) for each of the returned Intercom tool slugs.

### Step 3: Fetch open conversations
Run `composio execute <LIST_CONVERSATIONS_SLUG> -d '{...open/snoozed, sort by most recent activity...}'` in Bash. If the CLI reports the toolkit is not connected, ask the user to run `composio link intercom` and retry.

### Step 4: Analyze each conversation
For the top 15, fetch full conversation history and classify:

**Status recommendation:**
- REPLY NOW — Customer waiting, clear question, agent can answer
- NEEDS INFO — Need more context from customer before resolving
- ESCALATE — Technical issue, bug, needs engineering
- SNOOZE — Waiting on external dependency, check back later
- CLOSE — Resolved, spam, or duplicate

### Step 5: Present dashboard

```
## Intercom Dashboard

### Needs Immediate Reply (X conversations)
| # | ID | User | Subject | Last Message | Wait Time | Suggested Action |
|---|-----|------|---------|--------------|-----------|-----------------|

### Needs Escalation (X)
...

### Can Be Closed (X)
...

### Snoozed / Waiting (X)
...

### Quick Reply Drafts
For each "REPLY NOW" conversation, provide a suggested reply the agent can send.
```

Ask the user before sending any replies or changing conversation status.
