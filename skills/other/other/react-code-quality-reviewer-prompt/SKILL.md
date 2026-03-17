---
name: react-code-quality-reviewer-prompt
description: Use when a React implementation task is complete and needs quality-focused code review, especially test quality validation (behavioral tests, assertion counts, mock boundaries, anti-patterns like getter/className tests)
---

> ⚠️ **Spelling:** It's `saurun:` (with U), not "sauron"

# React Code Quality Reviewer Prompt Template

## Overview

Prompt template for dispatching a React code quality review subagent. Core principle: verify that React code is well-built (clean, tested, maintainable) with special focus on test quality — tests should catch real bugs, not verify DOM structure or mock calls.

## When to Use

- After a React implementation task is complete and you need a quality-focused code review
- When you want to validate test quality beyond basic coverage (behavioral testing, structure, mock boundaries)
- When dispatching a unified code review that checks both spec compliance and code quality in a single pass

Implementers should follow `saurun:react-tdd` to proactively prevent the anti-patterns this reviewer flags.

## When NOT to Use

- For non-React code — the checklist is React/Vitest/RTL-specific
- For general architecture or design reviews without implementation code to inspect

## Quick Reference

| Section | Focus |
|---------|-------|
| Behavioral Testing | Tests catch bugs, not verify structure |
| Test Structure | Max 3 assertions, naming, it.each usage |
| Test Infrastructure | RTL render wrapper, MSW handlers |
| Mock Boundaries | MSW for HTTP only, real Zustand stores |
| Coverage | Edge cases, error paths, happy+failure |
| React 19 | useFormStatus, use(), Server Actions, useOptimistic |
| Tailwind v4 | CSS-first config, new syntax |
| Zustand | Real stores, subscription patterns |
| Accessibility | ARIA, keyboard nav, screen readers |

## Required Dependency

**REQUIRED PLUGIN:** `superpowers` — provides `code-reviewer` agent and `requesting-code-review/code-reviewer.md` base template.

The base template handles: git diff inspection, standard review checklist (code quality, architecture, testing, requirements, production readiness), and output format (Strengths, Issues by severity, Recommendations, Assessment with merge verdict). This skill adds React test quality criteria via `ADDITIONAL_REVIEW_CRITERIA`.

## Placeholder Variables

| Variable | Source |
|---|---|
| `WHAT_WAS_IMPLEMENTED` | From implementer subagent's completion report |
| `PLAN_OR_REQUIREMENTS` | Plan file path + task number, e.g. "Task 3 from _docs/plans/feature-x.md" |
| `BASE_SHA` | Commit SHA before implementation (`git log`) |
| `HEAD_SHA` | Current commit after implementation (typically `HEAD`) |
| `DESCRIPTION` | One-line task summary |

## Common Mistakes

- **Applying to non-React code** — checklist is Vitest/RTL/MSW-specific. Will produce false positives on other stacks.
- **Forgetting placeholder variables** — template breaks if `BASE_SHA`/`HEAD_SHA` are left as placeholders. Get actual SHAs from `git log`.
- **Missing superpowers plugin** — dispatch targets `superpowers:code-reviewer`. Task tool call fails without it.
- **MSW/Vitest as universal rule** — checklist assumes MSW + Vitest + RTL. Adjust if your project uses Jest + nock or other test tooling.

## Dispatch Template

This skill provides `ADDITIONAL_REVIEW_CRITERIA` for a unified review that checks both spec compliance and code quality in a single pass. The reviewer subagent loads this skill via the Skill tool and follows its criteria checklist.

Dispatch by calling the Task tool with `superpowers:code-reviewer`, instructing it to load this skill:

```
Task tool (superpowers:code-reviewer):
  Use template at requesting-code-review/code-reviewer.md

  WHAT_WAS_IMPLEMENTED: [from implementer's report]
  PLAN_OR_REQUIREMENTS: Task N from [plan-file]
  BASE_SHA: [commit before task]
  HEAD_SHA: [current commit]
  DESCRIPTION: [task summary]

  ADDITIONAL_REVIEW_CRITERIA: |
    ## React Test Quality Review Checklist

    Review ALL test files in the diff. For each test, apply these checks:

    ### Behavioral Testing
    - [ ] No className/style tests (flag: test asserts on `toHaveClass`, `toHaveStyle`, CSS variable values)
    - [ ] No getter/setter tests (flag: `can set`, `can get`, `has default`, `is nullable`)
    - [ ] Every test catches a real bug — ask "what bug does this prevent?" If answer is "none", flag it
    - [ ] Tests verify user-visible outcomes (text, roles, store state), not mock interactions (`toHaveBeenCalled`, `vi.fn()`)
    - [ ] No assertion-less tests (every test has at least one `expect`)
    - [ ] No "renders without crashing" tests — zero-assertion smoke tests prove nothing

    ### Test Structure
    - [ ] Max 3 assertions per test (single logical assertion OK even if multiple expect calls)
    - [ ] Naming follows `it('should [expected behavior] when [condition]')`
    - [ ] No "and" in test names — split into separate tests
    - [ ] `it.each`/`describe.each` used when testing same behavior with multiple inputs
    - [ ] One behavior per test — a test named "removes and clears" is two tests

    ### Test Infrastructure
    - [ ] Shared custom render wrapper used (not inline provider wrapping per test)
    - [ ] Zustand stores reset in `beforeEach` using the store's designated reset action or `useStore.setState(initialState)` — do NOT use `setState` with test values then assert those same values
    - [ ] No test-only props or exports in production components (no `data-testid` when accessible queries work)
    - [ ] MSW `setupServer` in shared setup file, not duplicated per test
    - [ ] `vitest.setup.ts` configures MSW lifecycle (`beforeAll/afterEach/afterAll`)
    - [ ] `onUnhandledRequest: 'error'` set in MSW server.listen()

    ### Mock Boundaries
    - [ ] API boundaries mocked via MSW (`http.get`, `http.post`, etc.)
    - [ ] Zustand stores NOT mocked — use real stores with controlled state
    - [ ] React components NOT mocked — render real component tree
    - [ ] Custom hooks NOT mocked — test through component rendering
    - [ ] `vi.mock` used ONLY for browser APIs (`window.location`, `IntersectionObserver`, timers)
    - [ ] Mock setup is <50% of test code

    ### Coverage
    - [ ] Edge cases tested (null, undefined, empty arrays, boundary values)
    - [ ] Error paths tested (API failures, invalid input, not found)
    - [ ] All new components/hooks have at least one test
    - [ ] Happy path + at least one failure path per user flow

    <!-- Review these sections when React 19 / Tailwind v4 are no longer the latest major versions -->
    ### React 19 Specifics
    - [ ] `useFormStatus` used correctly (only in child of `<form action>`)
    - [ ] `use()` for promises/context used in render (not in callbacks/effects)
    - [ ] Server Actions properly handled (if applicable)
    - [ ] `useOptimistic` used for optimistic UI updates (if applicable)

    <!-- Review these sections when React 19 / Tailwind v4 are no longer the latest major versions -->
    ### Tailwind v4 Compliance
    - [ ] No v3 CSS variable syntax: `[--var]` → must be `(--var)`
    - [ ] Renamed utilities correct: `shadow`→`shadow-sm`, `rounded`→`rounded-sm`, `blur`→`blur-sm`
    - [ ] No `ring-offset-*` (deprecated) → use `outline-*` + `outline-offset-*`
    - [ ] No `theme()` in arbitrary values → use `var(--color-*)` directly
    - [ ] `cn()` used for class merging (not template literals)
    - [ ] No `!prefix` important modifier → use `suffix!`

    ### Zustand Store Review
    - [ ] Selectors used to prevent unnecessary re-renders: `useStore((s) => s.field)` not `useStore()`
    - [ ] No derived state stored (compute in selector or component)
    - [ ] Actions don't read stale state (use `get()` inside `set()` callback)

    ### Accessibility (WCAG 2.1 AA)
    - [ ] Interactive elements have accessible names (aria-label or visible text)
    - [ ] Focus states visible: `focus-visible:outline-2 focus-visible:outline-offset-2`
    - [ ] Color contrast meets 4.5:1 for text
    - [ ] Form fields have associated labels
    - [ ] Dynamic content changes announced (aria-live, aria-busy)
    - [ ] Keyboard navigation works (Tab order, Enter/Space activation)

    ### Anti-Patterns to Flag
    Flag these by name in review:
    - **CanSetProperties**: Test that only verifies state assignment or prop values
    - **ClassNameTest**: Test that asserts on `toHaveClass` or CSS classes
    - **RendersSmokeTest**: Test with zero assertions ("renders without crashing")
    - **MockVerifyOnly**: Test where only assertion is `toHaveBeenCalled` or `vi.fn()` verification
    - **AssertionOverload**: Test with >3 unrelated assertions (Important); >5 unrelated is Critical
    - **DualBehavior**: Test name contains "and" — testing two things (e.g., "removes and clears")
    - **StoreMock**: `vi.mock` on Zustand store, component, or custom hook
    - **Assertionless**: Test with zero `expect()` calls — passes silently, catches nothing
    - **DirectSetState**: Test that uses `useStore.setState()` to SET values then asserts those same values
    - **ProviderDuplicate**: Provider wrapping copy-pasted across test files instead of shared render
    - **V3Syntax**: Tailwind v3 syntax in v4 project (brackets for CSS vars, old utility names)

    ### Severity Guide
    - **Critical**: className/getter tests, store/component mocking, no tests for new components, >5 unrelated assertions, assertion-less tests, v3 CSS variable syntax `[--var]`
    - **Important**: missing it.each, >3 unrelated assertions, duplicate provider setup, mock-verify-only, test naming violations, "and" in test names, missing accessibility labels
    - **Minor**: naming convention inconsistency, missing edge case test, magic numbers in test data
```

**Code reviewer returns:** Strengths, Issues (Critical/Important/Minor), Assessment — with specific test quality findings using the checklist above.
