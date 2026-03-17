---
name: judgment-postmortem-calibration
description: "Build VC judgment faster through structured postmortems with quantified calibration: log initial takes, track prediction accuracy with Brier scores, and measure learning rate over time. Use after decisions, passes, and major diligence sprints."
license: Proprietary
compatibility: Works offline; improved with longitudinal tracking; optional Salesforce logging.
metadata:
  author: evalops
  version: "0.3"
---
# Judgment postmortem calibration

## When to use
Use this skill when you want to:
- Improve selection judgment (faster learning, fewer repeated mistakes)
- Capture why you said yes/no and how evidence changed your view
- **Measure your prediction accuracy and learning rate over time**
- Build an internal "decision log" that compounds
- Review investments or passes after outcomes are known

**Trigger points:**
- After every IC decision (invest or pass)
- After every competitive loss
- Quarterly: review passes that raised from others + calculate calibration metrics
- Annually: review portfolio outcomes vs initial thesis + measure learning rate

## Inputs you should request (only if missing)
- Deal name + date of first meeting
- Your initial take (reconstruct honestly if not documented)
- Outcome to date (funded by others? traction? pivot? shut down?)
- Original memo or notes (if available)
- **Your probability estimates at decision time (if recorded)**

## Outputs you must produce
1) **Decision log entry** (structured, one page)
2) **Calibration scorecard** (predictions vs reality with scores)
3) **Brier score calculation** (for probabilistic predictions)
4) **Updated heuristics** (2-5 actionable bullets)
5) **Pattern library update** (what archetype was this?)
6) **Learning rate metrics** (are you getting better?)
7) **Follow-up list** (who to ping, what to track)

Templates:
- assets/decision-log.md
- assets/calibration-tracker.csv (for longitudinal tracking)

## Core principle: Measure what you believe, then score it

The value of postmortems comes from:
1. **Honest recording** of what you believed at decision time
2. **Quantified predictions** (probabilities, not just "I thought X")
3. **Systematic scoring** against outcomes
4. **Tracking improvement** over time

## Procedure

### 1) Capture the timeline with predictions
| Date | Event | Your belief | Confidence (%) | Outcome |
|---|---|---|---|---|
| First meeting | "This will be a $1B+ outcome" | 20% | |
| First meeting | "Product-market fit within 12 months" | 60% | |
| Diligence | "They'll close 3 enterprise deals in 6 months" | 40% | |
| Decision | "Worth investing" | 70% | |
| +12 months | | | Actual outcome |

### 2) Record the initial thesis with probabilities

**At first meeting, I believed:**
- What would make the company win:
- P(success | investment) estimate: ___% 
- P(this raises next round) estimate: ___%
- P(achieves stated 12-month milestones) estimate: ___%
- Top risk and P(risk materializes): ___% 
- My recommendation:

**At decision point, I believed:**
- P(success | investment): ___%
- P(raises next round): ___%
- Top risks with probabilities:
  1. Risk: ___ | P(materializes): ___%
  2. Risk: ___ | P(materializes): ___%
- Final recommendation:

### 3) Document the decision
- **Decision:** Invest / Pass / Lost competitive
- **Stated rationale (at the time):**
- **Unstated factors (be honest):**
- **Confidence in decision:** ___%

### 4) Score predictions against reality

**Prediction scorecard:**
| Prediction | Your P(true) | Actual (1/0) | Brier contribution |
|---|---|---|---|
| "This will raise Series A" | 70% | 1 (yes) | (0.7-1)² = 0.09 |
| "Product-market fit in 12mo" | 60% | 0 (no) | (0.6-0)² = 0.36 |
| "3 enterprise deals in 6mo" | 40% | 0 (no) | (0.4-0)² = 0.16 |
| "Top risk materializes" | 30% | 1 (yes) | (0.3-1)² = 0.49 |

**Brier score for this deal:** (sum of contributions) / n = ___
- Perfect = 0.0, Random = 0.25, Always wrong = 1.0
- Good forecaster: < 0.20
- Reasonable forecaster: 0.20 - 0.25

### 5) Calculate calibration (are your probabilities accurate?)

Group your historical predictions by confidence level:

| Confidence bucket | Predictions | Outcomes (% true) | Calibration gap |
|---|---|---|---|
| 10-20% | 15 | 18% true | +3% (slightly under-confident) |
| 30-40% | 22 | 28% true | -7% (slightly over-confident) |
| 50-60% | 18 | 52% true | -3% (well calibrated) |
| 70-80% | 12 | 58% true | -17% (over-confident) |
| 90%+ | 5 | 80% true | -12% (over-confident) |

**Calibration insight:** "I tend to be over-confident in the 70-80% range. When I say 75%, things happen ~60% of the time."

### 6) Identify what you underweighted or overweighted

**For this deal:**
- Underweighted: ___
- Overweighted: ___
- Surprise factor: ___

**Pattern across deals (update quarterly):**
| Factor | Times underweighted | Times overweighted |
|---|---|---|
| Team learning rate | | |
| Distribution advantages | | |
| Timing/market readiness | | |
| Technical moat | | |
| Competition | | |
| Founder-market fit | | |

### 7) Extract heuristics (portable rules)

Good heuristics are:
- Specific enough to act on
- Falsifiable
- Tied to observed evidence
- **Attached to a base rate**

**Heuristic format:**
"When [specific condition], [outcome] happens [X%] of the time in my experience."

Examples:
- "When a seed-stage founder can't name a specific buyer trigger event, they fail to hit enterprise sales targets 80% of the time."
- "When we invest in a second-time founder with prior distribution success, they raise Series A 90% of the time."

Write 2-5 heuristics from this postmortem:
1. 
2. 
3. 

### 8) Update your pattern library with base rates

**Archetype performance tracking:**
| Archetype | Deals | Success rate | Avg Brier | Notes |
|---|---|---|---|---|
| First-time founder, crowded market | 8 | 25% | 0.28 | Over-confident on differentiation |
| Second-time founder, distribution edge | 5 | 80% | 0.15 | Under-confident on execution |
| Technical founder, no GTM | 6 | 33% | 0.32 | Over-weight technical moat |

### 9) Measure learning rate (quarterly)

**Rolling Brier score by quarter:**
| Quarter | Deals scored | Avg Brier | Calibration gap | Trend |
|---|---|---|---|---|
| Q1 2025 | 12 | 0.28 | 15% over-confident | Baseline |
| Q2 2025 | 15 | 0.24 | 10% over-confident | Improving |
| Q3 2025 | 14 | 0.21 | 8% over-confident | Improving |
| Q4 2025 | 16 | 0.19 | 5% over-confident | Good |

**Learning rate = (Brier_t - Brier_t-1) / Brier_t-1**

Target: 5-10% improvement per quarter until Brier < 0.20

### 10) Create follow-up list

| What to track | Signal | Recheck date | Prediction to score |
|---|---|---|---|
| | | | P(___) = ___% |
| | | | P(___) = ___% |

| Who to keep warm | Why | Next touch |
|---|---|---|
| | | |

## Quarterly calibration review

Every quarter:
1. Score all predictions that reached outcome date
2. Calculate Brier scores by deal and overall
3. Update calibration table (predictions vs outcomes by confidence bucket)
4. Identify systematic biases (over/under-confidence patterns)
5. Review passes that raised: were pass reasons validated?
6. Update heuristics with new base rates
7. Calculate learning rate vs previous quarter

**Quarterly output:**
- Brier score trend chart
- Calibration curve (predicted % vs actual %)
- Top 3 biases to correct
- Updated heuristic base rates

## Annual review: Portfolio outcomes vs initial thesis

For each portfolio company:
- What did we believe at investment?
- What's the current reality?
- Where were we right/wrong?
- Score the original predictions
- Update archetype base rates

**Annual output:**
- Portfolio Brier score
- Best/worst calibrated predictions
- Archetype performance update
- Learning rate over 4 quarters
- Heuristics validated or invalidated

## Salesforce logging (optional)
If Salesforce is your system of record:
- Add predictions as structured fields on Opportunity (or in Notes)
- Record confidence levels at each stage
- Link postmortem Note titled "Postmortem (YYYY-MM-DD)"
- Update outcome fields when known
- Tag with heuristics extracted

## Edge cases
- If you have no outcome yet: run a "process postmortem" focused on what you learned and what evidence was missing. Record predictions for future scoring.
- If the outcome is ambiguous: define binary success criteria now, score later.
- If you can't remember your initial thesis: reconstruct as honestly as possible, and **start recording predictions with probabilities now**.
- If you have few deals: even 10-15 scored predictions start to show calibration patterns.
