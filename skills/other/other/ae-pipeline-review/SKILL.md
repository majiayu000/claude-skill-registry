---
name: ae-pipeline-review
description: >
  Help AEs get a status check on their accounts with open deals -- where things stand, where to focus, and what next steps to take.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Account Intelligence"
compatibility: Requires Amplemarket MCP server
---


# AE Pipeline Review

Help AEs get a status check on their accounts with open deals -- where things stand, where to focus, and what next steps to take.

## Instructions

When an AE wants to review their accounts or deals, pull account data, engagement history, and AI insights to assess each account and recommend next steps.

### Steps

1. **Identify the AE's accounts.** Either:
    - Use `mcp__claude_ai_Amplemarket__list_accounts` filtered by the AE's email to find accounts they own
    - Filter for accounts with open opportunities if possible
    - Or ask the AE for the specific accounts or domains they want reviewed
2. **Gather account data** by calling `mcp__claude_ai_Amplemarket__get_account` for each account. This gives engagement stats, AI-generated insights (interest level, current solution, competitors, pain points, champions, decision makers, gatekeepers, timelines), CRM data, and contacts.
3. **Assess each account.** For each, evaluate:
    - Deal momentum -- is engagement progressing or stalled?
    - Stakeholder coverage -- are champions, decision makers, and economic buyers identified? Is the deal single-threaded?
    - Risks -- gone cold, competitor mentioned, champion left, missing key roles?
    - Next steps -- what should the AE do next?
4. **Help with next steps when asked.** If the AE wants to act on a specific account:
    - `mcp__claude_ai_Amplemarket__search_people` to find additional stakeholders for multi-threading
    - `mcp__claude_ai_Amplemarket__get_contacts` to check status on specific contacts
    - `mcp__claude_ai_Amplemarket__enrich_person` for deeper context on a key stakeholder
5. **Present a well-formatted account review.** Prioritize by urgency -- which accounts need action now vs progressing fine. For each, show current state, key people, and recommended next step.

## Examples

**User prompt:** "Give me a status on my deals"

**Simple example output:** The agent pulls the AE's accounts, finds 3 needing immediate attention (one stalled in negotiation for 2 weeks, one single-threaded with only a junior contact, one where the champion seems to be going cold). 6 are progressing normally. Presented as a prioritized list with per-account summary and next steps.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Too many accounts | Focus on accounts with open opportunities or recent engagement first. Offer to review the rest separately. |