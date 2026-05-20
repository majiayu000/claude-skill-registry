---
name: audit-impl
description: Audit a completed implementation against its originating plan(s). Returns GO (merge approved) or NO GO (generates remediation file for retry). Final gate before merge in any implementation pipeline.
---

# Implementation Audit Skill

Audit a completed implementation against its plan(s) before merge. Identifies gaps, missed
requirements, scope creep, and unexpected changes. Produces a GO or NO GO verdict.

## When to Use

- After implementation completes and tests pass, as the last step before merging
- In single-plan pipelines: audit the worktree against the plan
- In multi-group pipelines: audit the feature branch against all group plans via manifest
- Standalone: `/audit-impl {plans_input} {implementation_ref} {base_branch}`

## Arguments

```
{plans_input} {implementation_ref} {base_branch}
```

- `plans_input` — one of:
  - A single plan `.md` file path
  - A comma-separated list of `.md` plan file paths (no spaces around commas)
  - A directory containing `*_plan_*.md` files
  - A `manifest_*.json` from `/make-groups`
- `implementation_ref` — worktree path (if intact), branch name, or commit SHA containing the implementation
- `base_branch` — branch to diff against (default: `main`)

## Critical Constraints

**NEVER:**
- Modify source files, plan files, or any other files — read-only audit only
- Run tests — this skill audits, it does not fix
- Create files outside `temp/audit-impl/`
- Emit a GO verdict when any `MISSING` or `CONFLICT` finding exists

**ALWAYS:**
- Use Explore subagents for all file reads and diff retrieval
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

2. **Otherwise, detect whether `implementation_ref` is a commit SHA or branch name:**
   - Detect SHA: `echo "$implementation_ref" | grep -qE '^[0-9a-f]{40}$'`
   - **If SHA:**
     - Run: `git diff {implementation_ref}..{base_branch}` — two-dot, SHA on the left
     - This shows all commits added to base_branch since the snapshot.
   - **If branch name:**
     - Run: `git diff {base_branch}...{implementation_ref}` — three-dot
   - If git reports "unknown revision or path not in the working tree", abort with:
     > "implementation_ref '{implementation_ref}' is neither an existing worktree
     > directory nor a known git ref."

**Path-existence guard:** Before issuing a `Read` call on a path that is not guaranteed to
exist (e.g., plan file arguments, `temp/investigate/` reports, external file references), use
`Glob` or `ls` to confirm the path exists first. This prevents ENOENT errors that cascade into
sibling parallel-call cancellations.

### Step 1 — Load Plans via Parallel Subagents

Launch one Explore subagent per plan file in parallel. Each returns:

- Plan title and stated scope
- All files the plan said it would create, modify, or delete
- All tests the plan said it would add or modify
- Key requirements and constraints listed in the plan

Aggregate into a unified requirements inventory.

### Step 2 — Load Implementation Diff

**Stale branch guard (branch name refs only — skip for SHA refs):**

```bash
# Only run for branch name refs (not SHA):
if ! echo "$implementation_ref" | grep -qE '^[0-9a-f]{40}$'; then
    # Step 1: ref must exist at all
    git rev-parse --verify {implementation_ref} 2>/dev/null
    # Step 2: branch must not already be fully merged into base
    git merge-base --is-ancestor {implementation_ref} {base_branch}
fi
```

- If ref lookup fails: abort with a clear error —
  `"branch ref '{implementation_ref}' not found — it may have been absorbed by a fast-forward
   merge before audit-impl ran."`

- If `--is-ancestor` exits 0 (branch is already an ancestor of base — fully merged): log a
  warning, then treat this as **GO** with note:
  `"Branch '{implementation_ref}' is already an ancestor of '{base_branch}' — absorbed by
   fast-forward merge prior to audit. No delta to evaluate; returning GO."`

Launch one Explore subagent to retrieve:

- `git diff {base_branch}...HEAD --stat` — file-level summary
- `git log {base_branch}..HEAD --oneline` — commit history
- `git diff {base_branch}...HEAD` — full diff

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

---

#### If NO GO

Generate `temp/audit-impl/remediation_{topic}_{YYYY-MM-DD_HHMMSS}.md`:

```markdown
Dry-walkthrough verified = TRUE

# Remediation Plan: {topic}

## Audit Context

Generated by `/audit-impl` after auditing:
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
- Run the project's test suite
- Re-run `/audit-impl` to confirm GO
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
MERGE BLOCKED — feed remediation file to /implement-worktree or /retry-worktree
```

## Output Location

```
temp/audit-impl/
└── remediation_{topic}_{YYYY-MM-DD_HHMMSS}.md    (written on NO GO only)
```

## Related Skills

- **`/implement-worktree`** — produces the worktree this skill audits
- **`/make-groups`** — produces the manifest this skill accepts as `plans_input`
- **`/dry-walkthrough`** — validates plans before implementation; audit-impl validates after
