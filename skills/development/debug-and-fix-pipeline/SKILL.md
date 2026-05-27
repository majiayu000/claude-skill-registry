---
name: debug-and-fix-pipeline
description: "Diagnose a failed Bauplan job, pin the exact data state, collect evidence, apply a minimal fix, and rerun. Evidence first, changes second."
allowed-tools:
  - Bash(bauplan:*)
  - Bash(git)
  - Read
  - Write
  - Glob
  - Grep
  - WebFetch(domain:docs.bauplanlabs.com)
---

# Debug and Fix Pipeline

## What This Skill Does

A Bauplan pipeline job has failed. This skill walks through a structured diagnosis and repair: pin the exact state that caused the failure, collect evidence, find the root cause, apply a minimal fix, and confirm the fix works.

The core principle is **evidence first, changes second** — never guess at a fix before understanding what broke and why.

## When to Use This Skill

Use this when:

- A `bauplan run` has failed and you need to understand why
- You have a failed job ID, a branch name with a broken run, or a time window to search for failures
- You want to fix the pipeline and verify the fix against the exact data state that caused the failure

## What You'll Need

At least one of:

- A Bauplan **job ID** (preferred)
- A Bauplan **branch name** where the failure happened
- A **time window** to search for failed jobs
- A **local path** to the pipeline project directory

If none are provided, the skill will try to infer from context. If ambiguous, it will ask.

## Workflow at a Glance

```
Step 0  Setup
        Confirm Bauplan connectivity, check for Git, create output directories.

Step 1  Pin the failing state
        Extract the branch, commit hash, and error message from the failed job.
        → Write job report

Step 2  Create a debug branch
        Branch from the exact failing ref so you see the same data the job saw.

Step 3  Collect evidence and find root cause
        Inspect schemas, sample data, and trace upstream until you find
        the model whose inputs are clean but whose output is broken.
        → Write data snapshot reports as you go

Step 4  Apply a minimal fix
        Create a Git debug branch, make the smallest change that addresses
        the root cause. One logical change per commit.

Step 5  Rerun and verify
        Re-execute the pipeline on the debug branch and confirm the fix works.
        → Write summary report
```

The skill produces three types of reports in `debug/`: a job report, data snapshots, and a final summary. These are the deliverables — they document what happened, what was found, and what was changed.

---

## Hard Rules

1. **NEVER touch `main`** — not in Bauplan, not in Git.
2. **NEVER change code without Git** — every edit lives on a Git debug branch with a commit. The Git branch is created in Step 4 when fixes begin, not during investigation.
3. **NEVER query a moving ref** — always target `branch@commit_hash` or a tag.
4. **NEVER rerun before inspecting** — understand the failure, then act.
5. **NEVER clean up debug branches** unless the user explicitly asks.
6. **NEVER guess CLI flags.** Before running any `bauplan` CLI command, verify the exact flag names against the CLI reference doc in the project. If unsure about a flag, check first.
7. **NEVER create files outside `debug/` and the pipeline project directory.** No top-level documentation, no READMEs, no schema guides. Your outputs are: the `debug/` report files and edits to existing pipeline code. Nothing else.
8. **NEVER write Python scripts for diagnosis.** Steps 0–3 (evidence collection and root cause analysis) use `bauplan` CLI commands exclusively. The only Python you write is pipeline code fixes (models, project config).
9. **NEVER branch from the current checkout or a previous debug session.** The debug branch must be created from the failing job's own ref (`job_branch@job_commit` from Step 1). If you branch from anywhere else, you will investigate the wrong data and reach wrong conclusions.

Common CLI flag mistakes to avoid:
- ❌ `--format json` → ✅ `--output json` (or `-o json`)
- ❌ `--branch` on read commands → ✅ `--ref` (use `--branch` only for write operations like `create`, `delete`)
- ❌ `--id` on `job get` → ✅ positional argument: `bauplan job get <JOB_ID>`

If any rule cannot be satisfied, **STOP** and report the blocker.

---

## Detailed Steps

### Step 0 — Setup

**Bauplan:** Run `bauplan info` to confirm connectivity and get your username (needed for branch naming in Step 2). Do not create any branches yet.

**Git:** Check whether `.git` exists. Note the result — you will need it in Step 4 when code changes begin. Do not create any Git branches yet.

**Create output directories:**
```bash
mkdir -p debug/{job,data_snapshot}
```

### Step 1 — Pin the Failing State

**Goal:** Extract three things from the failing job: the **branch** it ran on, the **commit hash** representing the data state, and the **raw error message**. Use CLI commands only — do not write scripts.

- If you have a **job id**:
  ```bash
  bauplan job get <job_id>
  bauplan job logs <job_id>
  ```
  From the output, extract:
  1. The **branch** the job ran against (e.g., `ciro.debug_2d87c900`)
  2. The **commit hash** on that branch at the time of the run
  3. The **error message** (copy verbatim — you will analyze it in Step 3)

- If `job get` does not show the commit hash directly, find it by listing commits on the job's branch:
  ```bash
  bauplan commit --ref <job_branch> --limit 10
  ```
  Match by timestamp against the job's created/finished time → extract `commit_hash`.

- If you need to find the job first:
  ```bash
  bauplan job ls --status fail --limit 10
  ```
  Identify the matching job, then `bauplan job get <job_id>`.

- Fall back to asking the user if neither approach yields a concrete hash.

End this step with three values:
- `job_branch`: the branch the failing job ran on
- `job_commit`: the commit hash on that branch (or a clear statement that the data state cannot be pinned)
- `raw_error`: the verbatim error message from the logs

**⏸ WRITE REPORT NOW:** Before proceeding, write `debug/job/<job_id>.md` using the Job Report template. The user needs something to read while you continue working. Do not defer this.

### Step 2 — Create Bauplan Debug Branch

**CRITICAL:** The debug branch must be created from the **failing job's own ref** — the `job_branch@job_commit` you extracted in Step 1. Do NOT branch from whatever happens to be checked out, from a previous debug session, or from `main`. The point of branching from the failing ref is to see the exact data state the job saw when it failed.

```bash
bauplan branch create <username>.debug_<job_id_short> --from-ref <job_branch>@<job_commit>
bauplan checkout <username>.debug_<job_id_short>
```

If `job_commit` could not be pinned in Step 1, branch from `job_branch` (without a hash). Note in the job report that the data ref is approximate.

### Step 3 — Collect Evidence and Locate the Root Cause

Do this **before any fixes**.

#### Code assumption

**Assume the code in the current repository is what ran at the time of failure.** It is the user's responsibility to ensure they are on the correct Git commit before invoking this skill. Read the pipeline code in place (`models.py`, `.sql` files, `expectations.py`, `bauplan_project.yml`) to understand the DAG structure.

#### 3A — Identify failing models

A pipeline run can fail in **one or more models**. Using the raw error from Step 1 and the pipeline code, identify every model that errored — not just the first one. For each, note:
- The **model name** (function name or SQL filename)
- The **file** it lives in
- What the error message means in the context of that model's logic

Do not re-run `bauplan job get` or `bauplan job logs` — you already have the error from Step 1.

#### 3B — Collect data evidence

Start from the failing model(s) and work outward. For each failing model, inspect:

1. **Its inputs** — every table it reads from (its `bauplan.Model(...)` references)
2. **Its output** — the table it produces (function name or SQL filename)

If the DAG is unclear from code:
```bash
bauplan table ls --ref <pinned_ref>
```

**Query guardrails:** All sample queries must use `LIMIT 20`. All profiling queries (counts, stats) must use `LIMIT 1`. Never run unbounded queries.

For each table, run against the pinned ref:

```bash
# Schema
bauplan table get <ns>.<table> --ref <pinned_ref>

# Row count
bauplan query --ref <pinned_ref> "SELECT COUNT(*) as n FROM <ns>.<table>"

# Sample (20 rows)
bauplan query --ref <pinned_ref> --max-rows 20 "SELECT * FROM <ns>.<table> LIMIT 20"

# Basic stats per column
bauplan query --ref <pinned_ref> "SELECT MIN(<col>), MAX(<col>), COUNT(*) - COUNT(<col>) as nulls FROM <ns>.<table>"
```

**⏸ WRITE REPORT as you go:** Write `debug/data_snapshot/<table>.md` immediately after collecting evidence for each table (using the Data Report template). Do not wait until all tables are inspected.

#### 3C — Trace upstream if needed

The model that errors is not necessarily the model with the bug. After collecting evidence for a failing model's inputs, check:

- If an **input table** has anomalies (unexpected nulls, wrong types, schema drift), the root cause is likely **upstream**. Identify which model produced the bad input, collect evidence for *its* inputs, and repeat.
- Keep tracing upward until you find a model whose **inputs are clean but whose output is broken**. That is the model to fix.

There is no fixed scope limit — follow the evidence as far upstream as it leads. But collect evidence for each new table as you go (query + write report).

#### 3D — Classify and conclude

Based on everything collected, determine:

**Classification** — one of:
- **Planning/compilation** — DAG or schema error before execution
- **Runtime** — crash, timeout, dependency issue during execution
- **Expectation** — data quality check failed
- **Logical correctness** — runs clean but produces wrong results

**Model to fix** — the model whose inputs are clean but whose output (or behavior) is broken. This may or may not be the model that errored.

If you cannot localize the failure using the collected evidence, stop and report.

### Step 4 — Apply a Minimal Fix

#### Git setup (first time only)

Code changes require version control. Before editing any files:

- **Git available and not on `main`:** Create a debug branch:
  ```bash
  git checkout -b debug/bpln_<job_id_short>
  ```
  If the working tree is dirty, commit a snapshot checkpoint first so the pre-fix state is preserved.

- **Git available but on `main`:** Create the debug branch from `main`, which moves you off it:
  ```bash
  git checkout -b debug/bpln_<job_id_short>
  ```

- **No Git repo:** Note code provenance as "unversioned" in the summary report. Fixes will go through `code_run` instead of local commits.

#### Fix priority

Prefer fixes closest to the data contract boundary, because contract-level issues propagate furthest and are cheapest to verify:

1. **Schema corrections** — wrong column types, missing columns, mismatched output declarations
2. **Input tightening** — add or fix `filter` / `columns` in `bauplan.Model()` to reject bad data earlier
3. **Expectation fixes** — fix existing expectations that are misconfigured or too strict/lenient
4. **Transform logic** — change the model's computation only if the above three don't resolve it

Rules:
- One logical change per commit. No refactors.
- Commit message must include the Bauplan job id.

Never amend or squash during debugging.

### Step 5 — Rerun and Verify

#### Determinism check

Before rerunning, assess what you can actually prove:

| Condition                      | Status |
|--------------------------------|--------|
| Data ref pinned to commit hash | ✅ or ❌ |
| Git SHA pinned for code        | ✅ or ❌ |

- **Both pinned** → rerun is **deterministic**. A green result proves the fix works against the exact failing state.
- **One or both unpinned** → rerun is **best-effort**. A green result is encouraging but not conclusive. State this explicitly.

#### Execute

```bash
# Preferred: strict mode, from the debug branch
bauplan run --project-dir <dir> --ref <debug_branch> --strict on

# Fallback: dry run first, then full run
bauplan run --project-dir <dir> --ref <debug_branch> --dry-run --strict on
bauplan run --project-dir <dir> --ref <debug_branch> --strict on
```

After a green run: if Step 3 queries revealed data anomalies (e.g., wrong types, unexpected nulls), re-execute those queries to confirm the anomalies are resolved. Record before vs. after evidence.

**⏸ WRITE REPORT NOW:** Write `debug/summary.md` using the Summary template. This is the final deliverable — the single document that explains what happened, what changed, and what was verified. YOU MUST INCLUDE THE FULL HASH FOR REPRODUCIBILITY - DO NOT SHORTEN THE COMMIT HASH.

---

## Report Templates

Three report files, written at specific points in the workflow (marked with ⏸ above). Use these templates exactly.

### Report 1: Job Report → `debug/job/<job_id>.md`

Write this after Step 1 (pinning the failing state). This is a factual record of what the job reported — no analysis.

```markdown
# Job Report: <job_id>

## Metadata
- **Job ID**: <job_id>
- **Status**: Failed
- **Kind**: <kind from job get>
- **User**: <user>
- **Created**: <timestamp>
- **Finished**: <timestamp>
- **Job Branch** (branch the job ran on): <job_branch>
- **Job Commit** (data state at time of failure): <job_commit or "not pinned — approximate">

## Error
<Full error message from job logs, verbatim. Do not interpret — just paste.>
```

### Report 2: Data Report → `debug/data_snapshot/<table>.md` (one per table)

Write these during Step 3. One file per table inspected.

```markdown
# Data Evidence: <namespace>.<table>

## Role in Failure
<How this table relates to the failure, e.g.
"direct input to failing model X", "output of failing model X", "upstream producer of bad input to Y">

## Schema
<Paste output of bauplan table get>

## Row Count
<number>

## Sample (20 rows)
<Paste query output>

## Anomalies
<Specific findings tied to the failure. If none, say "No anomalies detected.">
```

### Report 3: Summary → `debug/summary.md`

Write this last, after the fix is applied and the rerun completes. This is the single document someone reads to understand what happened and what changed.

```markdown
# Debug Summary

## Job
<job_id> — failed on <job_branch> at <timestamp>
Pinned ref: <job_branch>@<job_commit>
Bauplan debug branch: <debug_branch> (created from pinned ref)
Git debug branch: <git_branch or "unversioned">

## Failing Model(s)
<For each model that errored, list name and file>

## Root Cause Model
- **Model**: <the model whose inputs are clean but whose output/behavior is broken — may differ from the erroring model(s)>
- **File**: <path>
- **Classification**: <planning/compilation, runtime, expectation, or logical correctness>

## What broke
<One sentence: what the error was>

## Why it broke
<One sentence: the root cause, based on evidence from data snapshots>

## What was fixed
<List each commit with one-line description>

## Determinism
<"Deterministic" or "Best-effort" — cite which conditions were met>

## Rerun result
<"Green" or "Failed — <reason>">
```

Do not produce any other files. The fix itself lives in Git commits to pipeline code. The reports live in `debug/`. That is the complete output.
