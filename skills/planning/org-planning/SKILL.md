# Org Planning Skill

> Version: 1.1.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-23

Agent-accessible project planning via org-mode with hierarchical structures, task dependencies, programmatic queries, and integration with beads execution layer.

## When to Activate

Use this skill when:
- Planning a project or querying task status
- Checking if tasks are blocked by dependencies
- Listing next actions or updating task states
- Managing task dependencies via org-edna
- Delegating tasks to beads execution layer
- Checking status of delegated tasks
- Working with the `planning/` directory
- Interacting with org-mode files programmatically

## Core Principles

### 1. Use org-todo for State Changes

Always use `(org-todo STATE)` to change task states, never direct property manipulation.

*org-edna triggers only fire through org-todo; direct property manipulation bypasses the dependency cascade system entirely.*

### 2. JSON Output for Agent Consumption

All programmatic queries should return JSON with `{success, data/error}` structure.

*Reliable parsing, consistent error handling, and clear success/failure signaling across shell boundaries.*

### 3. IDs Are Forever

Use org-id for stable task references; prefer UUIDs for agent-created tasks.

*File paths and line numbers change; org-id provides stable references that survive refactoring and archiving.*

### 4. Cache Awareness

org-ql caches results per-buffer keyed on query+action pairs.

*Actions must be pure/side-effect-free for reliable caching; cache invalidates only on buffer modification.*

### 5. Explicit Dependency Modeling

Use both BLOCKER and TRIGGER properties even when redundant.

*BLOCKER documents what blocks this task; TRIGGER documents what this task enables - bidirectional documentation aids understanding.*

### 6. Suppress Interactive Prompts

Wrap operations in let-bindings that disable note prompts and confirmations.

*Agent operations must complete without user interaction; prompts cause hangs in non-interactive contexts.*

### 7. Condition-Case Everything

Wrap all agent-facing functions in condition-case for error capture.

*Errors should be returned as data, not thrown as exceptions that break the calling agent.*

### 8. Delegation Awareness

Tasks delegated to beads execution layer use DELEGATED_TO property and WAITING state.

*Org-mode is the planning layer; beads is the execution layer. DELEGATED_TO creates bidirectional traceability; WAITING accurately reflects that the task awaits external completion.*

---

## Workflow

### Phase 1: Query Planning State

Retrieve current state of tasks, projects, or dependencies.

1. Determine query type - next actions, blocked tasks, by project, by state, overdue, scheduled
2. Select appropriate `beadsmith/agent-*` function or construct org-ql query
3. Execute via `emacsclient --eval`
4. Parse JSON response - strip outer quotes, unescape internal quotes
5. Check success field before using data

**Outputs:** JSON with task list including id, heading, todo state, tags, dates, blocker info; file and line references for each task

```elisp
;; List all NEXT actions
(beadsmith/agent-list-next-actions)

;; Custom query
(beadsmith/agent-query '(and (todo) (deadline :to 7)))
```

```bash
emacsclient --eval '(beadsmith/agent-list-next-actions)' \
  | sed 's/^"//;s/"$//' | sed 's/\\"/"/g' | jq .
```

### Phase 2: Check Task Dependencies

Determine if a task is blocked and by what.

1. Get task ID (from prior query or known identifier)
2. Call `beadsmith/agent-task-blocked-p` with the ID
3. Parse response for blocked status and blocking_tasks array
4. If blocked, optionally query status of blocking tasks

**Outputs:** Boolean blocked status, list of blocking task IDs if blocked, original BLOCKER property string

```elisp
(beadsmith/agent-task-blocked-p "task-id-here")
```

```bash
emacsclient --eval '(beadsmith/agent-task-blocked-p "task-id")' \
  | sed 's/^"//;s/"$//' | sed 's/\\"/"/g' | jq .
```

### Phase 3: Update Task State

Change a task's TODO state, potentially triggering cascades.

1. Verify task exists via `beadsmith/agent-get-task`
2. Check if task is blocked (for transitions to DONE)
3. Call `beadsmith/agent-set-todo-state` or `beadsmith/agent-complete-task`
4. Verify state change succeeded via response
5. Note that TRIGGER properties will fire automatically if completing

**Outputs:** Success/failure status, new state confirmation, side effects from triggers

```elisp
;; Set to specific state
(beadsmith/agent-set-todo-state "task-id" "NEXT")

;; Complete task (fires triggers)
(beadsmith/agent-complete-task "task-id")
```

```bash
emacsclient --eval '(beadsmith/agent-complete-task "task-id")' \
  | sed 's/^"//;s/"$//' | sed 's/\\"/"/g' | jq .
```

### Phase 4: Get Task Details

Retrieve full information about a specific task.

1. Call `beadsmith/agent-get-task` with known task ID
2. Parse response for all task properties
3. Use for displaying task info or making decisions

**Outputs:** Complete task record with heading, state, tags, dates, dependencies, location

```elisp
(beadsmith/agent-get-task "task-id-here")
```

### Phase 5: Create or Modify Tasks

Add new tasks or update existing task properties.

1. For new tasks - find insertion point, use `org-insert-heading`, set properties including ID
2. For modifications - locate via `org-id-find`, use `org-entry-put` for properties
3. Always call `org-id-add-location` after creating new IDs
4. Save buffer after modifications

**Outputs:** New task ID if created, confirmation of modification

```elisp
;; Create task with ID (at point in org buffer)
(org-insert-heading)
(insert "TODO New task heading")
(org-entry-put nil "ID" (org-id-new))
(org-id-add-location (org-entry-get nil "ID") (buffer-file-name))
(save-buffer)

;; Modify property
(org-with-point-at (org-id-find "task-id" 'marker)
  (org-entry-put nil "SCHEDULED" "<2026-01-25 Sat>")
  (save-buffer))
```

### Phase 6: Delegate to Beads Execution Layer

Hand off a task to the beads execution layer for agent swarm execution.

1. Evaluate if task is appropriate for delegation (see spawn-to-beads skill for criteria)
2. Use spawn-to-beads skill to create bead epic and establish bidirectional reference
3. Org task receives DELEGATED_TO property with bead epic ID
4. Org task transitions to WAITING state
5. When bead epic completes, complete-to-org skill updates org task to DONE

**Outputs:** Org task in WAITING state with DELEGATED_TO property, bead epic created with source_org_id reference

```elisp
;; Mark task as delegated (after bead epic created)
(org-with-point-at (org-id-find "task-id" 'marker)
  (org-entry-put nil "DELEGATED_TO" "bd-epic-id")
  (org-todo "WAITING")
  (save-buffer))
```

```bash
# Check if task is delegated
emacsclient --eval '(beadsmith/agent-get-task "task-id")' \
  | sed 's/^"//;s/"$//' | sed 's/\\"/"/g' \
  | jq '.data.delegated_to // "not delegated"'
```

### Phase 7: Query Delegated Tasks

Find tasks that are delegated to beads and check their status.

1. Query for tasks with DELEGATED_TO property
2. For each, the property value is the bead epic ID
3. Use `bd epic status` to check completion
4. If epic complete, trigger complete-to-org workflow

**Outputs:** List of delegated tasks with their bead epic IDs, completion status of each delegation

```elisp
;; Query all delegated tasks
(beadsmith/agent-query '(and (todo) (property "DELEGATED_TO")))
```

```bash
# Find all delegated tasks
emacsclient --eval '(beadsmith/agent-query (quote (and (todo) (property "DELEGATED_TO"))))' \
  | sed 's/^"//;s/"$//' | sed 's/\\"/"/g' | jq .
```

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| **Shell JSON Parsing** | Calling emacsclient from shell | `emacsclient --eval '(func)' \| sed 's/^"//;s/"$//' \| sed 's/\\"/"/g' \| jq .` | emacsclient wraps output in quotes; this extracts clean JSON |
| **Timeout Wrapper** | Production emacsclient calls | `timeout 30 emacsclient --eval '(func)' \|\| echo '{"success":false,"error":"Timeout"}'` | Prevents indefinite blocking |
| **Health Check** | Before operation sequences | `emacsclient --eval 't' >/dev/null 2>&1 \|\| exit 1` | Verify daemon is responsive |
| **Optimized org-ql Queries** | Performance on large files | Put optimizable predicates (todo, tags, property, deadline) first in 'and' expressions | These use fast regex preambles |
| **Hybrid Human-Readable IDs** | Tasks humans will reference | `(format "task-%s-%s" slug (substring (org-id-uuid) 0 8))` | Readability + uniqueness guarantee |
| **Dependency Chain Navigation** | Understanding task relationships | Query task, extract BLOCKER ids, recursively query those | Builds dependency graph |
| **Cascading Completion** | Task triggers others | Use `(org-todo "DONE")`, then verify targets via query | Triggers only fire through org-todo |
| **Batch Query Efficiency** | Multiple queries needed | Combine into single emacsclient call with progn | Amortizes connection overhead |
| **Delegation Handoff** | Task requires agent execution with parallelization or >2 hours effort | Use spawn-to-beads skill to create epic, set DELEGATED_TO property, transition to WAITING | Org-mode is for planning; beads is for agent swarm execution. Clear handoff prevents confusion |
| **Completion Callback** | Bead epic with source_org_id completes | Use complete-to-org skill to update org task to DONE | Maintains bidirectional consistency |
| **Human Override Warning** | Human completes org task with DELEGATED_TO set | Log warning; do not auto-cancel epic | Preserves epic data; surfaces potential orphan for weekly review |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Direct TODO Property Manipulation** | org-edna triggers never fire; cascades broken | Always use `(org-todo "DONE")` |
| **Assuming org-ql Results Are Fresh** | Cached results returned if buffer unchanged | Understand caching; force tick update if needed |
| **Human-Readable IDs Without Uniqueness** | ID collisions cause wrong task lookup | Use UUIDs or hybrid format with UUID suffix |
| **Ignoring Error Responses** | Operating on null/undefined data; silent failures | Always check success before accessing data |
| **Blocking on Interactive Prompts** | Agent hangs waiting for input forever | Wrap in let-bindings that suppress prompts |
| **Parsing Emacsclient Output as Raw JSON** | Parse error from quotes and escaping | Strip quotes and unescape with sed first |
| **Cold-Cache Performance Assumptions** | First lookup triggers full file scan | Pre-warm cache; design for occasional slow lookups |
| **Fire-and-Forget State Changes** | Silent failures; inconsistent state | Check response success; verify state if critical |
| **Tracking Execution in Org** | Org becomes cluttered; loses strategic clarity; duplicates bead state | Delegate to beads for execution; org tracks only planning-level state |
| **Orphaned Delegations** | Broken bidirectional reference; impossible to trace correctly | Always use spawn-to-beads skill which sets both sides atomically |

---

## Quality Checklist

Before completing:

- [ ] Using `beadsmith/agent-*` functions for all agent operations
- [ ] JSON responses parsed correctly (quote stripping, unescaping)
- [ ] Success field checked before accessing data
- [ ] Errors handled gracefully with informative messages
- [ ] State changes use org-todo, not direct property manipulation
- [ ] Interactive prompts suppressed in all code paths
- [ ] Task IDs are stable (org-id based, not file:line)
- [ ] org-ql queries have optimizable predicates first
- [ ] Timeout protection on emacsclient calls
- [ ] Daemon health verified before operation sequences
- [ ] Delegated tasks have DELEGATED_TO property and WAITING state
- [ ] Delegation uses spawn-to-beads skill (not manual property setting)
- [ ] Completed delegations update org via complete-to-org skill

---

## Examples

**Morning planning review**

```bash
# Check what's scheduled for today
emacsclient --eval '(beadsmith/agent-list-scheduled-today)' | parse_json

# Check for overdue items
emacsclient --eval '(beadsmith/agent-list-overdue)' | parse_json

# Get next actions
emacsclient --eval '(beadsmith/agent-list-next-actions)' | parse_json
```

**Complete a task and verify cascade**

```bash
# Complete the task
result=$(emacsclient --eval '(beadsmith/agent-complete-task "task-a")' | parse_json)

# Verify cascade - check if dependent task is now unblocked
status=$(emacsclient --eval '(beadsmith/agent-task-blocked-p "task-b")' | parse_json)

# task-b should now have blocked=false if task-a was its only blocker
```

**Find all blocked tasks and their blockers**

```bash
# Get tasks with BLOCKER property
blocked=$(emacsclient --eval '(beadsmith/agent-list-blocked)' | parse_json)

# For each, check what's actually blocking
for id in $(echo "$blocked" | jq -r '.data[].id'); do
  emacsclient --eval "(beadsmith/agent-task-blocked-p \"$id\")" | parse_json
done
```

**Custom query for high-priority tasks due this week**

```bash
emacsclient --eval '(beadsmith/agent-query 
  (quote (and (todo) 
              (priority "A") 
              (deadline :to 7))))' | parse_json
```

**Delegate task to beads and check status**

```bash
# 1. Identify task appropriate for delegation
task_id="task-implement-auth"

# 2. Use spawn-to-beads skill to create epic (see that skill for details)
# This returns the bead epic ID and updates the org task

# 3. Later, check delegated tasks status
emacsclient --eval '(beadsmith/agent-query 
  (quote (and (todo "WAITING") (property "DELEGATED_TO"))))' | parse_json

# 4. For each delegated task, check bead epic status
# bd epic status <epic-id>

# 5. When epic complete, complete-to-org skill updates org task
```

---

## API Reference

### Query Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `beadsmith/agent-query` | `(QUERY)` | Execute arbitrary org-ql query, return JSON |
| `beadsmith/agent-get-task` | `(ID)` | Get full details for task by org-id |
| `beadsmith/agent-list-next-actions` | `()` | All tasks in NEXT state |
| `beadsmith/agent-list-blocked` | `()` | All tasks with BLOCKER property |
| `beadsmith/agent-list-waiting` | `()` | All tasks in WAITING state |
| `beadsmith/agent-list-overdue` | `()` | Tasks with deadline before today |
| `beadsmith/agent-list-scheduled-today` | `()` | Tasks scheduled for today or earlier |

### Mutation Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `beadsmith/agent-complete-task` | `(ID)` | Mark task DONE, firing org-edna triggers |
| `beadsmith/agent-set-todo-state` | `(ID STATE)` | Set task to STATE (TODO, NEXT, WAITING, DONE, CANCELLED) |

### Dependency Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `beadsmith/agent-task-blocked-p` | `(ID)` | Check if task is blocked by incomplete dependencies |

### Response Format

All functions return JSON:

```json
{"success": true, "data": [...]}
{"success": false, "error": "Error message"}
```

---

## org-edna Dependency Syntax

### Finders (Target Selection)

| Syntax | Description |
|--------|-------------|
| `ids(id1 id2 ...)` | Tasks with specified org-ids |
| `previous-sibling` / `next-sibling` | Adjacent sibling headings |
| `siblings` | All siblings at same level |
| `ancestors` / `descendants` | Parent chain or child tree |
| `children` | Immediate children only |
| `self` | Current heading |
| `match("TAGS" SCOPE)` | Org-map-entries style matching |

### Conditions

| Syntax | Description |
|--------|-------------|
| `done?` / `!done?` | Target is/isn't in DONE state |
| `todo-state?(STATE)` | Target has specific TODO state |
| `has-property?("PROP" "VAL")` | Target has property value |

### Actions (for TRIGGER)

| Syntax | Description |
|--------|-------------|
| `todo!(STATE)` | Set TODO state |
| `scheduled!("DATE")` / `deadline!("DATE")` | Set planning dates (`.` = completion day, `+Nd` = relative) |
| `set-property!("PROP" "VAL")` | Set property value |
| `tag!("tag1:tag2")` | Apply tags |

### Consideration (Quantifiers)

| Syntax | Description |
|--------|-------------|
| `consider(all)` | Block only if ALL targets meet condition |
| `consider(any)` | Block if ANY target meets condition (default) |
| `consider(N)` | Block if at least N targets meet condition |

### Examples

```org
;; Block until both tasks complete
:BLOCKER: ids("task-a" "task-b")

;; When done, set next sibling to NEXT and schedule for today
:TRIGGER: next-sibling todo!(NEXT) scheduled!(".")
```

---

## TODO States

| State | Meaning |
|-------|---------|
| `TODO` | Task identified but not yet actionable |
| `NEXT` | Next action, ready to work on |
| `WAITING` | Blocked on external input or event (including delegation to beads) |
| `DONE` | Completed |
| `CANCELLED` | No longer needed |

---

## Integration Properties

| Property | Purpose | Example |
|----------|---------|---------|
| `DELEGATED_TO` | Bead epic ID when task delegated to execution layer | `bd-a3f8` |
| `BLOCKER` | org-edna blocking dependencies | `ids("task-a" "task-b")` |
| `TRIGGER` | org-edna completion triggers | `next-sibling todo!(NEXT)` |

## Human Override Behavior

**Governance Decision (2026-01-23):** When a human completes an org task that has DELEGATED_TO set, warn but take no automatic action.

### Why No Auto-Cancellation

- Bead epic may be partially complete with valuable work
- Auto-cancellation risks data loss
- Human override may be intentional (e.g., task no longer needed)
- Epic data preserved for audit trail

### Warning Pattern

When completing a task with DELEGATED_TO:

```elisp
;; Check before completing
(when (org-entry-get nil "DELEGATED_TO")
  (message "WARNING: Task has delegated epic %s - epic may need manual cleanup"
           (org-entry-get nil "DELEGATED_TO")))
```

### Weekly Review Process

During GTD weekly review, check for orphaned epics:

```bash
# Find DONE tasks with DELEGATED_TO still set
emacsclient --eval '(beadsmith/agent-query 
  (quote (and (todo "DONE") (property "DELEGATED_TO"))))' | parse_json

# For each, check if epic is still open
# If so, decide: close epic, or was completion a mistake?
```

Orphaned epics should be manually reviewed and either:
- Closed (work no longer needed)
- Continued (org completion was premature)
- Archived (for historical record)

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `spawn-readiness` | Use to validate org task before delegation |
| `spawn-to-beads` | Use when delegating org task to beads execution layer |
| `complete-to-org` | Called when bead epic with source_org_id completes |
| `beads-plan` | Used after spawn-to-beads to decompose the bead epic |
| `beads-execute` | Used by agents to execute beads within the epic |

---

## Infrastructure

| Component | Path |
|-----------|------|
| Daemon service | `~/.config/systemd/user/emacs.service` |
| Emacs config | `~/.config/emacs/init.el` |
| Planning directory | `~/src/beadsmith/planning/` |
| ID locations cache | `~/.config/emacs/.org-id-locations` |

### Prerequisites

- Emacs daemon running: `systemctl --user status emacs`
- org-ql and org-edna packages loaded
- Planning files in `~/src/beadsmith/planning/`

---

## References

- [org-ql GitHub](https://github.com/alphapapa/org-ql)
- [org-edna documentation](https://www.nongnu.org/org-edna-el/)
- [Org-mode manual](https://orgmode.org/manual/)
- GNU Emacs emacsclient manual
- Research synthesis from alphapapa/org-ql issues and discussions
- Research synthesis from org-edna community patterns
