---
name: budget-optimizer
description: 'Use when the user asks to "allocate my influencer budget", "optimize spend across tiers", or "compare budget scenarios"; produces a tier/platform/content allocation table, ROI and CPM/CPE projections, scenario comparisons, and mid-campaign reallocation moves. Not for building the full campaign plan — use campaign-planner.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Use when planning budget allocation for a new influencer campaign, splitting spend across nano/micro/macro tiers or platforms, estimating influencer costs and projecting ROI, modeling conservative vs aggressive scenarios, justifying a budget request, or reallocating budget mid-campaign based on performance."
argument-hint: "<total budget> [platforms] [campaign goal]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Plan
---

# Budget Optimizer

This skill helps you allocate and optimize your influencer marketing budget to maximize return on investment. It considers platform costs, influencer tier economics, and campaign objectives to recommend optimal budget distribution.

## Quick Start

Shortest invocation:

```
Help me allocate a $30,000 budget for an influencer campaign on Instagram and TikTok
```

Common scenario:

```
Optimize my influencer budget across micro and macro influencers for a Gen Z product launch — compare a $50K and a $100K scenario
```

Output: a tier/platform/content allocation table, projected reach + CPM/CPE, 2-3 budget scenarios, and a recommended split.

## Skill Contract

- **Reads**: total budget, fixed vs influencer-available split, campaign goal, target platforms, tier constraints (max per influencer, minimum count), industry, and — for mid-campaign work — spend-to-date and per-influencer results. Connector data via `~~influencer database` / `~~social platform analytics` when available.
- **Writes**: a budget allocation recommendation (tier / platform / content tables), ROI and cost-efficiency projections, scenario comparison, optimization strategies, plus a handoff summary. Save path: `memory/influencer/budget-optimizer/YYYY-MM-DD-<topic>.md`.
- **Promotes**: approved total budget, the chosen scenario, locked tier mix, and any spend constraints — promote durable facts to `memory/hot-cache.md`.
- **Done when**:
  1. Allocation sums to 100% of the stated budget with a contingency line.
  2. Every projected metric is labeled Measured / User-provided / Estimated.
  3. One recommended scenario is named with its rationale.
- **Primary next skill**: [outreach-manager](../../activate/outreach-manager/SKILL.md) — turn the funded allocation into influencer outreach.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family has no required live integrations (Tier 1). The skill works with nothing but the numbers you provide — give it your total budget, target platforms, and campaign goal, and it runs against the built-in cost benchmarks below.

Optional connectors that sharpen the estimates when present:

- `~~influencer database` — real rate cards instead of benchmark ranges.
- `~~social platform analytics` — actual reach, CPM, and engagement to replace estimated projections.
- `~~CRM` — past campaign spend and conversion data for ROI calibration.

Mark any connector-derived number Measured; mark benchmark-derived numbers Estimated; mark numbers you state as User-provided. See [CONNECTORS.md](../../CONNECTORS.md) for the keyless data recipes.

## Instructions

When a user requests budget optimization:

1. **Gather Budget Parameters**

   ```markdown
   ### Budget Optimization Parameters
   
   **Campaign Details**:
   - Campaign Goal: [awareness/engagement/conversion]
   - Target Audience: [description]
   - Timeline: [duration]
   - Geographic Focus: [regions]
   
   **Budget Information**:
   - Total Budget: $[X]
   - Fixed Costs: $[X] (agency, tools, etc.)
   - Available for Influencers: $[X]
   
   **Platform Priorities**:
   - Primary: [platform]
   - Secondary: [platform(s)]
   
   **Constraints**:
   - Must include: [requirements]
   - Maximum per influencer: $[X]
   - Minimum influencers: [#]
   ```

2. **Analyze Cost Benchmarks**

   ```markdown
   ## Cost Benchmarks
   
   ### Influencer Cost by Tier & Platform
   
   #### Instagram
   
   | Tier | Followers | Cost/Post | Cost/Story | Cost/Reel |
   |------|-----------|-----------|------------|-----------|
   | Nano | 1K-10K | $50-250 | $25-100 | $75-300 |
   | Micro | 10K-100K | $250-1,000 | $100-500 | $300-1,500 |
   | Mid-tier | 100K-500K | $1,000-5,000 | $500-2,000 | $1,500-7,500 |
   | Macro | 500K-1M | $5,000-10,000 | $2,000-5,000 | $7,500-15,000 |
   | Mega | 1M+ | $10,000+ | $5,000+ | $15,000+ |
   
   #### TikTok
   
   | Tier | Followers | Cost/Video | Notes |
   |------|-----------|------------|-------|
   | Nano | 1K-10K | $50-200 | High engagement typical |
   | Micro | 10K-100K | $200-1,000 | Sweet spot for many brands |
   | Mid-tier | 100K-500K | $1,000-3,000 | Viral potential |
   | Macro | 500K-1M | $3,000-7,500 | Established creators |
   | Mega | 1M+ | $7,500+ | Celebrity tier |
   
   #### YouTube
   
   | Tier | Subscribers | Dedicated Video | Integration | Mention |
   |------|-------------|-----------------|-------------|---------|
   | Micro | 10K-100K | $1,000-5,000 | $500-2,000 | $200-500 |
   | Mid-tier | 100K-500K | $5,000-15,000 | $2,000-7,500 | $500-2,000 |
   | Macro | 500K-1M | $15,000-30,000 | $7,500-15,000 | $2,000-5,000 |
   | Mega | 1M+ | $30,000+ | $15,000+ | $5,000+ |
   
   ### Industry Adjustments
   
   | Industry | Cost Multiplier | Notes |
   |----------|-----------------|-------|
   | Beauty/Fashion | 1.2-1.5x | High demand, competitive |
   | Tech | 1.1-1.3x | Specialized expertise |
   | Food/Beverage | 1.0x | Standard rates |
   | Finance | 1.3-1.5x | Compliance requirements |
   | Health/Wellness | 1.2-1.4x | Trust requirements |
   | Gaming | 0.9-1.1x | Platform dependent |
   | Travel | 1.0-1.2x | Seasonal variations |
   | Parenting | 1.0-1.1x | Engaged audiences |
   ```

3. **Create Budget Allocation**

   ```markdown
   ## Budget Allocation Recommendation
   
   ### Total Budget: $[X]
   
   ### Recommended Allocation
   
   #### By Influencer Tier
   
   | Tier | % Budget | Amount | # Influencers | Cost/Influencer |
   |------|----------|--------|---------------|-----------------|
   | Macro | [%] | $[X] | [#] | ~$[X] |
   | Micro | [%] | $[X] | [#] | ~$[X] |
   | Nano | [%] | $[X] | [#] | ~$[X] |
   | **Total** | **100%** | **$[X]** | **[#]** | |
   
   **Rationale**: [Why this tier mix for this campaign goal]
   
   #### By Platform
   
   | Platform | % Budget | Amount | Rationale |
   |----------|----------|--------|-----------|
   | [Platform 1] | [%] | $[X] | [why] |
   | [Platform 2] | [%] | $[X] | [why] |
   | [Platform 3] | [%] | $[X] | [why] |
   
   #### By Content Type
   
   | Content Type | % Budget | Amount | Quantity |
   |--------------|----------|--------|----------|
   | [Type 1] | [%] | $[X] | [#] pieces |
   | [Type 2] | [%] | $[X] | [#] pieces |
   
   #### Other Budget Items
   
   | Item | Amount | % of Total | Notes |
   |------|--------|------------|-------|
   | Product/Gifting | $[X] | [%] | [notes] |
   | Content Amplification | $[X] | [%] | Boosting top content |
   | Tools/Software | $[X] | [%] | [tools] |
   | Contingency | $[X] | [%] | 5-10% buffer |
   ```

4. **Project ROI**

   ```markdown
   ## ROI Projections
   
   ### Expected Results
   
   | Metric | Projection | Methodology |
   |--------|------------|-------------|
   | Total Reach | [X] | [calculation] |
   | Impressions | [X] | Reach × [frequency] |
   | Engagements | [X] | Reach × [ER%] |
   | Video Views | [X] | [if applicable] |
   | Link Clicks | [X] | [click rate] |
   | EMV | $[X] | Impressions × CPM |
   
   ### Cost Efficiency Metrics
   
   | Metric | Projected | Industry Avg | vs. Avg |
   |--------|-----------|--------------|---------|
   | CPM | $[X] | $[Y] | [better/worse] |
   | CPE | $[X] | $[Y] | [better/worse] |
   | Cost per Video View | $[X] | $[Y] | [better/worse] |
   | Cost per Click | $[X] | $[Y] | [better/worse] |
   
   ### ROI Calculation
   
   **Investment**: $[X]
   **Expected Value**: $[X] (EMV + direct value)
   **Projected ROI**: [X]:1
   
   ### Conversion Projections (if applicable)
   
   | Stage | Number | Rate | Notes |
   |-------|--------|------|-------|
   | Reach | [X] | - | Starting point |
   | Clicks | [X] | [%] | Click-through rate |
   | Site Visits | [X] | [%] | Bounce considered |
   | Conversions | [X] | [%] | Conversion rate |
   | Revenue | $[X] | [AOV] | Average order value |
   | **ROAS** | **[X]:1** | | Return on ad spend |
   ```

5. **Model Scenarios**

   ```markdown
   ## Budget Scenarios
   
   ### Scenario Comparison
   
   | Factor | Conservative | Recommended | Aggressive |
   |--------|--------------|-------------|------------|
   | **Budget** | $[X] | $[Y] | $[Z] |
   | # Influencers | [#] | [#] | [#] |
   | Tier Mix | [mix] | [mix] | [mix] |
   | Est. Reach | [X] | [X] | [X] |
   | Est. Engagements | [X] | [X] | [X] |
   | Projected CPM | $[X] | $[X] | $[X] |
   | Projected ROI | [X]:1 | [X]:1 | [X]:1 |
   | Risk Level | Low | Medium | Higher |
   
   ### Scenario A: Conservative ($[X])
   
   **Strategy**: Focus on proven micro-influencers with high engagement
   
   | Tier | # | Budget | Content |
   |------|---|--------|---------|
   | Micro | [#] | $[X] | [#] posts |
   | Nano | [#] | $[X] | [#] posts |
   
   **Pros**:
   - Lower risk
   - Higher engagement rates
   - More content pieces
   
   **Cons**:
   - Limited reach
   - Less brand awareness impact
   - Slower momentum
   
   ---
   
   ### Scenario B: Recommended ($[Y])
   
   **Strategy**: Balanced mix with macro anchor and micro support
   
   | Tier | # | Budget | Content |
   |------|---|--------|---------|
   | Macro | [#] | $[X] | [#] posts |
   | Micro | [#] | $[X] | [#] posts |
   | Nano | [#] | $[X] | [#] posts |
   
   **Pros**:
   - Balanced reach and engagement
   - Credibility from macro names
   - Volume from micro/nano
   
   **Cons**:
   - More complex management
   - Medium budget commitment
   
   ---
   
   ### Scenario C: Aggressive ($[Z])
   
   **Strategy**: Macro-heavy with celebrity/mega-influencer
   
   | Tier | # | Budget | Content |
   |------|---|--------|---------|
   | Mega | [#] | $[X] | [#] posts |
   | Macro | [#] | $[X] | [#] posts |
   | Micro | [#] | $[X] | [#] posts |
   
   **Pros**:
   - Maximum reach
   - Strong brand association
   - Potential viral moments
   
   **Cons**:
   - Higher cost per engagement
   - Concentration risk
   - Less authentic feel
   
   ---
   
   ### Recommendation
   
   **Recommended Scenario**: [Scenario X]
   
   **Rationale**: [Why this scenario best meets campaign goals]
   ```

6. **Provide Optimization Tips**

   ```markdown
   ## Budget Optimization Strategies
   
   ### Cost Reduction Strategies
   
   | Strategy | Potential Savings | Trade-offs |
   |----------|-------------------|------------|
   | Negotiate multi-post deals | 15-25% | Commitment required |
   | Product-only compensation | 50-80% | Limited to nano/small micro |
   | Affiliate-heavy model | Variable | Performance-dependent |
   | Long-term ambassadors | 20-30% | Less variety |
   | Emerging influencers | 40-60% | Less proven |
   | Off-peak timing | 10-20% | Less competitive periods |
   
   ### Value Maximization Strategies
   
   1. **Bundle deliverables**: Negotiate package deals
      - Example: "Post + Stories + Reel" vs. separate pricing
      - Typical savings: 15-20%
   
   2. **Usage rights negotiation**: Get more rights for budget
      - Include: Whitelisting, repurposing rights
      - Value add without major cost increase
   
   3. **Performance incentives**: Align interests
      - Base fee + performance bonus
      - Motivates quality content
   
   4. **Content amplification**: Boost top performers
      - Allocate 10-20% for paid amplification
      - Extend reach of best content
   
   5. **UGC rights**: Maximize content value
      - Negotiate perpetual rights
      - Repurpose across channels
   
   ### Budget Red Flags
   
   ⚠️ **Warning Signs**:
   - >40% of budget on single influencer
   - CPM significantly above industry average
   - No contingency allocated
   - All budget on unproven creators
   - Ignoring content amplification
   ```

7. **Mid-Campaign Optimization**

   ```markdown
   ## Mid-Campaign Budget Reallocation
   
   ### Current Performance vs. Plan
   
   | Metric | Planned | Actual | Variance | Action |
   |--------|---------|--------|----------|--------|
   | Spend to Date | $[X] | $[X] | [%] | [action] |
   | Content Live | [#] | [#] | [%] | [action] |
   | Reach | [X] | [X] | [%] | [action] |
   | Engagement | [X] | [X] | [%] | [action] |
   | CPM | $[X] | $[X] | [%] | [action] |
   
   ### Top Performers
   
   | Influencer | Spend | Results | ROI | Recommendation |
   |------------|-------|---------|-----|----------------|
   | @[handle1] | $[X] | [results] | [X]:1 | Increase investment |
   | @[handle2] | $[X] | [results] | [X]:1 | Increase investment |
   
   ### Underperformers
   
   | Influencer | Spend | Results | ROI | Recommendation |
   |------------|-------|---------|-----|----------------|
   | @[handle3] | $[X] | [results] | [X]:1 | Reduce/cut |
   | @[handle4] | $[X] | [results] | [X]:1 | Reduce/cut |
   
   ### Reallocation Recommendation
   
   | From | To | Amount | Rationale |
   |------|----|--------|-----------|
   | [Source] | [Destination] | $[X] | [why] |
   | [Source] | [Destination] | $[X] | [why] |
   
   **Expected Impact**:
   - Additional reach: [X]
   - Improved ROI: [X]:1 → [Y]:1
   ```

## What This Skill Does

1. **Budget Allocation**: Distributes budget across platforms and tiers
2. **Cost Estimation**: Estimates influencer costs by tier and platform
3. **ROI Projection**: Forecasts expected returns
4. **Scenario Planning**: Models different allocation strategies
5. **Efficiency Analysis**: Identifies best value opportunities
6. **Reallocation Recommendations**: Suggests optimizations based on performance

## When to Use This Skill

- Planning budget allocation for a new campaign
- Optimizing spend across multiple influencer tiers
- Deciding between platform investments
- Justifying budget requests to stakeholders
- Reallocating budget mid-campaign based on performance
- Comparing cost efficiency across strategies

## Example

**User**: "Optimize a $30,000 budget for a skincare product launch on Instagram and TikTok targeting Gen Z"

**Output**:

```markdown
## Budget Allocation: $30,000 Skincare Launch

### Recommended Distribution

| Category | Allocation | Notes |
|----------|------------|-------|
| TikTok Influencers | $15,000 (50%) | Primary for Gen Z |
| Instagram Influencers | $9,000 (30%) | Credibility + visual |
| Content Amplification | $4,500 (15%) | Boost top performers |
| Contingency | $1,500 (5%) | Flexibility |

### Influencer Mix

| Platform | Tier | # | Cost Each | Total | Content |
|----------|------|---|-----------|-------|---------|
| TikTok | Micro (50-100K) | 5 | $1,500 | $7,500 | 5 videos |
| TikTok | Nano (10-50K) | 15 | $500 | $7,500 | 15 videos |
| Instagram | Micro (50-100K) | 3 | $2,000 | $6,000 | 3 Reels + Stories |
| Instagram | Nano (10-50K) | 6 | $500 | $3,000 | 6 posts |

**Total Influencers**: 29
**Total Content Pieces**: 29+ (excluding stories)

### Projected Results

- Reach: 2.8M - 3.5M (Estimated)
- Engagements: 280K - 400K (Estimated)
- CPM: $8.50 - $10.70 (Estimated)
- Projected ROI: 3.5:1 (Estimated)

This allocation prioritizes TikTok for viral potential while using Instagram for credibility and detailed product showcase.
```

## Tips for Budget Optimization

1. **Don't put all eggs in one basket** - Diversify across tiers
2. **Reserve amplification budget** - Best content deserves reach
3. **Plan for contingency** - Things change mid-campaign
4. **Negotiate packages** - Multi-post deals save money
5. **Track cost efficiency** - CPM/CPE matter more than raw spend

## Reference Materials

- Shared contract: [skill-contract.md](../../references/skill-contract.md)
- Shared state model: [state-model.md](../../references/state-model.md)
- Connector recipes: [CONNECTORS.md](../../CONNECTORS.md)
- Sibling skills:
  - [campaign-planner](../campaign-planner/SKILL.md) — the campaign plan this budget funds
  - [influencer-discovery](../../map/influencer-discovery/SKILL.md) — find influencers in budget range
  - [outreach-manager](../../activate/outreach-manager/SKILL.md) — turn the allocation into outreach
  - [roi-calculator](../../track/roi-calculator/SKILL.md) — calculate actual ROI post-campaign
  - [performance-analyzer](../../track/performance-analyzer/SKILL.md) — inform reallocation decisions

## Next Best Skill

**Primary**: [outreach-manager](../../activate/outreach-manager/SKILL.md) — once the allocation is funded and the tier mix is locked, move to recruiting the influencers it pays for.

**Alternates** (same IMPACT family):

- [influencer-discovery](../../map/influencer-discovery/SKILL.md) — if you need to source candidates that fit each tier's per-influencer budget first.
- [campaign-planner](../campaign-planner/SKILL.md) — if the budget exposed a gap in the underlying campaign plan.

**Termination**: keep a visited-set. If the recommended next skill was already invoked in this session's chain, stop and report chain-complete instead of re-invoking. Default `max-depth: 3`. When routing is ambiguous, present the options and stop rather than auto-following.
