---
name: task-authoring
description: Task Authoring skill for the ikigai project
---

# Task Authoring

Guidance for creating task files from requirements (user stories, bugs, gaps).

## Critical Context

**Task execution is UNATTENDED. No human in the loop.**

When `/orchestrate` runs, it executes all tasks automatically. If a sub-agent needs context you didn't provide, it will:
- Fail and escalate (wasting attempts)
- Succeed partially (creating technical debt)
- Spawn research agents (ballooning token usage)

**There is no one to ask for help. The task file IS the help.**

## Efficiency Principle

**Spend generously during task authoring to save massively during execution.**

Task authoring happens ONCE. Task execution happens N times (once per task in the orchestration loop). Therefore:

- **During authoring:** Use research agents, explore codebase, read extensively, think deeply
- **During execution:** Sub-agent has everything, executes immediately, no exploration needed

**Token math:**
- Poor task authoring: 10K tokens → Each of 20 tasks researches → 200K+ execution tokens
- Good task authoring: 50K tokens → 20 tasks execute directly → 40K execution tokens

**Completeness requirement:**
- Poor task: "Implement feature X" → Sub-agent fails or researches (unattended failure)
- Good task: Lists skills, files, interface specs, patterns, edge cases → Sub-agent executes to completion

## Prerequisites

- `/load cdd` - For release directory structure and abstraction levels (plan vs tasks)
- `/load task` - For order.json format and task state machine

## Process

1. **Review source material** - Read and understand the requirements thoroughly
2. **Think deeply** - Consider edge cases, dependencies, and implementation approaches
3. **Break down** - Split into smallest achievable, testable units
4. **Create order.json** - Define execution order and metadata (see task skill for format)

## File Naming

**DO NOT use numeric prefixes.** Order is defined in `order.json`, not filenames.

| Good | Bad |
|------|-----|
| `provider-types.md` | `01-provider-types.md` |
| `openai-adapter.md` | `02-openai-adapter.md` |
| `tests-integration.md` | `20-tests-integration.md` |

Use descriptive kebab-case names that reflect the task's purpose.

## order.json

See `/load task` for the canonical order.json format.

**Key points for authoring:**
- Tasks execute serially in array order (position 0 first)
- Place dependencies before dependents in the array
- The `Depends on:` field in task files is documentation only - array position is what matters

## Task File Requirements

### Model/Thinking Selection

Choose minimum capability needed for each task:

| Complexity | Model | Thinking |
|------------|-------|----------|
| Straightforward | sonnet | none |
| Moderate | sonnet | thinking |
| Complex | sonnet | extended |
| Very complex | opus | extended |

Default to `sonnet/none` and escalate only when complexity demands it.

### Working Directory Context

**CRITICAL:** Every task file MUST include a Context section stating:
- Working directory is project root (where `Makefile` lives)
- All paths are relative to project root, not to the task file

This prevents sub-agents from misinterpreting paths like `cdd/plan/` as relative to `cdd/tasks/`.

### Skill Loading

**Task execution automatically loads the `implementor` skillset as baseline:**
- `jj` - Version control workflow
- `errors` - Result types and error handling
- `style` - Code style conventions
- `tdd` - Test-driven development workflow

**List ONLY additional skills needed beyond the baseline:**
- Specify skills needed for THIS task only
- Don't load large reference skills (database, source-code) unless task directly requires them
- Don't assume sub-agent will research or explore - give them what they need upfront
- **Never load `align`** - sub-agents execute, they don't negotiate

**Goal:** Sub-agent executes immediately with provided context. No exploration, no research sub-agents.

### Source Code Links

**Provide ALL file paths the sub-agent needs - be complete.**

- List specific implementation files to read/modify
- List specific test files to follow as patterns
- List related existing code as examples
- Be exhaustive - sub-agent should NOT need to search or explore

### Library Constraints

**Specify which libraries the sub-agent should use.**

- List allowed libraries for this task (from plan)
- Explicitly state "do not introduce new dependencies"
- Reference existing usage patterns in the codebase

Sub-agents will reach for familiar libraries (lodash, axios, etc.) unless constrained. Be explicit.

### Pre/Post Conditions

- Pre-conditions must be verifiable before starting
- Post-conditions must be testable after completion
- Chain logically: post(N) = pre(N+1)

**MANDATORY POSTCONDITIONS FOR ALL TASKS:**

These postconditions are NON-NEGOTIABLE. Every task MUST achieve ALL of them:

- [ ] `make all` succeeds - production code compiles without errors
- [ ] `make build-tests` succeeds - all test code compiles without errors
- [ ] `make check` succeeds - all tests pass
- [ ] `make lint` succeeds - complexity and file size checks pass

**If a task cannot achieve these, it MUST report as `failed` (not `partial`, not `success`).**

There are NO exceptions. Tasks that leave broken code should trigger escalation, not be marked as done.

### Context (What/How/Why)

**Every task must provide complete context so sub-agent can execute immediately.**

- **What** - The specific goal with full details
- **How** - Exact approach, patterns, and implementation guidance
- **Why** - Business/technical rationale for decision-making

**Goal:** Sub-agent has everything needed to execute. No need to research background, explore alternatives, or understand broader context.

### Execution Expectations

**UNATTENDED EXECUTION: Provide everything needed for autonomous completion.**

Tasks execute without human oversight. The sub-agent cannot ask questions or request clarification. Everything it needs must be in the task file.

Checklist for complete task authoring:
- [ ] Additional skills beyond baseline (jj, errors, style, tdd) listed explicitly
- [ ] All file paths to read/modify listed
- [ ] All test patterns and examples referenced
- [ ] Allowed libraries specified, new dependencies forbidden
- [ ] Edge cases and error conditions documented
- [ ] Success criteria clearly defined
- [ ] Rollback/failure handling specified
- [ ] TDD workflow (Red/Green/Verify) included in Test Implementation section

If unsure whether to include something: **INCLUDE IT**. Over-specification is safe. Under-specification causes unattended failures.

Task instructions should emphasize:
- Persistence to complete the goal despite obstacles
- Task success is the measure, not partial progress
- All needed context is provided in this task file

**Why this matters:** Complete task authoring prevents unattended failures and prevents sub-agents from spawning research/explore agents, which would balloon token usage across the orchestration loop.

### Test-Driven Development

**All tasks follow TDD workflow (Red/Green/Verify):**

1. **Red** - Write failing test first (with stub implementation that compiles)
2. **Green** - Implement minimal code to pass
3. **Verify** - Run `make check`

The task template enforces this sequence with explicit workflow steps in the "Test Implementation" section.

## jj Workflow Requirements

Every task MUST follow this jj workflow:

### Pre-condition: Clean Workspace

Before starting, verify working copy has no changes:
```bash
jj diff --summary
```

If output is non-empty, STOP and fail the task. Previous task did not complete properly.

### Post-condition: Committed Changes

After completing work (success, partial, or failed), commit ALL changes using the commit message template below.

The workspace MUST be clean when the task ends, regardless of outcome.

### Commit Message Template

First line format: `task(<exact-filename.md>): <status> - <brief description>`

**CRITICAL:** Use the exact task filename including `.md` extension.

```
task(<task-filename.md>): <success|partial|failed> - <brief description>

<Optional: Details about what was accomplished, failures, or remaining work>
```

**Status values:**

- **success** - All objectives met, all tests passing, `make check` clean
- **partial** - Some objectives met, some tests passing, but incomplete
- **failed** - Unable to complete objectives, tests may be failing, errors encountered

**Examples:**

```
task(provider-types.md): success - implemented provider type definitions

All provider factory functions complete, tests passing, make check clean.
```

```
task(openai-adapter.md): partial - adapter struct and lifecycle functions

Create/destroy working, integration tests still failing on API response parsing.
```

```
task(tests-integration.md): failed - mock server configuration errors

Attempted integration test setup but unable to resolve server config issues.
Committing partial work for debugging and escalation.
```

**Rollback operations:**

Find all commits for a task (search commit descriptions):
```bash
jj log --no-graph -T 'description' | grep "task(provider-types.md)"
```

Backout a specific commit:
```bash
jj backout -r <revision>
```

See recent commits:
```bash
jj log --limit 20
```

### Reporting Task Status

The jj commit records what happened. The task must ALSO report its status to the orchestration system:
- Use `/task-done <name>` for success
- Use `/task-fail <name>` for partial or failed (allows retry/escalation)

## Task Template

```markdown
# Task: [Descriptive Name]

**UNATTENDED EXECUTION:** This task executes automatically without human oversight. Provide complete context.

**Model:** sonnet/thinking
**Depends on:** task-name.md (or "None")

## Context

**Working directory:** Project root (where `Makefile` lives)
**All paths are relative to project root**, not to this task file.

All needed context is provided in this file. Do not research, explore, or spawn sub-agents.

## Pre-Read

**Skills:**
(Baseline skills jj, errors, style, tdd are pre-loaded. Only list additional skills.)
- `/load skill-name` - Why needed

**Source:**
- `path/to/file.h` - What to learn from it

**Plan:**
- `cdd/plan/relevant.md` - Sections to reference

## Libraries

Use only:
- `library-name` - For what purpose

Do not introduce new dependencies.

## Preconditions

- [ ] Working copy is clean (verify with `jj diff --summary`)

## Objective

One paragraph: what this task accomplishes and why.

## Interface

Functions to implement (signatures and contracts, not code):

| Function | Purpose |
|----------|---------|
| `res_t foo_create(...)` | Creates X, returns OK/ERR |
| `void foo_destroy(...)` | Cleanup, NULL-safe |

Structs to define (members and purpose, not C code):

| Struct | Members | Purpose |
|--------|---------|---------|
| `foo_t` | name, count, items | Represents X |

## Behaviors

- When X happens, do Y
- Error handling: return ERR with category Z
- Memory: talloc ownership rules

## Test Implementation

**Follow TDD workflow (Red/Green/Verify):**

**Step 1 - Red (Failing Test):**
- Write test code in tests/unit/[module]/[module]_test.c
- Add function declarations to header files
- Add stub implementations that compile but return minimal values (e.g., `return OK(NULL);`)
- Build and run: `make check`
- Verify test FAILS with assertion failure (NOT compilation error)

**Step 2 - Green (Minimal Implementation):**
- Implement ONLY what the current tests require
- STOP when all tests pass
- Do NOT write code "because you'll need it later"

**Step 3 - Verify:**
- Run `make check` - all tests must pass
- Run `make lint` - complexity under threshold

**Required test scenarios:**
- Create/destroy lifecycle
- Error case: invalid input returns ERR_INVALID_ARG
- Edge case: empty/null input handled correctly
- [Add task-specific scenarios here]

## Completion

After completing work (whether success, partial, or failed), commit all changes:

```bash
jj commit -m "$(cat <<'EOF'
task([exact-filename.md]): [success|partial|failed] - [brief description]

[Optional: Details about what was accomplished, failures, or remaining work]
EOF
)"
```

**Example:**
```bash
jj commit -m "$(cat <<'EOF'
task(provider-types.md): success - implemented provider type definitions

All provider factory functions complete, tests passing, make check clean.
EOF
)"
```

Report status to orchestration:
- Success: `/task-done [task-name]`
- Partial/Failed: `/task-fail [task-name]`

## Postconditions

- [ ] Compiles without warnings
- [ ] All tests pass
- [ ] `make check` passes
- [ ] All changes committed using commit message template
- [ ] Working copy is clean (no uncommitted changes)
```
