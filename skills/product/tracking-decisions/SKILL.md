---
name: tracking-decisions
description: Use when making prioritization calls, strategic bets, or any decision worth tracking for future learning - logs decision context, rationale, and expected outcomes for later review
---

# Tracking Decisions

## Why This Matters

PMs make dozens of prioritization calls. Without tracking outcomes, you can't learn which instincts are calibrated. This skill creates a feedback loop: Decision → Expected Outcome → Actual Result → Lesson.

## When to Use

- Prioritizing Feature A over Feature B
- Deciding to defer/cut scope
- Choosing between technical approaches
- Making strategic bets in quarterly planning
- Any decision you'd want to revisit in 30-90 days

## Process

### 1. Create Decision Log

Create file: `outputs/decisions/YYYY-MM-DD-[short-title].md`

### 2. Fill Decision Template

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: tracking-decisions
review_date: YYYY-MM-DD
status: open
---

# Decision: [Short descriptive title]

## Context
[What situation prompted this decision? What's the business context?]

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| [Option A] | [Benefits] | [Drawbacks] |
| [Option B] | [Benefits] | [Drawbacks] |
| [Option C] | [Benefits] | [Drawbacks] |

## Decision
**Chosen:** [Which option]

**Rationale:**
- [Reason 1] `[Evidence/Assumption]`
- [Reason 2] `[Evidence/Assumption]`
- [Reason 3] `[Evidence/Assumption]`

## Expected Outcome
[What do you expect to happen as a result of this decision?]

## Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

## Review Date
**Check back:** YYYY-MM-DD (typically 30-90 days)

---

## Outcome (fill in at review date)

**Status:** *(pending | ✅ correct | ⚠️ partially correct | ❌ wrong)*

**Actual Result:**
[What actually happened?]

**Success Criteria Results:**
- [ ] [Criterion 1]: [Met/Not met - why]
- [ ] [Criterion 2]: [Met/Not met - why]
- [ ] [Criterion 3]: [Met/Not met - why]

**Lessons Learned:**
- [What would you do differently?]
- [What assumptions were wrong?]
- [What signals did you miss?]

**Calibration Note:**
[Did your intuition match reality? Over/under-confident?]
```

### 3. Set Calendar Reminder

After logging, set a reminder for the review date.

### 4. Review Process

At review date:
1. Open the decision log
2. Fill in the Outcome section honestly
3. Update status in frontmatter
4. Extract lessons for future decisions

## Quarterly Decision Review

Every quarter, review all decisions from 90+ days ago:

```markdown
## Q[X] Decision Review

| Decision | Expected | Actual | Outcome | Key Lesson |
|----------|----------|--------|---------|------------|
| [Title] | [Expected] | [Actual] | ✅/⚠️/❌ | [Lesson] |

**Patterns:**
- [What types of decisions am I good at?]
- [What types of decisions am I bad at?]
- [What signals should I weight more/less?]
```

## Output Location

- Individual decisions: `outputs/decisions/YYYY-MM-DD-[title].md`
- Quarterly reviews: `outputs/decisions/Qx-YYYY-review.md`

## Evidence Rules

Same as all PM OS outputs:
- Tag rationale as `[Evidence]` or `[Assumption]`
- Be honest in outcome assessment
- Don't retrofit rationale after knowing the outcome
