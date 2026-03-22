---
name: superhuman
version: 0.1.0
description: >
  AI-native software development lifecycle that replaces traditional SDLC.
  Triggers on "plan and build", "break this into tasks", "build this feature
  end-to-end", "sprint plan this", "superhuman this", or any multi-step
  development task. Decomposes work into dependency-graphed sub-tasks, executes
  in parallel waves with TDD verification, and tracks progress on a persistent
  board. Handles features, refactors, greenfield projects, and migrations.
category: engineering
tags:
  - sdlc
  - planning
  - parallel-execution
  - tdd
  - task-management
  - workflow
recommended_skills: [agile-scrum, test-strategy, project-execution, clean-code, code-review-mastery]
platforms:
  - claude-code
  - gemini-cli
  - openai-codex
  - mcp
sources:
  - url: https://github.com/AbsolutelySkilled/AbsolutelySkilled
    accessed: 2026-03-14
    description: Original skill design combining sprint planning, TDD, spec-driven development, and parallel agent execution into a unified AI-native lifecycle
license: MIT
maintainers:
  - github: maddhruv
---

When this skill is activated, always start your first response with the 🧢 emoji.

# Superhuman: AI-Native Development Lifecycle

Superhuman is a development lifecycle built from the ground up for AI agents. Traditional methods like Agile, Waterfall, and TDD were designed around human constraints - limited parallelism, context switching costs, communication overhead, and meetings. AI agents have none of these constraints. Superhuman exploits this by decomposing work into dependency-graphed sub-tasks, executing independent tasks in parallel waves, enforcing TDD verification at every step, and tracking everything on a persistent board that survives across sessions.

The model has 7 phases: **INTAKE - DECOMPOSE - DISCOVER - PLAN - EXECUTE - VERIFY - CONVERGE**.

---

## Activation Banner

**At the very start of every Superhuman invocation**, before any other output, display this ASCII art banner:

```
███████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗
██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║
███████╗██║   ██║██████╔╝█████╗  ██████╔╝███████║██║   ██║██╔████╔██║███████║██╔██╗ ██║
╚════██║██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║
███████║╚██████╔╝██║     ███████╗██║  ██║██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║
╚══════╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
```

This banner is mandatory. It signals to the user that Superhuman mode is active.

---

## Activation Protocol

**Immediately after displaying the banner**, enter plan mode before doing anything else:

1. **On platforms with native plan mode** (e.g., Claude Code's `EnterPlanMode`, Gemini CLI's planning mode): invoke the native plan mode mechanism immediately.
2. **On platforms without native plan mode**: simulate plan mode by completing all planning phases (INTAKE through PLAN) in full before making any code changes. Present the complete plan to the user for explicit approval before proceeding to EXECUTE.

This ensures that every Superhuman invocation begins with structured thinking. The first four phases (INTAKE, DECOMPOSE, DISCOVER, PLAN) are inherently planning work - no files should be created or modified until the user has approved the plan and execution begins in Phase 5.

---

## Session Resume Protocol

When Superhuman is invoked and a `.superhuman/board.md` already exists in the project root:

1. **Detect**: Read the existing board and determine its status (`in-progress`, `blocked`, `completed`)
2. **Display**: Print a compact status summary showing completed/in-progress/blocked/remaining tasks
3. **Resume**: Pick up from the last incomplete wave - do NOT restart from INTAKE
4. **Reconcile**: If the codebase has changed since the last session (e.g., manual edits, other commits), run a quick diff check against the board's expected state and flag any conflicts before resuming

If the board is marked `completed`, ask the user whether to start a new Superhuman session (archive the old board to `.superhuman/archive/`) or review the completed work.

**Never blow away an existing board without explicit user confirmation.**

---

## Codebase Convention Detection

**Before INTAKE begins**, automatically detect the project's conventions by scanning for key files. This grounds all subsequent phases in reality rather than assumptions.

### Auto-detect Checklist
| Signal | Files to Check |
|---|---|
| **Package manager** | `package-lock.json` (npm), `yarn.lock` (yarn), `pnpm-lock.yaml` (pnpm), `bun.lockb` (bun), `Cargo.lock` (cargo), `go.sum` (go) |
| **Language/Runtime** | `tsconfig.json` (TypeScript), `pyproject.toml` / `setup.py` (Python), `go.mod` (Go), `Cargo.toml` (Rust) |
| **Test runner** | `jest.config.*`, `vitest.config.*`, `pytest.ini`, `.mocharc.*`, test directory patterns |
| **Linter/Formatter** | `.eslintrc.*`, `eslint.config.*`, `.prettierrc.*`, `ruff.toml`, `.golangci.yml` |
| **Build system** | `Makefile`, `webpack.config.*`, `vite.config.*`, `next.config.*`, `turbo.json` |
| **CI/CD** | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` |
| **Available scripts** | `scripts` section of `package.json`, `Makefile` targets |
| **Directory conventions** | `src/`, `lib/`, `app/`, `tests/`, `__tests__/`, `spec/` |
| **Codedocs** | `docs/.codedocs.json`, `documentation/.codedocs.json`, or any `.codedocs.json` in the repo |

### Codedocs Detection

If a `.codedocs.json` manifest is found, the repo has structured codedocs output. Record its location on the board and set a flag `codedocs_available: true`. This changes how DISCOVER and PLAN operate - see those phases for details.

When codedocs is available, read `docs/OVERVIEW.md` and `docs/GETTING_STARTED.md` immediately during convention detection and append their key facts (tech stack, module map, entry points, dev commands) to the `## Project Conventions` section of the board. This front-loads context that would otherwise require separate codebase exploration in DISCOVER.

### Output
Write the detected conventions to the board under a `## Project Conventions` section. Reference these conventions in every subsequent phase - particularly PLAN and the Mandatory Tail Tasks verification step.

---

## When to Use This Skill

**Use Superhuman when:**
- Multi-step feature development touching 3+ files or components
- User says "build this end-to-end" or "plan and execute this"
- User says "break this into tasks" or "sprint plan this"
- Any task requiring planning + implementation + verification
- Greenfield projects, major refactors, or migrations
- Complex bug fixes that span multiple systems

**Do NOT use Superhuman when:**
- Single-file bug fixes or typo corrections
- Quick questions or code explanations
- Tasks the user wants to do manually with your guidance
- Pure research or exploration tasks

---

## Key Principles

### 1. Dependency-First Decomposition
Every task is a node in a directed acyclic graph (DAG), not a flat list. Dependencies between tasks are explicit. This prevents merge conflicts, ordering bugs, and wasted work.

### 2. Wave-Based Parallelism
Tasks at the same depth in the dependency graph form a "wave". All tasks in a wave execute simultaneously via parallel agents. Waves execute in serial order. This maximizes throughput while respecting dependencies.

### 3. Test-First Verification
Every sub-task writes tests before implementation. A task is only "done" when its tests pass. No exceptions for "simple" changes - tests are the proof of correctness.

### 4. Persistent State
All progress is tracked in `.superhuman/board.md` in the project root. This file survives across sessions, enabling resume, audit, and handoff. The user chooses during INTAKE whether the board is git-tracked or gitignored.

### 5. Interactive Intake
Never assume. Scale questioning depth to task complexity - simple tasks get 3 questions, complex ones get 8-10. Extract requirements, constraints, and success criteria before writing a single line of code.

---

## Core Concepts

### The 7 Phases

```
INTAKE --> DECOMPOSE --> DISCOVER --> PLAN --> EXECUTE --> VERIFY --> CONVERGE
  |           |             |          |         |           |          |
  |  gather   |  build DAG  | research | detail  | parallel  | test +   | merge +
  |  context  |  + waves    | per task | per task| waves     | verify   | close
```

### Task Graph
A directed acyclic graph (DAG) where each node is a sub-task and edges represent dependencies. Tasks with no unresolved dependencies can execute in parallel. See `references/dependency-graph-patterns.md`.

### Execution Waves
Groups of independent tasks assigned to the same depth level in the DAG. Wave 1 runs first (all tasks in parallel), then Wave 2 (all tasks in parallel), and so on. See `references/wave-execution.md`.

### Board
The `.superhuman/board.md` file is the single source of truth. It contains the intake summary, task graph, wave assignments, per-task status, research notes, plans, and verification results. See `references/board-format.md`.

### Sub-task Lifecycle
```
pending --> researching --> planned --> in-progress --> verifying --> done
                                           |                |
                                           +--- blocked     +--- failed (retry)
```

---

## Phase 1: INTAKE (Interactive Interview)

The intake phase gathers all context needed to decompose the task. Scale depth based on complexity.

### Complexity Detection
- **Simple** (single component, clear scope): 3 questions
- **Medium** (multi-component, some ambiguity): 5 questions
- **Complex** (cross-cutting, greenfield, migration): 8-10 questions

### Core Questions (always ask)
1. **Problem Statement**: What exactly needs to be built or changed? What triggered this work?
2. **Success Criteria**: How will we know this is done? What does "working" look like?
3. **Constraints**: Are there existing patterns, libraries, or conventions we must follow?

### Extended Questions (medium + complex)
4. **Existing Code**: Is there related code already in the repo? Should we extend it or build fresh?
5. **Dependencies**: Does this depend on external APIs, services, or other in-progress work?

### Deep Questions (complex only)
6. **Edge Cases**: What are the known edge cases or failure modes?
7. **Testing Strategy**: Are there existing test patterns? Integration vs unit preference?
8. **Rollout**: Any migration steps, feature flags, or backwards compatibility needs?
9. **Documentation**: What docs need updating? API docs, README, architecture docs?
10. **Priority**: Which parts are most critical? What can be deferred if needed?

### Board Persistence Question (always ask)
Ask: "Should the `.superhuman/` board be git-tracked (audit trail, resume across machines) or gitignored (local working state)?"

### Output
Write the intake summary to `.superhuman/board.md` with all answers captured. See `references/intake-playbook.md` for the full question bank organized by task type.

---

## Phase 2: DECOMPOSE (Task Graph Creation)

Break the intake into atomic sub-tasks and build the dependency graph.

### Sub-task Anatomy
Each sub-task must have:
- **ID**: Sequential identifier (e.g., `SH-001`)
- **Title**: Clear, action-oriented (e.g., "Create user authentication middleware")
- **Description**: 2-3 sentences on what this task does
- **Type**: `code` | `test` | `docs` | `infra` | `config`
- **Complexity**: `S` (< 50 lines) | `M` (50-200 lines) | `L` (200+ lines - consider splitting)
- **Dependencies**: List of task IDs this depends on (e.g., `[SH-001, SH-003]`)

### Decomposition Rules
1. Every task should be S or M complexity. If L, decompose further
2. Test tasks are separate from implementation tasks
3. Infrastructure/config tasks come before code that depends on them
4. Documentation tasks depend on the code they document
5. Aim for 5-15 sub-tasks. Fewer means under-decomposed; more means over-engineered
6. Every task graph MUST end with three mandatory tail tasks (see below)
7. Apply the complexity budget (see below)

### Complexity Budget
After decomposition, sanity-check total scope before proceeding:
- Count the total number of tasks by complexity: S (small), M (medium), L (large)
- If any L tasks remain, decompose them further - L tasks are not allowed
- If total estimated scope exceeds **15 M-equivalent tasks** (where 1 L = 3 M, 1 S = 0.5 M), flag to the user that scope may be too large for a single Superhuman session
- Suggest splitting into multiple Superhuman sessions with clear boundaries (e.g., "Session 1: backend API, Session 2: frontend integration")
- The user can override and proceed, but they must explicitly acknowledge the scope

### Mandatory Tail Tasks
Every Superhuman task graph must include these three tasks as the final tasks, in this order:

**Third-to-last task: Self Code Review**
- **Type**: `review`
- **Title**: "Self code review of all changes"
- **Description**: Run a structured code review of all changes made across every completed sub-task using the `code-review-mastery` methodology. Get the full diff of all changes since the rollback point. Execute the review pyramid bottom-up: Security > Correctness > Performance > Design > Readability > Convention > Testing. Classify each finding as `[MAJOR]` or `[MINOR]`. Fix all `[MAJOR]` findings immediately and address reasonable `[MINOR]` findings. Re-run the review after fixes to confirm no new issues were introduced. Only proceed when no `[MAJOR]` findings remain.
- **Dependencies**: All other implementation/test/docs tasks
- **Acceptance Criteria**: Zero `[MAJOR]` findings remaining after fixes. All `[MINOR]` findings documented on the board (fixed or explicitly deferred).

**Second-to-last task: Requirements Validation**
- **Type**: `verify`
- **Title**: "Validate changes against original requirements"
- **Description**: Review all changes made across every completed sub-task and compare them against the original user prompt and intake summary. Verify that every requirement, success criterion, and constraint from INTAKE is satisfied. If any requirement is unmet or the implementation deviates from what was asked, flag the gaps and loop back to EXECUTE to address them. Do NOT proceed to the final task until all requirements are confirmed met.
- **Dependencies**: The self code review task above
- **Acceptance Criteria**: Every success criterion from INTAKE is demonstrably satisfied. If gaps are found, reiterate until they are resolved.

**Last task: Full Project Verification**
- **Type**: `verify`
- **Title**: "Run full project verification suite"
- **Description**: Run all available verification checks in the repo, in order. Use the project's package manager scripts (check `package.json`, `Makefile`, `pyproject.toml`, etc.) - never invoke tools directly. Skip any that are not configured in the project - only run what exists:
  1. **Tests** - Run the test script (`npm test`, `yarn test`, `pnpm test`, `make test`, `pytest`, etc.)
  2. **Lint** - Run the lint script (`npm run lint`, `yarn lint`, `pnpm lint`, `make lint`, etc.)
  3. **Typecheck** - Run the typecheck script (`npm run typecheck`, `yarn typecheck`, `pnpm typecheck`, `make typecheck`, etc.)
  4. **Build** - Run the build script (`npm run build`, `yarn build`, `pnpm build`, `make build`, etc.)
- **Dependencies**: The requirements validation task above
- **Acceptance Criteria**: All available checks pass. If any check fails, fix the issues and re-run until green. Do not mark the board as complete until every available check passes.

### Build the DAG
1. List all sub-tasks
2. For each task, identify which other tasks must complete first
3. Draw edges from dependencies to dependents
4. Verify no cycles exist (it's a DAG, not a general graph)

### Assign Waves
Group tasks by depth level in the DAG:
- **Wave 1**: Tasks with zero dependencies (roots of the DAG)
- **Wave 2**: Tasks whose dependencies are all in Wave 1
- **Wave N**: Tasks whose dependencies are all in Waves 1 through N-1

### Present for Approval
Generate an ASCII dependency graph and wave assignment table. Present to the user and wait for explicit approval before proceeding.

Example output:
```
Task Graph:
  SH-001 [config: Init project structure]
    |
    +---> SH-002 [code: Database schema]
    |       |
    |       +---> SH-004 [code: User model]
    |       +---> SH-005 [code: Auth model]
    |
    +---> SH-003 [code: API router setup]
              |
              +---> SH-006 [code: Auth endpoints]
                      |
                      +---> SH-007 [test: Auth integration tests]
                      +---> SH-008 [docs: API documentation]

  --- Mandatory Tail Tasks ---
  SH-007, SH-008
    |
    +---> SH-009 [review: Self code review of all changes]
              |
              +---> SH-010 [verify: Validate changes against original requirements]
                        |
                        +---> SH-011 [verify: Run full project verification suite]

Wave Assignments:
  Wave 1: SH-001                          (1 task, serial)
  Wave 2: SH-002, SH-003                  (2 tasks, parallel)
  Wave 3: SH-004, SH-005, SH-006         (3 tasks, parallel)
  Wave 4: SH-007, SH-008                  (2 tasks, parallel)
  Wave 5: SH-009                          (1 task, self code review)
  Wave 6: SH-010                          (1 task, requirements validation)
  Wave 7: SH-011                          (1 task, full project verification)
```

Update the board with the full task graph and wave assignments. See `references/dependency-graph-patterns.md` for common patterns and the wave assignment algorithm.

---

## Phase 3: DISCOVER (Parallel Research)

Research each sub-task before planning implementation. This phase is parallelizable per wave.

### Per Sub-task Research
For each sub-task, investigate in this order - docs first, source second:

1. **Codedocs Lookup** (if `codedocs_available: true` on the board)
   - Check `docs/INDEX.md` to find which module doc covers the files relevant to this task
   - Read the relevant `docs/modules/<module>.md` for public API, internal structure, dependencies, and implementation notes
   - Check `docs/patterns/` for any cross-cutting pattern docs (error handling, testing strategy, logging) that apply to this task
   - Use `docs/OVERVIEW.md` for architecture context and to understand how this task's module fits into the system
   - **Only proceed to Codebase Exploration below if the docs don't contain enough detail** - flag any gaps in the docs as a staleness note on the board
   - Record which doc files were used in the task's research notes on the board

2. **Codebase Exploration** (always run; use to fill gaps left by docs or when codedocs is not available)
   - Find existing patterns, utilities, and conventions relevant to this task
   - Identify files that will be created or modified
   - Check for reusable functions, types, or components
   - Understand the testing patterns used in the project

3. **Web Research** (when codebase context is insufficient)
   - Official documentation for libraries and APIs involved
   - Best practices and common patterns
   - Known gotchas or breaking changes

4. **Risk Assessment**
   - Flag unknowns or ambiguities
   - Identify potential conflicts with other sub-tasks
   - Note any assumptions that need validation

### Execution Strategy
- Launch parallel Explore agents for all tasks in Wave 1 simultaneously
- Once Wave 1 research completes, launch Wave 2 research, and so on
- Each agent writes its findings to the board under the respective task

### Output
Append research notes to each sub-task on the board:
- Key files identified
- Reusable code/patterns found
- Risks and unknowns flagged
- External docs referenced

---

## Phase 4: PLAN (Execution Planning)

Create a detailed execution plan for each sub-task based on research findings.

### Per Sub-task Plan
For each sub-task, specify:

1. **Files to Create/Modify**: Exact file paths
2. **Test Files**: Test file paths (TDD - these are written first)
3. **Implementation Approach**: Brief description of the approach
4. **Acceptance Criteria**: Specific, verifiable conditions for "done"
5. **Test Cases**: List of test cases to write
   - Happy path tests
   - Edge case tests
   - Error handling tests

### Planning Rules
1. Tests are always planned before implementation
2. Each plan must reference specific reusable code found in DISCOVER
3. Plans must respect the project's existing conventions (naming, structure, patterns)
4. If a plan reveals a missing dependency, update the task graph (re-approve with user)

### Output
Update each sub-task on the board with its execution plan. The board now contains everything an agent needs to execute the task independently.

---

## Phase 5: EXECUTE (Wave-Based Implementation)

Execute tasks wave by wave. Within each wave, spin up parallel agents for independent tasks.

### Pre-Execution Snapshot
Before executing the first wave, create a git safety net:
1. Ensure all current changes are committed or stashed
2. Record the current commit hash on the board under `## Rollback Point`
3. If execution goes catastrophically wrong (build broken after max retries, critical files corrupted), the user can `git reset --hard` to this commit
4. Remind the user of the rollback point hash when flagging unrecoverable failures

### Wave Execution Loop
```
for each wave in [Wave 1, Wave 2, ..., Wave N]:
  for each task in wave (in parallel):
    1. Write tests (TDD - red phase)
    2. Implement code to make tests pass (green phase)
    3. Refactor if needed (refactor phase)
    4. Update board status: in-progress -> verifying
  wait for all tasks in wave to complete
  run wave boundary checks (conflict resolution, progress report)
  proceed to next wave
```

### Agent Context Handoff Format
Each parallel agent receives a standardized prompt with these sections:
```
## Task: {SH-XXX} - {Title}

### Context
{Description from the board}

### Project Conventions
{Detected conventions from Codebase Convention Detection - package manager, test runner, linter, directory patterns}

### Research Notes
{Findings from DISCOVER phase for this task}

### Execution Plan
- Files to create/modify: {list}
- Test files: {list}
- Approach: {from PLAN phase}

### Acceptance Criteria
{Specific, verifiable conditions from PLAN phase}

### Rules
1. Follow TDD: write tests first, then implement
2. Use the project's existing patterns and conventions
3. Do NOT modify files outside your task scope
4. If you encounter a blocker, stop and report it - do not work around it
5. Update the board with your status when done
```

### Wave Boundary Checks
After all tasks in a wave complete, before proceeding to the next wave:

**1. Conflict Resolution**
- Check if any two agents in the wave modified the same file
- If conflicts exist: review both changes, merge them intelligently (prefer the change that better satisfies its task's acceptance criteria), and verify the merged result
- If conflicts cannot be auto-resolved: flag to the user with both versions and let them decide
- Run a quick build/test check after any merge to catch integration issues early

**2. Progress Report**
Print a compact status table after each wave:
```
Wave 2 Complete (3/6 waves done)
-----------------------------------------
| Task   | Status | Notes               |
|--------|--------|----------------------|
| SH-001 | done   |                      |
| SH-002 | done   |                      |
| SH-003 | done   |                      |
| SH-004 | done   | wave 2               |
| SH-005 | done   | wave 2               |
| SH-006 | next   | wave 3               |
| SH-007 | next   | wave 3               |
| SH-008 | queued | wave 4               |
-----------------------------------------
```

### Scope Creep Guard
During EXECUTE, agents may discover additional work needed ("oh, this also needs X"). Handle scope creep strictly:

1. **Blocking discovery** (can't complete the current task without it): Add a new task to the DAG, assign it to the current or next wave, and flag the change to the user on the board. Continue with other tasks in the wave.
2. **Non-blocking discovery** (nice-to-have, related improvement, cleanup): Do NOT absorb it. Add it to a `## Deferred Work` section on the board. Mention it in the CONVERGE summary. The user decides whether to start a new Superhuman session for it.
3. **Never silently expand scope** - every addition to the DAG must be visible on the board and flagged in the next progress report.

### Handling Blocked Tasks
If a task cannot proceed:
1. Mark it as `blocked` on the board with a reason
2. Continue with non-blocked tasks in the same wave
3. After the wave completes, reassess blocked tasks
4. If the blocker is resolved, add the task to the next wave

### Handling Failures
If an agent fails to complete a task:
1. Capture the error/failure reason on the board
2. Attempt one retry with adjusted approach
3. If retry fails, mark as `failed` and flag for user attention with the rollback point hash
4. Continue with other tasks - don't let one failure block the wave

See `references/wave-execution.md` for detailed agent orchestration patterns.

---

## Phase 6: VERIFY (Per-Task + Integration)

Every sub-task must prove it works before closing.

### Per-Task Verification
For each completed sub-task, run:
1. **Tests**: Run the task's test suite - all tests must pass
2. **Lint**: Run the project's linter on modified files
3. **Type Check**: Run type checker if applicable (TypeScript, mypy, etc.)
4. **Build**: Verify the project still builds

### Integration Verification
After each wave completes:
1. Run tests for tasks that depend on this wave's output
2. Check for conflicts between parallel tasks (file conflicts, API mismatches)
3. Run the full test suite if available

### Verification Loop
```
if all checks pass:
  mark task as "done"
  update board with verification report
else:
  mark task as "failed"
  loop back to EXECUTE for this task (max 2 retries)
  if still failing after retries:
    flag for user attention
    continue with other tasks
```

### Output
Update each sub-task on the board with a verification report:
- Tests: pass/fail (with details on failures)
- Lint: clean/issues
- Type check: pass/fail
- Build: pass/fail

See `references/verification-framework.md` for the full verification protocol.

---

## Phase 7: CONVERGE (Final Integration)

Merge all work and close out the board.

### Steps
1. **Merge**: If using worktrees or branches, merge all work into the target branch
2. **Full Test Suite**: Run the complete project test suite
3. **Documentation**: Update any docs that were part of the task scope
4. **Summary**: Generate a change summary with:
   - Files created/modified (with line counts)
   - Tests added (with coverage if available)
   - Key decisions made during execution
   - Any deferred work or follow-ups
5. **Close Board**: Mark the board as `completed` with a timestamp
6. **Suggest Commit**: Propose a commit message summarizing the work

### Board Finalization
The completed board serves as an audit trail:
- Full history of all 7 phases
- Every sub-task with its research, plan, and verification
- Timeline of execution
- Any issues encountered and how they were resolved

---

## Gotchas

1. **Parallel agents modifying shared files without a lock strategy** - Two agents in the same wave that both edit the same utility file or test fixture will produce a merge conflict at the wave boundary. During DECOMPOSE, identify shared files and assign ownership to one task; other tasks must treat those files as read-only until the owning task completes.

2. **Board marked `completed` but tests were never run** - The mandatory tail task "Run full project verification suite" is frequently skipped when agents declare done based on subjective confidence. Never mark the board `completed` until the actual test/lint/build commands have been run and their output recorded on the board.

3. **DISCOVER phase skipped for "obvious" tasks** - Agents assume they know the codebase well enough to skip research. Then they write code that duplicates existing utilities, uses the wrong import paths, or misses a convention that would have been visible in a 2-minute code scan. Always run DISCOVER, even for small tasks.

4. **Rollback point recorded after Wave 1 has already started** - Recording the git commit hash mid-wave means the rollback point already includes partial changes. The pre-execution snapshot must be taken before any file is touched - before Wave 1 begins, not during it.

5. **Scope creep absorbed silently expands the DAG without user visibility** - Agents frequently discover adjacent improvements during EXECUTE and absorb them into the current task without flagging them. This makes the wave take longer than planned, obscures what changed, and violates the scope agreement from INTAKE. Everything outside the original scope goes to the Deferred Work section.

---

## Anti-Patterns and Common Mistakes

| Anti-Pattern | Better Approach |
|---|---|
| Skipping intake for "obvious" tasks | Even simple tasks benefit from 3 intake questions - assumptions kill projects |
| Flat task lists without dependencies | Always model as a DAG - hidden dependencies cause merge conflicts and ordering bugs |
| Executing without user approval of the graph | Always present the wave plan and get explicit approval before any execution |
| Skipping TDD for "simple" changes | Tests are verification proof, not optional extras - write them first, always |
| Massive sub-tasks (L+ complexity) | Decompose further until all tasks are S or M - large tasks hide complexity |
| Not persisting board state | Always write to `.superhuman/board.md` - it enables resume, audit, and handoff |
| Over-decomposing into 20+ micro-tasks | Aim for 5-15 tasks - too many creates overhead that defeats the purpose |
| Ignoring research phase | DISCOVER prevents rework - 10 minutes of research saves hours of wrong implementation |
| Sequential execution when parallelism is possible | Always check the DAG for parallel opportunities - that's the whole point of Superhuman |
| Silently absorbing scope creep during EXECUTE | Flag blocking additions on the board; defer non-blocking discoveries to the Deferred Work section |
| Starting fresh when a board already exists | Detect existing boards, display status, and resume from last incomplete wave |
| Assuming project conventions without checking | Always run Codebase Convention Detection before INTAKE - read `package.json`, config files, directory structure |
| No rollback plan before execution | Record the git commit hash before Wave 1 starts - offer rollback if things go sideways |
| Parallel agents modifying the same file without reconciliation | Run conflict resolution checks at every wave boundary before proceeding |
| Skipping self code review before verification | Verification catches build/test failures but not code quality issues - review catches bugs, security issues, and design problems that tests miss |
| Ignoring `docs/` when it exists | Reading raw source files when codedocs output is available wastes context window and misses curated architecture context - always check for `.codedocs.json` during Convention Detection and use docs-first in DISCOVER |

---

## References

For detailed guidance on specific phases, load these reference files:

- **`references/intake-playbook.md`** - Full question bank organized by task type (feature, bug, refactor, greenfield, migration), with scaling rules and example sessions
- **`references/dependency-graph-patterns.md`** - Common DAG patterns, ASCII rendering format, wave assignment algorithm, and example graphs
- **`references/wave-execution.md`** - Parallel agent orchestration, agent prompt templates, blocked task handling, error recovery
- **`references/verification-framework.md`** - TDD workflow per sub-task, verification signals, integration testing, failure handling
- **`references/board-format.md`** - Full `.superhuman/board.md` specification with format, status transitions, and example board

---

## Companion check

> On first activation of this skill in a conversation: check which companion skills are installed by running `ls ~/.claude/skills/ ~/.agent/skills/ ~/.agents/skills/ .claude/skills/ .agent/skills/ .agents/skills/ 2>/dev/null`. Compare the results against the `recommended_skills` field in this file's frontmatter. For any that are missing, mention them once and offer to install:
> ```
> npx skills add AbsolutelySkilled/AbsolutelySkilled --skill <name>
> ```
> Skip entirely if `recommended_skills` is empty or all companions are already installed.
