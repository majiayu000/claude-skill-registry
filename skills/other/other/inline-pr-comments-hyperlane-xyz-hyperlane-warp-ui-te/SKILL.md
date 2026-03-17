---
name: inline-pr-comments
description: Post inline PR review comments on specific lines. Use this skill to deliver code review feedback as inline comments rather than a single summary.
---

# Inline PR Comments Skill

Use this skill to post code review feedback as inline comments on specific lines in a PR.

## When to Use

- After completing a code review (use with /claude-review, /claude-security-review)
- When you have specific line-by-line feedback to deliver
- To make review feedback more actionable

## Instructions

Post a review with inline comments using `gh api`:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews --input - << 'EOF'
{
  "event": "COMMENT",
  "body": "Optional summary of overall findings",
  "comments": [
    {
      "path": "path/to/file.ts",
      "line": 42,
      "body": "Issue description and suggested fix"
    },
    {
      "path": "another/file.ts",
      "start_line": 10,
      "line": 15,
      "body": "Multi-line comment spanning lines 10-15"
    }
  ]
}
EOF
```

### Comment Fields

- `path` - File path relative to repo root
- `line` - Line number in the NEW version of the file (right side of diff)
- `start_line` + `line` - For comments spanning multiple lines
- `body` - Markdown-formatted feedback

### Limitations

- Can only comment on lines that appear in the diff (changed/added lines)
- Comments on unchanged lines will fail with "Line could not be resolved"

### Handling Non-Diff Findings

When you discover issues in code NOT changed by the PR:

1. **Include in summary body** - Always report in the `"body"` field
2. **Format clearly** - Use a dedicated section "## Observations Outside This PR"
3. **Be actionable** - Include file:line references so author can follow up
4. **Don't block** - These are informational; don't use `REQUEST_CHANGES` for non-diff issues

Example structure:

```json
{
  "event": "COMMENT",
  "body": "## Review Summary\n[inline feedback summary]\n\n## Observations Outside This PR\nWhile reviewing, I noticed:\n- `src/utils/foo.ts:142`: Pre-existing null check missing\n- `src/core/bar.ts:78-82`: Similar pattern to line 45 issue - consider deduping",
  "comments": [
    // Only lines IN the diff
  ]
}
```

### Feedback Guidelines

| Feedback Type                 | In Diff? | Where to Put It                                           |
| ----------------------------- | -------- | --------------------------------------------------------- |
| Specific code issue           | Yes      | Inline comment on that line                               |
| Pattern repeated across files | Yes      | Inline on first occurrence + note "same issue in X, Y, Z" |
| Related issue found           | No       | Summary body under "Observations Outside This PR"         |
| Pre-existing bug discovered   | No       | Summary body (consider separate issue if critical)        |
| Overall architecture concern  | N/A      | Summary body                                              |
| Approval/changes requested    | N/A      | Use `event: "APPROVE"` or `event: "REQUEST_CHANGES"`      |

Be concise. Group minor style issues together.
