---
name: ln-404-test-executor
description: Executes Story Finalizer test tasks (label "tests") from Todo -> To Review. Enforces risk-based limits and priority.
---

# Test Task Executor

Runs a single Story final test task (label "tests") through implementation/execution to To Review.

## Purpose & Scope
- Handle only tasks labeled "tests"; other tasks go to ln-401.
- Follow the 11-section test task plan (E2E/Integration/Unit, infra/docs/cleanup).
- Enforce risk-based constraints: Priority ≤15; E2E 2-5, Integration 0-8, Unit 0-15, total 10-28; no framework/DB/library/performance tests.
- Update Linear/kanban for this task only: Todo -> In Progress -> To Review.

## Task Storage Mode

| Aspect | Linear Mode | File Mode |
|--------|-------------|-----------|
| **Load task** | `get_issue(task_id)` | `Read("docs/tasks/epics/.../tasks/T{NNN}-*.md")` |
| **Load Story** | `get_issue(parent_id)` | `Read("docs/tasks/epics/.../story.md")` |
| **Update status** | `update_issue(id, state)` | `Edit` the `**Status:**` line in file |
| **Test results** | Linear comment | Append to task file |

**File Mode transitions:** Todo → In Progress → To Review

## Workflow (concise)
1) **Receive task:** Get task ID from orchestrator (ln-400); fetch full test task description (Linear: get_issue; File: Read task file); read linked guides/manuals/ADRs/research; review parent Story and manual test results if provided.
2) **Read runbook:** **Read `docs/project/runbook.md`** — understand test environment setup, Docker commands, test execution prerequisites. Use exact commands from runbook.
3) **Validate plan:** Check Priority ≤15 and test count limits; ensure focus on business flows (no infra-only tests).
4) **Start work:** Set task In Progress (Linear: update_issue; File: Edit status line); move in kanban.
5) **Implement & run:** Author/update tests per plan; reuse existing fixtures/helpers; run tests; fix failing existing tests; update infra/doc sections as required.
6) **Complete:** Ensure counts/priority still within limits; set task To Review; move in kanban; add comment summarizing coverage, commands run, and any deviations.

## Critical Rules
- Single-task only; no bulk updates.
- Do not mark Done; ln-402 approves. Task must end in To Review.
- Keep language (EN/RU) consistent with task.
- No framework/library/DB/performance/load tests; focus on business logic correctness (not infrastructure throughput).
- Respect limits and priority; if violated, stop and return with findings.
- **Do NOT commit.** Leave all changes uncommitted — ln-402 reviews and commits with task ID reference.

## Definition of Done
- Task identified as test task and set to In Progress; kanban updated.
- Plan validated (priority/limits) and guides read.
- Tests implemented/updated and executed; existing failures fixed.
- Docs/infra updates applied per task plan.
- Task set to To Review; kanban moved; summary comment added with commands and coverage.

## Test Failure Analysis Protocol

**CRITICAL:** When a **newly written test** fails, STOP and analyze BEFORE changing anything.

**Step 1: Verify Test Correctness**
- Does test match AC requirements exactly? (Given/When/Then from Story)
- Is expected value correct per business logic?
- If uncertain: Query `ref_search_documentation(query="[domain] expected behavior")`

**Step 2: Decision**
| Test matches AC? | Action |
|------------------|--------|
| YES | **BUG IN CODE** → Fix implementation, not test |
| NO | Test is wrong → Fix test assertion |
| UNCERTAIN | **MANDATORY:** Query MCP Ref + ask user before changing |

**Step 3: Document in Linear comment**
"Test [name] failed. Analysis: [test correct / test wrong]. Action: [fixed code / fixed test]. Reason: [justification]"

**RED FLAGS (require user confirmation):**
- ⚠️ Changing assertion to match actual output ("make test green")
- ⚠️ Removing test case that "doesn't work"
- ⚠️ Weakening expectations (e.g., `toContain` instead of `toEqual`)

**GREEN LIGHTS (safe to proceed):**
- ✅ Fixing typo in test setup/mock data
- ✅ Fixing code to match AC requirements
- ✅ Adding missing test setup step

## Test Writing Principles

### 1. Strict Assertions - Fail on Any Mismatch

**Use exact match assertions by default:**

| Strict (PREFER) | Loose (AVOID unless justified) |
|-----------------|--------------------------------|
| Exact equality check | Partial/substring match |
| Exact length check | "Has any length" check |
| Full object comparison | Partial object match |
| Exact type check | Truthy/falsy check |

**WARN-level assertions FORBIDDEN** - test either PASS or FAIL, no warnings.

### 2. Expected-Based Testing for Deterministic Output

**For deterministic responses (API, transformations):**
- Use **snapshot/golden file testing** for complex deterministic output
- Compare actual output vs expected reference file
- Normalize dynamic data before comparison (timestamps → fixed, UUIDs → placeholder)

### 3. Golden Rule

> "If you know the expected value, assert the exact value."

**Forbidden:** Using loose assertions to "make test pass" when exact value is known.

## Reference Files
- Kanban format: `docs/tasks/kanban_board.md`

---
**Version:** 3.2.0 (Added Test Writing Principles: strict assertions, expected-based testing, golden rule)
**Last Updated:** 2026-01-15
