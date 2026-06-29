---
name: content-amplifier
description: 'Use when the user asks to "amplify influencer content with paid media", "set up whitelisting or Spark Ads", or "decide which posts to boost"; produces a content-selection scorecard, a paid amplification strategy (whitelisting/boosting/dark posts), audience targeting, and a budget+optimization plan. Not for creating ad variations from raw clips — use ugc-repurposer.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Activate when the user has organic influencer content and wants to extend its reach with paid spend: choosing which posts to boost, setting up whitelisted Partnership Ads or TikTok Spark Ads, planning dark posts, allocating an ad budget across creators and platforms, building audience targeting off creator lookalikes, or running an optimization and scale/pause playbook for boosted creator content."
argument-hint: "<campaign or content set> [budget] [platform]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Convert
---

# Content Amplifier

This skill helps you extend the reach of influencer content through paid amplification strategies. It identifies which content to boost, how to set up campaigns, and how to optimize for maximum impact.

## Quick Start

Shortest invocation:

```
Which influencer content should we amplify from [campaign]?
```

Common scenario:

```
Create a paid amplification plan for our influencer campaign with $[X] budget across TikTok and Instagram
```

## Skill Contract

- **Reads**: organic content set (creator handles, platform, content type, reach, engagement rate, views), amplification budget, campaign objective (awareness/traffic/conversions), target platforms, any prior performance data the user provides.
- **Writes**: content-selection scorecard, paid amplification strategy (whitelisting / brand boosting / dark posts), audience targeting plan, budget allocation, optimization playbook. Save to `memory/influencer/content-amplifier/YYYY-MM-DD-<topic>.md`.
- **Promotes**: durable facts (chosen amplification mix, per-creator spend tiers, winning audiences, scale/pause thresholds) to `memory/hot-cache.md`.
- **Done when**:
  1. Each candidate piece is scored and tiered (must amplify / consider / do not amplify) with a recommended spend.
  2. A budget allocation exists by content, objective, and platform, summing to the stated budget.
  3. An optimization plan with KPI targets and scale/pause rules is recorded.
- **Primary next skill**: [ugc-repurposer](../../convert/ugc-repurposer/SKILL.md) — turn the selected winners into ad variations.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family is Tier 1: it works with no live integrations. Ask the user for the content set, budget, objective, and platforms, and the skill produces the full plan from those inputs.

Where a connector could sharpen the output (all optional):

- `~~social platform analytics` — pull organic reach, engagement rate, and view counts instead of asking the user to paste them.
- `~~ad platform` (Meta Ads Manager, TikTok Ads Manager, Google Ads) — read live CPM/CTR/CPC/ROAS for the optimization playbook, and confirm Spark Ads / Partnership Ad authorization status.
- `~~influencer database` — verify creator audience demographics for lookalike targeting.
- `~~CRM` — supply customer and retargeting audiences for conversion campaigns and exclusions.

See [CONNECTORS.md](../../CONNECTORS.md) for the verified free/keyless recipe per category. None are required; absent a connector, the user supplies the numbers.

## Instructions

When a user requests amplification help:

1. **Assess Available Content**

   ```markdown
   ### Content Inventory for Amplification
   
   **Campaign**: [name]
   **Total Content Pieces**: [#]
   **Amplification Budget**: $[X]
   
   ### Content Performance Overview
   
   | Creator | Platform | Content Type | Organic Reach | ER | Views | Potential |
   |---------|----------|--------------|---------------|----|----- -|-----------|
   | @[handle1] | [platform] | [type] | [reach] | [%] | [views] | ⭐⭐⭐⭐⭐ |
   | @[handle2] | [platform] | [type] | [reach] | [%] | [views] | ⭐⭐⭐⭐ |
   | @[handle3] | [platform] | [type] | [reach] | [%] | [views] | ⭐⭐⭐ |
   ```

2. **Select Content for Amplification**

   ```markdown
   ## Content Selection for Amplification
   
   ### Selection Criteria
   
   | Criterion | Weight | Why It Matters |
   |-----------|--------|----------------|
   | Organic performance | [%] | Proven engagement |
   | Hook quality | [%] | Paid attention capture |
   | Message clarity | [%] | Brand communication |
   | Production quality | [%] | Professional impression |
   | CTA effectiveness | [%] | Conversion potential |
   
   ### Content Scoring
   
   | Content | Organic | Hook | Message | Quality | CTA | Total | Rank |
   |---------|---------|------|---------|---------|-----|-------|------|
   | @[handle1] | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] | [X/25] | 1 |
   | @[handle2] | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] | [X/25] | 2 |
   
   ### Top Picks for Amplification
   
   **Tier 1: Must Amplify**
   
   | Content | Reason | Recommended Spend |
   |---------|--------|-------------------|
   | @[handle1] [content] | [why] | $[X] ([%] of budget) |
   | @[handle2] [content] | [why] | $[X] ([%] of budget) |
   
   **Tier 2: Consider If Budget Allows**
   
   | Content | Reason | Recommended Spend |
   |---------|--------|-------------------|
   | @[handle3] [content] | [why] | $[X] ([%] of budget) |
   
   **Do Not Amplify**
   
   | Content | Reason |
   |---------|--------|
   | @[handle4] [content] | [why it's not worth paid spend] |
   ```

3. **Develop Amplification Strategy**

   ```markdown
   ## Amplification Strategy
   
   ### Strategy Overview
   
   **Objective**: [awareness/traffic/conversions]
   **Total Budget**: $[X]
   **Duration**: [timeframe]
   **Platforms**: [platforms]
   
   ### Amplification Methods
   
   #### Option 1: Whitelisting / Spark Ads
   
   **What it is**: Running ads through the creator's account
   
   | Platform | Format | Requirements | Best For |
   |----------|--------|--------------|----------|
   | Meta Branded Content | Partnership Ads | Creator grants access | Native feel, social proof |
   | TikTok Spark Ads | Spark Ads | Creator authorization | TikTok algorithm, authenticity |
   | YouTube | BrandConnect | Creator approval | Long-form, YouTube search |
   
   **Advantages**:
   - Maintains creator's identity and credibility
   - Better engagement than brand ads
   - Native platform integration
   - Social proof preserved
   
   **Setup Requirements**:
   - [ ] Creator access/authorization
   - [ ] Content approved for paid use
   - [ ] Proper disclosure maintained
   
   #### Option 2: Brand Account Boosting
   
   **What it is**: Sharing/reposting and boosting from brand accounts
   
   **Advantages**:
   - Full control over targeting
   - Simpler to set up
   - No creator coordination needed
   
   **Disadvantages**:
   - Loses some authenticity
   - May perform differently than organic
   
   #### Option 3: Dark Posts
   
   **What it is**: Ads using creator content that don't appear organically
   
   **Best for**: Testing multiple versions, specific targeting
   
   ### Recommended Strategy Mix
   
   | Method | % of Budget | Amount | Rationale |
   |--------|-------------|--------|-----------|
   | Whitelisting | [%] | $[X] | [reason] |
   | Brand Boosting | [%] | $[X] | [reason] |
   | Dark Posts | [%] | $[X] | [reason] |
   ```

4. **Set Up Targeting**

   ```markdown
   ## Audience Targeting Strategy
   
   ### Primary Audience: Lookalike/Similar
   
   **Source**: [creator's audience / engaged users / converters]
   **Similarity**: [1-10% / narrow-broad]
   
   **Targeting**:
   - Lookalike of creator's engaged followers
   - Interest overlap with creator's niche
   - Demographics matching creator's audience
   
   ### Secondary Audience: Expansion
   
   **For Awareness Campaigns**:
   | Audience Segment | Size | Targeting Details |
   |------------------|------|-------------------|
   | Interest-based | [size] | [interests] |
   | Behavioral | [size] | [behaviors] |
   | Demographic | [size] | [demographics] |
   
   **For Conversion Campaigns**:
   | Audience Segment | Size | Targeting Details |
   |------------------|------|-------------------|
   | Retargeting | [size] | Website visitors, engagers |
   | Custom | [size] | Email lists, customers |
   | Lookalike | [size] | Purchase lookalikes |
   
   ### Targeting by Platform
   
   #### Meta (Instagram/Facebook)
   
   | Ad Set | Audience | Targeting | Budget |
   |--------|----------|-----------|--------|
   | [Ad Set 1] | [description] | [details] | $[X] |
   | [Ad Set 2] | [description] | [details] | $[X] |
   
   #### TikTok
   
   | Ad Group | Audience | Targeting | Budget |
   |----------|----------|-----------|--------|
   | [Ad Group 1] | [description] | [details] | $[X] |
   
   ### Exclusions
   
   - Existing customers (if not retargeting)
   - Previous purchasers (if awareness)
   - [Other exclusions]
   ```

5. **Allocate Budget**

   ```markdown
   ## Budget Allocation
   
   ### Total Amplification Budget: $[X]
   
   ### By Content
   
   | Content | Platform | Spend | % | Rationale |
   |---------|----------|-------|---|-----------|
   | @[handle1] video | TikTok | $[X] | [%] | Top performer, high engagement |
   | @[handle2] reel | Instagram | $[X] | [%] | Strong hook, conversion-focused |
   | @[handle3] post | Instagram | $[X] | [%] | Good UGC, authentic feel |
   | Testing pool | Various | $[X] | [%] | A/B testing new content |
   
   ### By Objective
   
   | Objective | Budget | % | Expected Result |
   |-----------|--------|---|-----------------|
   | Awareness/Reach | $[X] | [%] | [impressions] |
   | Traffic | $[X] | [%] | [clicks] |
   | Conversions | $[X] | [%] | [conversions] |
   
   ### By Platform
   
   | Platform | Budget | % | CPM Estimate | Expected Reach |
   |----------|--------|---|--------------|----------------|
   | TikTok | $[X] | [%] | $[X] | [reach] |
   | Instagram | $[X] | [%] | $[X] | [reach] |
   | Facebook | $[X] | [%] | $[X] | [reach] |
   
   ### Pacing
   
   | Period | Daily Budget | Purpose |
   |--------|--------------|---------|
   | Days 1-3 | $[X]/day | Learning phase |
   | Days 4-7 | $[X]/day | Optimization |
   | Days 8+ | $[X]/day | Scaling winners |
   ```

6. **Optimization Guide**

   ```markdown
   ## Optimization Playbook
   
   ### KPIs to Monitor
   
   | Metric | Target | Action If Below | Action If Above |
   |--------|--------|-----------------|-----------------|
   | CPM | $[X] | Adjust targeting | Scale budget |
   | CTR | [%] | Test new creatives | Scale spend |
   | CPC | $[X] | Optimize audience | Increase bid |
   | CVR | [%] | Review landing page | Scale budget |
   | ROAS | [X]:1 | Pause or adjust | Significantly scale |
   
   ### Optimization Schedule
   
   | Day | Action |
   |-----|--------|
   | Day 1-2 | Let campaigns run, collect data |
   | Day 3 | First optimization: pause underperformers |
   | Day 5 | Audience refinement: expand or narrow |
   | Day 7 | Budget reallocation to winners |
   | Ongoing | Weekly optimization cycles |
   
   ### A/B Testing Plan
   
   | Test | Variable A | Variable B | Success Metric |
   |------|------------|------------|----------------|
   | [Test 1] | [version A] | [version B] | [metric] |
   | [Test 2] | [version A] | [version B] | [metric] |
   
   ### When to Scale
   
   **Scale up when**:
   - CPM stable and below target for 3+ days
   - ROAS consistently above [X]:1
   - Frequency below [X]
   - Engagement rate maintained
   
   **Scale method**: 
   - Increase budget 20-30% every 2-3 days
   - Expand audiences gradually
   - Duplicate winning ad sets
   
   ### When to Pause
   
   **Pause when**:
   - CPM 50%+ above target with no improvement
   - ROAS below [X]:1 for 3+ days
   - Frequency above [X]
   - Engagement rate declining
   
   ### Creative Refresh
   
   When to refresh:
   - Frequency reaches [X]+
   - Engagement declining week-over-week
   - CTR drops below [%]
   
   Refresh options:
   - New creator content
   - Different cuts/edits
   - New hook variations
   - Different CTAs
   ```

7. **Platform-Specific Setup**

   ```markdown
   ## Platform Setup Guides
   
   ### Meta (Instagram/Facebook) - Partnership Ads
   
   **Step 1: Creator Authorization**
   1. Creator goes to Instagram Settings > Business > Branded Content
   2. Creator adds your brand as approved partner
   3. Or creator shares post code for specific content
   
   **Step 2: Create Campaign**
   1. Go to Ads Manager > Create Campaign
   2. Select objective
   3. At ad level, select "Use existing post"
   4. Enter branded content ad code
   5. Set up targeting and budget
   
   **Best Practices**:
   - Use creator's caption (edited if needed)
   - Maintain disclosure
   - Test multiple placements
   
   ### TikTok - Spark Ads
   
   **Step 1: Creator Authorization**
   1. Creator opens TikTok app
   2. Goes to video > ... > Ad settings
   3. Turns on "Ad authorization"
   4. Copies authorization code (valid 7-365 days)
   
   **Step 2: Create Campaign**
   1. Go to TikTok Ads Manager
   2. Create campaign with chosen objective
   3. At ad level, select "Spark Ads"
   4. Enter authorization code
   5. Configure targeting
   
   **Best Practices**:
   - Keep TikTok native feel
   - Use In-Feed or TopView placements
   - Enable comments for social proof
   
   ### YouTube - Video Ads
   
   **Setup**:
   1. Get content rights or creator upload to brand channel
   2. Create Video campaign in Google Ads
   3. Select ad format (skippable, non-skippable, etc.)
   4. Configure targeting
   
   **Best Practices**:
   - First 5 seconds are critical
   - Include brand early for non-skippable
   - Use companion banners
   ```

## Example

**User**: "We have 5 influencer TikToks from our launch campaign. Which should we amplify with our $5,000 paid budget?"

**Output**:

```markdown
## Amplification Recommendation

### Content Ranking

| Creator | Views | ER | Hook Score | Amplify? | Budget |
|---------|-------|-----|------------|----------|--------|
| @creator1 | 245K | 8.2% | 5/5 | ✅ Yes | $2,000 |
| @creator3 | 89K | 6.5% | 4/5 | ✅ Yes | $1,500 |
| @creator2 | 156K | 4.1% | 3/5 | ⚠️ Maybe | $500 |
| @creator4 | 34K | 9.8% | 4/5 | ✅ Yes | $800 |
| @creator5 | 67K | 2.3% | 2/5 | ❌ No | $0 |

### Recommended Strategy

**Total Budget**: $5,000

1. **@creator1** ($2,000) - Strongest hook, viral potential, prioritize for awareness
2. **@creator3** ($1,500) - Great product demo, good for consideration
3. **@creator4** ($800) - High engagement despite lower views, loyal audience
4. **@creator2** ($500) - Test budget only, monitor closely
5. **Testing Reserve** ($200) - A/B test variations

### Setup Priority
1. Get Spark Ads authorization from top 3 creators
2. Create awareness campaign for @creator1
3. Create traffic campaign for @creator3
4. Scale winners after 3-day learning phase
```

## Tips for Amplification Success

1. **Don't amplify bad content** - Paid won't fix poor creative
2. **Start with proven winners** - Organic success predicts paid success
3. **Maintain authenticity** - Whitelisting outperforms brand reposts
4. **Test before scaling** - Small tests before big budgets
5. **Optimize continuously** - Paid requires active management

## Reference Materials

- [skill-contract.md](../../references/skill-contract.md) — shared contract and Handoff Summary format.
- [state-model.md](../../references/state-model.md) — HOT/WARM/COLD memory tiers and save conventions.
- [CONNECTORS.md](../../CONNECTORS.md) — free/keyless data recipes per connector category.
- Sibling skills: [content-reviewer](../../activate/content-reviewer/SKILL.md), [ugc-repurposer](../../convert/ugc-repurposer/SKILL.md), [budget-optimizer](../../plan/budget-optimizer/SKILL.md), [performance-analyzer](../../track/performance-analyzer/SKILL.md).

## Next Best Skill

**Primary**: [ugc-repurposer](../../convert/ugc-repurposer/SKILL.md) — turn the selected amplification winners into ad-ready variations and cut-downs.

**Alternates (same Convert family)**:
- [performance-analyzer](../../track/performance-analyzer/SKILL.md) — measure amplification results once campaigns are live.
- [budget-optimizer](../../plan/budget-optimizer/SKILL.md) — reallocate paid budget across the recommended tiers.

**Termination note**: maintain a visited-set this session. If a recommended skill has already run, stop and report the chain complete rather than re-invoking it. Stop after a maximum chain depth of 3.
