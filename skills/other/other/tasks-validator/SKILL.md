---
name: tasks-validator
description: Phase 3.5 — Automatic tasks validation after generation. Detects circular dependencies, validates execution order, checks task sizing, verifies infra-before-feature ordering, validates AC coverage, and checks for test tasks. Generates tasks-validation.md in the state directory.
---

# Tasks Validator

Runs **automatically as Phase 3.5**, between Tasks generation and Implementation.
Purpose: catch execution plan problems before they cause implementation failures mid-sprint.

## Position in flow

```
[TechSpec Validation]
      ↓
Tasks generation
      ↓
[Tasks Validation]  ← THIS SKILL
      ↓
Implementation (per task)
```

## Entry conditions

- `tasks.md` must exist in `tasks/prd-{slug}/` (run Tasks generation first)
- `prd.md` must exist for AC coverage validation
- Generates `tasks-validation.md` and saves to `.claude/feature-state/{slug}/`
- Load if already exists (resume flow)
- Can be forced with `--revalidate`

---

## Validation 1: Dependency Graph — Circular Detection

### Build the graph

Parse the tasks table from `tasks.md`, extracting:
- Task ID (e.g., "Task 1", "1", "1.1")
- "Depends On" column values

Build an adjacency list:
```
Task 1 → []
Task 2 → [Task 1]
Task 3 → [Task 2, Task 5]
Task 4 → [Task 3, Task 1]
Task 5 → [Task 3]   ← CYCLE: 3→5→3
```

### Cycle detection algorithm

Use depth-first search (DFS) with visited + recursion-stack tracking:
1. For each unvisited node, run DFS
2. Mark node as "in recursion stack" when visiting
3. If DFS reaches a node that is "in recursion stack" → cycle detected

### Output

For each cycle detected:
- ❌ Blocker: "Circular dependency: Task A → Task B → ... → Task A"
- Propose resolution: remove the weakest dependency in the cycle (the one most likely to be an error)

### Auto-fix proposal

```
Circular dependency detected: Task 3 → Task 5 → Task 3

Option A: Remove "Task 5" from Task 3's dependencies
  (Task 3 runs before Task 5, as originally numbered)

Option B: Merge Task 3 and Task 5 into a single task
  (if they are genuinely interdependent)

Option C: Reorder — run Task 5 before Task 3
  (if Task 5 should logically precede Task 3)
```

---

## Validation 2: Execution Order vs Dependencies

### Check ordering violations

For each task, verify that all its declared dependencies have **lower** task numbers (or appear earlier in the list):

```
Task 4 says "Depends On: Task 6"
Task 4 is ordered BEFORE Task 6 → ❌ ORDER VIOLATION
```

### Auto-fix: Topological Sort

When ordering violations are detected, compute a valid topological execution order:

1. Build dependency graph (from Validation 1)
2. Run Kahn's algorithm (BFS-based topological sort):
   - Start with tasks that have no dependencies
   - Process each task after all its dependencies
3. Present the sorted order:

```
Suggested execution order:
1. Task 1 (no deps)
2. Task 3 (deps: Task 1)
3. Task 5 (deps: Task 1)
4. Task 2 (deps: Task 3, Task 5)
5. Task 4 (deps: Task 2)
6. Task 6 (deps: Task 4)
```

If the original order differs: ⚠️ Warning or ❌ Blocker depending on severity.
- Same logical groupings but different numbers → ⚠️ Warning
- Dependencies genuinely violated (will cause implementation failure) → ❌ Blocker

---

## Validation 3: Task Sizing

### Size heuristics

Evaluate each task based on the information in its description:

| Signals | Size | Action |
|---------|------|--------|
| "Create one file", "Add one method", 1-2 verbs | S | ✅ Pass |
| "Create model + service + tests", 3-5 files mentioned | M | ✅ Pass |
| "Implement entire module", 6-10 files, multiple domains | L | ⚠️ Warning: "Consider splitting if complexity grows" |
| "Cross-service", "includes migration", "UI + API + DB", 10+ files | XL | ❌ Blocker: "Must be split before execution" |

### XL task auto-split

When an XL task is detected, propose a split into 2-4 smaller tasks:

```
Task 5 (XL): "Implement complete notifications module — UI + API + Firestore + tests"

Proposed split:
  Task 5a: Create Firestore notification schema and data model
  Task 5b: Implement notification API endpoints
  Task 5c: Create notification UI components
  Task 5d: Write integration tests for notification flow
```

Present the split to the user before modifying `tasks.md`.

---

## Validation 4: Infra Before Feature

### Infrastructure task patterns

Identify tasks that set up infrastructure dependencies:

| Pattern | Category |
|---------|----------|
| "install dependency", "add to package.json", "npm install" | Dependency setup |
| "create migration", "update schema", "alter table", "add collection" | Schema/migration |
| "define interface", "create type", "add model" | Type definition |
| "configure", "initialize", "set up X client" | Service initialization |
| "create worktree", "set up environment" | Environment setup |

### Check ordering rule

For each feature task, verify that its infrastructure prerequisites appear before it:

```
Task 6: "Create Firestore connections collection" (schema task)
Task 2: "Implement ConnectionService using connections collection"
  → Task 2 depends on Task 6, but Task 6 comes AFTER Task 2 → ❌ ORDER VIOLATION
```

For each violation:
- ❌ Blocker if the dependency is explicit in "Depends On"
- ⚠️ Warning if the dependency is implicit (inferred from description)

---

## Validation 5: AC → Task Coverage

Cross-reference every Acceptance Criteria from `prd.md` with the task list:

### Coverage check

For each AC in the PRD:
1. Extract the AC text
2. Search task descriptions for implementation of that AC (by keyword match)
3. Mark as covered or missing

```markdown
| AC | Covered by Task | Status |
|----|-----------------|--------|
| AC-1: User can connect with trainer | Task 3 — ConnectionService.connect() | ✅ |
| AC-2: Connection stored in Firestore | Task 2 — Firestore schema | ✅ |
| AC-3: Trainer sees connected students list | Task 5 — CMS student list | ✅ |
| AC-4: User receives email notification | — | ❌ Missing |
```

### Missing AC coverage = Blocker

If any AC has no corresponding task:
- ❌ Blocker: "AC-{N}: '{text}' has no implementing task"
- Auto-suggest: "Add task: Implement {AC requirement}"

---

## Validation 6: Test Tasks Exist

Check if the task list includes any testing tasks:

### Test task patterns
Keywords that indicate a test task: `test`, `spec`, `validate`, `verify`, `unit test`, `integration test`, `e2e`, `write tests`, `add tests`.

### Classification
- **≥1 test task found** → ✅ Pass
- **No test tasks found** → ⚠️ Warning (non-blocking):
  ```
  ⚠️ No test tasks found in task list.
  Suggested additions:
  - Task N: Write unit tests for {main component}
  - Task N+1: Write integration tests for {main flow}
  ```

---

## Behavior

| Finding type | Effect |
|--------------|--------|
| ✅ Pass | Continue silently |
| ⚠️ Warning | Present to user, can be dismissed |
| ❌ Blocker | **Stop flow**. User must correct before implementation starts |

### User interaction for blockers

```
❌ Tasks Validation Failed — cannot start implementation

Blocker 1: Circular dependency detected
  Task 3 → Task 5 → Task 3
  Suggested fix: Remove "Task 5" from Task 3's dependencies

Blocker 2: Execution order violation
  Task 4 depends on Task 6, but Task 4 is listed before Task 6
  Suggested order: [1, 2, 3, 5, 6, 4]

Blocker 3: AC-4 ("User receives email notification") has no implementing task
  Suggested addition: "Implement email notification trigger on connection"

Would you like me to update tasks.md to fix these issues? [Yes / Let me fix manually / Show full report]
```

### User interaction for warnings only

```
⚠️ Tasks Validation — warnings found (non-blocking)

• Task 7 is size L — monitor for scope creep during implementation
• No test tasks found — add test tasks for better coverage
  Suggested: "Task 9: Write unit tests for ConnectionService"

Continue to implementation? [Yes, continue / Let me add test tasks first]
```

---

## Output: tasks-validation.md

Save to `.claude/feature-state/{slug}/tasks-validation.md`:

```markdown
## Tasks Validation Report

Generated: {timestamp}
Tasks: tasks/prd-{slug}/tasks.md

### ✅ Passed
- No circular dependencies detected
- All tasks ordered correctly (respects dependency graph)
- Infra tasks precede their dependents
- Test tasks present

### ⚠️ Warnings (non-blocking)
- Task 6 is size L — consider splitting if implementation gets complex

### ❌ Blockers (must fix before implementation)
- Circular dependency: Task 3 → Task 5 → Task 3
- Task 4 depends on Task 6 but is ordered before it
- AC-4 "User receives notification" has no corresponding task

### Dependency Graph
| Task | Depends On | Valid? |
|------|-----------|--------|
| Task 1 | — | ✅ |
| Task 2 | Task 1 | ✅ |
| Task 3 | Task 2, Task 5 | ❌ CYCLE |
| Task 4 | Task 6 | ❌ ORDER |
| Task 5 | Task 3 | ❌ CYCLE |
| Task 6 | Task 4 | ✅ |

### Suggested Execution Order
[Topological sort result after fixes]
Task 1 → Task 2 → Task 4 → Task 6 → Task 3/5

### Task Sizes
| Task | Description (excerpt) | Estimated Size |
|------|----------------------|----------------|
| Task 1 | Create User type | S |
| Task 5 | Full notification module | XL ❌ |
| Task 7 | Implement CMS list view | L ⚠️ |

### AC Coverage
| AC | Covered by Task | Status |
|----|-----------------|--------|
| AC-1 | Task 3 | ✅ |
| AC-4 | — | ❌ Missing |

### Verdict
BLOCKED — fix 3 blocker(s) before starting implementation.
```

---

## Integration with implementation

When `tasks-validation.md` exists and has no blockers:
- spec-executor reads the Suggested Execution Order for task sequencing
- Any XL tasks proposed to be split must be reflected in the actual task list before execution begins
- AC Coverage matrix is used during implementation to confirm each AC is addressed
