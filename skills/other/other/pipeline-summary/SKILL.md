---
name: pipeline-summary
categories: [github]
description: Create a GitHub issue and PR summarizing pipeline bugs and fixes. Use when a pipeline run completes with accumulated bug fixes on a feature branch.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '[SKILL: pipeline-summary] Creating pipeline run summary (issue + PR)...'"
          once: true
---

# Pipeline Summary

Create a GitHub issue documenting bugs encountered during a pipeline run
and a PR from the feature branch into the target branch.

## Arguments

`/autoskillit:pipeline-summary {bug_report_path} {feature_branch} {target_branch} {workspace} [{token_summary_path}] [{closing_issue}]`

- **bug_report_path** — Path to the JSON file containing bug metadata
- **feature_branch** — Name of the branch containing all accumulated fixes
- **target_branch** — Branch to create the PR against (e.g., "main")
- **workspace** — Path to the git repository workspace
- **token_summary_path** — (Optional) Path to a JSON file with token/timing data written by the orchestrator. When absent or the file does not exist, the skill operates exactly as today with no token table in the PR body.
- **closing_issue** — (Optional) GitHub issue number whose `## Requirements` section should be extracted and embedded in the PR body. When absent or empty, requirements extraction is skipped.

## When to Use

- End of a pipeline run with `collect_on_branch` enabled
- Any pipeline that accumulates fixes on a feature branch and needs a summary

## Critical Constraints

**NEVER:**
- Fail the pipeline if `gh` is not available or not authenticated — write a local summary instead
- Create empty issues or PRs (skip if no bugs to report)
- Modify any source code — this skill only creates GitHub artifacts and a summary file

**ALWAYS:**
- Check `gh auth status` before attempting GitHub operations
- Push the feature branch before creating the PR
- Write a local summary markdown file regardless of GitHub availability
- Output `summary_path=<path>` for capture by the orchestrator
- If GitHub operations succeed, also output `issue_url=<url>` and `pr_url=<url>`

## Workflow

### Step 1: Parse Arguments
Parse up to six positional arguments from the prompt. The fifth (`token_summary_path`) and sixth (`closing_issue`) are optional.

### Step 2: Read Bug Report
Read the JSON file at `{bug_report_path}`. Expected structure:
```json
[
  {
    "step": "string — pipeline step where failure occurred",
    "error": "string — error description",
    "fix": "string — what was done to fix it",
    "iteration": "number — which bugfix iteration"
  }
]
```
If the file is empty, contains `[]`, or doesn't exist, write a clean-run summary and exit successfully.

### Step 3: Write Local Summary
Write a markdown summary to `{workspace}/run-summary.md`:
- Title: "Pipeline Run Summary — {date}"
- Bug count and fix count
- Table of all bugs with step, error, fix, iteration
- Branch info: feature branch name, target branch

Output: `summary_path={workspace}/run-summary.md`

### Step 3b: Append Token+Timing Table (if token_summary_path provided)

If `token_summary_path` was provided as a fifth argument and the file exists, read it as JSON. The JSON has the structure:

```json
{
  "steps": [
    {
      "step_name": "string",
      "input_tokens": 0,
      "output_tokens": 0,
      "cache_creation_input_tokens": 0,
      "cache_read_input_tokens": 0,
      "invocation_count": 0,
      "elapsed_seconds": 0.0
    }
  ],
  "total": {
    "input_tokens": 0,
    "output_tokens": 0,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
    "total_elapsed_seconds": 0.0
  }
}
```

Append the following two markdown sections to `run-summary.md`:

```markdown
## Token Usage

| Step | Input | Output | Cache Write | Cache Read | Calls | Elapsed (s) |
|------|-------|--------|-------------|------------|-------|-------------|
| {step_name} | {input_tokens} | {output_tokens} | {cache_creation_input_tokens} | {cache_read_input_tokens} | {invocation_count} | {elapsed_seconds:.1f} |
| **Total** | {total.input_tokens} | {total.output_tokens} | {total.cache_creation_input_tokens} | {total.cache_read_input_tokens} | — | {total.total_elapsed_seconds:.1f} |
```

If `token_summary_path` is absent or the file does not exist, skip this step — no token table is added.

### Step 4: Check GitHub Availability
Run `gh auth status 2>/dev/null`. If exit code is non-zero or `gh` is not found:
- Log "GitHub CLI not available or not authenticated — skipping issue/PR creation"
- Exit successfully (the local summary is sufficient)

### Step 5: Push Feature Branch
```bash
cd {workspace}
git push -u origin {feature_branch}
```
If push fails (no remote, network issue), log the error and exit successfully.

### Step 5b: Fetch Requirements from Closing Issue (if closing_issue known)

- If `closing_issue` was provided as the sixth argument:
  ```bash
  gh issue view {closing_issue} --json body -q .body
  ```
  Extract the `## Requirements` section: `requirements_section` = everything from `## Requirements` to the next `## ` heading or end of body, whichever comes first.
- If gh auth is unavailable or `closing_issue` is not provided: skip gracefully — `requirements_section = ""`.

### Step 6: Create GitHub Issue
Write the issue body to a temp file, then:
```bash
TEMP_ISSUE_BODY="temp/pipeline-summary/issue_body_$(date +%Y%m%d-%H%M%S).md"
mkdir -p "$(dirname "${TEMP_ISSUE_BODY}")"
# [write the issue body content to ${TEMP_ISSUE_BODY} here]
gh issue create \
  --title "Pipeline Run Summary — {date}: {bug_count} bug(s) fixed" \
  --body-file "${TEMP_ISSUE_BODY}" \
  --label "pipeline-summary"
```
Capture the issue URL from stdout. If the label doesn't exist, retry without `--label`.

Output: `issue_url={url}`

### Step 7: Create Pull Request
Write the PR body to a temp file (reference the issue), then:
```bash
TEMP_PR_BODY="temp/pipeline-summary/pr_body_$(date +%Y%m%d-%H%M%S).md"
mkdir -p "$(dirname "${TEMP_PR_BODY}")"
# [write the PR body content to ${TEMP_PR_BODY} here]
gh pr create \
  --title "Pipeline fixes — {date}" \
  --body-file "${TEMP_PR_BODY}" \
  --base {target_branch} \
  --head {feature_branch}
```
The PR body (`temp_pr_body`) contains:
- `## Summary` — bug count and branch info
- `## Requirements` (if `requirements_section` is non-empty from Step 5b)
- `Closes #{closing_issue}` (if closing_issue was provided)
- Bug table from Step 3
- Token/timing table from Step 3b (if available)

Capture the PR URL from stdout.

Output: `pr_url={url}`

## Output
- Always: `summary_path={workspace}/run-summary.md`
- If GitHub available: `issue_url={url}` and `pr_url={url}`

## Orchestrator Calling Convention

For recipe authors who want to include token/timing data in the PR body:

1. Call the `get_token_summary` MCP tool to retrieve current pipeline token data.
2. Write the JSON result to `temp/token_summary_{timestamp}.json` using a `run_python` step. (relative to the current working directory)
   The `run_python` step executes in the MCP server process and has access to the live
   `ToolContext` via the server context; call `ctx.token_log.get_report()` and
   `ctx.token_log.compute_total()`, then write `{"steps": ..., "total": ...}` as JSON.
   Capture the output path via `print(f"token_summary_path={out}")`.
3. Pass the file path as the fifth positional argument to `run_skill pipeline-summary`.

> Note: The headless session for `pipeline-summary` runs in a separate process with its own
> (empty) token log, which is why the file-based handoff is required. `run_python` steps share
> the live in-process token log with the MCP server, so they can access accumulated timing data
> directly without a network call.