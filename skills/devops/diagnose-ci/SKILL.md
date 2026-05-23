---
name: diagnose-ci
categories: [ci]
---

# diagnose-ci Skill

Fetch CI logs for a failing branch, classify the failure type, and write a structured
diagnosis report to `temp/diagnose-ci/`. Called by the orchestrator on `ci_watch` failure
before routing to `resolve-failures`.

## Invocation

```
/autoskillit:diagnose-ci {branch} [run_id] [ci_failed_jobs] [workflow]
```

**Positional args:**
- `branch` — the git branch whose CI run to investigate
- `run_id` (optional) — specific workflow run ID; if absent, discover from `gh run list`
- `ci_failed_jobs` (optional) — JSON array of failed job names from `wait_for_ci`, used to scope log fetching
- `workflow` (optional) — workflow filename (e.g. `tests.yml`); if provided, scopes `gh run list` to that workflow only; use `-` to skip

## Critical Constraints

**NEVER:**
- Modify any source code files
- Run the test suite
- Write files outside `temp/diagnose-ci/`
- Block on missing `gh` CLI — write a minimal `failure_type=unknown` diagnosis instead

**ALWAYS:**
- Initialize code-index: call `set_project_path` to current cwd before any search
- Write the diagnosis file before emitting output tokens
- Emit the three output tokens (`diagnosis_path`, `failure_type`, `is_fixable`) at the end of the response on their own lines

## Workflow

### Step 1: Initialize Code Index

```
mcp__code-index__set_project_path(path=<cwd>)
```

### Step 2: Discover Run ID (if not provided)

If `run_id` is not provided as an argument (or is `-`):
```bash
gh run list --branch {branch} --limit 1 --json databaseId,status,conclusion
```
If `workflow` is provided and is not `-`:
```bash
gh run list --branch {branch} --workflow {workflow} --limit 1 --json databaseId,status,conclusion
```
Parse the JSON to extract `databaseId` as `run_id`.

If `gh` is unavailable or the command fails, skip to Step 5 (write minimal diagnosis).

### Step 3: Fetch Failure Summary

```bash
gh run view {run_id} --log-failed
```
Capture the output (stdout). This is the primary failure log.

### Step 4: Fetch Per-Job Logs

For each failing job in `ci_failed_jobs` (or all failed jobs from `gh run view` if not provided):
```bash
gh api repos/{owner}/{repo}/actions/runs/{run_id}/jobs
```
For each failed job, fetch last 200 lines of logs via:
```bash
gh api repos/{owner}/{repo}/actions/jobs/{job_id}/logs
```

Use `gh repo view --json nameWithOwner` to resolve `{owner}/{repo}` if needed.

### Step 5: Classify Failure

Analyze the log output to classify `failure_type` as one of:
- `test` — pytest/jest/unit test failures
- `lint` — ruff, flake8, eslint, or formatting failures
- `build` — compilation or build errors
- `type_check` — mypy, pyright, or TypeScript type errors
- `env` — missing environment variables, secrets, or infrastructure issues
- `unknown` — cannot determine from logs

Determine `is_fixable`:
- `true` for `test`, `lint`, `build`, `type_check`
- `false` for `env`, `unknown`

### Step 6: Write Diagnosis Report

Create directory `temp/diagnose-ci/` if it doesn't exist. Write the diagnosis file:

```markdown
# CI Diagnosis: {branch}

**Run ID:** {run_id}
**Failure Type:** {failure_type}
**Is Fixable:** {is_fixable}
**Branch:** {branch}

## Log Excerpt

```
{first 200 lines of failure log}
```

## Recommended Fix Approach

{1-3 sentences describing how resolve-failures should approach this}
```

Save to `temp/diagnose-ci/diagnosis_{timestamp}.md`. (relative to the current working directory)

### Step 7: Emit Output Tokens

Emit these tokens on their own lines at the end of your response:

```
diagnosis_path = /absolute/path/to/temp/diagnose-ci/diagnosis_{timestamp}.md
failure_type = test|lint|build|type_check|env|unknown
is_fixable = true|false
```

## gh Unavailable Fallback

If `gh` is unavailable at any step, write a minimal diagnosis:
- `failure_type=unknown`
- `is_fixable=false`
- Diagnosis body: "gh CLI unavailable — logs could not be fetched. Manual inspection required."

Then emit the output tokens and exit.