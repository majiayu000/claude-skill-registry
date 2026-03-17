---
name: reply-comments
description: Reply to PR review comments after addressing them. Resolves conversations where changes were made. Uses polite tone for humans, terse factual responses for AI bots.
---

# Reply to Review Comments

Reply to PR review comments after addressing the feedback. Use this after `/review-comments` to close the feedback loop.

## Usage

```
/reply-comments
/reply-comments 123    # Specific PR number
```

## Instructions

### 1. Find the PR

If no PR number provided, get it from the current branch:

```bash
gh pr view --json number,url,title,headRepositoryOwner,headRepository \
  --jq '{number, url, title, owner: .headRepositoryOwner.login, repo: .headRepository.name}'
```

### 2. Fetch Review Comments

Get all review comments with their thread/resolution status:

```bash
# Get inline code review comments
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments \
  --jq '.[] | {id, path, line, body, user: .user.login, in_reply_to_id, created_at}'
```

### 3. Get Recent Commits

Check what was recently committed to understand which comments were addressed:

```bash
# Get recent commit messages and changed files
git log --oneline -10
git diff HEAD~1 --name-only
```

### 4. Identify Addressed Comments

For each review comment, determine if it was addressed by:
- Checking if the file/line was modified in recent commits
- Matching commit messages to comment content (e.g., "address review feedback")
- Looking for code changes that match suggested fixes

### 5. Compose Replies

Use different tones based on the reviewer:

**AI Bots** (amazon-q-developer[bot], copilot[bot], github-actions[bot], etc.):
- Terse, factual responses
- Just state what was done
- Examples:
  - "Fixed."
  - "Done."
  - "Changed to use `const`."
  - "Added null check."
  - "Not applicable - already handled by X."

**Human Reviewers** (anyone without [bot] suffix):
- Short but polite responses
- Acknowledge their feedback
- Examples:
  - "Good catch, fixed!"
  - "Thanks - updated."
  - "Done, good suggestion."
  - "Makes sense, changed it."
  - "Addressed in latest commit."

For comments NOT addressed (intentionally skipped):
- "Keeping as-is because {brief reason}."
- "Intentional - {brief explanation}."

### 6. Post Replies

Reply to each comment:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -f body="{reply_text}"
```

### 7. Resolve Threads (if addressed)

Use GraphQL to resolve review threads where changes were made:

```bash
# First, get the thread ID for the comment
gh api graphql -f query='
  query($owner: String!, $repo: String!, $pr: Int!) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $pr) {
        reviewThreads(first: 100) {
          nodes {
            id
            isResolved
            comments(first: 1) {
              nodes {
                databaseId
                body
              }
            }
          }
        }
      }
    }
  }
' -f owner="{owner}" -f repo="{repo}" -F pr={pr_number}

# Then resolve each thread that was addressed
gh api graphql -f query='
  mutation($threadId: ID!) {
    resolveReviewThread(input: {threadId: $threadId}) {
      thread {
        isResolved
      }
    }
  }
' -f threadId="{thread_id}"
```

### 8. Summary

Report what was done:

```
Replied to 6 comments:
- amazon-q-developer[bot]: 3 (all resolved)
- @username: 2 (2 resolved, 1 kept as-is)
- copilot[bot]: 1 (resolved)
```
