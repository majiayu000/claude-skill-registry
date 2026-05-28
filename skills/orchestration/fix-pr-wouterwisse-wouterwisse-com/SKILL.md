---
name: fix-pr
description: Thoroughly address ALL PR comments using parallel Opus subagents. Each subagent invokes /task skill.
allowed-tools: Task, TodoWrite, TaskOutput
---

# Fix PR Skill - Orchestrator

**Orchestrator ONLY spawns Opus subagents and collects summaries. ALL work is delegated.**

## Critical Rules

1. **NEVER read files** - subagents read files
2. **NEVER run commands** - subagents run commands
3. **NEVER call gh API** - subagents call gh API
4. **NEVER create commits** - subagents create commits
5. Orchestrator only: spawns agents, tracks todos, reports summaries

## Git Safety Rules (CRITICAL)

**This skill does NOT modify git history. Ever.**

- NO `git rebase` - rewrites history, causes divergence
- NO `git reset --hard` - destroys uncommitted work
- NO `git push --force` - overwrites remote history
- NO `git merge` - user decides when to merge
- `git fetch` - safe, read-only
- `git status` - safe, read-only
- `git push` - safe for new commits only (will fail if diverged)

**If the branch needs to be rebased onto main, the user must do it manually BEFORE running /fix-pr.**

---

## Phase 1: Analysis Subagent

Spawn a single subagent to detect PRs and fetch/categorize comments:

```
Task(general-purpose, model: opus):

Analyze open PR and categorize comments.

---

## Tasks

1. **Check for open PR**:
   ```bash
   gh pr list --head "$(git branch --show-current)" --state open --json number,title,url
   ```

2. **For the PR found, fetch ALL comments with thread context**:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{number}/comments --jq '.[] | {id, in_reply_to_id, path, line, body, user: .user.login}'
   gh api repos/{owner}/{repo}/pulls/{number}/reviews --jq '.[] | select(.body != "") | {user: .user.login, state, body}'
   ```

3. **Build thread map**: Group replies under parent comments to understand context.

4. **Categorize EVERY comment**:
   - **TO_FIX**: Actionable changes (including ALL nitpicks)
   - **SKIP**: Already resolved in thread, false positive, or owner overruled
   - **RESPOND**: Questions that need explanation (not code changes)
   - **DEFER**: Out of scope, requires broader refactoring → needs GitHub issue

5. **Extract instructions**:
   - CodeRabbit (`coderabbitai[bot]`): Look for `<summary>Prompt for AI Agents</summary>` section
   - Claude Code Review (`claude[bot]`): Use the full comment body as instruction
   - Human reviewers: Use full comment body as instruction

---

## Output Format

```yaml
---
PR_FOUND:
  number: 42
  branch: feature/xyz
  url: [url]

COMMENTS:
  TO_FIX:
    - id: "123456"
      reviewer: coderabbitai[bot]
      file: src/app/page.tsx
      line: 45
      instruction: "Add error handling for missing data..."
    - id: "123457"
      reviewer: wtrwts
      file: src/components/Card.tsx
      line: 80
      instruction: "should be private"

  SKIP:
    - id: "123459"
      reason: "Reply from owner: 'This is intentional'"

  RESPOND:
    - id: "123460"
      reviewer: wtrwts
      question: "Why did you choose approach A?"

  DEFER:
    - id: "123461"
      reviewer: coderabbitai[bot]
      reason: "Requires splitting the component - architectural change"
      suggested_issue_title: "Refactor: Split Card component into focused components"

SUMMARY:
  total: 12
  to_fix: 6
  skip: 2
  respond: 2
  defer: 2
---
```
```

---

## Phase 2: Create Todo List

Based on analysis results, create todo list:

```yaml
todos:
  - content: "Analyze PR and categorize comments"
    status: completed
  - content: "Fix: error handling in page (coderabbitai)"
    status: pending
  - content: "Fix: make property private (wtrwts)"
    status: pending
  - content: "Skip: intentional pattern (reply to comment)"
    status: pending
  - content: "Respond: explain approach choice"
    status: pending
  - content: "Defer: create issue for component refactor"
    status: pending
  - content: "Verify builds"
    status: pending
  - content: "Push changes"
    status: pending
```

---

## Phase 3: Parallel Fix Subagents

Spawn parallel subagents for ALL TO_FIX comments in a SINGLE message:

```
Task(general-purpose, model: opus):

Fix PR review comment by invoking /task skill.

---

## Context

- PR: #42
- Comment ID: 123456
- Reviewer: coderabbitai[bot]
- File: src/app/page.tsx
- Line: 45

## Reviewer Instructions

[PASTE THE EXTRACTED INSTRUCTION HERE]

---

## Workflow

1. **Invoke the /task skill** to make the fix:
   ```
   Skill(task)
   ```

   Pass these details to /task:
   - TASK: Fix the issue described in reviewer instructions above
   - Commit message format:
     ```
     fix(<scope>): <description>

     Addresses PR #42 review comment:
     - <reviewer>: "<brief summary>"
     ```

2. **After /task completes**, reply to the PR comment as a THREADED REPLY:

   **CRITICAL: Use `--input -` with JSON to ensure `in_reply_to` is correctly passed as an integer. This creates a threaded reply, NOT a standalone comment.**

   ```bash
   COMMIT_SHA=$(git rev-parse --short HEAD)
   COMMENT_ID=123456  # The comment ID from analysis

   # Create threaded reply using JSON input (most reliable method)
   echo '{"body": "Fixed in '"$COMMIT_SHA"'", "in_reply_to": '"$COMMENT_ID"'}' | \
     gh api repos/{owner}/{repo}/pulls/42/comments --method POST --input -
   ```

   **Verify the reply was threaded:** Check the response includes `"in_reply_to_id": 123456`. If `in_reply_to_id` is null, the reply failed to thread.

---

## Output Format

```yaml
---
STATUS: SUCCESS | FAILURE
COMMENT_ID: "123456"
COMMIT: abc1234
FILES_CHANGED:
  - [file1]
REPLIED: true | false
REPLY_THREADED: true | false
ERRORS: [if FAILURE or REPLY_THREADED=false]
---
```
```

**Spawn ALL fix subagents in parallel** (single message, multiple Task calls).

---

## Phase 4: Handle Skips, Responses, and Deferrals

Spawn a single subagent to handle non-fix items:

```
Task(general-purpose, model: opus):

Handle skipped comments, questions, and deferred items.

---

## SKIP Comments (Reply with reason)

**CRITICAL: Always create THREADED REPLIES using JSON input with `in_reply_to` as an integer.**

For each skipped comment:

```bash
COMMENT_ID={comment_id}  # The numeric comment ID

echo '{"body": "Acknowledged - [reason from analysis]", "in_reply_to": '"$COMMENT_ID"'}' | \
  gh api repos/{owner}/{repo}/pulls/{pr}/comments --method POST --input -
```

Skip reasons:
- "Already addressed in discussion above"
- "This is intentional because [reason]"
- "Keeping current approach per owner guidance"

## RESPOND Comments (Answer questions)

For each question:
1. Read the relevant code to understand context
2. Formulate clear technical answer
3. Reply as a THREADED REPLY:
   ```bash
   COMMENT_ID={comment_id}

   echo '{"body": "[Technical explanation]", "in_reply_to": '"$COMMENT_ID"'}' | \
     gh api repos/{owner}/{repo}/pulls/{pr}/comments --method POST --input -
   ```

## DEFER Comments (Create GitHub issues)

For each deferred item:

```bash
gh issue create \
  --title "[suggested_issue_title]" \
  --body "## Context

This issue was identified during PR #[number] review by @[reviewer].

**Original comment:** [link]
> [quote comment]

## Problem
[describe what needs to change]

## Proposed Solution
[concrete steps]

## Related
- PR #[number]
---
*Created from PR review comment*"
```

Then reply to original comment as a THREADED REPLY:
```bash
COMMENT_ID={comment_id}
ISSUE_URL="[issue_url]"

echo '{"body": "Created issue: '"$ISSUE_URL"'\n\nThis requires broader refactoring beyond this PR'\''s scope.", "in_reply_to": '"$COMMENT_ID"'}' | \
  gh api repos/{owner}/{repo}/pulls/{pr}/comments --method POST --input -
```

---

## Output Format

```yaml
---
SKIPPED:
  - comment_id: "123458"
    replied: true
RESPONDED:
  - comment_id: "123459"
    replied: true
DEFERRED:
  - comment_id: "123460"
    issue_created: "https://github.com/.../issues/99"
    replied: true
---
```
```

---

## Phase 5: Collect All Results

Use TaskOutput to wait for all subagents.

Aggregate:
- Fixes completed
- Commits created
- Comments replied to
- Issues created

---

## Phase 6: Verification Subagent

Spawn verification subagent:

```
Task(general-purpose, model: opus):

Verify all PR fixes are complete and working. DO NOT PUSH - push happens in Phase 7.

---

## Tasks

1. **Check git status**:
   ```bash
   git status
   ```

2. **Run TypeScript check**:
   ```bash
   npx tsc --noEmit
   ```

3. **Run lint**:
   ```bash
   npm run lint
   ```

4. **Run build**:
   ```bash
   npm run build
   ```

**DO NOT push here. Push happens in Phase 7 after verification passes.**

---

## Output Format

```yaml
---
STATUS: VERIFIED | FAILED
TYPESCRIPT: PASSED | FAILED
LINT: PASSED | FAILED
BUILD: PASSED | FAILED
ERRORS: [if FAILED]
---
```
```

**If verification fails, stop and report errors. Do not proceed to push.**

---

## Phase 7: Push & Re-Review Subagent

**Only run this phase if Phase 6 verification passed.**

Spawn push subagent to push all commits at once:

```
Task(general-purpose, model: opus):

Push all committed fixes. The push will automatically trigger new reviews from CodeRabbit and Claude via GitHub Actions.

---

## Tasks

1. **Push all changes**:
   ```bash
   git push
   ```

---

## Output Format

```yaml
---
STATUS: PUSHED | FAILED
ERRORS: [if FAILED]
---
```
```

---

## Phase 8: Resolve Confirmed Threads

**Run this phase after AI reviewers have had time to re-check the fixes (typically 1-2 minutes after push).**

Spawn a subagent to find and resolve threads where the AI reviewer has confirmed the fix:

```
Task(general-purpose, model: opus):

Find review threads where CodeRabbit or Claude has confirmed the fix is good, and resolve those threads.

---

## Tasks

### 1. Fetch all review threads for the PR using GraphQL

```bash
gh api graphql -f query='
query {
  repository(owner: "{owner}", name: "{repo}") {
    pullRequest(number: {pr_number}) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(last: 1) {
            nodes {
              author {
                login
              }
              body
            }
          }
        }
      }
    }
  }
}'
```

### 2. Identify threads to resolve

A thread should be resolved if ALL conditions are met:
- Thread is NOT already resolved (`isResolved: false`)
- The LAST comment is from `coderabbitai[bot]` OR `claude[bot]`
- The last comment body contains resolution indicators:
  - "LGTM" (case-insensitive)
  - "Looks good"
  - "looks good now"
  - "resolved"
  - "fixed"
  - "addressed"
  - checkmark emoji
  - "The issue has been"
  - "correctly implemented"
  - "properly addressed"

**DO NOT resolve threads where:**
- The last comment is from a human reviewer (they should resolve manually)
- The last comment contains questions or requests for further changes
- The AI reviewer is still asking for clarification

### 3. Resolve each confirmed thread

For each thread that should be resolved:

```bash
THREAD_ID="<thread_id_from_step_1>"
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "'$THREAD_ID'"}) {
    thread {
      isResolved
    }
  }
}'
```

---

## Output Format

```yaml
---
STATUS: SUCCESS | PARTIAL | NO_THREADS
THREADS_ANALYZED:
  total: 15
  already_resolved: 8
  ai_confirmed: 5
  human_pending: 2
THREADS_RESOLVED:
  - thread_id: "RT_..."
    reviewer: coderabbitai[bot]
    confirmation: "LGTM! The changes look good."
  - thread_id: "RT_..."
    reviewer: claude[bot]
    confirmation: "Correctly implemented as suggested."
NOT_RESOLVED:
  - thread_id: "RT_..."
    reason: "Last comment from human reviewer"
  - thread_id: "RT_..."
    reason: "AI reviewer still asking questions"
ERRORS: [if any]
---
```
```

**Note:** If AI reviewers haven't responded yet, this phase will find no threads to resolve. You can run `/fix-pr` again later to resolve threads once AI reviews complete.

---

## Phase 9: Report to User

Summarize all results:

```markdown
## PR Fixes Complete

### PR Processed
- PR #42: 5 comments addressed

### Summary
| Category | Count | Status |
|----------|-------|--------|
| Fixed | 5 | All committed |
| Skipped | 2 | Replied with reasons |
| Responded | 2 | Questions answered |
| Deferred | 1 | Issue #99 created |

### Commits
- abc1234: fix(app): add error handling
- def5678: refactor(component): make helper private

### Verification
- TypeScript: PASSED
- Lint: PASSED
- Build: PASSED
- Pushed: All changes pushed (auto-triggers new reviews)

### Threads Resolved
| Reviewer | Status |
|----------|--------|
| coderabbitai[bot] | Resolved (LGTM) |
| claude[bot] | Resolved (Fixed) |
| wtrwts | Pending (human reviewer) |

[If any failures, list specific errors]
```

---

## Key Principles

1. **Orchestrator is minimal** - only spawns and collects
2. **Analysis happens once** - single subagent categorizes all comments from ALL reviewers
3. **Fixes are parallel** - spawn all fix subagents simultaneously
4. **Post-processing is batched** - single subagent handles skips/responses/deferrals
5. **Verification is separate** - dedicated subagent for builds
6. **Push once at the end** - single push after all fixes verified (auto-triggers new reviews)
7. **Every comment addressed** - nothing is silently ignored
8. **Minimal reply noise** - just state what was done (commit hash), no re-review requests
9. **Auto-resolve confirmed threads** - when AI reviewers confirm fixes are good, resolve those threads via GraphQL API (human-reviewed threads require manual resolution)
10. **ALWAYS use threaded replies** - ALL replies MUST use JSON input with `in_reply_to` as an integer
