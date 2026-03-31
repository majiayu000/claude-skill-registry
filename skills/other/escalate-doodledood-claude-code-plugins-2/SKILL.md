---
name: escalate
description: 'Structured escalation within the /do workflow. Surfaces blocking issues, scope changes, and workflow pauses with evidence, referencing the Manifest hierarchy. Called by /do, not directly.'
user-invocable: false
---

# /escalate - Structured Escalation

## Goal

Structure escalation events during /do execution — blocking issues, scope changes, and workflow pauses — with evidence and clear next steps.

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

### Proposed Amendment

During implementation, you discovered a criterion should change — not because it's blocking, but because reality revealed a better formulation. No 3-attempt evidence needed — just rationale.

```markdown
## Escalation: Proposed Amendment to [ID]

**Current criterion:** [current wording]
**Proposed change:** [new wording]

### Rationale
[What you discovered during implementation that motivates this change]

### Impact
- Deliverables affected: [which ones]
- Work already done: [what would need to change if approved]

### Requesting
Approve amendment, reject and continue with current criterion, or adjust.
```

**When to use**: You CAN meet the criterion as written, but discovered it should be different. Approach pivots don't need this — just log and adapt. Use this when the manifest's criteria themselves should change.

**vs Self-Amendment**: If the USER or a reviewer triggered the change, use Self-Amendment instead — that proceeds autonomously without human approval.

### Self-Amendment

User input or a PR review comment contradicts or extends the manifest. No 3-attempt evidence needed — this is a scope change, not a blocker.

```markdown
## Escalation: Self-Amendment

**Trigger:** [user message or PR comment that contradicts/extends the manifest]
**Affected items:** [which INV-G*, AC-*, PG-* items are contradicted or need additions]

### What changed
[Concise description of the scope change — what the user/reviewer wants that the manifest doesn't cover or contradicts]

### Manifest path
[Path to manifest file]

### Execution log path
[Path to execution log]
```

**When to use**: The USER or a REVIEWER triggered a scope change — they said something that contradicts or extends the manifest. This is a mechanical exit, not a decision point. /do handles the amendment flow after this escalation.

**vs Proposed Amendment**: If YOU discovered the criterion should change (no user/reviewer trigger), use Proposed Amendment instead — that requires human approval.

### User-Requested Pause

User explicitly asked to stop mid-workflow (e.g., "commit so I can deploy", "stop here for now"). No 3-attempt evidence needed—just explain the pause.

```markdown
## Escalation: User-Requested Pause

**Reason:** [what user asked for]
**Current state:** [what's done, what's pending]

### Progress Summary
- Completed: [ACs done]
- In progress: [current work]
- Remaining: [ACs not started]

### To Resume
[How to continue - e.g., "/do <manifest> <log>" or specific next steps]
```

**When to use**: User interrupts workflow for legitimate reasons (deploy, review, break). Not a blocker—just a handoff.

## Medium Routing

When medium is non-local, /do routes escalations through the medium directly — /escalate is not invoked. The escalation templates above still define the expected content structure; /do uses them when composing messages to the channel.
