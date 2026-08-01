---
name: kai-retention
description: Customer retention system — churn analysis, retention tactics, loyalty programs, and engagement scoring. Use when "retention", "reduce churn", "keep customers", "loyalty program", "customer retention", "churn prevention", "churn analysis", "engagement scoring", "win-back", "customer lifetime value", or any request to analyze, prevent, or reduce customer churn.
---

## Objective

A retention system the business can run: a churn diagnosis that names which churn type is actually costing money, an engagement health score with defined signals and thresholds, intervention playbooks per risk tier, a win-back sequence, involuntary-churn prevention, and a 90-day implementation roadmap with the metrics to watch.

Diagnose before prescribing. A loyalty program aimed at voluntary churn does nothing when the real leak is failed payments, and a dunning sequence does nothing when customers leave in week three because onboarding never delivered value.

## Done when

Work type `strategy-plan` — floor **E3/C3/O1** (`harness/eco-floors.yaml`). The system is a plan; nothing leaves the workspace until a human sends it.

- **E3** — a named human approved the retention playbook, the engagement scoring spec, and the email sequences.
- **C3** — `banned_word_check` clean on all customer-facing copy, every email sequence at **10+/16** on Four U's, and a non-author read the system end to end. Max 2 auto-retry cycles on gate failures for email content.
- **O1** — the plan names its metric with baseline, threshold, window, and owner: monthly churn rate, cohort retention curve, health score distribution, NPS trend, and expansion versus contraction revenue.

Sending any sequence is separate work under `email-lifecycle` (E5/C3/O3), where unsubscribe and sender-identity compliance is a C4 field-standard item, not a lint.

## Constraints

- **Read `MARKETING.md` from the project root first.** If it does not exist, build it from the codebase — CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config — using the template from `/kai-email-system`, and confirm the draft. Do not ask the user what the product is.
- **Seven things must be known before diagnosis:** business model (SaaS, ecommerce, services, marketplace); current churn rate; customer count and average revenue per customer; retention efforts already running; known churn reasons from exit surveys, support tickets, or the cancellation flow; whether product usage and feature adoption are tracked; and customer segments (free vs. paid, plan tiers, cohorts).
- **No banned Tier 1 words in any customer-facing copy.**
- **Win-back emails comply with CAN-SPAM** — see `harness/references/cold-email-rules.md`.
- **Loyalty rewards must not erode margins below profitability.** Redemption options drive retention, not margin destruction.
- **Discounts in rescue plays cap at 20%** unless the user approves higher, and all email sequences target 10+/16 on Four U's before they count as deliverable.
- **Match the prescription to the maturity level.** Predictive churn scoring proposed to a Level 0 business is a plan that never gets built.

| Level | Current state |
|---|---|
| 0 | No retention effort beyond the product itself |
| 1 | Basic cancellation flow plus occasional check-in emails |
| 2 | Lifecycle emails, usage tracking, support triggers |
| 3 | Predictive churn scoring, proactive intervention, loyalty program |

## Context

| Need | Load |
|---|---|
| Retention mechanics, churn tactics, loyalty design | `knowledge/playbooks/customer-retention.md` |
| Retention as a growth loop | `knowledge/playbooks/growth-loops-applied.md` |
| Lifecycle email structure and triggers | `knowledge/channels/email-lifecycle.md` |
| Which persona is churning | `knowledge/personas/_persona-index.md` |
| CAN-SPAM compliance for win-back sends | `harness/references/cold-email-rules.md` |
| Lifecycle email format contract and gate minimums | `harness/skill-contracts/email-lifecycle.yaml` |
| Product, ICP, voice, current channels | `MARKETING.md` (project root) |

**Churn types** — separate them before proposing anything. **Voluntary**: the customer actively cancels (dissatisfaction, budget, switched). **Involuntary**: payment failure, expired card, billing issue. **Passive**: stops using without cancelling (ghost users).

**Churn timeline** — most exits cluster: first 30 days (onboarding failure), 60–90 days (value not realized), at renewal (annual decision point), or after a price increase or feature change. **Leading indicators**: login frequency decline, feature usage drop, support ticket spike, NPS/CSAT decline, billing page visits.

**Engagement score (0–100)** — the rubric:

| Signal | Weight | Scoring |
|---|---|---|
| Login frequency (last 14 days) | 25% | Daily=100, Weekly=60, Monthly=20, None=0 |
| Core feature usage | 25% | Used all=100, Used some=50, Used none=0 |
| Support interactions | 15% | Positive=80, Neutral=50, Negative=20 |
| Account expansion signals | 15% | Upgraded=100, Stable=50, Downgraded=10 |
| Referral/advocacy | 10% | Referred=100, NPS promoter=60, Passive=30 |
| Billing health | 10% | Current=100, Late=30, Failed=0 |

**Risk tiers and the play for each:**

| Tier | Score | Play |
|---|---|---|
| Red | 0–39 | Immediate rescue: personal outreach within 24 hours, a concession (discount, extended trial, premium support), escalation to customer success, win-back sequence |
| Yellow | 40–69 | Proactive nurture: usage tips for unused features, office hours or webinar invite, relevant case study, a short feedback survey (not NPS) |
| Green | 70–100 | Expansion and advocacy: referral or testimonial request, early access, advisory board or beta invite, relevant cross-sell or upsell |

**Win-back** for already-churned customers: a 3-email sequence at Day 1, Day 7, Day 30, each addressing a different churn reason, each carrying a specific offer or product update.

**Involuntary churn prevention**: a dunning sequence of 3–5 emails over 14 days, smart retry logic for failed payments, and a card-update reminder before expiration.

**Loyalty program**, where the model supports one: reward mechanics (points, tiers, milestones, or referral credits), earning actions mapped to business goals, redemption options that drive retention, and a launch communication plan.

**Gates**, on every email file:

```bash
python scripts/quality_gates/banned_word_check.py <file>
python scripts/quality_gates/four_us_score.py <file>
```

## Escalate when

- Churn rate, cohort data, or usage data is unavailable and the diagnosis would be guesswork.
- The stated churn reason from the user conflicts with what exit surveys or support tickets show.
- A rescue play needs a discount above 20%.
- The proposed loyalty mechanics would push unit economics negative.
- Churn is driven by the product rather than by marketing — say so; a retention campaign cannot fix broken onboarding.
- Win-back targets contacts whose consent basis or suppression status is unclear.
