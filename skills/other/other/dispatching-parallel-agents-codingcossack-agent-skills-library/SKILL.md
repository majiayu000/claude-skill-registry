---
name: dispatching-parallel-agents
description: Dispatches one subagent per independent domain to parallelize investigation/fixes. Use when you have 2+ unrelated failures (e.g., separate failing test files, subsystems, bugs) with no shared state or ordering dependencies.
---

# Dispatching Parallel Agents

Dispatch one agent per independent problem. Let them work concurrently.

## Dispatch Workflow

Copy and track:

```
- [ ] 1. Identify independent domains
- [ ] 2. Create focused agent tasks
- [ ] 3. Dispatch in parallel
- [ ] 4. Review and integrate
```

### 1. Identify Independent Domains

Group failures by what's broken:

- File A tests: Tool approval flow
- File B tests: Batch completion
- File C tests: Abort functionality

Each domain is independent—fixing tool approval doesn't affect abort tests.

**Critical check:** If fixing one might fix others → investigate together first (don't parallelize).

### 2. Create Focused Agent Tasks

Each agent needs:

- **Scope:** One test file or subsystem
- **Goal:** Make these tests pass
- **Constraints:** Don't change unrelated code
- **Output:** Summary of findings and fixes

### 3. Dispatch in Parallel

Example (Claude Code):

```typescript
Task("Fix agent-tool-abort.test.ts failures")
Task("Fix batch-completion-behavior.test.ts failures")
Task("Fix tool-approval-race-conditions.test.ts failures")
```

### 4. Review and Integrate

1. Read each agent's summary
2. Check for conflicts (same files edited?)
   - If two agents touched the same file → stop and re-scope (one owner per file)
3. Run full test suite
4. If failures:
   - Check for merge conflicts → resolve manually
   - If no conflicts → investigate as new failures
5. Repeat until green

## Agent Prompt Template

```markdown
Fix the [N] failing tests in [file path]:

1. "[test name]" - [error summary]
2. "[test name]" - [error summary]

Context: [relevant background, e.g., "These are timing/race condition issues"]

Your task:
1. Read the test file, understand what each test verifies
2. Identify root cause—timing issues or actual bugs?
3. Fix by [preferred approach, e.g., "replacing arbitrary timeouts with event-based waiting"]

Do NOT: [anti-patterns, e.g., "just increase timeouts—find the real issue"]

Return: Summary of root cause and changes made.
```

## Common Mistakes

| ❌ Bad | ✅ Good |
|--------|---------|
| "Fix all the tests" | "Fix agent-tool-abort.test.ts" |
| "Fix the race condition" | Paste error messages + test names |
| No constraints | "Do NOT change production code" |
| "Fix it" | "Return summary of root cause and changes" |

## Example

**Scenario:** 6 test failures across 3 files after major refactoring.

**Failures:**

- agent-tool-abort.test.ts: 3 failures (timing issues)
- batch-completion-behavior.test.ts: 2 failures (tools not executing)
- tool-approval-race-conditions.test.ts: 1 failure (execution count = 0)

**Decision:** Independent domains—abort logic separate from batch completion separate from race conditions.

**Dispatch:**

```
Agent 1 → Fix agent-tool-abort.test.ts
Agent 2 → Fix batch-completion-behavior.test.ts
Agent 3 → Fix tool-approval-race-conditions.test.ts
```

**Results:**

- Agent 1: Replaced timeouts with event-based waiting
- Agent 2: Fixed event structure bug (threadId in wrong place)
- Agent 3: Added wait for async tool execution

**Integration:** All fixes independent, no conflicts, full suite green.
