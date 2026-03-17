---
name: plot-idea
description: >-
  Create a plan for review: idea branch, plan file, and draft PR.
  Part of the Plot workflow. Use on /plot-idea.
globs: []
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/skills
  version: 1.0.0-beta.1
compatibility: Designed for Claude Code and Cursor. Requires git. Currently uses gh CLI for forge operations, but the workflow works with any git host that supports pull request review.
---

# Plot: Create Idea

Create a plan for review: idea branch, plan file, and draft PR.

**Input:** `$ARGUMENTS` in the format `<slug>: <title description>`

Example: `/plot-idea sse-backpressure: Handle SSE client disconnects gracefully`

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
| 1. Parse Input | Small | String parsing |
| 2. Pre-flight Checks | Small (hard gate), Mid (soft warning) | Slug collision is mechanical; title similarity needs mid-tier |
| 3-8. Create Branch through Summary | Small | Git/gh commands, templates, file ops |

The entire skill is small-model capable except the soft duplicate warning (title similarity in step 2).

### 1. Parse Input

If `$ARGUMENTS` is empty or missing:
- Look at the conversation context for clues about what the user wants to plan
- If obvious, propose: "It looks like you want to plan `<slug>: <title>`. Shall I proceed?"
- Otherwise ask: "What's the idea? Usage: `/plot-idea <slug>: <title>`"

Extract `slug` and `title` from `$ARGUMENTS`:
- Everything before the first `:` is the slug (trimmed)
- Everything after is the title (trimmed)
- If no `:` found, treat the entire input as the slug and ask for a title
- Slug must match `[a-z0-9-]+` (lowercase letters, digits, hyphens only). If it doesn't, ask the user to fix it rather than silently normalizing

### 2. Pre-flight Checks

- Warn if working tree has uncommitted changes (offer to stash)
- Verify `gh auth status` has project scope
- Check that branch `idea/<slug>` does not already exist (if it does, ask whether to check it out or pick a new name)
- **Duplicate detection:**
  - `ls docs/plans/active/ 2>/dev/null` + `gh pr list --json headRefName --jq '.[].headRefName' | grep '^idea/'` to find existing plans and idea branches
  - **Hard gate:** if a plan with the identical slug already exists (file or branch), stop and ask the user to pick a different name
  - **Soft warning:** if any existing plan title shares 3+ significant words with the proposed title, warn the user and ask to confirm this is intentionally separate work (only check Draft/Approved plans, not Delivered ones)

> **Smaller models:** Skip the title similarity check. Enforce the hard gate (identical slug) only. Ask the user: "Could not check for similar plan titles. Please verify manually that this doesn't overlap with existing plans."

### 3. Create Branch

```bash
git fetch origin main
git checkout -b idea/<slug> origin/main
```

### 4. Create Plan File

```bash
CREATE_DATE=$(date -u +%Y-%m-%d)
```

Write `docs/plans/${CREATE_DATE}-<slug>.md` with this template:

```markdown
# <title>

> <title as one-line summary>

## Status

- **Phase:** Draft
- **Type:** feature | bug | docs | infra
- **Sprint:** <!-- optional, filled when plan is added to a sprint -->

## Changelog

<!-- Release note entry. Written during planning, refined during implementation. -->

- <user-facing change description>

## Motivation

<!-- Why does this matter? What problem does it solve? -->

## Design

### Approach

<!-- How will this be implemented? Key architectural decisions. -->

### Open Questions

- [ ] ...

## Branches

<!-- Branches to create when approved: -->
<!-- - `type/name` — description -->

- `feature/<slug>` — <description>

## Notes

<!-- Session log, decisions, links -->
```

Ask the user what **Type** to use, presenting this reference:

| Type | Use when | Examples |
|------|----------|----------|
| `feature` | New user-facing functionality | API endpoint, UI component, CLI command |
| `bug` | Fixing a defect | Crash fix, data corruption, incorrect output |
| `docs` | Documentation-only | README updates, API docs, guides |
| `infra` | CI, build, tooling, release automation | GitHub Actions, Dockerfile, linter config, deps |

Always ask — don't infer from the title.

### 5. Create Active Symlink and Commit

```bash
mkdir -p docs/plans/active docs/plans/delivered
ln -s ../${CREATE_DATE}-<slug>.md docs/plans/active/<slug>.md
git add docs/plans/${CREATE_DATE}-<slug>.md docs/plans/active/<slug>.md
git commit -m "plot: <title>"
git push -u origin idea/<slug>
```

### 6. Create PR

Create a **draft** PR (plan is still being written/refined):

```bash
gh pr create \
  --draft \
  --title "Plan: <title>" \
  --body "$(cat <<'EOF'
## Plan

See [`docs/plans/${CREATE_DATE}-<slug>.md`](../blob/idea/<slug>/docs/plans/${CREATE_DATE}-<slug>.md) on this branch.

Refine the plan, then mark ready for review with `gh pr ready`. Once reviewed, run `/plot-approve <slug>` to merge and start implementation.

---
*Created with `/plot-idea`*
EOF
)"
```

### 7. Add to Project Board

Read the `## Plot Config` section from `CLAUDE.md` for the project board name. If configured:

```bash
gh pr edit <number> --add-project "<project board name>"
```

If no project board is configured, skip this step.

### 8. Summary

Print:
- Branch: `idea/<slug>`
- Plan file: `docs/plans/<CREATE_DATE>-<slug>.md`
- Active index: `docs/plans/active/<slug>.md` (symlink)
- PR URL (draft)
- Next steps:
  1. Refine the plan (especially the **Branches** section)
  2. When ready for review: `gh pr ready <number>`
  3. After review: `/plot-approve <slug>`
