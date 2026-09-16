---
name: code-comment-discipline
description: Apply whenever writing or editing source code in any core's build agent (backend-eng, ui-builder, or equivalent). Governs when a comment belongs at all and what it may say. Default is no comment; a comment is only for the non-obvious. Never restates what the code does, never narrates the task, fix, or conversation that produced it.
---

# Code Comment Discipline

Well-named identifiers and clear structure explain what code does. A
comment earns its place only when it explains something the code cannot:
a hidden constraint, a non-obvious invariant, a workaround for a specific
external bug, or behavior that would surprise a reader.

## Default: no comment

Most lines, functions, and blocks need zero comments. Before writing one,
check whether the same clarity is reachable by renaming a variable or
function instead — prefer that over a comment every time.

## When a comment is allowed

Only for the non-obvious:

- A constraint imposed from outside the code (an API's undocumented
  limit, a browser quirk, a platform requirement) that isn't visible at
  the call site.
- An invariant the code relies on that isn't implied by types or names
  (e.g. "callers must hold the lock before this runs").
- A deliberate workaround for a specific bug in a dependency, with enough
  detail to know when it's safe to remove.
- Behavior that looks like a mistake but is intentional.

## What a comment must never say

- What the code does — that's the identifier's job, not the comment's.
- Why *this* task needed the change, who asked for it, or which ticket,
  issue, or conversation prompted it.
- History: "used to be X," "changed from Y," "removed Z," "previously,"
  "now we," or any other before/after narration. A comment states the
  current state and its non-obvious reason only, never how it got there.
- A restatement of the function/variable name in prose ("increments the
  counter" above `counter++`).

## Applying to existing comments

When editing a file that already has comments violating these rules,
remove or rewrite them as part of the same change rather than leaving
them in place — don't let a nearby edit normalize the pattern.
