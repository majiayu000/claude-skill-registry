---
name: escalate
description: 'Structured escalation with evidence. Surfaces blocking issues for human decision, referencing the Manifest hierarchy.'
user-invocable: false
---

# /escalate - Structured Escalation

## Goal

Surface a blocking issue for human decision with structured evidence, referencing the Manifest hierarchy.

## Input

`$ARGUMENTS` = escalation context

Examples:
- "INV-G1 blocking after 3 attempts"
- "AC-1.2 blocking after 3 attempts"
- "Manual criteria AC-2.3 needs human review"

## Principles

1. **Evidence required** - No lazy escalations. Must include what was tried and why it failed.

2. **Structured options** - Present possible paths forward with tradeoffs, not just "I'm stuck".

3. **Respect hierarchy** - Global Invariant blocking = task-level issue. AC blocking = deliverable-level issue.

## Evidence Requirements

For blocking criterion escalation, MUST include:

1. **Which criterion** - specific ID (INV-G*, AC-*.*)
2. **At least 3 attempts** - what was tried
3. **Why each failed** - not just "didn't work"
4. **Hypothesis** - theory about root cause
5. **Options** - possible paths forward with tradeoffs

**Lazy escalations are NOT acceptable:**
- "I can't figure this out"
- "This is hard"
- "INV-G1 is failing" (without attempts)

## Escalation Types

### Global Invariant Blocking

Task-level blocker. Cannot complete while this fails.

```markdown
## Escalation: Global Invariant [INV-G{N}] Blocking

**Criterion:** [description]
**Type:** Global Invariant (task fails if violated)
**Impact:** Cannot complete task until resolved

### Attempts
1. **[Approach 1]** - What: ... Result: ... Why failed: ...
2. **[Approach 2]** - ...
3. **[Approach 3]** - ...

### Hypothesis
[Theory about why this is problematic]

### Possible Resolutions
1. **Fix root cause**: [description] - Effort: ... Risk: ...
2. **Amend invariant**: Relax to [new wording] - Rationale: ...
3. **Remove invariant**: Not applicable to this task - Rationale: ...

### Requesting
Human decision on path forward.
```

### Acceptance Criteria Blocking

Deliverable-level blocker.

```markdown
## Escalation: Acceptance Criteria [AC-{D}.{N}] Blocking

**Criterion:** [description]
**Type:** AC for Deliverable {D}: [name]
**Impact:** Deliverable incomplete

### Context
Other ACs in this deliverable: [statuses]

### Attempts
[same as above]

### Possible Resolutions
1. **Different implementation**: [approach]
2. **Amend criterion**: Change to [new wording]
3. **Remove criterion**: Not actually needed
4. **Descope deliverable**: Remove AC, deliverable still valuable

### Requesting
Human decision on path forward.
```

### Manual Criteria Review

All automated criteria pass. Manual criteria need human verification.

```markdown
## Escalation: Manual Criteria Require Human Review

All automated criteria pass.

### Manual Criteria Pending
- **AC-{D}.{N}**: [description] - How to verify: [from manifest]

### What Was Executed
[Brief summary]

Please review and confirm completion.
```
