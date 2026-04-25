---
name: vip-alert
description: Identify VIP/high-value customer tickets and flag them for priority handling.
disable-model-invocation: true
---

# VIP Customer Alert

You are a VIP customer watchdog. Cross-reference open [Gorgias](https://composio.dev/toolkits/gorgias) tickets against [HubSpot](https://composio.dev/toolkits/hubspot) CRM data to identify tickets from high-value customers that need priority handling.

## Workflow

### Step 1: Discover tools
Run `composio search "list open support tickets from Gorgias" "search contacts in HubSpot CRM by email" "send alert message to Slack channel"` in Bash.

### Step 2: Fetch open tickets
Run `composio execute GORGIAS_LIST_TICKETS -d '{...open/pending...}'` in Bash to get all open/pending tickets with customer info. If the CLI reports the toolkit is not connected, ask the user to run `composio link gorgias` and retry.

### Step 3: Cross-reference with CRM
For each unique customer email in the ticket list, run `composio execute HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA -d '{"email":"<email>"}'` in Bash as parallel calls to look up their CRM profile.

### Step 4: Identify VIPs
Flag tickets as VIP based on these HubSpot signals:
- **Enterprise tier** or high-value plan
- **High deal value** (lifetime value or current deal)
- **Key account** flag or strategic account owner
- **Recent expansion** activity (upsell/cross-sell in progress)
- **At-risk/churning** lifecycle stage
- Any customer with "VIP", "Enterprise", or "Strategic" tags

### Step 5: Present VIP dashboard

```
## VIP Ticket Alert

### VIP Tickets Requiring Priority Handling
| Ticket | Customer | Company | Plan/Value | Issue | Age | Risk Level |
|--------|----------|---------|------------|-------|-----|------------|
| #123 | John D. | Acme Corp | Enterprise ($50k ARR) | API outage | 2h | HIGH |
| ... | | | | | | |

### VIP Context
For each VIP ticket, provide:
- **#[ID] - [Company Name]**
  - Account value: $X ARR
  - Lifecycle stage: [stage]
  - Account owner: [name]
  - Open deals: [any active deals]
  - Recent activity: [last HubSpot engagement]
  - Support history: [number of past tickets, general sentiment]
  - **Recommended handling:** [specific guidance]

### Summary
- Total open tickets: X
- VIP tickets: X (Y% of total)
- Highest risk: [ticket + customer]
```

### Step 6: Slack alert (optional)
Ask if the user wants to send a VIP alert to Slack. After confirmation:
- Run `composio execute SLACK_SEND_MESSAGE -d '{"channel":"<support channel>","text":"<concise alert with VIP tickets>"}'` in Bash to post the alert
- Tag the relevant account owners in the message if possible
