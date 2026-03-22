---
name: github
description: Use for GitHub operations - create PR, pull request, issues, repository, commits, branches, code search, file contents, fork, merge. 26 tools for GitHub API integration.
version: 1.0.0
title: "Github"
status: active
---

# github Skill

Access GitHub API for repository operations, pull requests, issues, code search, and more.

## Context Efficiency

Traditional MCP approach:
- All 26 tools loaded at startup
- Estimated context: 13000 tokens

This skill approach:
- Metadata only: ~100 tokens
- Full instructions (when used): ~5k tokens
- Tool execution: 0 tokens (runs externally)

## How This Works

Instead of loading all MCP tool definitions upfront, this skill:
1. Tells you what tools are available (just names and brief descriptions)
2. You decide which tool to call based on the user's request
3. Generate a JSON command to invoke the tool
4. The executor handles the actual MCP communication

## Available Tools

- `create_or_update_file`: Create or update a single file in a GitHub repository
- `search_repositories`: Search for GitHub repositories
- `create_repository`: Create a new GitHub repository in your account
- `get_file_contents`: Get the contents of a file or directory from a GitHub repository
- `push_files`: Push multiple files to a GitHub repository in a single commit
- `create_issue`: Create a new issue in a GitHub repository
- `create_pull_request`: Create a new pull request in a GitHub repository
- `fork_repository`: Fork a GitHub repository to your account or specified organization
- `create_branch`: Create a new branch in a GitHub repository
- `list_commits`: Get list of commits of a branch in a GitHub repository
- `list_issues`: List issues in a GitHub repository with filtering options
- `update_issue`: Update an existing issue in a GitHub repository
- `add_issue_comment`: Add a comment to an existing issue
- `search_code`: Search for code across GitHub repositories
- `search_issues`: Search for issues and pull requests across GitHub repositories
- `search_users`: Search for users on GitHub
- `get_issue`: Get details of a specific issue in a GitHub repository.
- `get_pull_request`: Get details of a specific pull request
- `list_pull_requests`: List and filter repository pull requests
- `create_pull_request_review`: Create a review on a pull request
- `merge_pull_request`: Merge a pull request
- `get_pull_request_files`: Get the list of files changed in a pull request
- `get_pull_request_status`: Get the combined status of all status checks for a pull request
- `update_pull_request_branch`: Update a pull request branch with the latest changes from the base branch
- `get_pull_request_comments`: Get the review comments on a pull request
- `get_pull_request_reviews`: Get the reviews on a pull request

## Usage Pattern

When the user's request matches this skill's capabilities:

**Step 1: Identify the right tool** from the list above

**Step 2: Generate a tool call** in this JSON format:

```json
{
  "tool": "tool_name",
  "arguments": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

**Step 3: Execute via bash:**

```bash
python .claude/skills/mcp-skills/executor.py --skill github --call 'YOUR_JSON_HERE'
```


## Getting Tool Details

If you need detailed information about a specific tool's parameters:

```bash
python .claude/skills/mcp-skills/executor.py --skill github --describe tool_name
```

This loads ONLY that tool's schema, not all tools.

## Examples

### Example 1: Simple tool call

User: "Create a GitHub issue"

Your workflow:
1. Identify tool: `create_issue`
2. Generate call JSON
3. Execute:

```bash
python .claude/skills/mcp-skills/executor.py --skill github --call '{"tool": "create_issue", "arguments": {"owner": "user", "repo": "repo", "title": "Bug fix"}}'
```

### Example 2: Get tool details first

```bash
python .claude/skills/mcp-skills/executor.py --skill github --describe create_issue
```

Returns the full schema, then you can generate the appropriate call.

## Error Handling

If the executor returns an error:
- Check the tool name is correct
- Verify required arguments are provided
- Ensure the MCP server is accessible

## Performance Notes

Context usage comparison for this skill:

| Scenario | MCP (preload) | Skill (dynamic) |
|----------|---------------|-----------------|
| Idle | 13000 tokens | 100 tokens |
| Active | 13000 tokens | 5k tokens |
| Executing | 13000 tokens | 0 tokens |

Savings: ~61% reduction in typical usage

---

*This skill was auto-generated from an MCP server configuration.*
*Generator: mcp_to_skill.py*
