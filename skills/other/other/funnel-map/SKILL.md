---
name: funnel-map
description: Map complete funnel from ad to conversion, documenting each step, identifying metrics at each stage, calculating stage-to-stage conversion rates, and highlighting biggest drop-off points. Use for funnel optimization, diagnosing conversion issues, or documenting funnel architecture.
---

# Funnel Map

Document and analyze complete conversion funnels.

## Process

### Step 1: Document Each Funnel Step

**Standard Funnel Elements:**
1. Ad (Creative)
2. Landing Page / Pre-sell
3. Quiz (if applicable)
4. Sales Page / VSL
5. Checkout / Lead Form
6. Upsells (if applicable)
7. Thank You / Confirmation

**For Each Step Document:**
- URL/asset name
- Purpose in funnel
- Key message
- Primary CTA
- Technical requirements

### Step 2: Identify Metrics at Each Stage

**Ad Level:**
- Impressions
- Clicks
- CTR
- CPC
- CPM

**Landing/Quiz Level:**
- Page views
- Time on page
- Scroll depth
- Quiz completion rate
- Exit rate

**Conversion Level:**
- Add to cart / Initiate checkout
- Form submissions
- Purchase/conversion
- Upsell acceptance rate

### Step 3: Calculate Stage-to-Stage Rates

**Conversion Rate Formula:**
Stage N Conversion = (Stage N Actions / Stage N-1 Actions) × 100

**Example Flow:**
```
1000 Ad Clicks
  → 800 Land on Page (80% click-to-land)
    → 400 Start Quiz (50% page-to-quiz)
      → 280 Complete Quiz (70% quiz completion)
        → 140 View Offer (50% quiz-to-offer)
          → 28 Purchase (20% offer-to-purchase)

Overall: 28/1000 = 2.8% click-to-purchase
```

### Step 4: Highlight Drop-off Points

**Identify Biggest Leaks:**
- Which stage has lowest conversion rate?
- Which stage loses most absolute volume?
- Which stage is below industry benchmark?

**Prioritize by Impact:**
Impact = Volume at stage × Potential improvement %

### Step 5: Output Funnel Visualization

```
## FUNNEL MAP: [Offer/Campaign Name]

### FUNNEL OVERVIEW

**Type:** [Lead Gen / E-commerce / VSL / Quiz]
**Total Steps:** [#]
**End Goal:** [Purchase / Lead / Call]

---

### FUNNEL VISUALIZATION

```
┌─────────────────┐
│   AD CREATIVE   │ Impressions: [X]
│    CTR: X%      │ Clicks: [X]
└────────┬────────┘
         │ [X%] click-to-land
         ▼
┌─────────────────┐
│  LANDING PAGE   │ Views: [X]
│   Time: Xs      │ Bounce: [X%]
└────────┬────────┘
         │ [X%] page-to-next
         ▼
┌─────────────────┐
│     QUIZ        │ Starts: [X]
│  Complete: X%   │ Completes: [X]
└────────┬────────┘
         │ [X%] quiz-to-offer
         ▼
┌─────────────────┐
│  SALES PAGE     │ Views: [X]
│   VSL: X%       │ Watch: [X%]
└────────┬────────┘
         │ [X%] page-to-checkout
         ▼
┌─────────────────┐
│   CHECKOUT      │ Initiates: [X]
│                 │ Completes: [X]
└────────┬────────┘
         │ [X%] checkout completion
         ▼
┌─────────────────┐
│   CONVERSION    │ Total: [X]
│   CPA: $X       │ Revenue: $[X]
└─────────────────┘
```

---

### METRICS BY STAGE

| Stage | In | Out | Rate | Benchmark | Status |
|-------|-----|-----|------|-----------|--------|
| Ad → Click | [X] imp | [X] click | [X%] CTR | [X%] | [G/Y/R] |
| Click → Land | [X] click | [X] land | [X%] | 90%+ | [G/Y/R] |
| Land → Quiz | [X] land | [X] start | [X%] | 50%+ | [G/Y/R] |
| Quiz Completion | [X] start | [X] done | [X%] | 70%+ | [G/Y/R] |
| Quiz → Offer | [X] done | [X] view | [X%] | 80%+ | [G/Y/R] |
| Offer → Checkout | [X] view | [X] init | [X%] | 10-20% | [G/Y/R] |
| Checkout Complete | [X] init | [X] buy | [X%] | 30%+ | [G/Y/R] |

**Overall Funnel:**
- Click to Conversion: [X%]
- Cost Per Conversion: $[X]
- Revenue Per Click: $[X]

---

### DROP-OFF ANALYSIS

**Biggest Leak:** [Stage Name]
- Current rate: [X%]
- Benchmark: [X%]
- Gap: [X points]
- Volume lost: [X potential conversions]
- Revenue impact: $[X]

**Root Cause Analysis:**
- [Possible reason 1]
- [Possible reason 2]
- [Possible reason 3]

---

### STAGE DETAILS

**STAGE 1: Ad Creative**
- Asset: [Description]
- Metrics: CTR [X%], CPC $[X]
- Status: [Working/Needs work]
- Notes: [Observations]

**STAGE 2: Landing Page**
- URL: [Link]
- Purpose: [What it does]
- Metrics: [Key stats]
- Status: [Working/Needs work]
- Issues: [If any]

**STAGE 3: [Next Stage]**
...

---

### OPTIMIZATION PRIORITIES

**Priority 1: [Stage with biggest impact]**
- Current: [X%]
- Target: [X%]
- Actions:
  1. [Specific improvement]
  2. [Specific improvement]
- Expected lift: [X%]
- Revenue impact: $[X]

**Priority 2: [Next biggest opportunity]**
...

---

### A/B TEST ROADMAP

| Stage | Test | Control | Variant | Hypothesis |
|-------|------|---------|---------|------------|
| [Stage] | [Element] | [Current] | [New] | [Expected] |

---

### BENCHMARK COMPARISON

| Metric | Our Funnel | Industry | Gap |
|--------|------------|----------|-----|
| CTR | [X%] | [X%] | [+/-] |
| Land-to-Lead | [X%] | [X%] | [+/-] |
| Checkout Rate | [X%] | [X%] | [+/-] |
| Overall CVR | [X%] | [X%] | [+/-] |

---

### FUNNEL HEALTH SCORE

| Factor | Score | Weight | Weighted |
|--------|-------|--------|----------|
| Traffic Quality | X/10 | 20% | X |
| Page Performance | X/10 | 25% | X |
| Offer Strength | X/10 | 30% | X |
| Checkout Flow | X/10 | 25% | X |
| **TOTAL** | | | X/10 |

---

### ACTION ITEMS

**Immediate:**
1. [ ] [Action]
2. [ ] [Action]

**This Week:**
1. [ ] [Action]

**This Month:**
1. [ ] [Action]
```

## Funnel Optimization Principles

**Fix Biggest Leaks First:**
- Largest volume × lowest rate = priority
- Small improvements at scale = big impact

**Test One Variable at a Time:**
- Isolate changes
- Measure impact clearly
- Build on winners

**Metrics Hierarchy (Jason K):**
- Initiate checkout = 3x purchase data
- Use leading indicators for faster decisions

Source: Jason K, general funnel optimization
