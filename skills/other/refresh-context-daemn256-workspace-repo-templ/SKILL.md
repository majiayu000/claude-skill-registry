---
name: refresh-context
description: Update stale workspace context.
---

# Refresh Context

The Planner drives this workflow with Orchestrator support. Verify and update the workspace context file when it may be outdated by scanning the codebase for changes and reconciling with documented state.

**Prerequisites:** Existing workspace context file, access to codebase.

---

## Phase 1: Read Current Context

Understand what the workspace context currently states.

### Steps

1. Read the existing workspace context file
2. Summarize what it contains
3. Note the last-updated timestamp

---

## Phase 2: Scan Codebase

Detect changes since last context refresh.

### Steps

1. Look for new directories or modules
2. Check for changed file patterns
3. Review updated configuration
4. Check for moved documentation
5. Verify convention adherence

---

## Phase 3: Report Inconsistencies

Present findings for human review.

### Steps

1. Compare current context against detected state
2. List items that need updating, removal, or verification
3. Highlight questions about ambiguous changes

### Staleness Indicators

- References files that no longer exist
- Mentions patterns not seen in recent code
- Lists stack components that have changed
- Documentation links are broken
- Conventions don't match observed code

### Output

```markdown
## Context Anchors

- **Phase:** Report Inconsistencies

## Inconsistencies Found

| Item   | Current State | Detected State | Action Needed          |
| ------ | ------------- | -------------- | ---------------------- |
| <item> | <current>     | <detected>     | <update/remove/verify> |

## Questions

- <ambiguous change needing input>

## Next Step

Approve changes before applying.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Await human input before making changes.

---

## Phase 4: Apply Updates

Update the workspace context file with approved changes.

### Steps

1. Apply approved corrections
2. Add new discoveries
3. Remove obsolete content
4. Update timestamp

### Output

```markdown
## Changes Applied

- Updated: <list>
- Added: <list>
- Removed: <list>

## Next Step

Context refreshed.

**Approval Required:** No
```

---

## Error Handling

| Error                              | Recovery                                   |
| ---------------------------------- | ------------------------------------------ |
| No workspace context file exists   | Offer to create one via setup workflow     |
| File has incompatible format       | Note format issues, propose migration      |
| Too many changes to review at once | Batch into sections, process incrementally |
