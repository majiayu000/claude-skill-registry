---
name: sdr-account-prioritization-plan
description: >
  Help SDRs figure out which accounts to focus on and how to break into them -- combining internal engagement data with external signals to prioritize accounts and plan next moves.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Account Intelligence"
compatibility: Requires Amplemarket MCP server
---


# SDR Account Prioritization Plan

Help SDRs figure out which accounts to focus on and how to break into them -- combining internal engagement data with external signals to prioritize accounts and plan next moves.

## Instructions

When an SDR wants to plan their account work, pull account data, enrich with external signals, and build a prioritized penetration plan with specific next steps per account.

### Steps

1. **Identify the SDR's accounts.** Either:
    - Use `mcp__claude_ai_Amplemarket__list_accounts` filtered by the SDR's email to find accounts they own
    - Or ask the SDR for the accounts or domains they want to review
2. **Gather internal data** by calling `mcp__claude_ai_Amplemarket__get_account` for each account. This gives engagement stats, AI-generated insights, and known contacts.
3. **Gather external signals** to identify which accounts have timely reasons to engage now. Use `mcp__claude_ai_Amplemarket__search_companies` or `WebSearch` to check for:
    - Recent funding rounds
    - Leadership changes
    - Hiring surges
    - Product launches or expansions
    - Any other buying signals
4. **Prioritize accounts.** Rank by combining:
    - **Engagement signals** -- which accounts are showing life? Recent opens, replies, interested signals from the AI insights
    - **External signals** -- which accounts have timely triggers that create an opening?
    - **Account fit** -- which accounts are the best ICP match based on firmographics and insights?
    
    The best accounts to focus on are the ones where internal engagement and external signals converge.
    
5. **For each priority account, build a penetration plan:**
    - **What do we know?** -- summarize engagement history and AI insights (interest level, pain points, current solution, competitors)
    - **What don't we know yet?** -- gaps in understanding, unanswered questions, missing information
    - **Who should we go after?** -- check existing contacts via `mcp__claude_ai_Amplemarket__get_contacts` for interaction history, and use `mcp__claude_ai_Amplemarket__search_people` to find new contacts who haven't been reached yet. Consider who's already been contacted, what happened, and who's missing.
    - **What's the angle?** -- based on engagement insights + external signals, what's the best way in?
6. **Help with execution when asked.** If the SDR wants to act:
    - Find contacts at an account via `mcp__claude_ai_Amplemarket__search_people`
    - Enrich a specific person via `mcp__claude_ai_Amplemarket__enrich_person`
    - Create a lead list from discovered contacts via `mcp__claude_ai_Amplemarket__create_lead_list`
7. **Present a well-formatted penetration plan.** Lead with the prioritized account list, then give per-account plans. Keep it action-oriented -- the SDR should finish reading and know exactly who to reach out to and why.

## Examples

**User prompt:** "Help me plan my week -- which accounts should I focus on?"

**Simple example output:** The agent pulls 20 accounts, checks engagement data and external signals. Surfaces 5 priority accounts: 2 with recent positive engagement (warm replies, should follow up), 2 with strong external signals (one just raised Series B, another hired a new VP Sales), and 1 where engagement + external signals converge (interested reply last week AND the company just announced expansion). For each, it shows what we know, who to target, and the recommended angle.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Too many accounts | Prioritize the top 5-10 based on signal strength. Offer to plan the rest in a follow-up. |