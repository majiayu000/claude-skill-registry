---
name: ca-conflict
description: Stop everything and surface a rule conflict — persona vs. docs vs. code. Present both sides and the conflict-hierarchy level; the user resolves. No silent reconciliation.
argument-hint: (none)
---

# $ca-conflict — conflict protocol

Orchestrator protocol, not a skill route. When a rule conflict surfaces — the persona, a `.codearbiter/` document, and code contradict each other, or two docs contradict each other — all other work STOPs and the conflict is presented for the user to resolve. The orchestrator never picks a side.

## Flow

1. **Halt** — suspend the in-progress task. No partial progress.
2. **Identify** the conflicting sources (A and B): which document, file, or rule each is.
3. **Quote** the exact passages side by side.
4. **Classify** the conflict against the §2 conflict-resolution hierarchy and name the level the
   tension sits at. Note which source was more recently updated — informational, not determinative.
5. **Present** and wait. Work resumes only after the user explicitly resolves.

## Output

```
## Conflict detected — work halted

### Source A
File: <path> · Last updated: <date>
> <exact quoted text>

### Source B
File: <path> · Last updated: <date>
> <exact quoted text>

### Nature of conflict
<what the two sources disagree about>

### Conflict-hierarchy level
Level N — <why the tension sits here>

### To resolve
<options — update A, update B, or supersede one via an ADR>

---
Work is halted. Resolve before the orchestrator proceeds.
```

## When routed automatically

The orchestrator surfaces a conflict on its own when the persona and a `.codearbiter/` doc contradict
each other, two docs contradict, code contradicts an accepted ADR, a new ADR contradicts an accepted
one, or a task instruction contradicts a hard gate.

## After resolution

The orchestrator records the resolution; if the user authorized a doc update, it makes that update
(the one sanctioned side effect) and resumes from the suspension point.

## Hard gate

MUST stop ALL other work. MUST NOT pick a side without explicit user instruction. MUST NOT decide by
recency alone. MUST NOT silently continue past a detected conflict. If the conflict involves a guessed
or auto-resolved `[CONFIRM-NN]`, flag that as a separate critical finding.
