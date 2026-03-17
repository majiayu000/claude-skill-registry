---
name: github-pr-review
description: Handles PR review comments and feedback resolution. Use when user wants to resolve PR comments, handle review feedback, fix review comments, address PR review, check review status, respond to reviewer, verify PR readiness, review PR comments, analyze review feedback, evaluate PR comments, assess review suggestions, or triage PR comments. Fetches comments via GitHub CLI, classifies by severity, applies fixes with user confirmation, commits with proper format, replies to threads.
---

# GitHub PR review

Resolves Pull Request review comments with severity-based prioritization, fix application, and thread replies.

## Current PR

!`gh pr view --json number,title,state,milestone -q '"PR #\(.number): \(.title) (\(.state)) | Milestone: \(.milestone.title // "none")"' 2>/dev/null`

## Core workflow

### 1. Fetch, filter, and classify comments

```bash
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
PR=$(gh pr view --json number -q '.number')
LAST_PUSH=$(git log -1 --format=%cI HEAD)

# Inline review comments - filter out replies (keep only originals)
gh api repos/$REPO/pulls/$PR/comments --jq '
  [.[] | select(.in_reply_to_id == null) |
   {id, path, user: .user.login, created_at, body: .body[0:200]}]
'

# PR-level reviews with non-empty body (CodeRabbit sections, Gemini, etc.)
gh api repos/$REPO/pulls/$PR/reviews --jq '
  [.[] | select(.body | length > 0) |
   {id, user: .user.login, state, submitted_at, body: .body[0:500]}]
'
```

**Filter new vs already-seen**: compare `created_at`/`submitted_at` with `$LAST_PUSH`. Comments posted after the last push are new. Mark older comments as "previous round" in the summary table.

**Parse CodeRabbit review bodies**: the initial fetch truncates bodies for classification. For reviews from CodeRabbit (`user.login` starts with `coderabbitai`), fetch the full body separately:

```bash
gh api repos/$REPO/pulls/$PR/reviews --jq '
  [.[] | select(.user.login | startswith("coderabbitai")) |
   {id, submitted_at, body}]
'
```

CodeRabbit posts structured `<details>` blocks containing outside-diff, duplicate, and nitpick comments. Each block includes file path, line range, severity, and optionally a "Prompt for AI Agents" with pre-built context. See `references/coderabbit_parsing.md` for full parsing guide.

**Use CodeRabbit AI prompts when available**: if a comment (or the review body) contains a "Prompt for AI Agents" `<details>` block, use it to understand the issue and suggested approach. Always read the actual code before proposing a fix.

Classify all comments by severity and process in order: CRITICAL > HIGH > MEDIUM > LOW.

| Severity | Indicators | Action |
|----------|------------|--------|
| CRITICAL | `critical.svg`, `_🔒 Security_`, `_🔴 Critical_`, "security", "vulnerability" | Must fix |
| HIGH | `high-priority.svg`, `_⚠️ Potential issue_`, `_🐛 Bug_`, `_🟠 Major_`, "High Severity" | Should fix |
| MEDIUM | `medium-priority.svg`, `_🛠️ Refactor suggestion_`, `_💡 Suggestion_`, "Medium Severity" | Recommended |
| LOW | `low-priority.svg`, `_🧹 Nitpick_`, `_🔧 Optional_`, `_🟡 Minor_`, `_🔵 Trivial_`, `_⚪ Info_`, "style", "nit" | Optional |

See `references/severity_guide.md` for full detection patterns (Gemini badges, CodeRabbit emoji, Cursor comments, keyword fallback, related comments heuristics).

### 2. Show review summary table

Before processing, display a structured overview of all comments:

```
| # | ID         | Severity | File:Line          | Type     | Status   | Summary            |
|---|------------|----------|--------------------|----------|----------|--------------------|
| 1 | 123456789  | CRITICAL | src/auth.py:45     | inline   | new      | SQL injection risk |
| 2 | 987654321  | HIGH     | src/db.py:346-350  | outside  | new      | Missing join cond  |
| 3 | 555555555  | HIGH     | src/chunk.py:188   | duplicate| previous | Stale metadata     |
| 4 | 444444444  | LOW      | tests/test_q.py:12 | nitpick  | previous | Naming convention  |
```

- **Type**: `inline`, `outside` (outside diff), `duplicate`, `minor`, `nitpick` (from CodeRabbit sections), or `review` (generic PR-level)
- **Status**: `new` (posted after last push) or `previous` (from earlier rounds)
- Group related comments (same file, same root cause, "also applies to" ranges) and note clusters
- Deduplicate: if the same issue appears both as an inline comment and in a CodeRabbit review body section (e.g., duplicate), keep one entry and note both sources

If there are **more than 10 comments**, suggest saving a review summary to Claude's memory for tracking across sessions. The summary should include: PR number, comment IDs, severity, status (new/addressed/deferred/won't fix), and brief description. This helps maintain continuity when new comments arrive after subsequent pushes.

### 3. Process each comment

For each comment, in severity order:

1. **Show context**: comment ID, severity, file:line, quote
2. **Check for AI prompt**: if CodeRabbit "Prompt for AI Agents" is available for this comment, use it to understand the issue and suggested approach
3. **Check for proposed fix**: if CodeRabbit includes a "Proposed fix" or "Suggested fix" code block, use it as a starting point (but verify correctness)
4. **Read affected code** and propose fix (always read the actual code, even when an AI prompt or proposed fix provides context)
5. **Handle "also applies to"**: if the comment references additional line ranges, include all locations in the fix
6. **Confirm with user** before applying
7. **Apply fix** if approved
8. **Verify ALL issues** in the comment are addressed (multi-issue comments are common)

### 4. Commit changes

Use git-commit skill format. Functional fixes get separate commits, cosmetic fixes are batched:

| Change type | Strategy |
|-------------|----------|
| Functional (CRITICAL/HIGH) | Separate commit per fix |
| Cosmetic (MEDIUM/LOW) | Single batch `style:` commit |

Reference the comment ID in the commit body.

### 5. Reply to threads

#### Inline comments

**Important**: use `--input -` with JSON. The `-f in_reply_to=...` syntax does NOT work.

```bash
COMMIT=$(git rev-parse --short HEAD)
gh api repos/$REPO/pulls/$PR/comments \
  --input - <<< '{"body": "Fixed in '"$COMMIT"'. Brief explanation.", "in_reply_to": 123456789}'
```

#### Non-inline comments (CodeRabbit review body)

Comments embedded in the review body (outside diff, duplicate, nitpick) do not have inline threads. The GitHub API does not support replying to a review body directly. Post a general PR comment referencing the specific issue:

```bash
gh pr comment $PR --body "Fixed in $COMMIT. Addresses outside-diff comment on file/path.py:346-350."
```

**Reply templates** (no emojis, minimal and professional):

| Situation | Template |
|-----------|----------|
| Fixed | `Fixed in [hash]. [brief description of fix]` |
| Won't fix | `Won't fix: [reason]` |
| By design | `By design: [explanation]` |
| Deferred | `Deferred to [issue/task]. Will address in future iteration.` |
| Acknowledged | `Acknowledged. [brief note]` |

### 6. Run tests and push

Run the project test suite. All tests must pass before pushing. Push all fixes together to minimize review loops.

### 7. Submit review (optional)

After addressing all comments, formally submit a review:

- `gh pr review $PR --approve --body "..."` - all comments addressed, PR is ready
- `gh pr review $PR --request-changes --body "..."` - critical issues remain
- `gh pr review $PR --comment --body "..."` - progress update, no decision yet

### 8. Verify milestone

```bash
gh pr view $PR --json milestone -q '.milestone.title // "none"'
```

If the PR has no milestone, check for open milestones:

```bash
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
gh api repos/$REPO/milestones --jq '[.[] | select(.state=="open")] | .[] | "\(.number): \(.title)"'
```

If open milestones exist, inform the user and suggest assigning:

```bash
gh pr edit $PR --milestone "[milestone-title]"
```

Do **not** assign automatically. This is a reminder only.

## Avoiding review loops

When bots (Gemini, Codex, etc.) review every push:

1. **Batch fixes**: accumulate all fixes, push once
2. **Draft PR**: convert to draft during fixes
3. **Commit keywords**: some bots respect `[skip ci]` or `[skip review]`

## Important rules

- **ALWAYS** fetch both inline comments (`pulls/$PR/comments`) and review bodies (`pulls/$PR/reviews`)
- **ALWAYS** parse CodeRabbit review bodies for all section types (outside diff, duplicate, minor, nitpick)
- **ALWAYS** use CodeRabbit "Prompt for AI Agents" as primary context when available
- **ALWAYS** show the review summary table before processing
- **ALWAYS** confirm before modifying files
- **ALWAYS** verify ALL issues in multi-issue comments are fixed, including "also applies to" ranges
- **ALWAYS** run tests before pushing
- **ALWAYS** reply to resolved threads using standard templates
- **ALWAYS** submit formal review (`gh pr review`) after addressing all comments
- **ALWAYS** check milestone at the end and remind if missing
- **ALWAYS** suggest saving a review summary to memory when there are more than 10 comments
- **NEVER** use emojis in commit messages or thread replies
- **NEVER** skip HIGH/CRITICAL comments without explicit user approval
- **NEVER** assign milestone automatically - suggest only
- **Functional fixes** -> separate commits (one per fix)
- **Cosmetic fixes** -> batch into single `style:` commit
- **Duplicate comments** -> treat as higher priority than their label (issue was already flagged before)
- **Related comments** -> group and fix together when they share root cause or file context

## References

- `references/severity_guide.md` - Severity detection patterns (Gemini badges, CodeRabbit emoji, Cursor comments, keyword fallback, related comments heuristics)
- `references/coderabbit_parsing.md` - CodeRabbit review body structure, section parsing, "Prompt for AI Agents" usage, duplicate and "also applies to" handling
