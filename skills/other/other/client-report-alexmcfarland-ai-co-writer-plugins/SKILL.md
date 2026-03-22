---
name: client-report
description: Write a professional progress or results report. Sections include Period Summary, Work Completed, Results & Metrics, Challenges & Solutions, Next Period Plan, and Action Items. Professional and results-focused. Use when user needs a "client report", "progress update", "monthly report", or "results report".
---

## Load Context First

Before executing this skill, read the following files from the project folder if they exist:

1. **USER.md** — who the user is, how they think, how they work
2. **BUSINESS.md** — their business, products, positioning, brand voice, content strategy
3. **ICP.md** — their ideal customer, their language, their fears, what makes them buy
4. **Voice or brand voice skill** — look for any installed skill related to voice, tone, or brand voice and apply it automatically
5. Any additional context provided by the user in this session

Use all context silently. Do not reference or summarize files unless asked.

---

# Client Report Writer

**Purpose:** Write professional progress or results reports that demonstrate value, maintain transparency, and keep projects on track.

## Output Format

```markdown
# [Report Type] Report: [Client/Project Name]

**Period:** [Date range]
**Prepared by:** [User name]
**Date:** [Today]

---

## Executive Summary

[2-3 sentences: what was accomplished, key metrics, overall status]

**Status:** 🟢 On Track / 🟡 Minor Issues / 🔴 Needs Attention

---

## Work Completed

| # | Task/Deliverable | Status | Notes |
|---|-----------------|--------|-------|
| 1 | [Task] | ✅ Complete | [Details] |
| 2 | [Task] | ✅ Complete | [Details] |
| 3 | [Task] | 🔄 In Progress | [Details] |

**Key accomplishments:**
- [Specific achievement #1]
- [Specific achievement #2]
- [Specific achievement #3]

---

## Results & Metrics

| Metric | Previous Period | This Period | Change |
|--------|----------------|-------------|--------|
| [Metric 1] | [Value] | [Value] | [+/-X%] |
| [Metric 2] | [Value] | [Value] | [+/-X%] |
| [Metric 3] | [Value] | [Value] | [+/-X%] |

**Key insight:** [What the numbers mean and why they matter]

---

## Challenges & Solutions

### Challenge: [Name]
**What happened:** [Description]
**How we handled it:** [Solution]
**Impact:** [How it affected the project/timeline]

[Repeat for each challenge]

---

## Next Period Plan

| Priority | Task | Target Date | Owner |
|----------|------|-------------|-------|
| High | [Task] | [Date] | [Who] |
| High | [Task] | [Date] | [Who] |
| Medium | [Task] | [Date] | [Who] |
| Low | [Task] | [Date] | [Who] |

---

## Action Items

| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 1 | [Action needed] | [Client/User] | [Date] | Pending |
| 2 | [Action needed] | [Client/User] | [Date] | Pending |

---

**Questions or feedback?** [Contact method]
```

## Quality Checklist

- [ ] Executive summary gives full picture in 2-3 sentences
- [ ] Work completed is specific (not "worked on stuff")
- [ ] Metrics include comparison to previous period
- [ ] Challenges are stated honestly with solutions
- [ ] Next period plan has clear priorities and owners
- [ ] Action items have owners and due dates
- [ ] Tone is professional and results-focused
- [ ] No fabricated metrics — all from user input
