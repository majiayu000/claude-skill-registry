---
name: spec-executor
description: Execute implementation specs with batched checkpoints. Follows specs exactly, stops on blockers, supports parallelization.
argument-hint: <spec-file> [--batch-size=<n>] [--no-checkpoint] [--dry-run] [--resume]
---

# Spec Executor

Executes implementation specs (typically created by the spec-writer skill). Follows specs exactly with batched execution, checkpoints for user feedback, and parallelization support.

## Arguments

- `spec-file` (required): Path to the spec file to execute
- `--batch-size=<n>`: Steps per checkpoint (overrides config)
- `--no-checkpoint`: Run without pausing for checkpoints
- `--dry-run`: Show what would be done without making changes
- `--resume`: Resume from last checkpoint
- `--parallel=<true|false>`: Enable/disable parallelization

## Configuration

Check for `.claude/spec-workflow/config.yaml`:

```yaml
paths:
  worktrees: "./worktrees"

services:
  backend:
    path: "./backend"
    build: "npm run build"
    test: "npm test"
    lint: "npm run lint"
  frontend:
    path: "./frontend"
    build: "npm run build"
    test: "npm test"

execution:
  batchSize: 5
  checkpoint:
    behavior: "smart"           # "pause" | "continue" | "smart"
  parallel:
    enabled: true
    maxAgents: 3
```

If no config, auto-detect services and use defaults.

## Core Philosophy

**Follow the spec. Stop on blockers. Never guess.**

This skill prioritizes:

1. **Spec-driven execution** - Follow spec instructions exactly, don't improvise
2. **Stop on blockers** - Pause and ask rather than guess when something is unclear
3. **Parallelization-aware** - Use sub-agents for concurrent work when spec indicates
4. **Leveraging git worktrees** - Isolate spec work in dedicated worktrees

---

## Phase 0: Project Context

Before any execution, load permanent project context:

1. Check for `.claude/spec-workflow/PROJECT.md`
   - If found: read and store as PROJECT_DNA context
   - Extract: Architecture Rules, Code Conventions, Known Constraints, "Done" criteria
2. Use PROJECT_DNA throughout implementation:
   - **Architecture Rules** → enforce in every file change (flag violations)
   - **Code Conventions** → guide naming, file structure, error handling
   - **Known Constraints** → avoid assuming unavailable infrastructure
   - **"Done" criteria** → validate against when marking tasks complete
3. If not found: proceed without it (non-blocking)

---

## Phase 1: Environment Setup

Before executing, verify the environment is ready:

### Check for worktree (if specified in spec)

If spec frontmatter contains `worktree`:

1. Verify worktree exists at configured path (default: `./worktrees/[name]`)
2. Ensure we're working in that worktree
3. Verify branch matches frontmatter

If worktree doesn't exist:

1. Notify user: "Spec references worktree that doesn't exist. Create it?"
2. If yes, invoke `/create-worktree [name] --spec=[spec-path]`
3. Continue once created

### If no worktree specified

Proceed in current directory, but warn user that changes won't be isolated.

---

## Phase 2: Load & Review

1. **Read the full spec file**

2. **Parse the spec**
   - Extract Implementation Steps table
   - Identify parallelization groups (if present)
   - Note any Open Questions or unresolved items
   - Check spec status

3. **Review critically before starting**

   Present a summary:
   ```
   **Spec Review: [Feature Name]**

   **Tasks:** [N] implementation steps
   **Parallelization:** [Yes/No - describe groups if present]
   **Dependencies:** [List any external dependencies]
   **Estimated scope:** [Small/Medium/Large based on task count]

   **Concerns before starting:**
   - [Any unclear instructions]
   - [Any unresolved Open Questions from spec]
   - [Any missing information]

   **Parallelization Plan:**
   [Describe how tasks will be parallelized if applicable]

   Ready to proceed?
   ```

If `--dry-run`, stop here after showing the plan.

---

## Phase 2.5: AC Lock Checkpoint

Before starting any implementation:

1. **Check for `accepted-criteria.md`** in `.claude/feature-state/{slug}/`
   - If found: show locked ACs as a reminder, proceed
   - If not found: run the AC Lock flow (extract from prd.md + techspec.md + tasks.md, present to user, wait for confirmation)
2. **Do not start Phase 3 until** `accepted-criteria.md` is saved
3. **Emergency bypass**: if user types `skip-ac-lock`, log bypass and proceed without file

---

## Phase 3: Execute Batch

### Pre-Task: File Index

Before implementing each task:

1. **Build file index** from task description and spec Appendix:
   - Files to **modify** (will be edited)
   - Files to **create** (new files)
   - Files to **delete** (if any)
   - Files to **read** as reference only (not modified)

2. **Verify pre-conditions**:
   - Does each file-to-modify exist?
   - Does any file have uncommitted changes? (flag potential conflict)
   - Are the functions/classes the task will extend actually present?

3. **Save index** to `.claude/feature-state/{slug}/task-{n}-index.json`:
   ```json
   {
     "task": 3,
     "files_to_modify": ["src/api/users.ts"],
     "files_to_create": ["src/api/students.ts"],
     "files_to_delete": [],
     "reference_files": ["src/lib/firebase-admin.ts"],
     "pre_conditions": {
       "src/api/users.ts": { "exists": true, "has_uncommitted_changes": false }
     }
   }
   ```

4. **Load only the necessary files** — read files_to_modify and reference_files; avoid loading the entire project.

### Task Execution

For each task in the current batch:

1. **Mark task in_progress** in todo list
2. **Run Pre-Task File Index** (see above)
3. **Execute the task** following spec instructions exactly
4. **Run Post-Task Validation** (see below)
5. **Mark task completed** only after validation passes

### Post-Task Validation

After implementing each task:

1. **Lint modified files only** (not full project):
   ```bash
   # TypeScript/JavaScript
   npx eslint {files_to_modify}
   npx tsc --noEmit {files_to_modify}

   # Swift
   swiftlint lint {files_to_modify}

   # Rust
   cargo clippy -- -D warnings  # scoped to modified module

   # Python
   ruff check {files_to_modify}

   # Go
   go vet {files_to_modify}
   ```

2. **Run related tests only**:
   ```bash
   # TypeScript/JavaScript
   jest --findRelatedTests {files_to_modify}

   # Swift — run target containing modified files
   swift test --filter {ModuleName}

   # Rust
   cargo test {module_name}

   # Python
   pytest {test_file_for_modified_module}

   # Go
   go test ./{package}/...
   ```

3. **Report per-task result**:
   ```
   Task {N} — Post-Task Validation
   Files modified: {list}
   Lint: ✅ 0 errors / ❌ {N} errors
   Tests: ✅ {N} passed / ❌ {N} failed
   ```

4. **If validation passes** → mark task ✅ and continue
5. **If validation fails** → invoke Failure Recovery (see below)

### Failure Recovery

When a task fails post-task validation:

**Level 1 — Auto-correction (up to 2 attempts):**

| Failure type | Auto-fix |
|-------------|---------|
| Missing import | Add import, re-run lint |
| Unused variable | Remove or use it |
| TypeScript type simple error | Infer correct type from context |
| Snapshot test outdated | Update snapshot (if configured) |
| Lint warning (not error) | Fix inline, continue |

After each auto-fix attempt, re-run lint + tests.
If still failing after 2 attempts → Level 2.

**Level 2 — Structured diagnosis:**

```
⚠️ Task {N} Failed

Error type: {TypeScript/Lint/Test}
File: {path}:{line}
Error: {message}

Root cause analysis:
{explanation of why this failed — e.g., "missing field on existing type"}

Impact on remaining tasks:
- Task {N+2} also depends on {affected entity} → will also fail without fix
- Tasks {list} are unaffected

Options:
A) Fix the root cause now and re-run Task {N} (recommended)
B) Replan Tasks {N} through {M} with a new approach
C) Mark Task {N} as blocked, skip to Task {N+1} (cascade risk)
D) Stop execution and review the spec

Proceed with: A / B / C / D ?
```

**Level 3 — Replan remaining tasks:**

When user chooses option B:
1. Identify tasks that depend on the failing task
2. Propose alternative tasks that cover the same ACs
3. Present new task plan to user for confirmation
4. Update `tasks.md` and state directory with replanned tasks
5. Log in `failure-log.md`

**Failure log** (`.claude/feature-state/{slug}/failure-log.md`):
```markdown
## Failure Log

### Task {N} — {timestamp}
Error: {message}
Auto-fix attempts: {0|1|2}
Resolution: {Option A/B/C/D chosen}
Replanned tasks: {list or "none"}
Status: Resolved ✅ | Replanned ♻️ | Blocked ⏸️
```

**Configurable via `.feature-marker.json`:**
```json
{
  "per_task_validation": {
    "lint": true,
    "tests": "related",
    "fail_behavior": "pause"
  },
  "failure_recovery": {
    "auto_fix": true,
    "auto_fix_max_attempts": 2,
    "auto_fix_types": ["lint", "unused-imports", "snapshot"],
    "replan_on_cascade": true
  }
}
```

### Parallelization

If spec includes a Sub-agent Parallelization Plan:

1. **Identify independent tasks** in current group
2. **Launch sub-agents** using Task tool for parallel execution
3. **Wait for all agents** to complete before proceeding
4. **Collect results** and verify all succeeded

```
Launching parallel execution for Group 1:

Agent 1: Task 1.1 - [Description]
Agent 2: Task 1.2 - [Description]

Waiting for completion...
```

Respect `execution.parallel.maxAgents` from config.

### Following the Spec

**DO:**
- Follow Implementation Steps in order (respecting dependencies)
- Use patterns described in Architecture & Design section
- Implement exactly what's specified in Requirements
- Run verifications specified in Validation & Testing Plan

**DON'T:**
- Add features not in the spec
- Skip steps or combine tasks arbitrarily
- Ignore the spec's design decisions
- Proceed past blockers without asking

---

## Phase 4: Report & Checkpoint

After each batch (based on `batchSize`):

```
**Checkpoint: Batch [N] Complete**

**Completed tasks:**
- [x] Task 1: [Brief description of what was done]
- [x] Task 2: [Brief description of what was done]

**Verification results:**
- Tests: [Pass/Fail - details]
- Lint: [Pass/Fail]
- Build: [Pass/Fail]

**Files modified:**
- `path/to/file1` - [What changed]
- `path/to/file2` - [What changed]

**Next batch:** Tasks [N+1] through [N+3]
```

Checkpoint behavior (from config or argument):
- `pause`: Always pause for user review
- `continue`: Auto-continue if no issues
- `smart`: Pause on warnings/errors, continue otherwise

---

## Phase 5: Continue

1. **Apply feedback** from previous checkpoint
2. **Execute next batch** following Phase 3 process
3. **Report progress** following Phase 4 process
4. **Repeat** until all tasks complete

---

## Phase 6: Finalize

After all tasks complete:

1. **Run full validation**

   For each service in spec's `services` frontmatter (or all configured services if not specified):

   ```
   # Use commands from config, or auto-detect
   [service.build command]
   [service.lint command]
   [service.test command]
   ```

2. **Update spec status**
   - Edit spec file frontmatter to change status to "Implemented"
   - Add completion date

3. **Final summary**
   ```
   **Spec Execution Complete: [Feature Name]**

   **Tasks completed:** [N] of [N]
   **Files modified:** [Count]
   **Tests:** [Pass/Fail]
   **Build:** [Pass/Fail]

   **Summary of changes:**
   - [High-level description of what was implemented]

   **Next steps:**
   - [ ] Manual testing per spec's Validation Plan
   - [ ] Code review
   - [ ] Commit and PR
   ```

---

## Critical Stop Points

**STOP and ask the user when:**

1. **Blockers encountered**
   - Missing dependency or file
   - Failed test that can't be fixed after several attempts
   - Unclear instruction in spec

2. **Spec gaps**
   - Implementation step references non-existent file
   - Missing information needed to proceed
   - Conflicting instructions

3. **Scope questions**
   - Discovering additional work not in spec
   - Edge cases not covered by spec

### Stop Format

```
**Execution Paused: [Reason]**

**Context:** [What I was trying to do]
**Issue:** [What went wrong or is unclear]
**Question:** [Specific question for user]

Options:
A) [Suggested resolution 1]
B) [Suggested resolution 2]
C) Skip this task and continue
D) Stop execution entirely

How should I proceed?
```

---

## Progress Tracking

### Managing TODOs

Mirror spec's Implementation Steps in todo list:

```
Todos:
- [x] Step 1: [Task from spec]
- [x] Step 2: [Task from spec]
- [ ] Step 3: [Task from spec] (in_progress)
- [ ] Step 4: [Task from spec] (pending)
```

### Spec File Updates

Update checkboxes in spec's Validation & Testing Plan as tests are written/pass.

---

## Workflow Summary

```
spec-file
     │
     ▼
┌─────────────────────────────────┐
│ PHASE 1: ENVIRONMENT SETUP      │
│ • Check/create worktree         │
│ • Verify environment ready      │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│ PHASE 2: LOAD & REVIEW          │
│ • Parse spec                    │
│ • Flag concerns                 │
│ • Confirm ready to proceed      │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│ PHASE 3: EXECUTE BATCH          │
│ • Follow spec exactly           │
│ • Use sub-agents if parallel    │
│ • Track tasks                   │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│ PHASE 4: CHECKPOINT             │
│ • Report progress               │
│ • Show verification results     │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│ PHASE 5: CONTINUE               │
│ • Next batch → Phase 3          │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│ PHASE 6: FINALIZE               │
│ • Full validation               │
│ • Update spec status            │
│ • Summary & next steps          │
└─────────────────────────────────┘
     │
     ▼
   Feature Implemented
```

---

## Upon Implementation Completion

1. Ask the user if they would like to commit the changes now.
2. If yes, create a commit with a summary of changes made.
3. If committed, ask if they would like to open a PR for review.
4. If yes, create a PR with appropriate title and description.
