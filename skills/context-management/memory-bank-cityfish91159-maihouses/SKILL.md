---
name: memory_bank
description: Establishes a persistent "Long-Term Memory" file to prevent context amnesia across sessions.
allowed-tools: Read, Edit, Write
---

# Memory Bank Protocol

## 1. The Core Rule
**"Read First, Write Last."**
- **Start of Task**: You MUST read `MEMORY.md` (at project root) to understand the project's current state, constraints, and architecture.
- **End of Task**: You MUST update `MEMORY.md` if you have:
    - Added a new feature.
    - Changed the architecture.
    - Discovered a new bug or constraint.

## 2. File Structure Constraint
Your `MEMORY.md` updates must roughly follow this template to maintain readability:

```markdown
## 1. Active Context
- **Goal**: [Current Objective]
- **Status**: [Progress]

## 2. Architecture & Tech Stack
- [Key tech decisions]

## 3. Known Issues & Technical Debt
- [List of things that are broken or hacky]

## 4. Operational Rules
- [Do's and Don'ts specific to this project]
```

## 3. Maintenance Triggers
- **New Pattern**: If you implement a new pattern (e.g., "All lists must be virtualized"), add it to `Operational Rules`.
- **Bug Hunt**: If you spend >10 mins debugging something, write the "Cause & Fix" in `Known Issues` so the next agent doesn't suffer.
- **Schema Change**: If `api/` changes, update `Architecture`.

## 4. Verification Checklist
- [ ] Did I read `MEMORY.md` at the start?
- [ ] Did I verify if my plan conflicts with "Known Issues"?
- [ ] Did I update "Active Context" to reflect my completed work?
