---
name: audit-impl
categories: [audit]
description: Audit a completed implementation against its originating plan(s). Returns GO (merge approved) or NO GO (generates remediation file for retry). Final gate before merge in any implementation pipeline.
---

# Implementation Audit Skill

Audit a completed implementation against its plan(s) before merge. Identifies gaps, missed
requirements, scope creep, and unexpected changes. Produces a GO or NO GO verdict.

## When to Use

- After implementation completes and tests pass, as the last step before merging
- In single-plan pipelines: audit the worktree against the plan
- In multi-group pipelines: audit the feature branch against all group plans via manifest
- Standalone: `/autoskillit:audit-impl {plans_input} {branch_name} {base_branch}`

## Arguments

```
{plans_input} {branch_name} {base_branch} [conflict_report_paths]
```

- `plans_input` — one of:
  - A single plan `.md` file path
  - A comma-separated list of `.md` plan file paths (no spaces around commas)
  - A directory containing `*_plan_*.md` files
  - A `manifest_*.json` from `/autoskillit:make-groups`
- `branch_name` — commit SHA of the pre-implementation base ref (preferred from pipeline,
  stable after merge_worktree destroys named refs); a branch name is also accepted for
  standalone invocations. A live worktree path is accepted for legacy use (Step 0 extracts
  the branch name automatically).
- `base_branch` — branch to diff against (default: `integration`)
- `conflict_report_paths` (optional) — comma-separated list of absolute paths to conflict
  resolution reports produced by `resolve-merge-conflicts`. When provided and non-empty,
  cross-reference resolution decisions against plan intent in Step 2.5.

## Critical Constraints

**NEVER:**
- Modify source files, plan files, or any other files — read-only audit only
- Run tests — this skill audits, it does not fix
- Create files outside `temp/audit-impl/`
- Emit a GO verdict when any `MISSING` or `CONFLICT` finding exists

**ALWAYS:**
- Use Explore subagents for all file reads and diff retrieval
- Use `model: "sonnet"` when spawning all subagents via the Task tool
- Resolve all plan files before starting (abort early if any are missing)
- Write `Dry-walkthrough verified = TRUE` as the absolute first line of any remediation file

## Workflow

### Step 0 — Parse Arguments

Resolve `plans_input`:

- **Single `.md` file**: no comma, ends in `.md` → use it directly
- **Comma-separated `.md` paths**: value contains `,` → split on `,`, trim whitespace
  from each token. Validate that each trimmed token ends in `.md`; log a warning and
  skip any token that does not. Use each valid token as a plan file path
- **Directory**: no comma, does not end in `.md` or `.json` → glob for `*_plan_*.md`
  files in the directory
- **`manifest_*.json`**: no comma, ends in `.json` → parse it; extract `groups[*].file`
  paths, resolved relative to the manifest's parent directory

Verify every plan file exists. If any are missing, abort with a clear error listing them.

Determine the diff source from `implementation_ref`:

1. **If `implementation_ref` is an existing directory path:**
   - Extract the branch name: `git -C {implementation_ref} branch --show-current`
   - Run: `git diff {base_branch}...{branch_name}` from the current working directory
   - (This handles legacy manual invocations where a live worktree path is passed.)

2. **Otherwise, detect whether `implementation_ref` is a commit SHA or branch name:**
   - Detect SHA: `echo "$implementation_ref" | grep -qE '^[0-9a-f]{40}$'`
   - **If SHA (pre-implementation base ref, preferred from pipeline):**
     - Run: `git diff {implementation_ref}..{base_branch}` — two-dot, SHA on the left
     - This shows all commits added to base_branch since the pre-implementation snapshot,
       covering the full multi-group implementation across all merged worktrees.
   - **If branch name:**
     - Run: `git diff {base_branch}...{implementation_ref}` — three-dot (unchanged)
   - If git reports "unknown revision or path not in the working tree", abort with:
     > "implementation_ref '{implementation_ref}' is neither an existing worktree
     > directory nor a known git ref. If you are passing a worktree path, ensure
     > the worktree has not been deleted before calling audit-impl."

The old silent fallthrough (non-existent path treated as branch name without error)
is removed. A clear error is emitted instead.

Parse the optional fourth positional argument `conflict_report_paths` (may be absent or empty
string). Split on `,`, trim each entry, and filter out any empty strings after splitting;
store as `conflict_report_path_list`. Proceed even if empty — the cross-reference check in
Step 2.5 is skipped when the list is empty.

**Path-existence guard:** Before issuing a `Read` call on a path that is not guaranteed to
exist (e.g., plan file arguments, `temp/investigate/` reports, external file references), use
`Glob` or `ls` to confirm the path exists first. This prevents ENOENT errors that cascade into
sibling parallel-call cancellations.

### Step 0.5 — Code-Index Initialization (required before any code-index tool call)

Call `set_project_path` with the repo root where this skill was invoked (not a worktree path):

```
mcp__code-index__set_project_path(path="{PROJECT_ROOT}")
```

Code-index tools require **project-relative paths**. Always use paths like:

    src/<your_package>/some_module.py

NOT absolute paths like:

    /absolute/path/to/src/<your_package>/some_module.py

> **Note:** Code-index tools (`find_files`, `search_code_advanced`, `get_file_summary`,
> `get_symbol_body`) are only available when the `code-index` MCP server is configured.
> If `set_project_path` returns an error, fall back to native `Glob` and `Grep` tools
> for the same searches — they provide equivalent results without the code-index server.

Agents launched via `run_skill` inherit no code-index state from the parent session — this
call is mandatory at the start of every headless session that uses code-index tools.

### Step 1 — Load Plans via Parallel Subagents

Launch one Explore subagent per plan file in parallel. Each returns:

- Plan title and stated scope
- All files the plan said it would create, modify, or delete
- All tests the plan said it would add or modify
- Key requirements and constraints listed in the plan

Aggregate into a unified requirements inventory.

### Step 2 — Load Implementation Diff

**Stale branch guard (branch name refs only — skip for SHA refs):**

Skip this check when `implementation_ref` is a commit SHA (a SHA-as-ancestor of base_branch
is expected after all worktrees are merged — this check is only meaningful for named refs).

```bash
# Only run for branch name refs (not SHA):
if ! echo "$implementation_ref" | grep -qE '^[0-9a-f]{40}$'; then
    # Step 1: ref must exist at all
    git rev-parse --verify {implementation_ref} 2>/dev/null
    # Step 2: branch must not already be fully merged into base (fast-forward absorption check)
    git merge-base --is-ancestor {implementation_ref} {base_branch}
fi
```

- If ref lookup fails (branch ref not found): abort with a clear error —
  `"branch ref '{implementation_ref}' not found — it may have been absorbed by a fast-forward
   merge before audit_impl ran. This is a pipeline routing error."` Output `{"success": false}`
  with this message. Do not proceed to audit.

- If `--is-ancestor` exits 0 (branch is an ancestor of base — already fully merged): log a
  warning, then treat this as **GO** with note:
  `"Branch '{implementation_ref}' is already an ancestor of '{base_branch}' — absorbed by
   fast-forward merge prior to audit. No delta to evaluate; returning GO."` This is
  O(1), unambiguous, and distinguishes the stale-fast-forward case from legitimate no-op
  branches (empty diff is an unreliable guard; `--is-ancestor` is the correct tool).

Launch one Explore subagent to retrieve:

- `git diff {base_branch}...HEAD --stat` — file-level summary
- `git log {base_branch}..HEAD --oneline` — commit history
- `git diff {base_branch}...HEAD` — full diff

### Step 2.5 — Conflict Resolution Context Check

Before running standard audit, check if any plan contains a `PR Changes Inventory` section
(written by `merge-pr` to document all files changed by the PR).

If a `PR Changes Inventory` is found:
1. Extract the **Category C — Clean Carry-Overs** file list from each plan.
2. For each Category C file, verify it appears in the implementation diff.
3. Any Category C file absent from the diff is a `MISSING` finding — even if no plan
   requirement explicitly named it. Missing carry-over files indicate silent data loss
   in the conflict resolution and always force a `NO GO` verdict.

Record all Category C `MISSING` findings alongside the standard audit findings in Step 3.

**Conflict Resolution Report Cross-Reference (when `conflict_report_path_list` is non-empty):**

For each path in `conflict_report_path_list`:
1. Check whether the file exists before reading. If the path does not exist, log a warning
   `"Warning: conflict report not found at {path} — skipping"` and continue to the next path.
2. Read the conflict resolution report.
3. Parse the `## Per-File Resolution Decisions` table — extract all rows as
   `(file, category, confidence, strategy, justification)` tuples.
4. For each resolved file, check against the plan:
   - **Category 3 resolution flagged**: Any row with `Category = 3` indicates a Category 3
     (architectural tension) conflict was resolved rather than escalated. This ALWAYS forces a
     `CONFLICT` finding — Category 3 conflicts must never be automatically resolved per the
     `resolve-merge-conflicts` escalation contract.
   - **Strategy contradicts plan intent**: If the plan's `## Resolver Contract` or
     `## Implementation Steps` sections prescribe a specific outcome for the file that
     contradicts the recorded strategy (e.g., plan says "preserve the new API signature"
     but strategy is "ours" which kept the old signature), record a `CONFLICT` finding.
   - **Resolved file absent from diff**: If a file listed in the report's table is absent
     from the implementation diff entirely, record a `MISSING` finding — the resolved
     content was not carried into the integration branch.

Record all findings from this cross-reference alongside the standard Step 3 audit findings.
Each `CONFLICT` or `MISSING` finding here forces a `NO GO` verdict per the existing verdict
logic (Step 4).

### Step 3 — Audit via Parallel Subagents

Divide the requirements inventory into up to 3 slices. Launch parallel Explore subagents,
each receiving its slice and the full diff. Each subagent checks:

1. **Coverage** — Is every file and function the plan named present in the diff?
2. **Correctness** — Does the implementation match the plan's stated intent? Flag inversions,
   missing logic, or wrong approaches.
3. **Scope creep** — What is in the diff that no plan called for? Flag unexpected files or
   additions.
4. **Test coverage** — Were the plan's specified tests added?
5. **Cross-plan conflicts** (multi-plan only) — Do any two plans' changes interfere or
   contradict?

Each subagent returns structured findings:

- `COVERED` — requirement satisfied in the diff
- `MISSING` — required change absent from diff
- `ODD` — change in diff with no plan backing
- `CONFLICT` — two plans' implementations interfere with each other

### Step 4 — Verdict

**NO GO** if any finding is `MISSING` or `CONFLICT`.

**GO (with notes)** if only `ODD` findings exist — unexpected additions that do not break
correctness.

**GO** if all findings are `COVERED`.

### Step 5 — Output

#### If GO or GO with notes

Print:

```
## Audit Result: GO

### Scope Audited
{list of plan files audited}

### Summary
{2–3 sentences on overall implementation quality}

### Notes
{Minor ODD findings — not blockers. Omit section if none.}

### Verdict
MERGE APPROVED
```

Exit 0. The pipeline may proceed to merge.

After printing the GO result, emit the following structured output token as the very
last line of your text output:

```
verdict = GO
```

---

#### If NO GO

Generate `temp/audit-impl/remediation_{topic}_{YYYY-MM-DD_HHMMSS}.md`:

```markdown
Dry-walkthrough verified = TRUE

# Remediation Plan: {topic}

## Audit Context

Generated by `/autoskillit:audit-impl` after auditing:
{list of original plan files}

## Findings

{For each MISSING and CONFLICT finding:}

### {Finding type}: {short title}

- **Plan reference:** {plan file + section}
- **Expected:** {what the plan specified}
- **Found:** {what the diff shows, or "not present"}

## Remediation Steps

{For each finding, a concrete fix:}

### Fix: {short title}

- **File:** {path}
- **Change:** {what to add, modify, or remove}
- **Requirement:** {plan requirement this satisfies}

## Verification

After remediation:
- Run `task test-all`
- Re-run `/autoskillit:audit-impl` to confirm GO
```

Then print:

```
## Audit Result: NO GO

### Scope Audited
{list of plan files audited}

### Findings
{Mirror the findings from the remediation file}

### Remediation File
{absolute path to remediation file}

### Verdict
MERGE BLOCKED — feed remediation file to /autoskillit:retry-worktree or /autoskillit:implement-worktree-no-merge
```

Exit 1.

After printing the NO GO result, emit the following structured output tokens as the very
last lines of your text output:

```
verdict = NO GO
remediation_path = {absolute_path_to_remediation_file}
```

The `verdict` token must be exactly `GO` or `NO GO` — this is the value the recipe's
`on_result: field: verdict` routing matches against. The `remediation_path` token must
be the absolute path to the remediation file written in this session (only emitted for
NO GO; omit the `remediation_path=` line entirely on GO).

## Output Location

```
temp/audit-impl/
└── remediation_{topic}_{YYYY-MM-DD_HHMMSS}.md    (written on NO GO only)
```

## Related Skills

- `/autoskillit:implement-worktree` — produces the worktree this skill audits
- `/autoskillit:implement-worktree-no-merge` — orchestrator-mode implementation
- `/autoskillit:retry-worktree` — consumes the remediation file on NO GO
- `/autoskillit:make-groups` — produces the manifest this skill accepts as `plans_input`
