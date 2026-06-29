---
name: competitor-tracker
description: 'Use when the user asks to "track competitor influencer marketing", "see who my rivals partner with", or "benchmark my influencer program"; produces a competitor partnership roster, campaign and content-strategy breakdown, performance estimates, and a gap/opportunity list. Not for finding your own new creators — use influencer-discovery.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Use when the user wants to understand a competitor's influencer marketing: which creators they partner with, what campaigns and content formats they run, estimated reach and spend, and where they leave gaps. Activate for competitive benchmarking, finding untapped or former-competitor creators, and spotting strategy shifts over time."
argument-hint: "<your brand> [competitor names] [platform]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Map
---

# Competitor Tracker

This skill helps you monitor and analyze your competitors' influencer marketing activities. It tracks who they partner with, what campaigns they run, how they structure collaborations, and what results they appear to achieve.

## Quick Start

Shortest invocation:

```
Monitor [competitor name]'s influencer marketing activities
```

Common scenario — compare a set of rivals and surface gaps:

```
Compare influencer strategies across [competitor 1], [competitor 2], and [competitor 3], then show me which influencers they're missing in [category]
```

## Skill Contract

- **Reads**: your brand name, the competitor set, platforms to monitor, time period, focus areas (partnerships/campaigns/content/all). Public creator handles and post data the user supplies or that ~~social platform analytics returns.
- **Writes**: a competitive intelligence report saved to `memory/influencer/competitor-tracker/YYYY-MM-DD-<topic>.md` (partnership roster, campaign analysis, content-strategy review, performance estimates, side-by-side comparison, opportunity list).
- **Promotes**: durable facts (named competitors, their primary tiers/platforms, confirmed exclusive partners, recurring campaign windows) to `memory/hot-cache.md`.
- **Done when**:
  1. Each tracked competitor has a partnership roster and campaign breakdown with sources or stated estimates.
  2. A side-by-side comparison table covers your brand plus every competitor.
  3. At least 3 ranked opportunities (untapped creators, strategy gaps, or open platforms) are listed.
- **Primary next skill**: [campaign-planner](../../plan/campaign-planner/SKILL.md)

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family is Tier 1 — it works with no live integrations. Ask the user for the competitor set, the platforms, and any creator handles they already know, then build the analysis from public posts and stated estimates.

Where a tool could speed things up, use `~~` connector placeholders:

- `~~influencer database` — pull a competitor's known partner roster and tier mix.
- `~~social platform analytics` — estimate reach, engagement rate, and post cadence per creator.
- `~~CRM` — cross-check whether a former competitor partner has already touched your pipeline.

Label every estimate as an estimate. See [CONNECTORS.md](../../CONNECTORS.md) for the keyless/free recipe per category.

## Instructions

When a user requests competitor tracking:

1. **Define Competitive Set**

   ```markdown
   ### Competitive Tracking Parameters
   
   **Your Brand**: [brand name]
   **Competitors to Track**:
   
   | Competitor | Priority | Category | Notes |
   |------------|----------|----------|-------|
   | [Comp 1] | High | Direct | [notes] |
   | [Comp 2] | High | Direct | [notes] |
   | [Comp 3] | Medium | Indirect | [notes] |
   
   **Platforms to Monitor**: [platforms]
   **Time Period**: [date range]
   **Focus Areas**: [partnerships/campaigns/content/all]
   ```

2. **Track Influencer Partnerships**

   ```markdown
   ## Competitor Influencer Partnerships
   
   ### [Competitor Name]
   
   **Overview**:
   - Total identified partnerships: [#]
   - Active influencer roster: ~[#] creators
   - Primary platforms: [platforms]
   - Influencer tiers used: [mega/macro/micro/nano mix]
   
   #### Current/Recent Partners
   
   | Influencer | Platform | Followers | Partnership Type | Duration |
   |------------|----------|-----------|------------------|----------|
   | @[handle1] | [platform] | [count] | [ambassador/campaign/one-off] | [ongoing/date] |
   | @[handle2] | [platform] | [count] | [type] | [duration] |
   | @[handle3] | [platform] | [count] | [type] | [duration] |
   
   #### Partnership Patterns
   
   **Influencer Selection Criteria** (observed):
   - Follower range: [typical range]
   - Content style: [style preference]
   - Demographics: [audience focus]
   - Niche focus: [categories]
   
   **Relationship Types**:
   | Type | % of Partnerships | Examples |
   |------|-------------------|----------|
   | Brand Ambassadors | [%] | @[handle] |
   | Campaign-based | [%] | @[handle] |
   | One-off posts | [%] | @[handle] |
   | Affiliate | [%] | @[handle] |
   
   **Partnership Frequency**:
   - New partnerships/month: ~[#]
   - Average partnership length: [duration]
   - Repeat collaboration rate: [%]
   
   #### Notable Partners
   
   **[Influencer Name] @[handle]**
   - Relationship since: [date]
   - Content produced: [#] pieces
   - Estimated spend: [$X]
   - Why they work together: [analysis]
   ```

3. **Analyze Campaigns**

   ```markdown
   ## Competitor Campaign Analysis
   
   ### [Competitor Name] Campaigns
   
   #### Recent/Current Campaigns
   
   **Campaign: [Name/Theme]**
   
   | Attribute | Details |
   |-----------|---------|
   | Timeline | [dates] |
   | Platforms | [platforms] |
   | # of Influencers | [count] |
   | Influencer Tier Mix | [breakdown] |
   | Content Type | [types] |
   | Hashtag | #[hashtag] |
   | CTA | [call to action] |
   | Estimated Spend | [$X] |
   
   **Campaign Content Examples**:
   1. @[handle]: [content description] - [engagement]
   2. @[handle]: [content description] - [engagement]
   
   **Campaign Performance Estimates**:
   | Metric | Estimated Value |
   |--------|-----------------|
   | Total Reach | [estimate] |
   | Total Engagement | [estimate] |
   | Engagement Rate | [%] |
   | Content Pieces | [#] |
   | EMV | [$X] |
   
   **What Worked**:
   - [Observation 1]
   - [Observation 2]
   
   **What Didn't**:
   - [Observation 1]
   
   ---
   
   #### Campaign Calendar
   
   | Month | Campaigns | Themes | Spend Level |
   |-------|-----------|--------|-------------|
   | [Month] | [campaigns] | [themes] | [low/medium/high] |
   
   #### Campaign Strategy Patterns
   
   **Seasonal Patterns**:
   - Q1: [typical activity]
   - Q2: [typical activity]
   - Q3: [typical activity]
   - Q4: [typical activity]
   
   **Launch Patterns**:
   - New product launches: [influencer approach]
   - Seasonal campaigns: [approach]
   - Always-on: [approach]
   ```

4. **Review Content Strategy**

   ```markdown
   ## Competitor Content Strategy
   
   ### [Competitor Name]
   
   #### Content Format Preferences
   
   | Format | Usage % | Performance | Notes |
   |--------|---------|-------------|-------|
   | Static posts | [%] | [engagement] | [notes] |
   | Reels/TikToks | [%] | [engagement] | [notes] |
   | Stories | [%] | [engagement] | [notes] |
   | YouTube videos | [%] | [engagement] | [notes] |
   | Live streams | [%] | [engagement] | [notes] |
   
   #### Content Themes
   
   | Theme | Frequency | Example | Performance |
   |-------|-----------|---------|-------------|
   | Product demo | [%] | [example] | [performance] |
   | Lifestyle integration | [%] | [example] | [performance] |
   | Tutorial/How-to | [%] | [example] | [performance] |
   | UGC/Testimonial | [%] | [example] | [performance] |
   | Behind-the-scenes | [%] | [example] | [performance] |
   
   #### Messaging Analysis
   
   **Key Messages Used**:
   1. "[Message 1]" - used in [%] of content
   2. "[Message 2]" - used in [%] of content
   
   **Value Propositions Emphasized**:
   - [Prop 1]: [frequency]
   - [Prop 2]: [frequency]
   
   **Hashtag Strategy**:
   - Branded hashtags: #[hashtag1], #[hashtag2]
   - Campaign hashtags: #[hashtag]
   - Community hashtags: #[hashtag]
   
   #### Creative Direction
   
   **Visual Style**:
   - Aesthetic: [description]
   - Color palette: [colors]
   - Production level: [polished/authentic/mix]
   
   **Tone of Voice**:
   - [Description of typical influencer content tone]
   
   **Creative Freedom Given**:
   - [High/Medium/Low] - [evidence]
   ```

5. **Estimate Performance**

   ```markdown
   ## Competitor Performance Estimates
   
   ### [Competitor Name]
   
   #### Overall Program Metrics (Estimated)
   
   | Metric | Monthly Avg | Quarterly | Annual |
   |--------|-------------|-----------|--------|
   | Active Partnerships | [#] | [#] | [#] |
   | Content Pieces | [#] | [#] | [#] |
   | Total Reach | [X] | [X] | [X] |
   | Total Engagement | [X] | [X] | [X] |
   | EMV Generated | [$X] | [$X] | [$X] |
   | Est. Spend | [$X] | [$X] | [$X] |
   
   #### Performance by Platform
   
   | Platform | Reach | Engagement | ER | Est. Spend |
   |----------|-------|------------|----|-----------| 
   | Instagram | [X] | [X] | [%] | [$X] |
   | TikTok | [X] | [X] | [%] | [$X] |
   | YouTube | [X] | [X] | [%] | [$X] |
   
   #### Performance by Influencer Tier
   
   | Tier | Partners | Avg Reach | Avg ER | Est. Cost/Partner |
   |------|----------|-----------|--------|-------------------|
   | Mega | [#] | [X] | [%] | [$X] |
   | Macro | [#] | [X] | [%] | [$X] |
   | Micro | [#] | [X] | [%] | [$X] |
   | Nano | [#] | [X] | [%] | [$X] |
   
   #### Top Performing Content
   
   1. **@[handle]** - [content type]
      - Engagement: [X]
      - Why it worked: [analysis]
   
   2. **@[handle]** - [content type]
      - Engagement: [X]
      - Why it worked: [analysis]
   
   #### Underperforming Content
   
   1. **@[handle]** - [content type]
      - Engagement: [X]
      - Why it failed: [analysis]
   ```

6. **Generate Competitive Comparison**

   ```markdown
   ## Competitive Comparison
   
   ### Side-by-Side Analysis
   
   | Factor | [Your Brand] | [Comp 1] | [Comp 2] | [Comp 3] |
   |--------|--------------|----------|----------|----------|
   | # Active Partners | [#] | [#] | [#] | [#] |
   | Primary Tier | [tier] | [tier] | [tier] | [tier] |
   | Main Platform | [platform] | [platform] | [platform] | [platform] |
   | Est. Monthly Spend | [$X] | [$X] | [$X] | [$X] |
   | Avg ER | [%] | [%] | [%] | [%] |
   | Content Style | [style] | [style] | [style] | [style] |
   | Relationship Type | [type] | [type] | [type] | [type] |
   
   ### Strategy Comparison
   
   | Strategy Element | [Comp 1] | [Comp 2] | [Comp 3] |
   |------------------|----------|----------|----------|
   | Ambassador program | ✅/❌ | ✅/❌ | ✅/❌ |
   | Affiliate program | ✅/❌ | ✅/❌ | ✅/❌ |
   | Product seeding | ✅/❌ | ✅/❌ | ✅/❌ |
   | Paid partnerships | ✅/❌ | ✅/❌ | ✅/❌ |
   | Events/Trips | ✅/❌ | ✅/❌ | ✅/❌ |
   | User-generated content | ✅/❌ | ✅/❌ | ✅/❌ |
   
   ### Share of Voice
   
   ```
   Category Influencer Share of Voice:
   
   [Your Brand]  |████████░░░░░░░░| 20%
   [Comp 1]      |██████████████░░| 35%
   [Comp 2]      |████████████░░░░| 30%
   [Comp 3]      |██████░░░░░░░░░░| 15%
   ```
   ```

7. **Identify Opportunities**

   ```markdown
   ## Competitive Opportunities
   
   ### Influencer Availability
   
   **Untapped Influencers** (not working with competitors):
   
   | Influencer | Platform | Followers | Fit Score | Opportunity |
   |------------|----------|-----------|-----------|-------------|
   | @[handle] | [platform] | [count] | [score] | [why available] |
   | @[handle] | [platform] | [count] | [score] | [why available] |
   
   **Former Competitor Partners** (available):
   
   | Influencer | Former Partner | Why Ended | Your Opportunity |
   |------------|----------------|-----------|------------------|
   | @[handle] | [competitor] | [reason] | [opportunity] |
   
   ### Strategy Gaps
   
   **What Competitors Are Missing**:
   
   1. **[Gap 1]**: [description]
      - Opportunity: [how to capitalize]
      - Priority: [High/Medium/Low]
   
   2. **[Gap 2]**: [description]
      - Opportunity: [how to capitalize]
      - Priority: [High/Medium/Low]
   
   ### Platform Opportunities
   
   | Platform | Competitor Activity | Your Opportunity |
   |----------|---------------------|------------------|
   | [Platform] | [low/medium/high] | [opportunity] |
   
   ### Niche Opportunities
   
   | Niche | Competitor Coverage | Your Opportunity |
   |-------|---------------------|------------------|
   | [Niche] | [level] | [opportunity] |
   
   ### Content Format Opportunities
   
   | Format | Competitor Usage | Performance | Your Opportunity |
   |--------|------------------|-------------|------------------|
   | [Format] | [level] | [if known] | [opportunity] |
   ```

8. **Generate Insights Report**

   ```markdown
   # Competitive Intelligence Report
   
   **Report Date**: [date]
   **Period Covered**: [timeframe]
   **Competitors Analyzed**: [list]
   
   ## Executive Summary
   
   **Key Findings**:
   1. [Finding 1]
   2. [Finding 2]
   3. [Finding 3]
   
   **Top Opportunities**:
   1. [Opportunity 1]
   2. [Opportunity 2]
   
   **Threats to Monitor**:
   1. [Threat 1]
   2. [Threat 2]
   
   ## Strategic Recommendations
   
   ### Immediate Actions (This Month)
   
   1. **[Action 1]**
      - Why: [rationale]
      - How: [approach]
      - Expected impact: [outcome]
   
   2. **[Action 2]**
      - Why: [rationale]
      - How: [approach]
   
   ### Short-term (This Quarter)
   
   1. **[Action]**: [description]
   
   ### Long-term (This Year)
   
   1. **[Action]**: [description]
   
   ## Tracking Recommendations
   
   **Continue monitoring**:
   - [Competitor]: [specific aspects]
   - [Influencer]: [why important]
   
   **Set alerts for**:
   - [Trigger 1]
   - [Trigger 2]
   
   ## Next Review Date: [date]
   ```

## When to Use This Skill

- Understanding competitor influencer strategies
- Identifying influencers working with competitors
- Finding gaps in competitor coverage
- Benchmarking your influencer program
- Learning from competitor successes and failures
- Identifying saturated vs. available influencers

## What This Skill Does

1. **Partnership Tracking**: Monitors which influencers competitors use
2. **Campaign Analysis**: Analyzes competitor campaign themes and tactics
3. **Content Strategy Review**: Examines content approaches and formats
4. **Performance Estimation**: Estimates competitor campaign performance
5. **Gap Identification**: Finds opportunities competitors are missing
6. **Trend Detection**: Spots shifts in competitor strategies

## Invocation Patterns

### Track Specific Competitors

```
Monitor [competitor name]'s influencer marketing activities
```

```
Who are the influencers partnering with [competitor]?
```

### Competitive Analysis

```
Compare influencer strategies across [competitor 1], [competitor 2], and [competitor 3]
```

### Find Opportunities

```
What influencer opportunities are my competitors missing in [category]?
```

## Example

**User**: "Track the influencer marketing activities of Glossier, Fenty Beauty, and Rare Beauty"

**Output**: [Comprehensive competitor analysis showing Glossier's UGC-heavy approach, Fenty's diverse creator network, Rare Beauty's mental health-focused partnerships, with identification of gaps and opportunities]

## Tips for Success

1. **Monitor continuously** - Set up regular tracking cadence
2. **Go beyond surface level** - Look for patterns, not just partnerships
3. **Track changes** - Note strategy shifts over time
4. **Learn from failures too** - Competitor mistakes are lessons
5. **Stay objective** - Data over assumptions

## Reference Materials

- [skill-contract.md](../../references/skill-contract.md) — shared contract and handoff summary format.
- [state-model.md](../../references/state-model.md) — memory tiers and save-path conventions.
- [CONNECTORS.md](../../CONNECTORS.md) — keyless/free data recipe per `~~` connector category.
- Sibling Map skills: [influencer-discovery](../influencer-discovery/SKILL.md) — find creators competitors aren't using; [fit-scorer](../fit-scorer/SKILL.md) — score competitor partners for your brand.
- [trend-spotter](../../insight/trend-spotter/SKILL.md) — spot trends competitors are riding.

## Next Best Skill

- **Primary**: [campaign-planner](../../plan/campaign-planner/SKILL.md) — turn competitive gaps into a differentiated campaign.
- **Alternate (Map)**: [influencer-discovery](../influencer-discovery/SKILL.md) — pursue the untapped and former-competitor creators this analysis surfaced.
- **Alternate (Map)**: [fit-scorer](../fit-scorer/SKILL.md) — score a competitor's roster against your brand before you poach.

Termination note: keep a visited-set of skills invoked this session. If the next skill has already run this session, stop and report the chain complete instead of re-invoking. Max chain depth is 3 hops.
