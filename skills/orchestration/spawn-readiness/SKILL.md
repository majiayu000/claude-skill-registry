# Spawn Readiness Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-25

Validate that an org task is ready for delegation to beads execution layer.

## When to Activate

Use this skill when:
- Checking spawn readiness before delegation
- Validating a task for beads handoff
- Asking "is this task ready for beads?"
- Before invoking spawn-to-beads skill
- Quick validation before delegation

## Core Principles

### 1. Validation Is Informational

Output is READY or NOT_READY with specific deficiencies - no blocking prompts.

*Agent can decide whether to proceed or address deficiencies; validation doesn't gate execution.*

### 2. Quick Checklist

This is a lightweight validation, not a heavy refinement workflow.

*Keep it fast; if deep refinement is needed, that's a different process.*

### 3. Preview the Spawn

Show what epic would be created before committing.

*Allows quick sanity check without side effects.*

### 4. No Human Confirmation

Do not ask user to confirm - run validation and report results.

*This is pre-spawn validation, not a gate. User decides based on output.*

---

## Workflow

### Phase 1: Validate Org Task Existence

Confirm the org task exists and is accessible.

1. Query org task by provided ID
2. Verify task exists in org-mode
3. Extract basic task information

**Outputs:** Task existence confirmation, basic task data (heading, state)

```bash
result=$(emacsclient --eval '(beadsmith/agent-get-task "org-task-id")' \
  | sed 's/^"//;s/"$//' | sed 's/\\"/"/g')

if echo "$result" | jq -e '.success' > /dev/null; then
  echo "EXISTS"
else
  echo "NOT_FOUND"
fi
```

### Phase 2: Check Preconditions

Verify task meets all preconditions for delegation.

| Check | Description | Fail Message |
|-------|-------------|--------------|
| valid_id | Task has a valid org-id | Task lacks valid org-id |
| has_description | Task has description/body content | Task has no description - add context for agents |
| appropriate_state | Task is in TODO or NEXT state | Task is in wrong state (must be TODO or NEXT) |
| not_already_delegated | Task does not have DELEGATED_TO | Task already delegated to beads |

**Outputs:** List of passed checks, list of failed checks (if any)

### Phase 3: Preview Spawn

Show what epic would be created.

1. Extract heading as proposed epic title
2. Extract body as proposed epic description
3. Map org priority to bead priority:
   - A → P1
   - B → P2
   - C → P3
   - (none) → P2
4. Show preview without creating anything

**Outputs:** Proposed epic title, description (with source_org_id marker), priority

### Phase 4: Emit Verdict

Output final readiness verdict.

1. If all preconditions met → **READY**
2. If any precondition failed → **NOT_READY** with deficiency list
3. Include preview in both cases for context

**Outputs:** Verdict (READY or NOT_READY), deficiency list (if NOT_READY), epic preview

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Blocking on Validation** | Adds unnecessary gate; user can decide based on output | Output verdict and let caller decide |
| **Deep Refinement** | Scope creep; this should be quick | Just validate preconditions; refinement is separate |
| **Modifying State** | Validation should be read-only | Only read task state; spawn-to-beads does actual work |

---

## Quality Checklist

Before completing:

- [ ] Org task ID provided
- [ ] Task existence verified
- [ ] Task has valid org-id
- [ ] Task has description/body
- [ ] Task is in TODO or NEXT state
- [ ] Task not already delegated (no DELEGATED_TO)
- [ ] Preview generated showing proposed epic
- [ ] Verdict emitted (READY or NOT_READY)

---

## Examples

**Task ready for spawn**

```
=== Spawn Readiness Check ===

Task: Implement authentication system
ID: task-impl-auth
State: TODO

Preconditions:
  [PASS] Valid org-id
  [PASS] Has description
  [PASS] State is TODO or NEXT
  [PASS] Not already delegated

Preview:
  Epic Title: Implement authentication system
  Priority: P2 (no org priority set)
  Description: [source_org_id: task-impl-auth] JWT-based auth with...

VERDICT: READY

Next: Run spawn-to-beads skill to create epic
```

**Task not ready - already delegated**

```
=== Spawn Readiness Check ===

Task: Build API endpoints
ID: task-build-api
State: WAITING

Preconditions:
  [PASS] Valid org-id
  [PASS] Has description
  [FAIL] State is TODO or NEXT (actual: WAITING)
  [FAIL] Not already delegated (DELEGATED_TO: bd-x7y2)

VERDICT: NOT_READY

Deficiencies:
  1. Task is in WAITING state (must be TODO or NEXT)
  2. Task already delegated to bd-x7y2

Action: This task is already spawned to beads. Check bd epic status bd-x7y2
```

**Task not ready - no description**

```
=== Spawn Readiness Check ===

Task: Fix bug
ID: task-fix-bug
State: TODO

Preconditions:
  [PASS] Valid org-id
  [FAIL] Has description (task body is empty)
  [PASS] State is TODO or NEXT
  [PASS] Not already delegated

VERDICT: NOT_READY

Deficiencies:
  1. Task has no description - agents need context to execute

Action: Add description to org task, then retry validation
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `spawn-to-beads` | Run this skill before spawn-to-beads to validate readiness |
| `org-planning` | Uses org-planning queries to check task state |
| `beads-plan` | After spawn, beads-plan decomposes the epic |

---

## References

- `spawn-to-beads` skill - The skill that performs actual spawning
- `org-planning` skill - Querying org task state
