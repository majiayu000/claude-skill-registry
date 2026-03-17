---
name: github-url-intercept
version: 2.1.0
description: "BLOCKING INTERCEPT: When ANY github.com URL appears in user input, STOP and use this skill. Never fetch GitHub HTML pages directly - they are 5-10MB and will exhaust your context window. This skill routes URLs to efficient API calls (1-50KB). Triggers on: pull/, issues/, blob/, tree/, commit/, compare/, discussions/."
license: MIT
model: claude-opus-4-5
metadata:
  domains:
  - github
  - url-parsing
  - context-optimization
  type: interceptor
  complexity: low
  priority: critical
  related_skills:
  - github
---
# GitHub URL Intercept

> **CRITICAL**: This skill activates AUTOMATICALLY when you see ANY `github.com` URL.
> Do NOT use `web_fetch`, `curl`, or any browser-based fetch on GitHub URLs.
> Doing so wastes 1-2.5 MILLION tokens on HTML that provides no useful data.

**MANDATORY BEHAVIOR**: Parse the URL → Route to API → Return structured JSON.

---

## Quick Reference (Copy-Paste Commands)

**When you see a GitHub URL, use these commands immediately:**

```powershell
# PR URL → Use this
pwsh .claude/skills/github/scripts/pr/Get-PRContext.ps1 -PullRequest {n} -Owner {owner} -Repo {repo}

# Issue URL → Use this
pwsh .claude/skills/github/scripts/issue/Get-IssueContext.ps1 -Issue {n} -Owner {owner} -Repo {repo}

# File/blob URL → Use this
gh api repos/{owner}/{repo}/contents/{path}?ref={ref}

# Commit URL → Use this
gh api repos/{owner}/{repo}/commits/{sha}

# Comment fragment (#discussion_r{id}) → Use this
gh api repos/{owner}/{repo}/pulls/comments/{id}
```

---

## Triggers

| Phrase | Action |
|--------|--------|
| Any `github.com` URL in user input (even bare URL pasted alone) | Parse URL type and route to API |
| `analyze` / `research` / `scan` + GitHub URL | Route based on URL type |
| URL + question (e.g., "...#r123 what's the tracking issue?") | Extract fragment, call specific API |
| Multiple GitHub URLs in one prompt | Process each URL, batch API calls |

---

## When to Use

Use this skill when:

- Any `github.com` URL appears in user input (automatic activation)
- User pastes a PR, issue, commit, file, or actions URL
- User asks to "analyze" or "review" a GitHub link

Use [github](../github/SKILL.md) instead when:

- Performing mutations (creating PRs, posting comments, adding labels)
- Operating on the current repository without a URL

## URL Patterns (Detailed Reference)

| Pattern | Example | Why Intercept |
|---------|---------|---------------|
| `github.com/.../pull/` | `https://github.com/owner/repo/pull/123` | PR HTML is 5-10MB |
| `github.com/.../pull/.../checks` | `https://github.com/owner/repo/pull/123/checks?check_run_id=...` | CI checks page bloat |
| `github.com/.../pull/.../files` or `/changes` | `https://github.com/owner/repo/pull/123/files#r123456` | Diff view with comment fragment |
| `github.com/.../issues/` | `https://github.com/owner/repo/issues/456` | Issue HTML is 2-5MB |
| `github.com/.../actions/runs/` | `https://github.com/owner/repo/actions/runs/123/job/456` | Workflow run page bloat |
| `github.com/.../blob/` | `https://github.com/owner/repo/blob/main/file.py` | File page has nav bloat |
| `github.com/.../tree/` | `https://github.com/owner/repo/tree/main/src` | Directory listing bloat |
| `github.com/.../commit/` | `https://github.com/owner/repo/commit/abc123` | Commit page overhead |
| `github.com/.../compare/` | `https://github.com/owner/repo/compare/main...feat` | Diff page overhead |
| `github.com/.../discussions/` | `https://github.com/owner/repo/discussions/789` | Discussion page bloat |
| Fragment `#discussion_r{id}` | Review comment ID in `/changes` or `/files` URL | Extract ID, call API directly |
| Fragment `#issuecomment-{id}` | Issue comment ID | Extract ID, call API directly |
| Fragment `#pullrequestreview-{id}` | Review ID | Extract ID, call API directly |
| Fragment `#r{id}` (short form) | Review comment in `/changes#r123` | Same as `#discussion_r{id}` |

---

## Decision Flow

```text
GitHub URL detected in user input
│
├─ Has fragment (#pullrequestreview-, #discussion_r, #issuecomment-)?
│     Yes → Extract ID, use gh api for specific comment/review
│
├─ Is /pull/{n}?
│     Yes → Get-PRContext.ps1 -PullRequest {n} -Owner {o} -Repo {r}
│           (or Get-PRReviewComments.ps1 / Get-PRReviewThreads.ps1 for comments)
│
├─ Is /issues/{n}?
│     Yes → Get-IssueContext.ps1 -Issue {n} -Owner {o} -Repo {r}
│
├─ Is /blob/{ref}/{path} or /tree/{ref}/{path}?
│     Yes → gh api repos/{o}/{r}/contents/{path}?ref={ref}
│
├─ Is /commit/{sha}?
│     Yes → gh api repos/{o}/{r}/commits/{sha}
│
└─ Is /compare/{base}...{head}?
      Yes → gh api repos/{o}/{r}/compare/{base}...{head}
```

---

## Process

### Phase 1: URL Detection and Parsing

| Step | Action | Verification |
|------|--------|--------------|
| 1.1 | Detect github.com URL in user input | URL pattern matched |
| 1.2 | Extract owner/repo from path | Both values non-empty |
| 1.3 | Identify URL type (pull, issues, blob, tree, commit, compare) | Type classified |
| 1.4 | Extract fragment ID if present | Fragment parsed or null |

### Phase 2: Route Selection

| Step | Action | Verification |
|------|--------|--------------|
| 2.1 | Check if github skill script exists for URL type | Script path resolved |
| 2.2 | If script exists → use github skill (primary route) | Script invocation planned |
| 2.3 | If no script → use gh api (fallback route) | API command constructed |
| 2.4 | For fragments → always use gh api with specific endpoint | Endpoint includes ID |

### Phase 3: Execution

| Step | Action | Verification |
|------|--------|--------------|
| 3.1 | Execute selected command | Command runs without error |
| 3.2 | Receive structured JSON response | `Success: true` for scripts |
| 3.3 | Parse relevant fields for user query | Response processed |

---

## URL Routing Table

### Primary: Use GitHub Skill Scripts

| URL Pattern | Script | Parameters |
|-------------|--------|------------|
| `/pull/{n}` | `Get-PRContext.ps1` | `-PullRequest {n} -Owner {o} -Repo {r}` |
| `/pull/{n}` (with diff) | `Get-PRContext.ps1` | `-PullRequest {n} -IncludeDiff` |
| `/pull/{n}` (review comments) | `Get-PRReviewComments.ps1` | `-PullRequest {n}` |
| `/pull/{n}` (review threads) | `Get-PRReviewThreads.ps1` | `-PullRequest {n}` |
| `/pull/{n}` (CI status) | `Get-PRChecks.ps1` | `-PullRequest {n}` |
| `/issues/{n}` | `Get-IssueContext.ps1` | `-Issue {n} -Owner {o} -Repo {r}` |

**Script location**: `.claude/skills/github/scripts/`

### Fallback: Raw gh Commands

Use only when no script exists for the operation:

| URL Pattern | API Call |
|-------------|----------|
| `/pull/{n}#pullrequestreview-{id}` | `gh api repos/{o}/{r}/pulls/{n}/reviews/{id}` |
| `/pull/{n}#discussion_r{id}` | `gh api repos/{o}/{r}/pulls/comments/{id}` |
| `/pull/{n}/files#r{id}` or `/changes#r{id}` | `gh api repos/{o}/{r}/pulls/comments/{id}` |
| `/pull/{n}#issuecomment-{id}` | `gh api repos/{o}/{r}/issues/comments/{id}` |
| `/pull/{n}/checks` | `gh api repos/{o}/{r}/check-runs?head_sha=...` or use `Get-PRChecks.ps1` |
| `/issues/{n}#issuecomment-{id}` | `gh api repos/{o}/{r}/issues/comments/{id}` |
| `/actions/runs/{run_id}` | `gh api repos/{o}/{r}/actions/runs/{run_id}` |
| `/actions/runs/{run_id}/job/{job_id}` | `gh api repos/{o}/{r}/actions/jobs/{job_id}` |
| `/blob/{ref}/{path}` | `gh api repos/{o}/{r}/contents/{path}?ref={ref}` |
| `/tree/{ref}/{path}` | `gh api repos/{o}/{r}/contents/{path}?ref={ref}` |
| `/commit/{sha}` | `gh api repos/{o}/{r}/commits/{sha}` |
| `/compare/{base}...{head}` | `gh api repos/{o}/{r}/compare/{base}...{head}` |

---

## URL Parsing Pattern

Extract owner, repo, and resource from GitHub URLs:

```text
https://github.com/{owner}/{repo}/pull/{number}
https://github.com/{owner}/{repo}/issues/{number}
https://github.com/{owner}/{repo}/blob/{ref}/{path}
https://github.com/{owner}/{repo}/tree/{ref}/{path}
https://github.com/{owner}/{repo}/commit/{sha}
https://github.com/{owner}/{repo}/compare/{base}...{head}
```

**Fragment extraction** (when present):

- `#pullrequestreview-{id}` → Review ID
- `#discussion_r{id}` → Discussion comment ID
- `#issuecomment-{id}` → Issue comment ID

---

## Why This Matters (CRITICAL)

**Fetching GitHub HTML is catastrophic for your context window:**

| Method | Response Size | Token Cost | Time | Usability |
|--------|---------------|------------|------|-----------|
| ❌ HTML fetch | 5-10 MB | 1-2.5M tokens | 10-30s | **UNUSABLE** - HTML noise, no structured data |
| ✅ API call | 1-50 KB | 250-12K tokens | 0.5-2s | Clean JSON with exactly what you need |
| ✅ Script | 1-50 KB | 250-12K tokens | 0.5-2s | Structured output, error handling |

**Impact**: 100-1000x reduction in token consumption.

**If you fetch GitHub HTML directly, you will:**

1. Consume your entire context window on ONE page
2. Get no useful structured data (just HTML soup)
3. Be unable to process subsequent user requests
4. Need to start a new conversation

**ALWAYS use this skill when you see a GitHub URL.**

---

## Examples

### Bare URL Pasted (Most Common!)

```text
Input: "https://github.com/rjmurillo/ai-agents/pull/735/checks?check_run_id=59355308734"

Action:
  1. Parse: owner=rjmurillo, repo=ai-agents, pr=735, type=checks
  2. Route: pwsh .claude/skills/github/scripts/pr/Get-PRChecks.ps1 -PullRequest 735 -Owner rjmurillo -Repo ai-agents
```

### URL with Question After It

```text
Input: "https://github.com/owner/repo/pull/715/changes#r2656144507 are the graph refactoring items part of Issue 722?"

Action:
  1. Extract fragment: r2656144507 (review comment ID)
  2. Call: gh api "repos/owner/repo/pulls/comments/2656144507"
  3. Answer user's question using the comment content
```

### Multiple URLs in One Prompt

```text
Input: "https://github.com/owner/repo/pull/715#discussion_r123 https://github.com/owner/repo/pull/715#discussion_r456"

Action:
  1. Parse each URL
  2. Batch: gh api "repos/owner/repo/pulls/comments/123"
  3. Batch: gh api "repos/owner/repo/pulls/comments/456"
```

### Research/Analyze Pattern

```text
Input: "analyze https://github.com/modu-ai/moai-adk for insights"

Action:
  1. Use deepwiki MCP or gh api to get repo info
  2. Call: gh api "repos/modu-ai/moai-adk" (NOT web_fetch!)
```

### CI/Actions Run URL

```text
Input: "https://github.com/owner/repo/actions/runs/20675405338/job/59362398542?pr=740"

Action:
  1. Extract: run_id=20675405338, job_id=59362398542
  2. Call: gh api "repos/owner/repo/actions/jobs/59362398542"
```

### PR URL → Script

```text
Input: "Review this: https://github.com/owner/repo/pull/123"

Action:
  pwsh ".claude/skills/github/scripts/pr/Get-PRContext.ps1" -PullRequest "123" -Owner "owner" -Repo "repo"
```

### File URL → API

```text
Input: "would a hook like https://github.com/ruvnet/claude-flow/blob/main/.claude/settings.json help?"

Action:
  gh api "repos/ruvnet/claude-flow/contents/.claude/settings.json?ref=main"
```

---

## Anti-Patterns (NEVER DO THESE)

| ❌ NEVER | Why It's Catastrophic | ✅ Do This Instead |
|----------|----------------------|-------------------|
| `web_fetch("https://github.com/...")` | 5-10 MB HTML, 1-2.5M tokens WASTED | Parse URL, use script or `gh api` |
| `curl https://github.com/...` | Same catastrophic result | Use `gh` CLI for authentication + JSON |
| `fetch` / `requests.get` on GitHub URLs | Same catastrophic result | Route through this skill |
| `gh pr view` without `--json` | Unstructured text output | Use `Get-PRContext.ps1` for structured JSON |
| Fetching full page to find one comment | Fetches 5MB to read 500 bytes | Extract fragment ID (`#discussion_r...`), call specific endpoint |
| Ignoring GitHub URLs in user input | User expects you to understand the link | ALWAYS parse and route |
| Hardcoding owner/repo in commands | Breaks when user shares fork/different repo | Extract from URL path |

**RED FLAG PHRASES** - If you're about to do any of these, STOP:

- "Let me fetch that page..."
- "I'll retrieve the content from that URL..."
- "Accessing the GitHub page..."

**These indicate you're about to waste millions of tokens. Use this skill instead.**

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| [github](../github/SKILL.md) | Full PR/issue operations (mutations, reactions, labels) |
| [pr-comment-responder](../pr-comment-responder/SKILL.md) | Systematic PR review response |

---

## Verification Checklist

Before processing any GitHub URL:

- [ ] Extracted owner/repo from URL path
- [ ] Identified URL type (PR, issue, blob, commit, compare)
- [ ] Extracted fragment ID if present (#discussion_r, #issuecomment-, #pullrequestreview-)
- [ ] Selected appropriate github skill script (primary) or gh command (fallback)
- [ ] Did NOT use web_fetch, curl, or browser-based fetch on the URL
- [ ] Received structured JSON response with `Success: true` (for scripts)
