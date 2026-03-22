---
name: deliverability-watchdog
description: >
  Monitor email deliverability health and flag mailboxes or domains showing signs of spam or bounce issues before they damage sender reputation.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Deliverability"
compatibility: Requires Amplemarket MCP server
---


# Deliverability Watchdog

Monitor email deliverability health and flag mailboxes or domains showing signs of spam or bounce issues before they damage sender reputation.

## Instructions

When invoked (on-demand or recurring), query analytics for deliverability metrics across mailboxes and domains, identify anything trending in the wrong direction, and present a health report.

### Steps

1. **Confirm scope.** Default to last 30 days, full account. Ask if the user wants a specific team, rep, or domain.
2. **Gather the data** by submitting these analytics questions via `mcp__claude_ai_Amplemarket__ask_analytics`:
    - Overall bounce rate and spam rate
    - Bounce rate and spam rate by mailbox
    - Bounce rate and spam rate by sending domain
    - Bounce rate and spam rate trend over the timeframe (weekly breakdown)
    - Open rate by mailbox (low open rate can signal spam folder placement)
    - Email volume by mailbox
    
    Submit all in parallel, poll with `mcp__claude_ai_Amplemarket__get_analytics_result`.
    
3. **Analyze for problems.** Look for:
    - Mailboxes or domains with elevated spam or bounce rates
    - Mailboxes with unusually low open rates compared to the account average (potential spam folder placement)
    - Trends -- is anything getting worse week over week?
    - Volume concentration -- any mailbox carrying a disproportionate share of sends?
4. **Present a well-formatted health report.** Lead with an overall health summary, then break down by mailbox and domain. Flag anything that needs attention and recommend actions.
    
    If running as a recurring Slack report, format using Slack mrkdwn and post to the configured channel. Only post if there's something worth flagging -- don't spam the channel when everything is healthy.
    

## Examples

**User prompt:** "Check our email deliverability -- anything we should worry about?"

**Simple example output:** The agent finds overall bounce rate is 1.8% (healthy) but one mailbox has a 4.2% spam rate trending up over 3 weeks. Open rate on that mailbox dropped from 45% to 28%. Recommends pausing that mailbox, investigating content/authentication, and redistributing volume. Presented as a health summary table with per-mailbox breakdown and a trend section.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Spam rate data not available | Fall back to bounce rate and open rate as proxy signals. Low open rate + high bounce often correlates with deliverability issues. |