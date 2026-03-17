---
name: subagent-driven-development
model: standard
description: Execute implementation plans by dispatching a fresh subagent per task with two-stage review (spec compliance then code quality). Use when you have an implementation plan with mostly independent tasks and want high-quality, fast iteration within a single session.
version: 1.0.0
---

# Subagent-Driven Development

Execute a plan by dispatching a fresh subagent per task, with two-stage review after each — spec compliance first, then code quality.

**Core principle:** Fresh subagent per task + two-stage review = no context pollution, high quality, fast iteration.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install subagent-driven-development
```


## When to Use This Skill

- You have an implementation plan with discrete, mostly independent tasks
- You want to execute the plan within a single session (no human-in-the-loop between tasks)
- Tasks can be implemented and reviewed sequentially without tight coupling

| Condition                     | This Skill     | Alternative                         |
| ----------------------------- | -------------- | ----------------------------------- |
| Have a plan, same session     | **Yes**        | —                                   |
| Have a plan, parallel session | No             | executing-plans                     |
| No plan yet                   | No             | Write a plan first                  |
| Tasks tightly coupled         | No             | Manual execution or decompose more  |

## The Process

```
┌─────────────────────────────────────────────────────┐
│  1. Read plan, extract ALL tasks with full text      │
│  2. Note shared context (arch, deps, conventions)    │
│  3. Create TodoWrite with all tasks                  │
└──────────────────────┬──────────────────────────────┘
                       ▼
          ┌────── Per Task ──────┐
          │                      │
          │  Dispatch Implementer (references/implementer-prompt.md)
          │       │                                │
          │       ▼                                │
          │  Questions?──yes──► Answer, re-dispatch│
          │       │no                              │
          │       ▼                                │
          │  Implement + test + commit + self-review│
          │       │                                │
          │       ▼                                │
          │  Dispatch Spec Reviewer (references/spec-reviewer-prompt.md)
          │       │                                │
          │       ▼                                │
          │  Compliant?──no──► Implementer fixes──┘
          │       │yes             then re-review
          │       ▼
          │  Dispatch Code Reviewer (references/code-quality-reviewer-prompt.md)
          │       │
          │       ▼
          │  Approved?──no──► Implementer fixes, re-review
          │       │yes
          │       ▼
          │  Mark task complete
          └───────┬──────────────┘
                  ▼
          More tasks? ──yes──► next task
                  │no
                  ▼
          Final cross-task code review
                  ▼
          Finish development branch
```

## Prompt Templates

Three reference prompts are provided for the subagent roles:

| Role               | File                                        | Purpose                                |
| ------------------ | ------------------------------------------- | -------------------------------------- |
| **Implementer**    | `references/implementer-prompt.md`          | Implement, test, commit, self-review   |
| **Spec reviewer**  | `references/spec-reviewer-prompt.md`        | Verify code matches spec exactly       |
| **Code reviewer**  | `references/code-quality-reviewer-prompt.md`| Verify code is clean and maintainable  |

## Example Workflow

```
Controller: Reading plan — 5 tasks extracted, TodoWrite created.

─── Task 1: Hook installation script ───

[Dispatch implementer with full task text + context]

Implementer: "Should the hook be installed at user or system level?"
Controller:  "User level (~/.config/hooks/)"

Implementer: ✅ Implemented install-hook command
  - Added tests (5/5 passing)
  - Self-review: missed --force flag, added it
  - Committed

[Dispatch spec reviewer]
Spec reviewer: ✅ Spec compliant — all requirements met

[Dispatch code reviewer with git SHAs]
Code reviewer: ✅ Approved — clean, good coverage

[Mark Task 1 complete]

─── Task 2: Recovery modes ───

[Dispatch implementer]

Implementer: ✅ Added verify/repair modes (8/8 tests passing)

[Dispatch spec reviewer]
Spec reviewer: ❌ Issues:
  - Missing: progress reporting ("report every 100 items")
  - Extra: added --json flag (not in spec)

[Implementer fixes: remove --json, add progress reporting]
Spec reviewer: ✅ Spec compliant

[Dispatch code reviewer]
Code reviewer: Important — magic number 100, extract constant

[Implementer fixes: extract PROGRESS_INTERVAL]
Code reviewer: ✅ Approved

[Mark Task 2 complete]

... (tasks 3-5) ...

[Final cross-task code review]
Final reviewer: ✅ All requirements met, ready to merge
```

## Controller Responsibilities

The controller (you) orchestrates the flow. Key duties:

| Responsibility                    | Detail                                                    |
| --------------------------------- | --------------------------------------------------------- |
| **Extract tasks upfront**         | Read plan once, extract all task text — subagents never read the plan file |
| **Provide full context**          | Give each subagent the complete task text + architectural context          |
| **Answer questions**              | Respond clearly and completely before letting subagent proceed            |
| **Enforce review order**          | Spec compliance first, code quality second — never reversed              |
| **Track progress**                | Update TodoWrite after each task completes                               |
| **Dispatch sequentially**         | One implementation subagent at a time to avoid conflicts                  |

## Quality Gates

Each task passes through three quality checks:

| Gate               | Who             | What                                              |
| ------------------ | --------------- | ------------------------------------------------- |
| **Self-review**    | Implementer     | Completeness, naming, YAGNI, test quality          |
| **Spec review**    | Spec reviewer   | Matches requirements exactly — nothing more, less  |
| **Code review**    | Code reviewer   | Clean code, maintainability, test coverage         |

## Advantages

**vs. manual execution:**
- Fresh context per task (no confusion from accumulated state)
- Subagents follow TDD naturally
- Questions surfaced before work begins, not after

**vs. parallel-session plans:**
- No handoff overhead
- Continuous progress
- Review checkpoints are automatic

**Cost trade-off:** More subagent invocations (implementer + 2 reviewers per task), but catches issues early — cheaper than debugging later.

## NEVER Do

- **Skip either review** — both spec compliance and code quality are mandatory
- **Start code review before spec review passes** — wrong order wastes effort on code that doesn't meet spec
- **Dispatch multiple implementers in parallel** — causes merge conflicts and context corruption
- **Make subagents read the plan file** — provide full task text directly
- **Skip scene-setting context** — subagent needs to understand where the task fits architecturally
- **Ignore subagent questions** — answer fully before they proceed
- **Accept "close enough" on spec compliance** — if the reviewer found issues, it's not done
- **Skip re-review after fixes** — reviewer found issues → implementer fixes → reviewer reviews again
- **Let self-review replace actual review** — self-review is a first pass, not a substitute
- **Move to next task with open review issues** — current task must be fully approved first
- **Fix issues manually instead of through a subagent** — manual fixes pollute controller context

## Handling Failures

| Situation                    | Response                                              |
| ---------------------------- | ----------------------------------------------------- |
| Subagent asks questions      | Answer clearly, provide additional context if needed  |
| Reviewer finds issues        | Same implementer subagent fixes, reviewer re-reviews  |
| Subagent fails task entirely | Dispatch a new fix subagent with specific instructions |
| Task blocked by dependency   | Reorder remaining tasks or resolve dependency first    |
