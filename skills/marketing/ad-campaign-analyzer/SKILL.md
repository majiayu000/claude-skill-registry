---
name: ad-campaign-analyzer
description: >
  Analyze ad campaign performance data (Google, Meta, LinkedIn) to identify what's
  working, what's wasting budget, and specific cut/scale/test recommendations. Takes
  CSV or pasted data, runs statistical analysis, and produces a diagnostic report
  with action items.
tags: [ads]
---

# Ad Campaign Analyzer

Take raw campaign performance data and turn it into clear decisions. This skill doesn't just summarize metrics — it diagnoses problems, identifies winners, checks statistical significance, and tells you exactly what to cut, scale, and test next.

**Core principle:** Most startup founders check their ad dashboard, see a ROAS number, and either panic or celebrate. This skill gives you the nuanced analysis a paid media specialist would: what's actually significant, what's noise, and where your next dollar should go.

## When to Use

- "Analyze my Google Ads performance"
- "Which ads should I kill?"
- "Is this campaign working?"
- "Where am I wasting ad spend?"
- "Optimize my Meta Ads"

## Phase 0: Intake

1. **Campaign data** — One of:
   - CSV export from Google Ads / Meta Ads Manager / LinkedIn Campaign Manager
   - Pasted performance table
   - Screenshots of dashboard (we'll extract the data)
2. **Platform(s)** — Google / Meta / LinkedIn / All
3. **Time period** — What date range does this cover?
4. **Monthly budget** — Total ad spend in this period
5. **Primary goal** — What conversion are you optimizing for? (Demos / Trials / Purchases / Leads)
6. **Target metrics** — Do you have target CPA or ROAS? (If not, we'll benchmark)
7. **Any known changes?** — Did you change creative, budget, or targeting during this period?

## Phase 1: Data Ingestion & Normalization

### Accepted Data Formats

| Source | Key Columns Expected |
|--------|---------------------|
| **Google Ads** | Campaign, Ad Group, Keyword, Impressions, Clicks, CTR, CPC, Conversions, Conv Rate, Cost, Conv Value |
| **Meta Ads** | Campaign, Ad Set, Ad, Impressions, Reach, Clicks, CTR, CPC, Conversions, Cost Per Result, Amount Spent, ROAS |
| **LinkedIn Ads** | Campaign, Impressions, Clicks, CTR, CPC, Conversions, Cost, Leads |

Normalize all data into a standard analysis format:

| Dimension | Impressions | Clicks | CTR | CPC | Conversions | Conv Rate | CPA | Spend | Revenue/Value |
|-----------|------------|--------|-----|-----|-------------|----------|-----|-------|--------------|

## Phase 2: Performance Diagnostics

### 2A: Campaign-Level Health Check

For each campaign:

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| CTR | [X%] | [Industry avg] | [Good/Okay/Poor] |
| CPC | $[X] | [Category avg] | [Good/Okay/Poor] |
| Conv Rate | [X%] | [Benchmark] | [Good/Okay/Poor] |
| CPA | $[X] | [Target or benchmark] | [Good/Okay/Poor] |
| ROAS | [X] | [Target or benchmark] | [Good/Okay/Poor] |
| Impression Share | [X%] | [>60% ideal] | [Good/Okay/Poor] |

### 2B: Budget Waste Detection

Identify spend that produced no or negative return:

| Waste Type | Signal | Action |
|-----------|--------|--------|
| **Zero-conversion keywords/ads** | Spend > $[X] with 0 conversions | Pause or add negatives |
| **High CPA outliers** | CPA > 3x target | Pause or restructure |
| **Low CTR ads** | CTR < 50% of campaign average | Replace creative |
| **Broad match bleed** | Search terms report showing irrelevant clicks | Add negative keywords |
| **Audience overlap** | Same users hit by multiple campaigns | Exclude audiences |
| **Dayparting waste** | Conversions cluster at certain hours; spend is 24/7 | Set ad schedule |

### 2C: Winner Identification

Find what's actually working:

| Winner Type | Signal | Action |
|------------|--------|--------|
| **Top-performing keywords** | Lowest CPA, highest conv rate | Increase bid, add variants |
| **Winning ads** | Highest CTR + conv rate combo | Scale spend, clone for other groups |
| **Best audiences** | Lowest CPA segment | Increase budget allocation |
| **Best times** | Peak conversion hours/days | Concentrate budget |

### 2D: Statistical Significance Check

For any A/B test (ad variants, audiences, landing pages):

```
Test: [Variant A] vs [Variant B]
Metric: [Conv Rate / CTR / CPA]
Variant A: [X%] (n=[sample_size])
Variant B: [Y%] (n=[sample_size])
Confidence level: [X%]
Verdict: [Statistically significant / Not enough data / Too close to call]
Recommended action: [Pick winner / Continue test / Increase budget to reach significance]
```

Minimum sample: 100 clicks per variant for CTR tests, 30 conversions per variant for CPA tests.

## Phase 3: Funnel Analysis

### Click → Conversion Path

```
Impressions: [N] (100%)
     ↓ CTR: [X%]
Clicks: [N] ([X%] of impressions)
     ↓ Landing page → Conversion: [X%]
Conversions: [N] ([X%] of clicks)
     ↓ Conversion → Revenue: $[X] avg
Revenue: $[N]
```

### Funnel Drop-Off Diagnosis

| Drop-Off Point | Rate | Benchmark | Likely Cause | Fix |
|----------------|------|-----------|-------------|-----|
| Impression → Click | [CTR%] | [Benchmark] | [Ad relevance / targeting] | [Copy/targeting change] |
| Click → Conversion | [Conv%] | [Benchmark] | [Landing page / offer / audience mismatch] | [LP optimization] |
| Conversion → Revenue | [Close%] | [Benchmark] | [Lead quality / sales process] | [Qualification criteria] |

## Phase 4: Output Format

```markdown
# Ad Campaign Analysis — [Product/Client] — [DATE]

Period: [Date range]
Total spend: $[X]
Platform(s): [Google / Meta / LinkedIn]
Primary goal: [Conversions / Revenue / Leads]

---

## Executive Summary

[3-5 sentences: Overall performance verdict, biggest win, biggest problem, top recommendation]

---

## Performance Dashboard

| Campaign | Spend | Impressions | Clicks | CTR | CPC | Conversions | CPA | ROAS | Verdict |
|----------|-------|------------|--------|-----|-----|-------------|-----|------|---------|
| [Name] | $[X] | [N] | [N] | [X%] | $[X] | [N] | $[X] | [X] | [Scale/Optimize/Pause] |

---

## Budget Waste Report

**Total estimated waste: $[X] ([X%] of total spend)**

### Wasted on zero-conversion items: $[X]
[List of keywords/ads/audiences with spend but no conversions]

### Wasted on high-CPA items: $[X]
[List of items with CPA > 3x target]

### Recommended saves: $[X]/month
[Specific items to pause]

---

## Winners to Scale

### Top Keywords/Audiences
| Item | CPA | Conv Rate | Current Spend | Recommended Spend |
|------|-----|----------|--------------|-------------------|

### Top Ads
| Ad | CTR | Conv Rate | Why It Works |
|----|-----|----------|-------------|

---

## A/B Test Results

### [Test Name]
- Variant A: [Metric] (n=[N])
- Variant B: [Metric] (n=[N])
- Confidence: [X%]
- **Verdict:** [Winner / Continue / Inconclusive]

---

## Action Plan

### Immediate (This Week)
- [ ] **Pause:** [Specific items — keywords, ads, audiences]
- [ ] **Scale:** [Specific items — increase budget/bids]
- [ ] **Add negatives:** [Specific keywords from search terms]

### This Month
- [ ] **Test:** [New ad angles / audiences / landing pages]
- [ ] **Restructure:** [Ad groups that need splitting or merging]
- [ ] **Optimize:** [Bid strategy changes]

### Next Month
- [ ] **Expand:** [New campaigns / channels to test]
- [ ] **Review:** [Run this analysis again]
```

Save to `clients/<client-name>/ads/campaign-analysis-[YYYY-MM-DD].md`.

## Cost

| Component | Cost |
|-----------|------|
| Data analysis | Free (LLM reasoning) |
| Statistical calculations | Free |
| **Total** | **Free** |

## Tools Required

- No external tools needed — pure reasoning skill
- User provides campaign data as CSV, paste, or screenshot

## Trigger Phrases

- "Analyze my ad campaign performance"
- "Which ads should I pause?"
- "Where am I wasting ad budget?"
- "Is my Google Ads campaign working?"
- "Optimize my Meta Ads spend"
