---
name: weekly-digest
description: Generate a weekly support digest and post it to [Slack](https://composio.dev/toolkits/slack)
disable-model-invocation: true
---

# Weekly Support Digest

You are a support reporting analyst. Generate a comprehensive weekly support digest covering ticket volume, trends, top issues, and team performance, then post it to Slack.

## Workflow

### Step 1: Discover tools
Run `composio search "list support tickets from Gorgias filtered by date range" "get ticket details from Gorgias" "send a formatted message to Slack channel"` in Bash.

### Step 2: Fetch the week's data
Run `composio execute GORGIAS_LIST_TICKETS -d '{...past 7 days...}'` in Bash to pull all tickets from the past 7 days. Paginate to get the complete set. If the CLI reports the toolkit is not connected, ask the user to run `composio link gorgias` and retry.

### Step 3: Enrich key tickets
For a representative sample (up to 25 tickets), run `composio execute GORGIAS_GET_TICKET -d '{"ticket_id":"<ID>"}'` in Bash as parallel calls to get response time data and message details.

### Step 4: Compile the digest

```
## Weekly Support Digest
**Week of:** [Monday date] - [Sunday date]

### At a Glance
- New tickets: X (+/-Y% vs last week)
- Resolved: X
- Still open: X
- Avg first response: Xh
- Avg resolution time: Xh
- CSAT: X% (if available)

### Top Issues This Week
1. [Issue category] - X tickets - [brief description of trend]
2. [Issue category] - X tickets
3. [Issue category] - X tickets

### Notable Tickets
- **Biggest fire:** #[ID] - [what happened and how it was resolved]
- **Longest open:** #[ID] - [status and why]
- **Best resolution:** #[ID] - [quick/creative resolution worth highlighting]

### Trends
- [Any emerging patterns]
- [Issues that are growing/shrinking]
- [Product areas generating the most tickets]

### Recommendations
- [Process improvements]
- [Product fixes that would reduce ticket volume]
- [Knowledge base articles to create/update]
```

### Step 5: Confirm and post to Slack
Show the digest to the user for review. After confirmation:
1. Run `composio execute SLACK_FIND_CHANNELS -d '{...}'` in Bash to find the target Slack channel, parse the JSON output for the channel ID
2. Format the digest as a Slack message (use markdown_text for formatting)
3. Run `composio execute SLACK_SEND_MESSAGE -d '{"channel":"<channel id>","text":"<digest>"}'` in Bash
4. Parse the JSON output and confirm with the posted message link
