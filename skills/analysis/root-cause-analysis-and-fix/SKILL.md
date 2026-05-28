---
name: root-cause-analysis-and-fix
description: “Inspect a failed Bauplan pipeline run on a dev branch, reconstruct the frozen data state, collect evidence, propose a minimal code fix using Git, and rerun deterministically where possible.”
allowed-tools:
	•	Bash(bauplan:*)
	•	Bash(git)
	•	Read
	•	Write
	•	Glob
	•	Grep
	•	WebFetch(domain:docs.bauplanlabs.com)
---

# Root Cause Analysis and Fix (Data + Code)

This skill is for debugging failed Bauplan runs. It assumes a failure has already occurred and prioritizes evidence collection before any change.
Data state is controlled by Bauplan data refs. Code state is controlled by Git. Both must be treated explicitly.

## CRITICAL RULES
	1.	NEVER run or write anything on main (Bauplan or Git).
	2.	NEVER change code without Git version control.
	3.	NEVER inspect data on a moving ref. All queries must target an explicit ref (branch@[commit_hash] or tag).
	4.	NEVER rerun blindly. Always inspect the frozen failing state first.
	5.	Keep debug branches open until the issue is understood. Do not clean up unless explicitly asked by the user.

If any rule cannot be satisfied, STOP and REPORT the blocker.

## Required Inputs

You need at least one of the following:
	•	Bauplan job id (preferred)
	•	Bauplan branch name
	•	Time window to locate failed jobs
	•	Local path to the working directory with the failing code.

If none are provided:
	•	Infer from context (recent commands, repo config).
	•	Verify using Bauplan info and local Git inspection.
	•	If inference is ambiguous, ask the user to clarify.


## Step 0: Establish safety boundaries (Bauplan and Git)

### 0A. Confirm you are not on Bauplan main

```bash
bauplan info
```

If the active branch is main, STOP and create a dev branch:

```bash
bauplan checkout -branch <username>.debug_<short_name>
```

DO NOT proceed without a Bauplan debug branch.

### 0B. Confirm Git prerequisites

Before touching code, verify:
	•	.git directory exists.
	•	Git is installed and usable.
	•	You are not on main or a protected branch.
	•	Claude Code can run Git commands locally.
	•	If pushing or opening a PR is required, remote credentials are configured.

If any prerequisite is missing:
	•	Do not modify code.
	•	Record the missing prerequisite as a blocker.
	•	Proceed only with evidence collection.

## Step 1: Identify the frozen data ref for the failed job

**Goal:** obtain a commit hash from Bauplan representing the exact data state used by the failed run.

### 1A. If you have a job id
	•	Fetch job metadata (status, timestamps, ref at start).
	•	Fetch full job logs.
	•	Extract any commit properties associated with the job (if any).

### 1B. Map job to a commit hash

Approach:
	•	Start from the branch the job ran against.
	•	List recent commits and locate the one whose metadata references the job id.
	•	Extract commit_hash.

If mapping is not possible:
	•	Fall back to “ref at start” from job metadata, if available.
	•	Otherwise, ask the user for a commit hash.

**You must end this step with either:
	•	a concrete commit hash, or
	•	an explicit statement that the data state cannot be reliably pinned.**

## Step 2: Create a Bauplan debug branch from the failing ref

Create a new branch from the pinned failing ref, not from main.

Use ref syntax: `<source_branch>@<commit_hash>`

Example:

from_ref = "dev@abc123"
debug branch = "<username>.debug_<job_id_or_short_hash>"

Record in debug/job/<job_id>.md:
	•	source branch
	•	commit hash
	•	debug branch name
	•	exact `from_ref` used

## Step 3: Establish Git code provenance

Bauplan currently does not provide code snapshots. Code reproducibility is handled exclusively by Git.

### 3A. Determine whether code is pinned

Attempt to identify the Git commit that produced the failing run:
	•	Look for a Git SHA in:
	•	CI logs
	•	orchestrator metadata
	•	job annotations
	•	commit messages
	•	If found, check out that SHA locally.

If no Git SHA can be identified:
	•	Mark code as not pinned.
	•	Proceed with caution.
	•	All conclusions must be labeled conditional.

### 3B. Create a Git debug branch

Create or switch to a Git branch dedicated to this debug session.

Naming convention:

debug/bpln_<job_id_or_short_hash>

If the working tree is dirty:
	•	Commit a snapshot checkpoint before applying fixes.
	•	This represents the assumed failing code state.

Record in debug/job/<job_id>.md:
	•	git_base_sha (or unknown)
	•	git_debug_branch

## Step 4: Collect evidence (before any fixes)

### 4A. Code evidence
**Goal:** obtain all the information about the code that ran at the time of failure. Given the declarative nature of Bauplan, this will include the declaration of infrastructure (i.e. the decorator `@bauplan.python()`)

Collect:
	•	Entrypoint that triggered the run
	•	Transformation code executed (SQL, Python models, expectations)
	•	Declared contracts (schemas, expectations, materialization)

Snapshot into `debug/code_snapshot/.`

State explicitly:
	•	whether code is pinned to a Git SHA
	•	or whether it reflects current working code

### 4B. Execution evidence (logs)
**Goal:** obtain all the information about the execution environment of the failing job (i.e. server responses, dependencies, containers, traceback errors etc.)

From the job:
	•	Full error message
	•	Failing model or step
	•	Runtime context (Python version, dependencies, limits)

Summarize strictly from the API responses and the logs. Avoid speculation and interpretation.

### 4C. Data evidence at the pinned ref
**Goal:** establish the status of the data assets that either affected the failed job (e.g. input upstream tables or data sources) or were affected by the failing job (e.g. resulting downstream tables or updates).

All queries must run against the pinned ref or tag.
For each relevant table:
	•	schema
	•	row count
	•	small sample (10–20 rows)
	•	targeted anomaly query tied to the failure
    •   quick stats (max/min values, general statistics, etc)

Write one file per table in `debug/data_snapshot/<table>.md.`

### Step 5: Localize the failure

Classify the failure based on evidence only:
	•	Planning or compilation failure
	•	Runtime failure
	•	Expectation failure
	•	Logical correctness failure

If you cannot produce a minimal reproducer query on the pinned ref, the failure is not localized. Stop and report that limitation.


### Step 6: Apply a minimal fix (Git only)

Rules:
	•	One logical change per iteration.
	•	No refactors.
	•	Prefer schema corrections, input tightening, or expectation fixes.

Workflow:
	1.	Edit code on the Git debug branch.
	2.	Review diff.
	3.	Commit the change.

Commit message must include the Bauplan job id.

Record every fix in debug/fix_log.md:
	•	file changed
	•	diff summary
	•	why this change addresses the evidence

Never amend or squash during debugging.


### Step 7: Rerun deterministically where possible

Rerun on the Bauplan debug branch created from the pinned ref.

If supported, use:
	•	rerun(job_id, ref=...)

Otherwise:
	•	dry run first
	•	then full run with strict mode preserved

Determinism conditions:
	•	Data ref pinned
	•	Git SHA pinned

If Git SHA is unknown, label the rerun as best effort.

After a green run:
	•	Re-execute the queries that previously demonstrated failure.
	•	Record before vs after evidence.


## Output Contract

You must produce:
	1.	debug/job/<job_id>.md
	•	job metadata
	•	pinned data commit hash
	•	git_base_sha (or unknown)
	2.	debug/code_snapshot/
	•	with an explicit statement on code pinning
	3.	debug/data_snapshot/
	•	evidence from the pinned ref
	4.	debug/fix_log.md
	•	minimal fix history
	5.	Either:
	•	a successful rerun on the debug branch, or
	•	a single, concrete external blocker stated plainly


If you want next, I can:
	•	Strip this down into a “compact agent version”.
	•	Add a strict decision tree that prevents Claude from touching code prematurely.
	•	Align this 1:1 with how you want to document Bauplan + Claude workflows publicly.