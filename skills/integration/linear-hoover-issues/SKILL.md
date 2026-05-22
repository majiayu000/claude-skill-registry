---
name: linear-hoover-issues
description: "{{ 𝛀𝛀𝛀 }} Find Linear issues addressed by this branch and inject into PR body"
model: opus
disable-model-invocation: true
allowed-tools: ["mcp__plugin_linear_linear__get_issue", "mcp__plugin_linear_linear__save_issue", "mcp__plugin_linear_linear__list_issues", "Bash(git:*)", "Bash(gh:*)", "Read", "Grep"]
---

Identify any Linear issues that have been addressed by work on this branch, and inject them into the PR description.

## Tools

Use the Linear MCP tools (`mcp__plugin_linear_linear__*`) for all Linear API interactions.

## Analyse the branch

1. Run `git log main..HEAD --oneline` to get all commits on this branch
2. Run `git diff main...HEAD --stat` to understand the scope of changes
3. Extract any Linear issue IDs explicitly mentioned in commit messages (e.g. `FOU-123`)

## Search Linear

1. Search across all active Linear issues (exclude completed, cancelled, duplicate) using `mcp__plugin_linear_linear__list_issues`
2. For each commit message and changed file, check whether any Linear issue's title or description describes work that this branch has addressed
3. Include issues that were:
   - Explicitly referenced in commits
   - Implicitly resolved by the changes (match issue descriptions against the actual diff)
4. For each candidate, briefly justify why you think this branch covers it

## Present findings

Show all candidate issues in a table:
- Issue ID + title
- How it was matched (explicit reference / implicit from changes)
- Confidence (high / medium / low)

Wait for approval. The user may remove false positives.

## Apply

Once approved, for each confirmed issue:
1. Assign to `me` using `mcp__plugin_linear_linear__save_issue`
2. Set status to `In Review`

## Inject into PR

If a PR exists for the current branch, update its body. If not, output the snippet for manual inclusion.

Find the `## Overview` section in the PR body and insert the following immediately after the overview content, as a child heading:

```html
<h3>Linear Issues</h3>
```

Followed by a list of links, one per line:

```
[<strong>${ISSUE_ID}:</strong> <i>${issue title}</i>](${linear_issue_url})
```

Example:

```md
### Linear Issues
[<strong>FOU-123:</strong> <i>Add user authentication flow</i>](https://linear.app/foundry/issue/FOU-123)
[<strong>FOU-456:</strong> <i>Fix sidebar overflow on mobile</i>](https://linear.app/foundry/issue/FOU-456)
```
