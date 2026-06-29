---
name: performance-analyzer
description: 'Use when the user asks to "analyze influencer campaign performance", "compare influencers", or "find what content worked"; produces metric scorecards vs target and benchmark, platform/influencer/content rankings, engagement-quality and sentiment reads, conversion-attribution breakdowns, and ranked learnings. Not for dollar-level return math — use roi-calculator.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Use mid-flight or post-campaign when a user wants to evaluate influencer results, compare creators against each other, find top-performing content or formats, judge engagement quality and comment sentiment, connect influencer activity to conversions, or build performance benchmarks for future planning."
argument-hint: "<campaign name> [platform or influencer handles]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Track
---

# Performance Analyzer

This skill helps you analyze influencer marketing campaign performance comprehensively. It goes beyond surface metrics to understand what truly worked and why.

## Quick Start

Shortest invocation:

```
Analyze performance of [campaign name] influencer campaign
```

Common scenario — compare creators within one campaign:

```
Compare performance of these influencers from [campaign]: @handle1, @handle2, @handle3
```

## Skill Contract

- **Reads**: campaign name and date range; native platform analytics (reach, views, engagement); influencer-supplied reports or screenshots; website/GA traffic and conversion data; sales and promo-code redemption data; targets and benchmarks if the user has them.
- **Writes**: a performance analysis to `memory/influencer/performance-analyzer/YYYY-MM-DD-<campaign>.md` covering core-metric scorecards, platform/influencer/content rankings, engagement-quality and sentiment reads, conversion attribution, and ranked learnings.
- **Promotes**: durable facts (top-performing creators, winning formats, platform ROI splits, roster renew/drop calls) to `memory/hot-cache.md`.
- **Done when**:
  - Core metrics are scored against target and benchmark with a performance verdict.
  - Top and bottom performers are ranked with reasons, and content patterns that worked are named.
  - Conversions are attributed by method (promo code / UTM / direct / estimated) and 3-5 learnings are written.
- **Primary next skill**: [roi-calculator](../../track/roi-calculator/SKILL.md) — turn measured performance into dollar-level return.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family needs no live integrations (Tier 1). The skill runs entirely on inputs you provide — paste platform exports, influencer report screenshots, GA numbers, and promo-code redemption counts, and it builds the full analysis. Ask the user for whatever is missing rather than blocking.

Where a connector could speed the work, the skill marks it with a `~~` placeholder:

- `~~social platform analytics` — native reach/engagement/video metrics per post.
- `~~web analytics` — site traffic, click-through, and on-site conversion data.
- `~~ecommerce / sales platform` — revenue, orders, AOV, promo-code redemptions.
- `~~influencer database` — historical creator benchmarks for comparison.

No placeholder is required to run. See [CONNECTORS.md](../../CONNECTORS.md) for the verified free/keyless data recipe per category.

## Instructions

When a user requests performance analysis:

1. **Gather Performance Data**

   ```markdown
   ### Performance Data Collection
   
   **Campaign**: [name]
   **Period**: [start] - [end]
   **Influencers**: [count]
   **Platforms**: [platforms]
   
   ### Data Sources
   
   | Source | Metrics Available | Collection Method |
   |--------|-------------------|-------------------|
   | Native analytics | Reach, views, engagement | Platform export |
   | Influencer reports | Screenshots/exports | From creators |
   | Website analytics | Traffic, conversions | GA/tracking |
   | Sales data | Revenue, orders | E-commerce platform |
   | Promo code data | Redemptions | Sales system |
   ```

2. **Analyze Core Metrics**

   ```markdown
   ## Campaign Performance Overview
   
   ### Summary Metrics
   
   | Metric | Result | Target | vs. Target | vs. Benchmark |
   |--------|--------|--------|------------|---------------|
   | Total Reach | [X] | [X] | [+/-X%] | [+/-X%] |
   | Total Impressions | [X] | [X] | [+/-X%] | [+/-X%] |
   | Total Engagements | [X] | [X] | [+/-X%] | [+/-X%] |
   | Engagement Rate | [X%] | [X%] | [+/-X%] | [+/-X%] |
   | Total Video Views | [X] | [X] | [+/-X%] | [+/-X%] |
   | Link Clicks | [X] | [X] | [+/-X%] | [+/-X%] |
   | Promo Code Uses | [X] | [X] | [+/-X%] | N/A |
   | Conversions | [X] | [X] | [+/-X%] | [+/-X%] |
   | Revenue | $[X] | $[X] | [+/-X%] | N/A |
   
   ### Performance Score: [X/10]
   
   **Assessment**: [Excellent/Good/Average/Below Average/Poor]
   
   ### Key Highlights
   
   ✅ **What Exceeded Expectations**:
   - [Highlight 1]
   - [Highlight 2]
   
   ⚠️ **What Underperformed**:
   - [Issue 1]
   - [Issue 2]
   ```

3. **Analyze by Platform**

   ```markdown
   ## Platform Performance
   
   ### Platform Comparison
   
   | Platform | Reach | Engagements | ER | Clicks | Conversions | CPA |
   |----------|-------|-------------|-------|--------|-------------|-----|
   | Instagram | [X] | [X] | [%] | [X] | [X] | $[X] |
   | TikTok | [X] | [X] | [%] | [X] | [X] | $[X] |
   | YouTube | [X] | [X] | [%] | [X] | [X] | $[X] |
   | **Total** | **[X]** | **[X]** | **[%]** | **[X]** | **[X]** | **$[X]** |
   
   ### Platform Insights
   
   **Best Performing Platform**: [Platform]
   - Why: [analysis]
   - Key content: [what worked]
   
   **Underperforming Platform**: [Platform]
   - Why: [analysis]
   - Improvement opportunity: [suggestion]
   
   ### Platform-Specific Metrics
   
   #### Instagram
   
   | Metric | Feed Posts | Reels | Stories |
   |--------|------------|-------|---------|
   | Reach | [X] | [X] | [X] |
   | Engagements | [X] | [X] | [X] |
   | ER | [%] | [%] | [%] |
   | Saves | [X] | [X] | N/A |
   | Shares | [X] | [X] | [X] |
   
   #### TikTok
   
   | Metric | Result | Benchmark |
   |--------|--------|-----------|
   | Views | [X] | |
   | Likes | [X] | |
   | Comments | [X] | |
   | Shares | [X] | |
   | Average Watch Time | [X]s | |
   | Completion Rate | [%] | |
   ```

4. **Analyze by Influencer**

   ```markdown
   ## Influencer Performance
   
   ### Influencer Ranking
   
   | Rank | Influencer | Reach | ER | Conversions | ROI | Score |
   |------|------------|-------|-------|-------------|-----|-------|
   | 1 | @[handle] | [X] | [%] | [X] | [X]:1 | ⭐⭐⭐⭐⭐ |
   | 2 | @[handle] | [X] | [%] | [X] | [X]:1 | ⭐⭐⭐⭐ |
   | 3 | @[handle] | [X] | [%] | [X] | [X]:1 | ⭐⭐⭐⭐ |
   | 4 | @[handle] | [X] | [%] | [X] | [X]:1 | ⭐⭐⭐ |
   | 5 | @[handle] | [X] | [%] | [X] | [X]:1 | ⭐⭐ |
   
   ### Top Performers Deep Dive
   
   #### #1: @[handle]
   
   | Metric | Result | vs. Campaign Avg |
   |--------|--------|------------------|
   | Reach | [X] | [+/-X%] |
   | Engagement Rate | [%] | [+/-X%] |
   | Video Completion | [%] | [+/-X%] |
   | Click-through Rate | [%] | [+/-X%] |
   | Conversion Rate | [%] | [+/-X%] |
   | Cost per Conversion | $[X] | [+/-X%] |
   
   **Why They Performed Well**:
   - [Reason 1]
   - [Reason 2]
   - [Reason 3]
   
   **Content Analysis**:
   - Format: [what they posted]
   - Hook: [how they opened]
   - Message: [how they communicated]
   - CTA: [what they asked viewers to do]
   
   **Recommendation**: [Renew/Expand/Ambassador potential]
   
   ### Underperformers Analysis
   
   #### @[handle]
   
   **Results**: [summary]
   **Why Underperformed**: [analysis]
   **Learning**: [what to do differently]
   ```

5. **Content Performance Analysis**

   ```markdown
   ## Content Performance
   
   ### Top Performing Content
   
   | Rank | Creator | Platform | Format | Reach | ER | Key Feature |
   |------|---------|----------|--------|-------|-------|-------------|
   | 1 | @[handle] | [platform] | [format] | [X] | [%] | [why it worked] |
   | 2 | @[handle] | [platform] | [format] | [X] | [%] | [why it worked] |
   | 3 | @[handle] | [platform] | [format] | [X] | [%] | [why it worked] |
   
   ### Content Format Analysis
   
   | Format | Pieces | Avg Reach | Avg ER | Best Performer |
   |--------|--------|-----------|--------|----------------|
   | Video (Reels/TikTok) | [#] | [X] | [%] | @[handle] |
   | Static Images | [#] | [X] | [%] | @[handle] |
   | Carousels | [#] | [X] | [%] | @[handle] |
   | Stories | [#] | [X] | [%] | @[handle] |
   | YouTube Videos | [#] | [X] | [%] | @[handle] |
   
   ### Content Theme Analysis
   
   | Theme | Pieces | Avg ER | Conversion Rate | Notes |
   |-------|--------|--------|-----------------|-------|
   | Product demo | [#] | [%] | [%] | [notes] |
   | Lifestyle | [#] | [%] | [%] | [notes] |
   | Tutorial | [#] | [%] | [%] | [notes] |
   | Review | [#] | [%] | [%] | [notes] |
   | Unboxing | [#] | [%] | [%] | [notes] |
   
   ### Winning Content Patterns
   
   **Hook Patterns That Worked**:
   - [Pattern 1]: [examples]
   - [Pattern 2]: [examples]
   
   **Messaging That Resonated**:
   - [Message type 1]: [why it worked]
   - [Message type 2]: [why it worked]
   
   **Visual Elements That Performed**:
   - [Element 1]
   - [Element 2]
   ```

6. **Engagement Quality Analysis**

   ```markdown
   ## Engagement Quality
   
   ### Engagement Breakdown
   
   | Type | Volume | % of Total | Quality Assessment |
   |------|--------|------------|-------------------|
   | Likes | [X] | [%] | Passive |
   | Comments | [X] | [%] | [quality] |
   | Saves | [X] | [%] | High intent |
   | Shares | [X] | [%] | High value |
   | Link clicks | [X] | [%] | Direct action |
   
   ### Comment Sentiment Analysis
   
   | Sentiment | % | Examples |
   |-----------|---|----------|
   | Positive | [%] | "[example]", "[example]" |
   | Neutral/Questions | [%] | "[example]", "[example]" |
   | Negative | [%] | "[example]", "[example]" |
   
   **Key Themes in Comments**:
   - [Theme 1]: [frequency] mentions
   - [Theme 2]: [frequency] mentions
   - [Theme 3]: [frequency] mentions
   
   ### Purchase Intent Signals
   
   | Signal | Count | Examples |
   |--------|-------|----------|
   | "Where to buy" questions | [#] | |
   | Price questions | [#] | |
   | Code requests | [#] | |
   | "Just ordered" | [#] | |
   | Tagged friends | [#] | |
   
   ### Engagement Quality Score: [X/10]
   ```

7. **Conversion & Attribution Analysis**

   ```markdown
   ## Conversion Analysis
   
   ### Conversion Funnel
   
   ```
   Reach        [XXXXXXXXXX] 1,000,000  (100%)
                     ↓
   Engagements  [XXXXXXX   ]   150,000  (15%)
                     ↓
   Link Clicks  [XXX       ]    25,000  (2.5%)
                     ↓
   Site Visits  [XX        ]    20,000  (2%)
                     ↓
   Add to Cart  [X         ]     5,000  (0.5%)
                     ↓
   Purchases    [X         ]     2,000  (0.2%)
   ```
   
   ### Conversion Metrics
   
   | Metric | Result | Benchmark | Status |
   |--------|--------|-----------|--------|
   | Click-through Rate | [%] | [%] | ✅/❌ |
   | Landing Page CVR | [%] | [%] | ✅/❌ |
   | Overall CVR | [%] | [%] | ✅/❌ |
   | Cost per Click | $[X] | $[X] | ✅/❌ |
   | Cost per Conversion | $[X] | $[X] | ✅/❌ |
   
   ### Attribution by Method
   
   | Method | Conversions | Revenue | % of Total |
   |--------|-------------|---------|------------|
   | Promo codes | [X] | $[X] | [%] |
   | UTM tracking | [X] | $[X] | [%] |
   | Direct attribution | [X] | $[X] | [%] |
   | Estimated influence | [X] | $[X] | [%] |
   
   ### Promo Code Performance
   
   | Code | Influencer | Uses | Revenue | AOV |
   |------|------------|------|---------|-----|
   | [CODE1] | @[handle] | [X] | $[X] | $[X] |
   | [CODE2] | @[handle] | [X] | $[X] | $[X] |
   | [CODE3] | @[handle] | [X] | $[X] | $[X] |
   ```

8. **Generate Insights & Recommendations**

   ```markdown
   ## Insights & Recommendations
   
   ### Top 5 Learnings
   
   1. **[Learning 1]**
      - What we observed: [data]
      - Why it matters: [significance]
      - Future application: [how to use this]
   
   2. **[Learning 2]**
      - What we observed: [data]
      - Why it matters: [significance]
      - Future application: [how to use this]
   
   [Continue for top 5]
   
   ### What Worked
   
   | Element | Performance | Recommendation |
   |---------|-------------|----------------|
   | [Element 1] | [metric] | Do more of this |
   | [Element 2] | [metric] | Expand this approach |
   
   ### What Didn't Work
   
   | Element | Performance | Recommendation |
   |---------|-------------|----------------|
   | [Element 1] | [metric] | Adjust or eliminate |
   | [Element 2] | [metric] | Test alternatives |
   
   ### Optimization Opportunities
   
   | Opportunity | Expected Impact | Effort | Priority |
   |-------------|-----------------|--------|----------|
   | [Opportunity 1] | [impact] | [effort] | High |
   | [Opportunity 2] | [impact] | [effort] | Medium |
   | [Opportunity 3] | [impact] | [effort] | Low |
   
   ### Influencer Roster Recommendations
   
   | Influencer | Recommendation | Rationale |
   |------------|----------------|-----------|
   | @[handle1] | Renew/Ambassador | Top performer |
   | @[handle2] | Renew at same level | Solid results |
   | @[handle3] | Don't renew | Below expectations |
   | @[handle4] | Increase investment | High potential |
   
   ### Future Campaign Recommendations
   
   1. **Platform Mix**: [recommendation]
   2. **Influencer Tier**: [recommendation]
   3. **Content Format**: [recommendation]
   4. **Messaging**: [recommendation]
   5. **Budget Allocation**: [recommendation]
   ```

## Example

**User**: "Analyze performance of our summer skincare campaign with 10 influencers"

**Output**:

```markdown
# Summer Skincare Campaign Performance Analysis

## Executive Summary

**Campaign Performance**: Above Average (7.5/10)

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Total Reach | 2.4M | 2M | ✅ +20% |
| Engagement Rate | 4.2% | 3.5% | ✅ +20% |
| Conversions | 1,847 | 2,000 | ⚠️ -8% |
| Revenue | $142,500 | $150,000 | ⚠️ -5% |
| ROI | 2.8:1 | 3:1 | ⚠️ -7% |

## Top 3 Performers

1. **@skincaresarah** - ROI 4.2:1, highest conversions
2. **@glowwithgrace** - Best engagement (6.8%)
3. **@beautyreview** - Highest reach per dollar

## Key Learning

TikTok outperformed Instagram significantly (3.5:1 ROI vs 2.1:1). Recommend shifting 20% of Instagram budget to TikTok for future campaigns.

## Recommendation

Renew partnerships with top 5 performers. Replace bottom 2 with TikTok-native creators.
```

## Reference Materials

- [skill-contract.md](../../references/skill-contract.md) — shared contract and handoff format.
- [state-model.md](../../references/state-model.md) — memory tiers and save-path conventions.
- [CONNECTORS.md](../../CONNECTORS.md) — verified free/keyless data recipes per connector category.
- The C3 benchmark at [references/c3/scoring-architecture.md](../../references/c3/scoring-architecture.md) — scoring architecture when a structured score is needed.
- Sibling skills: [roi-calculator](../../track/roi-calculator/SKILL.md), [report-generator](../../track/report-generator/SKILL.md), [fit-scorer](../../map/fit-scorer/SKILL.md), [campaign-planner](../../plan/campaign-planner/SKILL.md).

## Next Best Skill

**Primary**: [roi-calculator](../../track/roi-calculator/SKILL.md) — convert measured performance into dollar-level ROI, cost-per-result, and payback math.

**Alternates** (same Track family):

- [report-generator](../../track/report-generator/SKILL.md) — package the analysis into a formal stakeholder report.
- [fit-scorer](../../map/fit-scorer/SKILL.md) — feed proven performers back into creator scoring for the next round.

**Termination note**: Maintain a visited-set. If a skill has already been invoked this session, stop and report chain-complete rather than re-running it. Cap the chain at max-depth 3 hops; if results are inconclusive after that, surface the open loops to the user instead of continuing.
