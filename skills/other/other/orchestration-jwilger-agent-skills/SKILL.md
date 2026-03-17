---
name: orchestration
description: >-
  Multi-agent orchestration patterns: delegation, context passing, workflow
  gates, and role-based coordination. Activate when coordinating multiple
  specialized roles, delegating file edits, or managing TDD cycle handoffs.
  The orchestrator never writes files directly.
license: CC0-1.0
compatibility: >-
  Works on any harness. Adapts to the delegation topology available:
  hub-and-spoke (flat), shallow hierarchy, or sequential role-switching.
  Hub-and-spoke is the default assumption.
metadata:
  author: jwilger
  version: "1.0"
  requires: [tdd-cycle]
  context: [test-files, domain-types, source-files, task-state]
  phase: build
  standalone: false
---

# Orchestration

**Value:** Communication and respect -- the orchestrator ensures every
specialized role receives complete context and every concern is heard before
work proceeds.

## Purpose

Teaches the main conversation to coordinate work through specialized roles
without performing specialized work itself. Solves the problem of an LLM
trying to do everything at once, which leads to skipped reviews, inconsistent
quality, and tangled responsibilities.

## Practices

### Never Write Files Directly

The orchestrator decides WHAT to do and WHO should do it. It never uses
Write or Edit tools on project files. All file modifications flow through
specialized roles.

**Role selection:**

| File type | Role | Scope |
|-----------|------|-------|
| Test files | Test Writer | `*_test.*`, `*.test.*`, `tests/`, `spec/` |
| Production code | Implementer | `src/`, `lib/`, `app/` |
| Type definitions | Domain Modeler | Structs, enums, interfaces, traits |
| Architecture docs | Architect | `ARCHITECTURE.md`, ADRs |
| Config, docs, scripts | File Updater | Everything not specialized |

How roles map to agents depends on the harness delegation topology:

- **Hub-and-spoke (flat):** The orchestrator spawns leaf-node specialists
  directly. Specialists cannot sub-delegate. All coordination flows through
  the orchestrator. Common on Claude Code, Amp, and OpenAI Agents SDK.
- **Shallow hierarchy:** The orchestrator delegates to specialists who may
  invoke one level of sub-specialists. Cap depth at 2-3 levels; deeper
  nesting duplicates work and degrades context quality. Common on OpenCode,
  Goose, and CrewAI.
- **Sequential role-switching:** The orchestrator plays each role itself:
  "I am now acting as the Test Writer role" -- then shifts back when done.
  Use on single-agent harnesses or when the orchestrator cannot spawn.

When in doubt, prefer hub-and-spoke. Flat delegation gives the orchestrator
unmediated feedback from every role and keeps coordination simple. Roles are
leaf workers -- if a role needs sub-work done, it reports back to the
orchestrator, which decides whether to decompose further.

**Do not:**
- Make "quick fixes" directly ("just one line")
- Edit files while "in orchestrator mode"
- Skip delegation because "it is trivial"

### Provide Complete Context Every Time

Roles have zero memory of the main conversation. Every delegation must
include all information needed to complete the task.

**Required context template:**
```
TASK: What to accomplish
FILES: Specific file paths to read or modify
CURRENT STATE: What exists, what is passing/failing
REQUIREMENTS: What "done" looks like
CONSTRAINTS: Domain types to use, patterns to follow
ERROR: Exact error message (if applicable)
```

**Do not:**
- Say "as discussed earlier" or "continue from where we left off"
- Summarize errors instead of providing exact text
- Assume a role knows project conventions without stating them

### Enforce Workflow Gates

Work proceeds through gates. A gate is a precondition that must be satisfied
before the next step begins. Gates prevent skipping steps.

**TDD cycle gates:**
1. Red complete (test written and failing) -> Domain review of test
2. Domain review passed -> Green (implement)
3. Green complete (test passing) -> Domain review of implementation
4. Domain review passed -> Next test or ship

If a role raises a concern (e.g., domain modeler vetoes a test for primitive
obsession), the gate does not open until the concern is resolved. The
orchestrator facilitates resolution:

1. Concern raised -- affected role responds with rationale
2. Orchestrator summarizes both positions
3. Seek compromise (max 2 rounds)
4. No consensus after 2 rounds -- escalate to user

**The domain modeler has veto power** over primitive obsession, invalid state
representability, and parse-don't-validate violations. This veto can only be
overridden by the user, not by the orchestrator.

### Use Task Dependencies When Available

On harnesses with task/todo tools, encode workflow gates as task dependencies.
Create tasks for each step and block downstream tasks on upstream completion.

```
Task 1: Write failing test [RED]
Task 2: Review test, create types [DOMAIN] -- blocked by Task 1
Task 3: Implement to pass test [GREEN] -- blocked by Task 2
Task 4: Review implementation [DOMAIN] -- blocked by Task 3
```

On harnesses without task tools, track state explicitly in conversation:
"RED complete. Test fails with: [error]. Proceeding to DOMAIN review."

### Proxy Role Questions to User

Roles running as subagents cannot ask the user questions directly. When a
role's output contains questions or indicates it is blocked on a decision:

1. Detect the blocking question
2. Present it to the user with the role's context
3. Deliver the user's answer back to the role with full context

### Resume Agents Instead of Re-Delegating

On harnesses that support agent resume (e.g., Claude Code), prefer resuming
a stopped agent over starting a new one. When an agent stops because it
needs user input or is blocked on a decision:

1. Capture the agent's question and blocking context
2. Present the question to the user (using user-input-protocol if available)
3. Resume the agent with the user's answer

The resumed agent retains its prior conversation and working state. Do NOT
re-send the full context template -- the agent already has it. Only provide
the new information (the user's answer, clarification, or unblocking data).

This is more efficient than fire-and-forget delegation because the agent
keeps accumulated context -- file contents it read, intermediate reasoning,
partial progress. Re-delegating would discard all of that and start cold.

**When to resume vs. re-delegate:**
- **Resume** when the agent has accumulated significant context and just
  needs one piece of information to continue.
- **Re-delegate** when the agent's task has fundamentally changed, when
  the agent finished its task and a new one is starting, or when the
  harness does not support resume.

**Note:** The "Provide Complete Context Every Time" practice applies to
NEW delegations only. Resumed agents already have their context.

### Respect Delegation Depth

Do not nest delegation deeper than the harness supports. Even on harnesses
that allow deep nesting, prefer shallow topologies:

- **3-4 active agents** is the empirical sweet spot per workflow cycle
- Deeper trees add coordination cost with diminishing quality returns
- Subagents duplicating parent work is a sign of excessive depth
- Context gets summarized (lossy) at each delegation boundary

If a role needs help, it reports back to the orchestrator rather than
spawning its own specialists. The orchestrator decides whether to decompose
further. This keeps feedback loops short and coordination centralized.

## Enforcement Note

This skill provides advisory guidance. It cannot mechanically prevent the
orchestrator from writing files directly or skipping gates. On harnesses with
plugin support (Claude Code hooks, OpenCode event hooks), enforcement plugins
add mechanical guardrails -- PreToolUse hooks block unauthorized file edits,
SubagentStop hooks require domain review after red and green phases. On
harnesses without enforcement, follow these practices by convention. If you
observe violations, point them out. For available enforcement plugins, see
the [Harness Plugin Availability](../../README.md#harness-plugin-availability) table.

## Verification

After completing a workflow cycle guided by this skill, verify:

- [ ] Orchestrator did not use Write or Edit tools on project files
- [ ] Every role delegation included complete context (task, files, state, requirements)
- [ ] Domain review occurred after both red and green phases
- [ ] No workflow gates were skipped
- [ ] Role concerns were addressed before proceeding (not ignored)
- [ ] User was consulted for any unresolved disagreements
- [ ] Agents needing user input were resumed (not re-delegated) when the harness supports it
- [ ] Delegation depth matched harness topology (no nesting beyond what is supported)

## Dependencies

This skill requires `tdd-cycle` for the red/domain/green/domain workflow it
orchestrates. For enhanced workflows, it integrates with:

- **domain-modeling:** Domain modeler role applies these principles during review
- **code-review:** Three-stage review before shipping
- **task-management:** Encodes workflow gates as task dependencies
- **user-input-protocol:** Structured format for proxying role questions

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill domain-modeling
```
