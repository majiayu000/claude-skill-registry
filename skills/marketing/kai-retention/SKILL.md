---
name: kai-retention
description: Customer retention system — churn analysis, retention tactics, loyalty programs, and engagement scoring. Use when "retention", "reduce churn", "keep customers", "loyalty program", "customer retention", "churn prevention", "churn analysis", "engagement scoring", "win-back", "customer lifetime value", or any request to analyze, prevent, or reduce customer churn.
---

# kai-retention — Customer Retention System

Design a complete retention system: churn diagnostics, retention tactics, engagement scoring, loyalty mechanics, and win-back campaigns.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## References

Load these files as context before starting:

- `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\customer-retention.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\growth-loops-applied.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\channels\email-lifecycle.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\personas\_persona-index.md`

## Phase 1 — Discovery

1. Read from `MARKETING.md`. Only ask about things not covered there:
   - Business model (SaaS, ecommerce, services, marketplace)
   - Current churn rate (monthly/annual, if known)
   - Customer count and average revenue per customer
   - Current retention efforts (any emails, loyalty program, support)
   - Known churn reasons (from exit surveys, support tickets, cancellation flow)
   - Product usage data availability (do they track feature adoption?)
   - Customer segments (free vs. paid, plan tiers, cohorts)
2. Identify the retention maturity level:
   - **Level 0**: No retention effort beyond the product itself
   - **Level 1**: Basic cancellation flow + occasional check-in emails
   - **Level 2**: Lifecycle emails + usage tracking + support triggers
   - **Level 3**: Predictive churn scoring + proactive intervention + loyalty program

## Phase 2 — Analysis

### Churn Diagnostics
1. Categorize churn types:
   - **Voluntary**: Customer actively cancels (dissatisfaction, budget, switched)
   - **Involuntary**: Payment failure, expired card, billing issue
   - **Passive**: Stops using but doesn't cancel (ghost users)
2. Map the churn timeline: when do most customers leave?
   - First 30 days (onboarding failure)
   - 60-90 days (value not realized)
   - At renewal (annual plan decision point)
   - After price increase or feature change
3. Identify leading indicators of churn:
   - Login frequency decline
   - Feature usage drop
   - Support ticket volume spike
   - NPS/CSAT score decline
   - Billing page visits

### Engagement Scoring Model
Define a health score (0-100) based on:

| Signal | Weight | Scoring |
|--------|--------|---------|
| Login frequency (last 14 days) | 25% | Daily=100, Weekly=60, Monthly=20, None=0 |
| Core feature usage | 25% | Used all=100, Used some=50, Used none=0 |
| Support interactions | 15% | Positive=80, Neutral=50, Negative=20 |
| Account expansion signals | 15% | Upgraded=100, Stable=50, Downgraded=10 |
| Referral/advocacy | 10% | Referred=100, NPS promoter=60, Passive=30 |
| Billing health | 10% | Current=100, Late=30, Failed=0 |

**Risk tiers**: Green (70-100), Yellow (40-69), Red (0-39).

## Phase 3 — Produce

Build these deliverables:

### Retention Playbook
Intervention strategies by risk tier:

**Red (0-39) — Immediate Rescue**
- Trigger personal outreach within 24 hours
- Offer concession (discount, extended trial, premium support)
- Escalate to customer success manager
- Deploy win-back email sequence

**Yellow (40-69) — Proactive Nurture**
- Send usage tips targeting unused features
- Invite to office hours or webinar
- Share relevant case study or success story
- Request feedback (short survey, not NPS)

**Green (70-100) — Expansion & Advocacy**
- Request referral or testimonial
- Offer early access to new features
- Invite to advisory board or beta program
- Cross-sell or upsell relevant add-ons

### Win-Back Campaign
For customers who have already churned:
- 3-email sequence: Day 1, Day 7, Day 30
- Each email addresses a different churn reason
- Include a specific offer or product update
- Run through quality gates before sending

### Loyalty Program Design (if applicable)
- Reward mechanics: points, tiers, milestones, or referral credits
- Earning actions mapped to business goals
- Redemption options that drive retention (not margin erosion)
- Communication plan for program launch

### Involuntary Churn Prevention
- Dunning email sequence (3-5 emails over 14 days)
- Smart retry logic for failed payments
- Card update reminder before expiration

## Phase 4 — Output

1. Deliver the retention playbook and engagement scoring spec.
2. Run all email sequences through quality gates:
   - `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\banned_word_check.py <file>`
   - `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\four_us_score.py <file>`
3. Include a 90-day implementation roadmap and monthly metrics to track (churn rate, cohort retention, health score distribution, NPS trend, expansion vs. contraction revenue).

## Constraints

- No banned Tier 1 words in any customer-facing copy.
- Win-back emails must comply with CAN-SPAM (reference: `E:\Dev2\kai-cmo-harness-work\harness\references\cold-email-rules.md`).
- Loyalty program rewards must not erode margins below profitability.
- Discount offers in rescue plays capped at 20% unless user approves higher.
- All email sequences target 10+/16 on Four U's scoring.
- Max 2 auto-retry cycles on quality gate failures for email content.
