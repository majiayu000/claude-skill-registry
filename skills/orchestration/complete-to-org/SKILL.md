# Complete to Org Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-23

Update an org-mode task to DONE when its delegated bead epic completes, maintaining bidirectional consistency.

## When to Activate

Use this skill when:
- Bead epic with source_org_id reaches 100% completion
- Closing a spawned epic (created via spawn-to-beads)
- Need to update org planning layer after agent execution completes

## Core Principles

### 1. Callback Before Close

Trigger the org callback BEFORE closing the bead epic.

*Source reference is in the epic description; easier to access while epic is still open.*

### 2. Verify Source Exists

Confirm the source org task exists before attempting update.

*Org task may have been deleted or archived; graceful handling prevents errors.*

### 3. Use org-todo for State Change

Always use org-todo to transition to DONE, never direct property manipulation.

*org-edna triggers only fire through org-todo; direct manipulation breaks cascades.*

### 4. Idempotent Completion

Completing an already-DONE task should be a no-op, not an error.

*Callbacks may be triggered multiple times; idempotency prevents errors.*

### 5. Optional Annotation

Optionally add completion note with epic ID and summary.

*Audit trail of what executed and when aids future review.*

---

## Workflow

### Phase 1: Extract Source Reference

Find the source_org_id in the bead epic.

1. Query bead epic details using `bd show`
2. Parse description for `[source_org_id: <id>]` pattern
3. If not found, this is not a spawned epic - no callback needed
4. If found, capture the org-id for callback

**Outputs:** source_org_id or indication that callback not needed

```bash
# Extract source_org_id from epic description
source_id=$(bd show <epic-id> --json | jq -r '.description' \
  | grep -oP 'source_org_id: \K[^\]]+')

if [ -z "$source_id" ]; then
  echo "Not a spawned epic - no callback needed"
else
  echo "Source org ID: $source_id"
fi
```

### Phase 2: Verify Epic Completion

Confirm the epic is actually complete before callback.

1. Run `bd epic status` to check completion percentage
2. If not 100%, warn and optionally abort
3. If 100%, proceed with callback

**Outputs:** Completion percentage, go/no-go for callback

```bash
# Check epic completion status
bd epic status <epic-id>
# Look for "100%" or "Progress: X/X complete"
```

### Phase 3: Verify Org Task Exists

Confirm the source org task still exists and is in expected state.

1. Query org task by source_org_id
2. Check if task exists (may have been deleted/archived)
3. Check current state (should be WAITING if properly spawned)
4. If task doesn't exist, log warning and skip callback

**Outputs:** Task existence confirmation, current task state

```bash
result=$(emacsclient --eval '(beadsmith/agent-get-task "source-org-id")' \
  | sed 's/^"//;s/"$//' | sed 's/\\"/"/g')

if echo "$result" | jq -e '.success' > /dev/null; then
  echo "Task exists"
  echo "$result" | jq '.data.todo'
else
  echo "Task not found"
fi
```

### Phase 4: Complete Org Task

Transition the org task to DONE state.

1. Use `beadsmith/agent-complete-task` to mark DONE
2. This fires org-edna TRIGGER properties if any
3. Verify state change succeeded

**Outputs:** Completion confirmation, any triggered cascades

```bash
emacsclient --eval '(beadsmith/agent-complete-task "source-org-id")' \
  | sed 's/^"//;s/"$//' | sed 's/\\"/"/g' | jq .
```

### Phase 5: Archive and Close Epic

Now safe to close the bead epic and archive for audit trail.

1. Org callback complete
2. Archive epic data before closing (governance decision: indefinite retention)
3. Close epic normally
4. Reference link maintained in org task's DELEGATED_TO property for history

**Outputs:** Archived epic data, confirmation that callback complete, closed epic

```bash
# Archive epic data for audit trail
mkdir -p .beads/archive
bd export -o ".beads/archive/$(date +%Y%m%d)-<epic-id>.jsonl"

# Close the epic
bd close <epic-id> -r "All tasks complete. Org task updated. Archived."
```

**Archive Policy (Governance Decision 2026-01-23):**
- Epics archived indefinitely in `.beads/archive/`
- Disk space is cheap; audit trail is valuable
- Archived data enables historical analysis and debugging
- No automatic deletion

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| **Source Extraction** | Parsing description | `grep -oP 'source_org_id: \K[^\]]+'` | Extracts just the ID from bracketed format |
| **Idempotent Check** | Task might be DONE | Check state first; if DONE, return success | Prevents duplicate callback errors |

### Complete Callback Script

```bash
#!/bin/bash
epic_id="$1"

# Extract source
source_id=$(bd show "$epic_id" --json | jq -r '.description' \
  | grep -oP 'source_org_id: \K[^\]]+')

if [ -z "$source_id" ]; then
  echo "Not a spawned epic"
  exit 0
fi

# Verify epic complete
if ! bd epic status "$epic_id" | grep -q "100%"; then
  echo "Epic not 100% complete"
  exit 1
fi

# Complete org task
result=$(emacsclient --eval "(beadsmith/agent-complete-task \"$source_id\")" \
  | sed 's/^"//;s/"$//' | sed 's/\\"/"/g')

if echo "$result" | jq -e '.success' > /dev/null; then
  echo "Org task completed"
else
  echo "Failed: $(echo "$result" | jq -r '.error')"
  exit 1
fi
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Callback After Close** | Epic archived; harder to access description | Extract source and callback BEFORE closing |
| **Ignoring Missing Source** | Non-spawned epics cause errors | Gracefully skip if not spawned epic |
| **Direct TODO Property Set** | org-edna triggers don't fire | Use `agent-complete-task` or `org-todo` |
| **No Completion Verification** | Org shows DONE but work incomplete | Verify 100% epic completion first |
| **Silent Failures** | Inconsistent state between layers | Verify callback succeeded |

---

## Quality Checklist

Before completing:

- [ ] Source org ID extracted from epic description
- [ ] Epic verified at 100% completion
- [ ] Source org task verified to exist
- [ ] Org task completed via org-todo (not direct property)
- [ ] Completion verified successful
- [ ] Ready to close bead epic

---

## Examples

**Standard completion callback**

```bash
# Epic bd-a3f8 has finished all tasks
epic_id="bd-a3f8"

# 1. Extract source reference
source_id=$(bd show "$epic_id" --json | jq -r '.description' \
  | grep -oP 'source_org_id: \K[^\]]+')
# Returns: task-implement-auth

# 2. Verify epic complete
bd epic status "$epic_id"
# Shows: Progress: 8/8 complete (100%)

# 3. Verify org task exists
emacsclient --eval "(beadsmith/agent-get-task \"$source_id\")" | parse_json
# Shows task in WAITING state

# 4. Complete org task
emacsclient --eval "(beadsmith/agent-complete-task \"$source_id\")" | parse_json
# Returns: {"success": true}

# 5. Now close the epic
bd close "$epic_id" -r "All tasks complete. Org task updated."
```

**Non-spawned epic (no callback needed)**

```bash
# Epic bd-x1y2 was created directly, not from org
epic_id="bd-x1y2"

# 1. Check for source reference
source_id=$(bd show "$epic_id" --json | jq -r '.description' \
  | grep -oP 'source_org_id: \K[^\]]+')
# Returns: (empty)

# 2. No source_org_id means no callback needed
echo "Not a spawned epic - closing directly"

# 3. Close normally
bd close "$epic_id" -r "All tasks complete."
```

**Org task already completed**

```bash
# Human may have manually completed the org task
epic_id="bd-a3f8"
source_id="task-implement-auth"

# Check org task state
state=$(emacsclient --eval "(beadsmith/agent-get-task \"$source_id\")" \
  | parse_json | jq -r '.data.todo')
# Returns: DONE

# Task already DONE - callback is no-op
echo "Org task already complete - skipping callback"

# Close epic normally
bd close "$epic_id" -r "Complete. Org task was already DONE."
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `spawn-to-beads` | Inverse operation - spawn creates, this completes |
| `org-planning` | Target layer - tasks updated here |
| `beads-execute` | Execution completes, triggering this callback |

---

## References

- `planning/systems-analysis.md` - Layered architecture decision
- `docs/integration-architecture.md` - Full integration specification
- `spawn-to-beads` skill - The inverse operation
