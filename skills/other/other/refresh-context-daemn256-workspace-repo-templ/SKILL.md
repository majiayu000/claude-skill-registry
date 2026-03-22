---
name: refresh-context
description: Update stale workspace context
---

# Refresh Context

Uses **Planner** (primary) with **Orchestrator** support. Verify and update the workspace context file when it may be outdated. Scans the codebase for changes and reconciles with documented state.

**Prerequisites:** Existing workspace context file, access to codebase

---

## Phase 1: Read Current Context

### Review Existing State

1. Read the existing workspace context file (`docs/workspace/context.md`)
2. Summarize what it contains
3. Note the last-updated timestamp

### Output

```markdown
## Context Anchors

- **Phase:** 1 — Read Current Context

## Current Context Summary

<summary of what the context file states>

- **Last updated:** <date if available>
- **Sections present:** <list>

## Next Step

Continue to codebase scan.

**Approval Required:** No
```

---

## Phase 2: Scan Codebase

### Detect Changes

1. Look for new directories or modules
2. Check for changed file patterns
3. Review updated configuration
4. Check for moved documentation
5. Verify convention adherence

### Output

```markdown
## Context Anchors

- **Phase:** 2 — Scan Codebase

## Scan Results

<findings from codebase scan>

## Next Step

Continue to inconsistency report.

**Approval Required:** No
```

---

## Phase 3: Report Inconsistencies

### Compare and Present

1. Compare current context against detected state
2. List items that need updating, removal, or verification
3. Highlight questions about ambiguous changes

### Output

```markdown
## Context Anchors

- **Phase:** 3 — Report Inconsistencies

## Detected Changes

| Item   | Current State       | Detected State   | Action                   |
| ------ | ------------------- | ---------------- | ------------------------ |
| <item> | <what context says> | <what was found> | Update / Remove / Verify |

## Questions

- <ambiguous change needing human input>

## Next Step

Awaiting human input before making changes.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not update the context file until human explicitly approves:

- Which items to update
- Which items to remove
- Answers to questions about ambiguous changes

---

## Phase 4: Apply Updates

### Update Context File

1. Apply approved corrections
2. Add new discoveries
3. Remove obsolete content
4. Update timestamp

### Output

```markdown
## Context Anchors

- **Phase:** 4 — Apply Updates

## Changes Applied

- Updated: <list>
- Added: <list>
- Removed: <list>

## Next Step

Context refreshed. No further action needed.

**Approval Required:** No
```

---

## Staleness Indicators

Signs that workspace context might be stale:

- References files that no longer exist
- Mentions patterns not seen in recent code
- Lists stack components that have changed
- Documentation links are broken
- Conventions don't match observed code

---

## Error Handling

| Error                              | Recovery                                   |
| ---------------------------------- | ------------------------------------------ |
| No workspace context file exists   | Offer to create one via /setup-workspace   |
| File has incompatible format       | Note format issues, propose migration      |
| Too many changes to review at once | Batch into sections, process incrementally |
