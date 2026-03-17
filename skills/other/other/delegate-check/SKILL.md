---
name: delegate-check
description: Review what should be delegated
role_groups: [leadership]
jtbd: |
  Leaders stay in the weeds when they should delegate. This scans recent activities 
  and time spent, identifies low-leverage work, suggests delegation opportunities, 
  and checks team capacity so you focus on what only you can do.
time_investment: "15-20 minutes per review"
---

## Purpose

Identify delegation opportunities to focus on high-leverage leadership work.

## Usage

- `/delegate-check` - Review delegation opportunities

---

## Steps

1. **Analyze recent activities:**
   - Review last 2 weeks of meetings
   - Check daily plans for time spent
   - Identify recurring tasks

2. **Categorize work:**
   - Strategic (only you can do)
   - Tactical (could be delegated)
   - Administrative (should be delegated)

3. **Identify delegation candidates:**
   - What tasks are recurring?
   - What could others learn from?
   - What's taking your time but isn't strategic?

4. **Check team capacity:**
   - Who has bandwidth?
   - Who would benefit from development?

5. **Create delegation plan:**
   - What to delegate
   - To whom
   - Transition approach

---

## Output Format

```markdown
# Delegation Opportunities

## Low-Leverage Work (Should Delegate)
- [Task/Activity] - Time: [X hrs/week] - Delegate to: [Name]

## Development Opportunities
- [Task] - Good for [Person] to learn

## Strategic Work (Keep)
- [Activity] - Why only you: [Reason]

## Delegation Plan
1. [Task] → [Person] - Transition: [Approach]
```
