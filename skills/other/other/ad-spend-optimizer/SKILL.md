---
name: ad-spend-optimizer
description: Optimize paid advertising budget allocation across channels using performance data, attribution models, and ROI analysis
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Ad Spend Optimizer

> Systematically optimize paid advertising budget allocation across channels based on performance data, attribution analysis, and ROI targets.

## When to Use This Skill

- Quarterly budget planning
- Channel mix optimization
- Performance troubleshooting
- Scaling paid acquisition
- ROI analysis and reporting

## Methodology Foundation

Based on **marginal ROI optimization** and **portfolio theory for marketing**, combining:
- Channel performance analysis
- Attribution modeling
- Diminishing returns curves
- Test and scale frameworks

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Analyzes channel performance | Budget constraints |
| Calculates ROI by channel | Risk tolerance |
| Recommends allocation shifts | Testing budgets |
| Identifies optimization opportunities | Business priorities |
| Creates performance dashboards | Platform selection |

## Instructions

### Step 1: Audit Current Performance

**Key Metrics by Channel:**

| Metric | Definition | Target |
|--------|------------|--------|
| ROAS | Revenue / Ad Spend | >3:1 |
| CAC | Cost to Acquire Customer | <LTV/3 |
| CPA | Cost per Acquisition | Varies |
| CTR | Clicks / Impressions | Benchmark |
| Conv Rate | Conversions / Clicks | Benchmark |

### Step 2: Attribution Analysis

**Attribution Models:**

| Model | Logic | Best For |
|-------|-------|----------|
| Last Click | 100% to final touchpoint | Direct response |
| First Click | 100% to first touchpoint | Awareness campaigns |
| Linear | Equal across all touchpoints | Balanced view |
| Time Decay | More to recent touchpoints | Shorter cycles |
| Position | 40% first, 40% last, 20% middle | Balanced with emphasis |
| Data-Driven | ML-based attribution | Sophisticated analysis |

### Step 3: Identify Optimization Opportunities

**Optimization Levers:**

| Lever | Impact | Effort |
|-------|--------|--------|
| Budget reallocation | High | Low |
| Audience targeting | High | Medium |
| Creative refresh | Medium | Medium |
| Bid optimization | Medium | Low |
| Landing page | High | High |
| New channel test | Variable | Medium |

### Step 4: Calculate Optimal Allocation

**Marginal ROI Analysis:**
- Where is next $1 best spent?
- Identify diminishing returns
- Find underinvested channels
- Balance efficiency vs. scale

### Step 5: Implement and Monitor

**Test Framework:**
- 70% proven channels
- 20% optimization tests
- 10% new channel experiments

## Examples

### Example 1: Full Budget Optimization

**Input:**
```
Optimize this ad spend:
- Monthly budget: $100,000
- Channels: Google Ads (50K), Meta (30K), LinkedIn (15K), Other (5K)
- Goals: B2B SaaS, $200 target CAC, need 500 leads/month
```

**Output:**
```
## Ad Spend Optimization Analysis

### Current Performance Audit

| Channel | Spend | Leads | CAC | ROAS | CPL |
|---------|-------|-------|-----|------|-----|
| Google Ads | $50,000 | 180 | $278 | 2.1x | $278 |
| Meta | $30,000 | 150 | $200 | 2.8x | $200 |
| LinkedIn | $15,000 | 45 | $333 | 1.5x | $333 |
| Other | $5,000 | 20 | $250 | 2.0x | $250 |
| **Total** | **$100,000** | **395** | **$253** | **2.2x** | **$253** |

**Current Status:**
- Missing target: 395 leads vs 500 goal (79%)
- Above CAC target: $253 vs $200 goal

---

### Channel Analysis

#### Google Ads ($50K)

| Breakdown | Spend | Leads | CAC | Assessment |
|-----------|-------|-------|-----|------------|
| Brand | $10,000 | 80 | $125 | ✅ Efficient |
| Non-Brand | $25,000 | 70 | $357 | ⚠️ High CAC |
| Display | $15,000 | 30 | $500 | ❌ Cut |

**Findings:**
- Brand is highly efficient but limited scale
- Non-brand has high CAC but scalable
- Display not performing—recommend pause

**Recommendations:**
- Increase brand budget (limited by search volume)
- Optimize non-brand (better audiences, negatives)
- Pause display, reallocate to Meta

---

#### Meta ($30K)

| Breakdown | Spend | Leads | CAC | Assessment |
|-----------|-------|-------|-----|------------|
| Lookalike | $15,000 | 85 | $176 | ✅ Best performer |
| Interest | $10,000 | 45 | $222 | ✅ Good |
| Retargeting | $5,000 | 20 | $250 | ✅ Standard |

**Findings:**
- Lookalike audiences are star performers
- Interest targeting has room to scale
- Strong overall channel

**Recommendations:**
- Increase lookalike budget significantly
- Test new lookalike seeds
- Shift underperforming Google budget here

---

#### LinkedIn ($15K)

| Breakdown | Spend | Leads | CAC | Assessment |
|-----------|-------|-------|-----|------------|
| Sponsored Content | $10,000 | 35 | $286 | ⚠️ High |
| Lead Gen Forms | $5,000 | 10 | $500 | ❌ Very high |

**Findings:**
- Highest CAC channel
- But: LinkedIn leads often higher quality (enterprise)
- Lead Gen Forms underperforming

**Recommendations:**
- Reduce overall LinkedIn spend
- Shift to sponsored content only
- Test LinkedIn for enterprise segment specifically

---

#### Other ($5K)

**Breakdown:** Reddit, Quora, programmatic
**Performance:** Mixed, small sample sizes

**Recommendation:** Continue testing but don't scale yet

---

### Recommended Budget Reallocation

#### Before vs After

| Channel | Current | Proposed | Change |
|---------|---------|----------|--------|
| Google Ads | $50,000 | $35,000 | -$15,000 |
| Meta | $30,000 | $50,000 | +$20,000 |
| LinkedIn | $15,000 | $8,000 | -$7,000 |
| Testing | $5,000 | $7,000 | +$2,000 |
| **Total** | **$100,000** | **$100,000** | - |

---

#### Detailed Allocation

**Google Ads ($35K)**
| Campaign | Budget | Expected Leads | Expected CAC |
|----------|--------|----------------|--------------|
| Brand | $12,000 | 95 | $126 |
| Non-Brand (optimized) | $23,000 | 75 | $307 |
| Display | $0 | 0 | - |
| **Total** | **$35,000** | **170** | **$206** |

**Meta ($50K)**
| Campaign | Budget | Expected Leads | Expected CAC |
|----------|--------|----------------|--------------|
| Lookalike | $30,000 | 170 | $176 |
| Interest | $15,000 | 65 | $231 |
| Retargeting | $5,000 | 20 | $250 |
| **Total** | **$50,000** | **255** | **$196** |

**LinkedIn ($8K)**
| Campaign | Budget | Expected Leads | Expected CAC |
|----------|--------|----------------|--------------|
| Sponsored Content | $8,000 | 28 | $286 |
| Lead Gen | $0 | 0 | - |
| **Total** | **$8,000** | **28** | **$286** |

**Testing ($7K)**
| Test | Budget | Purpose |
|------|--------|---------|
| TikTok | $3,000 | New channel |
| YouTube | $2,500 | Video content |
| Reddit (scale) | $1,500 | Community |

---

### Projected Results

| Metric | Current | Proposed | Change |
|--------|---------|----------|--------|
| Total Leads | 395 | 473 | +20% |
| Blended CAC | $253 | $211 | -17% |
| Goal Achievement | 79% | 95% | +16 pts |
| ROAS | 2.2x | 2.6x | +18% |

---

### Implementation Roadmap

**Week 1:**
- [ ] Pause Google Display campaigns
- [ ] Reduce LinkedIn Lead Gen to $0
- [ ] Increase Meta Lookalike by $5K

**Week 2:**
- [ ] Complete Google to Meta shift
- [ ] Launch TikTok test campaign
- [ ] Set up new Lookalike audiences

**Week 3-4:**
- [ ] Monitor and optimize
- [ ] Scale what's working
- [ ] Report on progress

---

### Monitoring Dashboard

```
┌────────────────────────────────────────────────────────┐
│  AD SPEND DASHBOARD                        Week 1      │
├────────────────────────────────────────────────────────┤
│                                                        │
│  SPEND PACING                                          │
│  Google:  ████████░░░░  $8,200/$8,750 (94%)          │
│  Meta:    █████████░░░  $11,800/$12,500 (94%)         │
│  LinkedIn:██████░░░░░░  $1,500/$2,000 (75%)          │
│  Testing: █████░░░░░░░  $900/$1,750 (51%)            │
│                                                        │
│  LEADS THIS WEEK                                       │
│  Target: 118 | Actual: 124 | Pacing: +5%             │
│                                                        │
│  CAC THIS WEEK                                         │
│  Target: $211 | Actual: $195 | Status: ✅             │
│                                                        │
│  ALERTS:                                               │
│  ⚠️ LinkedIn CPC up 15% - monitor                     │
│  ✅ Meta Lookalike exceeding expectations              │
│                                                        │
└────────────────────────────────────────────────────────┘
```
```

### Example 2: Quick Channel Assessment

**Input:**
```
Should we increase spend on this channel?
- Channel: Facebook
- Current spend: $10K/month
- CAC: $150
- Target CAC: $200
- Leads: 67
- Need: More leads
```

**Output:**
```
## Channel Scale Assessment: Facebook

### Current Performance

| Metric | Value | Status |
|--------|-------|--------|
| Spend | $10,000 | Baseline |
| Leads | 67 | - |
| CAC | $150 | ✅ Below target |
| Headroom | $50 | Room to scale |

### Scale Recommendation: YES, but carefully

**Why scale:**
- CAC ($150) is 25% below target ($200)
- Indicates efficiency headroom
- Leads are needed

**How to scale:**

| Scenario | Spend | Expected Leads | Expected CAC |
|----------|-------|----------------|--------------|
| Conservative | $15,000 | 90 | $167 |
| Moderate | $20,000 | 110 | $182 |
| Aggressive | $25,000 | 125 | $200 |

**Recommendation:** Start with moderate (+$10K)

### Scaling Checklist

- [ ] Expand Lookalike audiences
- [ ] Test new interest targets
- [ ] Increase frequency caps gradually
- [ ] Monitor CAC weekly
- [ ] Set alert at $185 CAC

### Warning Signs (Stop Scaling)

- CAC exceeds $200
- CTR drops >20%
- Frequency >3.0
- Negative ROI on increment
```

## Skill Boundaries

### What This Skill Does Well
- Analyzing channel performance
- Recommending budget shifts
- Calculating ROI projections
- Creating optimization frameworks

### What This Skill Cannot Do
- Access your ad accounts
- Make real-time bid changes
- Know your specific creative
- Guarantee performance

## Iteration Guide

**Follow-up Prompts:**
- "Analyze [specific channel] performance"
- "How should we test [new channel]?"
- "Create a pacing dashboard for [budget]"
- "What's causing [performance issue]?"

## References

- Google Ads Optimization Guide
- Meta Business Suite Best Practices
- LinkedIn Marketing Solutions
- AdEspresso Budget Allocation

## Related Skills

- `google-ads-expert` - Google-specific
- `aarrr-metrics` - Full funnel view
- `growth-loops` - Sustainable growth

## Skill Metadata

- **Domain**: Acquisition
- **Complexity**: Intermediate-Advanced
- **Mode**: centaur
- **Time to Value**: 2-3 hours per analysis
- **Prerequisites**: Ad account access, performance data
