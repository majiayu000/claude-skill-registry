---
name: evolve
description: Turn a repeated failure pattern into a system improvement. Outputs a concrete proposal for constraints, docs, or automation.
---

# Evolve

Convert repeated mistakes into rules or automation. Requires 2+ occurrences with evidence.

## Inputs

Ask the user for:
- What happened (describe the failure)
- How many times (must be 2+ across sessions or PRs)
- Evidence (PR/issue links or excerpts)
- Where it should have been caught (tooling, docs, invariant)

## Decision hierarchy (smallest effective change)

1. **Automate** — Can tooling enforce it (lint rule, CI check, pre-commit hook)? If yes, propose automation first.
2. **Tier 1 constraint** — Applies to all code, critical to enforce? Add to AGENTS.md invariants.
3. **Tier 2 guidance** — System-specific, helpful but not critical? Add to the relevant doc in `docs/`.
4. **Reference only** — Best practice but not enforceable? Add as a comment or reference doc.

## Output format

```
## System Evolution Proposal
### Failure Pattern
What: <description>
Frequency: <X> times across <Y> PRs/sessions
Evidence: <links or excerpts>
### Decision: AUTOMATION | TIER 1 | TIER 2 | REFERENCE
Rationale: <1-2 sentences>
### Proposed Change
Location: <exact file path + section>
Proposed addition:
  <exact text to add — use positive constraints>
### Implementation Steps
1. <what to modify>
2. <validation needed>
3. <PR creation>
```

## Notes

- Use positive language ("Do X", not "Don't do Y").
- Do not modify files until the user approves the proposal.
- Prefer automation when possible — enforced beats documented.
