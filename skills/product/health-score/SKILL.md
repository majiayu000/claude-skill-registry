---
name: health-score
description: Review account health across portfolio
role_groups: [customer_success]
jtbd: |
  You manage many accounts and can't track them all manually. This scans customer 
  account pages, identifies at-risk accounts (no recent contact, open issues), flags 
  upcoming renewals, and suggests proactive outreach so you prevent churn before 
  it happens.
time_investment: "10-15 minutes per review"
---

## Purpose

Monitor portfolio health, identify at-risk accounts, and prioritize proactive engagement.

## Usage

- `/health-score` - Full portfolio review
- `/health-score [segment]` - Focus on specific segment/tier

---

## Steps

1. **Scan customer account pages** in 05-Areas/People/External/ and 05-Areas/Companies/
2. **For each account, assess:**
   - Last contact date (flag if >30 days)
   - Open support issues
   - Product adoption/usage trends
   - Upcoming renewal dates
   - Champion engagement

3. **Calculate health indicators:**
   - Green: Engaged, no issues
   - Yellow: Warning signs
   - Red: At-risk

4. **Generate portfolio dashboard:**
   - Health distribution
   - At-risk accounts with reasons
   - Proactive outreach recommendations

---

## Output Format

```markdown
# 💚 Portfolio Health Score

**Accounts:** [Total]
**Health distribution:** Green: [X] | Yellow: [X] | Red: [X]

## 🚨 At-Risk (Red)
### [Account Name]
- **Risk factors:** No contact in 45 days, support ticket open 2 weeks
- **Renewal:** [Date] (X days away)
- **Action:** Schedule check-in call this week

## ⚠️ Watch List (Yellow)
[Similar format]

## ✅ Healthy (Green)
[Count] accounts in good standing

## Proactive Outreach Needed
1. [Account] - [Reason] - [Suggested action]
```
