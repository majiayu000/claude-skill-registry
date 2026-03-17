---
name: esper:atom
description: Create or refine a single increment. Smart stage detection — no active creates one, incomplete refines, ready waits for `esper:go`.
---

You are working in atom mode — focused on a single increment at a time.

## Step 1: Read context

Run `esperkit context get` to understand the current state.
Read `.esper/CONSTITUTION.md` for project constraints.

## Step 2: Smart stage detection

Check the context for `active_increment`:

### No active increment

1. Ask the user what they want to work on
2. Run `esperkit spec index` to show available specs
3. Help the user define the increment scope:
   - Title (concise, imperative — "Add user authentication")
   - Type: feature, fix, or chore
   - Which spec file is relevant (if any)
   - Which spec section is relevant (if any)
4. Run `esperkit increment create --title "..." --lane atomic --type <type> [--spec <file>] [--spec_section <section>]`
5. Run `esperkit increment activate <filename>`
6. Read the created increment file
7. Help the user fill in the body sections:
   - **Context**: what exists and why this change matters
   - **Scope**: what will change (specific, enumerated items)
   - **Files Affected**: file paths with create/modify annotations
   - **Verification**: exact commands and expected outcomes
   - **Spec Impact**: which specs may need updating
8. Write the refined increment file

### Active increment — incomplete as document

If the increment's body sections still have placeholder text:
1. Read the full increment file
2. Read referenced spec files
3. Help the user refine the incomplete sections
4. Write updates to the increment file

### Active increment — fully authored

If all body sections are filled in:
1. Present a summary of the increment
2. Tell the user the increment is ready for implementation
3. Say: "Run `esper:go` to begin implementation."

## Step 3: Plan authoring loop

Stay in the plan-authoring loop:
1. Present the current increment state
2. Accept refinements from the user
3. Write updates
4. Repeat until the user is satisfied

Do NOT begin implementation. Atom mode is for authoring the increment plan.
Implementation starts when the user runs `esper:go`.

## Available CLI commands

- `esperkit context get` — read current context
- `esperkit increment list` — list increments
- `esperkit increment create --title "..." --lane atomic [--type feature|fix|chore] [--spec <file>] [--spec_section <section>]` — create
- `esperkit increment activate <file>` — activate
- `esperkit spec index` — show spec tree
- `esperkit spec get <file>` — read a spec
