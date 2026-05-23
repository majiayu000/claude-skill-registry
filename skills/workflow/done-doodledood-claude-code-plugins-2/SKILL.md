---
name: done
description: 'Completion marker for the /do workflow. Outputs hierarchical execution summary showing Global Invariants respected and all Deliverables completed. Called by /verify after all criteria pass, not directly.'
user-invocable: false
---

# /done - Completion Marker

## Goal

Output a completion summary showing what was accomplished, organized by the Manifest hierarchy.

## Input

`$ARGUMENTS` = completion context (optional)

## What to Do

Read the execution log and manifest. Output a summary that shows:

1. **Intent** - What was the goal
2. **Global Invariants** - All respected
3. **Deliverables** - Each with its ACs, all passing
4. **Key changes** - Files modified, commits made
5. **Tradeoffs applied** - How preferences were used

## Output Format

```markdown
## Execution Complete

All global invariants pass. All acceptance criteria verified.

### Intent
**Goal:** [from manifest]

### Global Invariants
| ID | Description | Status |
|----|-------------|--------|
| INV-G1 | ... | PASS |

### Deliverables

#### Deliverable 1: [Name]
| ID | Description | Status |
|----|-------------|--------|
| AC-1.1 | ... | PASS |

**Key Changes:**
- [file] - [what changed]

---

### Tradeoffs Applied
| Decision | Preference | Outcome |
|----------|------------|---------|

### Files Modified
| File | Changes |
|------|---------|

---
Manifest execution verified complete.
```

## Principles

1. **Mirror manifest structure** - Hierarchy should match: Intent → Global Invariants → Deliverables
2. **Show evidence** - Link changes to deliverables, describe behavioral changes (not just file lists)
3. **Adapt detail to complexity** - Simple task = condensed output. Complex task = full hierarchy.
4. **Called by /verify only** - /done is the final step after /verify confirms all criteria pass. If the execution log doesn't show verification, something went wrong upstream.

## Medium Routing

When medium is non-local, /done output goes through the calling context (/verify → /do). No special routing needed — just produce the summary as normal.
