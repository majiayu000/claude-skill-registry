---
name: new-rep-ramp-tracker
description: >
  Track a new rep's ramp progress against team benchmarks at the same tenure, helping managers spot early if someone is ahead, on track, or falling behind.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Team & Coaching"
compatibility: Requires Amplemarket MCP server
---


# New Rep Ramp Tracker

Track a new rep's ramp progress against team benchmarks at the same tenure, helping managers spot early if someone is ahead, on track, or falling behind.

## Instructions

When a manager wants to check how a new rep is ramping, query analytics for the rep's performance since their start date and compare to what the team typically looks like at the same stage.

### Steps

1. **Identify the rep and their start date.** The user will name a rep. Ask when they started if not provided -- this is essential to scope the data and pick the right comparison window (30/60/90 days).
2. **Gather the data** by submitting these analytics questions via `mcp__claude_ai_Amplemarket__ask_analytics`:
    - Rep's outreach volume by week since start date
    - Rep's reply rate and interested rate since start date
    - Rep's meetings booked since start date
    - Rep's Duo leads actioned and dismiss rate since start date (if Duo is enabled)
    - Team average for the same metrics at the same tenure (e.g., "What was the team's average email volume in their first 60 days?")
    
    Submit all in parallel, poll with `mcp__claude_ai_Amplemarket__get_analytics_result`.
    
3. **Analyze the ramp trajectory.** Look for:
    - Is activity ramping week over week or flat?
    - How does engagement quality compare to team average at this stage?
    - Time to first meeting -- how long did it take vs team average?
    - Any early warning signs (declining activity, high dismiss rate, low engagement)?
4. **Present a well-formatted ramp report.** Show the rep's trajectory with weekly progression, comparison to team benchmarks, and a clear assessment: ahead, on track, or needs attention. Include specific recommendations if the rep is falling behind.

## Examples

**User prompt:** "How is Sarah ramping? She started 6 weeks ago."

**Simple example output:** The agent finds Sarah's weekly email volume has been steadily increasing (45 → 78 → 95 → 110 → 125 → 140), ahead of the team's typical ramp at 6 weeks (avg 105). Her reply rate is slightly below team average at this stage (3.2% vs 4.1%) but trending up. She booked her first meeting in week 4 (team average: week 3). Assessment: activity ramp is strong, engagement quality needs a bit more time. Presented as a weekly progression table with team benchmarks alongside.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Team benchmark data for "same tenure" not available | Compare to team's current averages instead, noting the rep is new and expected to be below average. |