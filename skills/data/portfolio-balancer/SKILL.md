---
name: portfolio_balancer
description: "Daily Permanent Portfolio analysis with allocation drift and rebalancing recommendations"
---

# portfolio_balancer

**Multi-step workflow**: Daily Permanent Portfolio analysis with allocation drift and rebalancing recommendations

> **CRITICAL**: Always invoke steps using the Skill tool. Never copy/paste step instructions directly.

Automated daily portfolio analysis implementing Harry Browne's Permanent Portfolio strategy.

The Permanent Portfolio maintains equal 25% allocations across four asset classes designed
to perform in different economic conditions:
- Stocks (25%): Prosperity/Growth
- Long-Term Bonds (25%): Deflation/Recession
- Gold (25%): Inflation
- Cash/Treasuries (25%): Tight Money/Recession

This workflow:
1. Collects portfolio data via `bin/robinhood positions --save` CLI
2. Analyzes current allocation against 25/25/25/25 targets
3. Tracks satellite stock picks (optional 10-20% of stock allocation)
4. Evaluates margin usage efficiency vs fees paid
5. Generates rebalancing recommendations when drift exceeds user-defined threshold
6. Produces a human-readable daily report for manual review

IMPORTANT: This system is read-only. No trades are executed automatically.
All recommendations require manual review and execution.


## Available Steps

1. **collect_portfolio_data** - Gather current portfolio positions, values, and prices from Robinhood using bin/robinhood CLI
2. **analyze_allocation** - Calculate current allocation percentages, identify drift from targets, analyze margin efficiency (requires: collect_portfolio_data)
3. **generate_recommendations** - Create specific rebalancing recommendations based on drift analysis (requires: analyze_allocation)
4. **generate_report** - Compile comprehensive human-readable daily report with all analysis and recommendations (requires: collect_portfolio_data, analyze_allocation, generate_recommendations)

## Execution Instructions

### Step 1: Analyze Intent

Parse any text following `/portfolio_balancer` to determine user intent:
- "collect_portfolio_data" or related terms → start at `portfolio_balancer.collect_portfolio_data`
- "analyze_allocation" or related terms → start at `portfolio_balancer.analyze_allocation`
- "generate_recommendations" or related terms → start at `portfolio_balancer.generate_recommendations`
- "generate_report" or related terms → start at `portfolio_balancer.generate_report`

### Step 2: Invoke Starting Step

Use the Skill tool to invoke the identified starting step:
```
Skill tool: portfolio_balancer.collect_portfolio_data
```

### Step 3: Continue Workflow Automatically

After each step completes:
1. Check if there's a next step in the sequence
2. Invoke the next step using the Skill tool
3. Repeat until workflow is complete or user intervenes

### Handling Ambiguous Intent

If user intent is unclear, use AskUserQuestion to clarify:
- Present available steps as numbered options
- Let user select the starting point

## Guardrails

- Do NOT copy/paste step instructions directly; always use the Skill tool to invoke steps
- Do NOT skip steps in the workflow unless the user explicitly requests it
- Do NOT proceed to the next step if the current step's outputs are incomplete
- Do NOT make assumptions about user intent; ask for clarification when ambiguous

## Context Files

- Job definition: `.deepwork/jobs/portfolio_balancer/job.yml`