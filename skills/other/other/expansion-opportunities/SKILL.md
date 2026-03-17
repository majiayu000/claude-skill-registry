---
name: expansion-opportunities
description: Identify upsell/cross-sell opportunities
role_groups: [customer_success, sales]
jtbd: |
  You're focused on retention and miss expansion opportunities. This reviews active 
  accounts, identifies product usage patterns, suggests expansion based on needs 
  expressed, and prioritizes by likelihood so you systematically grow accounts.
time_investment: "15-20 minutes per review"
---

## Purpose

Systematically identify and prioritize account expansion opportunities.

## Usage

- `/expansion-opportunities` - Portfolio-wide review
- `/expansion-opportunities [account]` - Focus on specific account

---

## Steps

1. **Review active accounts:**
   - Current products/features used
   - Usage patterns and adoption
   - Team size vs. potential
   - Budget signals

2. **Identify expansion triggers:**
   - Pain points that premium features solve
   - Departments not yet using product
   - Features requested
   - Competitor tools they use

3. **Assess expansion potential:**
   - Upsell: Upgrade to higher tier
   - Cross-sell: Additional products
   - Seat expansion: More users

4. **Prioritize by likelihood:**
   - High: Budget available, need expressed
   - Medium: Fit exists, need to create urgency
   - Low: Future opportunity

---

## Output Format

```markdown
# 🎯 Expansion Opportunities

**Accounts reviewed:** [Count]
**Total expansion potential:** $[Amount]

## High Priority

### [Account] - $[Potential value]
- **Type:** Upsell / Cross-sell / Seat expansion
- **Trigger:** [Why now]
- **Next step:** [Action]

## Medium Priority
[Similar format]

## Expansion by Type
- Upsell: $[Amount] ([X] opportunities)
- Cross-sell: $[Amount] ([X] opportunities)
- Seat expansion: $[Amount] ([X] opportunities)
```
