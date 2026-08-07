---
name: pm-metrics
description: Делает ревью продуктовых метрик — тренды, аномалии, root causes и рекомендации к действиям. Включает декомпозицию North Star (L1/L2), диагностику retention-кривых, анализ воронки, разбор A/B-экспериментов, проверку соответствия OKR и фреймворк атрибуции аномалий. User-invoked only — do NOT auto-trigger. Triggers on /pm-metrics, "обзор метрик", "разбор воронки", "анализ удержания", "ретеншн", "A/B результаты", "review metrics", "DAU analysis", "retention analysis", "funnel analysis", "metric anomaly".
---

# pm-metrics — Product metrics review


Part of the Personal Corp framework — running a one-person business through AI agents.
Systematically review product metrics, identify trend changes, locate root causes, output action recommendations. Includes North Star decomposition, retention diagnostics, funnel methodology, and A/B experiment reading.

## Inputs

| Field | Required | Notes |
|---|---|---|
| Metric data | yes | Excel / CSV / pasted table / verbal description |
| Cycle | no | Weekly / monthly / quarterly review; default weekly |
| Focus | no | Full review / single-metric anomaly / experiment readout |
| Business context | no | Releases, campaigns, incidents in the period |

**Mode:** full data → complete review; single-metric change → focused anomaly analysis.

## Step 1 — Data integrity check

- Confirm time coverage (current vs comparison period)
- Confirm metric coverage (which North Star / L1 / L2 are present)
- Flag missing critical data

## Step 2 — North Star metric system

**Decomposition:** North Star → L1 → L2.

**L1 dimensions:**
- **User growth:** DAU/WAU/MAU, new, returning
- **User engagement:** core action frequency, session length, feature reach
- **User retention:** D1 / D7 / D30
- **Conversion efficiency:** signup → activation → paid step-by-step rates
- **Business value:** paid rate, ARPU, LTV
- **Satisfaction:** NPS, complaint rate, ratings

**North Star selection guide:**

| Product type | Recommended NSM | Typical L1 |
|---|---|---|
| Social / community | Weekly active posters | DAU/MAU ratio, interactions per user, D7 retention |
| Tools / productivity | Weekly users completing core task | Task completion rate, frequency, feature reach |
| E-commerce | Weekly transacting users | GMV, AOV, repeat rate, conversion |
| Content / media | Weekly content-consumption time | Time per user, completion rate, return rate |
| SaaS / B2B | Weekly active teams | Team penetration, feature depth, renewal rate |

## Step 3 — Growth metric analysis

**Definitions:**
- **DAU:** distinct users with valid action that day
- **WAU:** distinct users active ≥ 1 day in 7
- **MAU:** distinct users active ≥ 1 day in 30
- **DAU/MAU ratio (stickiness):** > 0.5 very high, 0.3-0.5 high, 0.2-0.3 medium, < 0.2 low

**User segmentation:**

| Type | Definition | Focus |
|---|---|---|
| **New** | First-time user | Channel quality, activation rate |
| **Active retained** | Active in both periods | Depth, feature reach |
| **Returning** | Inactive last period, active this | Return reason, secondary retention |
| **Churned** | Active last period, inactive this | Churn cause, win-back potential |
| **Dormant** | Inactive multiple periods | Possibly permanent loss |

**Growth identity:** This-period MAU = prev-period retained + new + returning − churned

## Step 4 — Retention analysis

**Definitions:**
- **D1:** % of new users who return on day 2
- **D7:** % of new users who return on day 8
- **D30:** % of new users who return on day 31

**Retention benchmarks:**

| Product type | D1 | D7 | D30 | Note |
|---|---|---|---|---|
| Social / messaging | > 70% | > 50% | > 35% | High-frequency essential |
| Tools | > 40% | > 25% | > 15% | "Use and leave" pattern |
| Content / news | > 35% | > 20% | > 10% | Many alternatives, lower retention |
| E-commerce | > 25% | > 15% | > 8% | Low-frequency, watch repeat rate instead |
| Games | > 40% | > 20% | > 10% | High variance by genre |
| SaaS / B2B | > 60% | > 45% | > 30% | High switching cost, higher baseline |

**Retention-curve diagnosis:**
- **Steep drop** (D1 → D7 loses > 60%): activation experience broken — users didn't find value
- **Slow decay** (D7 → D30 keeps falling, doesn't level): no long-term hook
- **L-shape** (levels off after D7): healthy, core user base formed
- **Bounce-back** (sudden uptick on a specific day): cyclical use pattern (e.g. weekday-only)

**Retention segmentation:**
- By channel: organic vs paid retention gap
- By behavior: completed activation vs not
- By cohort month: compare month-over-month curves to gauge product improvement

## Step 5 — Conversion funnel analysis

**Funnel construction:**
1. Define start and end points (e.g. homepage visit → payment success)
2. Split into key intermediate steps (each step = a user decision point)
3. Per-step rate = arriving at next / arriving at this

**Funnel framework:**

| Step | Action | Output |
|---|---|---|
| **Draw** | List steps + rates | Full funnel view |
| **Identify bottleneck** | Find lowest-rate step | Optimization focus |
| **Benchmark** | Compare history / industry / competitor | Gap quantification |
| **Segment** | By channel / device / user type | Locate problem cohort |
| **Hypothesize** | Why is the bottleneck there? | Optimization direction |
| **Experiment** | Propose A/B test | Action plan |

**Common funnels:**
- **Acquisition:** impression → click → install/signup → activation
- **Activation:** signup → onboarding done → core action first-trigger
- **Payment:** browse → cart → order → pay success
- **Sharing:** trigger → share click → recipient open → recipient conversion

## Step 6 — A/B experiment readout

| Dimension | Standard | Note |
|---|---|---|
| **Statistical significance** | p < 0.05 | p > 0.05 → inconclusive, don't decide |
| **Effect size** | Lift > MDE | Significant but tiny lift may not be worth it |
| **Sample size** | Reaches pre-set N | "Significant" without N is unreliable |
| **Duration** | Covers ≥ 1-2 full weeks | Avoid weekday/weekend bias |
| **AA check** | Pre-period baselines match | Mismatch → split assignment is broken |

**Decision framework:**
- Significant + large effect → ship to all
- Significant + small effect → weigh long-term value vs cost
- Not significant → don't ship; investigate (wrong hypothesis? sample? execution?)
- Metric conflict (A up, B down) → weigh, prioritize North Star

**Common pitfalls:**
- Reading results too early (before reaching N)
- Looking only at primary metric, not guardrails
- Multiple peeks → false positives
- Ignoring novelty effect (early data inflated)

## Step 7 — OKR alignment check

| Check | Healthy | Anomaly signal |
|---|---|---|
| **Coverage** | Every KR has ≥ 1 trackable metric | A KR with no measurable proxy |
| **Consistency** | Metric direction matches KR target | Metric up but KR no progress |
| **Pacing** | Linear pacing ≥ 50% by mid-quarter | Severely behind schedule |
| **Attribution** | Metric movement attributable to team action | Metric improved due to industry tailwind, not team |

**OKR progress table:**

| OKR | KR metric | Target | Current | Progress % | Trend | Risk |
|---|---|---|---|---|---|---|
| {O1} | {KR1} | {target} | {current} | {X%} | Up/flat/down | On-track / at-risk / severe |

## Step 8 — Anomaly attribution

When a metric moves anomalously, work the framework:

1. **Quantify:** how much, starting when?
2. **Decompose:** segment by channel / region / version / cohort to localize
3. **Time-align:** what happened around the inflection? (release, campaign, incident, competitor move)
4. **Eliminate:** rule out causes one by one until the most likely root remains
5. **Cross-check:** verify the attribution via other metrics

**Common causes:**

| Category | Pattern | Verification |
|---|---|---|
| Release | Inflection aligns with deploy time | Compare per-version |
| Campaign | Up during campaign, drops after | Compare per-channel |
| Tech incident | Sudden drop + recovery | Check error logs and uptime |
| External | Industry-wide change | Compare with competitor / industry data |
| Channel mix | One channel changed dramatically | Per-channel decomposition |
| Seasonality | Same as YoY | Look at last year's same period |

## Step 9 — Generate review report

```markdown
# Product Metrics Review

**Period:** {date range}
**Product:** {name}
**Type:** {weekly / monthly / quarterly}

## 1. Health Overview
| Layer | Metric | Current | Previous | MoM | Target | Status |
|---|---|---|---|---|---|---|
| North Star | {} | {} | {} | {±X%} | {} | OK / warn / alert |
| L1 | {} | {} | {} | {±X%} | {} | OK / warn / alert |

**Overall judgment:** {one-sentence summary}

## 2. User Growth
- DAU: {value}, MoM {change}
- MAU: {value}, DAU/MAU = {stickiness}
- Composition: new {X}% / retained {Y}% / returning {Z}%

## 3. Retention
| Metric | Current | Previous | Benchmark | Assessment |
|---|---|---|---|---|

## 4. Funnel
| Step | Users | Rate | MoM | Bottleneck? |
|---|---|---|---|---|

**Bottleneck diagnosis:** {description}

## 5. Experiments / Feature Effects
| Experiment | Primary metric Δ | Significance | Conclusion |
|---|---|---|---|

## 6. OKR Progress
| KR | Target | Current | Progress | Risk |
|---|---|---|---|---|

## 7. Anomaly Attribution
| Anomaly | Magnitude | Start | Attribution | Confidence |
|---|---|---|---|---|

## 8. Key Insights
1. {insight 1: finding + data + meaning}
2. {insight 2}
3. {insight 3}

## 9. Action Recommendations
| Priority | Action | Linked metric | Expected impact | Owner |
|---|---|---|---|---|
```

## Review cadence

| Type | Frequency | Time | Audience | Focus |
|---|---|---|---|---|
| **Weekly** | Every Monday | 15-30 min | PM | NSM + anomalies + experiments |
| **Monthly** | Month start | 30-60 min | Product team | All L1 + retention + funnel + OKR pacing |
| **Quarterly** | Quarter end | 60-90 min | Product + ops + eng | Strategy review + OKR scoring + next-quarter plan |

## Quality bar

1. Metric definitions clear — every metric has a calculation note
2. Data has comparisons — current always compared to previous, YoY, or target
3. Attribution evidenced — no causation from correlation alone
4. Recommendations actionable — owner-assignable
5. Limitations tagged — call out small samples or data quality issues

## Common analysis pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| **Simpson's paradox** | Total goes up while every segment goes down | Always segment, never just look at totals |
| **Survivorship bias** | Only retained users analyzed, churned ignored | Compare retained vs churned behavior |
| **Vanity metric** | Cumulative signups only ever grow, not decision-useful | Use active metrics (DAU/WAU) instead |
| **Time-window trap** | Comparison window happens to be an outlier | Cross-validate across multiple windows |
| **Goodhart's law** | Target becomes a metric, stops measuring well | Set guardrails to prevent gaming |

## Red lines

1. **No fabricated data** — missing data → tag "missing", don't extrapolate
2. **Don't conflate correlation with causation** — attribution must say "highly correlated" or "confirmed causal"
3. **Don't over-read small swings** — small fluctuation → tag "within normal noise"
4. **Don't ignore negatives** — flag risks even when overall is up

## When input is incomplete

- **Single metric only** → focus on that anomaly, no full review
- **No history** → snapshot only, tag "no baseline, recommend establishing tracking"
- **Verbal description** → analyze based on description, tag "recommend exact data for verification"
- **No targets** → use industry benchmarks, suggest team set explicit targets

## Related skills

- `/pm-feedback` — pair quantitative anomaly with qualitative voice-of-customer
- `/pm-prioritize` — adjust priority based on metric findings
- `/pm-roadmap` — adjust roadmap based on OKR pacing

