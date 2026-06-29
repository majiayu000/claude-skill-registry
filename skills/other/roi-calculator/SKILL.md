---
name: roi-calculator
description: 'Use when the user asks to "calculate influencer ROI", "prove campaign value", or "what was our ROAS"; produces direct ROI/ROAS, earned media value, attribution-modeled revenue, LTV-based ROI, and a stakeholder-ready summary. Not for building the full slide/written report — use report-generator.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Use when measuring or projecting influencer campaign ROI, justifying or defending budgets, comparing ROI across campaigns or channels, evaluating individual influencer or tier value, or preparing executive-level ROI numbers. Activate when the user supplies spend and results data and wants ROI, ROAS, EMV, CPA/CAC, attribution, or LTV impact computed."
argument-hint: "<campaign name or spend> [revenue] [results data]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Track
---

# ROI Calculator

This skill helps you calculate and communicate the return on investment for influencer marketing campaigns using various methodologies appropriate for your goals and available data.

## Quick Start

Shortest invocation:

```
Calculate ROI for our influencer campaign: $25K spend, $72K revenue, 2.1M reach
```

Common scenario — compare methods before reporting:

```
What's the ROI of our campaign using direct revenue, EMV, and LTV-based methods?
```

## Skill Contract

- **Reads**: campaign spend breakdown, results data (reach, impressions, engagements, clicks, conversions, revenue, new customers), AOV and repeat-rate data if LTV is in scope, any prior performance output from `performance-analyzer`.
- **Writes**: ROI calculation file at `memory/influencer/roi-calculator/YYYY-MM-DD-<topic>.md` containing direct ROI/ROAS, EMV, cost-efficiency metrics, attribution-modeled revenue, LTV-based ROI, by-influencer ROI, and a summary report block.
- **Promotes**: durable headline numbers (final ROI %, ROAS, total investment, net profit, recommended attribution model) to `memory/hot-cache.md`.
- **Done when**:
  1. At least one ROI methodology is computed with the inputs and formula shown.
  2. Each headline metric is stated against a benchmark with a pass/fail status.
  3. A bottom-line assessment (profitable / break-even / loss) and 1-3 recommendations are written.
- **Primary next skill**: [report-generator](../../track/report-generator/SKILL.md)

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family is Tier 1 — it works with no live integrations. Ask the user for spend and results data and compute everything from those inputs. Connectors below can pull the numbers automatically when available:

- `~~social platform analytics` — reach, impressions, engagements, video views per platform for EMV and cost-per-metric math.
- `~~ecommerce / analytics` — revenue, conversions, link clicks, and AOV for direct ROI and attribution.
- `~~CRM` — new-customer counts, repeat-purchase rate, and lifetime value for LTV-based ROI.
- `~~influencer database` — per-influencer fees and tier data for by-influencer ROI.

With zero integrations, supply the investment and results tables by hand and the skill still produces every calculation. See [CONNECTORS.md](../../CONNECTORS.md) for the free/keyless recipe per category.

## Instructions

When a user requests ROI calculation:

1. **Gather ROI Inputs**

   ```markdown
   ### ROI Calculation Inputs
   
   **Campaign Details**:
   - Campaign: [name]
   - Duration: [dates]
   - Objective: [awareness/consideration/conversion]
   
   **Investment (Total Spend)**:
   | Category | Amount |
   |----------|--------|
   | Influencer fees | $[X] |
   | Product/Gifting | $[X] |
   | Production costs | $[X] |
   | Paid amplification | $[X] |
   | Agency/Tools | $[X] |
   | **Total Investment** | **$[X]** |
   
   **Results Data**:
   | Metric | Value |
   |--------|-------|
   | Total Reach | [X] |
   | Total Impressions | [X] |
   | Total Engagements | [X] |
   | Video Views | [X] |
   | Link Clicks | [X] |
   | Conversions/Sales | [X] |
   | Revenue | $[X] |
   | New Customers | [X] |
   ```

2. **Calculate Direct ROI**

   ```markdown
   ## Direct ROI Calculation
   
   ### Simple ROI
   
   **Formula**: (Revenue - Investment) / Investment × 100
   
   ```
   Revenue:     $[X]
   Investment:  $[X]
   Profit:      $[X]
   
   ROI = ($[Revenue] - $[Investment]) / $[Investment] × 100
   ROI = [X]%
   ```
   
   ### Return on Ad Spend (ROAS)
   
   **Formula**: Revenue / Investment
   
   ```
   ROAS = $[Revenue] / $[Investment]
   ROAS = [X]:1
   
   Interpretation: For every $1 spent, generated $[X] in revenue
   ```
   
   ### Direct ROI Summary
   
   | Metric | Value | Benchmark | Status |
   |--------|-------|-----------|--------|
   | ROI % | [X]% | [X]% | ✅/❌ |
   | ROAS | [X]:1 | [X]:1 | ✅/❌ |
   | Profit | $[X] | - | |
   
   **Assessment**: [Profitable/Break-even/Loss]
   ```

3. **Calculate Earned Media Value (EMV)**

   ```markdown
   ## Earned Media Value Calculation
   
   ### EMV Methodology
   
   EMV estimates the equivalent paid media cost to achieve the same results.
   
   ### Impression-Based EMV
   
   **Formula**: Impressions × Industry CPM / 1000
   
   | Platform | Impressions | CPM | EMV |
   |----------|-------------|-----|-----|
   | Instagram | [X] | $[X] | $[X] |
   | TikTok | [X] | $[X] | $[X] |
   | YouTube | [X] | $[X] | $[X] |
   | **Total** | **[X]** | - | **$[X]** |
   
   ### Engagement-Based EMV
   
   **Formula**: Engagements × Cost per Engagement
   
   | Engagement Type | Volume | CPE | EMV |
   |-----------------|--------|-----|-----|
   | Likes | [X] | $[X] | $[X] |
   | Comments | [X] | $[X] | $[X] |
   | Shares | [X] | $[X] | $[X] |
   | Saves | [X] | $[X] | $[X] |
   | Video Views | [X] | $[X] | $[X] |
   | **Total** | - | - | **$[X]** |
   
   ### Combined EMV
   
   | Method | Value |
   |--------|-------|
   | Impression EMV | $[X] |
   | Engagement EMV | $[X] |
   | **Average EMV** | **$[X]** |
   
   ### EMV ROI
   
   ```
   EMV Generated: $[X]
   Investment:    $[X]
   EMV Multiple:  [X]x
   
   For every $1 spent, earned $[X] in equivalent media value
   ```
   
   ### EMV Caveats
   
   ⚠️ **Note**: EMV is an estimate and varies by methodology. Use for directional comparison, not absolute measurement.
   ```

4. **Calculate Cost Efficiency Metrics**

   ```markdown
   ## Cost Efficiency Analysis
   
   ### Cost Per Metrics
   
   | Metric | Formula | Result | Benchmark | Status |
   |--------|---------|--------|-----------|--------|
   | CPM | Spend ÷ (Impressions/1000) | $[X] | $[X] | ✅/❌ |
   | CPR (Reach) | Spend ÷ (Reach/1000) | $[X] | $[X] | ✅/❌ |
   | CPE | Spend ÷ Engagements | $[X] | $[X] | ✅/❌ |
   | CPV (Video) | Spend ÷ Views | $[X] | $[X] | ✅/❌ |
   | CPC | Spend ÷ Clicks | $[X] | $[X] | ✅/❌ |
   | CPA | Spend ÷ Acquisitions | $[X] | $[X] | ✅/❌ |
   | CAC | Total Spend ÷ New Customers | $[X] | $[X] | ✅/❌ |
   
   ### Efficiency Score
   
   | Rating | CPM Range | CPC Range | CPA Range |
   |--------|-----------|-----------|-----------|
   | Excellent | <$[X] | <$[X] | <$[X] |
   | Good | $[X]-$[X] | $[X]-$[X] | $[X]-$[X] |
   | Average | $[X]-$[X] | $[X]-$[X] | $[X]-$[X] |
   | Below Avg | $[X]-$[X] | $[X]-$[X] | $[X]-$[X] |
   | Poor | >$[X] | >$[X] | >$[X] |
   
   **Your Campaign**: [Rating]
   
   ### vs. Other Channels
   
   | Channel | CPA | vs. Influencer |
   |---------|-----|----------------|
   | Influencer Marketing | $[X] | - |
   | Paid Social | $[X] | [+/-X%] |
   | Paid Search | $[X] | [+/-X%] |
   | Display Ads | $[X] | [+/-X%] |
   | Email Marketing | $[X] | [+/-X%] |
   ```

5. **Apply Attribution Modeling**

   ```markdown
   ## Attribution Analysis
   
   ### Attribution Methods
   
   | Method | Description | Result | Notes |
   |--------|-------------|--------|-------|
   | First Touch | All credit to first interaction | $[X] | Awareness focus |
   | Last Touch | All credit to last interaction | $[X] | Conversion focus |
   | Linear | Equal credit across touchpoints | $[X] | Balanced view |
   | Time Decay | More credit to recent touches | $[X] | Recency bias |
   | Position Based | 40/20/40 first/middle/last | $[X] | Common B2C model |
   
   ### Attributed Revenue by Model
   
   | Model | Attributed Revenue | ROI |
   |-------|-------------------|-----|
   | First Touch | $[X] | [X]% |
   | Last Touch | $[X] | [X]% |
   | Linear | $[X] | [X]% |
   | Time Decay | $[X] | [X]% |
   | Position Based | $[X] | [X]% |
   
   ### Recommended Model for Your Business
   
   **Recommended**: [Model]
   **Rationale**: [Why this model fits your customer journey]
   
   ### Multi-Touch Journey Example
   
   ```
   Customer Journey:
   
   Day 1: Sees @creator1 TikTok (Awareness) ─────┐
   Day 3: Sees @creator2 Instagram Reel ─────────┤
   Day 5: Clicks @creator1's link (Consideration)┼── Purchase Day 7
   Day 7: Uses @creator2's code (Conversion) ────┘
   
   Attribution:
   Last Touch:     100% to @creator2
   First Touch:    100% to @creator1
   Linear:         50% each
   Position Based: 40% @creator1, 40% @creator2, 20% repeat exposure
   ```
   ```

6. **Calculate Customer Lifetime Value Impact**

   ```markdown
   ## Lifetime Value Analysis
   
   ### New Customer Metrics
   
   | Metric | Influencer Acquired | Overall Average |
   |--------|--------------------|--------------------|
   | New customers | [X] | - |
   | First order AOV | $[X] | $[X] |
   | Repeat purchase rate | [%] | [%] |
   | Customer lifetime value | $[X] | $[X] |
   
   ### LTV-Based ROI
   
   **Formula**: (New Customers × Avg LTV) - Investment / Investment
   
   ```
   New Customers:     [X]
   Average LTV:       $[X]
   Total LTV:         $[X]
   Investment:        $[X]
   
   LTV-Based ROI = ($[X] - $[X]) / $[X] × 100
   LTV-Based ROI = [X]%
   ```
   
   ### Short-term vs. Long-term View
   
   | Timeframe | Revenue | ROI |
   |-----------|---------|-----|
   | Immediate (this campaign) | $[X] | [X]% |
   | 6-month projected | $[X] | [X]% |
   | 12-month projected | $[X] | [X]% |
   | Lifetime projected | $[X] | [X]% |
   
   ### Customer Quality Indicators
   
   | Indicator | Influencer-Acquired | Organic | Paid Ads |
   |-----------|--------------------|---------| ---------|
   | AOV | $[X] | $[X] | $[X] |
   | Return rate | [%] | [%] | [%] |
   | Repeat rate | [%] | [%] | [%] |
   | NPS/Satisfaction | [X] | [X] | [X] |
   ```

7. **Calculate By-Influencer ROI**

   ```markdown
   ## Influencer-Level ROI
   
   ### Individual Influencer Performance
   
   | Influencer | Investment | Revenue | ROI | ROAS | Rank |
   |------------|------------|---------|-----|------|------|
   | @[handle1] | $[X] | $[X] | [X]% | [X]:1 | 1 |
   | @[handle2] | $[X] | $[X] | [X]% | [X]:1 | 2 |
   | @[handle3] | $[X] | $[X] | [X]% | [X]:1 | 3 |
   | @[handle4] | $[X] | $[X] | [X]% | [X]:1 | 4 |
   | @[handle5] | $[X] | $[X] | [X]% | [X]:1 | 5 |
   
   ### ROI Distribution
   
   ```
   Influencer ROI Distribution:
   
   @handle1  |████████████████████| 320%
   @handle2  |██████████████      | 180%
   @handle3  |████████████        | 150%
   @handle4  |██████              | 75%
   @handle5  |████                | 45%
   
   Campaign Average: 180%
   ```
   
   ### Investment Efficiency
   
   | Influencer | % of Budget | % of Revenue | Efficiency |
   |------------|-------------|--------------|------------|
   | @[handle1] | [%] | [%] | [X]x |
   | @[handle2] | [%] | [%] | [X]x |
   
   ### ROI by Tier
   
   | Tier | Investment | Revenue | ROI | Avg ROAS |
   |------|------------|---------|-----|----------|
   | Macro | $[X] | $[X] | [%] | [X]:1 |
   | Micro | $[X] | $[X] | [%] | [X]:1 |
   | Nano | $[X] | $[X] | [%] | [X]:1 |
   ```

8. **Generate ROI Report Summary**

   ```markdown
   # ROI Summary Report
   
   ## Campaign: [Name]
   ## Period: [Dates]
   
   ---
   
   ## Investment Summary
   
   | Category | Amount | % of Total |
   |----------|--------|------------|
   | Influencer Fees | $[X] | [%] |
   | Product/Gifts | $[X] | [%] |
   | Amplification | $[X] | [%] |
   | Other | $[X] | [%] |
   | **Total Investment** | **$[X]** | **100%** |
   
   ## Returns Summary
   
   | Return Type | Value |
   |-------------|-------|
   | Direct Revenue | $[X] |
   | Earned Media Value | $[X] |
   | New Customers | [X] |
   | Projected LTV | $[X] |
   
   ## ROI by Methodology
   
   | Methodology | ROI | Notes |
   |-------------|-----|-------|
   | Direct Revenue ROI | [X]% | Hard returns |
   | ROAS | [X]:1 | Revenue per dollar |
   | EMV Multiple | [X]x | Media value generated |
   | LTV-Based ROI | [X]% | Long-term value |
   
   ## Key Metrics
   
   | Metric | Result | Benchmark | Status |
   |--------|--------|-----------|--------|
   | CPM | $[X] | $[X] | ✅/❌ |
   | CPA | $[X] | $[X] | ✅/❌ |
   | ROAS | [X]:1 | [X]:1 | ✅/❌ |
   
   ## Bottom Line
   
   **Investment**: $[X]
   **Return**: $[X]
   **Net Profit**: $[X]
   **ROI**: [X]%
   
   **Assessment**: [Campaign was profitable/broke even/lost money]
   
   ## Recommendations
   
   1. [Key recommendation 1]
   2. [Key recommendation 2]
   3. [Key recommendation 3]
   
   ---
   
   *Report Generated: [Date]*
   ```

9. **Roll up into the C³ Campaign Value Index (CVI)**

   This skill emits the **ROI** scope score of [C³](../../references/c3-benchmark.md) and the **CVI** rollup. Score ROI on the **0–100 rubric** in [c3/roi-campaign-benchmark.md](../../references/c3/roi-campaign-benchmark.md) (Return · Orchestration · Impact, each on Pass/Partial/Fail → scaled to 0–100). **This 0–100 ROI score is not the financial ROI % from steps 1–8** — feed the rubric score into the formula, never the percentage (R1 simply *consumes* your ROI%/ROAS as one of its inputs). Then combine it with the Creator and Content scope scores — from [fit-scorer](../../map/fit-scorer/SKILL.md) (ACE) and [content-reviewer](../../activate/content-reviewer/SKILL.md) (ART) — as a geometric mean:

   ```
   CVI = ( ACE_avg × ART_avg × ROI )^(1/3)
   ```

   `ACE_avg` is the **budget-weighted** mean of the campaign's creator ACE scores; `ART_avg` is the simple mean of its content ART scores (per scoring-architecture §8). Keep the three scope scores beside the CVI — the index ranks and alerts, the three scores diagnose. If ACE or ART is unavailable, emit the ROI score and mark CVI **pending (needs ACE/ART)** rather than guessing. A blocked scope (e.g. an ART T1/T2 veto on the content, or an ACE A2/C1/E2 veto on the creator) caps the rollup — surface it, don't average it away.

## Example

**User**: "Calculate ROI for our influencer campaign: $25K spend, $72K revenue, 2.1M reach"

**Output**:

```markdown
# ROI Calculation Summary

## Investment & Returns

| Item | Value |
|------|-------|
| Total Investment | $25,000 |
| Direct Revenue | $72,000 |
| Total Reach | 2,100,000 |

## ROI Results

### Direct ROI
- **Profit**: $47,000
- **ROI**: 188%
- **ROAS**: 2.88:1

For every $1 spent, you generated $2.88 in revenue.

### Earned Media Value
- **EMV** (at $8 CPM): $16,800
- **EMV Multiple**: 0.67x

### Cost Efficiency
- **CPM**: $11.90 (Good)
- **Est. CPA**: ~$54 (if 460 conversions)

## Assessment: ✅ Strong Performance

This campaign outperformed the typical 2:1 ROAS benchmark for influencer marketing. Recommend increasing investment in similar campaigns.
```

## Industry ROI Benchmarks

| Industry | Avg ROAS | Good ROAS | Excellent ROAS |
|----------|----------|-----------|----------------|
| Beauty/Skincare | 3:1 | 5:1 | 8:1 |
| Fashion | 2.5:1 | 4:1 | 6:1 |
| Food & Beverage | 2:1 | 3.5:1 | 5:1 |
| Tech/Electronics | 2:1 | 3:1 | 4:1 |
| Health/Fitness | 2.5:1 | 4:1 | 6:1 |

## Reference Materials

- [skill-contract.md](../../references/skill-contract.md) — shared contract and Handoff Summary format.
- [state-model.md](../../references/state-model.md) — memory tiers and save-path conventions.
- [CONNECTORS.md](../../CONNECTORS.md) — free/keyless data recipe per connector category.
- C³ scoring: [c3-benchmark.md](../../references/c3-benchmark.md) (CVI rollup formula) and [c3/roi-campaign-benchmark.md](../../references/c3/roi-campaign-benchmark.md) — the ROI Campaign rubric this skill emits into the CVI.
- [performance-analyzer](../performance-analyzer/SKILL.md) — supplies the results data this skill consumes.
- [report-generator](../../track/report-generator/SKILL.md) — wraps these numbers into a full report.
- [budget-optimizer](../../plan/budget-optimizer/SKILL.md) — uses ROI output to reallocate spend.
- [campaign-planner](../../plan/campaign-planner/SKILL.md) — sets the ROI targets these results are checked against.

## Next Best Skill

**Primary**: [report-generator](../../track/report-generator/SKILL.md) — turn the ROI numbers into a stakeholder-ready report.

**Alternates** (same Track family):

- [performance-analyzer](../performance-analyzer/SKILL.md) — go back for deeper performance breakdowns if the ROI math exposed gaps.
- [budget-optimizer](../../plan/budget-optimizer/SKILL.md) — feed by-influencer and by-tier ROI into the next budget allocation.

Termination note: keep a visited-set of skills invoked this session. If the primary next skill was already run, stop and report the chain complete rather than re-invoking it. Stop after at most 3 hops in a single chain.
