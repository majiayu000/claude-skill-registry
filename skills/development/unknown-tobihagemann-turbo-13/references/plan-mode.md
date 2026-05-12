# Turboplan: Plan Mode

Draft → refine → self-improve → mark ready → implement to produce a plan file and execute it in the same session.

## Task Tracking

Use `update_plan` to track each phase:

1. Run `$draft-plan` skill
2. Run `$refine-plan` skill
3. Run `$self-improve` skill
4. Mark plan ready
5. Run `$implement-plan` skill

## Phase 1: Run `$draft-plan` Skill

Run the `$draft-plan` skill with the input. The input may be a freeform task description, an explicit slug, or a spec path. Capture the resolved plan path from `$draft-plan`'s output for the next phases.

## Phase 2: Run `$refine-plan` Skill

Run the `$refine-plan` skill with `<path>` from Phase 1.

## Phase 3: Run `$self-improve` Skill

Run the `$self-improve` skill to compound planning learnings.

## Phase 4: Mark Plan Ready

Update the plan's YAML frontmatter to `status: ready`.

## Phase 5: Run `$implement-plan` Skill

Run the `$implement-plan` skill with the plan path from Phase 1.

Then update or check the active plan and proceed to any remaining task.

## Rules

- Route revisions through `$refine-plan` or `$draft-plan`.
