---
name: build-deck
description: Generate executive presentation deck content from business data
user-invocable: true
---

You are helping executive leadership build presentation deck content.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+snowflake` to load the snowflake MCP tools. All tools below are prefixed with `mcp__snowflake__` (e.g., `mcp__snowflake__get_consolidated_kpis`).

Follow these steps:

### Step 1: Define the Deck

Ask the user:
- **Audience**: Board, investors, leadership team, department heads?
- **Focus**: Full business review, specific topic, or quarterly update?
- **Key message**: What's the one thing you want the audience to take away?
- **Length**: How many slides / how much detail?

### Step 2: Gather Data

Pull relevant data based on the deck focus:
- `mcp__snowflake__get_consolidated_kpis` — overall KPIs
- `mcp__snowflake__get_pnl_summary` — financial performance
- `mcp__snowflake__get_channel_revenue` — channel breakdown
- `mcp__snowflake__get_unit_economics` — unit economics

### Step 3: Build Slide Content

Generate structured content for each slide. Use the `narrative-builder` agent for executive-quality prose.

**Typical slide structure:**
1. **Title slide** — meeting title, date, confidentiality
2. **Executive summary** — 3-5 bullet headline
3. **Revenue performance** — total, by channel, growth rates
4. **Profitability** — margin trends, cost structure
5. **Operational metrics** — fulfillment, inventory
6. **Strategic priorities** — key initiatives and progress
7. **Risks and opportunities** — what needs attention
8. **Next steps / asks** — decisions needed

For each slide, provide:
- Slide title
- Key data points / metrics
- Narrative text (1-3 sentences)
- Suggested visualization type (chart, table, callout)

### Step 4: Review and Refine

Present the deck outline and ask the user:
- Any slides to add, remove, or reorder?
- Any data points to emphasize or de-emphasize?
- Tone adjustments (more optimistic, more cautious, etc.)?

### Step 5: Follow-Up

Offer:
- **Refine specific slides** with more data
- **Executive summary** — `/jf-executive-suite:executive-summary`
- **Investor metrics** — `/jf-executive-suite:investor-metrics`

### Error Handling

- If Snowflake MCP is unavailable, build the deck structure with placeholder data points and note what needs to be filled in
- If specific data is incomplete, note gaps and suggest manual data entry
