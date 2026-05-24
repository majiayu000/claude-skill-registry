---
name: github-pr-fix
description: "Fix pull requests based on review feedback and CI failures. Use when: (1) Addressing PR review comments, (2) Fixing CI/test failures, (3) Resolving merge conflicts, (4) Implementing requested changes."
---

# GitHub PR Fix Skill

Automation skill for fixing pull requests based on review feedback, CI failures, and other issues.

## Purpose

This skill helps you:
1. Analyze PR review comments and CI failures
2. Fix code issues in priority order (build → test → lint)
3. Push fixes to the PR branch
4. Reply to review comments with fix status

## Prerequisites

This skill can use:
- **`ghx`** (default): Preferred for context + publish because it reduces API-shape mistakes and retry loops
- **`gh` CLI** (selective fallback): Use for simple read/one-off write operations, or when `ghx` is unavailable

## Environment & Paths

- **`GITHUB_OUTPUT_DIR`**: Where this skill writes artifacts  
  - Default: system-recommended output directory if provided by caller; otherwise a temp dir `/tmp/holon-ghprfix-*`
- **`GITHUB_CONTEXT_DIR`**: Where `ghx` writes collected data  
  - Default: `${GITHUB_OUTPUT_DIR}/github-context`
- **`GITHUB_TOKEN` / `GH_TOKEN`**: Token for GitHub operations (scopes: `repo` or `public_repo`)

## Inputs & Outputs

- **Inputs**: `${GITHUB_CONTEXT_DIR}/github/pr.json`, `review_threads.json`, `check_runs.json`, `pr.diff`, etc. (from `ghx` when available, else collected with `gh` APIs)
- **Outputs** (agent writes under `${GITHUB_OUTPUT_DIR}`):
  - `summary.md`
  - `manifest.json`
  - `publish-results.json`

## Definition of Done (Strict)

The run is successful only if all of the following are true:
1. Required code fixes are committed and pushed to the existing PR branch.
2. Publish step is executed via ghx batch publish mechanism and `${GITHUB_OUTPUT_DIR}/publish-results.json` is produced.
3. `publish-results.json` contains no failed reply action.

If replies are planned but not published, the run is not successful.

## Publishing Strategy (Token + Accuracy)

Optimize for expected total token cost across the full run (including retries/rework), not shortest immediate command count.

- Use `ghx` by default for multi-step/high-risk publish operations (`reply_review`, review posting, batch comment updates).
- `gh` is acceptable for low-risk/simple operations (single read query, single top-level comment).
- If not using `ghx` for publish, record `fallback_reason` in outputs and verify publish result explicitly.
- Avoid ad-hoc API shapes for review replies. If direct REST fallback is required, use `POST /repos/{owner}/{repo}/pulls/{pull_number}/comments` with `in_reply_to`.

### 1. Context Collection

If context is not pre-populated, collect PR context with:
- preferred: `ghx` (with diff/checks/threads/files enabled)
- fallback: `gh pr view`, `gh pr diff`, `gh api` to produce equivalent files under `${GITHUB_CONTEXT_DIR}/github/`.

### 2. Analyze PR Feedback

Read the collected context:
- `${GITHUB_CONTEXT_DIR}/github/pr.json`: PR metadata and reviews
- `${GITHUB_CONTEXT_DIR}/github/review_threads.json`: Review comments with line numbers
- `${GITHUB_CONTEXT_DIR}/github/check_runs.json`: CI check results
- `${GITHUB_CONTEXT_DIR}/github/test-failure-logs.txt`: Failed test logs
- `${GITHUB_CONTEXT_DIR}/github/pr.diff`: Code changes

Identify issues in priority order:
1. **Build errors** - Blocking, must fix first
2. **Test failures** - High priority
3. **Import/type errors** - Medium priority
4. **Lint issues** - Lower priority
5. **Refactor requests** - Non-blocking, can defer

### 3. Fix Issues

Check out the PR branch and fix issues:

```bash
# Checkout PR branch
git checkout <pr-branch>

# Make fixes
# ... fix code issues ...

# Commit changes
git add .
git commit -m "Fix: <description>"

# Push to PR branch
git push
```

**IMPORTANT**: Commit your code fixes BEFORE replying to reviews. This ensures reviewers can see your actual fixes when reading your replies.

### 4. Generate Artifacts

Create the required output files:

#### `${GITHUB_OUTPUT_DIR}/summary.md`

Human-readable summary:
- PR reference
- Issues identified
- Fixes applied
- Review responses

#### `${GITHUB_OUTPUT_DIR}/manifest.json`

Execution metadata:
```json
{
  "provider": "github-pr-fix",
  "pr_ref": "holon-run/holon#123",
  "status": "completed|partial|failed",
  "fixes_applied": 5,
  "reviews_replied": 3,
  "fallback_reason": ""
}
```

### 5. Reply to Reviews

Publish review replies via ghx batch publish mechanism. `github-pr-fix` should describe reply requirements in natural-language/structured planning, then follow ghx documentation to build the publish request and execute batch publish.

Implementation guidance:
- default: use `ghx.sh intent run --intent=...` as documented by ghx
- fallback: use `gh api` only when needed, and synthesize `${GITHUB_OUTPUT_DIR}/publish-results.json` with equivalent per-action status

After publish, ensure `${GITHUB_OUTPUT_DIR}/publish-results.json` exists and check for failed reply actions.

## Output Contract

### Required Outputs

1. **`${GITHUB_OUTPUT_DIR}/summary.md`**: Human-readable summary
   - PR reference and description
   - Issues identified
   - Fixes applied
   - Review responses

2. **`${GITHUB_OUTPUT_DIR}/manifest.json`**: Execution metadata

3. **`${GITHUB_OUTPUT_DIR}/publish-results.json`**: Publishing execution result

## Git Operations

You are responsible for all git operations:

```bash
# Checkout PR branch
git checkout <pr-branch>

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Fix: <description>"

# Push to PR branch (NOT a new branch)
git push
```

**Note**: Push changes to the existing PR branch, do NOT create a new PR.

## Important Notes

- You are running **HEADLESSLY** - do not wait for user input or confirmation
- Fix issues in priority order: build → test → import → lint
- Commit fixes BEFORE replying to reviews
- Prefer `ghx` for publish when available; use `gh` fallback selectively and document `fallback_reason`
- Verify publish-results and fail when any reply action fails
- For non-blocking refactor requests, consider deferring to follow-up issues

## Reference Documentation

- **[pr-fix-workflow.md](references/pr-fix-workflow.md)**: Complete workflow guide
  - Error triage and priority order
  - Environment setup and verification
  - Test failure diagnosis
  - Handling refactor requests
  - Posting review replies

- **[diagnostics.md](references/diagnostics.md)**: Diagnostic confidence levels
  - Confidence levels for CI failure diagnosis
  - Common contract rules
