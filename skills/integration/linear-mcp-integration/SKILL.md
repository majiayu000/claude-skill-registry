---
name: Linear MCP Integration
description: >-
  Use Linear MCP server functions to interact with Linear issues, projects, teams,
  and comments. Use when: (1) Fetching issue requirements and acceptance criteria
  from Linear, (2) Validating PR changes against Linear issue requirements,
  (3) Creating or updating Linear issues and comments, (4) Checking issue status,
  labels, or relationships, (5) Listing issues by team, assignee, or project, or
  (6) Any Linear project management operation. Requires Linear MCP server
  configured and authenticated.
---

# Linear MCP Integration

Use Linear MCP server functions to interact with Linear's project management system.

## Prerequisites

- Linear MCP server configured and available
- Authentication: Linear API token configured in MCP server
- Access to Linear workspace

## Quick Start

**Get issue details:**

```typescript
mcp_Linear_get_issue({
  id: "LIN-123",
  includeRelations: true // get related/blocking issues
})
```

**List issues:**

```typescript
mcp_Linear_list_issues({
  team: "Engineering",
  state: "In Progress"
})
```

## Usage Patterns for PR Review

### Fetch Issue Requirements

**Step 1: Extract Issue ID from PR**

- Look for Linear issue references in PR title/body (e.g., `LIN-123`, `[LIN-123]`)
- Extract issue identifier

**Step 2: Get Issue Details**

```typescript
mcp_Linear_get_issue({
  id: "LIN-123", // extracted from PR
  includeRelations: true // to get blocking/related issues
})
```

**Step 3: Extract Requirements**

- Parse issue `description` for acceptance criteria
- Check `labels` for feature tags
- Review `comments` for additional context
- Check `relatedTo` and `blocks` for dependencies

### Validate PR Completeness

Check if PR addresses all requirements:

1. Get issue details with `mcp_Linear_get_issue`
2. Parse issue description for:
  - Acceptance criteria (checkboxes, numbered lists)
  - Feature requirements
  - Technical specifications
3. Compare PR changes against requirements
4. Identify gaps or missing implementations

### Update Issue Status

After PR review:

- Use `mcp_Linear_update_issue` to:
  - Update status (e.g., "In Review", "Ready for QA")
  - Add comments with review findings
  - Link related issues

### Create Review Comments

Post review findings to Linear:

```typescript
mcp_Linear_create_comment({
  issueId: "LIN-123",
  body: "## PR Review Summary\n\n✅ Requirements met: ...\n⚠️ Gaps identified: ..."
})
```

## Common Workflows

### PR Review with Issue Validation

1. Extract issue reference from PR title/body
2. Fetch issue using `mcp_Linear_get_issue`
3. Parse requirements from issue description
4. Review PR changes against requirements
5. Create comment on Linear issue with review summary
6. Update issue status if needed

### Issue Discovery

1. List issues for a team/project using `mcp_Linear_list_issues`
2. Filter by state, assignee, or labels
3. Get details for relevant issues
4. Cross-reference with PR changes

## Integration with GitHub

When reviewing PRs:

1. Extract Linear issue references from PR title/body
2. Use Linear MCP to fetch issue requirements
3. Validate PR changes against requirements
4. Post review findings back to Linear issue

## Reference Documentation

- **MCP Functions Reference**: See [mcp-functions.md](references/mcp-functions.md) for function summaries and examples. The MCP server provides authoritative function definitions with complete parameter types and schemas.
- **Linear API Documentation**: [developers.linear.app/docs](https://developers.linear.app/docs)

