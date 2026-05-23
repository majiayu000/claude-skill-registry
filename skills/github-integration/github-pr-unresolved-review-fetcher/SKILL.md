---
name: github-pr-unresolved-review-fetcher
description: Fetch unresolved PR review comments from GitHub. Use when working with pull request reviews, addressing review feedback, or checking outstanding review comments on a PR. Triggers on requests like "get PR reviews", "fetch review comments", "show unresolved comments", or "what feedback is pending on this PR".
---

# PR Review Fetcher

Fetch unresolved review comments from GitHub pull requests using GraphQL API.

## Usage

Run the script with owner, repo, and PR number:

```bash
bash scripts/fetch_unresolved_reviews.sh <owner> <repo> <pr_number>
```

Example:

```bash
bash scripts/fetch_unresolved_reviews.sh yaakaito aiblio 123
```

## Auto-detect from Current Branch

When working in a git repository with an open PR:

```bash
# Get current repo info
REPO_INFO=$(gh repo view --json owner,name -q '"\(.owner.login) \(.name)"')
OWNER=$(echo $REPO_INFO | cut -d' ' -f1)
REPO=$(echo $REPO_INFO | cut -d' ' -f2)

# Get PR number for current branch
PR_NUMBER=$(gh pr view --json number -q '.number')

# Fetch reviews
bash scripts/fetch_unresolved_reviews.sh "$OWNER" "$REPO" "$PR_NUMBER"
```

## Output Format

Returns XML-formatted review comments:

```xml
<review-comment>
  <file>src/example.ts</file>
  <line>42</line>
  <author>reviewer</author>
  <body>Consider using a more descriptive variable name here.</body>
</review-comment>
```

## Requirements

- `gh` CLI authenticated with GitHub
- `jq` for JSON processing
