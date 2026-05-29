---
name: knowledge-gap
description: Analyze help center for coverage gaps by comparing support tickets to existing articles
user-invocable: true
---

You are helping the customer experience team identify missing help center articles by analyzing support ticket patterns.

Follow these steps:

### Step 1: Gather Current Articles

Delegate to the `help-center-architect` agent to inventory all existing help center articles. Collect:
- Article titles and categories
- Topics covered by each article
- Last updated dates

If the user can provide a URL to the help center or an export, use that as the source.

### Step 2: Analyze Support Tickets

Delegate to the `knowledge-gap-analyzer` agent to analyze recent support tickets from Gorgias. Look for:
- Most common ticket categories by volume
- Recurring questions and themes
- Topics where agents repeatedly write similar responses
- Questions that could be resolved with self-service documentation

### Step 3: Identify Gaps

Cross-reference ticket themes against existing articles:
- **Missing coverage**: High-volume topics with no article
- **Outdated coverage**: Articles that exist but no longer match current products/policies
- **Thin coverage**: Topics with articles that don't fully answer customer questions

Rank gaps by:
1. Ticket volume (highest impact first)
2. Complexity of agent response (longer responses = bigger self-service opportunity)
3. Customer frustration signals

### Step 4: Recommend New Articles

For each gap, provide:
- Recommended article title
- Target category in the help center
- Outline of key sections to cover
- Estimated ticket deflection impact (high/medium/low)

Present results as a prioritized table.

### Error Handling

- If Gorgias data is unavailable, ask the user for a ticket export or recent support themes
- If the help center has no existing articles, skip Step 1 and focus on building from scratch
- If ticket volume is too low for patterns, suggest a minimum data window (e.g., 90 days)
