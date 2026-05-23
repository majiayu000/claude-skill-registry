---
name: prd-v09-launch-metrics
description: >
  Define success criteria and tracking setup for launch during PRD v0.9 Go-to-Market.
  Triggers on requests to define launch metrics, set up tracking, or when user asks "how do we measure launch success?",
  "launch KPIs", "tracking setup", "success criteria", "analytics", "launch goals".
  Outputs KPI- entries specialized for launch measurement.
---

# Launch Metrics

Position in workflow: v0.9 GTM Strategy → **v0.9 Launch Metrics** → v0.9 Feedback Loop Setup

## Purpose

Define how launch success is measured—specific metrics, targets, tracking infrastructure, and the dashboards that make progress visible.

## Core Concept: Metrics as North Star

> Launch metrics are not vanity numbers—they are **decision criteria**. Each metric should answer: "Is this working? Should we double down or pivot?" If a metric doesn't inform action, don't track it.

## Metric Layers for Launch

| Layer | What to Measure | Timeframe |
|-------|-----------------|-----------|
| **Reach** | How many saw us | Day 0-7 |
| **Acquisition** | How many signed up | Day 0-30 |
| **Activation** | How many got value | Day 1-14 |
| **Retention** | How many came back | Week 2-4 |
| **Revenue** | How many paid | Week 2-8 |
| **Referral** | How many shared | Week 3+ |

## Execution

1. **Review v0.3 Outcome Definition KPIs**
   - What KPI- entries exist from v0.3?
   - Which are most relevant for launch?
   - What launch-specific metrics are needed?

2. **Define launch-specific metrics**
   - Channel performance (per GTM-)
   - Funnel progression
   - Activation milestones
   - Early retention signals

3. **Set targets per timeframe**
   - Day 1, Day 7, Day 30, Day 90
   - Tie to product type expectations (from v0.2 BR-)

4. **Configure tracking infrastructure**
   - Analytics platforms
   - Event schemas
   - Dashboard setup

5. **Create visibility**
   - Daily launch dashboard
   - Weekly metrics review
   - Automated alerts for thresholds

6. **Create/Update KPI- entries** for launch

## KPI- Output Template (Launch Variant)

```
KPI-XXX: [Launch Metric Name]
Tier: [Tier 1 | Tier 2 | Tier 3]
Category: [Reach | Acquisition | Activation | Retention | Revenue | Referral]
Stage: Launch (v0.9)
Owner: [Who monitors this metric]

Definition: [Exact calculation formula]
Unit: [count | percentage | currency | ratio]
Source: [Where data comes from]

Targets:
  Day 1: [target]
  Day 7: [target]
  Day 30: [target]
  Day 90: [target]

Evidence: [CFD-XXX or benchmark that justifies targets]
Product Type Calibration: [How product type affects expectations]

Tracking:
  Event: [analytics event name if applicable]
  Dashboard: [Where to view this metric]
  Alert: [When to get notified]

Action Thresholds:
  Red: [Below this = urgent intervention]
  Yellow: [Below this = investigate]
  Green: [Above this = on track]

GTM Connection: [GTM-XXX channels this measures]
v0.3 KPI Link: [KPI-YYY from Outcome Definition if applicable]
```

**Example KPI- entries:**

```
KPI-101: Website Visitors (Launch Week)
Tier: Tier 3 (Leading)
Category: Reach
Stage: Launch (v0.9)
Owner: Growth Team

Definition: Unique visitors to marketing site
Unit: count
Source: Google Analytics / Plausible

Targets:
  Day 1: 5,000
  Day 7: 25,000
  Day 30: 50,000
  Day 90: 100,000

Evidence: CFD-025 (competitor launch benchmarks)
Product Type Calibration: Fast Follow = higher baseline expected

Tracking:
  Event: page_view (landing pages)
  Dashboard: Launch Dashboard > Reach panel
  Alert: <1,000 on Day 1

Action Thresholds:
  Red: <2,500 Day 7 (50% of target)
  Yellow: <20,000 Day 7 (80% of target)
  Green: >25,000 Day 7

GTM Connection: GTM-002 (Product Hunt), GTM-007 (Website)
v0.3 KPI Link: N/A (launch-specific)
```

```
KPI-102: Trial Signups
Tier: Tier 2 (Conversion)
Category: Acquisition
Stage: Launch (v0.9)
Owner: Product Team

Definition: Completed signup flow (email verified)
Unit: count
Source: Application database + Mixpanel

Targets:
  Day 1: 500
  Day 7: 2,000
  Day 30: 5,000
  Day 90: 15,000

Evidence: CFD-030 (industry signup rate benchmarks 5-10%)
Product Type Calibration: Fast Follow = 8-10% expected conversion

Tracking:
  Event: signup_completed
  Dashboard: Launch Dashboard > Acquisition panel
  Alert: Conversion rate <5%

Action Thresholds:
  Red: <100 Day 1 (messaging/channel mismatch)
  Yellow: <400 Day 1 (funnel friction)
  Green: >500 Day 1

GTM Connection: GTM-002, GTM-004 (Landing Page)
v0.3 KPI Link: KPI-001 (Trial Signups, general)
```

```
KPI-103: Activation Rate (First Value)
Tier: Tier 1 (Critical)
Category: Activation
Stage: Launch (v0.9)
Owner: Product Team

Definition: % of signups who complete first value action within 24h
Unit: percentage
Source: Mixpanel + Application events

First Value Action: Complete first [core action - e.g., generate code suggestion]

Targets:
  Day 1: 40%
  Day 7: 45%
  Day 30: 50%
  Day 90: 55%

Evidence: CFD-035 (activation benchmarks for dev tools 30-50%)
Product Type Calibration: Fast Follow = higher baseline (users know the category)

Tracking:
  Event: first_value_achieved
  Dashboard: Launch Dashboard > Activation panel
  Alert: Drops below 30%

Action Thresholds:
  Red: <25% (onboarding broken)
  Yellow: <35% (friction points)
  Green: >45%

GTM Connection: Measures effectiveness of all GTM- channels
v0.3 KPI Link: KPI-002 (Activation Rate, general)
```

```
KPI-104: Day 7 Retention
Tier: Tier 1 (Critical)
Category: Retention
Stage: Launch (v0.9)
Owner: Product Team

Definition: % of Day 0 signups who return on Day 7
Unit: percentage
Source: Mixpanel cohort analysis

Targets:
  Day 7: 25%
  Day 30: 20% (of Day 0)
  Day 90: 15% (of Day 0)

Evidence: CFD-040 (B2B SaaS retention benchmarks)
Product Type Calibration: Fast Follow = retention critical (easy to switch back)

Tracking:
  Event: session_start (Day 7 cohort)
  Dashboard: Launch Dashboard > Retention panel
  Alert: Day 7 retention <15%

Action Thresholds:
  Red: <15% (critical product-market fit issue)
  Yellow: <20% (value delivery problem)
  Green: >30% (strong PMF signal)

GTM Connection: Quality indicator for all GTM- traffic
v0.3 KPI Link: KPI-003 (Retention Rate, general)
```

## The Launch Funnel

Track conversion at each stage:

```
REACH → ACQUISITION → ACTIVATION → RETENTION → REVENUE → REFERRAL
 100%      10%           50%          25%        20%       10%
```

| Stage | Key Metric | Benchmark |
|-------|------------|-----------|
| Reach → Acquisition | Signup Rate | 5-15% |
| Acquisition → Activation | Activation Rate | 30-60% |
| Activation → Retention | D7 Retention | 20-40% |
| Retention → Revenue | Conversion Rate | 2-10% |
| Revenue → Referral | NPS / Referral Rate | 10-30% |

## Product Type Calibration

Expectations vary by product type (from v0.2 BR-):

| Product Type | Acquisition | Activation | Retention | Revenue |
|--------------|-------------|------------|-----------|---------|
| **Fast Follow** | High (known category) | High (familiar UX) | Medium (easy to switch) | Quick |
| **Slice** | Medium (niche) | High (focused value) | High (workflow fit) | Medium |
| **Innovation** | Low (education needed) | Low (learning curve) | High (if activated) | Slow |

## Tracking Infrastructure Checklist

| Component | Purpose | Tool Examples |
|-----------|---------|---------------|
| **Product Analytics** | User behavior | Mixpanel, Amplitude, PostHog |
| **Web Analytics** | Traffic, sources | GA4, Plausible, Fathom |
| **Event Tracking** | Specific actions | Segment, custom events |
| **Error Tracking** | Failures, issues | Sentry, LogRocket |
| **Session Recording** | User experience | Hotjar, FullStory |
| **A/B Testing** | Experiments | LaunchDarkly, Statsig |

## Event Schema for Launch

Define standard events for launch tracking:

```
# Acquisition Events
signup_started: { source, campaign, referrer }
signup_completed: { source, campaign, user_id }
signup_abandoned: { step, source, reason }

# Activation Events
onboarding_started: { user_id }
onboarding_step_completed: { user_id, step }
first_value_achieved: { user_id, action, time_to_value }

# Engagement Events
feature_used: { user_id, feature, context }
session_start: { user_id, day_number }
session_end: { user_id, duration }

# Conversion Events
upgrade_started: { user_id, plan }
payment_completed: { user_id, plan, amount }
```

## Launch Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│ LAUNCH DASHBOARD                    Last updated: [time]    │
├─────────────────────────────────────────────────────────────┤
│ REACH          │ ACQUISITION     │ ACTIVATION              │
│ Visitors: X    │ Signups: Y      │ Activated: Z%           │
│ Target: X      │ Target: Y       │ Target: Z%              │
│ [trend chart]  │ [trend chart]   │ [trend chart]           │
├─────────────────────────────────────────────────────────────┤
│ RETENTION      │ REVENUE         │ CHANNELS                │
│ D7: X%         │ MRR: $Y         │ Product Hunt: X         │
│ Target: X%     │ Target: $Y      │ Direct: Y               │
│ [cohort chart] │ [revenue chart] │ [breakdown chart]       │
└─────────────────────────────────────────────────────────────┘
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Vanity metrics only** | Tracking visitors but not activation | Focus on funnel progression |
| **No targets** | "We got 1000 signups!" (is that good?) | Set explicit targets per timeframe |
| **Lagging only** | Only tracking revenue | Add leading indicators (activation) |
| **No action thresholds** | Metrics exist but no response plan | Define red/yellow/green zones |
| **Over-instrumentation** | 200 events, can't find signal | Focus on 10-15 key events |
| **No attribution** | Don't know which channel works | Track source for all signups |

## Quality Gates

Before proceeding to Feedback Loop Setup:

- [ ] Launch funnel metrics defined (Reach → Referral)
- [ ] Targets set for Day 1, Day 7, Day 30
- [ ] Tracking infrastructure configured
- [ ] Launch dashboard created and accessible
- [ ] Action thresholds defined for critical metrics
- [ ] KPI- entries link to GTM- channels
- [ ] Product type calibration applied to targets

## Downstream Connections

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **Feedback Loop Setup** | KPI- thresholds trigger feedback collection | KPI-103 <30% → investigate with CFD- |
| **Daily Standup** | KPI- dashboard for launch status | "Activation at 42%, on track" |
| **Pivot Decisions** | KPI- data informs strategy | KPI-104 <15% → fundamental problem |
| **Investor Updates** | KPI- for launch performance | "Day 30: 5000 signups, 45% activated" |
| **v1.0 Planning** | KPI- baselines for growth targets | KPI-102 baseline → 10% MoM growth |

## Detailed References

- **Metric definition examples**: See `references/metric-examples.md`
- **KPI- entry template**: See `assets/kpi-launch-template.md`
- **Dashboard design guide**: See `references/dashboard-design.md`
- **Event schema examples**: See `references/event-schema.md`
