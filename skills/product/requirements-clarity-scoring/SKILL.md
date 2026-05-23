---
name: requirements-clarity-scoring
description: When gathering requirements during discovery phase to measure answer quality and decide when to proceed.
version: 1.1.0
tokens: ~350
confidence: high
sources:
  - https://standards.ieee.org/ieee/29148/6937/
  - https://www.reqview.com/doc/iso-iec-ieee-29148-templates/
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [requirements, discovery, clarity, planning]
---

## When to Use
When gathering requirements during discovery phase to measure answer quality and decide when to proceed.

## Patterns

### Clarity Scoring (1-5)
```
5 = CRYSTAL CLEAR
    - Specific, measurable answer
    - No ambiguity
    - Actionable immediately
    Example: "Response time must be <200ms at p95"

4 = CLEAR
    - Mostly specific
    - Minor gaps fillable
    Example: "Response should be fast" + "under 500ms is acceptable"

3 = PARTIAL
    - General direction known
    - Needs follow-up questions
    Example: "Performance matters" (how much? which operations?)

2 = VAGUE
    - Conflicting information
    - Multiple interpretations possible
    Example: "It should just work" (what does 'work' mean?)

1 = UNCLEAR
    - No answer or "I don't know"
    - Requires stakeholder escalation
    Example: "We haven't decided yet"
```

### Proceed Threshold
```
Calculate average score across all answers:

≥ 4.0  → PROCEED to next phase
3.5-4.0 → PROCEED with noted risks
3.0-3.5 → CLARIFY critical gaps first
< 3.0  → STOP - too many unknowns
```

### Question Categories to Score
```
1. Problem Definition (weight: HIGH)
2. Success Criteria (weight: HIGH)
3. Scope Boundaries (weight: HIGH)
4. Technical Constraints (weight: MEDIUM)
5. Timeline/Budget (weight: MEDIUM)
6. Nice-to-haves (weight: LOW)
```

## Anti-Patterns
- Proceeding with average < 3.0
- Ignoring LOW scores on HIGH weight items
- Assuming unstated requirements
- Not documenting score justification

## Verification Checklist
- [ ] All questions scored 1-5
- [ ] Weighted average calculated
- [ ] HIGH weight items all ≥ 3
- [ ] Gaps documented with follow-up plan
