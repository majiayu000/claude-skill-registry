---
name: plot-deliver
description: >-
  Verify all implementation is done, then deliver the plan.
  Part of the Plot workflow. Use on /plot-deliver.
globs: []
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/skills
  version: 1.0.0-beta.1
compatibility: Designed for Claude Code and Cursor. Requires git. Currently uses gh CLI for forge operations, but the workflow works with any git host that supports pull request review.
---

# Plot: Deliver Plan

Verify all implementation is done, then deliver the plan. This workflow can be run manually (using git and forge CLI), by an AI agent interpreting this skill, or via a workflow script (once available).

For docs/infra work, this is the end — live when merged. For features/bugs, `/plot-release` follows when the team is ready to cut a versioned release.

**Input:** `$ARGUMENTS` is the `<slug>` of a plan on main.

Example: `/plot-deliver sse-backpressure`

<!-- keep in sync with plot/SKILL.md Setup -->
## Setup

Add a `## Plot Config` section to the adopting project's `CLAUDE.md`:

    ## Plot Config
    - **Project board:** <your-project-name> (#<number>)  <!-- optional, for `gh pr edit --add-project` -->
    - **Branch prefixes:** idea/, feature/, bug/, docs/, infra/
    - **Plan directory:** docs/plans/
    - **Active index:** docs/plans/active/
    - **Delivered index:** docs/plans/delivered/

## Model Guidance

| Steps | Min. Tier | Notes |
|-------|-----------|-------|
| 1-4. Parse through Verify PRs | Small | Git/gh commands, helper script, state checks |
| 5. Verify Completeness | Frontier (orchestrator) + Small (subagents) | Orchestrator extracts deliverables and consolidates; small subagents gather PR diffs in parallel |
| 6. Release Note Check | Small | File existence checks |
| 7-8. Deliver and Summary | Small | File ops, git commands, template |

Step 5 is the prime example of subagent delegation: a frontier orchestrator handles the judgment (extracting deliverables, consolidating Done/Partial/Missing), while small subagents handle the data collection (running `gh pr diff`, reading PR metadata) in parallel. Without subagents, the frontier model does everything sequentially.

### 1. Parse Input

If `$ARGUMENTS` is empty or missing:
- List active plans: `ls docs/plans/active/ 2>/dev/null`
- If exactly one exists, propose: "Found plan `<slug>`. Deliver it?"
- If multiple exist, list them and ask which one to deliver
- If none exist, explain: "No active plans found in `docs/plans/active/`."

Extract `slug` from `$ARGUMENTS` (trimmed, lowercase, hyphens only).

### 2. Verify Plan Exists

Check that an active plan exists for this slug: `ls docs/plans/active/<slug>.md` on main.

- If not in `active/`, check `docs/plans/delivered/<slug>.md` — if found there: "Already delivered."
- Also check the Phase field in the plan file — if already `Delivered`, stop.
- If not found anywhere: "No plan found for `<slug>`."

Resolve the symlink to find the actual plan file path (e.g., `docs/plans/YYYY-MM-DD-<slug>.md`).

### 3. Read and Parse Plan

Read the plan file (resolved from the `active/` symlink) and parse the `## Branches` section for PR references. If the plan has a `Sprint: <name>` field in its Status section, extract it for the summary.

Expected format after `/plot-approve`:
```markdown
- `feature/name` — description → #12
```

### 4. Verify All PRs Merged

Run the helper:

```bash
../plot/scripts/plot-impl-status.sh <slug>
```

Or for each PR number found in the Branches section:

```bash
gh pr view <number> --json state,isDraft --jq '{state: .state, isDraft: .isDraft}'
```

- If all are `MERGED`: proceed to step 5
- If any are `OPEN`:
  - If any open PRs have `isDraft: true`, list them and run `gh pr ready <number>` to mark each one ready for review — this is part of the delivery flow, not optional
  - List all remaining open PRs and ask the user: "These PRs are still open. Merge them first, or deliver anyway?"
  - If user declines, stop and list the unfinished PRs
- If any are `CLOSED` (not merged): warn — these need manual attention

### 5. Verify Plan Completeness

> **Model tiers for this step:**
> - **Frontier (e.g., Opus):** Full deliverable extraction, parallel PR diff review via subagents (small-model subagents gather diffs, frontier consolidates), Done/Partial/Missing checklist.
> - **Mid (e.g., Sonnet):** Extract deliverables and check PR titles/descriptions (skip full diff review). Can delegate PR metadata collection to small subagents. Present a simplified checklist based on PR metadata rather than code changes. Ask user to verify.
> - **Small (e.g., Haiku):** Skip entirely. Verify all PRs are merged (step 4), then ask: "All implementation PRs are merged. Ready to deliver this plan?" Human judgment is the final gate.

Compare what the plan promised against what was actually delivered.

1. **Extract deliverables** from the plan file. Look for actionable items in sections like `## Design`, `## Branches`, or bulleted lists that describe what should be built. Number each deliverable for reference.

2. **Gather PR evidence using parallel subagents.** Launch one Task agent per merged PR to review what was implemented:
   - Each agent receives the PR number and the full list of deliverables.
   - Each agent runs `gh pr diff <number>` and reads the PR body via `gh pr view <number> --json title,body,files`.
   - Each agent returns: which deliverables (by number) are addressed by that PR, with a one-line summary of the evidence for each.
   - Launch all PR agents in parallel since they are independent.

3. **Consolidate results.** Merge the per-PR reports into a single checklist. For each deliverable, mark it:
   - **Done** — clear evidence in one or more PRs
   - **Partial** — some work done but not fully matching the plan
   - **Missing** — no evidence found in any PR

4. **Present the checklist** to the user and **ask to confirm** the plan is complete enough to deliver.
   - If all items are done: "All deliverables verified. Proceed with delivery?"
   - If any are partial/missing: list them and ask "Deliver anyway, or hold off?"
   - If the user declines, stop — do not deliver.

### 6. Check for Release Note Entries

For feature and bug plans, check whether release note entries exist:

**Discover release note tooling** — check in this order, stop at first match:

1. **Changesets:** Does `.changeset/config.json` exist? If so, the project uses `@changesets/cli`. Check if `.changeset/*.md` files (excluding README.md) exist on main.
2. **Project rules:** Read `CLAUDE.md` and `AGENTS.md` for release note instructions (e.g., custom scripts, specific commands).
3. **Custom scripts:** Check `package.json` for release-related scripts (e.g., `release`, `version`, `changelog`).

If no tooling is found, skip this step.

If tooling was found but no release note entries exist for this plan's work, **warn** the user: "No release note entries found for this feature. Consider adding one before releasing."

This is a warning, not a blocker — proceed with delivery regardless.

Skip this step entirely for docs/infra plans (they don't need release notes).

### 7. Deliver Plan

The plan file stays in place — only the symlink moves from `active/` to `delivered/`.

```bash
git checkout main && git pull origin main

# Update Phase field in the plan file
# Change **Phase:** Approved → **Phase:** Delivered
# Add - **Delivered:** YYYY-MM-DD to the Status section
DELIVER_DATE=$(date -u +%Y-%m-%d)

# Move symlink from active/ to delivered/
git rm docs/plans/active/<slug>.md
ln -s ../YYYY-MM-DD-<slug>.md docs/plans/delivered/<slug>.md
git add docs/plans/delivered/<slug>.md docs/plans/YYYY-MM-DD-<slug>.md
git commit -m "plot: deliver <slug>"
git push
```

(Replace `YYYY-MM-DD-<slug>.md` with the actual date-prefixed filename from the resolved symlink.)

### 8. Summary

Print:
- Delivered: `<slug>`
- Plan file: `docs/plans/YYYY-MM-DD-<slug>.md` (unchanged location)
- Index: moved from `active/` to `delivered/`
- All implementation PRs: merged
- If the plan has a Sprint field: show sprint progress ("N/M sprint items delivered")
- Type reminder:
  - If feature/bug: "Run `/plot-release` when ready to cut a versioned release."
  - If docs/infra: "Live on main — no release needed."
