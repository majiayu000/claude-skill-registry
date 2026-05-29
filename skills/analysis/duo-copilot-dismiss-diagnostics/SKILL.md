---
name: duo-copilot-dismiss-diagnostics
description: >
  Help admins understand what's driving their Duo dismiss rate by analyzing dismiss patterns across reasons, signals, lead attributes, and rep behavior.
metadata:
  author: amplemarket
  version: "1.0.4"
  category: "Copilot Tools"
compatibility: Requires Amplemarket MCP server
---


# Duo Copilot Dismiss Diagnostics

Help admins understand what's driving their Duo dismiss rate by analyzing dismiss patterns across reasons, signals, lead attributes, and rep behavior.

## Instructions

When an admin wants to diagnose their Duo dismiss rate, query analytics and analyze the results top-down to find the biggest contributors and recommend fixes.

### Steps

1. **Confirm scope.** Default to last 30 days, full account. Ask if the user wants a different timeframe or team scope.
2. **Gather the data** by submitting these analytics questions via `mcp__claude_ai_Amplemarket__ask_analytics`:
    - Overall dismiss rate and lead counts (generated, actioned, dismissed)
    - Dismiss reason breakdown (Bad lead, Bad company, Bad signal, Other)
    - Dismiss rate by signal type and signal name
    - Types of companies being dismissed (sizes, industries, etc.)
    - Profiles of dismissed leads (seniorities, titles, etc.)
    - Dismiss rate by rep
    
    Submit all in parallel, poll with `mcp__claude_ai_Amplemarket__get_analytics_result`.
    
3. **Analyze top-down.** Work through the data in this order:
    1. **Reasons** -- Which dismiss reason dominates?
    2. **Patterns within that reason** -- What's common about the dismissed leads or companies?
    3. **Signal contribution** -- Which signals drive the most dismisses in absolute terms?
    4. **Rep patterns** -- Is it universal or concentrated in a few reps?
4. **Present a well-formatted diagnostic report.** Lead with a summary headline, then use tables and clear sections to walk the admin through the findings. End with specific, actionable recommendations tied to Duo configuration changes.

## Examples

**User prompt:** "Our Duo dismiss rate is at 38%. What's going on?"

**Simple example output:** The agent finds that Bad company is the top dismiss reason (56%), discovers most of those are sub-50-employee companies coming from the Hiring Surge signal, notes rep dismiss rates are uniform (so it's a signal issue, not a rep issue), and recommends excluding small companies from Hiring Surge -- projecting the dismiss rate would drop to ~22%. All presented in a structured report with tables for the reason breakdown, signal contribution, and rep patterns.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Analytics can't break down attributes by dismiss reason | Submit separate queries and cross-reference. |