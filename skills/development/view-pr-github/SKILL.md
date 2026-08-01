---
name: view-pr-github
description: View GitHub PR status/details (prefer GitHub chat tools; gh is fallback).
---

---
name: view-pr-github
description: View GitHub PR status/details (prefer GitHub chat tools; gh is fallback).
compatibility: Preferred: GitHub chat tools configured for the repo. Fallback: GitHub CLI (gh) authenticated, plus network access.
---

# View PR (GitHub)

## Purpose
Read pull request status/details from GitHub.

Preferred: use GitHub chat tools (stable, structured, avoids pager/editor pitfalls).
Fallback: use non-interactive `gh` patterns.

Use this skill for **read-only PR inspection** (status, checks, reviewers, files, body). For creating/merging PRs, prefer the repo wrapper scripts (see the `create-pr-github` skill).

## Prefer GitHub Chat Tools (When Available)

If GitHub chat tools are available in the current session, prefer them for read-only inspection to reduce terminal approvals and avoid pager issues. Typical tool coverage:

- PR details: `mcp_github_get_pull_request`
- Changed files: `mcp_github_get_pull_request_files`
- Inline review comments: `mcp_github_get_pull_request_comments`
- Reviews: `mcp_github_get_pull_request_reviews`
- Status checks: `mcp_github_get_pull_request_status`

Use the `gh` CLI patterns below only when there is no matching chat tool (or you need `gh api` flexibility).

## Hard Rules
### Must
- Prefer GitHub chat tools when they can answer the question.
- If using `gh`, use a **non-interactive pager** for every `gh` call:
  - Prefer `GH_PAGER=cat` (gh-specific, overrides gh’s internal pager logic)
  - Also set `GH_FORCE_TTY=false` to reduce TTY-driven behavior
  - Prefer structured output (`--json`) and keep output small with `--jq` when practical.

### Must Not
- Run plain `gh ...` without `GH_PAGER=cat` (it may open `less` and block).
- Change global GitHub CLI config (no `gh config set ...`).

## Patterns

### Preferred: GitHub Chat Tools
Use chat tools for:
- PR details/metadata
- changed files
- reviews
- status checks
- conversation comments and inline review comments

If a tool exists that directly answers the question, use it. If not, use the `gh` fallback patterns below.

### Fallback: Minimal Safe Prefix
Use this prefix for every command:

```bash
GH_PAGER=cat GH_FORCE_TTY=false gh ...
```

### 1) View PR Summary (safe JSON)

```bash
GH_PAGER=cat GH_FORCE_TTY=false gh pr view <pr-number> \
  --json number,title,state,isDraft,url,mergeStateStatus,reviewDecision
```

### 2) View Checks (success/fail)

```bash
GH_PAGER=cat GH_FORCE_TTY=false gh pr view <pr-number> \
  --json statusCheckRollup \
  --jq '.statusCheckRollup[] | {name, status, conclusion}'
```

### 3) View Reviews / Review Requests

```bash
GH_PAGER=cat GH_FORCE_TTY=false gh pr view <pr-number> \
  --json latestReviews,reviewRequests \
  --jq '{latestReviews: [.latestReviews[] | {author: .author.login, state, submittedAt}], reviewRequests: [.reviewRequests[].login]}'
```

### 3a) View PR Conversation Comments (timeline discussion)

These are the “issue comments” on the PR conversation.

```bash
GH_PAGER=cat GH_FORCE_TTY=false gh api \
  --paginate \
  "/repos/{owner}/{repo}/issues/<pr-number>/comments" \
  --jq '.[] | {author: .user.login, createdAt: .created_at, url: .html_url, body: .body}'
```

### 3b) View Review Comments (inline on diffs)

These are the code-review comments attached to specific lines/paths in the diff.

```bash
GH_PAGER=cat GH_FORCE_TTY=false gh api \
  --paginate \
  "/repos/{owner}/{repo}/pulls/<pr-number>/comments" \
  --jq '.[] | {author: .user.login, createdAt: .created_at, url: .html_url, path: .path, line: .line, side: .side, body: .body}'
```

### 4) View Changed Files (names only)

```bash
GH_PAGER=cat GH_FORCE_TTY=false gh pr view <pr-number> --json files \
  --jq '.files[].path'
```

### 5) View PR Body (for review)

```bash
GH_PAGER=cat GH_FORCE_TTY=false gh pr view <pr-number> --json body --jq '.body'
```

## When To Prefer Wrapper Scripts
- If you are about to **create** or **merge** a PR: use `scripts/pr-github.sh create` / `scripts/pr-github.sh create-and-merge`.
- If you just need to **inspect** PR state/checks/reviews: use this skill’s `gh` patterns.

## When To Use `gh` CLI vs GitHub Chat Tools

### Prefer GitHub Chat Tools when
- You’re already in chat and just need **structured PR metadata** (details, changed files, status checks, comments).
- You want to avoid terminal-side pitfalls (auth prompts, pager behavior, large output).
- A tool exists that directly answers the question (e.g., a “get PR details” tool, “list PR comments”, active/open PR helpers).

### Prefer `gh` CLI when
- You need an API surface the chat tools don’t expose (or you need `gh api` flexibility).
- You need commands that are easy for Maintainers to reproduce locally.
- You’re following a documented repo workflow that standardizes on wrapper scripts and `gh`.

**Rule of thumb:** if a GitHub chat tool can fetch the data you need, use it; otherwise use `GH_PAGER=cat GH_FORCE_TTY=false gh ...` (or `gh api`) from this skill.
