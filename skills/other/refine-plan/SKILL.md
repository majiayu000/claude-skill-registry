---
name: refine-plan
description: "Iteratively review and revise a planning artifact until no new findings survive evaluation. Supports plans, shells, and specs. Use when the user asks to \"refine the plan\", \"refine the shells\", \"refine this spec\", \"iterate on the plan\", \"iterate on the shells\", \"tighten the plan\", \"tighten the shells\", \"tighten the spec\", \"improve the plan\", \"improve the shells\", or \"improve the spec\"."
---

# Refine Plan

Loop the review pipeline over a planning artifact until no new findings are accepted. Writes back to the artifact file(s) in place. Supports plans, shells, and specs.

## Task Tracking

At the start of every invocation (including re-runs from Step 5), use `update_plan` to track each step:

1. Resolve the artifact
2. Run `$review-plan` skill
3. Run `$evaluate-findings` skill
4. Run `$apply-findings` skill
5. Re-run `$refine-plan` skill if changed

## Step 1: Resolve the Artifact

### Determine Artifact Type

1. **Explicit argument** — If the user specified a type (e.g., "refine plan", "refine shells", "refine spec"), use it
2. **Conversation context** — Infer from conversation (e.g., if `$draft-plan` just ran, type is plan)
3. **Auto-detect** — Check `.turbo/` for existing artifacts. If multiple types exist, use `request_user_input`

### Resolve the Artifact File(s)

#### Plan

1. **Explicit path** — use it
2. **Explicit slug** — resolve to `.turbo/plans/<slug>.md`
3. **Single file** — Glob `.turbo/plans/*.md`. If exactly one file exists, use it
4. **Most recent** — most recently modified file
5. **Legacy fallback** — `.turbo/plan.md` if `.turbo/plans/` does not exist
6. **Nothing found** — tell the user to run `$turboplan` (for a new task) or `$pick-next-shell` (for existing shells) and stop

#### Shells

1. **Explicit spec slug** — Glob `.turbo/shells/<slug>-*.md`
2. **Explicit spec path** — derive slug from filename, glob as above
3. **Single spec** — Glob `.turbo/specs/*.md`. If exactly one, derive slug and glob for shells
4. **Most recent spec** — most recently modified spec, derive slug and glob
5. **Nothing found** — tell the user to run `$draft-shells` first and stop

For shells, read each shell file and extract from its YAML frontmatter: `spec` (source spec path) and `depends_on`. Verify the source spec exists. State the spec path, number of shells, and each shell's filename.

#### Spec

1. **Explicit path** — use it
2. **Explicit slug** — resolve to `.turbo/specs/<slug>.md`
3. **Single file** — Glob `.turbo/specs/*.md`. If exactly one, use it
4. **Most recent** — most recently modified
5. **Legacy fallback** — `.turbo/spec.md` if `.turbo/specs/` does not exist
6. **Nothing found** — tell the user to run `$draft-spec` first and stop

If multiple candidates exist and the choice is non-obvious, use `request_user_input`.

State the resolved path(s) before continuing.

## Step 2: Run `$review-plan` Skill

Run the `$review-plan` skill on the resolved artifact.

Always run this step even if the artifact looks polished.

## Step 3: Run `$evaluate-findings` Skill

Run the `$evaluate-findings` skill on the review findings from Step 2.

## Step 4: Run `$apply-findings` Skill

Run the `$apply-findings` skill on the evaluated results.

## Step 5: Re-run `$refine-plan` Skill if Changed

Check whether the artifact file(s) were edited during Step 4. Any edit counts.

The iteration number below refers to the `$refine-plan` run currently executing Step 5. It is not the iteration number of a prospective re-run. Iteration 1 is the initial run; iteration 2 is the first auto-re-run; iteration 3 is the second auto-re-run; iteration 4 and beyond exist only when the user opts in at the hard-cap ask. Iterations 1 and 2 always follow the classification gate (they never trigger the hard cap at their own Step 5, even when the auto-re-run they spawn would be iteration 3). The hard cap fires at the end of iteration 3 and every iteration thereafter.

**Iterations 1 and 2, if changes were made**, classify what Step 4 edited:

- **Structural edits** — run `$refine-plan` again by reading and following the installed skill instructions, passing the artifact type and resolved path. If the round contains both structural and prose-only edits, treat it as structural and re-run automatically.
- **Prose-only edits only** (reworded sentences in place, fixed stale examples, clarified existing text without changing meaning) — output a summary of what changed, then use `request_user_input` to ask whether to run one more round or stop here. Do not silently continue or silently stop.

**Iterations 1 and 2, if changes were made but you believe re-running is unnecessary**, use `request_user_input` to ask for skip permission. Do not skip silently.

**Iteration 3 or later, if Step 4 of this run made changes**, the hard cap is reached. This replaces the classification gate above for iteration 3 and every iteration after it. Output a summary of what is still changing and whether it is structural or prose-only. Then use `request_user_input` to offer three options: continue for another iteration, stop here and accept the artifact as-is, or escalate to `$consult-oracle` for a different perspective on the remaining issues.

The re-invocation is a full, fresh run of this skill. Every step (1-5) executes with its own task tracking and skill invocations.

Then update or check the active plan and proceed to any remaining task.

### Structural Edit Examples by Type

- **Plan** — added or removed steps, new or removed design decisions, rewired dependencies between steps, changed testing strategy
- **Shells** — added or removed shells, changed Produces/Consumes/Covers Spec Requirements wiring, changed frontmatter `depends_on`, added or removed spec requirement coverage
- **Spec** — added or removed sections, new or removed requirements, rewired cross-references, changed acceptance criteria

## Rules

- Every step must run in every iteration. `$evaluate-findings` is a judgment gate that must run before `$apply-findings` touches the artifact. Each step must invoke its designated skill by reading and following the installed skill instructions.
- Re-invocations from Step 5 are full runs with fresh task tracking and complete skill invocations.
- The artifact file(s) are the only files that should change. For shells, do not modify the source spec.
