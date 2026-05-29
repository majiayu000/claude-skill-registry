---
name: personal-jira-project-management
description: Manage JIRA issues for the Orient Task Force (YOUR_COMPONENT component). Use this skill when creating, updating, querying, or managing JIRA issues including Epics, Stories, Tasks, Bugs, and Sub-tasks. Covers issue hierarchy rules (Stories MUST have Epic parents), required fields by issue type, naming conventions, status transitions, SLA rules, and issue linking patterns. Use when asked to "create a ticket", "check blockers", "update JIRA", or any JIRA-related project management task.
---

# JIRA Management for Orient Task Force

## Project Context

- **Project Key**: `YOUR_PROJECT` (Genoox TF project)
- **Component**: `YOUR_COMPONENT`
- **Cloud ID**: `882ead72-4dfa-4fef-925d-fc9c9187853c` (for Atlassian MCP server)
- All issues MUST include the YOUR_COMPONENT component

## Actual Status Names in JIRA

The project uses these status names (not the simplified workflow in docs):
- **To Do**: `to do`, `Backlog`, `TO DO DEV`
- **In Progress**: `In dev`, `In Progress`, `In QA` 
- **Done**: `Done- Deployed`
- **Other**: `Linked to initiative` (for Epics)

## Issue Types

| Type | Purpose | Parent Required |
|------|---------|-----------------|
| Epic | Large initiative spanning multiple sprints | N/A |
| Story | User-facing functionality | **MANDATORY** - must link to Epic |
| Task | Technical/non-user-facing work | Optional Epic link |
| Bug | Defect or unexpected behavior | Optional Story/Epic link |
| Sub-task | Breakdown of larger issue | **MANDATORY** - must have parent (Story/Task/Bug) |

## Critical Rules

### Stories MUST Have Epic Parents
1. Before creating a Story, check for existing Epics
2. If no suitable Epic exists, ask user or create Epic first
3. **NEVER** create a Story without an Epic link

### Sub-tasks MUST Have Parents
- Valid parents: Story, Task, Bug
- Invalid parents: Epic, another Sub-task

## Required Fields by Type

### Epic
- Summary (required)
- Description with goals and scope (required)
- Component: YOUR_COMPONENT (required)

### Story
- Summary (required)
- Description with acceptance criteria (required)
- Epic Link (**MANDATORY**)
- Story Points (required)
- Priority (required)
- Component: YOUR_COMPONENT (required)

### Task
- Summary (required)
- Description (recommended)
- Component: YOUR_COMPONENT (required)

### Bug
- Summary (required)
- Description with steps to reproduce (required)
- Priority (required)
- Component: YOUR_COMPONENT (required)

## Naming Conventions

**Epic**: `[Area] Initiative Name` - e.g., `[Auth] User Authentication System`
**Story**: User story format preferred - e.g., `As a user, I want to reset my password`
**Task**: Action-oriented, start with verb - e.g., `Set up CI/CD pipeline`
**Bug**: `[Component] Brief issue description` - e.g., `[Login] Password reset email not sending`

## Workflow Transitions

```
To Do → In Progress → In Review → Done
```

### SLA Limits
| Status | Max Days | Action on Breach |
|--------|----------|-----------------|
| To Do | 5 days | Flag as stale |
| In Progress | 3 days | Check for blockers |
| In Review | 2 days | Escalate to reviewer |

## Issue Linking

| Link Type | Use When |
|-----------|----------|
| Blocks | Task A must complete before Task B can proceed |
| Is Blocked By | Task B cannot proceed until Task A completes |
| Relates To | General relationship, no dependency |

**Always link dependencies** - If Task A is required for Story B, create a "blocks" link.

## MCP Tools

### Quick Query Tools (Orient)
Use these for simple, fast queries:
- `ai_first_get_all_issues` - List all issues
- `ai_first_get_issue` - Get specific issue details
- `ai_first_get_in_progress` - Get in-progress issues
- `ai_first_get_blockers` - Get blocker issues
- `ai_first_check_sla_breaches` - Check SLA violations
- `ai_first_get_sprint_issues` - Get sprint issues
- `ai_first_get_board_issues` - Get Kanban board issues

### Comprehensive Tools (Atlassian MCP Server)
Use these for detailed queries and updates:
- `mcp_Atlassian-MCP-Server_searchJiraIssuesUsingJql` - Advanced JQL searches
- `mcp_Atlassian-MCP-Server_getJiraIssue` - Get full issue details with all fields
- `mcp_Atlassian-MCP-Server_createJiraIssue` - Create new issues
- `mcp_Atlassian-MCP-Server_editJiraIssue` - Update existing issues
- `mcp_Atlassian-MCP-Server_transitionJiraIssue` - Change issue status
- `mcp_Atlassian-MCP-Server_addCommentToJiraIssue` - Add comments
- `mcp_Atlassian-MCP-Server_getVisibleJiraProjects` - List accessible projects

### Manage Links
- `ai_first_jira_get_issue_links` - Get all links for an issue
- `ai_first_jira_create_issue_link` - Create link between issues
- `ai_first_jira_delete_issue_link` - Delete issue link

### Tool Selection Strategy

**Use Orient tools** when:
- Quick status checks needed
- Working with known issue keys
- Getting pre-filtered results (blockers, in-progress, etc.)

**Use Atlassian MCP Server** when:
- Need comprehensive issue details (assignee, epic, comments, custom fields)
- Creating or updating issues
- Running custom JQL queries
- Need to see project structure or available issue types
- Want full changelog or comment history

## Weekly Status Queries

### Recommended Approach for Status Updates

When asked for weekly status or "what was in progress this week":

1. **Get currently active issues** (fast check):
   ```
   ai_first_get_in_progress
   ai_first_get_board_issues
   ```

2. **Get comprehensive details** using Atlassian MCP:
   ```
   searchJiraIssuesUsingJql with:
   project = YOUR_PROJECT AND component = "YOUR_COMPONENT" AND statusCategory = "In Progress"
   ```

3. **Get full issue details** for each active issue (parallel calls):
   ```
   getJiraIssue for each key to get:
   - Assignee and reporter
   - Parent Epic (with epic summary/status)
   - Comments and recent updates
   - Custom fields (priority, deployment info, etc.)
   ```

### Useful JQL Query Patterns

**All YOUR_COMPONENT issues:**
```jql
project = YOUR_PROJECT AND component = "YOUR_COMPONENT" ORDER BY created DESC
```

**Active issues (In Progress):**
```jql
project = YOUR_PROJECT AND component = "YOUR_COMPONENT" AND statusCategory = "In Progress" ORDER BY updated DESC
```

**Issues updated this week:**
```jql
project = YOUR_PROJECT AND component = "YOUR_COMPONENT" AND updated >= startOfWeek() ORDER BY updated DESC
```

**In Development specifically:**
```jql
project = YOUR_PROJECT AND component = "YOUR_COMPONENT" AND status IN ("In dev", "In QA") ORDER BY status ASC, updated DESC
```

### Status Report Format

When providing weekly updates, organize by status category:

1. **🟡 IN DEVELOPMENT** - Issues in "In dev" status
2. **🟢 IN QA/TESTING** - Issues in "In QA" status  
3. **✅ COMPLETED THIS WEEK** - Recently moved to Done
4. **📈 KEY HIGHLIGHTS** - Major achievements, completed features, trends
5. **🎯 NEXT STEPS** - Action items, dependencies, blockers

**For each issue include:**
- Issue key with Atlassian URL: `[PROJ-XXXXX](https://your-domain.atlassian.net/browse/PROJ-XXXXX)`
- Summary (ticket title)
- Status
- Assignee (display name)
- Last updated date
- Parent Epic (with key and name)
- **Progress notes** from latest comments (especially completion/status updates)

**Make it actionable:**
- Highlight completed features with ✅
- Note any blockers or dependencies
- Call out items needing attention
- Summarize adoption/impact metrics if mentioned in comments

## AI Behavior

### Auto-Fix
- Missing Epic Link on Story: Prompt user to select Epic
- Missing Required Fields: Prompt before submission
- Naming Convention Violations: Auto-correct formatting

### Block (Refuse to Proceed)
- Story with no Epic parent
- Empty or too-short summary
- Required fields cannot be determined

### Warn (Allow User to Proceed)
- Optional fields missing
- Story points seem unusual
- Description shorter than recommended

## Troubleshooting

### Common Issues

**"No issues found" but you expect results:**
1. Verify you're using project key `YOUR_PROJECT` (not `YOUR_PROJECT`)
2. Check the component name is exactly `YOUR_COMPONENT` (case-sensitive)
3. Use Atlassian MCP server to verify project structure:
   ```
   getVisibleJiraProjects with searchString: "GENOOX"
   ```

**JQL syntax errors:**
- Date ranges use: `updated >= startOfWeek()` (not DURING for single status)
- Multiple statuses use: `status IN ("In dev", "In QA")`
- Status category: `statusCategory = "In Progress"` (matches multiple statuses)

**Getting detailed information:**
- Orient tools return summary info only
- Use `getJiraIssue` from Atlassian MCP for full details (assignee, epic parent, comments)
- Batch multiple `getJiraIssue` calls in parallel for efficiency

## Labels

| Label | Use For |
|-------|---------|
| `feature` | New functionality |
| `bugfix` | Bug fixes |
| `tech-debt` | Technical debt/refactoring |
| `blocked` | Issue is blocked |
| `urgent` | High priority attention needed |

## Description Templates

### Story
```markdown
## User Story
As a [type of user], I want [goal] so that [benefit].

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### Bug
```markdown
## Description
[Brief description]

## Steps to Reproduce
1. Step 1
2. Step 2

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]
```
