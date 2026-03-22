---
name: scenario-analyzer
description: Analyze news headlines, policy announcements, or geopolitical events to build 18-month probabilistic scenarios for Indian markets. Use when the user provides a headline or asks about the market impact of RBI policy, government announcements, global events, budget, or sector-specific news on NSE/BSE stocks.
---

# Scenario Analyzer (India Markets)

## Overview

This skill takes a news headline or event and builds probabilistic 18-month scenarios with cascading 1st, 2nd, and 3rd order sector impacts and specific stock recommendations for the Indian market.

## Architecture

```
Skill (Orchestrator)
├── Phase 1: Preparation
│   ├── Headline parsing (keywords, entities, actions, numbers)
│   ├── Event classification
│   └── Load references
├── Phase 2: Analysis
│   ├── Collect related news (past 2 weeks via WebSearch)
│   ├── Build 3 scenarios (Base/Bull/Bear, probabilities sum to 100%)
│   ├── Map 1°/2°/3° sector impacts
│   └── Identify 3-5 positive + 3-5 negative impact stocks
└── Phase 3: Report Generation
    ├── Compile findings
    ├── Assess scenario probability distribution
    └── Save report
```

## Event Classification

Classify the headline into one of these categories:

| Category | Indian Context Examples |
|----------|----------------------|
| **Monetary Policy** | RBI rate decision, CRR/SLR change, liquidity measures |
| **Fiscal Policy** | Union Budget, GST changes, PLI schemes, disinvestment |
| **Geopolitical** | India-China border, India-Pakistan, Russia-Ukraine, Middle East |
| **Commodity** | Crude oil shock, gold prices, metal tariffs, food inflation |
| **Regulatory** | SEBI rules, RBI NPA norms, telecom spectrum, pharma FDA |
| **Corporate** | Major M&A, earnings surprise, promoter pledging, fraud |
| **Global Macro** | Fed rate decision, US recession, China slowdown, tariffs |
| **Weather/Agriculture** | Monsoon forecast, crop damage, food prices |
| **Elections/Political** | State elections, central govt policy shifts |

## Workflow

### Phase 1: Preparation

1. **Parse the Headline**
   - Extract key entities (companies, sectors, countries, institutions)
   - Identify the action (increase, decrease, ban, approve, delay)
   - Note any numbers (rate changes, ₹ amounts, percentages)
   - Classify the event type

2. **Load References**
   ```
   Read: references/headline_event_patterns.md
   Read: references/sector_sensitivity_matrix.md
   Read: references/scenario_playbooks.md
   ```

### Phase 2: Analysis

3. **Collect Context**
   - Use WebSearch to find related news from the past 2 weeks
   - Identify any pre-existing trends or expectations
   - Note market's initial reaction if available

4. **Build 3 Scenarios**

   For each scenario:
   - **Name**: Descriptive title
   - **Probability**: Must sum to 100% across all 3
   - **Timeline**: 3 phases (0-6 months, 6-12 months, 12-18 months)
   - **Description**: What unfolds in each phase
   - **Key Assumptions**: What must hold true

   Typical structure:
   - **Base Case (40-55%)**: Most likely outcome given current trajectory
   - **Bull Case (20-35%)**: Optimistic scenario with positive catalysts
   - **Bear Case (15-30%)**: Pessimistic scenario with adverse developments

5. **Map Sector Impacts**

   For each scenario, assess impacts using the sector sensitivity matrix:

   | Order | Definition | Example (RBI Rate Cut) |
   |-------|-----------|----------------------|
   | 1st | Direct, immediate | Banks: NIM compression, Housing: demand boost |
   | 2nd | Indirect, 3-6 months | Auto: loan demand, Real estate: prices |
   | 3rd | Tertiary, 6-18 months | Cement: construction demand, Durables: consumer spending |

   Use NSE sectoral indices:
   - Nifty Bank, Nifty IT, Nifty Pharma, Nifty Auto, Nifty FMCG
   - Nifty Metal, Nifty Realty, Nifty Energy, Nifty Infra
   - Nifty PSU Bank, Nifty Private Bank, Nifty Financial Services

6. **Identify Stock Impacts**

   For each scenario:
   - 3-5 stocks that benefit most (positive impact)
   - 3-5 stocks that suffer most (negative impact)

   For each stock, provide:
   - Ticker (NSE symbol)
   - Current price (use broker MCP `get_ltp` — Groww or Zerodha Kite — if available)
   - Impact channel (why this stock is affected)
   - Magnitude estimate (High/Medium/Low)

### Phase 3: Report Generation

7. **Generate Report**

   Save as `reports/scenario_analysis_<topic>_YYYYMMDD.md` with sections:

   1. **Related News** (5-10 recent articles with sources)
   2. **Scenario Overview** (3 scenarios with probabilities)
   3. **Timeline** (0-6m, 6-12m, 12-18m phases for base case)
   4. **Sector Impact Matrix** (1°/2°/3° impacts per sector)
   5. **Positive Impact Stocks** (3-5 with rationale)
   6. **Negative Impact Stocks** (3-5 with rationale)
   7. **Investment Implications** (actionable takeaways)
   8. **Risk to Scenarios** (what could shift probabilities)
   9. **Disclaimer**

## Quality Standards

- All probabilities must sum to 100%
- Every impact claim must have a causal chain (event → mechanism → impact)
- Stock picks must include the impact channel, not just "will benefit"
- Consider second-order effects (e.g., rate cut → weak INR → IT sector benefit)
- Flag any confirmation bias in scenario construction
- Include both sectors that benefit AND those that lose

## Example Usage

```
User: "RBI cuts repo rate by 25 bps to 6%"

Analyst:
1. Classification: Monetary Policy
2. Key entities: RBI, repo rate, 25 bps, 6%
3. Collects recent RBI commentary and market expectations
4. Scenarios:
   - Base (50%): One more cut expected → banks pass on, housing demand rises
   - Bull (30%): Cycle of 75-100 bps cuts → strong credit growth, equity rally
   - Bear (20%): Global inflation returns → RBI pauses → rate-sensitive sell-off
5. 1° impacts: Banks, NBFCs, Housing Finance, Auto
6. 2° impacts: Real Estate, Consumer Durables
7. 3° impacts: Cement, Infrastructure
8. Stock picks: HDFCBANK, BAJFINANCE, GODREJPROP (positive); IT exporters if INR weakens
```

## Resources

### references/headline_event_patterns.md
Historical Indian market event patterns and reactions.

### references/sector_sensitivity_matrix.md
Event type × NSE sector impact matrix.

### references/scenario_playbooks.md
Scenario construction templates with Indian market context.
