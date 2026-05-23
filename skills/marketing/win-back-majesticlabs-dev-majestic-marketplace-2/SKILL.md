---
name: win-back
description: Design win-back campaigns to re-engage dormant customers and recover churned users with targeted messaging, special offers, and feedback collection to understand and address churn reasons.
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, AskUserQuestion
---

# Win-Back Campaign Designer

## Conversation Starter

Use `AskUserQuestion` to gather initial context. Begin by asking:

"I'll help you design win-back campaigns to recover churned and dormant customers.

Please provide:

1. **Business Type**: What do you sell? (SaaS, e-commerce, subscription, service)
2. **Churn Definition**: How do you define 'churned' vs 'dormant'?
3. **Churn Reasons**: Why do customers typically leave? (if known)
4. **Customer Value**: What's the average customer lifetime value?
5. **Past Attempts**: Have you tried win-back campaigns before? Results?
6. **Available Data**: What data do you have on churned customers?

I'll research win-back benchmarks and design campaigns tailored to your churn reasons."

## Research Methodology

Use WebSearch extensively to find:
- Win-back email benchmarks (open rates, recovery rates)
- Optimal timing for win-back campaigns by industry
- Exit survey best practices and question templates
- Re-engagement offer effectiveness studies

## Required Deliverables

### 1. Churn Segmentation Framework

**By Churn Reason:**

| Segment | Win-Back Difficulty | Approach |
|---------|---------------------|----------|
| Price-sensitive | Medium | Value + discount |
| Competition | Hard | Feature comparison |
| Non-usage | Easy | Re-education |
| Poor experience | Medium | Apology + fix proof |
| Changed needs | Very hard | Future trigger |
| Payment failure | Easy | Update prompt |

**By Recency:**

| Segment | Time Since Churn | Recovery Rate | Priority |
|---------|------------------|---------------|----------|
| Fresh | 0-30 days | 15-25% | Highest |
| Recent | 31-90 days | 8-15% | High |
| Aged | 91-180 days | 3-8% | Medium |
| Stale | 180+ days | 1-3% | Low |

**Prioritization Matrix:** Cross LTV tier with recency to determine approach (personal outreach vs automated).

### 2. Win-Back Email Sequence (5 emails)

| Email | Day | Purpose |
|-------|-----|---------|
| Check-In | 7 | Acknowledge absence, open dialogue |
| Value Reminder | 14 | Show what they're missing |
| The Offer | 21 | Incentive to return |
| Last Chance | 30 | Final push with urgency |
| Goodbye | 45 | Close loop, leave door open |

Full email copy: [resources/email-sequence.yaml](resources/email-sequence.yaml)

### 3. Win-Back Offer Framework

| Churn Reason | Recommended Offer |
|--------------|-------------------|
| Price-sensitive | Discount 25-50%, downgrade option |
| Competition | Feature match, switching assistance |
| Non-usage | Free training, onboarding call |
| Poor experience | Apology + credit, priority support |

Discount tiers by customer value and non-discount alternatives: [resources/offers-feedback.yaml](resources/offers-feedback.yaml)

### 4. Exit Survey & Feedback Collection

- Exit survey questions (at cancellation)
- Churned customer interview script
- Post-loss referral email template
- Feedback analysis template

Full templates: [resources/offers-feedback.yaml](resources/offers-feedback.yaml)

### 5. Automation Triggers

| Trigger | Definition | Sequence |
|---------|------------|----------|
| Soft churn | No login 30 days (active sub) | Re-engagement |
| Hard churn | Cancelled subscription | Win-back |
| Payment churn | Failed payment, no update | Dunning then Win-back |
| Dormant | No activity 60 days | Re-activation |

**Suppression Rules:**
- Opted out of marketing
- Already in win-back sequence
- Won back in last 90 days
- Churned 3+ times

### 6. Success Metrics

| Metric | Benchmark |
|--------|-----------|
| Win-back rate | 5-15% |
| Win-back CAC | < Original CAC |
| Second-churn rate | <50% in 6 months |

**Email Metrics by Stage:**

| Email | Open Rate | Click Rate | Conversion |
|-------|-----------|------------|------------|
| Check-in | 30-40% | 5-10% | N/A (replies) |
| Value reminder | 25-35% | 8-15% | 2-5% |
| Offer | 35-45% | 15-25% | 5-10% |
| Last chance | 40-50% | 20-30% | 5-10% |

**ROI Calculation:**
```
Win-back ROI = (Revenue Recovered - Campaign Cost) / Campaign Cost × 100

Example: 1,000 contacted × 10% win-back × $50 MRR × 12 mo = $60K recovered
Campaign cost: $2K → ROI: 2,900%
```

## Output Format

```markdown
# WIN-BACK CAMPAIGN BLUEPRINT: [Business Name]

## Executive Summary
[Churn situation and recovery strategy]

## Churn Segmentation
[Customer segments with prioritization]

## Win-Back Email Sequence
[5 emails with complete copy]

## Offer Framework
[Offers by segment and churn reason]

## Exit Feedback System
[Survey, interview script, analysis template]

## Automation Triggers
[Technical trigger logic]

## Success Metrics
[KPIs and tracking setup]

## Implementation Checklist
[ ] Set up churn segmentation
[ ] Build exit survey
[ ] Create email sequence
[ ] Configure automation triggers
[ ] Define offers by segment
[ ] Launch to fresh churn first
[ ] Monitor and optimize weekly
```

## Quality Standards

- **Segment-specific**: Different approaches for different churn reasons
- **Empathy-first**: Acknowledge the relationship, not just the transaction
- **Data-driven offers**: Base discounts on economics, not desperation
- **Feedback loop**: Always collect data to prevent future churn
- **Measurable outcomes**: Clear metrics for success

## Tone

Empathetic but direct. Write like a customer success leader who genuinely wants customers back—but respects their decision if they've moved on. No desperation, no manipulation—just honest outreach.
