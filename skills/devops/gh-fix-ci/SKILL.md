---
name: gh-fix-ci
description: >-
  Analyze failing GitHub PR checks by inspecting GitHub Actions runs via the
  gh CLI, fetching workflow logs, extracting failure snippets, and producing
  a structured diagnosis with fix recommendations. Trigger when the user asks
  to debug CI failures, inspect red checks on a pull request, or troubleshoot
  GitHub Actions errors. Treats external CI providers (Buildkite, CircleCI)
  as out of scope and reports only their details URL.
allowed-tools:
  - Bash
  - Read
  - Write
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - analyzer
    - ci-cd
    - github-actions
    - debugging
    - devops
  provenance:
    upstream_source: "gh-fix-ci"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T14:00:00+00:00"
    generator_version: "1.0.0"
    intent_confidence: 0.52
---

# GitHub CI Fix Analyzer

Diagnose failing GitHub PR checks by inspecting Actions runs, extracting log snippets, and recommending targeted fixes.

## Overview

This skill analyzes failing CI checks on GitHub pull requests to identify root causes and guide fixes. It uses the `gh` CLI to inspect check statuses, fetch workflow run logs, and extract actionable failure snippets. The pipeline handles `gh` field drift across CLI versions, falls back to job-level log fetching when run logs are unavailable, and scopes external CI providers out of the analysis.

**What it analyzes:**
- PR check statuses (pass, fail, pending, cancelled, timed out)
- GitHub Actions workflow run logs and job-level logs
- Failure markers (error, traceback, assertion, panic, timeout, segfault)
- Run metadata (workflow name, conclusion, branch, SHA, event trigger)

**What it reports:**
- Failing check names with run URLs and log snippets
- Root cause classification (build, test, lint, timeout, infrastructure, permission)
- Fix recommendations prioritized by severity
- External check URLs (Buildkite, CircleCI) without deep inspection

## Analysis Checklist

### Prerequisites

- [ ] `gh` CLI is installed and on PATH
- [ ] `gh auth status` succeeds with `repo` and `workflow` scopes
- [ ] Working directory is inside a git repository
- [ ] PR exists (explicit number/URL or current branch has an open PR)

### Check Inspection

- [ ] Fetch all PR checks via `gh pr checks <pr> --json`
- [ ] Handle field drift: retry with available fields if primary set is rejected
- [ ] Filter to failure/error/cancelled/timed_out conclusions
- [ ] Classify each check as GitHub Actions or external provider
- [ ] For external checks, record details URL only

### Log Retrieval

- [ ] Fetch run metadata via `gh run view <run_id> --json`
- [ ] Fetch run logs via `gh run view <run_id> --log`
- [ ] Fall back to job log via `gh api /repos/{owner}/{repo}/actions/jobs/{job_id}/logs`
- [ ] Handle zip payloads from job log API (report as unavailable)
- [ ] Extract failure snippet: scan for last failure marker, take context window

### Diagnosis

- [ ] Summarize each failing check with name, URL, and log snippet
- [ ] Classify failure type (build, test, lint, timeout, infrastructure, permission)
- [ ] Identify the specific file and line when available
- [ ] Cross-reference failure with recent PR diff
- [ ] Present fix plan and wait for explicit user approval

## Metrics

### Failure Classification

| Category | Log Markers | Common Causes |
|----------|-------------|---------------|
| Build error | `error`, `fatal`, `cannot find module` | Missing dependency, syntax error, type error |
| Test failure | `FAIL`, `AssertionError`, `expected ... got` | Regression, flaky test, missing fixture |
| Lint violation | `warning`, rule codes (E501, W503) | Style drift, new linter rule |
| Timeout | `timeout`, `timed_out`, `cancelled` | Slow test, infinite loop, resource starvation |
| Infrastructure | `rate limit`, `connection refused`, `503` | Runner capacity, network issue, outage |
| Permission | `403`, `permission denied`, `EACCES` | Missing secret, token scope, file perms |

### Severity Levels

| Level | Criteria | Action |
|-------|----------|--------|
| Critical | All checks failing, merge blocked | Fix immediately |
| High | Required check failing | Fix before merge |
| Medium | Optional check failing | Fix if straightforward |
| Low | Warning-only, non-blocking | Address in follow-up |

## Workflow

### Step 1: Verify gh Authentication

```bash
gh auth status
# If unauthenticated: gh auth login (ensure repo + workflow scopes)
```

### Step 2: Resolve the Pull Request

```bash
# Current branch PR
gh pr view --json number,url
# Explicit PR
gh pr view 123 --json number,url
```

### Step 3: Run the Inspection Script

```bash
python3 "<skill-directory>/scripts/inspect_pr_checks.py" \
  --repo "." --pr "<number-or-url>"
```

Flags: `--json` (machine output), `--max-lines 200` (snippet window, default 160), `--context 40` (context lines, default 30).

Manual fallback if the script is unavailable:

```bash
gh pr checks <pr> --json name,state,conclusion,detailsUrl,startedAt,completedAt
gh run view <run_id> --json conclusion,status,workflowName,name,event,headBranch,headSha,url
gh run view <run_id> --log
```

### Step 4: Scope External Checks

If `detailsUrl` lacks `/actions/runs/`, classify the check as external. Report name and URL only. Do not fetch logs from Buildkite, CircleCI, or other providers.

### Step 5: Summarize Failures

For each failing check report: check name, workflow, run URL, failure category, log snippet, and missing-log note if applicable.

### Step 6: Draft Fix Plan

- Identify root cause file and line from log
- Cross-reference with PR diff to confirm if newly introduced
- Draft concrete fix steps per failing check
- Wait for explicit user approval before implementing

### Step 7: Implement After Approval

1. Apply the fix (edit files, update config, add dependencies)
2. Summarize changes made
3. Suggest running relevant local tests before pushing
4. Offer to open or update the PR

### Step 8: Recheck Status

```bash
python3 "<skill-directory>/scripts/inspect_pr_checks.py" --repo "." --pr "<number>"
# Or: gh pr checks <pr>
```

## Report Format

```
GitHub CI Analysis Report
=========================
PR: #123 (feature/add-auth)
Repository: org/repo

Checks: 8 total, 2 failing, 6 passing

Failing:
1. [CRITICAL] test-suite (failure)
   Workflow: CI / test-suite
   Run: https://github.com/org/repo/actions/runs/12345
   Category: Test failure
   Snippet: AssertionError: expected 200 got 401 at test_auth.py:45

2. [MEDIUM] lint (failure)
   Workflow: CI / lint
   Run: https://github.com/org/repo/actions/runs/12346
   Category: Lint violation
   Snippet: E501 line too long (120 > 88) at src/auth/handler.py:23

External (not analyzed):
- Buildkite / deploy-preview: https://buildkite.com/org/pipeline/build/456
```

## Examples

### Example 1: Failing test suite

```
User: CI is red on my PR, can you investigate?

Assistant: I will check your PR checks now.

Assistant: I will check your PR checks now.

1. Running gh auth status... authenticated
2. Running inspect_pr_checks.py --repo . --pr 789
3. Found 1 failing check:

   [HIGH] test-suite (failure)
   Workflow: CI / test-suite
   Run: https://github.com/org/repo/actions/runs/99001
   Category: Test failure
   Snippet:
     tests/test_login.py:32
     AssertionError: expected status 200 but got 403
     Fixture missing read:user OAuth scope

Root cause: The PR adds a new OAuth scope requirement but the test
fixture in tests/conftest.py still uses the old scope set.

Fix plan:
1. Update tests/conftest.py mock_oauth_scopes to include read:user
2. Re-run pytest tests/test_login.py locally to confirm

Shall I apply this fix?
```

### Example 2: External CI provider

```
User: Why is the Buildkite check failing on PR #456?
Assistant: Checking PR #456 checks...

The Buildkite check is an external provider (not GitHub Actions).
I can only report its details URL:
- deploy-preview: https://buildkite.com/org/pipeline/build/789

Open the Buildkite link directly to inspect the build logs.
GitHub Actions checks on this PR are all passing.
```

## Interpretation Guide

### gh CLI Field Drift

The `gh` CLI may change available `--json` fields between versions. The bundled script handles this automatically by parsing the "Available fields:" error message and retrying with a compatible field set. The fallback fields are: `name`, `state`, `bucket`, `link`, `startedAt`, `completedAt`, `workflow`.

### Log Retrieval Hierarchy

1. `gh run view <id> --log` -- preferred, returns the full run log
2. `gh api /repos/{owner}/{repo}/actions/jobs/{id}/logs` -- fallback for in-progress or partial runs
3. Run metadata only -- when both log sources fail, report metadata without snippet

### Failure Marker Scanning

The script scans log lines in reverse order for these markers: `error`, `fail`, `failed`, `traceback`, `exception`, `assert`, `panic`, `fatal`, `timeout`, `segmentation fault`. It returns a context window (default 30 lines) around the last match, capped at `--max-lines` (default 160).

## Notes

- Always wait for user approval before implementing fixes.
- Do not attempt to parse logs from external CI providers.
- If `gh auth` fails, guide the user through `gh auth login` with correct scopes.
- The bundled script exits non-zero when failures remain (usable in automation).
- Merge commits and bot-triggered checks may produce different failure patterns.
- For very large logs, increase `--max-lines` and `--context` to capture more context.
