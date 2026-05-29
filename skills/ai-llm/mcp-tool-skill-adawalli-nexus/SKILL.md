---
name: mcp-server-instructions
description: Write effective MCP server instructions for tool compaction support. Use when creating or updating the `instructions` parameter in MaaSProtectedFastMCP server initialization. Helps LLMs understand when to search for tools, workflow patterns, and cross-feature relationships.
---

# MCP Server Instructions

Write workflow-focused server instructions that help LLMs understand your server's capabilities.

## What Instructions Are

The `instructions` field is an optional string in MCP's `InitializeResult` that gets injected into the LLM's system prompt. It helps models understand:

- How to use your server's tools together
- When to search for specific tools (with tool compaction)
- Operational constraints and patterns

**Evidence**: In controlled testing, well-written instructions improved task success from 60% to 85% - a 25% improvement.

## Template

```python
instructions="""[Server name] for [domain] operations.

KEY WORKFLOWS:
- [Name]: [tool1] -> [tool2] -> [tool3]
- [Name]: [tool1] -> [tool2] (when [condition])

CONSTRAINTS:
- [Limit or behavior users need to know]
- [Input format quirks]
- [Auto-pagination or chunking behavior]"""
```

## What to Include

Focus on what individual tool descriptions don't convey:

| Include                      | Example                                               |
| ---------------------------- | ----------------------------------------------------- |
| **Cross-tool relationships** | "Always call authenticate before any fetch\_\* tools" |
| **Operational patterns**     | "Search results expire after 10 minutes"              |
| **Constraints**              | "Rate limited to 100 requests/minute"                 |
| **Sequencing**               | "Use get_metadata before fetching large content"      |
| **Format flexibility**       | "IID accepts: #72, !72, '72', 72"                     |

## What to Avoid

| Avoid                       | Why                                      | Instead                          |
| --------------------------- | ---------------------------------------- | -------------------------------- |
| Repeating tool descriptions | Already in tool docstrings               | Show how tools work together     |
| Marketing language          | "comprehensive", "powerful" add no value | State capabilities factually     |
| Lengthy manuals             | Instructions should be <500 chars        | Be concise and actionable        |
| Listing all tools           | Tools are discoverable                   | Only mention in workflow context |

**Bad**: "The search tool searches for files"
**Good**: "Use search before read to validate paths. Results expire after 10 min."

## Process

1. **Find tools** - Read server.py, locate all `@app.tool()` decorators
2. **Group by workflow** - Which tools are used together?
3. **Find dependencies** - Which tools need output from others?
4. **Note constraints** - Pagination, size limits, rate limits, formats
5. **Identify non-obvious behaviors** - Auto-pagination, caching, chunking

## Common Patterns

- **Search -> Details**: `search_X -> get_X`
- **List -> Inspect -> Act**: `list_X -> get_X -> update_X`
- **Metadata First**: `get_X_metadata -> get_X_content` (for large content)
- **Two-Step Updates**: `get_editmeta -> update_X` (when schema required)
- **Hierarchical Browse**: `list_parent -> get_parent -> list_children`

## Examples

### Good

```python
instructions="""GitLab server for repository and CI/CD operations.

KEY WORKFLOWS:
- Code Review: list_merge_requests -> get_merge_request -> get_merge_request_diffs
- Pipeline Debug: list_pipelines_jobs -> get_job_log_metadata -> get_job_log_paginated
- File Browse: search_repositories -> get_repo_tree -> get_file_contents

CONSTRAINTS:
- MR IID accepts: #72, !72, "72", 72
- Job logs >500KB auto-paginate to last 2000 lines
- Use get_job_log_metadata before fetching large logs"""
```

### Bad

```python
# Too vague - doesn't help LLM understand capabilities
instructions="GitLab MCP Server that validates tokens via Authorization Server introspection"

# Marketing fluff - no actionable information
instructions="""This is a comprehensive GitLab integration server that provides
powerful capabilities for working with GitLab repositories..."""

# Tool listing - just repeats what's already in tool descriptions
instructions="""Available tools: search_repos, list_projects, get_project,
get_file, list_commits, get_commit, list_issues, get_issue..."""
```

## Limitations

Instructions are probabilistic guidance, not deterministic rules. They improve LLM behavior but cannot guarantee it. Don't rely on instructions for security-critical or privacy-sensitive enforcement.
