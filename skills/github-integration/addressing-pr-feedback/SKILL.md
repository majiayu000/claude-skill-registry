---
name: addressing-pr-feedback
description: Fetches, organizes, and addresses PR review comments from GitHub. Use when user asks to review PR comments, fix PR feedback, check what reviewers said, address review comments, or handle bot suggestions on a pull request. Triggers on "review PR", "fix comments", "PR feedback", "what did reviewers say", "address PR feedback", "check PR comments".
user_invocable: true
---

# Addressing PR Feedback

## Overview

Fetch PR review comments, separate bot suggestions from human feedback, present a summary, then let the user select which comments to address.

## Workflow

1. **Identify branch** → from user input or `git branch --show-current`
2. **Find PR** → `gh pr list --head <branch> --json number,title,url --jq '.[0]'`
3. **Fetch all comments** → review comments, issue comments, review summaries
4. **Group by reviewer type** → human reviewers (high priority) vs bots (suggestions)
5. **Present summary** → counts, timestamps, outdated status
6. **User selects** → checkbox multi-select via AskUserQuestion
7. **Fix selected** → read file, apply fix, optionally reply to comment

## Fetching Comments

```bash
# Inline review comments (on specific code lines)
gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/comments

# General PR comments
gh api repos/{owner}/{repo}/issues/<PR_NUMBER>/comments

# Review summaries
gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/reviews
```

**Key fields:**
- `created_at` — display as relative time ("2 hours ago")
- `position` — null means outdated (code changed since comment)
- `in_reply_to_id` — reply thread, group with parent
- `path` — file the comment is on

## Grouping Comments

| Category | Detection | Priority |
|----------|-----------|----------|
| **Bot** | Username contains `[bot]`, ends with `bot`, or is a known CI tool | Lower — automated suggestions |
| **Human** | All other usernames | Higher — requires response |

## Presenting Summary

```
## PR #123: "Add authentication flow"

### Human Reviewers (2 comments) — HIGH PRIORITY
- @alice: 1 comment on src/auth.ts (2 days ago)
- @bob: 1 comment on src/utils.ts (5 hours ago) ⚠️ OUTDATED

### Bot Suggestions (5 comments)
- 3 style/formatting (1 day ago)
- 2 potential improvements (1 day ago) ⚠️ 1 OUTDATED
```

Mark comments as ⚠️ OUTDATED when `position` is null (code changed since the comment was posted).

## User Selection

Use `AskUserQuestion` with `multiSelect: true`:

```
Which comments do you want me to address?
[ ] @alice: "Consider adding error handling for timeout" (2 days ago)
[ ] @bob: "This function could be simplified" (5h ago) ⚠️ OUTDATED
[ ] bot: "Missing return type annotation" (3 similar, 1 day ago)
```

Group similar bot comments to reduce noise. Show relative timestamps. Mark outdated comments — the user may skip these.

## Anti-Patterns

**Dumping all comments raw:** Always summarize and group first.

**Treating all comments equally:** Human comments get priority display over bot suggestions.

**Open-ended questions:** Use checkbox selection, not "which ones do you want me to fix?"

**Fixing without asking:** Always let the user select which comments to address.
