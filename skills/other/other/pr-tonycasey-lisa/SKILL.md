---
name: pr
description: "PR workflow operations: create PRs, check status, link PRs to issues, poll for comments, address feedback, watch PRs, save notes to memory. Triggers on 'pr create', 'pr checks', 'pr link', 'pr poll', 'pr address', 'pr comments', 'pr remember', 'watch pr', 'watching'."
---

## Purpose
Model-neutral helper for GitHub PR workflow operations including creating PRs with auto-generated content, checking CI status, linking PRs to issues, polling for and addressing review comments, tracking PRs you're working on, and saving PR notes to memory.

## Triggers
Use when the user says: "create pr", "pr create", "pr checks", "check pr", "pr link", "link pr", "link pr to issue", "pr poll", "poll pr", "pr address", "address comments", "pr comments", "view comments", "watch pr", "unwatch pr", "watching", "what prs am i watching", "pr status", "pr remember", "remember pr", "save pr note".

## How to use

### Create a PR
Create a PR with auto-generated body, issue linking, and auto-watch:

```bash
# Create PR from current branch (auto-detects base branch and linked issues)
lisa pr create

# Create PR linking to specific issues
lisa pr create --issue 40 --issue 41

# Create PR with custom title and base branch
lisa pr create --title "feat: add pr create command" --base develop

# Create as draft PR
lisa pr create --draft

# Skip auto-watching the PR
lisa pr create --no-watch

# Skip commenting on linked issues
lisa pr create --no-comment

# Output as JSON
lisa pr create --json
```

**Features:**
- **Auto-detects linked issues** from branch name (supports: `15`, `15-description`, `feature/15`, `issue-15`, `fix/#15`)
- **Auto-generates PR body** with Summary (from commits), Test Coverage (test files changed), and Linked Issues (`Closes #N`)
- **Comments on linked issues** with `PR: #N`
- **Auto-watches the PR** for future polling
- **Creates Neo4j relationships** (`CLOSES`) between PR and issues

**Output:**
```text
Created PR #51: https://github.com/owner/repo/pull/51
Linked issues: #40
```

### Check PR CI Status
Get the current status of CI checks for a PR:

```bash
# Check current repo's PR
lisa pr checks <PR_NUMBER>

# Check specific repo's PR
lisa pr checks <PR_NUMBER> --repo owner/repo

# Output as JSON
lisa pr checks <PR_NUMBER> --json
```

**Output:**
```text
PR #50 Checks
fix(github): prevent shell injection in GithubClient

✅ 2 passed, 0 failed

  ✓ ci/build
  ✓ security/gitguardian
```

### View PR Comments
Fetch and display PR review comments with triage status:

```bash
# View all comments
lisa pr comments <PR_NUMBER>

# View only pending comments
lisa pr comments <PR_NUMBER> --filter pending

# View only addressed comments
lisa pr comments <PR_NUMBER> --filter addressed

# Output as JSON
lisa pr comments <PR_NUMBER> --json
```

**Output:**
```text
PR: fix(github): prevent shell injection in GithubClient

Comments: 4 total (2 pending, 1 addressed, 1 resolved)

src/lib/infrastructure/github/GithubClient.ts
  :red_circle: Line:365 - @coderabbitai
    "Shell injection risk in command argument construction..."
  :yellow_circle: Line:138 - @coderabbitai (addressed)
    "The current escaping only handles double quotes..."
```

**Comment Status:**
- :red_circle: **pending** - Needs attention
- :yellow_circle: **addressed** - We replied, waiting for reviewer
- :white_check_mark: **resolved** - Reviewer marked as resolved

### Watch a PR
Start tracking a PR for updates (used by polling system):

```bash
# Watch a PR in current repo
lisa pr watch <PR_NUMBER>

# Watch a PR in specific repo
lisa pr watch <PR_NUMBER> --repo owner/repo
```

**Output:**
```text
Now watching PR #50: fix(github): prevent shell injection in GithubClient
```

### Unwatch a PR
Stop tracking a PR:

```bash
lisa pr unwatch <PR_NUMBER>
```

### Link PR to Issue
Create a CLOSES relationship between a PR and an issue:

```bash
# Link PR to issue in current repo
lisa pr link <PR_NUMBER> <ISSUE_NUMBER>

# Link in specific repo
lisa pr link <PR_NUMBER> <ISSUE_NUMBER> --repo owner/repo

# Skip commenting on the GitHub issue
lisa pr link <PR_NUMBER> <ISSUE_NUMBER> --no-comment

# Output as JSON
lisa pr link <PR_NUMBER> <ISSUE_NUMBER> --json
```

**Features:**
- Creates `CLOSES` relationship in Neo4j
- Comments on the GitHub issue with PR link (unless `--no-comment`)
- Idempotent - running twice returns `alreadyLinked: true`
- Creates PR and Issue nodes if they don't exist

**Output:**
```text
✓ Linked PR #28 to Issue #15
  PR: https://github.com/owner/repo/pull/28
  Issue: https://github.com/owner/repo/issues/15
```

**Already linked:**
```text
⚠ PR #28 is already linked to Issue #15
```

### Remember a PR Note
Save notes, decisions, or learnings about a PR to memory:

```bash
# Save a note about a PR
lisa pr remember 50 "Learned to always reply inline to review comments"

# Save a note for a specific repo
lisa pr remember 50 "Key decision: use factory pattern" --repo owner/repo

# Output as JSON
lisa pr remember 50 "Important learning" --json
```

**Features:**
- Saves note to memory with PR context (number and title)
- Tags with `github:pr` and `github:pr:<number>` for retrieval
- Useful for capturing decisions, learnings, and patterns from PR reviews

**Output:**
```text
✓ Saved note for PR #50
  Fact: PR #50 (Fix auth bug): Learned to always reply inline to review comments
  Tags: github:pr, github:pr:50
```

### Memory Integration

PR workflow integrates with Lisa's memory system for automatic knowledge capture:

**Auto-capture on merge:**
When a watched PR is merged, it is automatically saved to memory with the `github:pr-merged` tag. This happens during `lisa pr poll` when the PR status changes to merged (requires memory to be configured).

**Retrieve PR memories:**
```bash
# Search for PR-related memories
lisa memory load --query "PR merged"

# Load recent memories (PR notes will have github:pr tags)
lisa memory load --cache
```

**Tags:**
- `github:pr` - General PR memory
- `github:pr:<number>` - Specific PR (e.g., `github:pr:50`)
- `github:pr-merged` - Auto-captured merged PR

### List Watched PRs
See all PRs you're currently watching:

```bash
# List all watched PRs
lisa pr watching

# Filter by repo
lisa pr watching --repo owner/repo

# Output as JSON
lisa pr watching --json
```

**Output:**
```text
Watching 3 PR(s)

:green_circle: #50 fix(github): prevent shell injection in GithubClient
   TonyCasey/lisa :white_check_mark:
:green_circle: #49 feat(dal): add PR entity types and Neo4j repository
   TonyCasey/lisa :white_check_mark:
:purple_circle: #48 feat: add session compaction detection
   TonyCasey/lisa :white_check_mark: (merged)
```

**PR Status Indicators:**
- :green_circle: Open
- :purple_circle: Merged
- :white_circle: Closed

**Checks Indicators:**
- :white_check_mark: All passing
- :x: Failures
- :hourglass: Pending

### Poll PR for Updates
Monitor a PR for new review comments with auto-address support:

```bash
# Poll a PR (auto-address enabled by default)
lisa pr poll <PR_NUMBER>

# Poll without auto-address output
lisa pr poll <PR_NUMBER> --no-auto-address

# Output as JSON
lisa pr poll <PR_NUMBER> --json
```

**Features:**
- Detects new comments since last poll
- Auto-address outputs formatted comment details when new comments found
- Tracks comment resolution status when available (resolution detection pending)
- Shows which comments need attention

**Output:**
```text
PR #50: fix(github): prevent shell injection
New comments: 2

src/lib/GithubClient.ts:365
  @coderabbitai: "Shell injection risk in command argument..."
```

### Address PR Comments
Get formatted instructions for addressing specific comments:

```bash
# Get address instructions for a PR
lisa pr address <PR_NUMBER>

# Include more context lines around the code
lisa pr address <PR_NUMBER> --context 10
```

## PR Review Workflow

The recommended workflow for handling PR review comments:

### 1. Poll for new comments
```bash
lisa pr poll 50
```

### 2. Acknowledge the comment
Add an 👀 (eyes) emoji reaction to show you've seen the comment:
```bash
gh api repos/owner/repo/pulls/comments/COMMENT_ID/reactions -X POST -f content="eyes"
```

### 3. Address the feedback
- Read and understand the suggestion
- Make the requested code changes
- Commit with a descriptive message

### 4. Reply to the comment
Reply inline explaining what was done:
```bash
gh api repos/owner/repo/pulls/comments/COMMENT_ID/replies -X POST -f body="Fixed in commit abc123 - added try/catch with proper error logging"
```

### 5. Push and poll again
```bash
git push
lisa pr poll 50
```

### 6. Repeat
Continue polling and addressing comments until:
- All comments are resolved
- Reviewer approves the PR
- Any disagreements are discussed and concluded

**Example session:**
```bash
# Create PR and start watching
lisa pr create
# -> Created PR #50

# Poll for review comments
lisa pr poll 50
# -> New comment from @reviewer on line 42

# Acknowledge with eyes emoji
gh api repos/owner/repo/pulls/comments/12345/reactions -X POST -f content="eyes"

# Fix the code
vim src/file.ts
git add . && git commit -m "fix: add error handling per review"
git push

# Reply to the comment
gh api repos/owner/repo/pulls/comments/12345/replies -X POST -f body="Added try/catch - fixed in abc123"

# Poll again for response
lisa pr poll 50
# -> Comment resolved by reviewer
```

## I/O Contract

### lisa pr create
```json
{
  "success": true,
  "message": "Created PR #51: https://github.com/owner/repo/pull/51",
  "pr": {
    "number": 51,
    "url": "https://github.com/owner/repo/pull/51",
    "title": "feat: add pr create command",
    "repo": "owner/repo"
  },
  "linkedIssues": [40, 41],
  "body": "## Summary\n- feat: add feature\n\n## Linked Issues\nCloses #40\nCloses #41"
}
```

### lisa pr checks
```json
{
  "repo": "owner/repo",
  "prNumber": 50,
  "title": "PR title",
  "overallStatus": "success",
  "checks": [
    {"name": "ci/build", "status": "success", "detailsUrl": "..."}
  ],
  "summary": ":white_check_mark: 2 passed, 0 failed"
}
```

### lisa pr comments
```json
{
  "repo": "owner/repo",
  "prNumber": 50,
  "title": "PR title",
  "comments": [
    {
      "id": 12345,
      "file": "src/file.ts",
      "line": 42,
      "author": "reviewer",
      "body": "Comment text",
      "status": "pending",
      "htmlUrl": "..."
    }
  ],
  "summary": {"total": 4, "pending": 2, "addressed": 1, "resolved": 1}
}
```

### lisa pr watching
```json
{
  "action": "list",
  "success": true,
  "message": "Watching 3 PR(s)",
  "watchedPrs": [
    {
      "number": 50,
      "repo": "owner/repo",
      "title": "PR title",
      "status": "open",
      "checksStatus": "success",
      "unresolvedComments": 2,
      "watchingSince": "2026-01-26T10:00:00Z"
    }
  ]
}
```

### lisa pr poll
```json
{
  "action": "poll",
  "success": true,
  "repo": "owner/repo",
  "prNumber": 50,
  "title": "PR title",
  "hasNewComments": true,
  "newCommentCount": 2,
  "comments": [
    {
      "id": 12345,
      "file": "src/file.ts",
      "line": 42,
      "author": "reviewer",
      "body": "Comment text",
      "status": "pending"
    }
  ],
  "addressOutput": "## PR #50 Comments\n\n### src/file.ts:42\n..."
}
```

### lisa pr address
```json
{
  "action": "address",
  "success": true,
  "repo": "owner/repo",
  "prNumber": 50,
  "title": "PR title",
  "pendingComments": [
    {
      "id": 12345,
      "file": "src/file.ts",
      "line": 42,
      "author": "reviewer",
      "body": "Comment text",
      "codeContext": "function example() {\n  // line 42\n}"
    }
  ],
  "formattedOutput": "..."
}
```

### lisa pr link
```json
{
  "success": true,
  "message": "Linked PR #28 to Issue #15",
  "pr": {
    "number": 28,
    "repo": "owner/repo",
    "title": "Fix authentication bug",
    "url": "https://github.com/owner/repo/pull/28"
  },
  "issue": {
    "number": 15,
    "repo": "owner/repo",
    "title": "Authentication fails on mobile",
    "url": "https://github.com/owner/repo/issues/15"
  },
  "alreadyLinked": false
}
```

### lisa pr remember
```json
{
  "success": true,
  "message": "Saved note for PR #50",
  "pr": {
    "number": 50,
    "repo": "owner/repo",
    "title": "Fix auth bug"
  },
  "fact": "PR #50 (Fix auth bug): Learned to always reply inline",
  "tags": ["github:pr", "github:pr:50"]
}
```

## Cross-model checklist
- Claude: Use concise lisa pr commands; prefer --json for programmatic access
- Gemini: Use explicit commands; avoid model-specific tokens
- All: Neo4j must be running for watch/watching commands (lisa doctor to verify)

## Related Skills
- `/github` - For GitHub Issues, Projects, version bumping, and CI retriggers
