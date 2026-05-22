---
name: architecture-decision
description: Document architectural choices
role_groups: [engineering, leadership]
jtbd: |
  Architecture decisions get made in meetings and lost. This provides an ADR template, 
  prompts for context/options/decision, links to related projects, and saves to 
  06-Resources/ so future engineers understand why choices were made.
time_investment: "20-30 minutes per decision"
---

## Purpose

Document architecture decisions with context and rationale using Architecture Decision Records (ADR).

## Usage

- `/architecture-decision [topic]` - Document specific architecture decision

---

## Steps

1. **Prompt for decision context:**
   - What problem are we solving?
   - What constraints exist?

2. **Gather options considered:**
   - Option 1: Description, pros/cons
   - Option 2: Description, pros/cons
   - Option 3: Description, pros/cons

3. **Document decision made:**
   - Which option chosen
   - Why this option
   - Trade-offs accepted

4. **Link to related context:**
   - Related projects
   - Implementation notes

5. **Create ADR document** in 06-Resources/Architecture_Decisions/

---

## Output Format

```markdown
# ADR: [Title]

**Date:** [Today]
**Status:** Accepted
**Deciders:** [Names]

## Context
[What problem are we solving? What constraints?]

## Options Considered

### Option 1: [Name]
**Pros:**
- [Pro 1]

**Cons:**
- [Con 1]

### Option 2: [Name]
[Same structure]

## Decision
We chose [Option] because [reasoning].

## Trade-offs
- [Trade-off accepted]

## Implementation Notes
[How to implement this decision]
```
