---
name: jira-create
description: This skill should be used when creating new JIRA tickets, when the user wants to file a bug report, story, or task in JIRA, or when interactively building a well-structured ticket.
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

# JIRA Create Skill

## Overview

Create well-structured JIRA tickets using the Atlassian MCP Server or Atlassian CLI (`acli`), guiding users through gathering required information and formatting descriptions using a consistent template.

**Note: Prefer using the Atlassian MCP Server tools when available. The MCP server provides direct API integration without requiring CLI installation.**

## When to Use

Use this skill when:
- Creating a new JIRA ticket (Story, Bug, Task, Epic)
- User explicitly requests "create ticket", "file bug", "add story", etc.
- Building a structured ticket description interactively

Do NOT use this skill for:
- Searching existing tickets (use `jira-search` instead)
- Updating existing tickets (use `jira-update` instead)
- Sprint planning or backlog analysis (use `jira-backlog-summary` instead)

## Quick Reference

### MCP Server (Preferred)

**Create Issue:**
```
mcp__plugin_patsy_atlassian__createJiraIssue
  cloudId: "your-cloud-id"
  projectKey: "KEY"
  issueTypeName: "Story"
  summary: "Ticket summary"
  description: "Description text"
  assignee_account_id: "user-id" (optional)
  additional_fields: {
    labels: ["bug", "urgent"],
    priority: { name: "High" }
  }
```

### CLI Fallback

**Basic Create:**
```bash
acli jira workitem create \
  --project "KEY" \
  --type "Story" \
  --summary "Ticket summary" \
  --description "Description text"
```

**With Optional Fields:**
```bash
acli jira workitem create \
  --project "KEY" \
  --type "Bug" \
  --summary "Fix login issue" \
  --description-file "/tmp/description.md" \
  --assignee "@me" \
  --label "bug,urgent"
```

## Step-by-Step Process

### 1. Check for MCP Server Availability

First, check if the Atlassian MCP Server is available by looking for these tools:
- `mcp__plugin_patsy_atlassian__createJiraIssue` - Create new issues
- `mcp__plugin_patsy_atlassian__getJiraIssue` - Get issue details (for validation)
- `mcp__plugin_patsy_atlassian__getAccessibleAtlassianResources` - Get cloud ID

If MCP tools are available, prefer using them over the CLI approach.

### 2. Read the Issue Template

Read `references/issue_template.md` in this skill directory to understand the expected ticket structure.

### 3. Gather Required Information

Collect from user:
- **Project key** (e.g., "PROJ", "ENG", "PLAT")
- **Issue type** (Story, Bug, Task, Epic)
- **Summary** (concise, action-oriented title)

### 4. Gather Description Components

**For Stories:**
- User Story: "As a [role] I want to [action] because [reason]"
- Context: High-level overview and desired outcome
- Acceptance Criteria: Requirements using RFC 2119 language (MUST, SHOULD, MAY)
- Implementation Details: Technical suggestions (optional)
- Out of Scope: Explicit scope boundaries (optional)
- Resources: Links to documentation (optional)

**For Bugs:**
- Context: What's broken and the impact
- Steps to Reproduce: How to trigger the bug
- Expected Behavior: What should happen
- Actual Behavior: What actually happens
- Additional Info: Environment, logs, screenshots

**For Tasks:**
- Context: What needs to be done and why
- Acceptance Criteria: Success criteria
- Technical Details: Approach or requirements (optional)

### 5. Gather Optional Information

Ask if user wants to specify:
- Assignee (email or "@me" for self-assign)
- Priority (Highest, High, Medium, Low, Lowest)
- Labels (comma-separated)
- Epic link (parent epic key)
- Components (comma-separated)
- Story points (for Stories)

### 6. Format Description

Build description using template structure:
- Use appropriate template for issue type
- Include only sections with content
- Preserve emoji markers for visual hierarchy
- Format acceptance criteria as checkboxes

### 7. Validate Input

- Project key: uppercase alphanumeric (e.g., "PROJ")
- Summary: < 255 characters
- Epic link format: KEY-123
- Labels: no spaces in individual labels

### 8. Show Preview and Confirm

Display the formatted description and operation before execution (whether using MCP or CLI).

### 9. Execute Operation

Use the appropriate MCP tool or CLI command based on availability.

**MCP Example:**
```
mcp__plugin_patsy_atlassian__createJiraIssue with:
  cloudId: "your-cloud-id"
  projectKey: "PROJ"
  issueTypeName: "Story"
  summary: "Add user authentication system"
  description: "[formatted markdown description]"
  assignee_account_id: "user-id"
  additional_fields: {
    labels: ["security", "backend"]
  }
```

**CLI Example:**
```bash
acli jira workitem create \
  --project "PROJ" \
  --type "Story" \
  --summary "Add user authentication system" \
  --description-file "/tmp/description.md" \
  --assignee "@me" \
  --label "security,backend"
```

For CLI with multi-line descriptions, use `--description-file` flag.

### 10. Provide Summary

Show created ticket key and link: `https://your-domain.atlassian.net/browse/PROJ-123`

## Description Templates

### Story Template
```markdown
# User Story

As a [role] I want to [action] because [reason].

# Context

[High-level overview and desired outcome]

## Acceptance Criteria

 - [ ] MUST [requirement]
 - [ ] SHOULD [requirement]
 - [ ] MAY [requirement]

## Implementation/Technical Details or Suggestions

[Technical approach, sample code, design patterns]

## Out of Scope

[Explicit scope boundaries]

## Additional Information & Resources

- [Link to documentation]
```

### Bug Template
```markdown
# Bug Description

[What's broken and the impact]

## Steps to Reproduce

1. [Step one]
2. [Step two]
3. [Step three]

## Expected Behavior

[What should happen]

## Actual Behavior

[What actually happens]

## Additional Information

- Environment: [production/staging/local]
- Browser/Platform: [if applicable]
- Error logs: [if available]
```

### Task Template
```markdown
# Context

[What needs to be done and why]

## Acceptance Criteria

 - [ ] MUST [requirement]
 - [ ] SHOULD [requirement]

## Technical Details

[Approach or specific requirements]
```

## Common Mistakes

| Mistake | Solution |
|---------|----------|
| Inline multi-line description | Use `--description-file` flag for multi-line content |
| Spaces in labels | Labels must be comma-separated with no spaces: `--label "label1,label2"` |
| Missing RFC 2119 keywords | Acceptance criteria should use MUST, SHOULD, MAY keywords |
| Omitting optional sections | Skip empty sections entirely, don't include blank placeholders |
| Not reading template first | Always read `references/issue_template.md` before gathering info |

## Troubleshooting

- **"Project does not exist"**: Verify project key is correct and user has access
- **"Issue type not found"**: Check available issue types for the project
- **"Field required"**: Some projects require additional fields (components, fix versions)
- **Permission errors**: User may lack permission to create tickets in this project

## Configuration Requirements

Ensure user is authenticated:
```bash
acli jira auth
```

This prompts for:
- Jira URL (e.g., `https://your-domain.atlassian.net`)
- Email address
- API token (create at https://id.atlassian.com/manage-profile/security/api-tokens)

## MCP Server Integration

### Available Tools

The Atlassian MCP Server provides these JIRA creation tools:

- **`mcp__plugin_patsy_atlassian__createJiraIssue`** - Create a new issue
  - Parameters:
    - `cloudId` (string) - Atlassian cloud instance ID or site URL
    - `projectKey` (string) - Project key (e.g., "PROJ")
    - `issueTypeName` (string) - Issue type (Story, Bug, Task, Epic)
    - `summary` (string) - Issue title
    - `description` (string) - Issue description (supports markdown)
    - `assignee_account_id` (string, optional) - User account ID for assignee
    - `additional_fields` (object, optional) - Additional fields like labels, priority, components
  - Returns: Created issue details with key and link

- **`mcp__plugin_patsy_atlassian__getJiraIssue`** - Get issue details
  - Parameters: `cloudId` (string), `issueIdOrKey` (string)
  - Returns: Full issue details
  - Use this to validate the project exists or check created ticket

- **`mcp__plugin_patsy_atlassian__getAccessibleAtlassianResources`** - Get cloud ID
  - Parameters: None
  - Returns: List of accessible Atlassian resources with cloud IDs
  - Use this to discover the cloud ID for your Atlassian instance

### MCP vs CLI Usage

**Use MCP Server when:**
- Available in the environment
- Need structured responses with issue key
- Want consistent error handling
- Prefer direct API integration

**Use CLI when:**
- MCP server is not configured
- Need interactive prompts for fields
- Working with custom acli configurations
- Using description files for complex formatting

### Example MCP Workflow

**Create a story with full details:**
```
1. Get cloud ID (if not already known):
   Use mcp__plugin_patsy_atlassian__getAccessibleAtlassianResources

2. Create the issue:
   Use mcp__plugin_patsy_atlassian__createJiraIssue with:
   cloudId: "your-cloud-id-or-site-url"
   projectKey: "PROJ"
   issueTypeName: "Story"
   summary: "Implement user authentication"
   description: "# User Story\n\nAs a user I want to log in securely...\n\n## Acceptance Criteria\n\n- [ ] MUST support email/password login\n- [ ] SHOULD include 2FA option"
   assignee_account_id: "user-id"
   additional_fields: {
     labels: ["security", "backend"],
     priority: { name: "High" }
   }

3. MCP returns issue key (e.g., "PROJ-123") and link
```
