---
name: github-pr-review
description: Post PR review comments using the GitHub API with inline comments, suggestions, and priority labels.
triggers:
- /github-pr-review
---

# GitHub PR Review

Post structured code review feedback using the GitHub API with inline comments on specific lines.

## Key Rule: One API Call

Bundle ALL comments into a **single review API call**. Do not post comments individually.

## Posting a Review

Use the GitHub CLI (`gh`). The `GITHUB_TOKEN` is automatically available.

```bash
gh api \
  -X POST \
  repos/{owner}/{repo}/pulls/{pr_number}/reviews \
  -f commit_id='{commit_sha}' \
  -f event='COMMENT' \
  -f body='Brief 1-3 sentence summary.' \
  -f comments[][path]='path/to/file.py' \
  -F comments[][line]=42 \
  -f comments[][side]='RIGHT' \
  -f comments[][body]='🟠 Important: Your comment here.' \
  -f comments[][path]='another/file.js' \
  -F comments[][line]=15 \
  -f comments[][side]='RIGHT' \
  -f comments[][body]='🟡 Suggestion: Another comment.'
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `commit_id` | Commit SHA to comment on (use `git rev-parse HEAD`) |
| `event` | `COMMENT`, `APPROVE`, or `REQUEST_CHANGES` |
| `path` | File path as shown in the diff |
| `line` | Line number in the NEW version (right side of diff) |
| `side` | `RIGHT` for new/added lines, `LEFT` for deleted lines |
| `body` | Comment text with priority label |

### Multi-Line Comments

For comments spanning multiple lines, add `start_line` to specify the range:

```bash
  -f comments[][path]='path/to/file.py' \
  -F comments[][start_line]=10 \
  -F comments[][line]=12 \
  -f comments[][side]='RIGHT' \
  -f comments[][body]='🟡 Suggestion: Refactor this block:

```suggestion
line_one = "new"
line_two = "code"
line_three = "here"
```'
```

**Important**: The suggestion must have the same number of lines as the range (e.g., lines 10-12 = 3 lines).

## Priority Labels

Start each comment with a priority label. **Minimize nits** - leave minor style issues to linters.

| Label | When to Use |
|-------|-------------|
| 🔴 **Critical** | Must fix: security vulnerabilities, bugs, data loss risks |
| 🟠 **Important** | Should fix: logic errors, performance issues, missing error handling |
| 🟡 **Suggestion** | Worth considering: significant improvements to clarity or maintainability |
| 🟢 **Nit** | Optional: minor style preferences (use sparingly) |

**Example:**
```
🟠 Important: This function doesn't handle None, which could cause an AttributeError.

```suggestion
if user is None:
    raise ValueError("User cannot be None")
```
```

## GitHub Suggestions

For small code changes, use the suggestion syntax for one-click apply:

~~~
```suggestion
improved_code_here()
```
~~~

Use suggestions for: renaming, typos, small refactors (1-5 lines), type hints, docstrings.

Avoid for: large refactors, architectural changes, ambiguous improvements.

## Finding Line Numbers

```bash
# From diff header: @@ -old_start,old_count +new_start,new_count @@
# Count from new_start for added/modified lines

grep -n "pattern" filename     # Find line number
head -n 42 filename | tail -1  # Verify line content
```

## Fallback: curl

If `gh` is unavailable:

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews" \
  -d '{
    "commit_id": "{commit_sha}",
    "event": "COMMENT",
    "body": "Review summary.",
    "comments": [
      {"path": "file.py", "line": 42, "side": "RIGHT", "body": "Comment"},
      {"path": "file.py", "start_line": 10, "line": 12, "side": "RIGHT", "body": "Multi-line"}
    ]
  }'
```

## Summary

1. Analyze the code and identify important issues (minimize nits)
2. Post **ONE** review with all inline comments bundled
3. Use priority labels (🔴🟠🟡🟢) on every comment
4. Use suggestion syntax for concrete code changes
5. Keep the review body brief (details go in inline comments)
6. If no issues: post a short message
