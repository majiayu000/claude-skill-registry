---
name: github
version: 3.1.0
model: claude-opus-4-5
description: Execute GitHub operations (PRs, issues, milestones, labels, comments, merges)
  using PowerShell scripts with structured output and error handling. Use when working
  with pull requests, issues, review comments, CI checks, or milestones instead of raw gh.
license: MIT
metadata:
  domains:
    - github
    - pr
    - issue
    - labels
    - milestones
    - comments
    - reactions
  type: integration
  complexity: intermediate
  generator:
    keep_headings:
      - Decision Tree
      - Script Reference
      - Output Format
      - See Also
---
# GitHub Skill

Use these scripts instead of raw `gh` commands for consistent error handling and structured output.

---

## Triggers

| Phrase | Operation |
|--------|-----------|
| `get PR context for #123` | Get-PRContext.ps1 |
| `respond to review comments` | Post-PRCommentReply.ps1 |
| `check CI status` | Get-PRChecks.ps1 |
| `add label to issue` | Set-IssueLabels.ps1 |
| `assign milestone` | Set-ItemMilestone.ps1 |

---

## Decision Tree

```text
Need GitHub data?
├─ List PRs (filtered) → Get-PullRequests.ps1
├─ PR info/diff → Get-PRContext.ps1
├─ CI check status → Get-PRChecks.ps1
├─ CI failure logs → Get-PRCheckLogs.ps1
├─ Review comments → Get-PRReviewComments.ps1
├─ Review threads → Get-PRReviewThreads.ps1
├─ Unique reviewers → Get-PRReviewers.ps1
├─ Unaddressed bot comments → Get-UnaddressedComments.ps1
├─ PR merged check → Test-PRMerged.ps1
├─ Copilot follow-up PRs → Detect-CopilotFollowUpPR.ps1
├─ Issue info → Get-IssueContext.ps1
├─ Merge readiness check → Test-PRMergeReady.ps1
├─ Latest milestone → Get-LatestSemanticMilestone.ps1
└─ Need to take action?
   ├─ Create issue → New-Issue.ps1
   ├─ Create PR → New-PR.ps1
   ├─ Reply to review → Post-PRCommentReply.ps1
   ├─ Reply to thread (GraphQL) → Add-PRReviewThreadReply.ps1
   ├─ Comment on issue → Post-IssueComment.ps1
   ├─ Add reaction → Add-CommentReaction.ps1
   ├─ Apply labels → Set-IssueLabels.ps1
   ├─ Set issue milestone → Set-IssueMilestone.ps1
   ├─ Set PR/issue milestone (auto-detect) → Set-ItemMilestone.ps1
   ├─ Assign issue → Set-IssueAssignee.ps1
   ├─ Resolve threads → Resolve-PRReviewThread.ps1
   ├─ Process AI triage → Invoke-PRCommentProcessing.ps1
   ├─ Assign Copilot → Invoke-CopilotAssignment.ps1
   ├─ Enable/disable auto-merge → Set-PRAutoMerge.ps1
   ├─ Close PR → Close-PR.ps1
   └─ Merge PR → Merge-PR.ps1
```

---

## Script Reference

### PR Operations (`scripts/pr/`)

| Script | Purpose | Key Parameters |
|--------|---------|----------------|
| `Get-PullRequests.ps1` | List PRs with filters | `-State`, `-Label`, `-Author`, `-Base`, `-Head`, `-Limit` |
| `Get-PRContext.ps1` | PR metadata, diff, files | `-PullRequest`, `-IncludeChangedFiles`, `-IncludeDiff` |
| `Get-PRChecks.ps1` | CI check status, polling | `-PullRequest`, `-Wait`, `-TimeoutSeconds`, `-RequiredOnly` |
| `Get-PRCheckLogs.ps1` | Fetch logs from failing CI checks | `-PullRequest`, `-MaxLines`, `-ContextLines` |
| `Get-PRReviewComments.ps1` | Paginated review comments with stale detection | `-PullRequest`, `-IncludeIssueComments`, `-DetectStale`, `-ExcludeStale`, `-OnlyStale` |
| `Get-PRReviewThreads.ps1` | Thread-level review data | `-PullRequest`, `-UnresolvedOnly` |
| `Get-PRReviewers.ps1` | Enumerate unique reviewers | `-PullRequest`, `-ExcludeBots` |
| `Get-UnaddressedComments.ps1` | Bot comments needing attention | `-PullRequest` |
| `Get-UnresolvedReviewThreads.ps1` | Unresolved thread IDs | `-PullRequest` |
| `Test-PRMerged.ps1` | Check if PR is merged | `-PullRequest` |
| `Detect-CopilotFollowUpPR.ps1` | Detect Copilot follow-up PRs | `-PRNumber`, `-Owner`, `-Repo` |
| `Post-PRCommentReply.ps1` | Thread-preserving replies | `-PullRequest`, `-CommentId`, `-Body` |
| `Add-PRReviewThreadReply.ps1` | Reply to thread by ID (GraphQL) | `-ThreadId`, `-Body`, `-Resolve` |
| `Resolve-PRReviewThread.ps1` | Mark threads resolved | `-ThreadId` or `-PullRequest -All` |
| `Unresolve-PRReviewThread.ps1` | Mark threads unresolved | `-ThreadId` or `-PullRequest -All` |
| `Get-ThreadById.ps1` | Get single thread by ID | `-ThreadId` |
| `Get-ThreadConversationHistory.ps1` | Full thread comment history | `-ThreadId`, `-IncludeMinimized` |
| `Test-PRMergeReady.ps1` | Check merge readiness | `-PullRequest`, `-IgnoreCI`, `-IgnoreThreads` |
| `Set-PRAutoMerge.ps1` | Enable/disable auto-merge | `-PullRequest`, `-Enable`/`-Disable`, `-MergeMethod` |
| `Invoke-PRCommentProcessing.ps1` | Process AI triage output | `-PRNumber`, `-Verdict`, `-FindingsJson` |
| `New-PR.ps1` | Create PR with validation | `-Title`, `-Body`, `-Base` |
| `Close-PR.ps1` | Close PR with comment | `-PullRequest`, `-Comment` |
| `Merge-PR.ps1` | Merge with strategy | `-PullRequest`, `-Strategy`, `-DeleteBranch`, `-Auto` |

### Issue Operations (`scripts/issue/`)

| Script | Purpose | Key Parameters |
|--------|---------|----------------|
| `Get-IssueContext.ps1` | Issue metadata | `-Issue` |
| `New-Issue.ps1` | Create new issue | `-Title`, `-Body`, `-Labels` |
| `Set-IssueLabels.ps1` | Apply labels (auto-create) | `-Issue`, `-Labels`, `-Priority` |
| `Set-IssueMilestone.ps1` | Assign milestone | `-Issue`, `-Milestone` |
| `Post-IssueComment.ps1` | Comments with idempotency | `-Issue`, `-Body`, `-Marker` |
| `Invoke-CopilotAssignment.ps1` | Synthesize context for Copilot | `-IssueNumber`, `-WhatIf` |
| `Set-IssueAssignee.ps1` | Assign users to issues | `-Issue`, `-Assignees` |

### Milestone Operations (`scripts/milestone/`)

| Script | Purpose | Key Parameters |
|--------|---------|----------------|
| `Get-LatestSemanticMilestone.ps1` | Detect latest semantic version milestone | `-Owner`, `-Repo` |
| `Set-ItemMilestone.ps1` | Assign milestone to PR/issue (auto-detect) | `-ItemType`, `-ItemNumber`, `-MilestoneTitle` |

### Reactions (`scripts/reactions/`)

| Script | Purpose | Key Parameters |
|--------|---------|----------------|
| `Add-CommentReaction.ps1` | Add emoji reactions (batch support) | `-CommentId[]`, `-Reaction`, `-CommentType` |

---

## Output Format

All scripts output structured JSON with `Success` boolean:

```powershell
$result = pwsh -NoProfile scripts/pr/Get-PRContext.ps1 -PullRequest 50 | ConvertFrom-Json
if ($result.Success) { ... }
```

---

## Process

This skill provides a toolkit of PowerShell scripts for GitHub operations. Use scripts directly or compose them into workflows.

**Basic Usage:**

1. Identify the operation needed using the Decision Tree
2. Find the corresponding script in the Script Reference
3. Call the script with required parameters
4. Parse the JSON output and check `Success` field

**Example Flow:**

```powershell
# Get PR context
$pr = pwsh scripts/pr/Get-PRContext.ps1 -PullRequest 123 | ConvertFrom-Json

# Check CI status
$checks = pwsh scripts/pr/Get-PRChecks.ps1 -PullRequest 123 | ConvertFrom-Json

# Add comment if needed
if ($checks.FailedCount -gt 0) {
    pwsh scripts/pr/Post-PRCommentReply.ps1 -PullRequest 123 -Body "CI failures detected"
}
```

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Raw `gh pr view` commands | No structured output | Use `Get-PRContext.ps1` |
| Raw `gh api` for comments | Doesn't preserve threading | Use `Post-PRCommentReply.ps1` |
| Replying to thread expecting auto-resolve | Replies DON'T auto-resolve threads | Use `Resolve-PRReviewThread.ps1` after reply |
| Inline issue creation | Missing validation | Use `New-Issue.ps1` |
| Multiple individual reactions | 88% slower | Use batch mode in `Add-CommentReaction.ps1` |
| Hardcoding owner/repo | Breaks in forks | Let scripts infer from `git remote` |
| Ignoring exit codes | Missing error handling | Check `$LASTEXITCODE` |
| Skipping idempotency markers | Duplicate comments | Use `-Marker` parameter |

---

## See Also

| Document | Content |
|----------|---------|
| [examples.md](references/examples.md) | Complete script examples |
| [patterns.md](references/patterns.md) | Reusable workflow patterns |
| [copilot-prompts.md](references/copilot-prompts.md) | Creating @copilot directives |
| [copilot-synthesis-guide.md](references/copilot-synthesis-guide.md) | Copilot context synthesis |
| [api-reference.md](references/api-reference.md) | Exit codes, API endpoints, troubleshooting |
| `modules/GitHubCore.psm1` | Shared helper functions |

---

## Verification

Before completing a GitHub operation:

- [ ] Correct script selected from Decision Tree
- [ ] Required parameters provided (PR/issue number)
- [ ] Response JSON parsed successfully
- [ ] `Success: true` in response
- [ ] State change verified (for mutating operations)
