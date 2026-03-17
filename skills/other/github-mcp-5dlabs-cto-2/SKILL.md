---
name: github-mcp
description: GitHub operations for creating PRs, pushing files, and managing branches.
agents: [rex, grizz, nova, blaze, tap, spark, atlas, stitch, cleo, tess]
triggers: [pull request, PR, branch, push, commit, github, merge]
---

# GitHub MCP (Repository Operations)

Use GitHub MCP tools to interact with repositories programmatically.

## Tools

| Tool | Purpose |
|------|---------|
| `github_create_pull_request` | Create a new PR |
| `github_push_files` | Push file changes to a branch |
| `github_create_branch` | Create a new branch |
| `github_get_file_contents` | Read file from repository |
| `github_get_pull_request` | Get PR details |
| `github_get_pull_request_files` | List files changed in a PR |
| `github_create_pull_request_review` | Submit a PR review |
| `github_add_pull_request_review_comment` | Add inline comment to PR |

## Creating a PR

```
# 1. Create branch
github_create_branch({
  owner: "5dlabs",
  repo: "my-project",
  branch: "feature/task-42-auth",
  from_branch: "develop"
})

# 2. Push changes
github_push_files({
  owner: "5dlabs",
  repo: "my-project",
  branch: "feature/task-42-auth",
  files: [
    { path: "src/auth.ts", content: "..." }
  ],
  message: "feat: implement OAuth2 authentication"
})

# 3. Create PR
github_create_pull_request({
  owner: "5dlabs",
  repo: "my-project",
  title: "feat: implement OAuth2 authentication",
  body: "## Summary\n...",
  head: "feature/task-42-auth",
  base: "develop"
})
```

## Reading Files

```
github_get_file_contents({
  owner: "5dlabs",
  repo: "my-project",
  path: "src/config.ts",
  branch: "develop"
})
```

## PR Review

```
# Get changed files
github_get_pull_request_files({
  owner: "5dlabs",
  repo: "my-project",
  pull_number: 123
})

# Submit review
github_create_pull_request_review({
  owner: "5dlabs",
  repo: "my-project",
  pull_number: 123,
  event: "APPROVE",
  body: "LGTM! All checks pass."
})
```

## Best Practices

1. **Always branch from develop** - Not main
2. **Use conventional commits** - `feat:`, `fix:`, `chore:`
3. **Include Linear issue link** - In PR body
4. **Review before merge** - Check CI status
