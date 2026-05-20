---
name: plan-adr
description: Write an Architecture Decision Record
---

# Plan ADR

Uses **Planner**. Write an Architecture Decision Record documenting a significant technical decision, its context, alternatives considered, and consequences.

**Prerequisites:** A decision that has been made (or is proposed) that affects the system's architecture, conventions, or long-term direction

---

## Phase 1: Identify the Decision

### Determine ADR Scope

1. State the decision clearly in one sentence
2. Identify what triggered the decision (issue, incident, tech debt, new requirement)
3. Determine the ADR number by reading `docs/adr/` for the highest existing number
4. Confirm this warrants an ADR (significant, hard-to-reverse, or convention-setting)

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title> (if applicable)
- **Phase:** 1 — Identify

## Decision Statement

<One-sentence description of the decision>

## Trigger

<What prompted this decision>

## ADR Number

<next sequential number in docs/adr/>

## Next Step

Draft the ADR.

**Approval Required:** No
```

---

## Phase 2: Draft the ADR

### ADR Structure

Create the file at `docs/adr/<NNNN>-<kebab-case-title>.md` using this format:

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

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** 2 — Draft

## ADR Created

**File:** docs/adr/<NNNN>-<title>.md
**Status:** Proposed

## Next Step

Review the ADR for accuracy and completeness.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not change status to Accepted until human approves the ADR content.

---

## Error Handling

| Error                       | Recovery                                                   |
| --------------------------- | ---------------------------------------------------------- |
| Decision not yet made       | Draft as Proposed, note open questions                     |
| Supersedes existing ADR     | Link to it, update old ADR status to "Superseded by <new>" |
| Scope too broad for one ADR | Split into focused ADRs, one decision each                 |
| Missing alternatives        | Research at least 2 alternatives before drafting           |
