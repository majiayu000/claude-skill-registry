---
name: pr-comment-resolution
description: Resolve all PR reviewer comments — fetch, categorize, implement fixes, reply inline, verify, and push. Use when a PR has reviewer feedback that needs to be addressed.
---

# PR Comment Resolution

Fetch all reviewer comments on a PR, categorize them, implement fixes, reply inline, verify, and push.

## Step 1 — Identify PR

```
IF $ARGUMENTS contains PR number or URL:
  Use provided PR identifier
ELSE:
  gh pr view --json number,url,baseRefName,headRefName

FAIL FAST if no open PR found for current branch.
```

Extract: PR number, base branch, head branch, repo owner/name.

```bash
gh repo view --json owner,name --jq '.owner.login + "/" + .name'
```

## Step 2 — Gather Full Context

Collect all PR data. GitHub stores comments in 3 separate APIs — fetch ALL of them.

```bash
# PR metadata + diff
gh pr view $PR --json title,body,author,reviewRequests,reviews,labels,files
gh pr diff $PR

# Changed files list (for scope guard)
gh pr view $PR --json files --jq '.files[].path'

# Conversation comments (top-level PR discussion)
gh api repos/{owner}/{repo}/issues/$PR/comments

# Inline review comments (line-level feedback)
gh api repos/{owner}/{repo}/pulls/$PR/comments

# Review verdicts and summaries
gh api repos/{owner}/{repo}/pulls/$PR/reviews
```

Read every changed file in full to understand the surrounding context, not just the diff hunks.

## Step 3 — Categorize Comments

Cross-reference `workflow:code-review-excellence` severity labels when classifying.

```
For each comment/review:
  - blocking   — Must fix before merge
  - question   — Needs a response (may or may not need code change)
  - suggestion — Alternative approach worth considering
  - nit        — Minor style/preference, non-blocking
  - resolved   — Already addressed or outdated
  - unclear    — Cannot determine intent; needs clarification
```

### Detect Language Context

Inspect file extensions of changed files and cross-reference matching `languages:*` skills for implementation guidance:

| Extension | Skill |
|-----------|-------|
| `.py` | `languages:python-patterns` |
| `.js`, `.ts`, `.tsx` | `languages:js-ts-patterns` |
| `.go` | `languages:go-concurrency-patterns` |
| `.sh` | `languages:bash-defensive-patterns` |
| `.swift` | `languages:swift-patterns` |
| `.rs` | `languages:rust-project-patterns` |

### Produce Fix Plan

```
ORDERED FIX PLAN:
1. [blocking]   — Description (file:line) — from: @reviewer
2. [blocking]   — ...
3. [suggestion] — ...
4. [nit]        — ...

UNCLEAR (need clarification before implementing):
- Comment #id: "..." — What is unclear
```

**If ANY comment is classified as `unclear`: present the fix plan and ask for clarification BEFORE implementing anything.**

## Step 4 — Implement Fixes

### Execution order
1. Blocking issues first
2. Simple fixes (typos, imports, naming)
3. Complex fixes (refactoring, logic changes)
4. Nits last

### Rules
- **Scope guard**: Only touch files changed in the PR. If a fix requires changes outside PR scope, note it in the summary as deferred.
- **Atomic commits**: One commit per logical fix group. Use imperative mood, reference the comment.
- **Reply to threads inline**: Use the GitHub API to reply in the reviewer's thread, not as top-level comments.

```bash
# Reply to an inline review comment thread
gh api repos/{owner}/{repo}/pulls/$PR/comments/{comment_id}/replies \
  -f body="Fixed — [brief description of change]. See [commit_sha_short]."

# Reply to a top-level issue comment
gh api repos/{owner}/{repo}/issues/$PR/comments \
  -f body="Addressed — [brief description]."
```

### For questions (no code change needed)
Reply with a clear, concise answer in the thread. Don't make unnecessary code changes.

## Step 5 — Verify & Push

Cross-reference `workflow:verification-before-completion` — evidence before claims.

```
1. Run project tests (identify test command from package.json, Makefile, etc.)
2. Run linter if configured
3. Review full diff: git diff $(git merge-base HEAD origin/{base_branch})..HEAD
4. Confirm no unintended changes leaked in
5. Push
6. Watch CI: gh pr checks $PR --watch
7. Re-request review from original reviewers:
   gh pr edit $PR --add-reviewer {reviewer1},{reviewer2}
```

If tests or CI fail: diagnose, fix, add another commit, re-verify. Do not push failing code.

## Step 6 — Summary

Present to the user:

```markdown
## PR Comment Resolution Summary

### Comments Addressed
- [blocking] {description} — {commit_sha_short} (replied to @reviewer)
- [suggestion] {description} — {commit_sha_short}
- ...

### Questions Answered
- @reviewer: "{question}" — replied with explanation

### Deferred Items
- {description} — Reason: {out of scope / needs design discussion / ...}

### Verification
- Tests: {PASS/FAIL — evidence}
- Lint: {PASS/FAIL — evidence}
- CI: {PASS/FAIL/PENDING — link}
- Review re-requested: {reviewers}
```

Do not auto-file issues for deferred items. List them for the user to decide.

---

## Cross-References

- `workflow:code-review-excellence` — Severity labels, comment response patterns
- `workflow:verification-before-completion` — Verification gate before any completion claims
- `languages:*-patterns` — Auto-detected language-specific implementation guidance
