---
name: scenario-model
description: Build strategic what-if scenarios for executive decision-making
user-invocable: true
---

You are helping executive leadership build strategic scenarios for decision-making.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_consolidated_kpis`).

Follow these steps:

### Step 1: Define Strategic Question

Ask the user what strategic question they want to model:
- **Growth strategy** — "What if we enter a new channel?"
- **Pricing strategy** — "What if we raise/lower prices?"
- **M&A impact** — "What does the acquisition look like at different multiples?"
- **Market scenario** — "What if the market contracts 15%?"
- **Investment decision** — "What's the ROI on this initiative?"

### Step 2: Establish Baseline

Pull current data as the baseline:
- `mcp__snowflake__get_consolidated_kpis` — current KPIs
- `mcp__snowflake__get_pnl_summary` — current P&L
- `mcp__snowflake__get_channel_revenue` — current channel mix

Present the baseline to the user.

### Step 3: Build Scenarios

Delegate to the `financial-modeler` agent to build scenarios. Typically model 3 cases:
- **Bear case** — conservative assumptions
- **Base case** — most likely outcome
- **Bull case** — optimistic assumptions

For each scenario, project:
- Revenue impact (1-year and 3-year)
- Margin impact
- Cash flow implications
- Key risk factors

### Step 4: Evaluate and Compare

Use the `risk-assessor` agent to evaluate downside risks for each scenario.

Present a comparison:
- Side-by-side financial metrics across scenarios
- Risk-adjusted expected values
- Key decision criteria
- Sensitivity analysis — which assumptions drive the most variance

### Step 5: Recommendation

Synthesize the analysis into a recommendation:
- Which scenario or strategy is preferred and why
- Key assumptions that need validation
- Suggested next steps to de-risk

### Step 6: Follow-Up

Offer:
- **Refine scenarios** with adjusted assumptions
- **Build a deck** — `/jf-executive-suite:build-deck` with scenario analysis
- **Investor metrics** — `/jf-executive-suite:investor-metrics`

### Error Handling

- If Snowflake MCP is unavailable, build scenario frameworks with user-provided assumptions
- If baseline data is incomplete, note assumptions that must be manually provided
