---
name: inline-pr-comments
description: Post inline PR review comments on specific lines. Use this skill to deliver code review feedback as inline comments rather than a single summary.
---

# Inline PR Comments Skill

Use this skill to post code review feedback as inline comments on specific lines in a PR.

## When to Use

- After completing a code review (use with /claude-review, /claude-security-review, /claude-tob-review)
- When you have specific line-by-line feedback to deliver
- To make review feedback more actionable

## Instructions

Use MCP inline comment tool, not `gh api`:

1. For each issue on a changed line, call:
   - `mcp__github_inline_comment__create_inline_comment`
2. Required args:
   - `path`
   - `body`
   - `line` (single-line), or `startLine` + `line` (multi-line)
   - `side: "RIGHT"` unless intentionally commenting old code
3. After posting inline comments, update the Claude sticky summary comment with:
   - `mcp__github_comment__update_claude_comment`
4. Do **not** use `gh api` here; action tool permissions often block non-git Bash commands.

### Comment Fields (`create_inline_comment`)

- `path` - File path relative to repo root
- `line` - Line number in the NEW version of the file (right side of diff)
- `startLine` + `line` - For comments spanning multiple lines
- `side` - `RIGHT` (new code) or `LEFT` (old code), default to `RIGHT`
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

Example: update the sticky comment to include non-diff findings:

```yaml
tool: mcp__github_comment__update_claude_comment
args:
  body: |
    ## Review Summary
    [inline feedback summary]

    ## Observations Outside This PR
    While reviewing, I noticed:
    - `src/utils/foo.ts:142`: Pre-existing null check missing
    - `src/core/bar.ts:78-82`: Similar pattern to line 45 issue - consider deduping
```

### Feedback Guidelines

| Feedback Type                 | In Diff? | Where to Put It                                              |
| ----------------------------- | -------- | ------------------------------------------------------------ |
| Specific code issue           | ✅ Yes   | Inline comment on that line                                  |
| Pattern repeated across files | ✅ Yes   | Inline on first occurrence + note "same issue in X, Y, Z"    |
| Related issue found           | ❌ No    | Summary body under "Observations Outside This PR"            |
| Pre-existing bug discovered   | ❌ No    | Summary body (consider separate issue if critical)           |
| Overall architecture concern  | N/A      | Summary body                                                 |
| Approve PR                    | N/A      | Out of scope for this skill; keep feedback in sticky comment |
| Changes requested             | N/A      | Sticky comment; never use `REQUEST_CHANGES`                  |

Be concise. Group minor style issues together.
