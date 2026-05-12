# Turboplan: Spec Mode

Spec out the project, decompose into shells, then run `$pick-next-shell`. If the spec turns out to fit a single session, automatically switch to plan mode.

## Task Tracking

Use `update_plan` to track each phase:

1. Run `$draft-spec` skill
2. Run `$refine-plan` skill (spec)
3. Run `$draft-shells` skill
4. Run `$refine-plan` skill (shells)
5. Run `$self-improve` skill
6. Run `$pick-next-shell` skill

If `$draft-shells` lands on the single-shell bail-out (Phase 3), the flow switches to plan mode by following [plan-mode.md](plan-mode.md). Replace the active plan with new entries for [plan-mode.md](plan-mode.md)'s Phases 1-5 (Codex `update_plan` only supports `pending`/`in_progress`/`completed`, so call `update_plan` with the new step list to drop tasks 4-6 from this file).

## Phase 1: Run `$draft-spec` Skill

Run the `$draft-spec` skill with the user's task description. `$draft-spec` guides the discussion and writes `.turbo/specs/<slug>.md`. Capture the spec path.

## Phase 2: Run `$refine-plan` Skill (Spec)

Run the `$refine-plan` skill with `spec <path>` from Phase 1.

## Phase 3: Run `$draft-shells` Skill

Run the `$draft-shells` skill, passing the spec path from Phase 1.

After it returns, check `.turbo/shells/<spec-slug>-*.md`:

- **Shells written** — capture the shell paths and continue with Phase 4.
- **No shells written** — `$draft-shells` hit the single-shell bail-out. Switch to plan mode: read [plan-mode.md](plan-mode.md) and follow its phases, passing `<spec path>` from Phase 1 as the Phase 1 input. Phases 4-6 of this file do not run.

## Phase 4: Run `$refine-plan` Skill (Shells)

Run the `$refine-plan` skill with `shells <slug>` from Phase 3.

## Phase 5: Run `$self-improve` Skill

Run the `$self-improve` skill to compound planning learnings.

## Phase 6: Run `$pick-next-shell` Skill

Run the `$pick-next-shell` skill.

Then update or check the active plan and proceed to any remaining task.

## Rules

- When `$draft-shells` triggers the single-shell bail-out, [plan-mode.md](plan-mode.md)'s phases replace Phases 4-6 here. The spec from Phase 1 and its refinement from Phase 2 already happened and remain the source of truth for the plan.
