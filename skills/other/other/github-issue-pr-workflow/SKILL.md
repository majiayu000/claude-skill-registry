---
id: github-issue-pr-workflow
name: GitHub Issue and PR Workflow
description: List and search issues, PRs, commits; summarize status and reviews
role: engineering
requiredTools:
  - type: mcpService
    serviceType: github
---

## GitHub Issue and PR Workflow

When working with GitHub issues and pull requests:

- Use **github_list_repos** (tool name may have a suffix if multiple GitHub servers exist) when owner/repo is unknown; then **github_list_issues** or **github_list_prs** with owner, repo, and state (open/closed/all).
- Use **github_get_issue** or **github_get_pr** for full details, review status, and merge state before summarizing.
- Use **github_list_commits** and **github_get_commit** for commit history and change stats.
- Always specify owner and repo; use state and sort/direction for focused lists.
- Summarize counts, titles, and key metadata; avoid dumping full bodies unless the user asks.

## Step-by-step instructions

1. Resolve owner and repo: use **github_list_repos** if needed, or take from the user's question.
2. For "open issues" or "PRs in repo X": call **github_list_issues** or **github_list_prs** with owner, repo, state (e.g. open), and optional sort/direction.
3. For a specific issue or PR: call **github_get_issue** or **github_get_pr** with owner, repo, and issueNumber; summarize title, state, assignee, labels, and (for PRs) merge status and review state.
4. For commit history: use **github_list_commits** with owner, repo, and optional author/path/since/until; use **github_get_commit** for a single commit's details and stats.
5. When summarizing: report counts, key titles, and status; cite repo and filters used.

## Examples of inputs and outputs

- **Input**: "What open PRs are in acme/api-server?"  
  **Output**: Short list of PR numbers, titles, and state from **github_list_prs** (owner=acme, repo=api-server, state=open); optionally merge status per PR.

- **Input**: "Summarize PR #42 in acme/api-server."  
  **Output**: Title, state, merge status, review state, and key changes (additions/deletions) from **github_get_pr**; mention assignee and labels if relevant.

## Common edge cases

- **Repo not found**: Say "Repository [owner/repo] not found" and suggest checking name or permissions.
- **Issue/PR not found**: Say "Issue/PR [number] not found" and suggest checking the number or repo.
- **Large list**: Summarize count and a sample (e.g. first 5-10) with key fields; do not dump every item unless asked.
- **API/OAuth error**: Report that GitHub returned an error and suggest reconnecting or retrying.

## Tool usage for specific purposes

- **github_list_repos**: Use when owner/repo is unknown; then use list_issues/list_prs with the chosen repo.
- **github_list_issues**: Use for "open issues", "backlog", or by state; filter by state, sort, direction.
- **github_get_issue**: Use for full issue details before summarizing or when the user asks for one issue.
- **github_list_prs**: Use for "open PRs", "merged this week", or by state; filter by state, sort, direction.
- **github_get_pr**: Use for full PR details, merge status, and review state.
- **github_list_commits** / **github_get_commit**: Use for commit history and change stats.
