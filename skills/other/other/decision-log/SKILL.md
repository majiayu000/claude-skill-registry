---
name: decision-log
description: Document major decisions made
role_groups: [leadership]
jtbd: |
  Important decisions get made and the context is lost. This provides a decision 
  template, prompts for context/options/rationale, links to supporting materials, 
  and saves to a searchable decision log so you can reference why choices were made.
time_investment: "15-20 minutes per decision"
---

## Purpose

Maintain searchable log of major decisions with full context and rationale.

## Usage

- `/decision-log [decision]` - Document specific decision
- `/decision-log list` - View all logged decisions

---

## Steps

1. **Prompt for decision details:**
   - What was decided?
   - What were the options?
   - Who was involved?

2. **Document context:**
   - Why was this decision needed?
   - What factors influenced it?
   - What information was considered?

3. **Capture rationale:**
   - Why this choice?
   - What trade-offs were accepted?
   - What risks acknowledged?

4. **Save decision record** in 06-Resources/Decisions/

---

## Output Format

```markdown
# Decision: [Title]

**Date:** [Today]
**Deciders:** [Names]
**Status:** Decided

## Context
[Why was this decision needed?]

## Options Considered
1. [Option 1] - Pros/Cons
2. [Option 2] - Pros/Cons

## Decision
We chose [Option] because [rationale].

## Trade-offs Accepted
- [Trade-off 1]

## Follow-up Actions
- [ ] [Action 1] - Owner: [Name]
```
