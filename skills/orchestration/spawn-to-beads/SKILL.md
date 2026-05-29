# Spawn to Beads Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-23

Delegate an org-mode task to the beads execution layer by creating a bead epic with bidirectional references.

## When to Activate

Use this skill when:
- Delegating an org task to beads execution
- Creating a bead epic from an org-mode task
- Handing off work to agent swarm execution
- Task requires parallelization or >2 hours effort

## Core Principles

### 1. Bidirectional References Are Mandatory

Both sides of the handoff must reference the other - org task gets DELEGATED_TO, bead epic gets source_org_id.

*Without bidirectional references, completion callbacks fail and state becomes inconsistent.*

### 2. Atomic Handoff

Create the bead epic and update the org task in a single logical operation.

*Partial state (epic without org update, or vice versa) creates orphaned references.*

### 3. Preserve Task Context

Transfer relevant context from org task to bead epic description.

*Agents executing the epic need to understand the original intent and constraints.*

### 4. WAITING State Is Accurate

Org task in WAITING state correctly reflects that it awaits external completion.

*WAITING is semantically correct - the task is blocked on the bead epic completing.*

### 5. Delegation Criteria Matter

Not all tasks should be delegated - evaluate appropriateness before spawning.

*Simple tasks executed directly are more efficient than the overhead of bead coordination.*

---

## Workflow

### Phase 1: Evaluate Delegation Appropriateness

Determine if this task should be delegated to beads.

1. Check task complexity - estimated effort >2 hours favors delegation
2. Check parallelization potential - multiple independent subtasks favor delegation
3. Check agent-appropriateness - coding tasks favor delegation, external dependencies disfavor
4. If criteria not met, execute directly in org-mode without spawning beads

**Outputs:** Go/no-go decision on delegation, reasoning for the decision

**Delegation Criteria:**

| Factor | Delegate | Execute Directly |
|--------|----------|------------------|
| Effort | >2 hours | <1 hour |
| Subtasks | 3+ independent | 0-2 |
| Nature | Coding, automation | External calls, human coordination |
| Parallelization | Benefits from multiple agents | Sequential only |

### Phase 2: Extract Task Information

Read the org task to gather information for the epic.

1. Query org task by ID to get full details
2. Extract heading as epic title
3. Extract body/description for epic description
4. Note any relevant properties (priority, tags, etc.)
5. Capture the org-id for the source reference

**Outputs:** Epic title, epic description (prefixed with source_org_id), priority mapping

```bash
emacsclient --eval '(beadsmith/agent-get-task "org-task-id")' \
  | sed 's/^"//;s/"$//' | sed 's/\\"/"/g' | jq .
```

### Phase 3: Create Bead Epic

Instantiate the bead epic with source reference.

1. Construct epic title from org heading
2. Construct epic description with source_org_id marker at the start
3. Map org priority to bead priority (A->P1, B->P2, C->P3)
4. Create epic using `bd create`
5. Capture the returned epic ID

**Outputs:** Bead epic ID, confirmation of creation

```bash
# Create epic with source reference in description
bd create "Epic Title from Org" -t epic -p 1 \
  -d "[source_org_id: org-task-id] Original description from org task..."
```

**Source Reference Format:** `[source_org_id: <org-id>]` at start of description

### Phase 4: Update Org Task

Set DELEGATED_TO property and transition to WAITING.

1. Locate org task by ID
2. Set DELEGATED_TO property to the bead epic ID
3. Transition task to WAITING state using org-todo
4. Save the buffer
5. Verify the update succeeded

**Outputs:** Org task in WAITING state, DELEGATED_TO property set

```elisp
;; Update org task with delegation info
(org-with-point-at (org-id-find "org-task-id" 'marker)
  (org-entry-put nil "DELEGATED_TO" "bd-epic-id")
  (org-todo "WAITING")
  (save-buffer))
```

### Phase 5: Verify Bidirectional References

Confirm both sides of the handoff are correctly linked.

1. Query org task to verify DELEGATED_TO is set
2. Query bead epic to verify source_org_id is in description
3. If either fails, roll back and report error

**Outputs:** Verification status, both IDs confirmed linked

```bash
# Verify org side
emacsclient --eval '(beadsmith/agent-get-task "org-task-id")' \
  | grep -q "DELEGATED_TO" && echo "Org: OK" || echo "Org: MISSING"

# Verify bead side
bd show bd-epic-id --json | jq -r '.description' \
  | grep -q "source_org_id" && echo "Bead: OK" || echo "Bead: MISSING"
```

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| **Priority Mapping** | Transferring priority | A->P1, B->P2, C->P3, none->P2 | Maintains relative importance |
| **Source Reference Format** | Embedding org-id | `[source_org_id: <id>]` at start of description | Easily parseable, visible, survives edits |
| **Atomic Handoff** | Production use | Create epic first, update org only if succeeded | Epic creation can fail; don't update org prematurely |

### Atomic Handoff Script

```bash
# Create epic first
epic_id=$(bd create "$title" -t epic -p "$priority" \
  -d "[source_org_id: $org_id] $description" --json | jq -r '.id')

# Update org only if epic creation succeeded
if [ -n "$epic_id" ]; then
  emacsclient --eval "(progn
    (org-with-point-at (org-id-find \"$org_id\" 'marker)
      (org-entry-put nil \"DELEGATED_TO\" \"$epic_id\")
      (org-todo \"WAITING\")
      (save-buffer)))"
fi
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **One-Sided Reference** | Orphaned reference; completion callback fails | Complete both sides in single operation |
| **Direct State Setting** | org-edna triggers don't fire; state machine bypassed | Always use `(org-todo "WAITING")` |
| **Delegating Trivial Tasks** | Coordination overhead exceeds execution time | Execute trivial tasks directly |
| **Losing Context** | Agents lack information to execute correctly | Transfer full context to epic description |
| **Forgetting Verification** | Silent failures leave inconsistent state | Always verify bidirectional references |

---

## Quality Checklist

Before completing:

- [ ] Task evaluated against delegation criteria
- [ ] Org task details extracted completely
- [ ] Bead epic created with source_org_id in description
- [ ] Org task DELEGATED_TO property set to epic ID
- [ ] Org task transitioned to WAITING state via org-todo
- [ ] Bidirectional references verified
- [ ] Ready to use beads-plan skill to decompose the epic

---

## Examples

**Delegate authentication implementation**

```bash
# 1. Have org task "Implement user authentication"
org_id="task-implement-auth"

# 2. Check delegation criteria - this is >2 hours, parallelizable
# Decision: delegate

# 3. Extract task info
task_info=$(emacsclient --eval "(beadsmith/agent-get-task \"$org_id\")" | parse_json)
title=$(echo "$task_info" | jq -r '.data.heading')
description="JWT-based auth with login, logout, and session management"

# 4. Create bead epic
epic_id=$(bd create "$title" -t epic -p 1 \
  -d "[source_org_id: $org_id] $description" --json | jq -r '.id')
# Returns: bd-a3f8

# 5. Update org task
emacsclient --eval "(progn
  (org-with-point-at (org-id-find \"$org_id\" 'marker)
    (org-entry-put nil \"DELEGATED_TO\" \"$epic_id\")
    (org-todo \"WAITING\")
    (save-buffer)))"

# 6. Verify
# Org task now in WAITING with DELEGATED_TO: bd-a3f8
# Epic bd-a3f8 has [source_org_id: task-implement-auth] in description

# 7. Next: use beads-plan skill to decompose bd-a3f8 into tasks
```

**Decide not to delegate**

```bash
# 1. Have org task "Fix typo in README"
org_id="task-fix-typo"

# 2. Check delegation criteria
# - Effort: <30 minutes
# - Parallelization: none
# - Agent-appropriate: yes but trivial
# Decision: execute directly

# 3. Just do the work in org-mode
# Edit README.md, fix typo

# 4. Mark org task DONE
emacsclient --eval "(beadsmith/agent-complete-task \"$org_id\")"

# No beads involved - appropriate for trivial tasks
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `spawn-readiness` | Use before spawn to validate org task is ready |
| `org-planning` | Source layer - tasks originate here |
| `beads-plan` | Use after spawn to decompose epic |
| `beads-execute` | Use to execute tasks within epic |
| `complete-to-org` | Callback when epic completes |

---

## References

- `planning/systems-analysis.md` - Layered architecture decision
- `docs/integration-architecture.md` - Full integration specification
- `docs/workflow-decision-guide.md` - Delegation criteria details
