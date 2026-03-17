---
name: aarrr-metrics
description: Measure and optimize growth using the AARRR (Pirate Metrics) framework with stage-specific KPIs and funnel analysis
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# AARRR Pirate Metrics

> Apply Dave McClure's AARRR framework to measure and optimize growth through the five stages: Acquisition, Activation, Retention, Revenue, and Referral.

## When to Use This Skill

- Building growth dashboards
- Identifying funnel bottlenecks
- Prioritizing growth experiments
- Reporting to investors
- Diagnosing growth problems

## Methodology Foundation

Based on **Dave McClure's AARRR framework** (500 Startups), providing:
- Stage-specific metrics definition
- Funnel conversion analysis
- Prioritization framework
- Experiment design guidance

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Defines metrics per stage | Specific definitions for your product |
| Identifies bottlenecks | Experiment priorities |
| Suggests experiments | Resource allocation |
| Creates dashboards | Tool selection |
| Benchmarks performance | Acceptable thresholds |

## Instructions

### Step 1: Define Each Stage

**AARRR Stages:**

| Stage | Question | Focus |
|-------|----------|-------|
| **A**cquisition | How do users find you? | Traffic, channels |
| **A**ctivation | Do they have a great first experience? | Onboarding, aha moment |
| **R**etention | Do they come back? | Engagement, habit |
| **R**evenue | Do they pay? | Conversion, monetization |
| **R**eferral | Do they tell others? | Virality, NPS |

### Step 2: Set Stage-Specific Metrics

**Metrics Framework:**

| Stage | Primary Metric | Supporting Metrics |
|-------|----------------|-------------------|
| Acquisition | CAC, Unique visitors | Channel mix, CTR, CPM |
| Activation | Activation rate | Time to activate, drop-off points |
| Retention | D7/D30 retention | DAU/MAU, churn rate |
| Revenue | LTV, ARPU | Conversion rate, ACV |
| Referral | Viral coefficient | NPS, referral rate |

### Step 3: Map Your Funnel

**Funnel Template:**
```
Acquisition → Activation → Retention → Revenue → Referral
   100%    →    30%     →    15%    →    5%   →    1%
```

Calculate conversion rates between each stage.

### Step 4: Identify Bottlenecks

**Bottleneck Analysis:**
| Drop-off | Diagnosis |
|----------|-----------|
| Acquisition → Activation | Poor onboarding or wrong traffic |
| Activation → Retention | Not finding core value |
| Retention → Revenue | Pricing or value misalignment |
| Revenue → Referral | Not delighting paying users |

### Step 5: Prioritize Experiments

**ICE Framework:**
- **I**mpact: How much will it move the metric?
- **C**onfidence: How sure are we?
- **E**ase: How easy to implement?

## Examples

### Example 1: Complete AARRR Dashboard

**Input:**
```
Build an AARRR dashboard for a B2B SaaS product.
Monthly visitors: 50,000
Signups: 3,000
Activated users: 900
Paying customers: 150
Referrals generating signups: 45
```

**Output:**
```
## AARRR Dashboard: B2B SaaS

### Funnel Overview

```
┌──────────────────────────────────────────────────────────────┐
│                     AARRR FUNNEL                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ACQUISITION    ACTIVATION     RETENTION     REVENUE    REF │
│     50,000        3,000          900           150       45  │
│     100%          6%            30%           17%       30%  │
│                                                              │
│  ████████████  ████████        ████          ██         █   │
│                                                              │
│   Visitors   → Signups →    Activated →    Paid  → Referral │
│              (-94%)        (-70%)        (-83%)    (-70%)    │
│              ⚠️            ⚠️            ✅        ⚠️        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

### Stage-by-Stage Analysis

#### 1. ACQUISITION

**Metrics:**
| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| Monthly visitors | 50,000 | - | Baseline |
| Visitor → Signup | 6% | 2-5% | ✅ Good |
| CAC | $45 | <$50 | ✅ Good |
| Signups | 3,000 | - | - |

**Channel Breakdown:**
| Channel | Visitors | Signups | Conv % | CAC |
|---------|----------|---------|--------|-----|
| Organic | 20,000 | 1,500 | 7.5% | $0 |
| Paid Search | 15,000 | 900 | 6% | $60 |
| Content | 10,000 | 450 | 4.5% | $20 |
| Social | 5,000 | 150 | 3% | $80 |

**Analysis:** Acquisition is healthy. Organic performing best.
Paid social has high CAC—consider reallocating.

---

#### 2. ACTIVATION ⚠️ BOTTLENECK

**Metrics:**
| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| Signup → Activated | 30% | 40-60% | ⚠️ Below |
| Time to activate | 3.2 days | <1 day | ⚠️ Slow |
| Activation rate | 900/3,000 | - | - |

**Activation Definition:**
"Activated" = Created first project + invited 1 team member

**Drop-off Analysis:**
| Step | Users | Drop-off |
|------|-------|----------|
| Signup complete | 3,000 | - |
| Email verified | 2,400 | -20% |
| Created project | 1,500 | -38% |
| Invited team | 900 | -40% ⚠️ |

**Primary Bottleneck:** "Invite team member" step losing 40%

**Experiment Ideas:**
| Experiment | Hypothesis | ICE |
|------------|------------|-----|
| Skip team invite in onboarding | Removes friction, activate solo first | 8/8/9 = 8.3 |
| In-app invite prompt (day 2) | Right timing, after value seen | 7/7/8 = 7.3 |
| Email team invite reminder | Low effort, catches drop-offs | 5/6/9 = 6.7 |

---

#### 3. RETENTION

**Metrics:**
| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| Week 1 retention | 65% | 60%+ | ✅ Good |
| Month 1 retention | 45% | 40%+ | ✅ Good |
| DAU/MAU ratio | 28% | 20%+ | ✅ Good |
| Churn rate | 5%/month | <5% | ✅ OK |

**Retention Curve:**
```
Day 1:  100% ████████████████████
Day 7:   65% █████████████
Day 14:  52% ██████████
Day 30:  45% █████████
Day 60:  38% ████████
Day 90:  32% ██████
```

**Analysis:** Retention is solid. Users who activate tend to stick.
This confirms activation is the primary bottleneck.

---

#### 4. REVENUE

**Metrics:**
| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| Activated → Paid | 17% | 5-15% | ✅ Strong |
| Trial → Paid | 17% | 10-25% | ✅ Good |
| ARPU | $89/mo | - | Baseline |
| LTV | $1,068 | - | 12mo × ARPU |
| LTV:CAC | 24:1 | >3:1 | ✅ Excellent |

**Revenue Breakdown:**
| Plan | Customers | % | MRR |
|------|-----------|---|-----|
| Starter ($29) | 60 | 40% | $1,740 |
| Pro ($89) | 75 | 50% | $6,675 |
| Enterprise ($249) | 15 | 10% | $3,735 |
| **Total** | **150** | - | **$12,150** |

**Analysis:** Strong conversion and healthy LTV:CAC.
Not a bottleneck—maintain current approach.

---

#### 5. REFERRAL ⚠️ OPPORTUNITY

**Metrics:**
| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| Referral rate | 30% | 20%+ | ✅ Good |
| Viral coefficient | 0.45 | >1 = viral | ⚠️ Below |
| NPS | +32 | >30 | ✅ Good |
| Referral signups | 45 | - | - |

**Calculation:**
- 150 paying customers
- 30% refer (45 referrals)
- Each referral generates 1 signup
- Viral coefficient = 45/150 × (6% activation) = 0.018
- Not organic virality, but healthy referral base

**Experiment Ideas:**
| Experiment | Hypothesis | ICE |
|------------|------------|-----|
| Referral incentive (2-way) | Motivation for both parties | 7/8/7 = 7.3 |
| In-app share prompts | Right moment capture | 6/7/8 = 7.0 |
| Case study program | Social proof + referral | 5/6/6 = 5.7 |

---

### Priority Recommendations

| Priority | Focus | Current | Target | Impact |
|----------|-------|---------|--------|--------|
| 1 | Activation | 30% | 45% | +450 activated/mo |
| 2 | Referral | 30% | 50% | +30 referral signups |
| 3 | Paid channel mix | 6% conv | 8% conv | -$10 CAC |

**90-Day Goal:**
If activation improves 30% → 45%:
- +450 more activated users
- At 17% conversion = +76 new customers
- At $89 ARPU = +$6,800 MRR

---

### Dashboard Template

```
┌────────────────────────────────────────────────────────────┐
│  AARRR MONTHLY DASHBOARD                    January 2026   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ACQUISITION          ACTIVATION           RETENTION       │
│  Visitors: 50K        Activated: 900       D30: 45%       │
│  Signups: 3K          Rate: 30% ⚠️        Churn: 5%      │
│  CAC: $45             Time: 3.2d          DAU/MAU: 28%   │
│                                                            │
│  REVENUE              REFERRAL             OVERALL         │
│  Customers: 150       Referrals: 45        MRR: $12.2K    │
│  Conv: 17%            Rate: 30%            LTV:CAC: 24:1  │
│  ARPU: $89            NPS: +32             Health: 🟢     │
│                                                            │
│  BOTTLENECK: Activation (30% vs 45% target)               │
│  EXPERIMENT: Skip team invite onboarding                   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```
```

### Example 2: Quick Bottleneck Diagnosis

**Input:**
```
Diagnose this funnel:
- 100K visitors, 5K signups (5%)
- 4K activated (80%)
- 1K retained at D30 (25%)
- 200 paid (20%)
```

**Output:**
```
## Quick AARRR Diagnosis

### Funnel

| Stage | Users | Conv | Benchmark | Status |
|-------|-------|------|-----------|--------|
| Acquisition | 100K → 5K | 5% | 2-5% | ✅ Good |
| Activation | 5K → 4K | 80% | 40-60% | ✅ Excellent |
| Retention | 4K → 1K | 25% | 40%+ | ❌ Problem |
| Revenue | 1K → 200 | 20% | 5-15% | ✅ Strong |

### Bottleneck: RETENTION

**Problem:** Only 25% retained at D30 (should be 40%+)

**What this means:**
- Great at attracting and activating
- Users try it, find value initially
- But don't form a habit / come back
- Losing 3,000 activated users monthly

**Likely Causes:**
1. Single-use case (solved problem, left)
2. Not enough ongoing value
3. Poor re-engagement
4. Competitor switching

**Recommended Experiments:**
1. User interviews with churned users
2. Email re-engagement sequence
3. Weekly value summary email
4. Add recurring use case

**Impact if fixed:**
If retention → 40%: 1,600 retained → 320 paid
That's +120 customers/month (+60%)
```

## Skill Boundaries

### What This Skill Does Well
- Structuring growth metrics
- Identifying funnel bottlenecks
- Prioritizing experiments
- Creating dashboards

### What This Skill Cannot Do
- Access your actual data
- Know your specific definitions
- Run experiments
- Guarantee results

## Iteration Guide

**Follow-up Prompts:**
- "Design activation experiments for [problem]"
- "What metrics matter for [stage]?"
- "Create a retention analysis framework"
- "How do we improve [specific conversion]?"

## References

- Dave McClure - Pirate Metrics (500 Startups)
- Reforge Growth Series
- Amplitude Product Analytics
- Mixpanel Growth Framework

## Related Skills

- `product-led-growth` - PLG motions
- `growth-loops` - Sustainable growth
- `startup-metrics` - Investor metrics

## Skill Metadata

- **Domain**: Growth
- **Complexity**: Intermediate
- **Mode**: cyborg
- **Time to Value**: 2-3 hours for full setup
- **Prerequisites**: Analytics access, metric definitions
