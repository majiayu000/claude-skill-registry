---
name: pr-comments
description: Triage unresolved PR review comments, produce a severity-ordered fix plan, then resolve or fix each issue with subagents. Use when addressing PR feedback before merge.
user-invocable: true
---

# PR Comments — Triage & Fix

Fetch all unresolved PR review threads, deduplicate across bots, triage by severity, and produce a fix plan for human approval. After sign-off, resolve ignored threads and spawn subagents to fix real issues.

## Invocation

- `/pr-comments` — auto-detect PR from current branch
- `/pr-comments 608` — specific PR number

## Phase 1: Fetch Unresolved Threads

### 1a. Identify the PR

```bash
# Auto-detect from current branch, or use the provided PR number
gh pr view --json number,headRepositoryOwner,title,headRefName,baseRefName
```

### 1b. Fetch ALL review threads via GraphQL

Use GraphQL to get thread resolution status — this is the only reliable source of truth.

```bash
gh api graphql -f query='
{
  repository(owner: "{OWNER}", name: "{REPO_NAME}") {
    pullRequest(number: {PR_NUMBER}) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          comments(first: 20) {
            nodes {
              databaseId
              author { login }
              body
              path
              line
              originalLine
              createdAt
              url
            }
          }
        }
      }
    }
  }
}'
```

Paginate if `hasNextPage` is true. Collect every thread.

### 1c. Filter to unresolved threads only

- Keep threads where `isResolved == false`
- Note `isOutdated` — the diff may have moved; flag these for extra scrutiny

### 1d. Also fetch issue-level comments (PR conversation tab)

```bash
gh api --paginate "repos/{OWNER}/{REPO_NAME}/issues/{PR_NUMBER}/comments?per_page=100"
```

Filter to comments from **human reviewers only** (not bots). These are often the most important.

## Phase 2: Deduplicate & Classify

Multiple bots often flag the **same underlying issue** on the same file/line. Group them.

### 2a. Group by file + line range

Threads targeting the same file within a 5-line range likely address the same issue. Merge them into a single logical issue.

### 2b. Parse severity from bot comments

Each bot uses different severity markers:

| Bot | Format | Example |
|-----|--------|---------|
| `coderabbitai[bot]` | Emoji badge in body | `🟠 Major`, `🟡 Minor`, `🔴 Critical` |
| `gemini-code-assist[bot]` | SVG image alt text | `![medium]`, `![high]`, `![low]` |
| `chatgpt-codex-connector[bot]` | Shield badge | `P1`, `P2`, `P3` |
| `devin-ai-integration[bot]` | HTML comment metadata | Parse `devin-review-comment` JSON for severity |

Map all to a unified scale: **Critical > Major > Medium > Minor > Nitpick**

When multiple bots flag the same issue at different severities, take the **highest**.

### 2c. Classify each issue

For each deduplicated issue, determine:

1. **Category**: `security` | `bug` | `correctness` | `performance` | `accessibility` | `style` | `config` | `docs`
2. **Severity**: Critical / Major / Medium / Minor / Nitpick
3. **Confidence**: How likely is this a real problem vs. a false positive?
   - Human reviewer comments → always high confidence
   - Multiple bots flagging the same thing → high confidence
   - Single bot, no context about codebase patterns → low confidence
   - Bot flagging a SKILL.md or config file → usually noise

### 2d. Identify ignore candidates

Flag as **ignore candidate** if ANY of these apply:

- Bot comment on a non-source file (`.md`, config, migrations) with no security implications
- Style/nitpick-level feedback that contradicts project conventions (check AGENTS.md)
- Bot flagging something that was intentionally designed that way (check git blame / PR description)
- Outdated thread (`isOutdated == true`) where the code has already changed
- Duplicate of another issue already being addressed
- Bot suggesting a pattern that contradicts a loaded skill or AGENTS.md convention

## Phase 3: Write the Fix Plan

Write the plan to `.claude/scratchpad/pr-{PR_NUMBER}-review-plan.md`.

### Plan Format

```markdown
# PR #{PR_NUMBER} Review Plan — "{PR_TITLE}"

**Branch:** {branch_name}
**PR URL:** {pr_url}
**Threads fetched:** {total} total, {unresolved} unresolved, {outdated} outdated
**Bot breakdown:** {count per bot}

---

## Issues to Fix (ordered by severity)

Only include issues that will actually be fixed. Items classified as ignored in Phase 2 go EXCLUSIVELY in the Ignored section below — never list them here.

### 1. [{SEVERITY}] {Short description of the issue}

- **File:** `path/to/file.ts#L{line}`
- **Category:** {category}
- **Flagged by:** @bot1, @bot2
- **Comment URL:** {url to first comment}
- **What's wrong:** {1-2 sentence explanation in plain english}
- **Suggested fix:** {concrete description of what to change}

> Original comment (from @bot1):
> {relevant excerpt — strip boilerplate/badges}

---

### 2. [{SEVERITY}] ...

---

## Ignored (with reasoning)

Each ignored item appears ONLY here — not duplicated in the Issues to Fix section above.

### I1. @{bot} on `path/to/file.ts#L{line}`

- **Why ignored:** {specific reason — e.g., "contradicts project convention in AGENTS.md to not use explicit return types", "outdated thread, code already changed", "style nitpick on a config file"}
- **Original comment:** {link to comment}

### I2. ...

---

## Summary

- **{N} issues to fix** across {M} files
- **{K} comments ignored** ({reasons breakdown})
- Estimated complexity: {low/medium/high}
```

### Present to user

After writing the plan, tell the user:

> Review plan written to `.claude/scratchpad/pr-{PR_NUMBER}-review-plan.md`.
> **{N} issues to fix**, **{K} ignored**. Please review and confirm to proceed.

**STOP HERE.** Wait for the user to review and approve. Do not proceed until they confirm.

## Phase 4: Execute (after human approval)

Once the user approves (they may edit the plan first — re-read it before executing):

### 4a. Resolve ignored threads

For each ignored issue, resolve the GitHub thread with a brief comment explaining why:

```bash
# Post a reply comment on the thread
gh api -X POST "repos/{OWNER}/{REPO_NAME}/pulls/{PR_NUMBER}/comments" \
  -f body="Acknowledged — {reason}. Resolving." \
  -F in_reply_to={COMMENT_DATABASE_ID}

# Resolve the thread via GraphQL
gh api graphql -f query='
mutation {
  resolveReviewThread(input: { threadId: "{THREAD_NODE_ID}" }) {
    thread { isResolved }
  }
}'
```

Use concise, specific dismiss reasons. Examples:
- "Acknowledged — project convention is to omit explicit return types (see AGENTS.md). Resolving."
- "Acknowledged — outdated thread, code has been refactored. Resolving."
- "Acknowledged — this is intentional; sessionStorage is only accessed client-side. Resolving."

### 4b. Fix real issues with subagents

Group related issues that touch the same file or logical unit. Then launch **parallel subagents** (one per file or logical group) using the Task tool:

```
Launch a Task subagent (subagent_type: "general-purpose") for each group:

Prompt template:
"Fix the following PR review issue(s) on branch {BRANCH}:

Issue: {description}
File: {path}#{line}
What's wrong: {explanation}
Suggested fix: {fix description}

Read the file, understand the surrounding context, and make the fix.
After fixing, verify the change is correct.
Do NOT touch unrelated code."
```

- Use `subagent_type: "general-purpose"` for each group
- Launch groups in parallel where they touch different files
- Sequential if they touch the same file

### 4c. After all subagents complete

1. Resolve the fixed threads on GitHub (same GraphQL mutation as 4a, with a comment like "Fixed in latest push.")
2. Report results to the user

## Known Bot Noise Patterns

These are **almost always ignorable** — but verify before dismissing:

1. **coderabbit on SKILL.md / AGENTS.md files** — flags markdown structure, irrelevant
2. **gemini suggesting explicit return types** — check project AGENTS.md or lint config before accepting
3. **devin HTML comment metadata** — often duplicates what coderabbit already found
4. **codex P3 style suggestions** — usually preferences, not bugs
5. **Any bot suggesting `as` casts or non-null assertions** — check project conventions before accepting
6. **vercel[bot] deployment comments** — pure noise, never actionable
7. **Bot comments on migration files** — almost always false positives (auto-generated code)
