---
name: board-prep
description: Compile financial narrative for board meeting
role_groups: [finance, leadership]
jtbd: |
  Board meetings require pulling together financial narrative from multiple sources. 
  This gathers recent variance analyses, pulls key decisions and context, structures 
  a board-ready narrative, and identifies questions the board might ask so you're 
  fully prepared.
time_investment: "30-45 minutes per board meeting"
---

## Purpose

Compile comprehensive board materials with financial narrative, supporting context, and Q&A prep.

## Usage

- `/board-prep` - Prepare for next board meeting
- `/board-prep [date]` - Prepare for specific board meeting date

---

## Steps

1. **Gather financial context:**
   - Recent variance analyses
   - Quarter-to-date performance
   - Forecast vs budget
   - Cash position

2. **Pull key decisions** from recent meetings
3. **Identify board-relevant topics:**
   - Material changes
   - Risks or opportunities
   - Strategic decisions needed

4. **Structure board narrative:**
   - Financial performance summary
   - Key metrics
   - Variances explained
   - Outlook
   - Decisions needed

5. **Prepare Q&A:**
   - Anticipate board questions
   - Prepare answers with backup data

---

## Output Format

```markdown
# Board Materials: [Date]

## Financial Snapshot
- Revenue: [Actual] vs [Budget] ([X]%)
- Expenses: [Actual] vs [Budget] ([X]%)
- Cash: $[Amount]

## Key Updates
1. [Update 1]
2. [Update 2]

## Material Variances
[Link to variance analysis]

## Outlook
[Forecast for rest of period]

## Questions Board Might Ask
1. [Question] - Answer: [Prepared response]
```
