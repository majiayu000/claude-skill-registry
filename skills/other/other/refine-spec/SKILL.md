---
name: refine-spec
description: "Iteratively review and revise a specification document until no new findings survive evaluation. Runs /review-spec, /evaluate-findings, /apply-findings, then re-runs itself until stable. Use when the user asks to \"refine the spec\", \"refine this spec\", \"iterate on the spec\", \"tighten the spec\", or \"improve the spec\"."
---

# Refine Spec

Loop the spec review pipeline over a spec file until no new findings are accepted. Writes back to the spec file in place.

## Task Tracking

At the start of every invocation (including re-runs from Step 5), use `TaskCreate` to create a task for each step:

1. Resolve the spec file
2. Run `/review-spec` skill
3. Run `/evaluate-findings` skill
4. Run `/apply-findings` skill
5. Re-run `/refine-spec` skill if changed

## Step 1: Resolve the Spec File

Determine which spec file to refine using these rules in order:

1. **Explicit path** — If an absolute or relative path was passed, use it
2. **Explicit slug** — If a slug was passed (e.g., `photo-sorter-v2`), resolve to `.turbo/specs/<slug>.md`
3. **Single file** — Glob `.turbo/specs/*.md`. If exactly one file exists, use it
4. **Most recent** — If multiple files exist, use the most recently modified
5. **Legacy fallback** — If `.turbo/specs/` does not exist but `.turbo/spec.md` exists, use it
6. **Nothing found** — If no spec file exists, tell the user to run `/draft-spec` first and stop

If multiple files exist and the most-recent choice is non-obvious (e.g., several specs were modified within the same minute), use `AskUserQuestion` to let the user pick from the candidates.

State the resolved spec path before continuing.

## Step 2: Run `/review-spec` Skill

Run the `/review-spec` skill on the resolved spec file. Pass the full spec text.

Always run this step even if the spec looks polished.

## Step 3: Run `/evaluate-findings` Skill

Run the `/evaluate-findings` skill on the review findings from Step 2.

If zero actionable findings survive evaluation, skip to the end and report the spec as stable.

## Step 4: Run `/apply-findings` Skill

Run the `/apply-findings` skill on the evaluated results. The target file is the spec file resolved in Step 1. Apply accepted findings by editing the spec in place.

## Step 5: Re-run `/refine-spec` Skill if Changed

Check whether the spec file was edited during Step 4. Any edit counts.

**If changes were made**, classify what Step 4 edited:

- **Structural edits** (added or removed sections, new or removed requirements, rewired cross-references, changed acceptance criteria) — run `/refine-spec` again via the Skill tool, passing the resolved spec path. If the round contains both structural and prose-only edits, treat it as structural and re-run automatically.
- **Prose-only edits only** (reworded sentences in place, fixed stale examples, clarified existing text without changing meaning) — output a summary of what changed, then use `AskUserQuestion` to ask whether to run one more round or stop here. Do not silently continue or silently stop.

**If this is iteration 3 and changes were still made**, the hard cap is reached. This replaces the classification gate above. Output a summary of what is still changing and whether it is structural or prose-only. Then use `AskUserQuestion` to offer three options: continue for another iteration, stop here and accept the spec as-is, or escalate to `/consult-oracle` for a different perspective on the remaining issues.

The re-invocation is a full, fresh run of this skill. Every step (1-5) executes with its own task tracking and skill invocations.

## Rules

- Every step must run in every iteration. `/evaluate-findings` is a judgment gate that must run before `/apply-findings` touches the spec. Each step must invoke its designated skill via the Skill tool.
- Re-invocations from Step 5 are full runs with fresh task tracking and complete skill invocations.
- The spec file is the only file that should change.
- If `/review-spec` returns no findings on the first pass, report the spec as stable and stop.
