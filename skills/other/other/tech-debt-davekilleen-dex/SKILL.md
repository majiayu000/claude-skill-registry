---
name: tech-debt
description: Review and prioritize technical debt
role_groups: [engineering, leadership]
jtbd: |
  Tech debt accumulates but gets lost in scattered notes. This scans projects and 
  notes for tech debt mentions, groups by impact and effort, checks age of items, 
  and suggests prioritization so you can make data-driven decisions about when to 
  pay down debt.
time_investment: "15-20 minutes per review"
---

## Purpose

Inventory technical debt, assess impact/effort, and prioritize what to address.

## Usage

- `/tech-debt` - Full tech debt review
- `/tech-debt [component]` - Focus on specific system/component

---

## Steps

1. **Search for tech debt mentions:**
   - 04-Projects/
   - Meeting notes with keywords: "tech debt", "refactor", "technical debt", "needs cleanup"
   - Code review discussions

2. **Extract for each item:**
   - Description
   - Component/system affected
   - Impact (velocity, stability, security)
   - Estimated effort
   - Age (when first noted)

3. **Categorize by impact:**
   - Critical: Blocking work or security risk
   - High: Slowing velocity significantly
   - Medium: Creating friction
   - Low: Nice to have

4. **Generate prioritization matrix:**
   - High impact + low effort = Do now
   - High impact + high effort = Plan for
   - Low impact + low effort = Quick wins
   - Low impact + high effort = Defer

---

## Output Format

```markdown
# 🔧 Technical Debt Inventory

**Items identified:** [Count]
**Critical items:** [Count]

## Do Now (High Impact + Low Effort)
- [Item] - Impact: [Why] - Effort: [Estimate]

## Plan For (High Impact + High Effort)
- [Item] - Impact: [Why] - Effort: [Estimate]

## Aging Debt (>6 months)
- [Item] - First noted: [Date]

## Recommendations
1. [Top priority]
2. [Second priority]
```
