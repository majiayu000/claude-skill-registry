---
name: refine-plan-shells
description: "Iteratively review and revise plan shells until no new findings survive evaluation. Runs /review-plan-shells, /evaluate-findings, /apply-findings, then re-runs itself until stable. Use when the user asks to \"refine plan shells\", \"refine the shells\", \"iterate on the shells\", \"tighten the shells\", or \"improve the plan shells\"."
---

# Refine Plan Shells

Loop the shell review pipeline over a set of plan shells until no new findings are accepted. Writes back to the shell files in place.

## Task Tracking

At the start of every invocation (including re-runs from Step 5), use `TaskCreate` to create a task for each step:

1. Resolve the plan shells
2. Run `/review-plan-shells` skill
3. Run `/evaluate-findings` skill
4. Run `/apply-findings` skill
5. Re-run `/refine-plan-shells` skill if changed

## Step 1: Resolve the Plan Shells

Determine which set of shells to refine using these rules in order:

1. **Explicit spec slug** — If a spec slug was passed, glob `.turbo/plans/<slug>-*.md` and filter to files whose YAML frontmatter has `type: shell`
2. **Explicit spec path** — If a spec path was passed, derive the slug from the filename and glob as above
3. **Single spec** — Glob `.turbo/specs/*.md`. If exactly one spec exists, derive its slug and glob for shells
4. **Most recent spec** — If multiple specs exist, use the most recently modified. Derive its slug and glob for shells
5. **Nothing found** — If no shells exist, tell the user to run `/draft-plan-shells` first and stop

If multiple specs exist and the most-recent choice is non-obvious (e.g., several specs were modified within the same minute), use `AskUserQuestion` to let the user pick from the candidates.

Read each resolved shell file and extract from its YAML frontmatter:

- `type` (must be `shell`)
- `status`
- `spec` (source spec path)
- `depends_on`

Verify that the source spec exists. State the spec path, the number of shells found, and each shell's filename and status before continuing.

## Step 2: Run `/review-plan-shells` Skill

Run the `/review-plan-shells` skill, passing the spec slug or the list of shell paths. It reads all shells and the source spec, then checks wiring invariants (Produces, Consumes, Covers Spec Requirements) across all shells and returns combined findings.

Always run this step even if the shells look polished.

## Step 3: Run `/evaluate-findings` Skill

Run the `/evaluate-findings` skill on the review findings from Step 2.

If zero actionable findings survive evaluation, skip to the end and report the shells as stable.

## Step 4: Run `/apply-findings` Skill

Run the `/apply-findings` skill on the evaluated results. Target files are the shell files resolved in Step 1. Apply accepted findings by editing the affected files in place.

## Step 5: Re-run `/refine-plan-shells` Skill if Changed

Check whether any shell file was edited during Step 4. Any edit to any file counts.

**If changes were made**, classify what Step 4 edited:

- **Structural edits** (added or removed shells, changed `Produces`/`Consumes`/`Covers Spec Requirements` wiring, changed frontmatter `depends_on`, added or removed spec requirement coverage) — run `/refine-plan-shells` again via the Skill tool, passing the spec slug. If the round contains both structural and prose-only edits, treat it as structural and re-run automatically.
- **Prose-only edits only** (reworded implementation steps in place, fixed stale examples, clarified existing text without changing meaning) — output a summary of what changed, then use `AskUserQuestion` to ask whether to run one more round or stop here. Do not silently continue or silently stop.

**If changes were made but you believe re-running is unnecessary**, use `AskUserQuestion` to ask for skip permission. Do not skip silently.

**If this is iteration 3 and changes were still made**, the hard cap is reached. This replaces the classification gate above. Output a summary of what is still changing and whether it is structural or prose-only. Then use `AskUserQuestion` to offer three options: continue for another iteration, stop here and accept the shells as-is, or escalate to `/consult-oracle` for a different perspective on the remaining issues.

The re-invocation is a full, fresh run of this skill. Every step (1-5) executes with its own task tracking and skill invocations.

Check your task list for remaining tasks and proceed.

## Rules

- Every step must run in every iteration. `/evaluate-findings` is a judgment gate that must run before `/apply-findings` touches the shells. Each step must invoke its designated skill via the Skill tool.
- Re-invocations from Step 5 are full runs with fresh task tracking and complete skill invocations.
- Shell files are the only files that should change. Do not modify the source spec.
- If `/review-plan-shells` returns no findings on the first pass, report the shells as stable and stop.
