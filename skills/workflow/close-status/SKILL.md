---
name: close-status
description: Month-end close checklist and blockers
role_groups: [finance, leadership]
jtbd: |
  Month-end close has many moving parts and dependencies. This shows the close 
  checklist for the current period, flags incomplete items, surfaces blockers from 
  recent meetings, and tracks dependencies on other teams so you know exactly where 
  you stand.
time_investment: "10-15 minutes per check"
---

## Purpose

Track month-end close progress, identify blockers, and ensure timely completion.

## Usage

- `/close-status` - Current period close status
- `/close-status [month]` - Specific month (e.g., "January")

---

## Steps

1. **Read close checklist** (from finance files or standard close process)
2. **Check status of each item:**
   - Complete
   - In progress
   - Blocked
   - Not started
3. **Search recent meetings** for close-related discussions and blockers
4. **Identify dependencies** on other teams
5. **Calculate days remaining** until close deadline
6. **Generate status dashboard** with:
   - Checklist completion %
   - Blockers with owners
   - Timeline to completion
   - Critical path items

---

## Output Format

```markdown
# 📊 Close Status: [Month Year]

**Close deadline:** [Date]
**Days remaining:** [X]
**Completion:** [X]%

## Checklist Status
- [x] [Item 1] - Complete
- [ ] [Item 2] - In progress (Owner: [Name])
- [ ] [Item 3] - **BLOCKED** - [Reason]

## Blockers
1. [Blocker] - Owner: [Name] - Action: [What's needed]

## Dependencies
- Waiting on [Team/Person] for [Item]

## Critical Path
Items that must complete before others can start:
1. [Item] - [Status]
```
