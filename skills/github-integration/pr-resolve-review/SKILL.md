---
name: resolve-review
description: Interactive PR review resolution - one thread at a time with plan-execute loop. Invoke with /resolve-review [--author=<name>] [--pr=<number>] [--batch] [--self].
---

# Resolve Review

## Goal

Interactively process PR review threads one at a time. Each thread gets full attention: discussion, planning, execution, and resolution before moving to the next.

## Glossary

| Term       | Definition                                                                                             |
| ---------- | ------------------------------------------------------------------------------------------------------ |
| **Thread** | A GitHub review comment thread (atomic unit on GitHub)                                                 |
| **Item**   | A unit of work in this process - either a single thread or multiple related threads processed together |
| **Part**   | A distinct feedback point within a PR comment - multi-point comments are split into parts     |
| **PR Comment** | An issue comment on the PR (not tied to specific code lines), distinct from review threads |

**Actions** (what user chooses):

| Action    | Code change | Thread closed | Meaning                            |
| --------- | ----------- | ------------- | ---------------------------------- |
| Address   | Yes         | Yes           | Valid feedback, implement fix      |
| Dismiss   | No          | Yes           | Invalid/out-of-scope/noise         |
| Prior fix | No          | Yes           | Already fixed in earlier work      |
| Defer     | No          | No            | Too complex, handle manually later |
| Discuss   | TBD         | TBD           | Need conversation first            |

## Usage

- `/resolve-review` - Process all unresolved threads from current branch's PR
- `/resolve-review --author=copilot` - Only Copilot feedback
- `/resolve-review --author=<username>` - Only feedback from specific user
- `/resolve-review --pr=123` - Specific PR number
- `/resolve-review --batch` - Batch mode: defer all GitHub ops to end for confirmation
- `/resolve-review --author=copilot --pr=626` - Combine filters
- `/resolve-review --self` - Include your own comments and threads (for testing or self-review)
- `/resolve-review --self --pr=123` - Test against specific PR including own feedback

## Arguments

- All arguments: $ARGUMENTS
- `--author=<name>`: Filter by thread author (case-insensitive match against login)
- `--pr=<number>`: Specific PR number (default: current branch's PR)
- `--batch`: Batch mode - defer all GitHub operations until end of session, show confirmation before executing
- `--self`: Include own comments and review threads (disabled by default). Useful for testing or reviewing your own notes.
- `--no-commit`: Disable per-item commits. Changes accumulate, user commits manually after session.

## Instructions

### 1. Fetch Unresolved Review Threads

Get repo info and PR number:

```bash
OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')
PR_NUMBER=$(gh pr view --json number -q .number)
```

**Argument parsing**: Parse `$ARGUMENTS` for flags:

- Extract `--author=<value>` if present → store as `AUTHOR_FILTER`
- Extract `--pr=<number>` if present → override `PR_NUMBER`
- Extract `--self` flag if present → store as `INCLUDE_SELF=true`
- Extract `--no-commit` flag if present → store as `NO_COMMIT=true`

If `--pr` was provided, use it directly:

```bash
PR_NUMBER=123  # from --pr argument
```

**Error handling**: If `gh pr view` fails (no open PR for current branch) and no `--pr` provided:

```
No open PR found for the current branch.

Options:
1. Specify a PR number: /resolve-review --pr=123
2. Push your branch and open a PR first
```

Exit gracefully - do not proceed.

Fetch review threads and PR comments via unified GraphQL query:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  viewer { login }
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      id
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          isOutdated
          comments(first: 10) {
            nodes {
              id
              author { login }
              body
              path
              line
              originalLine
              diffHunk
              url
              createdAt
            }
          }
        }
      }
      comments(first: 100) {
        nodes {
          id
          author { login }
          body
          url
          createdAt
          isMinimized
          minimizedReason
        }
      }
    }
  }
}' -f owner="$OWNER" -f repo="$REPO" -F pr="$PR_NUMBER"
```

**Field mapping** (important for API calls later):

| Response field                  | Variable name      | Used for                                    |
| ------------------------------- | ------------------ | ------------------------------------------- |
| `pullRequest.id`                | `PR_NODE_ID`       | GraphQL replies and summary comment         |
| `thread.id`                     | `THREAD_NODE_ID`   | GraphQL `resolveReviewThread`               |
| `thread.comments[0].id`         | `COMMENT_NODE_ID`  | GraphQL `addReaction`, `addPullRequestReviewComment` |
| `comments[].id`                 | `COMMENT_NODE_ID`  | GraphQL `addReaction`, `minimizeComment`    |
| `viewer.login`                  | `CURRENT_USER`     | Self-exclusion filter                       |

**Limits**: Query fetches up to 100 threads with 10 comments each. If a thread has more than 10 comments, only the first 10 are returned. Note this to user if relevant.

**PR not found**: If the GraphQL response returns `pullRequest: null`, the PR doesn't exist:

```
PR #123 not found. Check the PR number and try again.
```

Exit gracefully.

**Zero threads**: If PR exists but no unresolved threads found, report "No unresolved review threads found" and exit.

**Filter criteria for review threads**:

- Only include threads where `isResolved: false`
- If `--author` provided, only include threads where first comment's author login contains the filter string (case-insensitive)
- Exclude threads where first comment's author matches `viewer.login` (unless `--self` flag)
- Sort by `createdAt` of first comment

**Filter criteria for PR comments**:

- Only include comments where `isMinimized: false`
- If `--author` provided, filter by author login (case-insensitive contains)
- Exclude comments where author matches `viewer.login` (unless `--self` flag)
- Sort by `createdAt`

**Note:** GitHub's GraphQL API doesn't support server-side filtering. These filters are applied client-side after fetching.

**Line number handling**:

- `line`: Current line number in the latest version of the file (may be `null` if code moved)
- `originalLine`: Line number when the comment was made (always present)
- Use `line` if available, fall back to `originalLine`
- If `isOutdated: true`, note this in the display - the code may have changed since the comment

### 1.5. PR Comments Discovery

After filtering, if any PR comments remain, prompt the user:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found N unresolved review threads.

Also found M PR comments (not on specific code lines):
  • @author: "First 40 chars of comment..." (2 days ago)
  • @author: "Another comment preview..." (1 day ago)

Include these as feedback to resolve? [Yes / No]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

- If **Yes**: PR comments are processed after review threads
- If **No**: PR comments are ignored for this session
- If zero review threads but PR comments exist: show prompt without "Also found" phrasing

### 1.6. Part Analysis for PR Comments

If PR comments are included, analyze each comment for distinct feedback points.

**Analysis process:**

1. Parse comment body for distinct feedback points
2. Look for: numbered lists, bullet points, separate paragraphs with different topics, "also"/"and"/"another thing" transitions
3. Create one "part" per distinct point
4. Single-point comments get one part (no splitting needed)

**Part data:**

- `comment_node_id`: Parent comment ID (for minimization)
- `comment_url`: Link to parent comment
- `part_index`: 1-based index within comment
- `part_total`: Total parts in this comment
- `part_text`: Extracted text for this part
- `full_body`: Full comment body (for context)

**Grouping:** Parts participate in semantic grouping (Step 2). A part from one comment could be grouped with a review thread or part from another comment if they address the same issue.

### 1.7. Session Preferences

After determining items to process, prompt for session preferences using AskUserQuestion with multiSelect.

**Display format:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found N items to process.

ℹ️  Each addressed item creates a commit (disable: --no-commit)

After resolving:
  [ ] Post summary comment to PR
  [ ] Push commits to remote
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**AskUserQuestion options** (both default: checked):
- `POST_SUMMARY`: Post summary comment to PR
- `PUSH_COMMITS`: Push commits to remote

If `--no-commit` flag is set, show modified message (omit PUSH_COMMITS option):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found N items to process.

ℹ️  Per-item commits disabled (--no-commit)

After resolving:
  [ ] Post summary comment to PR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Store selections in `SESSION_PREFS`.

**SESSION_PREFS data:**

- `post_summary`: boolean (from POST_SUMMARY selection)
- `push_commits`: boolean (from PUSH_COMMITS selection)

Step 5 (Summary) uses these preferences for end-of-session actions.

### 2. Semantic Grouping (Optional)

Analyze threads for potential grouping:

- Same file + adjacent lines (within 10 lines) = potential group
- Same reviewer + same conceptual issue = potential group
- PR comment parts can be grouped with review threads or other parts
- Same conceptual issue across different feedback types = potential group

**Only group if HIGH confidence**. Criteria:

- Threads reference the same function/block
- Threads describe the same issue type (e.g., "missing type cast" appearing twice)

If grouping is proposed, present to user:

```
I notice these threads might be related:
1. @copilot on file.ts:45 - "Type casting needed..."
2. @copilot on file.ts:52 - "Similar type issue..."

Group these together? [Yes / No, keep separate]
```

Mixed grouping (review thread + PR comment part):

```
I notice these items might be related:
1. @copilot on file.ts:45 - "Type casting needed..."
2. @copilot PR comment part 2/3 - "Similar type issue mentioned..."

Group these together? [Yes / No, keep separate]
```

If no high-confidence groupings found, skip this step silently.

### 3. Create Task List

Use TodoWrite to create one task per item:

```
[pending] #1 @author · file.ts:45 · "first 50 chars..."
[pending] #2 @author · file.ts:89 · "first 50 chars..."
```

### 4. Process Each Item (Serial Loop)

For EACH item, complete this entire loop before moving to next:

#### 4a. Present Item

Display:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ITEM 1 of N (3 threads)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Author: @username
File: path/to/file.ts:45
URL: https://github.com/...

Comment:
> [full text of first comment]

[If thread has multiple comments, show conversation:]
Reply from @other_user:
> [reply text]

Reply from @username:
> [reply text]

Diff context:
[show diffHunk from the API response]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Item header**: Show `(K threads)` only if item contains multiple threads (was grouped). Single-thread items don't need the count.

If `isOutdated: true`, add a warning:

```
⚠️  OUTDATED: This thread may reference code that has changed.
```

**Suggestion blocks**: If the comment body contains a GitHub suggestion block (` ```suggestion ... ``` `), highlight this:

```
📝 Contains code suggestion - can be applied directly if approved.
```

**PR Comment presentation** (single-point):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ITEM 5 of 9                                              PR COMMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Author: @username
URL: https://github.com/...

Comment:
> Full comment text here.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**PR Comment presentation** (multi-point, showing one part):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ITEM 6 of 9                                    PR COMMENT · part 1/3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Author: @username
URL: https://github.com/...

Full comment:
> Can we add a loading state? Also the error handling seems
> incomplete. And should we add types for the response?

This part:
> Can we add a loading state?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Header badge rules:**

- Review thread: `(K threads)` only if grouped
- Single-point PR comment: `PR COMMENT`
- Multi-point PR comment: `PR COMMENT · part N/M`

**PR comment differences:**

- No `File:` line (not tied to specific code)
- No `Diff context:` section
- Multi-point comments show both full comment and extracted part

**Analysis block**: After presenting the thread, analyze and display a triage assessment with a **suggested action**:

```
─── Analysis ──────────────────────────────────────────────────────
<SUGGESTED ACTION>
  reason:   <why this action>
  evidence: <commits, policies, code refs - if applicable>
  response: <what happens on GitHub thread>
  note:     <caveats, follow-up ideas - if applicable>
───────────────────────────────────────────────────────────────────
```

The suggested action is one of: ADDRESS, DISMISS, PRIOR FIX, DEFER, or DISCUSS (see Glossary).

**Analysis fields**:

| Field       | Required      | Purpose                                                      |
| ----------- | ------------- | ------------------------------------------------------------ |
| `reason:`   | Yes           | Why this action is suggested (logic, diagnosis)              |
| `evidence:` | If applicable | Specific proof (commits, policies, code locations)           |
| `response:` | Yes           | What happens on GitHub thread (resolve + comment text, etc.) |
| `note:`     | If applicable | Free-form: caveats, follow-up ideas                          |

**Example analyses**:

```
─── Analysis ──────────────────────────────────────────────────────
DISMISS
  reason:   ARIA not enforced per project policy
  evidence: CLAUDE.md § Accessibility, HEA-3834
  response: resolve, no comment
───────────────────────────────────────────────────────────────────
```

```
─── Analysis ──────────────────────────────────────────────────────
PRIOR FIX
  evidence: commit 15762eb
  reason:   Changed to color="primary" per design
  response: resolve + "Fixed in 15762eb"
───────────────────────────────────────────────────────────────────
```

```
─── Analysis ──────────────────────────────────────────────────────
ADDRESS
  reason:   Selector runs before early return, causes unnecessary work
  response: after fix → resolve + thumbs up
───────────────────────────────────────────────────────────────────
```

#### 4b. Get User Direction

Use AskUserQuestion:

| Option             | Description                                                      |
| ------------------ | ---------------------------------------------------------------- |
| Go with suggestion | Accept the suggested action + response from analysis             |
| Address            | Plan and implement a fix (requires approval before code changes) |
| Dismiss            | Invalid/out-of-scope feedback, close thread without code changes |
| Prior fix          | Already fixed in earlier work, close thread                      |
| Defer              | Too complex, leave thread open for manual handling later         |
| Discuss            | Talk through the issue before deciding                           |
| Abort              | Stop processing entirely and show summary                        |

**"Go with suggestion" behavior**: Accepts the suggested action from the analysis block and proceeds with the specified `response:`. If the suggested action is ADDRESS, still show the plan for approval before code changes (user is agreeing to the direction, not blanket-accepting the final resolution).

If "Discuss" selected: Have a conversation about the thread. When user indicates they're ready to decide (e.g., "ok let's address it", "skip this one", "I think we can move on"), proceed with that action. If unclear, ask "Ready to choose an action?" and present the same options again.

If "Abort" selected: Jump directly to step 5 (Summary), marking remaining threads as "Not processed".

#### 4c. Plan (if addressing)

**CRITICAL: No code changes without explicit approval.**

1. Read the relevant file(s) at the specified lines
2. Analyze what change is needed
3. If comment contains a suggestion block, extract the suggested code
4. Present proposed change to user:

   ```
   Proposed change for: file.ts:45

   The thread suggests: [summary]

   I propose:
   - [specific change 1]
   - [specific change 2]

   Approve this approach? [Yes / No, let's discuss]
   ```

5. Wait for explicit approval before proceeding

**If user says "No, let's discuss"**: Enter discussion mode. Talk through concerns, refine the approach, then present an updated plan. Repeat until user approves or decides to skip.

#### 4d. Execute (if approved)

1. Make the agreed-upon changes
2. Run type checks: `pnpm check:types` or project equivalent
3. **If type checks fail**:
   - Show the errors to user
   - Ask: "Type errors found. [Show full errors / Fix and retry / Skip this thread]"
   - If "Fix and retry": analyze errors, fix, re-run type checks
   - Repeat until passing or user skips
4. Show the diff to user
5. Ask: "Changes look correct? [Yes / No, needs revision]"
6. **Commit the change** (if approved and `--no-commit` not set):

   If `NO_COMMIT` is not set (from `--no-commit` flag):

   ```bash
   # Stage changed files
   git add <modified_files>

   # Commit with descriptive message
   git commit -m "fix(<scope>): <brief description from feedback>"
   ```

   Store commit SHA in item's `commit_sha` field for summary comment.

   **Commit message format:**
   - `fix(file): <action taken>` for bug fixes
   - `feat(file): <action taken>` for new functionality
   - `refactor(file): <action taken>` for refactoring

   Example: `fix(user): add null check before accessing name`

**If user says no (revision needed)**:

1. Ask: "What should be different?"
2. Discuss the issue
3. Make revised changes
4. Run type checks again (with same error handling)
5. Show updated diff
6. Repeat until user approves or decides to skip

#### 4e. Resolve on GitHub

Run this step for **all actions except Defer** (Address, Dismiss, Prior fix all close the thread).

**Batch mode (`--batch`)**: Skip execution. Store pending operation `{thread_ids, action, reply_text}` for batch execution at summary step.

**Incremental mode (default)**: Execute immediately with optimizations below.

1. **Ask about reply first** (before any API calls):

   Ask: "Add a reply comment? [Yes / No]"

   If yes: "What should the reply say?"

2. **Execute GitHub operations** via pure GraphQL:

   **Review thread resolution** (single or batched):

   ```bash
   gh api graphql -f query='
   mutation($commentId: ID!, $prId: ID!, $threadId: ID!, $body: String!) {
     addReaction(input: {subjectId: $commentId, content: THUMBS_UP}) {
       reaction { content }
     }
     addPullRequestReviewComment(input: {
       body: $body,
       pullRequestId: $prId,
       inReplyTo: $commentId
     }) {
       comment { id }
     }
     resolveReviewThread(input: {threadId: $threadId}) {
       thread { isResolved }
     }
   }' -f commentId="$COMMENT_NODE_ID" -f prId="$PR_NODE_ID" \
      -f threadId="$THREAD_NODE_ID" -f body="$REPLY" --silent
   ```

   If no reply needed, omit the `addPullRequestReviewComment` mutation.

   **Multi-thread batch** (all in one call):

   ```bash
   gh api graphql -f query='
   mutation {
     r1: addReaction(input: {subjectId: "ID1", content: THUMBS_UP}) { reaction { content } }
     r2: addReaction(input: {subjectId: "ID2", content: THUMBS_UP}) { reaction { content } }
     t1: resolveReviewThread(input: {threadId: "TID1"}) { thread { isResolved } }
     t2: resolveReviewThread(input: {threadId: "TID2"}) { thread { isResolved } }
   }' --silent
   ```

   **PR comment resolution:**

   PR comments don't get individual replies. Track part resolution state:

   - When first part of a comment is processed: add reaction (once per comment)
   - When ALL parts are resolved (addressed, dismissed, prior-fix): minimize the comment
   - If ANY part is deferred: comment stays visible (not minimized)

   ```bash
   # Reaction (once per comment, on first part)
   gh api graphql -f query='
   mutation($commentId: ID!) {
     addReaction(input: {subjectId: $commentId, content: THUMBS_UP}) {
       reaction { content }
     }
   }' -f commentId="$COMMENT_NODE_ID" --silent

   # Minimize (after all parts processed, if eligible)
   gh api graphql -f query='
   mutation($commentId: ID!) {
     minimizeComment(input: {subjectId: $commentId, classifier: RESOLVED}) {
       minimizedComment { isMinimized }
     }
   }' -f commentId="$COMMENT_NODE_ID" --silent
   ```

3. **Background resolution** (incremental mode):

   Use Claude Code's `run_in_background: true` parameter to run resolution while presenting next item:
   - Start background task for GitHub ops
   - Present next item to user immediately (no waiting)
   - Verify background task completed before summary

4. Mark task as completed in TodoWrite.

**Tracking:** Store `{item_id, action, commit_sha, thread_url}` for summary comment generation.

**Performance notes**:

- Pure GraphQL: single API surface, single ID type (node IDs)
- Batched mutations reduce HTTP round-trips
- `--silent` suppresses verbose JSON responses
- Background tasks eliminate user wait time between items

**Error handling**: If any API call fails:

- Show the error to user
- Ask: "Retry / Skip resolution / Abort session?"

#### 4f. Move to Next

Flow summary:

- **Go with suggestion**: Same as the suggested action
- **Address**: 4a → 4b → 4c → 4d → 4e → 4f (code change, close thread)
- **Dismiss**: 4a → 4b → 4e → 4f (no code, close thread)
- **Prior fix**: 4a → 4b → 4e → 4f (no code, close thread)
- **Defer**: 4a → 4b → 4f (no code, thread stays open for manual handling)
- **Discuss**: 4a → 4b → conversation → user chooses action → proceed accordingly
- **Abort**: 4a → 4b → jump to step 5

### 5. Summary

**Batch mode (`--batch`)**: Before showing the summary, execute all pending GitHub operations:

1. Show pending operations for confirmation:

   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   PENDING OPERATIONS                             N items → M threads
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   #1  ADDRESSED  @copilot
       └─ "Selector runs before early return"

       > Moved early return above selector call.

   #2  DISMISSED  @copilot (3 threads)
       ├─ "aria-label for filter button"
       ├─ "aria-label for dropdown buttons"
       └─ "ARIA menu roles"

       > Out of scope - accessibility strategy pending (HEA-3834).

   ...
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   ```

2. Use AskUserQuestion to let user select which items to execute (all selected by default, can deselect to skip). Include "Edit replies" and "Abort" as additional options.

3. If "Edit replies" selected: Let user modify reply text for specific items, then re-present selection.

4. If confirmed, execute all operations with progress indicator:

   ```
   Resolving threads... [████████░░] 8/10
   ```

5. Continue to summary display.

**Incremental mode**: Verify any background resolution tasks completed, then show summary.

**Summary comment** (posted if `POST_SUMMARY` selected and any Address actions):

1. Compose draft from all actions:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PR SUMMARY COMMENT (draft)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Feedback Summary

### Review Threads
- [Add null check](https://...) → [`abc1234`](https://github.com/.../commit/abc1234)
- [Also null check here](https://...) → [`abc1234`](https://github.com/.../commit/abc1234)

### PR Comments
- [Add loading state](https://...) → [`def5678`](https://github.com/.../commit/def5678)

### Deferred
- [Complex refactor needed](https://...) - left open for manual handling

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

2. Show draft to user for review. If user wants to edit, adjust content.

3. Format rules:
   - Group by: Review Threads, PR Comments, Deferred
   - Each addressed item links to thread AND commit (if commits enabled)
   - Grouped items sharing a commit show same commit link
   - Deferred items listed separately, no commit link
   - Dismissed/Prior-fix items omitted entirely
   - If `--no-commit` or no commits made, omit commit links
   - Omit empty sections

4. Post via GraphQL:

```bash
gh api graphql -f query='
mutation($prId: ID!, $body: String!) {
  addComment(input: {subjectId: $prId, body: $body}) {
    commentEdge { node { id url } }
  }
}' -f prId="$PR_NODE_ID" -f body="$SUMMARY_BODY" --silent
```

**Batch mode:** Include summary comment in pending operations for batch confirmation.

After all threads processed (or aborted):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY                                        N items → M threads
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

─── CLOSED (X threads) ────────────────────────────────────────────

#1  ADDRESSED  @author
    └─ "Truncated feedback summary..."
        https://github.com/owner/repo/pull/NNN#discussion_rNNNNNN

    > Reply text that was posted.

#2  DISMISSED  @author
    ├─ "First thread feedback summary"
    │   https://github.com/owner/repo/pull/NNN#discussion_rNNNNNN
    ├─ "Second thread feedback summary"
    │   https://github.com/owner/repo/pull/NNN#discussion_rNNNNNN
    └─ "Third thread feedback summary"
        https://github.com/owner/repo/pull/NNN#discussion_rNNNNNN

    > Reply posted to all threads.

#3  PRIOR FIX  @author
    └─ "Feedback that was already addressed"
        https://github.com/owner/repo/pull/NNN#discussion_rNNNNNN

    > Fixed in abc123.

─── REMAINS OPEN (Y threads) ──────────────────────────────────────

#4  DEFERRED  @author
    └─ "Complex issue needing manual review"
        https://github.com/owner/repo/pull/NNN#discussion_rNNNNNN

─── Artifacts ─────────────────────────────────────────────────────
  • [any files created/modified]
  • [any issues created]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Summary structure**:

| Element              | Description                                                       |
| -------------------- | ----------------------------------------------------------------- |
| Header               | `SUMMARY` left, `N items → M threads` right-aligned               |
| CLOSED section       | Items where thread was resolved (Addressed, Dismissed, Prior fix) |
| REMAINS OPEN section | Items where thread stays open (Deferred, Aborted)                 |
| Artifacts section    | Only if files modified or issues created                          |

**Item format**:

```
#N  ACTION  @author
    ├─ "Truncated feedback summary (~40 chars)"
    │   https://full-github-url-to-thread
    └─ "Another thread if grouped"
        https://full-github-url-to-thread

    > Reply text that was posted (or "(no reply)" if none)
```

- Item line: `#N  ACTION  @author` (no file names)
- Thread lines: truncated feedback summary + full clickable URL
- Tree connectors: `├─` / `└─` / `│` for visual hierarchy
- Reply block: quoted text of what was posted, for spot-checking

**Notes**:

- Items grouped by outcome (CLOSED vs REMAINS OPEN), not processing order
- Thread count in section header (visually self-evident from tree)
- Full URLs required (must be cmd-clickable)
- Reply block shows what user authored into the PR

**End of session** (no prompts - executes upfront selections):

1. If `SESSION_PREFS.post_summary` is true and any Address actions:
   - Post summary comment via GraphQL
   - Display: `Posted summary comment: <url>`

2. If `SESSION_PREFS.push_commits` is true and commits were made:
   - Push to remote: `git push`
   - Display: `Pushed N commits to origin/<branch>`

3. Display terminal summary (existing format)

**No additional prompts** - session preferences were collected upfront.

## Operations

| Action             | Description                                        |
| ------------------ | -------------------------------------------------- |
| Go with suggestion | Accept suggested action + response from analysis   |
| Address            | Plan and implement fix with user approval          |
| Dismiss            | Invalid/out-of-scope, close thread without changes |
| Prior fix          | Already fixed earlier, close thread                |
| Defer              | Too complex, leave thread open for manual handling |
| Discuss            | Talk through approach before deciding              |
| Abort              | Stop processing and show summary                   |

## Examples

```bash
# Process all Copilot feedback
/resolve-review --author=copilot

# Process feedback from specific reviewer
/resolve-review --author=ceremonious

# Process all feedback from current PR
/resolve-review

# Process feedback from specific PR
/resolve-review --pr=626

# Combine: Copilot feedback on specific PR
/resolve-review --author=copilot --pr=626

# Include your own comments (for testing)
/resolve-review --self

# Test against specific PR including own feedback
/resolve-review --self --pr=456
```

## Notes

- Requires `gh` CLI authenticated: `gh auth status`
- Thread resolution requires write access to the repo
- See **Field mapping** table in step 1 for which IDs to use where
- If a thread was resolved by someone else mid-session, the resolve call will succeed silently (idempotent)
- Copilot's login is `copilot-pull-request-reviewer` but `--author=copilot` should match it (case-insensitive contains)
- Outdated threads (`isOutdated: true`) may reference code that has moved or changed - verify before applying fixes
- PR comments use `minimizeComment` with `RESOLVED` classifier - comment becomes collapsed but expandable
- Multi-point PR comments are split into parts - each part is processed separately
- Summary comment is always posted if any items were addressed (provides consolidated reference)
- `--self` flag is useful for testing or when reviewing your own feedback/notes

## Reply Tone

PR replies come from the user's GitHub account. Keep them:

- Brief (1-2 sentences)
- Direct and factual
- Reference commits/code when relevant
- No AI pleasantries ("Great catch!", "Thanks for pointing this out!")
- No hedging ("I think", "perhaps", "might")
- Human but utilitarian

**Good examples**:

- "Fixed in abc123."
- "Moved early return above the selector call."
- "Intentional - added comment for clarity."
- "Out of scope for this PR, tracking in HEA-1234."

## Critical Rules

1. **NEVER make code changes without user approval** - Always present plan first
2. **ONE item at a time** - Complete full loop before moving to next
3. **Defer = thread stays open** - User must handle manually later
4. **Dismiss/Prior fix = thread closes** - No code changes, but thread is resolved
5. **Only unresolved threads** - Never show already-resolved threads
6. **Resolve = thumbs up + optional reply + mark thread resolved**
7. **User controls pace** - Wait for user input at each decision point
8. **Abort exits cleanly** - Show summary of what was done

## Appendix: API Strategy

**Principle:** Use pure GraphQL for all GitHub operations. Single API surface, single ID type (node IDs), single request per resolution batch.

**Rationale:**
- GraphQL mutations can be batched into one HTTP request
- Only need node IDs (`id` field), not database IDs
- Consistent approach across review threads and PR comments
- Easier to reason about and maintain

**Available mutations:**

| Operation | Mutation | Input |
|-----------|----------|-------|
| Add reaction | `addReaction` | `subjectId`, `content` |
| Reply to review thread | `addPullRequestReviewComment` | `pullRequestId`, `inReplyTo`, `body` |
| Resolve thread | `resolveReviewThread` | `threadId` |
| Minimize PR comment | `minimizeComment` | `subjectId`, `classifier` |
| Post PR comment | `addComment` | `subjectId` (PR ID), `body` |

**ID types:**

| Field | Used for |
|-------|----------|
| `pullRequest.id` | Reply target, summary comment target |
| `reviewThread.id` | Resolve thread |
| `comment.id` (in thread) | Reaction, reply inReplyTo |
| `comment.id` (PR comment) | Reaction, minimize |
