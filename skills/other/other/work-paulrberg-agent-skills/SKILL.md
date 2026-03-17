---
argument-hint: <task>
disable-model-invocation: false
name: work
user-invocable: true
description: This skill should be run only when the user explicitly invokes it. Orchestrates end-to-end task implementation — understands the task, assesses complexity, implements directly or via a team of subagents for complex work, and always finishes with a code-polish pass.
---

# Work

Orchestrate end-to-end task implementation: understand the task, assess complexity, implement directly or distribute across a team, then polish the result.

## Workflow

### 1) Parse Task

Read the task description from `$ARGUMENTS`.

- If `$ARGUMENTS` is empty, ask the user for a task description and stop.
- Extract key signals: scope (files, modules, components mentioned), action type (new feature, bug fix, refactor, migration), and any constraints.
- Note any referenced issues, PRs, or URLs for later context gathering.

### 2) Assess Complexity

Classify the task as **simple** or **complex** using these heuristics:

| Signal           | Simple                   | Complex                                       |
| ---------------- | ------------------------ | --------------------------------------------- |
| File count       | 1-3 files                | 4+ files                                      |
| Module span      | Single module or package | Cross-module or cross-package                 |
| Dependency chain | No new dependencies      | New packages or service integrations          |
| Risk surface     | Low (UI, docs, config)   | High (auth, payments, data, infra)            |
| Parallelism      | Sequential steps only    | Independent subtasks benefit from concurrency |

A task is complex when **3 or more** signals fall in the complex column. When in doubt, prefer the simple path — team overhead is only justified when parallelism provides a real speedup.

- **Simple** — proceed to Step 3.
- **Complex** — proceed to Step 4.

### 3) Implement (Simple Path)

Execute the task directly without spawning subagents.

1. **Gather context**: Read all relevant files. Understand existing code, tests, and conventions.
2. **Implement**: Make the changes. Follow project conventions inferred from existing code, linters, and formatters.
3. **Verify**: Run the narrowest useful checks:
   - Formatter/linter on touched files.
   - Targeted tests for touched modules.
   - Type check when relevant.
   - If fast checks pass, run broader checks only when risk warrants it.
4. Proceed to Step 5 (Polish).

### 4) Implement (Complex Path)

Distribute work across a team of subagents.

#### 4a) Decompose

Break the task into independent subtasks. Each subtask should:

- Target a distinct set of files with minimal overlap.
- Be completable without waiting on other subtasks (no circular dependencies).
- Include clear acceptance criteria.

Avoid over-decomposition. If subtasks cannot run in parallel, prefer the simple path.

#### 4b) Create Team and Assign

Create a team with a name derived from the task (e.g., "add-auth", "refactor-api"). Create a task for each subtask. Set up dependencies when ordering matters.

Spawn implementation agents as teammates. Assign each agent one or more tasks.

Recommended team sizing:

- 1 agent per module when modules are independent.
- Separate agent for shared utilities when consumers depend on them (utility blocks consumers).
- Dedicated agent for tests if test volume is high.

#### 4c) Coordinate

Monitor progress. As agents complete tasks:

- Review output for integration issues.
- Resolve cross-agent conflicts (merge overlaps, API mismatches).
- Assign follow-up tasks if gaps emerge.

After all tasks complete:

- Run integration verification: full test suite, type check, lint.
- Fix any integration issues directly — do not re-spawn agents for small fixes.
- Shut down teammates.
- Proceed to Step 5 (Polish).

### 5) Polish

Invoke `/code-polish` to simplify and review all session-modified files.

Wait for completion. If it reports residual risks or stop conditions, relay them to the user.

This step is mandatory — always run it, even if the implementation seems clean.

## Error Handling

| Error                                | Response                                                      |
| ------------------------------------ | ------------------------------------------------------------- |
| Empty `$ARGUMENTS`                   | Ask for a task description and stop                           |
| Verification failures after impl     | Attempt to fix; if unfixable, report to user before polishing |
| Team agent fails or times out        | Reclaim the task and complete it directly                     |
| `code-polish` reports stop condition | Relay to user with context                                    |

## Stop Conditions

Stop and ask for direction when:

- The task description is ambiguous and multiple interpretations exist.
- Implementation requires changing public APIs or breaking contracts not mentioned in the task.
- The task scope grows beyond the original description during implementation.
- External dependencies (APIs, services, packages) are unavailable or broken.
- A CRITICAL security concern is discovered in existing code adjacent to the task.
