---
name: rep-coaching-brief
description: >
  Generate coaching notes for a manager preparing a 1:1 with a rep, covering activity, engagement quality, conversion efficiency, and areas for improvement.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Team & Coaching"
compatibility: Requires Amplemarket MCP server
---


# Rep Coaching Brief

Generate coaching notes for a manager preparing a 1:1 with a rep, covering activity, engagement quality, conversion efficiency, and areas for improvement.

## Instructions

When a manager wants coaching notes on a specific rep, query analytics for that rep's performance across key metrics, compare to team averages, and present a structured brief for the 1:1.

### Steps

1. **Identify the rep and scope.** The user will name a rep or provide their email. Default to last 30 days. Ask if they want a different timeframe.
2. **Gather the data** by submitting these analytics questions via `mcp__claude_ai_Amplemarket__ask_analytics`:
    - Rep's outreach volume across all channels (email, LinkedIn, calls)
    - Rep's reply rate, open rate, interested rate
    - Rep's meetings booked
    - Rep's bounce rate
    - Rep's Duo leads actioned and dismiss rate (if Duo is enabled)
    - Rep's top sequences by reply rate
    - Rep's worst sequences by reply rate
    - Team averages for the same metrics (for comparison)
    
    Submit all in parallel, poll with `mcp__claude_ai_Amplemarket__get_analytics_result`.
    
3. **Analyze relative to the team.** For each metric, compare the rep to the team average. Identify:
    - Where they're above average (strengths to reinforce)
    - Where they're below average (areas for coaching)
    - Any notable patterns (e.g., high volume but low reply rate = messaging issue, low volume but high reply rate = capacity opportunity)
4. **Present a well-formatted coaching brief.** Lead with a quick summary of the rep's standing, then break down strengths, areas for improvement, and specific talking points for the 1:1. Include the data backing each point.

## Examples

**User prompt:** "Give me coaching notes for David Kim ahead of our 1:1"

**Simple example output:** The agent finds David's email volume is 15% below team average, but his reply rate is 2x the average. Meetings booked are average. His top sequence outperforms the team's best. Recommends the coaching focus on increasing David's volume since his engagement quality is excellent -- more sends at his reply rate would likely mean more meetings. Presented as a brief with a strengths section, improvement areas section, and suggested 1:1 talking points.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Rep name is ambiguous | Ask for the rep's email to match exactly in analytics queries. |