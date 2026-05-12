# Resolve Findings: Direct Path

Apply evaluated findings via `$apply-findings`.

## Task Tracking

Use `update_plan` to track each phase:

1. Run `$code-style` skill
2. Run `$apply-findings` skill
3. Run `$finalize` skill

## Phase 1: Run `$code-style` Skill

Run the `$code-style` skill to load mirror, reuse, and symmetry rules before editing.

## Phase 2: Run `$apply-findings` Skill

Run the `$apply-findings` skill on the evaluated findings.

## Phase 3: Run `$finalize` Skill

If changes were made, run the `$finalize` skill.

Then update or check the active plan and proceed to any remaining task.
