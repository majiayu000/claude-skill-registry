---
name: sophisticate-todos
description: 'Deepen a coarse task list: split compound items into atomic tasks, order them by real dependency, and pin an observable acceptance criterion to each. Use when the user says "sophisticate the todos", "these tasks are too vague", or a list reads as headings rather than executable work. To re-sync a list that is stale rather than coarse, use update-todos.'
metadata:
  short-description: 'Split, order, and pin acceptance criteria on tasks'
---

# sophisticate-todos

A list of headings is not a plan. "Improve the auth flow" cannot be executed, cannot be finished, and cannot be checked. It hides every decision that matters behind a verb nobody can act on.

This skill is structural: it deepens a list that is too coarse to execute. For a list that is well-formed but out of date, use `update-todos` instead.

## Diagnose

Classify every item exactly once:

| Class | Meaning |
|---|---|
| `atomic` | One behavior, executable as written |
| `compound` | Hides two or more separable pieces of work |
| `vague` | Names an area, not a change |
| `unordered` | Correct, but placed where its dependencies are unmet |
| `unverifiable` | Executable, but nobody can tell when it is done |

**Completion criterion:** zero unclassified items.

## Split

Every `compound` item becomes N atomic tasks. A task is atomic when it names one behavior and can be executed without a further design decision.

The test is not length. A one-line task that still requires choosing between two approaches is compound.

**Completion criterion:** no task remains that hides more than one decision.

## Order

Draw the dependency edges. B depends on A only when B cannot function without A's output, not merely because A feels earlier.

Mark genuinely independent tasks as parallel. Introduce a phase only where a real barrier exists, never as decoration.

**Completion criterion:** every dependency is an edge someone can point at, and independent work is marked parallel rather than serialized by accident.

## Pin acceptance

Every task gets one observable done-test: a command, an output, or a state someone can check. "Works correctly" is not an acceptance criterion.

**Completion criterion:** zero items remain `vague` or `unverifiable`, and every task carries exactly one acceptance criterion.
