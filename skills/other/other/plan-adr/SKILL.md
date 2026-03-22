---
name: plan-adr
description: Write an Architecture Decision Record.
---

# Plan ADR

The Planner drives this workflow. Write an Architecture Decision Record documenting a significant technical decision, its context, alternatives considered, and consequences.

---

## Phase 1: Identify the Decision

Scope the ADR before drafting.

### Steps

1. State the decision clearly in one sentence
2. Identify what triggered the decision (issue, incident, tech debt, new requirement)
3. Determine the ADR number by reading `docs/adr/` for the highest existing number
4. Confirm this warrants an ADR (significant, hard-to-reverse, or convention-setting)

### Output

Produce an ADR brief covering: decision statement, trigger, assigned ADR number.

**Approval Required:** No

---

## Phase 2: Draft the ADR

Create the ADR file using the standard format.

### File Location

`docs/adr/<NNNN>-<kebab-case-title>.md`

### ADR Format

```markdown
# <number>. <Title>

Date: <YYYY-MM-DD>

## Status

Proposed

## Context

<What is the issue that we're seeing that is motivating this decision or change?>

## Decision

<What is the change that we're proposing and/or doing?>

## Alternatives Considered

### <Alternative 1>

<Description and why it was rejected>

### <Alternative 2>

<Description and why it was rejected>

## Consequences

### Positive

- <what becomes easier>

### Negative

- <what becomes harder>

### Neutral

- <what changes but is neither better nor worse>
```

### Writing Rules

- Context section: describe the problem, not the solution
- Decision section: state what was decided, not why (that's in Context)
- Consequences: be honest about trade-offs — include negatives
- Status: use `Proposed` until human approves, then `Accepted`
- Link to related ADRs if this supersedes or extends one

### Output

Report the file path created and its Proposed status.

### ⛔ CHECKPOINT

**STOP.** Do not change status to Accepted until human approves the ADR content.

**Approval Required:** Yes

---

## Error Handling

| Error                       | Recovery                                                   |
| --------------------------- | ---------------------------------------------------------- |
| Decision not yet made       | Draft as Proposed, note open questions                     |
| Supersedes existing ADR     | Link to it, update old ADR status to "Superseded by <new>" |
| Scope too broad for one ADR | Split into focused ADRs, one decision each                 |
| Missing alternatives        | Research at least 2 alternatives before drafting           |
