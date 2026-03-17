---
name: issue-execute
description: Execute all solutions from issue queue with git commit after each solution. Supports batch processing and execution control.
argument-hint: "--queue=<id> [--worktree=<path|new>] [--skip-tests] [--skip-build] [--dry-run]"
---

# Issue Execute (Codex Version)

## Core Principle

**Serial Execution**: Execute solutions ONE BY ONE from the issue queue via `ccw issue next`. For each solution, complete all tasks sequentially (implement → test → verify), then commit once per solution with formatted summary. Continue autonomously until queue is empty.

## Project Context (MANDATORY FIRST STEPS)

Before starting execution, load project context:

1. **Read project tech stack**: `.workflow/project-tech.json`
2. **Read project guidelines**: `.workflow/project-guidelines.json`
3. **Read solution schema**: `~/.ccw/workflows/cli-templates/schemas/solution-schema.json`

This ensures execution follows project conventions and patterns.

## Parameters

- `--queue=<id>`: Queue ID to execute (REQUIRED)
- `--worktree=<path|new>`: Worktree path or 'new' for creating new worktree
- `--skip-tests`: Skip test execution during solution implementation
- `--skip-build`: Skip build step
- `--dry-run`: Preview execution without making changes

## Queue ID Requirement (MANDATORY)

**`--queue <queue-id>` parameter is REQUIRED**

### When Queue ID Not Provided

```
List queues → Output options → Stop and wait for user
```

**Actions**:

1. `ccw issue queue list --brief --json` - Fetch queue list
2. Filter active/pending status, output formatted list
3. **Stop execution**, prompt user to rerun with `codex -p "@.codex/prompts/issue-execute.md --queue QUE-xxx"`

**No auto-selection** - User MUST explicitly specify queue-id

## Worktree Mode (Recommended for Parallel Execution)

When `--worktree` is specified, create or use a git worktree to isolate work.

**Usage**:
- `--worktree` - Create a new worktree with timestamp-based name
- `--worktree <existing-path>` - Resume in an existing worktree (for recovery/continuation)

**Note**: `ccw issue` commands auto-detect worktree and redirect to main repo automatically.

```bash
# Step 0: Setup worktree before starting (run from MAIN REPO)

# Use absolute paths to avoid issues when running from subdirectories
REPO_ROOT=$(git rev-parse --show-toplevel)
WORKTREE_BASE="${REPO_ROOT}/.ccw/worktrees"

# Check if existing worktree path was provided
EXISTING_WORKTREE="${1:-}"  # Pass as argument or empty

if [[ -n "${EXISTING_WORKTREE}" && -d "${EXISTING_WORKTREE}" ]]; then
  # Resume mode: Use existing worktree
  WORKTREE_PATH="${EXISTING_WORKTREE}"
  WORKTREE_NAME=$(basename "${WORKTREE_PATH}")

  # Verify it's a valid git worktree
  if ! git -C "${WORKTREE_PATH}" rev-parse --is-inside-work-tree &>/dev/null; then
    echo "Error: ${EXISTING_WORKTREE} is not a valid git worktree"
    exit 1
  fi

  echo "Resuming in existing worktree: ${WORKTREE_PATH}"
else
  # Create mode: New worktree with timestamp
  WORKTREE_NAME="issue-exec-$(date +%Y%m%d-%H%M%S)"
  WORKTREE_PATH="${WORKTREE_BASE}/${WORKTREE_NAME}"

  # Ensure worktree base directory exists (gitignored)
  mkdir -p "${WORKTREE_BASE}"

  # Prune stale worktrees from previous interrupted executions
  git worktree prune

  # Create worktree from current branch
  git worktree add "${WORKTREE_PATH}" -b "${WORKTREE_NAME}"

  echo "Created new worktree: ${WORKTREE_PATH}"
fi

# Setup cleanup trap for graceful failure handling
cleanup_worktree() {
  echo "Cleaning up worktree due to interruption..."
  cd "${REPO_ROOT}" 2>/dev/null || true
  git worktree remove "${WORKTREE_PATH}" --force 2>/dev/null || true
  # Keep branch for debugging failed executions
  echo "Worktree removed. Branch '${WORKTREE_NAME}' kept for inspection."
}
trap cleanup_worktree EXIT INT TERM

# Change to worktree directory
cd "${WORKTREE_PATH}"

# ccw issue commands auto-detect worktree and use main repo's .workflow/
# So you can run ccw issue next/done directly from worktree
```

**Worktree Execution Pattern**:
```
0. [MAIN REPO] Validate queue ID (--queue required, or prompt user to select)
1. [WORKTREE] ccw issue next --queue <queue-id> → auto-redirects to main repo's .workflow/
2. [WORKTREE] Implement all tasks, run tests, git commit
3. [WORKTREE] ccw issue done <item_id> → auto-redirects to main repo
4. Repeat from step 1
```

**Note**: Add `.ccw/worktrees/` to `.gitignore` to prevent tracking worktree contents.

**Benefits:**
- Parallel executors don't conflict with each other
- Main working directory stays clean
- Easy cleanup after execution
- **Resume support**: Pass existing worktree path to continue interrupted executions

**Resume Examples:**
```bash
# List existing worktrees to find interrupted execution
git worktree list

# Resume in existing worktree (pass path as argument)
# The worktree path will be used instead of creating a new one
codex -p "@.codex/prompts/issue-execute.md --worktree /path/to/existing/worktree"
```

**Completion - User Choice:**

When all solutions are complete, output options and wait for user to specify:

```
All solutions completed in worktree. Choose next action:

1. Merge to main - Merge worktree branch into main and cleanup
2. Create PR - Push branch and create pull request (Recommended for parallel execution)
3. Keep branch - Keep branch for manual handling, cleanup worktree only

Please respond with: 1, 2, or 3
```

**Based on user response:**

```bash
# Disable cleanup trap before intentional cleanup
trap - EXIT INT TERM

# Return to main repo first (use REPO_ROOT from setup)
cd "${REPO_ROOT}"

# Validate main repo state before merge (prevents conflicts)
validate_main_clean() {
  if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️ Warning: Main repo has uncommitted changes."
    echo "Cannot auto-merge. Falling back to 'Create PR' option."
    return 1
  fi
  return 0
}

# Option 1: Merge to main (only if main is clean)
if validate_main_clean; then
  git merge "${WORKTREE_NAME}" --no-ff -m "Merge issue queue execution: ${WORKTREE_NAME}"
  git worktree remove "${WORKTREE_PATH}"
  git branch -d "${WORKTREE_NAME}"
else
  # Fallback to PR if main is dirty
  git push -u origin "${WORKTREE_NAME}"
  gh pr create --title "Issue Queue: ${WORKTREE_NAME}" --body "Automated issue queue execution (main had uncommitted changes)"
  git worktree remove "${WORKTREE_PATH}"
fi

# Option 2: Create PR (Recommended for parallel execution)
git push -u origin "${WORKTREE_NAME}"
gh pr create --title "Issue Queue: ${WORKTREE_NAME}" --body "Automated issue queue execution"
git worktree remove "${WORKTREE_PATH}"
# Branch kept on remote

# Option 3: Keep branch
git worktree remove "${WORKTREE_PATH}"
# Branch kept locally for manual handling
echo "Branch '${WORKTREE_NAME}' kept. Merge manually when ready."
```

**Parallel Execution Safety**: For parallel executors, "Create PR" is the safest option as it avoids race conditions during merge. Multiple PRs can be reviewed and merged sequentially.

## Execution Flow

```
STEP 0: Validate queue ID (--queue required, or prompt user to select)

INIT: Fetch first solution via ccw issue next --queue <queue-id>

WHILE solution exists:
  1. Receive solution JSON from ccw issue next --queue <queue-id>
  2. Execute all tasks in solution.tasks sequentially:
     FOR each task:
       - IMPLEMENT: Follow task.implementation steps
       - TEST: Run task.test commands
       - VERIFY: Check task.acceptance criteria
  3. COMMIT: Stage all files, commit once with formatted summary
  4. Report completion via ccw issue done <item_id>
  5. Fetch next solution via ccw issue next --queue <queue-id>

WHEN queue empty:
  Output final summary
```

## Step 1: Fetch First Solution

**Prerequisite**: Queue ID must be determined (either from `--queue` argument or user selection in Step 0).

Run this command to get your first solution:

```javascript
// ccw auto-detects worktree and uses main repo's .workflow/
// QUEUE_ID is required - obtained from --queue argument or user selection
const result = shell_command({ command: `ccw issue next --queue ${QUEUE_ID}` })
```

This returns JSON with the full solution definition:
- `item_id`: Solution identifier in queue (e.g., "S-1")
- `issue_id`: Parent issue ID (e.g., "ISS-20251227-001")
- `solution_id`: Solution ID (e.g., "SOL-ISS-20251227-001-1")
- `solution`: Full solution with all tasks
- `execution_hints`: Timing and executor hints

If response contains `{ "status": "empty" }`, all solutions are complete - skip to final summary.

## Step 2: Parse Solution Response

Expected solution structure:

```json
{
  "item_id": "S-1",
  "issue_id": "ISS-20251227-001",
  "solution_id": "SOL-ISS-20251227-001-1",
  "status": "pending",
  "solution": {
    "id": "SOL-ISS-20251227-001-1",
    "description": "Description of solution approach",
    "tasks": [
      {
        "id": "T1",
        "title": "Task title",
        "scope": "src/module/",
        "action": "Create|Modify|Fix|Refactor|Add",
        "description": "What to do",
        "modification_points": [
          { "file": "path/to/file.ts", "target": "function name", "change": "description" }
        ],
        "implementation": [
          "Step 1: Do this",
          "Step 2: Do that"
        ],
        "test": {
          "commands": ["npm test -- --filter=xxx"],
          "unit": ["Unit test requirement 1", "Unit test requirement 2"]
        },
        "regression": ["Verify existing tests still pass"],
        "acceptance": {
          "criteria": ["Criterion 1: Must pass", "Criterion 2: Must verify"],
          "verification": ["Run test command", "Manual verification step"]
        },
        "commit": {
          "type": "feat|fix|test|refactor",
          "scope": "module",
          "message_template": "feat(scope): description"
        },
        "depends_on": [],
        "estimated_minutes": 30,
        "priority": 1
      }
    ],
    "exploration_context": {
      "relevant_files": ["path/to/reference.ts"],
      "patterns": "Follow existing pattern in xxx",
      "integration_points": "Used by other modules"
    },
    "analysis": {
      "risk": "low|medium|high",
      "impact": "low|medium|high",
      "complexity": "low|medium|high"
    },
    "score": 0.95,
    "is_bound": true
  },
  "execution_hints": {
    "executor": "codex",
    "estimated_minutes": 180
  }
}
```

## Step 2.1: Determine Execution Strategy

After parsing the solution, analyze the issue type and task actions to determine the appropriate execution strategy. The strategy defines additional verification steps and quality gates beyond the basic implement-test-verify cycle.

### Strategy Auto-Matching

**Matching Priority**:
1. Explicit `solution.strategy_type` if provided
2. Infer from `task.action` keywords (Debug, Fix, Feature, Refactor, Test, etc.)
3. Infer from `solution.description` and `task.title` content
4. Default to "standard" if no clear match

**Strategy Types and Matching Keywords**:

| Strategy Type | Match Keywords | Description |
|---------------|----------------|-------------|
| `debug` | Debug, Diagnose, Trace, Investigate | Bug diagnosis with logging and debugging |
| `bugfix` | Fix, Patch, Resolve, Correct | Bug fixing with root cause analysis |
| `feature` | Feature, Add, Implement, Create, Build | New feature development with full testing |
| `refactor` | Refactor, Restructure, Optimize, Cleanup | Code restructuring with behavior preservation |
| `test` | Test, Coverage, E2E, Integration | Test implementation with coverage checks |
| `performance` | Performance, Optimize, Speed, Memory | Performance optimization with benchmarking |
| `security` | Security, Vulnerability, CVE, Audit | Security fixes with vulnerability checks |
| `hotfix` | Hotfix, Urgent, Critical, Emergency | Urgent fixes with minimal changes |
| `documentation` | Documentation, Docs, Comment, README | Documentation updates with example validation |
| `chore` | Chore, Dependency, Config, Maintenance | Maintenance tasks with compatibility checks |
| `standard` | (default) | Standard implementation without extra steps |

### Strategy-Specific Execution Phases

Each strategy extends the basic cycle with additional quality gates:

#### 1. Debug → Reproduce → Instrument → Diagnose → Implement → Test → Verify → Cleanup

```
REPRODUCE → INSTRUMENT → DIAGNOSE → IMPLEMENT → TEST → VERIFY → CLEANUP
```

#### 2. Bugfix → Root Cause → Implement → Test → Edge Cases → Regression → Verify

```
ROOT_CAUSE → IMPLEMENT → TEST → EDGE_CASES → REGRESSION → VERIFY
```

#### 3. Feature → Design Review → Unit Tests → Implement → Integration Tests → Code Review → Docs → Verify

```
DESIGN_REVIEW → UNIT_TESTS → IMPLEMENT → INTEGRATION_TESTS → TEST → CODE_REVIEW → DOCS → VERIFY
```

#### 4. Refactor → Baseline Tests → Implement → Test → Behavior Check → Performance Compare → Verify

```
BASELINE_TESTS → IMPLEMENT → TEST → BEHAVIOR_PRESERVATION → PERFORMANCE_CMP → VERIFY
```

#### 5. Test → Coverage Baseline → Test Design → Implement → Coverage Check → Verify

```
COVERAGE_BASELINE → TEST_DESIGN → IMPLEMENT → COVERAGE_CHECK → VERIFY
```

#### 6. Performance → Profiling → Bottleneck → Implement → Benchmark → Test → Verify

```
PROFILING → BOTTLENECK → IMPLEMENT → BENCHMARK → TEST → VERIFY
```

#### 7. Security → Vulnerability Scan → Implement → Security Test → Penetration Test → Verify

```
VULNERABILITY_SCAN → IMPLEMENT → SECURITY_TEST → PENETRATION_TEST → VERIFY
```

#### 8. Hotfix → Impact Assessment → Implement → Test → Quick Verify → Verify

```
IMPACT_ASSESSMENT → IMPLEMENT → TEST → QUICK_VERIFY → VERIFY
```

#### 9. Documentation → Implement → Example Validation → Format Check → Link Validation → Verify

```
IMPLEMENT → EXAMPLE_VALIDATION → FORMAT_CHECK → LINK_VALIDATION → VERIFY
```

#### 10. Chore → Implement → Compatibility Check → Test → Changelog → Verify

```
IMPLEMENT → COMPATIBILITY_CHECK → TEST → CHANGELOG → VERIFY
```

#### 11. Standard → Implement → Test → Verify

```
IMPLEMENT → TEST → VERIFY
```

### Strategy Selection Implementation

**Pseudo-code for strategy matching**:

```javascript
function determineStrategy(solution) {
  // Priority 1: Explicit strategy type
  if (solution.strategy_type) {
    return solution.strategy_type
  }

  // Priority 2: Infer from task actions
  const actions = solution.tasks.map(t => t.action.toLowerCase())
  const titles = solution.tasks.map(t => t.title.toLowerCase())
  const description = solution.description.toLowerCase()
  const allText = [...actions, ...titles, description].join(' ')

  // Match keywords (order matters - more specific first)
  if (/hotfix|urgent|critical|emergency/.test(allText)) return 'hotfix'
  if (/debug|diagnose|trace|investigate/.test(allText)) return 'debug'
  if (/security|vulnerability|cve|audit/.test(allText)) return 'security'
  if (/performance|optimize|speed|memory|benchmark/.test(allText)) return 'performance'
  if (/refactor|restructure|cleanup/.test(allText)) return 'refactor'
  if (/test|coverage|e2e|integration/.test(allText)) return 'test'
  if (/documentation|docs|comment|readme/.test(allText)) return 'documentation'
  if (/chore|dependency|config|maintenance/.test(allText)) return 'chore'
  if (/fix|patch|resolve|correct/.test(allText)) return 'bugfix'
  if (/feature|add|implement|create|build/.test(allText)) return 'feature'

  // Default
  return 'standard'
}
```

**Usage in execution flow**:

```javascript
// After parsing solution (Step 2)
const strategy = determineStrategy(solution)
console.log(`Strategy selected: ${strategy}`)

// During task execution (Step 3), follow strategy-specific phases
for (const task of solution.tasks) {
  executeTaskWithStrategy(task, strategy)
}
```

## Step 2.5: Initialize Task Tracking

After parsing solution and determining strategy, use `update_plan` to track each task:

```javascript
// Initialize plan with all tasks from solution
update_plan({
  explanation: `Starting solution ${item_id}`,
  plan: solution.tasks.map(task => ({
    step: `${task.id}: ${task.title}`,
    status: "pending"
  }))
})
```

**Note**: Codex uses `update_plan` tool for task tracking (not TodoWrite).

## Step 3: Execute Tasks Sequentially

Iterate through `solution.tasks` array and execute each task.

**Before starting each task**, mark it as in_progress:
```javascript
// Update current task status
update_plan({
  explanation: `Working on ${task.id}: ${task.title}`,
  plan: tasks.map(t => ({
    step: `${t.id}: ${t.title}`,
    status: t.id === task.id ? "in_progress" : (t.completed ? "completed" : "pending")
  }))
})
```

**After completing each task** (verification passed), mark it as completed:
```javascript
// Mark task as completed (commit happens at solution level)
update_plan({
  explanation: `Completed ${task.id}: ${task.title}`,
  plan: tasks.map(t => ({
    step: `${t.id}: ${t.title}`,
    status: t.id === task.id ? "completed" : t.status
  }))
})
```

### Phase A: IMPLEMENT

1. **Read context files in parallel** using `multi_tool_use.parallel`:
```javascript
// Read all relevant files in parallel for context
multi_tool_use.parallel({
  tool_uses: solution.exploration_context.relevant_files.map(file => ({
    recipient_name: "functions.read_file",
    parameters: { path: file }
  }))
})
```

2. Follow `task.implementation` steps in order
3. Apply changes to `task.modification_points` files
4. Follow `solution.exploration_context.patterns` for code style consistency
5. Run `task.regression` checks if specified to ensure no breakage

**Output format:**
```
## Implementing: [task.title] (Task [N]/[Total])

**Scope**: [task.scope]
**Action**: [task.action]

**Steps**:
1. ✓ [implementation step 1]
2. ✓ [implementation step 2]
...

**Files Modified**:
- path/to/file1.ts
- path/to/file2.ts
```

### Phase B: TEST

1. Run all commands in `task.test.commands`
2. Verify unit tests pass (`task.test.unit`)
3. Run integration tests if specified (`task.test.integration`)

**If tests fail**: Fix the code and re-run. Do NOT proceed until tests pass.

**Output format:**
```
## Testing: [task.title]

**Test Results**:
- [x] Unit tests: PASSED
- [x] Integration tests: PASSED (or N/A)
```

### Phase C: VERIFY

Check all `task.acceptance.criteria` are met using `task.acceptance.verification` steps:

```
## Verifying: [task.title]

**Acceptance Criteria**:
- [x] Criterion 1: Verified
- [x] Criterion 2: Verified
...

**Verification Steps**:
- [x] Run test command
- [x] Manual verification step

All criteria met: YES
```

**If any criterion fails**: Go back to IMPLEMENT phase and fix.

### Repeat for Next Task

Continue to next task in `solution.tasks` array until all tasks are complete.

**Note**: Do NOT commit after each task. Commits happen at solution level after all tasks pass.

## Step 3.5: Commit Solution

After ALL tasks in the solution pass implementation, testing, and verification, commit once for the entire solution:

```bash
# Stage all modified files from all tasks
git add path/to/file1.ts path/to/file2.ts ...

# Commit with clean, standard format (NO solution metadata)
git commit -m "[commit_type](scope): [brief description of changes]"

# Example commits:
# feat(auth): add token refresh mechanism
# fix(payment): resolve timeout handling in checkout flow
# refactor(api): simplify error handling logic
```

**Commit Type Selection**:
- `feat`: New feature or capability
- `fix`: Bug fix
- `refactor`: Code restructuring without behavior change
- `test`: Adding or updating tests
- `docs`: Documentation changes
- `chore`: Maintenance tasks

**Commit Language**:
- Use **Chinese** commit summary if project's `CLAUDE.md` specifies Chinese response guidelines or user explicitly requests Chinese
- Use **English** commit summary by default or when project targets international collaboration
- Check project's existing commit history for language convention consistency

**Output format:**
```
## Solution Committed: [solution_id]

**Commit**: [commit hash]
**Type**: [commit_type]([scope])

**Changes**:
- [Feature/Fix/Improvement]: [What functionality was added/fixed/improved]
- [Specific change 1]
- [Specific change 2]

**Files Modified**:
- path/to/file1.ts - [Brief description of changes]
- path/to/file2.ts - [Brief description of changes]
- path/to/file3.ts - [Brief description of changes]

**Solution**: [solution_id] ([N] tasks completed)
```

## Step 4: Report Completion

After ALL tasks in the solution are complete and committed, report to queue system with full solution metadata:

```javascript
// ccw auto-detects worktree and uses main repo's .workflow/
// Record ALL solution context here (NOT in git commit)
shell_command({
  command: `ccw issue done ${item_id} --result '${JSON.stringify({
    solution_id: solution.id,
    issue_id: issue_id,
    commit: {
      hash: commit_hash,
      type: commit_type,
      scope: commit_scope,
      message: commit_message
    },
    analysis: {
      risk: solution.analysis.risk,
      impact: solution.analysis.impact,
      complexity: solution.analysis.complexity
    },
    tasks_completed: solution.tasks.map(t => ({
      id: t.id,
      title: t.title,
      action: t.action,
      scope: t.scope
    })),
    files_modified: ["path1", "path2", ...],
    tests_passed: true,
    verification: {
      all_tests_passed: true,
      acceptance_criteria_met: true,
      regression_checked: true
    },
    summary: "[What was accomplished - brief description]"
  })}'`
})
```

**Complete Example**:

```javascript
shell_command({
  command: `ccw issue done S-1 --result '${JSON.stringify({
    solution_id: "SOL-ISS-20251227-001-1",
    issue_id: "ISS-20251227-001",
    commit: {
      hash: "a1b2c3d4",
      type: "feat",
      scope: "auth",
      message: "feat(auth): add token refresh mechanism"
    },
    analysis: {
      risk: "low",
      impact: "medium",
      complexity: "medium"
    },
    tasks_completed: [
      { id: "T1", title: "Implement refresh token endpoint", action: "Add", scope: "src/auth/" },
      { id: "T2", title: "Add token rotation logic", action: "Create", scope: "src/auth/services/" }
    ],
    files_modified: [
      "src/auth/routes/token.ts",
      "src/auth/services/refresh.ts",
      "src/auth/middleware/validate.ts"
    ],
    tests_passed: true,
    verification: {
      all_tests_passed: true,
      acceptance_criteria_met: true,
      regression_checked: true
    },
    summary: "Implemented token refresh mechanism with automatic rotation"
  })}'`
})
```

**If solution failed:**

```javascript
shell_command({
  command: `ccw issue done ${item_id} --fail --reason '${JSON.stringify({
    task_id: "TX",
    error_type: "test_failure",
    message: "Integration tests failed: timeout in token validation",
    files_attempted: ["path1", "path2"],
    commit: null
  })}'`
})
```

## Step 5: Continue to Next Solution

Fetch next solution (using same QUEUE_ID from Step 0/1):

```javascript
// ccw auto-detects worktree
// Continue using the same QUEUE_ID throughout execution
const result = shell_command({ command: `ccw issue next --queue ${QUEUE_ID}` })
```

**Output progress:**
```
✓ [N/M] Completed: [item_id] - [solution.description]
  Commit: [commit_hash] ([commit_type])
  Tasks: [task_count] completed
→ Fetching next solution...
```

**DO NOT STOP.** Return to Step 2 and continue until queue is empty.

## Final Summary

When `ccw issue next` returns `{ "status": "empty" }`:

**If running in worktree mode**: Prompt user for merge/PR/keep choice (see "Completion - User Choice" above) before outputting summary.

```markdown
## Issue Queue Execution Complete

**Total Solutions Executed**: N
**Total Tasks Executed**: M
**Total Commits**: N (one per solution)

**Solution Commits**:
| # | Solution | Tasks | Commit | Type |
|---|----------|-------|--------|------|
| 1 | SOL-xxx-1 | T1, T2 | abc123 | feat |
| 2 | SOL-xxx-2 | T1 | def456 | fix |
| 3 | SOL-yyy-1 | T1, T2, T3 | ghi789 | refactor |

**Files Modified**:
- path/to/file1.ts
- path/to/file2.ts

**Summary**:
[Overall what was accomplished]
```

## Execution Rules

1. **Never stop mid-queue** - Continue until queue is empty
2. **One solution at a time** - Fully complete (all tasks + commit + report) before moving on
3. **Sequential within solution** - Complete each task's implement/test/verify before next task
4. **Tests MUST pass** - Do not proceed if any task's tests fail
5. **One commit per solution** - All tasks share a single commit with formatted summary
6. **Self-verify** - All acceptance criteria must pass before solution commit
7. **Report accurately** - Use `ccw issue done` after each solution
8. **Handle failures gracefully** - If a solution fails, report via `ccw issue done --fail` and continue to next
9. **Track with update_plan** - Use update_plan tool for task progress tracking
10. **Worktree auto-detect** - `ccw issue` commands auto-redirect to main repo from worktree

## Error Handling

| Situation | Action |
|-----------|--------|
| `ccw issue next` returns empty | All done - output final summary |
| Tests fail | Fix code, re-run tests |
| Verification fails | Go back to implement phase |
| Solution commit fails | Check staging, retry commit |
| `ccw issue done` fails | Log error, continue to next solution |
| Any task unrecoverable | Call `ccw issue done --fail`, continue to next solution |

## CLI Command Reference

| Command | Purpose |
|---------|---------|
| `ccw issue queue list --brief --json` | List all queues (for queue selection) |
| `ccw issue next --queue QUE-xxx` | Fetch next solution from specified queue (**--queue required**) |
| `ccw issue done <id>` | Mark solution complete with result (auto-detects queue) |
| `ccw issue done <id> --fail --reason "..."` | Mark solution failed with structured reason |
| `ccw issue retry --queue QUE-xxx` | Reset failed items in specific queue |

## Start Execution

**Step 0: Validate Queue ID**

If `--queue` was NOT provided in the command arguments:
1. Run `ccw issue queue list --brief --json`
2. Filter and display active/pending queues to user
3. **Stop execution**, prompt user to rerun with `--queue QUE-xxx`

**Step 1: Fetch First Solution**

Once queue ID is confirmed, begin by running:

```bash
ccw issue next --queue <queue-id>
```

Then follow the solution lifecycle for each solution until queue is empty.
