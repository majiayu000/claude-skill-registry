---
name: react-implementer-prompt
description: Use when dispatching a React frontend subagent from an implementation plan with React 19, Vitest/RTL/MSW, Zustand, and Tailwind v4
---

> ⚠️ **Spelling:** It's `saurun:` (with U), not "sauron"

# React Implementer Subagent Prompt Template

## Overview

A fill-in prompt template for dispatching React implementer subagents. Ensures every subagent gets complete context, follows TDD, self-reviews, and reports consistently.

**Core principle:** The subagent should never need to read the plan file or guess context — everything it needs is in the prompt.

## When to Use

- Dispatching a subagent for a React frontend implementation task from a plan
- Breaking an implementation plan into parallelizable units of work
- Any React frontend task requiring TDD, self-review, and structured reporting

## When NOT to Use

- Backend-only tasks (use `saurun:dotnet-implementer-prompt`)
- One-off questions or investigations (just ask directly)
- Tasks with no implementation (e.g., pure documentation, plan writing)

## Common Mistakes

- **Not pasting full task text** — writing "see task 3 in plan" instead of pasting the actual spec. The subagent cannot read plan files.
- **Vague context** — saying "you know the project" instead of specifying component names, store shape, and existing patterns.
- **Forgetting working directory** — subagent starts in wrong directory, wastes cycles figuring out project structure.
- **Saying "mock the store"** — violates `react-tdd` mock boundary rule. Subagent must use real Zustand stores with MSW for API boundaries.
- **Not specifying expected test failures** — if you know what the RED step should look like, tell the subagent so it can verify.
- **Omitting dependencies between tasks** — not mentioning that Task 2 depends on types introduced in Task 1.

## Template

The following shows the prompt structure to pass to the Task tool when dispatching a subagent:

```
Task tool (saurun:frontend-implementer):
  description: "Implement Task N: [task name]"
  prompt: |
    You are implementing Task N: [task name]

    ## Task Description

    [FULL TEXT of task from plan - paste it here, don't make subagent read file]

    ## Context

    [Scene-setting: where this fits, dependencies, architectural context]

    ## Before You Begin

    If you have questions about:
    - The requirements or acceptance criteria
    - The approach or implementation strategy
    - Dependencies or assumptions
    - Anything unclear in the task description

    **Ask them now.** Raise any concerns before starting work.

    ## Your Job

    Once you're clear on requirements:
    1. Implement exactly what the task specifies
    2. **REQUIRED SUB-SKILL:** Follow saurun:react-tdd strictly. No exceptions.
    3. **REQUIRED SUB-SKILL:** Follow saurun:react-tailwind-v4-components for all styling.
    4. Verify implementation works: `npx vitest run`
    5. Commit after each green test cycle
    6. Self-review (see below)
    7. Report back

    Work from: [directory]

    **Stack:** React 19 + Vite + TypeScript + Tailwind v4 + Zustand + Vitest + RTL + MSW

    **While you work:** If you encounter something unexpected or unclear, **ask questions**.
    It's always OK to pause and clarify. Don't guess or make assumptions.

    ## TDD Workflow

    **REQUIRED SUB-SKILL:** Follow saurun:react-tdd for the full Red-Green-Refactor cycle. No shortcuts, no skipping steps.

    ## Before Reporting Back: Self-Review

    Review your work with fresh eyes. Ask yourself:

    **Completeness:**
    - Did I fully implement everything in the spec?
    - Did I miss any requirements?
    - Are there edge cases I didn't handle?

    **Quality:**
    - Is this my best work?
    - Are names clear and accurate?
    - Is the code clean and maintainable?

    **Discipline:**
    - Did I avoid overbuilding (YAGNI)?
    - Did I only build what was requested?
    - Did I follow existing patterns in the codebase?

    **Testing:**
    - Did I follow TDD? (test first, watch fail, minimal code, watch pass, refactor)
    - Would each test catch a real bug? If not, delete it.
    - Did I use real Zustand stores (not mocked)?
    - Did I use MSW for API boundaries?
    - **REFERENCE:** See saurun:react-tdd for complete test quality criteria.

    **Tailwind v4:**
    - Did I use parentheses for CSS variables: `bg-(--var)` not `bg-[--var]`?
    - Did I use v4 utility names: `shadow-sm` not `shadow`, `rounded-sm` not `rounded`?
    - Did I use `cn()` from project utils (typically `lib/utils.ts` in shadcn/ui projects) for class merging?

    If you find issues during self-review, fix them now before reporting.

    ## Report Format

    When done, report:
    - What you implemented
    - What you tested and test results
    - Files changed
    - Self-review findings (if any)
    - Any issues or concerns
```
