---
name: create-tdd-tasks
description: Transform SDD tasks into test-first TDD task pairs. Reads existing tasks from /create-tasks and generates paired test tasks with RED-GREEN dependencies. Use when user says "create tdd tasks", "add tdd pairs", "convert to tdd", or wants to apply test-first ordering to SDD tasks.
argument-hint: "[--task-group <group>]"
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, AskUserQuestion, TaskCreate, TaskGet, TaskList, TaskUpdate
---

# Create TDD Tasks Skill

Transform existing SDD implementation tasks into test-first TDD task pairs. For each implementation task, this skill creates a paired test task that must complete first, enforcing test-first development at the pipeline level.

This skill bridges the SDD pipeline (`/create-tasks`) and TDD execution (`/execute-tdd-tasks`), converting a standard task list into one where every implementation task is preceded by a failing-test-writing task.

**CRITICAL: Complete ALL 8 phases.** The workflow is not complete until Phase 8: Report is finished. After completing each phase, immediately proceed to the next phase without waiting for user prompts.

## Core Principles

1. **Test-first at the pipeline level** -- Every implementation task gets a paired test task that blocks it. Tests are written before implementation begins.
2. **Preserve existing dependencies** -- TDD pairs are inserted into the existing SDD dependency chain without breaking any original relationships.
3. **Merge mode awareness** -- Re-running this skill on a task list that already has TDD pairs detects and skips existing pairs instead of creating duplicates.
4. **Criteria-to-tests conversion** -- Acceptance criteria from SDD tasks are converted into test descriptions for the paired test task.
5. **Minimal metadata additions** -- Only `tdd_mode`, `tdd_phase`, and `paired_task_id` are added. All existing metadata is preserved.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

- Preview confirmation -> AskUserQuestion
- Anomaly resolution -> AskUserQuestion
- Error recovery options -> AskUserQuestion

Text output should only be used for:
- Presenting TDD pair previews and summaries
- Reporting completion status
- Displaying dependency chain visualizations

**NEVER do this** (asking via text output):
```
Should I proceed with creating 12 TDD task pairs?
1. Yes
2. No
```

**ALWAYS do this** (using AskUserQuestion tool):
```yaml
AskUserQuestion:
  questions:
    - header: "Confirm TDD Pair Creation"
      question: "Ready to create 12 TDD task pairs?"
      options:
        - label: "Yes, create pairs"
          description: "Create test tasks and set TDD dependencies"
        - label: "Show details"
          description: "See full list of pairs before creating"
        - label: "Cancel"
          description: "Don't create TDD pairs"
      multiSelect: false
```

### Plan Mode Behavior

**CRITICAL**: This skill transforms tasks, NOT creates an implementation plan. When invoked during Claude Code's plan mode:

- **DO NOT** create a plan for how to implement TDD
- **DO NOT** defer task transformation to an "execution phase"
- **DO** proceed with the full TDD task generation workflow immediately
- **DO** create test tasks using TaskCreate as normal

The TDD task pairs are planning artifacts themselves -- generating them IS the planning activity.

### Soft Dependency on sdd-tools

This skill is part of the `tdd-tools` plugin and works with agents in the same plugin (`tdd-executor`, `test-writer`). It bridges the SDD pipeline (`/create-tasks` from `sdd-tools`) and TDD execution (`/execute-tdd-tasks`). The `sdd-tools` plugin is expected to be installed since TDD tasks are generated from SDD tasks created by `/create-tasks`.

---

## Phase 1: Validate & Load References

**Goal:** Verify prerequisites and load reference materials.

### Step 1: Parse Arguments

Check `$ARGUMENTS` for optional `--task-group` filter:
- If `--task-group <group>` is present, extract the group name for filtering
- If no arguments provided, process all tasks

### Step 3: Load Reference Files

Read the TDD decomposition and dependency reference files:

1. `references/tdd-decomposition-patterns.md` -- Task pairing rules, naming conventions, metadata, merge mode detection
2. `references/tdd-dependency-rules.md` -- Dependency insertion algorithm, circular dependency detection and breaking

---

## Phase 2: Read Existing Tasks

**Goal:** Load the current task list and identify tasks to transform.

### Step 1: Get All Tasks

Use `TaskList` to retrieve all current tasks.

### Step 2: Apply Group Filter

If `--task-group` was specified:
- Filter to only tasks where `metadata.task_group` matches the specified group
- Tasks outside the group are not modified

If no `--task-group` specified:
- Process all tasks regardless of group

### Step 3: Validate Task List

Handle empty/missing states:

**Empty task list (no tasks at all):**
```
No tasks found. Please run /create-tasks first to generate implementation tasks from a spec.

Usage:
  /agent-alchemy-sdd:create-tasks <spec-path>
```

**No tasks matching --task-group filter:**
```
No tasks found for group "{group}".

Available task groups:
- {group1} ({n} tasks)
- {group2} ({n} tasks)

Try: /create-tdd-tasks --task-group {group1}
```

### Step 4: Classify Tasks

For each task, determine if it should receive a TDD pair:

**Eligible for TDD pairing:**
- Implementation tasks (subjects like "Create X", "Implement X", "Build X", "Add X")
- Business logic tasks
- API/endpoint tasks
- Data model tasks
- UI/frontend tasks

**Skip (no TDD pair created):**
- Tasks already marked with `tdd_mode: true` in metadata
- Test tasks (subjects like "Add tests for X", "Write tests for X", or tasks with `test` in `task_uid`)
- Configuration/setup tasks (subjects like "Configure X", "Set up X")
- Documentation tasks (subjects like "Document X", "Write docs for X")

Record the classification for each task: eligible, skipped (with reason).

---

## Phase 3: Detect Existing TDD Pairs (Merge Mode)

**Goal:** Identify tasks that already have TDD pairs to avoid duplication.

### Detection Algorithm

For each eligible task, check if it already has a TDD pair using these 4 signals (any match means paired):

1. **Metadata check**: Task has `tdd_mode: true` in metadata
2. **Paired task check**: Task has `paired_task_id` in metadata, and the paired task exists in the task list
3. **UID check**: A task exists with `task_uid` equal to this task's `task_uid` + `:red`
4. **Subject check**: A task with subject `"Write tests for {this task's subject}"` exists in the same `task_group`

### Merge Behavior

For tasks with existing TDD pairs:

| Existing Pair Status | Action |
|---------------------|--------|
| Both tasks pending | Skip -- pair already exists |
| Test completed, impl pending | Skip -- pair progressing normally |
| Test completed, impl completed | Skip -- pair fully done |
| Test completed, impl in_progress | Skip -- pair in progress |
| Test pending, impl completed | Flag as anomaly -- impl completed without tests |
| Only impl exists, test missing | Treat as unpaired -- create the test task |
| Only test exists, impl missing | Flag as orphan -- ask user |

### Report Merge Status

If any existing pairs detected:

```
TDD PAIR STATUS:
- {n} tasks already have TDD pairs (will skip)
- {m} tasks need TDD pairs (will create)
- {k} anomalies detected (need user input)
```

If anomalies exist, use AskUserQuestion to resolve each one:

```yaml
AskUserQuestion:
  questions:
    - header: "TDD Pair Anomaly"
      question: "Task #{id} '{subject}' was completed without its test task. What should I do?"
      options:
        - label: "Create test task anyway"
          description: "Add a test task for documentation/coverage purposes"
        - label: "Skip this task"
          description: "Leave it as-is without a test pair"
      multiSelect: false
```

---

## Phase 4: Generate Test Tasks

**Goal:** Create test task definitions for each eligible unpaired implementation task.

For each eligible task that needs a TDD pair, generate a paired test task.

### Step 1: Determine Test Task Subject

Follow the naming convention:
```
"Write tests for {original task subject}"
```

Examples:
- "Create User data model" -> "Write tests for Create User data model"
- "Implement POST /auth/login endpoint" -> "Write tests for Implement POST /auth/login endpoint"

### Step 2: Infer Test File Path

Determine the test file path based on the implementation task context:
- If implementation task references source files, derive test file path from project conventions
- Common patterns: `src/foo.ts` -> `tests/foo.test.ts`, `src/foo.py` -> `tests/test_foo.py`
- If no source files referenced, use the task subject to infer a path

### Step 3: Detect Test Framework

Determine the test framework using project detection:
1. Check for config files: `jest.config.*`, `vitest.config.*`, `pytest.ini`, `pyproject.toml`, `setup.cfg`
2. Check existing test files for import patterns
3. Check `package.json` for test dependencies
4. Default to the most common framework for the detected language

### Step 4: Convert Acceptance Criteria to Test Descriptions

**If the implementation task HAS acceptance criteria** (`**Acceptance Criteria:**` section):

Convert each criterion into a test description:

```markdown
**Test Descriptions:**

_From Functional Criteria:_
- [ ] Test that {criterion rephrased as test assertion}

_From Edge Cases:_
- [ ] Test that {edge case rephrased as test assertion}

_From Error Handling:_
- [ ] Test that {error scenario rephrased as test assertion}

_From Performance:_ (if applicable)
- [ ] Test that {performance target as measurable assertion}
```

**If the implementation task LACKS acceptance criteria:**

Generate basic test descriptions from the subject and description:

1. Parse the subject for intent ("Create X" -> test X exists and has expected structure)
2. Extract testable statements from description ("should...", "must...", "returns...", "validates...")
3. Generate minimal test descriptions:

```markdown
**Test Descriptions:**

_Inferred from task description:_
- [ ] Test that {subject entity} can be created/initialized
- [ ] Test that {subject entity} has expected structure/interface
- [ ] Test that {described behavior} works as described
```

### Step 5: Build Test Task Definition

Assemble the complete test task:

```
subject: "Write tests for {original subject}"
description: |
  Write failing tests for: {original task subject}

  Test file: {inferred test file path}
  Test framework: {detected framework}
  Original task: #{original_task_id}

  {test descriptions from Step 4}

  **Acceptance Criteria:**

  _Functional:_
  - [ ] All test descriptions converted into runnable test functions
  - [ ] Tests follow project test conventions (naming, structure, fixtures)
  - [ ] Tests are discoverable by the test runner
  - [ ] Tests fail when run without implementation (RED state)

  _Edge Cases:_
  - [ ] Tests handle import errors gracefully when implementation module does not exist

  _Error Handling:_
  - [ ] Test file is syntactically valid even when implementation is missing

  Source: {original source reference}
activeForm: "Writing tests for {original subject}"
metadata:
  tdd_mode: true
  tdd_phase: "red"
  paired_task_id: "{original_task_id}"
  priority: {inherited from original}
  complexity: {S or M -- test files are typically smaller}
  source_section: {inherited from original}
  spec_path: {inherited from original}
  feature_name: {inherited from original}
  task_uid: "{original_task_uid}:red"
  task_group: {inherited from original}
```

### Step 6: Plan Implementation Task Updates

For each original implementation task, plan the metadata update:

```yaml
metadata additions:
  tdd_mode: true
  tdd_phase: "green"
  paired_task_id: "{test_task_id}"  # Will be set after test task creation
```

---

## Phase 5: Set Dependencies

**Goal:** Insert TDD pairs into the existing dependency chain.

Apply the insertion algorithm from `tdd-dependency-rules.md`:

### For Each TDD Pair

Given implementation task `#N` with existing dependencies `blockedBy: [A, B, ...]`:

1. **Test task inherits upstream dependencies**: Test task `#T` gets `blockedBy: [A, B, ...]` (same as original)
2. **Implementation task gains test dependency**: Task `#N` adds `#T` to its `blockedBy` list
3. **Downstream tasks unchanged**: Tasks that depend on `#N` continue to depend on `#N`

### Dependency Insertion Example

```
Before: Model (#1) --> API (#2) --> UI (#3)

After:
  Test-Model (#4) blockedBy: []
  Model (#1) blockedBy: [#4]
  Test-API (#5) blockedBy: [#1]
  API (#2) blockedBy: [#1, #5]
  Test-UI (#6) blockedBy: [#2]
  UI (#3) blockedBy: [#2, #6]
```

### Circular Dependency Detection

After planning all insertions, validate the full dependency graph:

1. Build the complete graph from all tasks (original + new test tasks)
2. Run topological sort
3. If sort fails, a cycle exists

**Breaking cycles** (weakest-link strategy):

Score each dependency link in the cycle:
- TDD pair link (test -> impl): score 1 (weakest)
- Same-feature cross-layer: score 2
- Cross-feature dependency: score 3 (strongest)

Remove the dependency with the lowest score. Log a warning:

```
WARNING: Circular dependency detected after TDD pair insertion.
Cycle: {task chain}
Broken at: {removed link}
Reason: TDD pair link is weakest (score: 1)
Impact: {explanation of what may run out of order}
```

Add `needs_review: true` and `circular_dep_break: true` to the affected task's metadata.

---

## Phase 6: Preview & Confirm

**Goal:** Present the TDD transformation plan and get user approval.

### Display Preview

Present a summary of the planned changes:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TDD TASK PAIR GENERATION PREVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY:
  Total implementation tasks: {count}
  Eligible for TDD pairing: {eligible}
  Already have TDD pairs: {skipped} (merge mode)
  New TDD pairs to create: {new_pairs}
  Tasks skipped (test/config/docs): {skipped_ineligible}

NEW TDD PAIRS:
  Test Task                              | Blocks        | Phase
  ─────────────────────────────────────────────────────────────
  Write tests for {subject1}             | #{impl_id1}   | RED
  Write tests for {subject2}             | #{impl_id2}   | RED
  ...

DEPENDENCY CHAIN (after insertion):
  {visualization of the dependency chain with TDD pairs inserted}

{If circular deps detected and broken:}
WARNINGS:
  - Circular dependency broken at: {link}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Get Confirmation

Use AskUserQuestion to confirm:

```yaml
AskUserQuestion:
  questions:
    - header: "Confirm TDD Pair Creation"
      question: "Ready to create {n} TDD task pairs?"
      options:
        - label: "Yes, create pairs"
          description: "Create test tasks and update implementation tasks with TDD metadata"
        - label: "Show task details"
          description: "See full test task descriptions before creating"
        - label: "Cancel"
          description: "Don't create TDD pairs"
      multiSelect: false
```

If user selects "Show task details":
- Display each test task's full description
- Show the criteria-to-test conversion
- Then ask for confirmation again

If user selects "Cancel":
- Stop without creating any tasks
- Report cancellation

---

## Phase 7: Create Tasks

**Goal:** Create test tasks and update implementation tasks with TDD metadata.

### Step 1: Create Test Tasks

For each planned test task, use `TaskCreate`:

```
TaskCreate:
  subject: "Write tests for {original subject}"
  description: {generated description from Phase 4}
  activeForm: "Writing tests for {original subject}"
  metadata:
    tdd_mode: true
    tdd_phase: "red"
    paired_task_id: "{impl_task_id}"
    priority: {inherited}
    complexity: {estimated}
    source_section: {inherited}
    spec_path: {inherited}
    feature_name: {inherited}
    task_uid: "{original_uid}:red"
    task_group: {inherited}
```

Capture the returned task ID for each created test task.

### Step 2: Update Implementation Tasks

For each paired implementation task, use `TaskUpdate`:

```
TaskUpdate:
  taskId: "{impl_task_id}"
  metadata:
    tdd_mode: true
    tdd_phase: "green"
    paired_task_id: "{test_task_id}"
```

### Step 3: Set Dependencies

For each TDD pair, set the dependency relationships:

```
TaskUpdate:
  taskId: "{impl_task_id}"
  addBlockedBy: ["{test_task_id}"]
```

For test tasks that need upstream dependencies (inheriting from the original impl task):

```
TaskUpdate:
  taskId: "{test_task_id}"
  addBlockedBy: ["{upstream_dep_1}", "{upstream_dep_2}"]
```

### Step 4: Handle Circular Dependency Breaks

If any circular dependencies were detected and broken in Phase 5:

```
TaskUpdate:
  taskId: "{affected_task_id}"
  metadata:
    needs_review: true
    circular_dep_break: true
```

---

## Phase 8: Report

**Goal:** Present the final summary of created TDD task pairs.

### Completion Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TDD TASK PAIR CREATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Created {n} TDD task pairs
Set {m} dependency relationships

TDD PAIRS CREATED:
  Test Task (RED)                        | Impl Task (GREEN)        | Test Blocks
  ─────────────────────────────────────────────────────────────────────────────────
  #{test_id}: Write tests for {subj}     | #{impl_id}: {subj}       | #{impl_id}
  ...

DEPENDENCY CHAIN:
  {visual representation of the full dependency chain}

{If --task-group was used:}
Group: {group}
Tasks in group: {total}
TDD pairs added: {new}

{If merge mode detected:}
MERGE MODE:
  Existing pairs preserved: {n}
  New pairs created: {m}

{If circular deps broken:}
WARNINGS:
  {n} circular dependencies detected and broken. Review recommended.

NEXT STEPS:
  Run /execute-tdd-tasks to execute TDD pairs with RED-GREEN-REFACTOR workflow.
  Run /execute-tdd-tasks --task-group {group} for group-specific execution.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Error Handling

### Empty Task List

If TaskList returns no tasks:
- Inform user to run `/create-tasks` first
- Provide usage example
- Stop

### No Matching Group

If `--task-group` filter matches zero tasks:
- List available groups with task counts
- Suggest a valid group
- Stop

### All Tasks Already Paired

If merge mode detects that all eligible tasks already have TDD pairs:

```
All eligible tasks already have TDD pairs. Nothing to create.

TDD pair status:
- {n} active TDD pairs
- {m} completed TDD pairs
- {k} tasks skipped (test/config/docs)
```

### TaskCreate Failures

If a TaskCreate call fails:
- Log the failure
- Continue with remaining tasks
- Report partial results in Phase 8 with failed tasks listed

---

## Example Usage

### Convert all tasks to TDD pairs
```
/agent-alchemy-tdd:create-tdd-tasks
```

### Convert a specific group
```
/agent-alchemy-tdd:create-tdd-tasks --task-group user-authentication
```

### Re-run (merge mode)
```
/agent-alchemy-tdd:create-tdd-tasks --task-group user-authentication
```
If TDD pairs already exist for some tasks, they will be detected and skipped.

---

## Important Notes

- Never create duplicate test tasks -- always check merge mode signals first
- Preserve all existing task dependencies -- TDD pairs are inserted, not replacing
- Test tasks always block their paired implementation task
- Test task metadata always inherits `task_group`, `priority`, `feature_name`, `spec_path`, and `source_section` from the original
- Task UIDs for test tasks append `:red` to the original UID
- Always use imperative mood for subjects ("Write tests for X" not "Tests for X")
- Always include activeForm in present continuous ("Writing tests for X")
- Tasks with `tdd_mode: true` are never paired again (prevents double-pairing)

## Reference Files

- `references/tdd-decomposition-patterns.md` -- Task pairing rules, naming conventions, criteria conversion, merge mode
- `references/tdd-dependency-rules.md` -- Dependency insertion algorithm, circular dependency detection and breaking
