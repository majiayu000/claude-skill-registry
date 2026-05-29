---
name: esper:spec
description: Create, review, or revise spec files. Opens a spec editing loop that continues until the user advances with `esper:go`.
---

You are working on the project's spec tree — the authoritative documentation of system behavior.

## Step 1: Read context

Run `esperkit context get` to understand the current state.
Read `.esper/CONSTITUTION.md` for project vision and constraints.
Run `esperkit spec index` to see the spec tree structure.

## Step 2: Determine working scope

If the user specified a topic or file:
- Check if a spec file exists for it: `esperkit spec get <path>`
- If it exists, open it for revision
- If not, create it: `esperkit spec create <path>`

If no specific topic:
- Show the spec index and ask what area the user wants to work on
- If the spec tree is mostly scaffold (empty template files), offer to bootstrap specs from code analysis:
  - Read the codebase structure (key source files, package.json, etc.)
  - Propose a spec structure that documents what exists
  - Write initial specs based on the actual code

## Step 3: Spec authoring loop

Enter a revision loop:
1. Read the current spec file
2. Present the content to the user
3. Accept feedback and revisions
4. Write updates to the spec file
5. Repeat until the user is satisfied

When writing specs:
- Use clear, declarative language ("The system does X" not "The system should do X")
- Document actual behavior, not aspirational behavior
- Include concrete examples where helpful
- Reference other spec files by relative path when describing cross-cutting concerns

## Step 4: Stay in spec mode

Continue in the spec revision loop until:
- The user explicitly says they're done with specs
- The user invokes `esper:go` to advance to implementation
- The user switches to a different skill

Do NOT automatically advance to implementation. Spec work is its own distinct phase.

## Available CLI commands

- `esperkit spec index` — show the spec tree index
- `esperkit spec get <file>` — read a spec file
- `esperkit spec create <path>` — create a new spec file
- `esperkit spec set-root <path>` — change the spec root directory
- `esperkit spec archive <file>` — archive a spec file
- `esperkit spec list` — list all specs with metadata
