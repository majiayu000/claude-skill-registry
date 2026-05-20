---
name: resolve-merge-conflicts
categories: [github]
description: >
  Goal-aware resolution of rebase conflicts when merging a conflict-resolution worktree
  back into the integration branch. Analyzes the intent of each side of a conflict,
  resolves it in-place when confidence is HIGH or MEDIUM, and escalates when LOW.
---

# Resolve Merge Conflicts Skill

## Arguments (positional)

- `{worktree_path}` — absolute path to the existing worktree (must exist; rebase was aborted cleanly)
- `{plan_path}` — absolute path to the implementation plan (`temp/make-plan/…_plan_….md`, relative to the current working directory)
- `{base_branch}` — the integration branch to rebase onto (e.g. `integration/run-N`)

## Critical Constraints

**NEVER:**
- Run the full test suite — that is the pipeline `test` step's responsibility; tests already passed before `merge_to_integration` was attempted
- Attempt partial resolution when any conflict file is LOW confidence — abort and escalate instead
- Leave unresolved conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) in any file
- Loop back to the calling pipeline step — emit output tokens and exit cleanly
- Exceed 3 rebase continuation rounds — abort and escalate if exceeded

**ALWAYS:**
- Run `git rebase --abort` before emitting `escalation_required=true`
- Emit both `escalation_required=true` and `escalation_reason=` when escalating
- Emit `worktree_path=` and `branch_name=` on successful resolution
- Run `pre-commit run --all-files` after a successful rebase before emitting output tokens
- Validate all three positional arguments before touching git state
- Write `conflict_resolution_report_*.md` to `temp/resolve-merge-conflicts/` and emit `conflict_report_path=` after successful conflict resolution

## When to Use

- Called by the `merge-prs` when `merge_worktree` fails with
  `failed_step=rebase` and `state=worktree_intact_rebase_aborted`
- The worktree must still be intact (rebase aborted cleanly, no partial state)

## Workflow

### Step 0 — Validate inputs

Parse three positional path arguments (space-separated). Fail with a clear error message
if any is missing or invalid:

```
ERROR: resolve-merge-conflicts requires three arguments:
  worktree_path  — absolute path to the existing worktree
  plan_path      — absolute path to the implementation plan
  base_branch    — integration branch to rebase onto
```

Validation checks:
1. Verify `worktree_path` directory exists and is a git worktree:
   ```bash
   git -C {worktree_path} rev-parse --git-dir
   ```
2. Verify `plan_path` file exists (readable Markdown).
3. Verify `base_branch` is reachable:
   ```bash
   git -C {worktree_path} rev-parse --verify origin/{base_branch}
   ```
   If origin ref is not found, run `git -C {worktree_path} fetch origin {base_branch}` first.

### Step 1 — Load conflict context

Read `plan_path` to extract:
- What the original PR conflict was about (look for `## Context`, `## PR Summary`,
  `## Conflict Analysis` sections)
- What the implementation plan prescribed (look for `## Implementation Steps`)
- Which files were expected to be modified (look for `## PR Changes Inventory`,
  `Category A`, `Category B`, `Category C` sections)

Run commit log queries to understand the divergence:

```bash
# What commits exist in the worktree that are not on the integration branch
git -C {worktree_path} log --oneline origin/{base_branch}..HEAD

# What commits the integration branch received since the worktree was created
git -C {worktree_path} fetch origin
git -C {worktree_path} log --oneline HEAD..origin/{base_branch}
```

### Step 2 — Re-attempt rebase to surface conflicts

```bash
git -C {worktree_path} rebase origin/{base_branch}
```

**On success (clean rebase):** The integration branch advanced in a non-conflicting way
since the last attempt. Proceed directly to Step 7 — emit output tokens and exit.

**On conflict:** Proceed to Step 3.

### Step 3 — Analyze each conflicting file with goal awareness

For each file listed by `git -C {worktree_path} diff --name-only --diff-filter=U`:

#### 3.1 — Read the conflict diff

Read the full file content including conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
to understand the specific lines in tension.

#### 3.2 — Determine intent of **ours** (worktree side)

- Consult the plan's `## Implementation Steps` section
- Run `git -C {worktree_path} log --oneline -5 -- {file}` to see recent commits on this file
- Infer the functional intent: what behavior was being added or changed?

#### 3.3 — Determine intent of **theirs** (integration branch side)

- Run `git -C {worktree_path} log --oneline origin/{base_branch} -5 -- {file}` to see recent
  integration-branch commits touching this file
- Retrieve integration-branch file content:
  ```bash
  git -C {worktree_path} show origin/{base_branch}:{file}
  ```
- Infer the functional intent: what behavior was being added or changed?

#### 3.4 — Classify the conflict

Assign one of three conflict categories:

- **Category 1 — Textual overlap, compatible goals**: Both sides achieve the same functional
  outcome with different text (e.g., both added the same import, both updated the same
  docstring, or both reformatted the same block). Resolution: keep the better expression or
  combine them (e.g., union of imports).

- **Category 2 — Same file, different concerns**: Two independent features changed the same
  file. The changes address different functions, classes, or sections with no semantic
  interference. Resolution: interlace both sets of changes, ensuring correct ordering
  (sorted imports, proper placement of new functions/methods).

- **Category 3 — Architectural tension**: Both sides made structural decisions that cannot
  coexist without choosing one over the other or restructuring. Examples: conflicting class
  hierarchies, incompatible API signatures, contradictory type definitions.

#### 3.5 — Assign a confidence level

| Confidence | Criteria |
|---|---|
| **HIGH** | Category 1 or 2 conflict where the intent of **both** sides is clear from plan + git log |
| **MEDIUM** | Category 2 conflict where one side's intent has moderate ambiguity |
| **LOW** | Category 3 conflict; or any conflict where intent cannot be determined from available context; or the conflicting file is outside the scope recorded in the plan's PR Changes Inventory |

### Step 4 — Confidence gate

**Maintain a `resolution_log`:** As you resolve each file, record a log entry with:
`file` (path), `category` (1/2/3), `confidence` (HIGH/MEDIUM), `strategy` (ours/theirs/combined),
and `justification` (one sentence). Accumulate all entries across all rebase continuation rounds.
This list is consumed in Step 6 to write the decision report.

**If any conflict file is rated LOW:**

Run `git rebase --abort` immediately:

```bash
git -C {worktree_path} rebase --abort
```

Emit escalation output tokens and exit:

```
escalation_required = true
escalation_reason = <brief human-readable explanation: which file(s), which category, why confidence was LOW>
```

**Do NOT attempt partial resolution.** Partial resolution with remaining LOW-confidence
conflicts produces incorrect merges that are harder to debug than a clean abort.

**Escalation criteria — these ALWAYS cause LOW confidence and trigger abort:**

1. Any conflicting file is Category 3 (architectural tension)
2. The intent of either side cannot be determined from the plan + git log
3. `rebase --continue` triggers more than 3 additional conflict rounds
4. The conflict involves files outside the scope recorded in the plan's `PR Changes Inventory`

**If all conflict files are HIGH or MEDIUM:**

For each conflicting file, proceed to resolution (Step 4.1).

#### 4.1 — Resolve conflict markers

Edit each file directly to resolve all conflict markers. No unresolved `<<<<<<<`, `=======`,
or `>>>>>>>` markers may remain after editing.

Resolution strategy by category:

- **Category 1 (textual overlap)**: Prefer the implementation that is more precise or
  idiomatic. If genuinely equivalent, keep both if combinable (e.g., union of imports).
  For non-plan-critical sections, prefer the integration branch's version.

- **Category 2 (different concerns)**: Ensure both sets of changes are present and correctly
  ordered (e.g., imports sorted, new functions placed at the appropriate location in the file).

After resolving each file:
```bash
git -C {worktree_path} add {file}
```

#### 4.2 — Continue the rebase

After all files for this round are resolved and staged:

```bash
GIT_EDITOR=true git -C {worktree_path} rebase --continue
```

(`GIT_EDITOR=true` skips the interactive commit message prompt.)

**If `rebase --continue` surfaces a new conflict round:** Repeat Step 3 analysis for the
new conflicts. Track the number of continuation rounds. If the total exceeds 3, abort and
escalate:

```bash
git -C {worktree_path} rebase --abort
```

```
escalation_required = true
escalation_reason = Rebase required more than 3 continuation rounds — conflict complexity exceeds automated resolution threshold.
```

### Step 5 — Post-rebase hygiene

After a successful `rebase --continue` (no more conflict rounds):

```bash
cd {worktree_path} && pre-commit run --all-files
```

Fix any auto-fixable violations (ruff format, ruff check). Re-stage fixed files and
re-run `pre-commit run --all-files` to confirm clean.

**Do NOT run the full test suite.** Testing is handled by the pipeline's `test` step,
which already ran and passed before `merge_to_integration` was first attempted. Running
tests here would be redundant and is explicitly prohibited.

### Step 6 — Write Conflict Resolution Report

Create the directory and write the conflict resolution report:

```bash
mkdir -p {worktree_path}/temp/resolve-merge-conflicts
```

Write the report to:
```
{worktree_path}/temp/resolve-merge-conflicts/conflict_resolution_report_{YYYY-MM-DD_HHMMSS}.md
```

Report format:

```markdown
# Merge Conflict Resolution Report

**Worktree:** {worktree_path}
**Base Branch:** {base_branch}
**Timestamp:** {ISO-8601 timestamp, e.g. 2026-03-14T21:09:00Z}
**Files Conflicting:** {total number of files that had conflicts across all rebase rounds}
**Files Resolved:** {number of files successfully resolved}

## Per-File Resolution Decisions

| File | Category | Confidence | Strategy | Justification |
|------|----------|------------|----------|---------------|
| {file_path} | {1/2/3} | {HIGH/MEDIUM} | {ours/theirs/combined} | {one-sentence justification} |
```

One row per file from `resolution_log`. The table MUST be a standard GFM pipe table so downstream
tools can extract rows programmatically by splitting on `|`.

After writing, capture the absolute path to this file as `conflict_report_file_path` for use in
Step 7.

**If no conflicts were encountered** (clean rebase in Step 2, or Step 2 succeeded immediately):
Skip this step — emit `worktree_path=` and `branch_name=` only (no `conflict_report_path`).

### Step 7 — Emit output tokens

```
worktree_path = {worktree_path}
branch_name = {current_branch}
conflict_report_path = {conflict_report_file_path}
```

Where `{current_branch}` is the output of:
```bash
git -C {worktree_path} branch --show-current
```

Omit `conflict_report_path=` line entirely when the rebase was clean (no conflicts occurred — `resolution_log` is empty).

## Output contract

| Token | Type | When emitted |
|---|---|---|
| `worktree_path=` | directory_path | On successful resolution (confidence gate passed) |
| `branch_name=` | string | On successful resolution |
| `conflict_report_path=` | file_path | On successful resolution when at least one conflict was resolved |
| `escalation_required=true` | string literal `'true'` (lowercase) | When confidence is LOW or rebase rounds exceed 3 |
| `escalation_reason=` | string | When confidence is LOW — explains which file and why |

## Error handling

- **Validation failures**: Emit clear error message and abort before touching git state
- **`rebase --continue` failure** (not a conflict): Abort with `git -C {worktree_path} rebase --abort` and escalate
- **`pre-commit` failure**: Fix auto-fixable violations (ruff format/check) and re-run; do not escalate for formatting-only failures
- **Unexpected git state**: Run `git -C {worktree_path} rebase --abort` before exiting
