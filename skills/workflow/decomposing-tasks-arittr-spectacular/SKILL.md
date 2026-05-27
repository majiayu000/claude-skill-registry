---
name: decomposing-tasks
description: Use when you need to create an execution plan from a feature spec - handles worktree context, dispatches subagent for task decomposition, validates quality, analyzes dependencies, groups into phases, and commits the plan
---

# Task Decomposition

Create an execution-ready plan from a feature specification with automatic phase grouping based on file dependencies.

**When to use:** After completing a feature spec with `/spectacular:spec`, to create an implementation plan.

**Announce:** "I'm using the Task Decomposition skill to create an execution plan."

## Input

User will provide: `/spectacular:plan {spec-path}`

Example: `/spectacular:plan @specs/a1b2c3-magic-link-auth/spec.md`

Where `a1b2c3` is the runId and `magic-link-auth` is the feature slug.

## Multi-Repo Support

### Detecting Multi-Repo Mode

Check if workspace contains multiple repos:

```bash
# Detect workspace mode (same as writing-specs skill)
REPO_COUNT=$(find . -maxdepth 2 -name ".git" -type d 2>/dev/null | wc -l | tr -d ' ')
if [ "$REPO_COUNT" -gt 1 ]; then
  echo "Multi-repo workspace detected ($REPO_COUNT repos)"
  WORKSPACE_MODE="multi-repo"
  # List detected repos
  REPOS=$(find . -maxdepth 2 -name ".git" -type d | xargs -I{} dirname {} | sed 's|^\./||' | tr '\n' ' ')
  echo "Available repos: $REPOS"
else
  echo "Single-repo mode"
  WORKSPACE_MODE="single-repo"
fi
```

### Multi-Repo Task Format

In multi-repo mode, each task MUST specify which repo it belongs to:

```markdown
### Task 1.1: Add user_preferences table

**Repo**: backend
**Files**:
- prisma/schema.prisma
- prisma/migrations/*

**Constitution**: @backend/docs/constitutions/current/
```

### Single-Repo Task Format (unchanged)

```markdown
### Task 1.1: Add user_preferences table

**Files**:
- prisma/schema.prisma
- prisma/migrations/*

**Constitution**: @docs/constitutions/current/
```

## Full Workflow

### Step 0: Extract Run ID and Feature Slug from Spec

**First action**: Read the spec and extract the RUN_ID from frontmatter and determine the spec directory.

```bash
# Extract runId from spec frontmatter
RUN_ID=$(grep "^runId:" {spec-path} | awk '{print $2}')
echo "RUN_ID: $RUN_ID"

# Extract feature slug from the spec path
# Path pattern: .../specs/{runId}-{feature-slug}/spec.md
# Use sed to extract directory name without nested command substitution
SPEC_PATH="{spec-path}"
DIR_NAME=$(echo "$SPEC_PATH" | sed 's|^.*specs/||; s|/spec.md$||')
FEATURE_SLUG=$(echo "$DIR_NAME" | sed "s/^${RUN_ID}-//")
echo "FEATURE_SLUG: $FEATURE_SLUG"
```

**CRITICAL**: Execute this entire block as a single multi-line Bash tool call. The comment on the first line is REQUIRED - without it, command substitution `$(...)` causes parse errors.

**If RUN_ID not found:**
Generate one now (for backwards compatibility with old specs):

```bash
# Generate timestamp-based hash for unique ID
TIMESTAMP=$(date +%s)
RUN_ID=$(echo "{feature-name}-$TIMESTAMP" | shasum -a 256 | head -c 6)
echo "Generated RUN_ID: $RUN_ID (spec missing runId)"
```

**CRITICAL**: Execute this entire block as a single multi-line Bash tool call. The comment on the first line is REQUIRED - without it, command substitution `$(...)` causes parse errors.

**Spec Directory Pattern:**
Specs follow the pattern: `specs/{run-id}-{feature-slug}/spec.md`
Plans are generated at: `specs/{run-id}-{feature-slug}/plan.md`

**Announce:** "Using RUN_ID: {run-id} for {feature-slug} implementation"

### Step 0.5: Switch to Worktree Context

**Second action**: After extracting RUN_ID, switch to the worktree created by `/spectacular:spec`.

```bash
# Get absolute repo root to avoid recursive paths
REPO_ROOT=$(git rev-parse --show-toplevel)

# Check if already in correct worktree (avoid double cd)
CURRENT_DIR=$(pwd)
if [[ "$CURRENT_DIR" == "${REPO_ROOT}/.worktrees/${RUN_ID}-main" ]] || [[ "$CURRENT_DIR" == *"/.worktrees/${RUN_ID}-main" ]]; then
  echo "Already in worktree ${RUN_ID}-main"
else
  # Switch to worktree using absolute path
  cd "${REPO_ROOT}/.worktrees/${RUN_ID}-main"
fi
```

**CRITICAL**: Execute this entire block as a single multi-line Bash tool call. The comment on the first line is REQUIRED - without it, command substitution `$(...)` causes parse errors.

**If worktree doesn't exist:**
Error immediately with clear message:

```markdown
**Worktree Not Found**

The worktree for RUN_ID {run-id} doesn't exist.

Run `/spectacular:spec {feature}` first to create the workspace.

Expected worktree: .worktrees/{run-id}-main/
```

**IMPORTANT**: All subsequent operations happen in the worktree context.

- Spec is read from: `.worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/spec.md`
- Plan will be written to: `.worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/plan.md`
- No fallback to main repo (worktree is required)

### Step 1: Dispatch Subagent for Task Decomposition

**Announce:** "Dispatching subagent to generate execution plan from spec."

**IMPORTANT:** Delegate plan generation to a subagent to avoid context bloat. The subagent will read the spec, analyze tasks, and generate the plan in its isolated context.

Use the Task tool with `general-purpose` subagent type:

```
ROLE: Plan generation subagent for spectacular workflow

TASK: Generate execution plan from feature specification

SPEC_PATH: .worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/spec.md
RUN_ID: {run-id}
FEATURE_SLUG: {feature-slug}

IMPLEMENTATION:

**Announce:** "I'm performing task decomposition to create an execution plan."

Follow the Task Decomposition Process below to analyze the spec and generate a plan.

**The process will:**

1. Read the spec from SPEC_PATH above
2. Extract or design tasks (handles specs with OR without Implementation Plan section)
3. Validate task quality (no XL tasks, explicit files, proper chunking)
4. Analyze file dependencies between tasks
5. Group tasks into phases (sequential or parallel)
6. Calculate execution time estimates with parallelization savings
7. Generate plan.md in the spec directory

**Critical validations:**
- XL tasks (>8h) -> Must split before planning
- Missing files -> Must specify exact paths
- Missing acceptance criteria -> Must add 3-5 criteria
- Wildcard patterns -> Must be explicit
- Too many S tasks (>30%) -> Bundle into thematic M/L tasks

**Plan output location:**
.worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/plan.md

**Plan frontmatter must include:**
```yaml
---
runId: {run-id}
feature: {feature-slug}
created: YYYY-MM-DD
status: ready
---
```

**After plan generation:**
Report back to orchestrator with:
- Plan location
- Summary of phases and tasks
- Parallelization time savings
- Any validation issues encountered

If validation fails, report issues clearly so user can fix spec and re-run.
```

**Wait for subagent completion** before proceeding to Step 2.

### Step 2: Review Plan Output

After subagent completes, review the generated plan:

```bash
cat specs/{run-id}-{feature-slug}/plan.md
```

Verify:

- Phase strategies make sense (parallel for independent tasks)
- Dependencies are correct (based on file overlaps)
- No XL tasks (all split into M or smaller)
- Time savings calculation looks reasonable

### Step 2.5: Commit Plan to Worktree

After plan generation and review, commit the plan to the `{run-id}-main` branch in the worktree:

```bash
cd .worktrees/${RUN_ID}-main
git add specs/
git commit -m "plan: add ${FEATURE_SLUG} implementation plan [${RUN_ID}]"
```

This ensures the plan is tracked in the worktree branch and doesn't affect the main repo.

### Step 3: Report to User

**IMPORTANT**: After reporting completion, **STOP HERE**. Do not proceed to execution automatically. The user must review the plan and explicitly run `/spectacular:execute` when ready.

Provide comprehensive summary:

````markdown
**Execution Plan Generated & Committed**

**RUN_ID**: {run-id}
**Feature**: {feature-slug}
**Location**: .worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/plan.md
**Branch**: {run-id}-main (committed in worktree)

## Plan Summary

**Phases**: {count}

- Sequential: {count} phases ({tasks} tasks)
- Parallel: {count} phases ({tasks} tasks)

**Tasks**: {total-count}

- L (4-8h): {count}
- M (2-4h): {count}
- S (1-2h): {count}

## Time Estimates

**Sequential Execution**: {hours}h
**With Parallelization**: {hours}h
**Time Savings**: {hours}h ({percent}% faster)

## Parallelization Opportunities

{For each parallel phase:}

- **Phase {id}**: {task-count} tasks can run simultaneously
  - Tasks: {task-names}
  - Time: {sequential}h -> {parallel}h
  - Savings: {hours}h

## Next Steps (User Actions - DO NOT AUTO-EXECUTE)

**The plan command is complete. The following are suggestions for the user, not instructions to execute automatically.**

### 1. Review the Plan

```bash
cat .worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/plan.md
```

Verify task breakdown, dependencies, and estimates are correct.

### 2. Execute the Plan (when ready)

```bash
/spectacular:execute @.worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/plan.md
```

This is a separate command. Only run after reviewing the plan.

### 3. Modify Plan (if needed)

```bash
# Edit the plan file directly
vim .worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/plan.md

# Commit changes
cd .worktrees/{run-id}-main
git add specs/
git commit -m "plan: adjust task breakdown [${RUN_ID}]"

# Then execute
/spectacular:execute @.worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/plan.md
```

````

---

## Task Decomposition Process

This section details how to transform a feature specification into a structured implementation plan. The subagent dispatched in Step 1 follows this process.

### PR-Sized Chunks Philosophy

**Tasks should be PR-sized, thematically coherent units** - not mechanical file-by-file splits.

**Think like a senior engineer:**

- Bad: "Add schema" + "Install dependency" + "Add routes" (3 tiny tasks)
- Good: "Database Foundation" (schema + migration + dependencies as one unit)

**Task chunking principles:**

1. **Thematic Coherence** - Task represents a complete "thing"

   - Complete subsystem (agent system with tools + config + types)
   - Complete layer (all service methods for a feature)
   - Complete feature slice (UI flow from form to preview to confirm)

2. **Natural PR Size** - Reviewable in one sitting (4-7h)

   - M (3-5h): Sweet spot for most tasks
   - L (5-7h): Complex but coherent units (full UI layer, complete API surface)
   - S (1-2h): Rare - only for truly standalone work

3. **Logical Boundaries** - Clear separation points

   - Layer boundaries (Models, Services, Actions, UI)
   - Subsystem boundaries (Agent, Import Service, API)
   - Feature boundaries (Auth, Import, Dashboard)

4. **Stackable** - Dependencies flow cleanly
   - Database -> Logic -> API -> UI
   - Foundation -> Core -> Integration

**Good chunking examples:**

```
GOOD: PR-sized, thematic chunks
- Task 1: Database Foundation (M - 4h)
  - Schema changes + migration + dependency install
  - One coherent "foundation" PR

- Task 2: Agent System (L - 6h)
  - Agent config + tools + schemas + types
  - Complete agent subsystem as a unit

- Task 3: Import Service Layer (M - 4h)
  - All service methods + business logic
  - Clean layer boundary

- Task 4: API Surface (L - 6h)
  - Server actions + SSE route
  - Complete API interface

- Task 5: Import UI (L - 7h)
  - All components + page + integration
  - Complete user-facing feature

Total: 5 tasks, 27h
Each task is a reviewable PR that adds value
```

```
BAD: Too granular, mechanical splits
- Task 1: Add schema fields (S - 2h)
- Task 2: Create migration (S - 1h)
- Task 3: Install dependency (S - 1h)
- Task 4: Create agent config (M - 3h)
- Task 5: Create fetch tool (S - 1h)
- Task 6: Create schemas (S - 2h)
- Task 7: Create service (M - 4h)
- Task 8: Create actions (M - 3h)
- Task 9: Create SSE route (M - 3h)
- Task 10: Create form component (S - 2h)
- Task 11: Create progress component (S - 2h)
- Task 12: Create preview component (M - 2h)
- Task 13: Add routes (S - 1h)
- Task 14: Integrate components (S - 1h)

Total: 14 tasks, 28h
Too many tiny PRs, no coherent units
```

**Bundling heuristics:**

If you're creating S tasks, ask:

- Can this bundle with a related M task?
- Does this complete a subsystem or layer?
- Would a senior engineer create a separate PR for this?

**Common bundling patterns:**

- Schema + migration + dependencies -> "Database Foundation"
- Agent + tools + schemas -> "Agent System"
- Service + helper functions -> "Service Layer"
- Actions + API routes -> "API Layer"
- All UI components for a flow -> "UI Layer"

### Decomposition Step 1: Read Spec and Extract/Design Tasks

Read the spec file and extract tasks. The spec may provide tasks in two ways:

**Option A: Spec has "Implementation Plan" section** (structured task breakdown)
- Extract tasks directly from this section
- Each task should have: ID, description, files, complexity, acceptance criteria

**Option B: Spec has no "Implementation Plan"** (lean spec - requirements only)
- Analyze the requirements and design task breakdown yourself
- Look at: Functional Requirements, Architecture section, Files to Create/Modify
- Design PR-sized chunks following the chunking philosophy above
- Create tasks that implement all requirements

For each task (extracted or designed), capture:

- **Task ID** (from heading)
- **Description** (what to implement)
- **Repo** (multi-repo only - which repo this task belongs to)
- **Files** (explicit paths from spec)
- **Complexity** (S/M/L/XL - estimated hours)
- **Acceptance Criteria** (checklist items)
- **Implementation Steps** (detailed steps)

**Example extraction:**

```markdown
Spec has:

### Task 1: Database Schema

**Complexity**: M (2-4h)
**Files**:

- prisma/schema.prisma
- prisma/migrations/

**Description**: Add VerificationToken model for Auth.js...

**Acceptance**:

- [ ] Model matches Auth.js spec
- [ ] Migration runs cleanly

Extract to:
{
id: "task-1-database-schema",
description: "Add VerificationToken model",
files: ["prisma/schema.prisma", "prisma/migrations/"],
complexity: "M",
estimated_hours: 3,
acceptance_criteria: [...],
steps: [...]
}
```

**Multi-repo task extraction:**

For each task, also capture:
- **Repo** (multi-repo only): Which repo this task belongs to

```
{
  id: "task-1-1-database",
  repo: "backend",  // NEW FIELD - required in multi-repo mode
  files: ["prisma/schema.prisma"],
  ...
}
```

**Validation in multi-repo mode:**
- Every task MUST have a `repo` field
- Repo must be one of the detected repos in workspace
- Files are relative to the repo root (not workspace root)

### Decomposition Step 2: Validate Task Quality & Chunking

For each task, check for quality issues:

**CRITICAL (must fix):**

- XL complexity (>8h) -> Must split into M/L tasks
- No files specified -> Must add explicit file paths
- No acceptance criteria -> Must add 3-5 testable criteria
- Wildcard patterns (`src/**/*.ts`) -> Must use explicit paths
- Too many S tasks (>30% of total) -> Bundle into thematic M/L tasks

**HIGH (strongly recommend):**

- Standalone S task that could bundle with related work
- L complexity (5-8h) -> Verify it's a coherent unit, not arbitrary split
- >10 files -> Likely too large, consider splitting by subsystem
- <50 char description -> Add more detail about what subsystem/layer this completes
- <3 acceptance criteria -> Add more specific criteria

**Chunking validation:**

- If task is S (1-2h), verify it's truly standalone:

  - Can't be bundled with schema/migration/dependencies?
  - Can't be bundled with related service/action/component?
  - Would a senior engineer create a separate PR for this?

- If >50% of tasks are S, that's a red flag:
  - Likely too granular
  - Missing thematic coherence
  - Bundle related S tasks into M tasks

**If CRITICAL issues found:**

- STOP and report issues to user
- User must update spec or adjust chunking
- Re-run skill after fixes

**If only HIGH issues:**

- Report warnings
- Offer to continue or fix

### Decomposition Step 3: Analyze File Dependencies

Build dependency graph by analyzing file overlaps:

**Algorithm:**

```
For each task T1:
  For each task T2 (where T2 appears after T1):
    shared_files = intersection(T1.files, T2.files)

    If shared_files is not empty:
      T2.dependencies.add(T1.id)
      T2.dependency_reason = "Shares files: {shared_files}"
```

**Example:**

```
Task 1: ["prisma/schema.prisma"]
Task 2: ["src/lib/models/auth.ts"]
Task 3: ["prisma/schema.prisma", "src/types/auth.ts"]

Analysis:
- Task 2: No dependencies (no shared files with Task 1)
- Task 3: Depends on Task 1 (shares prisma/schema.prisma)
```

**Architectural dependencies:**
Also add dependencies based on layer order:

- Models -> Services -> Actions -> UI
- Database -> Types -> Logic -> API -> Components

**Cross-repo dependency analysis:**

In multi-repo mode, tasks in DIFFERENT repos are automatically independent (no file conflicts possible):

```
Task A: repo: backend, files: [src/api.ts]
Task B: repo: frontend, files: [src/api.ts]

Analysis: INDEPENDENT (different repos, even same filename)
```

Tasks in the SAME repo follow normal dependency rules:

```
Task A: repo: backend, files: [prisma/schema.prisma]
Task B: repo: backend, files: [prisma/schema.prisma, src/models.ts]

Analysis: Task B depends on Task A (same repo, shared file)
```

**Cross-repo sequential dependencies:**

Some tasks have logical dependencies across repos (not file-based):

```
Task A: repo: shared-lib, files: [src/types.ts]  # Defines shared types
Task B: repo: backend, files: [src/api.ts]       # Uses shared types

Analysis: Task B should run after Task A (API depends on shared types)
```

Mark these with explicit `depends_on` in the plan.

### Decomposition Step 4: Group into Phases

Group tasks into phases using dependency graph:

**Phase grouping algorithm:**

```
1. Start with tasks that have no dependencies (roots)
2. Group all independent roots into Phase 1
3. Remove roots from graph
4. Repeat until all tasks grouped

For each phase:
  - If all tasks independent: strategy = "parallel"
  - If any dependencies exist: strategy = "sequential"
```

**Example:**

```
Tasks:
- Task 1: [] (no deps)
- Task 2: [] (no deps)
- Task 3: [task-1, task-2]
- Task 4: [task-3]

Grouping:
Phase 1: [Task 1, Task 2] - parallel (independent)
Phase 2: [Task 3] - sequential (waits for Phase 1)
Phase 3: [Task 4] - sequential (waits for Phase 2)
```

### Decomposition Step 5: Calculate Execution Estimates

For each phase, calculate:

- **Sequential time**: Sum of all task hours
- **Parallel time**: Max of all task hours (if parallel strategy)
- **Time savings**: Sequential - Parallel

**Example:**

```
Phase 2 (parallel):
- Task A: 3h
- Task B: 2h
- Task C: 4h

Sequential: 3 + 2 + 4 = 9h
Parallel: max(3, 2, 4) = 4h
Savings: 9 - 4 = 5h (56% faster)
```

### Decomposition Step 6: Generate plan.md

Write plan to `{spec-directory}/plan.md`:

**Single-repo template:**

````markdown
# Feature: {Feature Name} - Implementation Plan

> **Generated by:** Task Decomposition skill
> **From spec:** {spec-path}
> **Created:** {date}

## Execution Summary

- **Total Tasks**: {count}
- **Total Phases**: {count}
- **Sequential Time**: {hours}h
- **Parallel Time**: {hours}h
- **Time Savings**: {hours}h ({percent}%)

**Parallel Opportunities:**

- Phase {id}: {task-count} tasks ({hours}h saved)

---

## Phase {N}: {Phase Name}

**Strategy**: {sequential|parallel}
**Reason**: {why this strategy}

### Task {ID}: {Name}

**Files**:

- {file-path-1}
- {file-path-2}

**Complexity**: {S|M|L} ({hours}h)

**Dependencies**: {[task-ids] or "None"}

**Description**:
{What to implement and why}

**Implementation Steps**:

1. {step-1}
2. {step-2}
3. {step-3}

**Acceptance Criteria**:

- [ ] {criterion-1}
- [ ] {criterion-2}
- [ ] {criterion-3}

**Mandatory Patterns**:

> **Constitution**: All code must follow @docs/constitutions/current/

See architecture.md for layer boundaries and patterns.md for required patterns.

**TDD**: Follow `test-driven-development` skill (write test first, watch fail, minimal code, watch pass)

**Quality Gates**:

```bash
pnpm biome check --write .
pnpm test {test-files}
```
````

---

{Repeat for all tasks in all phases}

**Multi-repo plan template:**

````markdown
# Feature: {Feature Name} - Implementation Plan

> **Generated by:** Task Decomposition skill
> **From spec:** {spec-path}
> **Created:** {date}
> **Workspace Mode:** multi-repo
> **Repos:** backend, frontend, shared-lib

## Execution Summary

- **Total Tasks**: {count}
- **Total Phases**: {count}
- **Sequential Time**: {hours}h
- **Parallel Time**: {hours}h
- **Time Savings**: {hours}h ({percent}%)

**Parallel Opportunities:**

- Phase {id}: {task-count} tasks ({hours}h saved)

---

## Phase {N}: {Phase Name}

**Strategy**: {sequential|parallel}
**Repos in phase**: {list of repos with tasks in this phase}

### Task {ID}: {Name}

**Repo**: {repo-name}
**Files**:

- {file-path-1}
- {file-path-2}

**Constitution**: @{repo-name}/docs/constitutions/current/

**Complexity**: {S|M|L} ({hours}h)

**Dependencies**: {[task-ids] or "None"}
**Cross-repo dependencies**: {[task-ids in other repos] or "None"}

**Description**:
{What to implement and why}

**Implementation Steps**:

1. {step-1}
2. {step-2}
3. {step-3}

**Acceptance Criteria**:

- [ ] {criterion-1}
- [ ] {criterion-2}
- [ ] {criterion-3}

**Mandatory Patterns**:

> **Constitution**: All code must follow @{repo-name}/docs/constitutions/current/

See architecture.md for layer boundaries and patterns.md for required patterns.

**TDD**: Follow `test-driven-development` skill (write test first, watch fail, minimal code, watch pass)

**Quality Gates**:

```bash
cd {repo-name}
pnpm biome check --write .
pnpm test {test-files}
```
````

---

{Repeat for all tasks in all phases}

````

### Decomposition Step 7: Report to Orchestrator

After generating plan, report back to orchestrator with:

**Single-repo report:**

```markdown
Task Decomposition Complete

**Plan Location**: specs/{run-id}-{feature-slug}/plan.md

## Breakdown
- Phases: {count}
- Tasks: {count}
- Complexity: {XL}: {n}, {L}: {n}, {M}: {n}, {S}: {n}

## Execution Strategy
- Sequential Phases: {count} ({tasks} tasks)
- Parallel Phases: {count} ({tasks} tasks)

## Time Estimates
- Sequential Execution: {hours}h
- With Parallelization: {hours}h
- **Time Savings: {hours}h ({percent}% faster)**
```

**Multi-repo report:**

```markdown
Task Decomposition Complete

**Plan Location**: specs/{run-id}-{feature-slug}/plan.md
**Workspace Mode**: multi-repo

## Per-Repo Breakdown

| Repo | Tasks | Hours |
|------|-------|-------|
| backend | 4 | 12h |
| frontend | 3 | 9h |
| shared-lib | 1 | 2h |

## Execution Strategy
- Sequential Phases: {count} ({tasks} tasks)
- Parallel Phases: {count} ({tasks} tasks)

## Cross-Repo Parallelization
- Phase 2: backend + frontend tasks run in parallel (different repos)
- Time saved: 6h (tasks execute simultaneously in separate repos)

## Time Estimates
- Sequential Execution: {hours}h
- With Parallelization: {hours}h
- **Time Savings: {hours}h ({percent}% faster)**
````

---

## Quality Rules

**Task Sizing (PR-focused):**
- S (1-2h): Rare - only truly standalone work (e.g., config-only changes)
  - Most S tasks should bundle into M
  - Ask: "Would a senior engineer PR this alone?"
- M (3-5h): Sweet spot - most tasks should be this size
  - Complete subsystem, layer, or feature slice
  - Reviewable in one sitting
  - Thematically coherent unit
- L (5-7h): Complex coherent units (use for major subsystems)
  - Full UI layer with all components
  - Complete API surface (actions + routes)
  - Major feature integration
- XL (>8h): NEVER - always split into M/L tasks

**Chunking Standards:**
- <30% S tasks is a red flag (too granular)
- Most tasks should be M (60-80%)
- Some L tasks for major units (10-30%)
- Rare S tasks for truly standalone work (<10%)

**File Specificity:**
- Good: `src/lib/models/auth.ts`
- Good: `src/components/auth/LoginForm.tsx`
- Bad: `src/**/*.ts` (too vague)
- Bad: `src/lib/models/` (specify exact files)

**Acceptance Criteria:**
- 3-5 specific, testable criteria
- Quantifiable (tests pass, build succeeds, API returns 200)
- Not vague ("works well", "is good")
- Not too many (>7 - task is too large)

**Dependencies:**
- Minimal (only true blockers)
- Explicit reasons (shares file X)
- No circular dependencies
- Not over-constrained (everything depends on everything)

## Error Handling

### Missing Worktree

If the worktree doesn't exist when trying to switch context:

```markdown
**Worktree Not Found**

The worktree for RUN_ID {run-id} doesn't exist at .worktrees/{run-id}-main/

This means `/spectacular:spec` hasn't been run yet for this feature.

## Resolution

1. Run `/spectacular:spec {feature-description}` first to create the worktree
2. Then run `/spectacular:plan @.worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/spec.md`

Or if you have an existing spec in the main repo, it needs to be migrated to a worktree first.
```

### Validation Failures

If the skill finds quality issues:

```markdown
**Plan Generation Failed - Spec Quality Issues**

The spec has issues that prevent task decomposition:

**CRITICAL Issues** (must fix):
- Task 3: XL complexity (12h estimated) - split into M/L tasks
- Task 5: No files specified - add explicit file paths
- Task 7: No acceptance criteria - add 3-5 testable criteria
- Too many S tasks (5 of 8 = 63%) - bundle into thematic M/L tasks

**HIGH Issues** (strongly recommend):
- Task 2 (S - 1h): "Add routes" - bundle with UI components task
- Task 4 (S - 2h): "Create schemas" - bundle with agent or service task
- Task 6: Wildcard pattern `src/**/*.ts` - specify exact files

## Fix These Issues

1. Edit the spec at {spec-path}
2. Address all CRITICAL issues (required)
3. Consider fixing HIGH issues (recommended)
4. Bundle S tasks into thematic M/L tasks for better PR structure
5. Re-run: `/spectacular:plan @{spec-path}`
```

### No Tasks Found

If spec has no "Implementation Plan" section and insufficient detail:

```markdown
**Cannot Generate Plan - No Tasks Found**

The spec at {spec-path} doesn't have an "Implementation Plan" section with tasks,
and lacks sufficient detail to design tasks automatically.

The spec must have either:
- An "Implementation Plan" section with tasks, OR
- Sufficient requirements and architecture details to design tasks

Current spec has:
- Functional Requirements: [YES/NO]
- Architecture section: [YES/NO]
- Files to create/modify: [YES/NO]

Use `/spectacular:spec` to generate a complete spec with task breakdown first:

```bash
/spectacular:spec "your feature description"
```

Then run `/spectacular:plan` on the generated spec.
```

### Circular Dependencies

If tasks have circular dependencies:

```markdown
**Circular Dependencies Detected**

The task dependency graph has cycles:
- Task A depends on Task B
- Task B depends on Task C
- Task C depends on Task A

This makes execution impossible.

## Resolution

Review the task file dependencies in the spec:
1. Check which files each task modifies
2. Ensure dependencies flow in one direction
3. Consider splitting tasks to break cycles
4. Re-run `/spectacular:plan` after fixing
```

## Integration with Other Skills

**Before:** Use `brainstorming` and `spec-feature` to create complete spec

**After:** Use `/spectacular:execute` command to run plan with `subagent-driven-development`

**Pairs with:**
- `subagent-driven-development` - Executes individual tasks
- `finishing-a-development-branch` - Completes implementation

## Project-Specific Configuration

For projects with a constitution, reference it in every task:

> **Constitution**: All tasks MUST follow @docs/constitutions/current/

Every task must include:
- Reference to constitution for architecture (layer boundaries, dependencies)
- Reference to constitution for patterns (validation, state management, etc.)
- Quality gates (linting, testing, building)

**Quality gates:**
```bash
pnpm biome check --write .
pnpm test
```

## Important Notes

- **Automatic strategy selection** - Skill analyzes dependencies and chooses sequential vs parallel
- **File-based dependencies** - Tasks sharing files must run sequentially
- **Quality gates** - Validates before generating (prevents bad plans)
- **Architecture adherence** - All tasks must follow project constitution at @docs/constitutions/current/
