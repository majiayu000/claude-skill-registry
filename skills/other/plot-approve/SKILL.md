---
name: plot-approve
description: >-
  Merge an approved plan and fan out into implementation branches.
  Part of the Plot workflow. Use on /plot-approve.
globs: []
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/skills
  version: 1.0.0-beta.1
compatibility: Designed for Claude Code and Cursor. Requires git. Currently uses gh CLI for forge operations, but the workflow works with any git host that supports pull request review.
---

# Plot: Approve Plan

Merge an approved plan and fan out into implementation branches. This workflow can be run manually (using git and forge CLI), by an AI agent interpreting this skill, or via a workflow script (once available).

**Input:** `$ARGUMENTS` is the `<slug>` of an existing idea.

Example: `/plot-approve sse-backpressure`

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
| 1-3. Parse through Merge | Small | Git/gh commands, helper script, state checks |
| 4. Read and Parse Plan | Small | Structured markdown parsing |
| 4b. Branch Conflicts | Mid | Cross-referencing multiple plan files |
| 5-8. Create Branches through Summary | Small | Git/gh commands, templates |

Nearly all steps are mechanical. Step 4b (branch conflict detection) requires reading multiple plan files and comparing branch lists — mid-tier reasoning.

### 1. Parse Input

If `$ARGUMENTS` is empty or missing:
- List open plan PRs: `gh pr list --json number,title,headRefName --jq '.[] | select(.headRefName | startswith("idea/"))'`
- If exactly one exists, propose: "Found plan `<slug>`. Approve it?"
- If multiple exist, list them and ask which one to approve
- If none exist, explain: "No open plan PRs found. Create one first with `/plot-idea <slug>: <title>`."

Extract `slug` from `$ARGUMENTS` (trimmed, lowercase, hyphens only).

### 2. Determine Plan PR State

Run the helper to get plan PR state:

```bash
../plot/scripts/plot-pr-state.sh <slug>
```

Handle each case:

- **Plan PR is a draft**: Error — "Plan is still a draft. Mark it ready for review first: `gh pr ready <number>`"
- **Plan PR is open and non-draft (ready for review)**: Proceed to merge it (step 3)
- **Plan PR is already merged**: That's the approval signal — skip merge, proceed directly to creating impl branches (step 4)
- **Plan PR is closed (not merged)**: Error — "Plan PR is closed. Reopen it or create a new one."
- **No PR found**: Error — "No PR found for branch `idea/<slug>`. Run `/plot-idea <slug>: <title>` first."

### 3. Merge Plan PR (if open and non-draft)

```bash
gh pr merge <number> --merge --delete-branch
```

This lands the plan file on main and deletes the `idea/<slug>` branch.

Default to **merge commits** to preserve granular commit history (plan refinement steps are valuable context). If the project's `CLAUDE.md` specifies a different merge strategy, follow that instead.

### 4. Read and Parse Plan

Pull main to get the (just-merged or previously-merged) plan:

```bash
git checkout main
git pull origin main
```

Find the plan file: `ls docs/plans/active/<slug>.md` resolves to the date-prefixed file (e.g., `docs/plans/YYYY-MM-DD-<slug>.md`). Read it and parse the `## Branches` section. If the plan has a `Sprint: <name>` field in its Status section, note the sprint membership for the summary. Expected format:

```markdown
- `type/name` — description
```

Each line must have a backtick-quoted branch name (e.g. `feature/sse-backpressure`) and a description after the `—` dash.

Example — a valid Branches section:
```markdown
## Branches

- `feature/sse-backpressure` — Handle client disconnects gracefully
- `bug/sse-memory-leak` — Fix connection pool leak on timeout
```

Parsing rules:
1. Find the `## Branches` section
2. For each line starting with `- \``: extract the branch name between backticks, extract the description after ` — `
3. Skip comment lines (`<!-- ... -->`) and blank lines
4. If no branches are listed (or section is empty/only has the template comment), error: "No branches listed in the plan. Add branches to the `## Branches` section before approving."
5. Validate each branch name starts with a known prefix: `feature/`, `bug/`, `docs/`, `infra/`

### 4b. Check for Branch Conflicts

Before creating branches, check if any branch name from the `## Branches` section already exists in another Draft/Approved plan:

- Read all active plan files via `docs/plans/active/*.md` on main (excluding the current plan)
- For each plan, parse its `## Branches` section for branch names
- If any branch name in the current plan already appears in another plan, warn the user and ask to confirm before proceeding

Also check if any of the branches already exist as remote branches (`git ls-remote --heads origin <branch-name>`). If so, warn — the branch may be from a previous run of `/plot-approve` or from unrelated work.

> **Smaller models:** Skip cross-plan branch conflict detection. Only check if the branch already exists on the remote (`git ls-remote --heads origin <branch>`). Cross-plan overlap detection requires mid-tier reasoning.

### 5. Create Implementation Branches and PRs

Collect approval metadata once (reuse for all branches):

```bash
APPROVED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
APPROVED_BY=$(gh api user --jq '.login')
```

For **each branch** in the parsed list (use the `APPROVED_AT` and `APPROVED_BY` values collected above):

```bash
git checkout -b <type>/<name> origin/main
```

**Update the plan file (date-prefixed) on the branch** to reflect the approval:

1. Change `**Phase:** Draft` → `**Phase:** Approved`
2. Insert an `## Approval` section immediately after the `## Status` block:

```markdown
## Approval

- **Approved:** <APPROVED_AT>
- **Approved by:** <APPROVED_BY>
- **Assignee:** <APPROVED_BY>
```

This provides the initial commit needed for PR creation (no empty commits).

```bash
git add docs/plans/YYYY-MM-DD-<slug>.md
git commit -m "plot: approve <slug>"
git push -u origin <type>/<name>

gh pr create \
  --draft \
  --assignee @me \
  --title "<description>" \
  --body "$(cat <<'EOF'
## Plan

Part of [<slug>](../blob/main/docs/plans/YYYY-MM-DD-<slug>.md).

---
*Created with `/plot-approve`*
EOF
)"
```

(Replace `YYYY-MM-DD` with the actual date prefix from the plan filename.)

Read the `## Plot Config` section from `CLAUDE.md` for the project board name. If configured:

```bash
gh pr edit <number> --add-project "<project board name>"
```

Collect all created PR numbers and URLs.

### 6. Check for Release Note Requirements

After creating implementation PRs, check for project-specific release note tooling:

1. **Changesets:** Does `.changeset/config.json` exist? If so, the project uses `@changesets/cli`.
2. **Project rules:** Read `CLAUDE.md` and `AGENTS.md` for release note instructions (e.g., custom scripts, specific commands).
3. **Custom scripts:** Check `package.json` for release-related scripts (e.g., `release`, `version`, `changelog`).

If tooling is found, note the specific tool for the summary (step 8).

If no tooling is found, skip — the plan's `## Changelog` section will be used during `/plot-release`.

### 7. Update Plan File on Main

After all branches are created, update the plan file on main (date-prefixed path) to reflect the approval and link the implementation PRs.

1. Change `**Phase:** Draft` → `**Phase:** Approved`
2. Insert an `## Approval` section immediately after the `## Status` block (same content as step 5):

```markdown
## Approval

- **Approved:** <APPROVED_AT>
- **Approved by:** <APPROVED_BY>
- **Assignee:** <APPROVED_BY>
```

3. In the `## Branches` section, append ` → #<number>` to each branch line.

Before:
```markdown
- `feature/sse-backpressure` — Handle disconnects
- `bug/sse-memory-leak` — Fix connection leak
```

After:
```markdown
- `feature/sse-backpressure` — Handle disconnects → #12
- `bug/sse-memory-leak` — Fix connection leak → #13
```

```bash
git checkout main
git add docs/plans/YYYY-MM-DD-<slug>.md
git commit -m "plot: link implementation PRs for <slug>"
git push
```

### 8. Summary

Print:
- Plan merged: PR #<plan-number> (or "already merged" if it was pre-merged)
- Implementation PRs created:
  - `type/name` → PR #<number> (URL)
  - `type/name` → PR #<number> (URL)
- If release note tooling was found in step 6: "Remember to add release note entries on each implementation branch (e.g., `pnpm exec changeset`)."
- If the plan has a Sprint field: "Part of sprint `<sprint-name>`."
- Next step: check out a branch and start implementing
