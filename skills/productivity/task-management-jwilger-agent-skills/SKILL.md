---
name: task-management
description: >-
  Work decomposition, dependency ordering, and status tracking for software
  tasks. Activate when breaking down features into tasks, managing work items,
  tracking dependencies, creating stories or epics, or asking what to work on
  next. Works with any task tool: harness-native todos, dot CLI, GitHub Issues,
  or file-based tracking.
license: CC0-1.0
compatibility: Designed for any coding agent (Claude Code, Codex, Cursor, OpenCode, etc.)
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: [task-state]
  phase: build
  standalone: true
---

# Task Management

**Value:** Communication and feedback. Breaking work into explicit, trackable
units makes intent visible, progress measurable, and handoffs clean. Small tasks
create short feedback loops that catch problems early.

## Purpose

Teaches how to decompose work into well-structured tasks with clear acceptance
criteria, manage dependencies between tasks, and track status through a
consistent lifecycle. The outcome is a work breakdown where every task is
unambiguous, appropriately scoped, and sequenced so nothing is blocked
unnecessarily.

## Practices

### Decompose Top-Down, Execute Bottom-Up

Break large goals into progressively smaller tasks until each task represents
a single deliverable outcome. Execute from the leaves up.

1. Start with the goal (epic or feature)
2. Identify 3-7 child tasks that together achieve the goal
3. For each child, ask: can one agent complete this in one session? If no, decompose further
4. Leaf tasks should take minutes to hours, not days

**Example:**
```
Epic: User Authentication
  Story: Registration flow
    Task: Create registration command handler
    Task: Build registration form component
    Task: Add email verification automation
  Story: Login flow
    Task: Create login command handler
    Task: Build login form component
```

**Do:**
- Name tasks with a verb and an outcome ("Create registration handler")
- Keep leaf tasks small enough for one focused session
- Include acceptance criteria on every leaf task

**Do not:**
- Create tasks so large that progress is invisible for hours
- Decompose so finely that task overhead exceeds task work
- Leave tasks as vague nouns ("Authentication" tells no one what to do)

### Write Acceptance Criteria as Verifiable Statements

Every leaf task needs criteria that are binary: met or not met. Use Given/When/Then
for behavior, checklists for deliverables.

1. State what must be true when the task is done
2. Each criterion is independently testable
3. Include edge cases that matter

**Example:**
```markdown
Task: Create registration command handler

Acceptance Criteria:
- [ ] Given valid registration data, when command is processed,
      then UserRegistered event is stored
- [ ] Given a duplicate email, when command is processed,
      then command is rejected with a clear error
- [ ] Given a password under 12 characters, when command is processed,
      then validation fails before reaching the handler
```

**Do not:**
- Write criteria that require subjective judgment ("works well")
- Omit error cases -- they are where bugs live
- Copy-paste generic criteria across unrelated tasks

### Declare Dependencies Explicitly

When task B cannot start until task A completes, declare the dependency.
Use the dependency graph to find unblocked work.

1. Before creating a task, ask: does this depend on another task's output?
2. Record the dependency in whatever tool you are using
3. Always query for unblocked/ready tasks rather than scanning the full list

**Dependency patterns:**
- **Sequential:** Schema -> Repository -> Service -> API endpoint
- **Fan-out:** One design task unblocks multiple implementation tasks
- **Fan-in:** Multiple tasks must complete before integration testing

**Do:**
- Keep dependency chains as short as possible -- long chains serialize work
- Prefer parallel-safe decomposition (tasks that can run simultaneously)

**Do not:**
- Create circular dependencies
- Assume an implicit ordering -- make every dependency explicit
- Block tasks unnecessarily (does B really need A, or just A's interface?)

### Track Status Through a Consistent Lifecycle

Tasks move through a fixed set of states. Transitions are explicit.

**Lifecycle:** Open -> Active -> Closed

1. **Open:** Task is defined and waiting. May be blocked by dependencies.
2. **Active:** Work is in progress. Only one task should be active per agent
   at a time to maintain focus.
3. **Closed:** Work is done and acceptance criteria are met. Always record why.

**Rules:**
- Activate a task before starting work on it
- Close a task only when all acceptance criteria are met
- Provide a close reason for audit trail
- If a task is abandoned, close it with the reason ("Superseded by X" or "No longer needed")

### Adapt to Available Tools

This skill works with whatever task tracking is available. Detect and use the
best option:

1. **Harness-native task tools** (Claude Code TodoWrite, Codex tasks): Use them
   directly. They integrate with the agent's workflow.
2. **dot CLI** (.dots/ directory): File-based, version-controlled. Use `dot ready`
   to find unblocked work. Close tasks on the feature branch before creating PRs.
3. **GitHub Issues**: Use for cross-team visibility. Link PRs to issues.
4. **File-based fallback**: Create a `TASKS.md` in the repo root. Use markdown
   checklists. Commit with changes.

The methodology (decompose, specify criteria, track dependencies, manage lifecycle)
is the same regardless of tool. The tool is interchangeable; the discipline is not.

## Enforcement Note

This skill provides advisory guidance on task decomposition and tracking. It
cannot mechanically prevent an agent from skipping task creation or working on
blocked items. On harnesses with plugin support, enforcement plugins can require
task activation before code changes and block work on tasks with unresolved
dependencies. On harnesses without enforcement, the agent follows these practices
by convention. For available enforcement plugins, see the
[Harness Plugin Availability](../../README.md#harness-plugin-availability) table.

## Verification

After completing work guided by this skill, verify:

- [ ] Every unit of work has a corresponding task with acceptance criteria
- [ ] No task was worked on while its dependencies were still open
- [ ] Active tasks were limited to one at a time per agent
- [ ] Closed tasks have a recorded reason
- [ ] The task hierarchy is navigable (parent-child relationships are clear)
- [ ] Remaining open tasks accurately reflect outstanding work

If any criterion is not met, revisit the relevant practice before proceeding.

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **tdd-cycle:** Each task maps to one or more TDD cycles. Task acceptance criteria
  become the tests you write in the red phase.
- **orchestration:** Task dependencies inform how work is delegated across agents.
- **architecture-decisions:** Major structural tasks should reference relevant ADRs.

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill tdd-cycle
```
