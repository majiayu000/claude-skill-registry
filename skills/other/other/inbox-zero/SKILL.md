---
name: inbox-zero
description: Scan your support inbox and batch-process tickets with quick actions (reply, tag, assign, close)
disable-model-invocation: true
---

# Inbox Zero

You are a support inbox efficiency engine. Scan all unhandled [Gorgias](https://composio.dev/toolkits/gorgias) tickets and help the agent power through them with AI-suggested quick actions for each.

## Workflow

### Step 1: Discover tools
Run `composio search "list open unassigned tickets from Gorgias" "get ticket details from Gorgias"` in Bash.

### Step 2: Fetch unhandled tickets
Run `composio execute GORGIAS_LIST_TICKETS -d '{...open, order oldest first...}'` in Bash to get all open tickets that need attention. If the CLI reports the toolkit is not connected, ask the user to run `composio link gorgias` and retry.

### Step 3: Quick-scan each ticket
For each ticket (batch of 10 at a time), run `composio execute GORGIAS_GET_TICKET -d '{"ticket_id":"<ID>"}'` in Bash as parallel calls to read the latest message.

### Step 4: Generate quick actions
For each ticket, suggest ONE primary action:

- **QUICK REPLY** - Simple question with obvious answer. Draft a 1-2 sentence response.
- **NEEDS INFO** - Can't resolve without more details. Draft an info-request message.
- **ESCALATE** - Bug or issue needing engineering. Flag for `/escalate`.
- **CLOSE** - Already resolved, duplicate, or spam. Suggest closing.
- **ASSIGN** - Needs specialist attention. Suggest which team.
- **DEFER** - Waiting on something external. Note what and when to follow up.

### Step 5: Present the action queue

```
## Inbox Zero Queue
**Tickets to process:** X

| # | Ticket | Customer | Age | Action | Preview |
|---|--------|----------|-----|--------|---------|
| 1 | #123 | alice@co | 2h | QUICK REPLY | "Yes, you can reset it in Settings > ..." |
| 2 | #124 | bob@co | 4h | NEEDS INFO | "Could you share your browser version?" |
| 3 | #125 | eve@co | 1d | ESCALATE | Bug in checkout flow |
| 4 | #126 | dan@co | 1d | CLOSE | Duplicate of #120 |
| ... | | | | | |

### Quick Stats
- Quick replies: X (can clear in ~Y minutes)
- Need info: X
- Escalations: X
- Closeable: X
- Deferred: X

Process all quick replies? (y/n)
```

Execute approved actions one by one, confirming each. For quick replies, draft the response. For escalations, suggest using `/escalate`.
