---
name: "pr-comments"
description: "Review and triage PR comments interactively"
argument-hint: "[pr-number]"
---

Displays all comments (from users and bots) and test results for a pull request, then helps triage them interactively.

## Optional PR number from user input
"$ARGUMENTS"

### Argument Handling
- If PR number provided: Use specified PR
- If empty: Use PR for current branch (via `gh pr view`)

## Process

### Step 1: Determine PR Number
Get the PR number to query:
```bash
# If user provided PR number, use it; otherwise get current branch's PR
if [ -n "$ARGUMENTS" ]; then
  PR_NUM="$ARGUMENTS"
else
  PR_NUM=$(gh pr view --json number --jq '.number' 2>/dev/null)
  if [ -z "$PR_NUM" ]; then
    echo "Error: No PR number provided and current branch has no associated PR"
    exit 1
  fi
fi
```

### Step 2: Fetch All Data
Retrieve PR comments, review comments, and test results:
```bash
# Get basic PR info
PR_INFO=$(gh pr view "$PR_NUM" --json title,author,url)
PR_TITLE=$(echo "$PR_INFO" | jq -r '.title')
PR_URL=$(echo "$PR_INFO" | jq -r '.url')
PR_AUTHOR=$(echo "$PR_INFO" | jq -r '.author.login')

# Get PR issue comments (conversation tab)
COMMENTS=$(gh pr view "$PR_NUM" --json comments --jq '.comments[]? | "**[\(.author.login)]** _\(.createdAt)_\n\(.body)\n"')
if [ -z "$COMMENTS" ]; then
  COMMENTS="No comments found"
fi

# Get review comments with IDs (inline code comments)
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
REVIEW_COMMENTS=$(gh api "repos/$REPO/pulls/$PR_NUM/comments" --jq '.[]? | "[ID: \(.id)] **[\(.user.login)]** _\(.path):\(.line // .original_line)_\n\(.body)\n"')
if [ -z "$REVIEW_COMMENTS" ]; then
  REVIEW_COMMENTS="No review comments found"
fi

# Get test/check results
CHECKS=$(gh pr checks "$PR_NUM" --json name,status,conclusion,detailsUrl)
```

### Step 3: Display All Comments and Tests
Show structured report with all data:
```bash
cat <<EOF
# PR #$PR_NUM: $PR_TITLE

**Author**: $PR_AUTHOR
**URL**: $PR_URL

---

## Comments

$COMMENTS

---

## Review Comments

$REVIEW_COMMENTS

---

## Test Results

$(echo "$CHECKS" | jq -r '.[] | "- [\(.conclusion // .status | ascii_upcase)] **\(.name)**\n  \(.detailsUrl)"')

---
EOF
```

### Step 4: Interactive Triage
Ask user to categorize each comment:
- **What to fix?** - Comments that need to be addressed (leave as is)
- **What to ignore?** - Comments to ignore (resolve + comment "ignore")
- **What is outdated?** - Comments no longer relevant (resolve + comment "outdated")
- **What is fixed?** - Comments already addressed (comment "fixed")

### Step 5: Process User Decisions
For each category, execute the appropriate actions:

**Ignore comments:**
```bash
# For each comment ID to ignore
gh api "repos/$REPO/pulls/$PR_NUM/comments/$COMMENT_ID/replies" -f body="ignore"
# Mark as resolved if it's a review comment thread
```

**Fixed comments:**
```bash
# For each comment ID that's fixed
gh api "repos/$REPO/pulls/$PR_NUM/comments/$COMMENT_ID/replies" -f body="fixed"
```

**Outdated comments:**
```bash
# For each comment ID that's outdated
gh api "repos/$REPO/pulls/$PR_NUM/comments/$COMMENT_ID/replies" -f body="outdated"
# Mark as resolved
```

**Untouched comments:**
- Leave as is (no action needed)

### Step 6: Summary
Display summary of actions taken:
- X comments marked as ignore
- X comments marked as fixed
- X comments marked as outdated
- X comments left for review
