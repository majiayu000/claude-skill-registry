---
name: GitLab Issue
description: Creates, retrieves, updates, and manages GitLab issues with comprehensive context gathering. Use when the user wants to create a new issue, view issue details, update existing issues, list project issues, or manage issue workflows in GitLab.
allowed-tools: gitlab-mcp(create_issue), gitlab-mcp(get_issue), gitlab-mcp(list_issues), gitlab-mcp(update_issue), gitlab-mcp(get_project), gitlab-mcp(list_merge_requests)
license: MIT
metadata:
  author: Foundation Skills
  version: 1.0.0
  mcp-server: gitlab-mcp
---

# GitLab Issue Management

Create, retrieve, update, and manage GitLab issues with comprehensive context integration and structured workflows.

## GitLab Instance Configuration

This skill is configured for a self-hosted GitLab instance:
- **GitLab URL:** https://gitlab-erp-pas.dedalus.lan
- All project identifiers, URLs, and references should use this self-hosted instance
- Ensure you have appropriate access credentials configured for this GitLab server

## When to Use This Skill

Activate this skill when:
- The user wants to create a new GitLab issue
- The user asks to view or retrieve issue details
- The user needs to update an existing issue
- The user wants to list issues in a project
- The user mentions managing issues, tickets, or tasks in GitLab
- The user wants to close, reopen, or modify issue properties
- The user needs to link issues to merge requests

## Critical Rules

**IMPORTANT: Always confirm project_id before creating or modifying issues**

**Always use descriptive issue titles and provide structured descriptions**

**Never create duplicate issues - search existing issues first when appropriate**

## Workflow

### 1. Gather Context

First, collect information about the current project and context:

- Identify the project (project_id or URL-encoded path)
- Understand the type of issue (bug, feature, task, etc.)
- Gather relevant labels, milestones, and assignees if applicable

### 2. Project Verification

Before any operation, verify the project exists and you have the correct identifier:

**Self-hosted GitLab Instance:** https://gitlab-erp-pas.dedalus.lan

Use `gitlab-mcp(get_project)` to:
- Confirm project exists on the self-hosted GitLab instance
- Get project details (default branch, visibility, etc.)
- Understand project structure
- Verify project path format (e.g., "namespace/project")

### 3. Issue Operations

#### Creating a New Issue

When creating issues, gather complete context:

**Required Information:**
- `project_id`: Project identifier (e.g., "namespace/project" or numeric ID)
- `title`: Clear, descriptive issue title

**Optional but Recommended:**
- `description`: Detailed description in Markdown format
- `labels`: Array of label names (e.g., ["bug", "priority::high"])
- `assignee_ids`: Array of user IDs to assign
- `milestone_id`: Milestone ID to associate
- `due_date`: Due date in YYYY-MM-DD format
- `confidential`: Boolean for sensitive issues

**Human-in-the-Loop - Ask for Context**

Always use AskUserQuestion to clarify issue details:

```
Question: "What type of issue is this?"
Options:
- "Bug report - something is not working correctly"
- "Feature request - new functionality needed"
- "Task - work item to complete"
- "Documentation - documentation needs update"
- "Other - let me describe it"
```

**Issue Description Template:**

Structure descriptions for clarity:

```markdown
## Summary
[Brief description of the issue]

## Current Behavior
[What is happening now - for bugs]

## Expected Behavior
[What should happen - for bugs]

## Steps to Reproduce
[For bugs - numbered steps]

## Acceptance Criteria
[For features/tasks - what defines "done"]

## Additional Context
[Screenshots, logs, related issues, etc.]
```

#### Retrieving Issue Details

Use `gitlab-mcp(get_issue)` with:
- `project_id`: Project identifier
- `issue_iid`: Internal issue ID (the number shown in GitLab, e.g., #42)

This returns complete issue information including:
- Title and description
- State (opened/closed)
- Labels and milestone
- Assignees and author
- Created/updated timestamps
- Related merge requests

#### Listing Issues

Use `gitlab-mcp(list_issues)` with filters:
- `project_id`: Project identifier
- `state`: "opened", "closed", or "all"
- `labels`: Filter by labels
- `milestone`: Filter by milestone title
- `assignee_id`: Filter by assignee
- `search`: Search in title and description
- `order_by`: Sort by "created_at", "updated_at", "priority", etc.
- `sort`: "asc" or "desc"
- `per_page`: Results per page (max 100)

#### Updating an Issue

When updating issues, only provide changed fields:

Use `gitlab-mcp(update_issue)` with:
- `project_id`: Project identifier
- `issue_iid`: Internal issue ID
- Plus any fields to update (title, description, labels, state_event, etc.)

**State Changes:**
- `state_event: "close"` - Close the issue
- `state_event: "reopen"` - Reopen the issue

### 4. Linking to Merge Requests

To find related merge requests:

Use `gitlab-mcp(list_merge_requests)` with filters to find MRs that reference the issue:
- Search for issue number in MR titles/descriptions
- Check MR descriptions for "Closes #XX" or "Fixes #XX" patterns

### 5. Execute Operations (Requires Confirmation)

**CRITICAL: Confirm with user before creating or modifying issues**

After gathering all information, present a summary for user approval:

```
Creating issue in project: namespace/project
Title: [title]
Description: [summary]
Labels: [labels]
Assignee: [assignee]

Proceed with issue creation?
```

## Issue Type Templates

### Bug Report

```markdown
## Bug Description
[Clear description of the bug]

## Environment
- Version: [version]
- OS: [operating system]
- Browser: [if applicable]

## Steps to Reproduce
1. [First step]
2. [Second step]
3. [See error]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Screenshots/Logs
[Attach relevant files]

## Possible Solution
[Optional: if you have ideas]
```

### Feature Request

```markdown
## Feature Description
[Clear description of the requested feature]

## Problem Statement
[What problem does this solve?]

## Proposed Solution
[How should this work?]

## Alternatives Considered
[Other approaches considered]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Additional Context
[Mockups, examples, etc.]
```

### Task

```markdown
## Task Description
[What needs to be done]

## Background
[Why is this needed?]

## Requirements
- [ ] [Requirement 1]
- [ ] [Requirement 2]

## Definition of Done
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Dependencies
[Related issues, blockers]
```

## Examples

### Example 1: Creating a Bug Report

**User:** "Create an issue for the login bug we discussed"

**AI Workflow:**
1. Ask for project_id if not known
2. Ask clarifying questions about the bug
3. Generate structured description
4. Present summary for confirmation
5. Create issue with gitlab-mcp(create_issue)

**Result:**
```
Title: [BUG] Login fails with OAuth2 when session expires

Description:
## Bug Description
Users are unable to log in using OAuth2 authentication when their 
previous session has expired.

## Steps to Reproduce
1. Log in with OAuth2 (Google/GitHub)
2. Wait for session to expire (or clear cookies)
3. Attempt to log in again
4. Observe error: "Invalid state parameter"

## Expected Behavior
User should be redirected to OAuth provider and log in successfully.

## Actual Behavior
Login fails with "Invalid state parameter" error.

## Environment
- Version: 2.3.1
- Browser: Chrome 120, Firefox 121

Labels: ["bug", "priority::high", "auth"]
```

### Example 2: Listing and Filtering Issues

**User:** "Show me all open bugs assigned to me"

**AI Workflow:**
1. Use gitlab-mcp(list_issues) with filters:
   - state: "opened"
   - labels: ["bug"]
   - scope: "assigned_to_me"

**Result:**
```
Found 3 open bug issues assigned to you:

#142 - [BUG] API timeout on large file uploads
      Labels: bug, priority::medium
      Created: 2024-01-15

#138 - [BUG] Dashboard graphs not rendering on Safari
      Labels: bug, frontend, priority::low
      Created: 2024-01-12

#125 - [BUG] Email notifications delayed by 30+ minutes
      Labels: bug, priority::high
      Created: 2024-01-08
```

### Example 3: Updating an Issue

**User:** "Close issue #142 and add a comment that it's fixed in v2.4.0"

**AI Workflow:**
1. First, add a note/comment to the issue
2. Then update issue state to closed

**Using gitlab-mcp(update_issue):**
```
project_id: "mygroup/myproject"
issue_iid: 142
state_event: "close"
```

**Result:**
```
Issue #142 "[BUG] API timeout on large file uploads" has been closed.
```

### Example 4: Feature Request with Full Context

**User:** "Create a feature request for adding dark mode support"

**AI Workflow:**
1. Ask clarifying questions about the feature
2. Gather acceptance criteria
3. Create structured issue

**Result:**
```
Title: [FEATURE] Add dark mode theme support

Description:
## Feature Description
Implement a dark mode theme option that users can toggle in their 
preferences.

## Problem Statement
Users working in low-light environments experience eye strain with 
the current bright interface. Dark mode would improve accessibility 
and user comfort.

## Proposed Solution
- Add theme toggle in user preferences
- Implement CSS variables for theme colors
- Store preference in user settings
- Support system preference detection

## Acceptance Criteria
- [ ] User can toggle between light/dark mode in settings
- [ ] Theme preference persists across sessions
- [ ] System preference is detected on first visit
- [ ] All UI components support both themes
- [ ] No accessibility contrast issues in dark mode

## Additional Context
Reference designs: [link to mockups]
Similar implementations: GitHub, GitLab, VS Code

Labels: ["feature", "enhancement", "ux"]
```

## Important Notes

- **Self-hosted GitLab:** All operations use https://gitlab-erp-pas.dedalus.lan
- **Always verify project access** - Ensure you have permission to create/modify issues on the self-hosted instance
- **Use labels consistently** - Follow project labeling conventions
- **Be specific in titles** - Prefix with [BUG], [FEATURE], [TASK] for clarity
- **Include reproduction steps** - Essential for bug reports
- **Define acceptance criteria** - Clear "definition of done" for features/tasks
- **Link related issues** - Use "Related to #XX" or "Blocks #XX" in descriptions
- **Mention users with @username** - For visibility and notifications
- **Use milestones** - Associate issues with releases or sprints when applicable

## GitLab Issue Best Practices

### Writing Effective Titles
- Be concise but descriptive
- Include issue type prefix: [BUG], [FEATURE], [TASK], [DOCS]
- Mention affected component if applicable
- Avoid vague titles like "Fix bug" or "Update code"

### Structuring Descriptions
- Use Markdown formatting for readability
- Include all relevant context upfront
- Add screenshots or logs when helpful
- Link to related issues, MRs, or documentation
- Use task lists for trackable sub-items

### Label Strategy
- Use scoped labels (e.g., `priority::high`, `status::in-progress`)
- Combine type labels (`bug`, `feature`) with area labels (`frontend`, `api`)
- Keep label taxonomy consistent across projects

### Assignment and Workflow
- Assign issues to specific team members
- Use milestones for sprint/release planning
- Update issue status as work progresses
- Close issues with reference to fixing MR: "Closes #XX"
