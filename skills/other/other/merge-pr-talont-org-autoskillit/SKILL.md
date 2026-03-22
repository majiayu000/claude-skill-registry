---
name: merge-pr
categories: [github]
description: Merge a single PR into the integration branch. For simple PRs, uses gh pr merge --squash --auto to enforce GitHub's required status checks. For needs_check PRs, re-assesses complexity and returns needs_plan=true with a conflict report when conflicts are detected. Use inside the merge-prs loop.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo 'Processing PR merge...'"
          once: true
---

# PR Merge Skill

Merge one PR into the current working branch (the integration branch). Handles both
simple direct merges and complexity re-assessment for PRs that may have accumulated
conflicts from earlier merges in the queue.

## When to Use

- Inside the `merge-prs` loop, once per PR
- Called with the PR number and its complexity tag from `analyze-prs` output

## Arguments

```
{pr_number} {complexity}
```

- `pr_number` — GitHub PR number (integer)
- `complexity` — `simple` or `needs_check` (from `analyze-prs` pr_order JSON)

## Critical Constraints

**NEVER:**
- Modify any source code files directly (conflict resolution is handled by `make-plan` + `implement-worktree-no-merge`)
- Use `git merge` to merge the PR into the integration branch — always use `gh pr merge --squash --auto`
- Close or comment on the PR
- Leave the git working tree in a dirty state
- Create files outside `temp/merge-prs/` directory

**ALWAYS:**
- Run `git status` before any operation to verify clean state
- Use `gh pr merge {pr_number} --squash --auto` for the simple path — this enforces the repository's required status checks before the merge executes
- Poll `gh pr view {pr_number} --json state,mergedAt` to confirm the merge completed
- Fetch the PR branch from remote before the deletion regression scan and conflict analysis

## Workflow

### Step 0: Validate Inputs

- Parse `pr_number` (must be a positive integer)
- Parse `complexity` (must be `simple` or `needs_check`)
- Verify git working tree is clean: `git status --porcelain` must be empty. If dirty: abort with error.
- Identify current branch: `git branch --show-current` (this is the integration branch)

### Step 1: Fetch PR Information

```bash
gh pr view {pr_number} --json number,title,headRefName,baseRefName,body,additions,deletions,files
gh pr diff {pr_number}
BASE_BRANCH=$(gh pr view {pr_number} --json baseRefName --jq '.baseRefName')
```

Extract:
- `pr_branch`: the headRefName
- `pr_title`: the title
- `pr_files`: list of changed file paths
- `BASE_BRANCH`: the baseRefName (target branch of the PR, e.g. `main`)

Fetch the PR branch locally:
```bash
git fetch origin {pr_branch}:{pr_branch} 2>/dev/null || git fetch origin pull/{pr_number}/head:{pr_branch}
```

### Step 1.5: Deletion Regression Scan

Before attempting any merge, check whether this PR reintroduces code that was
deliberately deleted from the base branch after the PR's branch point.

**This step runs for ALL PRs regardless of complexity tag.**

```bash
BASE_BRANCH=$(gh pr view {pr_number} --json baseRefName --jq '.baseRefName')
# 1. Find the divergence point between this PR and the base branch
MERGE_BASE=$(git merge-base origin/${BASE_BRANCH} origin/{pr_branch})

# 2. Files deleted from base since the branch point
DELETED_FILES=$(git diff --name-only --diff-filter=D ${MERGE_BASE} origin/${BASE_BRANCH})

# 3. Symbols (functions/classes) removed from files this PR modifies,
#    relative to base (catches deletions in files that still exist)
PR_FILES=$(git diff --name-only ${MERGE_BASE}...origin/{pr_branch})
if [ -n "$PR_FILES" ]; then
  DELETED_SYMBOLS=$(
    echo "$PR_FILES" | \
    git diff --diff-filter=M ${MERGE_BASE} origin/${BASE_BRANCH} --pathspecs-from-file=- \
      | grep '^-' \
      | grep -E '^-(def |class |async def )' \
      | sed 's/^-//' \
      | sort -u
  )
else
  DELETED_SYMBOLS=""
fi

# 4. What the PR adds (relative to the merge base)
PR_ADDITIONS=$(git diff ${MERGE_BASE}...origin/{pr_branch} | grep '^+' | grep -v '^+++')
```

**Detect regressions:**

- **File-level regression**: For each path in `DELETED_FILES`, check if
  `git show origin/{pr_branch}:{file}` succeeds — if yes, the PR re-adds a deleted file.
- **Symbol-level regression**: For each symbol in `DELETED_SYMBOLS`, check whether
  `PR_ADDITIONS` contains a matching `def {symbol_name}` or `class {symbol_name}` line.

**If regressions are found:**

Skip direct merge. Proceed to file classification (the PR Changes Inventory section
below). When writing the conflict report, include a `## Deletion Regressions` section
(see template below) and set `deletion_regression=true` in the output tokens.

The regression context (list of regressed files/symbols + the commits that deleted them
on base) must be written to the conflict report so `make-plan` understands that these
items must NOT be reintroduced in the implementation.

**If no regressions are found:** Continue to Step 2 / Step 3 as normal. Emit
`deletion_regression=false` in the Step 5 output.

**Gather regression evidence** for each found regression:

```bash
# For each regressed file: find the commit that deleted it on base
git log --diff-filter=D --oneline --follow -- {file_path} origin/${BASE_BRANCH} | head -1

# For each regressed symbol: find the commit that removed it
git log --diff-filter=M --oneline -p -- {file_path} origin/${BASE_BRANCH} \
  | grep -B20 "^-def {symbol_name}\|^-class {symbol_name}" \
  | grep "^[0-9a-f]\{7,\}" \
  | head -1
```

**Template for the conflict report** — add after the `## Resolver Contract` section:

```markdown
## Deletion Regressions

This PR was branched before the following deliberate deletions landed on `{base_branch}`.
The PR's changes reintroduce code that was intentionally removed. These MUST NOT be
preserved during conflict resolution — the deletion is the correct state.

| Deleted item | Type | Deleted by commit | What the PR does |
|---|---|---|---|
| `{path or symbol}` | file\|function\|class | `{sha} {commit message}` | Re-adds it |

**Resolver instruction:** Treat each item in this table as Category B (semantic overlap).
The correct resolution for every regression listed above is to **remove the reintroduced
code** from the PR's changes, not to restore it. The base branch's deletion is authoritative.
```

### Step 2: Simple Path — gh pr merge

Queue the merge on GitHub using auto-merge so that the integration branch ruleset
(required status checks) is enforced before GitHub executes the merge:

```bash
gh pr merge {pr_number} --squash --auto
```

**After queuing, poll until the PR is merged or until timeout:**

```bash
gh pr view {pr_number} --json state,mergedAt
```

- Poll interval: 30 seconds, timeout: 600 seconds (10 minutes)
- If `state == "MERGED"`: return `merged=true, needs_plan=false`
- If PR state transitions to `CLOSED` unexpectedly (CI failed and auto-merge was
  cancelled): return `merged=false` with an error message describing the CI failure
  so the pipeline can route to cleanup_failure
- Do NOT fall back to local git merge. If `gh pr merge` exits non-zero because
  GitHub detected a merge conflict (e.g. "Merge conflict" error), treat this as
  conflict detection: return `needs_plan=true` with `conflict_report_path` set so
  the pipeline routes to the complex worktree path.

### Step 3: Complexity Path — `needs_check` (Re-assessment)

Before attempting any merge, re-assess complexity against the current integration branch state.

Launch an Explore subagent to:

1. Determine `base_branch` from the PR: extract `baseRefName` from the `gh pr view` result in Step 1 (this is the branch the PR targets, e.g. `main`).

2. Get the current integration branch's changes since base_branch:
   ```bash
   git log ${BASE_BRANCH}..HEAD --oneline
   git diff ${BASE_BRANCH}...HEAD --stat
   ```
2. Get this PR's full diff: the diff fetched in Step 1
3. Identify file-level overlap: files in the PR diff that also appear in the integration branch diff
4. For each overlapping file, inspect both diffs to assess:
   - Do they modify the same functions or classes?
   - Would the PR's changes be semantically incompatible with what's already been merged?
   - Would resolving the conflicts require understanding the intent of both changes (not just picking lines)?
   - Do the combined test changes risk test suite conflicts?

**Re-assessment verdict:**

**Still simple** (all of these are true):
- File overlap is only in non-logic files (e.g., imports, constants, docstrings)
- No shared functions/classes are modified by both
- No test conflicts that require semantic reconciliation
→ Proceed to direct merge (same as Step 2 above)

**Complex** (any of these):
- Shared functions or classes modified by both
- The PR assumes a code structure that earlier merges have changed
- Resolving the conflict requires understanding the intent of both PRs
- Test changes from both sides modify the same test file in ways that conflict semantically
→ Proceed to write conflict report below

### Step 3.5: Fetch All PR-Changed Files

Before writing the conflict report, fetch the complete set of files changed on the PR branch
(not just the conflicting files) and classify them:

```bash
# All files changed on the PR branch relative to the base
git diff ${BASE_BRANCH}...origin/{pr_branch} --name-only
```

Classify each file into one of three categories:

- **Category A — Git Conflicts**: files where `git` reported unresolved conflicts
  (`git diff --name-only --diff-filter=U` after a failed merge attempt)
- **Category B — Semantic Overlaps**: files that were auto-merged by git but appear in
  both the PR and the integration branch diff (risky — may need human review)
- **Category C — Clean Carry-Overs**: files changed only by this PR; the integration branch
  did not touch them. These must be preserved in full during conflict resolution.

Assess whether the conflicts can be confidently resolved. If any conflict is genuinely
ambiguous (insufficient context, unclear intent, irreconcilable logic), set
`escalation_required=true` in the output and do not write a conflict report — instead
describe the ambiguity so a human can decide.

### Step 4: Write Conflict Report (complex path only)

Before composing the report, extract `## Requirements` from the PR body:
```bash
gh pr view {pr_number} --json body -q .body
```
Extract the `## Requirements` section if present — set `requirements_section = ""` if not found. Gracefully skip if `gh` is unavailable.

Compute timestamp: `YYYY-MM-DD_HHMMSS`.

Write `temp/merge-prs/conflict_pr{pr_number}_plan_{ts}.md`:

```markdown
# Conflict Resolution Plan: PR #{pr_number} — "{pr_title}"

## Context

This PR could not be merged directly into the integration branch because it has
semantic conflicts with previously merged PRs.

**PR:** #{pr_number}
**Branch:** {pr_branch}
**Integration Branch:** {integration_branch (current HEAD)}

## PR Changes Inventory

All files changed by this PR, classified by conflict type:

### Category A — Git Conflicts
Files where `git` reported unresolved merge conflicts:
- `{file}` — {brief description}

### Category B — Semantic Overlaps
Files that were auto-merged but are present in both the PR and the integration branch
diff (verify intent is preserved):
- `{file}` — {brief description}

### Category C — Clean Carry-Overs
Files changed only by this PR; the integration branch did not touch them.
**These files must be carried over in full** — they are not conflicts, just PR changes
that must not be dropped during resolution.
- `{file}` — {brief description}

## Resolver Contract

The implementer MUST:
1. Resolve all Category A conflicts, preserving the intent of both this PR and earlier merges.
2. Verify Category B files for semantic correctness after auto-merge.
3. Carry over every Category C file exactly as the PR changed it — no omissions.
4. **NEVER use `git merge` to apply changes.** Use `git cherry-pick <commit>` for individual
   commits or `git checkout <branch> -- <file>` for specific files. `merge_worktree` requires
   linear commit history — merge commits cause `WORKTREE_INTACT_MERGE_COMMITS_DETECTED` failure.

If any conflict cannot be confidently resolved, do NOT guess. Set `escalation_required=true`
in the output and describe the ambiguity for human review.

{If requirements_section is non-empty, include this block to give make-plan the full requirement context:}
## Requirements

{requirements_section from PR body}

## PR Summary

{pr_body or a 2–3 sentence summary of what the PR does}

## Conflict Analysis

### Overlapping Files

| File | What Earlier Merges Did | What This PR Does | Conflict Type |
|------|------------------------|-------------------|---------------|
| {path} | {summary} | {summary} | {logic/signature/test/structural} |

### Root Conflicts

For each conflict:

**Conflict {N}: {short title}**
- **File:** {path}
- **Function/Class:** {name if applicable}
- **Earlier merge changed:** {description}
- **This PR assumes:** {description}
- **Reconciliation needed:** {what needs to happen to satisfy both}

## Implementation Task

Apply the changes from PR #{pr_number} (branch: `{pr_branch}`) to the current integration
branch, resolving the conflicts identified above. The goal is to preserve the intent of
both this PR and the PRs already merged.

### Required Changes

For each conflict, specify what the reconciled implementation must do:

1. **{file path}**: {concrete description of the reconciled change needed}
2. ...

### Verification

After implementation:
- All tests from this PR's test files must pass
- All previously passing tests must continue to pass
- The functionality described in PR #{pr_number} must be present in the integration branch
```

### Step 5: Return Result

Print a JSON result block to stdout for recipe capture:

**On successful GitHub auto-merge (simple path, `state == "MERGED"`):**
```json
{
    "merged": true,
    "needs_plan": false,
    "deletion_regression": false,
    "pr_number": 42,
    "pr_branch": "feature/auth",
    "pr_title": "Add user authentication",
    "conflict_report_path": null
}
```

**On complex / conflict detected (including when `gh pr merge` reports a GitHub-side conflict):**
```json
{
    "merged": false,
    "needs_plan": true,
    "deletion_regression": false,
    "escalation_required": false,
    "pr_number": 47,
    "pr_branch": "feature/db-refactor",
    "pr_title": "Refactor database layer",
    "conflict_report_path": "temp/merge-prs/conflict_pr47_plan_YYYY-MM-DD_HHMMSS.md"
}
```

When `gh pr merge --squash --auto` itself exits non-zero due to a GitHub-side conflict,
treat this as a complex-path trigger: write the conflict report and return `needs_plan=true`
with `conflict_report_path` set. The pipeline then routes to make-plan → implement-worktree-no-merge
→ push_worktree_branch → create_conflict_pr → wait_for_conflict_ci → merge_conflict_pr.

**On deletion regression detected:**
```json
{
    "merged": false,
    "needs_plan": true,
    "deletion_regression": true,
    "escalation_required": false,
    "pr_number": 47,
    "pr_branch": "feature/stale-branch",
    "pr_title": "Feature from stale branch",
    "conflict_report_path": "temp/merge-prs/conflict_pr47_plan_YYYY-MM-DD_HHMMSS.md"
}
```

**On escalation required (ambiguous conflict):**
```json
{
    "merged": false,
    "needs_plan": false,
    "deletion_regression": false,
    "escalation_required": true,
    "pr_number": 47,
    "pr_branch": "feature/db-refactor",
    "pr_title": "Refactor database layer",
    "conflict_report_path": null,
    "escalation_reason": "Description of why the conflict cannot be resolved automatically"
}
```

Exit 0 in all cases — `needs_plan=true` and `escalation_required=true` are routing signals, not failures.

After printing the result block, emit the following structured output tokens as the
very last lines of your text output:

**On successful GitHub auto-merge:**
```
merged = true
needs_plan = false
deletion_regression = false
pr_number = {pr_number}
pr_branch = {pr_branch_name}
pr_title = {pr_title}
```

**On complex / conflict detected:**
```
merged = false
needs_plan = true
deletion_regression = false
escalation_required = false
pr_number = {pr_number}
pr_branch = {pr_branch_name}
pr_title = {pr_title}
conflict_report_path = {absolute_path_to_conflict_plan_file}
```

**On deletion regression detected:**
```
merged = false
needs_plan = true
deletion_regression = true
escalation_required = false
pr_number = {pr_number}
pr_branch = {pr_branch_name}
pr_title = {pr_title}
conflict_report_path = {absolute_path_to_conflict_plan_file}
```

**On escalation required:**
```
merged = false
needs_plan = false
deletion_regression = false
escalation_required = true
escalation_reason = {human-readable description of why the conflict cannot be resolved automatically}
pr_number = {pr_number}
pr_branch = {pr_branch_name}
pr_title = {pr_title}
```

Emit `conflict_report_path=` only when `needs_plan=true` and a conflict plan file was
written. Omit the line entirely on a successful direct merge or when `escalation_required=true`.

## Output Location

```
temp/merge-prs/
└── conflict_pr{N}_plan_{ts}.md    (written only when needs_plan=true)
```

## Related Skills

- **`/autoskillit:analyze-prs`** — Produces the pr_order JSON that feeds this skill
- **`/autoskillit:make-plan`** — Receives `conflict_report_path` as its task when needs_plan=true
- **`/autoskillit:dry-walkthrough`** — Verifies the plan before implementation
- **`/autoskillit:implement-worktree-no-merge`** — Implements conflict resolution in a worktree
