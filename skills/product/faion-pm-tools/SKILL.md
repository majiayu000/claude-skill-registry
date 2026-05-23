---
name: faion-pm-tools
user-invocable: false
description: ""
---

# PM Tools Mastery

**Comprehensive guide to project management platforms and workflows**

---

## Quick Reference

| Tool | Best For | Key Strength |
|------|----------|--------------|
| **Jira** | Enterprise, scaled agile | JQL, customization, integrations |
| **ClickUp** | All-in-one workspace | Flexibility, views, automation |
| **Linear** | Engineering teams | Speed, keyboard shortcuts, cycles |
| **GitHub Projects** | Open source, developers | Code integration, issue linking |
| **GitLab Boards** | DevOps teams | CI/CD integration, milestones |
| **Azure DevOps** | Microsoft ecosystem | Enterprise, pipelines, repos |
| **Notion** | Knowledge + PM hybrid | Databases, relations, docs |
| **Trello** | Simple kanban | Simplicity, Butler automation |

---

## M-PMT-001: Jira Workflow Management

### Overview

Jira is the industry standard for agile project management, supporting Scrum, Kanban, and hybrid workflows.

### Project Structure

```
Organization
├── Site (e.g., yourcompany.atlassian.net)
│   ├── Project A (Scrum)
│   │   ├── Board
│   │   ├── Backlog
│   │   ├── Sprints
│   │   └── Releases
│   ├── Project B (Kanban)
│   │   ├── Board
│   │   └── Backlog
│   └── Project C (Team-managed)
```

### Issue Types

| Type | Use Case | Typical Fields |
|------|----------|----------------|
| **Epic** | Large feature, spans sprints | Summary, Description, Priority |
| **Story** | User-facing feature | Story Points, Acceptance Criteria |
| **Task** | Technical work | Estimate, Assignee |
| **Bug** | Defect | Steps to Reproduce, Severity |
| **Sub-task** | Breakdown of parent issue | Parent link |

### JQL (Jira Query Language)

**Basic Queries:**

```jql
# Find my open issues
assignee = currentUser() AND status != Done

# Sprint backlog
project = "PROJ" AND sprint in openSprints()

# Bugs created this week
project = "PROJ" AND issuetype = Bug AND created >= -7d

# Epics without stories
issuetype = Epic AND "Epic Link" is EMPTY

# High priority overdue
priority in (Critical, High) AND duedate < now() AND status != Done
```

**Advanced Queries:**

```jql
# Issues changed status this week
status changed during (startOfWeek(), now())

# Issues in review for > 2 days
status = "In Review" AND status changed before -2d

# Unassigned issues in active sprint
assignee is EMPTY AND sprint in openSprints()

# Issues with no comments
issueFunction in commented("after -30d by any") ORDER BY created DESC
```

### Workflow Best Practices

**Standard Kanban Flow:**
```
Backlog → To Do → In Progress → In Review → Done
```

**Scrum Flow:**
```
Backlog → Sprint Backlog → In Progress → Code Review → QA → Done
```

**Rules:**
- Define clear "Definition of Done" for each status
- Limit WIP (Work in Progress) per column
- Use automation rules for status transitions
- Set required fields before transitions

### Board Configuration

| Setting | Recommendation |
|---------|----------------|
| **Columns** | 4-6 maximum (avoid 10+ columns) |
| **Swimlanes** | By Epic, Assignee, or Priority |
| **Quick Filters** | "Only My Issues", "Bugs Only", "Blocked" |
| **Card Colors** | By Priority or Issue Type |
| **WIP Limits** | In Progress: 3-5 per person |

### Automation Examples

**Auto-assign to reporter:**
```yaml
When: Issue created
If: Assignee is empty
Then: Assign issue to reporter
```

**Move to Done when merged:**
```yaml
When: Pull request merged
If: Issue linked to PR
Then: Transition issue to Done
```

**Notify on blocked:**
```yaml
When: Issue flagged
Then: Send Slack notification to #dev-alerts
```

### Integrations

| Integration | Use Case |
|-------------|----------|
| **Confluence** | Link documentation to issues |
| **Bitbucket/GitHub** | Smart commits, PR linking |
| **Slack** | Notifications, issue creation |
| **Tempo** | Time tracking, timesheets |
| **Zephyr** | Test management |

### Tips

1. **Use components** for team/area ownership
2. **Use labels** for cross-cutting concerns
3. **Create dashboards** for stakeholder reporting
4. **Archive old sprints** quarterly
5. **Review and clean custom fields** regularly

---

## M-PMT-002: ClickUp Setup

### Overview

ClickUp is an all-in-one productivity platform combining project management, docs, and collaboration.

### Hierarchy

```
Workspace
├── Space (e.g., Engineering)
│   ├── Folder (e.g., Product Development)
│   │   ├── List (e.g., Sprint 24.1)
│   │   │   ├── Task
│   │   │   │   └── Subtask
│   │   │   └── Task
│   │   └── List (e.g., Sprint 24.2)
│   └── Folder (e.g., Infrastructure)
└── Space (e.g., Marketing)
```

### Space Configuration

| Setting | Recommendation |
|---------|----------------|
| **Statuses** | Match your workflow (To Do, In Progress, Review, Done) |
| **Custom Fields** | Story Points, Priority, Sprint, Team |
| **Templates** | Create for recurring task types |
| **Automations** | Enable per-space rules |
| **Integrations** | GitHub, Slack, Figma, Google Drive |

### Views

| View | Best For |
|------|----------|
| **List** | Detailed task management, bulk editing |
| **Board** | Kanban workflow, visual status |
| **Calendar** | Deadline management, scheduling |
| **Timeline** | Gantt-style planning, dependencies |
| **Table** | Spreadsheet-like editing |
| **Workload** | Capacity planning, team balance |
| **Mind Map** | Brainstorming, task breakdown |

### Custom Fields

```yaml
# Sprint field (Dropdown)
Sprint:
  - Backlog
  - Sprint 24.1
  - Sprint 24.2
  - Sprint 24.3

# Story Points (Number)
Story Points: 0, 1, 2, 3, 5, 8, 13, 21

# Priority (Dropdown with colors)
Priority:
  - Critical (Red)
  - High (Orange)
  - Medium (Yellow)
  - Low (Blue)
```

### Automations

**When status changes:**
```yaml
Trigger: Status changes to "Done"
Action:
  - Set due date to today
  - Notify watcher via comment
```

**When task created:**
```yaml
Trigger: Task created in "Bugs" list
Action:
  - Set priority to High
  - Assign to QA Lead
  - Add tag "needs-triage"
```

**Recurring tasks:**
```yaml
Trigger: Every Monday at 9 AM
Action: Create task "Weekly standup summary"
  - List: Team Rituals
  - Assignee: Team Lead
  - Due: Same day
```

### Templates

**Bug Report Template:**
```markdown
## Description
[Describe the bug]

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS:
- Browser:
- Version:

## Screenshots
[Attach if applicable]
```

### ClickUp vs Jira

| Feature | ClickUp | Jira |
|---------|---------|------|
| **Setup complexity** | Low | Medium-High |
| **Customization** | High | Very High |
| **Price** | Lower | Higher |
| **Best for** | Startups, SMBs | Enterprise |
| **Docs integration** | Native | Confluence |
| **Learning curve** | Low | Medium |

---

## M-PMT-003: Linear Issue Tracking

### Overview

Linear is designed for high-velocity engineering teams, emphasizing speed, keyboard shortcuts, and beautiful design.

### Core Concepts

```
Workspace
├── Team (e.g., Platform)
│   ├── Projects (time-boxed initiatives)
│   ├── Cycles (sprints)
│   └── Issues
│       ├── Sub-issues
│       └── Comments
└── Team (e.g., Mobile)
```

### Cycle Planning

| Concept | Description |
|---------|-------------|
| **Cycle** | Time-boxed sprint (usually 1-2 weeks) |
| **Cooldown** | Gap between cycles for unplanned work |
| **Auto-archive** | Incomplete issues move to backlog |

**Cycle Configuration:**
- Duration: 1 or 2 weeks
- Cooldown: 1-3 days recommended
- Start day: Monday or Wednesday
- Auto-scheduling: Enable for predictable velocity

### Projects vs Cycles

| Concept | Purpose | Duration |
|---------|---------|----------|
| **Project** | Feature/initiative grouping | Weeks to months |
| **Cycle** | Sprint iteration | 1-2 weeks |
| **Roadmap** | High-level planning | Quarters |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `C` | Create new issue |
| `I` | Open issue details |
| `P` | Set project |
| `L` | Set label |
| `A` | Assign |
| `S` | Set status |
| `E` | Estimate |
| `Cmd+K` | Command palette |
| `G I` | Go to Inbox |
| `G M` | Go to My Issues |
| `G B` | Go to Board |

### Status Workflow

**Default Statuses:**
```
Triage → Backlog → Todo → In Progress → In Review → Done
                                            ↓
                                        Cancelled
```

**Custom Statuses:**
- Add "Blocked" after In Progress
- Add "QA" before Done
- Add "Deployed" after Done

### Labels & Filters

**Recommended Labels:**
```yaml
Type:
  - bug
  - feature
  - improvement
  - chore
  - documentation

Area:
  - frontend
  - backend
  - infrastructure
  - design

Priority:
  - urgent
  - high
  - medium
  - low
```

**Saved Filters:**
```
# My team's active work
team = "Platform" AND status in (Todo, "In Progress", "In Review")

# Bugs to triage
label = "bug" AND status = Triage

# Blocked issues
status = Blocked
```

### Integrations

| Integration | Features |
|-------------|----------|
| **GitHub** | Link PRs, auto-close issues |
| **GitLab** | Same as GitHub |
| **Slack** | Notifications, issue creation |
| **Figma** | Link designs to issues |
| **Sentry** | Auto-create issues from errors |
| **Zendesk** | Link support tickets |

### GitHub Integration

**Setup:**
1. Connect GitHub organization
2. Enable "Link PRs to issues"
3. Enable "Auto-close issues on merge"

**Branch naming convention:**
```
# Linear auto-detects these patterns
TEAM-123-feature-description
team-123/feature-description
```

### Roadmaps

```
Roadmap View:
├── Q1 2026
│   ├── Project: User Authentication
│   ├── Project: Payment System
│   └── Project: Mobile App
├── Q2 2026
│   └── Project: Analytics Dashboard
└── Backlog
    └── Project: AI Features
```

---

## M-PMT-004: GitHub Projects

### Overview

GitHub Projects (v2) provides native project management integrated with GitHub issues and pull requests.

### Project Types

| Type | Best For |
|------|----------|
| **Board** | Kanban workflow |
| **Table** | Spreadsheet-like view |
| **Roadmap** | Timeline planning |

### Setup

```
Organization
└── Project (e.g., Product Roadmap)
    ├── Views
    │   ├── Board (Status)
    │   ├── Table (All Fields)
    │   └── Roadmap (Timeline)
    ├── Fields
    │   ├── Status (Single select)
    │   ├── Priority (Single select)
    │   ├── Sprint (Iteration)
    │   └── Estimate (Number)
    └── Items (Issues, PRs, Draft issues)
```

### Custom Fields

```yaml
# Status (Single select)
Status:
  - Backlog
  - Ready
  - In Progress
  - In Review
  - Done

# Priority (Single select)
Priority:
  - P0 - Critical
  - P1 - High
  - P2 - Medium
  - P3 - Low

# Sprint (Iteration)
Sprint:
  Duration: 2 weeks
  Start: Monday

# Estimate (Number)
# Use for story points: 1, 2, 3, 5, 8, 13
```

### Automations

**Built-in Automations:**

| Trigger | Action |
|---------|--------|
| Item added to project | Set status to Backlog |
| Item reopened | Set status to Ready |
| Item closed | Set status to Done |
| PR merged | Set status to Done |
| Code review requested | Set status to In Review |

**GraphQL Custom Automations:**
```graphql
mutation {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: "PROJECT_ID"
      itemId: "ITEM_ID"
      fieldId: "STATUS_FIELD_ID"
      value: {singleSelectOptionId: "DONE_OPTION_ID"}
    }
  ) {
    projectV2Item {
      id
    }
  }
}
```

### Workflows with GitHub Actions

**Auto-add issues to project:**
```yaml
name: Add issue to project
on:
  issues:
    types: [opened]

jobs:
  add-to-project:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/orgs/ORG/projects/1
          github-token: ${{ secrets.ADD_TO_PROJECT_PAT }}
```

**Auto-set fields:**
```yaml
name: Set priority on bug
on:
  issues:
    types: [labeled]

jobs:
  set-priority:
    if: github.event.label.name == 'bug'
    runs-on: ubuntu-latest
    steps:
      - uses: titoportas/update-project-fields@v0.1.0
        with:
          project-url: https://github.com/orgs/ORG/projects/1
          github-token: ${{ secrets.GITHUB_TOKEN }}
          item-id: ${{ github.event.issue.node_id }}
          field-keys: Priority
          field-values: P1 - High
```

### Views Configuration

**Board View:**
```yaml
View: Kanban Board
Group by: Status
Sort by: Priority (descending)
Filter: is:open assignee:@me
```

**Table View:**
```yaml
View: Sprint Planning
Columns: Title, Status, Priority, Estimate, Sprint, Assignee
Sort by: Priority
Filter: sprint:current
```

**Roadmap View:**
```yaml
View: Q1 Roadmap
Date field: Sprint (start/end)
Group by: Milestone
Zoom: Months
```

### Issue Templates

**.github/ISSUE_TEMPLATE/bug_report.yml:**
```yaml
name: Bug Report
description: ""
labels: [bug, triage]
body:
  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: Clear description of the bug
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      value: |
        1. Go to '...'
        2. Click on '...'
        3. See error
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - Critical
        - High
        - Medium
        - Low
```

---

## M-PMT-005: GitLab Boards

### Overview

GitLab provides integrated issue boards with native CI/CD integration and DevOps workflows.

### Board Types

| Type | Scope | Best For |
|------|-------|----------|
| **Project Board** | Single repository | Small teams |
| **Group Board** | Multiple projects | Cross-team work |
| **Iteration Board** | Time-boxed sprints | Scrum teams |

### Structure

```
Group
├── Project A
│   ├── Issues
│   ├── Board (Project scope)
│   ├── Milestones
│   └── Labels
├── Project B
│   └── ...
└── Group Board (Cross-project)
```

### Labels Strategy

**Scoped Labels (mutually exclusive):**
```
workflow::backlog
workflow::ready
workflow::in-progress
workflow::review
workflow::done

priority::critical
priority::high
priority::medium
priority::low

type::feature
type::bug
type::chore
```

### Milestones

```yaml
Milestone: v2.0.0
  Due date: 2026-03-01
  Issues:
    - Feature: User authentication
    - Feature: Payment integration
    - Bug: Login timeout issue

Milestone: Sprint 24.1
  Start: 2026-01-13
  Due: 2026-01-27
  Iteration cadence: Bi-weekly
```

### Board Configuration

**Columns (based on labels):**
```
Open → workflow::ready → workflow::in-progress → workflow::review → Closed
```

**Filters:**
```
# Show only my issues
assignee_username = @me

# Current milestone
milestone = "Sprint 24.1"

# High priority bugs
label = priority::high AND label = type::bug
```

### Merge Request Integration

**Auto-close issues:**
```markdown
# In MR description
Closes #123
Fixes #456
Resolves #789
```

**Link without closing:**
```markdown
Related to #123
See #456
```

### CI/CD Integration

**.gitlab-ci.yml with issue tracking:**
```yaml
deploy:
  stage: deploy
  script:
    - deploy.sh
  environment:
    name: production
    url: https://app.example.com
    deployment_tier: production

# Auto-create issue on failure
on_failure:
  stage: notify
  script:
    - |
      curl --request POST \
        --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        --data "title=Pipeline failed: $CI_PIPELINE_ID" \
        --data "labels=bug,pipeline-failure" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/issues"
  when: on_failure
```

### Quick Actions

| Command | Action |
|---------|--------|
| `/assign @user` | Assign issue |
| `/label ~bug ~urgent` | Add labels |
| `/milestone %"Sprint 24.1"` | Set milestone |
| `/estimate 2h` | Set time estimate |
| `/spend 1h` | Log time spent |
| `/due 2026-01-31` | Set due date |
| `/close` | Close issue |
| `/relate #123` | Link to issue |

### Epics (Premium)

```
Epic: User Authentication System
├── Feature: Login page
├── Feature: OAuth integration
├── Feature: Password reset
└── Feature: 2FA support
```

---

## M-PMT-006: Azure DevOps Boards

### Overview

Azure DevOps provides enterprise-grade project management with deep Microsoft integration.

### Work Item Types

| Type | Agile | Scrum | CMMI |
|------|-------|-------|------|
| **Top Level** | Epic | Epic | Epic |
| **Feature** | Feature | Feature | Feature |
| **Backlog** | User Story | PBI | Requirement |
| **Task** | Task | Task | Task |
| **Bug** | Bug | Bug | Bug |

### Process Templates

```
Agile: Epic → Feature → User Story → Task
Scrum: Epic → Feature → PBI → Task
CMMI:  Epic → Feature → Requirement → Task
Basic: Epic → Issue → Task
```

### Board Configuration

**Columns:**
```
New → Active → Resolved → Closed
    → Approved → Committed → Done  (Scrum)
```

**Swimlanes:**
- By Team Member
- By Area Path
- By Parent Item
- Expedite Lane (for urgent items)

### Queries

**Flat Query:**
```
Work Item Type = Bug
AND State <> Closed
AND Assigned To = @Me
AND Area Path Under "Project\TeamA"
```

**Tree Query:**
```
# Parent items
Work Item Type In (Epic, Feature)
AND State <> Done

# Child items (linked)
Work Item Type = User Story
```

**Direct Links Query:**
```
# Find orphan stories (no parent)
Work Item Type = User Story
AND Link Type <> Parent
```

### Sprints/Iterations

**Setup:**
```
Project Settings → Boards → Project Configuration
└── Iterations
    ├── Sprint 1 (Jan 1-14)
    ├── Sprint 2 (Jan 15-28)
    └── Sprint 3 (Jan 29 - Feb 11)
```

**Capacity Planning:**
```yaml
Team Member: John
  Activity: Development
  Capacity: 6 hours/day
  Days off: Jan 10

Team Member: Jane
  Activity: Development
  Capacity: 8 hours/day
  Activity: Testing
  Capacity: 2 hours/day
```

### Dashboards

**Widgets:**
| Widget | Purpose |
|--------|---------|
| **Burndown** | Sprint progress |
| **Velocity** | Team capacity trend |
| **Cumulative Flow** | Work item flow |
| **Query Results** | Custom queries |
| **Build History** | Pipeline status |
| **Test Results** | Test pass rate |

### Pipelines Integration

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UpdateWorkItem@1
    inputs:
      workItemId: '$(System.PullRequest.WorkItemId)'
      state: 'Active'
    condition: eq(variables['Build.Reason'], 'PullRequest')
```

### Wiki & Documentation

```
Wiki
├── Home
├── Architecture
│   ├── System Overview
│   └── API Documentation
├── Development
│   ├── Getting Started
│   └── Coding Standards
└── Operations
    └── Runbooks
```

---

## M-PMT-007: Notion PM

### Overview

Notion combines project management with documentation, using flexible databases and relations.

### Database Structure

```
Workspace
├── Projects (Database)
│   └── Properties: Status, Owner, Timeline, Team
├── Tasks (Database)
│   └── Properties: Status, Project (Relation), Assignee, Due
├── Sprints (Database)
│   └── Properties: Start, End, Goal, Tasks (Relation)
└── Team (Database)
    └── Properties: Name, Role, Tasks (Relation)
```

### Database Properties

**Projects Database:**
```yaml
Properties:
  - Name (Title)
  - Status (Select): Planning, Active, Complete, On Hold
  - Owner (Person)
  - Team (Multi-select)
  - Timeline (Date range)
  - Priority (Select): P0, P1, P2, P3
  - Tasks (Relation → Tasks)
  - Progress (Formula): Tasks complete / Total tasks
```

**Tasks Database:**
```yaml
Properties:
  - Task (Title)
  - Status (Select): Backlog, Todo, In Progress, Review, Done
  - Project (Relation → Projects)
  - Sprint (Relation → Sprints)
  - Assignee (Person)
  - Due Date (Date)
  - Estimate (Number): Story points
  - Priority (Select)
  - Type (Select): Feature, Bug, Chore
```

### Views

| View Type | Use Case |
|-----------|----------|
| **Table** | Full data, filtering, sorting |
| **Board** | Kanban by status |
| **Calendar** | Due date planning |
| **Timeline** | Gantt-style view |
| **List** | Compact view |
| **Gallery** | Visual cards |

### Formulas

**Progress calculation:**
```
# In Projects database
round(prop("Tasks Complete") / prop("Total Tasks") * 100)
```

**Days until due:**
```
dateBetween(prop("Due Date"), now(), "days")
```

**Priority score:**
```
if(prop("Priority") == "P0", 4,
  if(prop("Priority") == "P1", 3,
    if(prop("Priority") == "P2", 2, 1)))
```

### Templates

**Meeting Notes Template:**
```markdown
# Meeting: [Title]
Date: [Date]
Attendees: [People]

## Agenda
- [ ] Item 1
- [ ] Item 2

## Notes


## Action Items
- [ ] @person: Task by [date]

## Decisions Made

```

**Sprint Planning Template:**
```markdown
# Sprint [Number]
Duration: [Start] - [End]

## Sprint Goal
[One sentence goal]

## Committed Items
[Linked tasks view filtered by Sprint = current]

## Capacity
| Team Member | Available Days | Capacity |
|-------------|----------------|----------|
| @person1    | 10             | 80 pts   |

## Risks
- Risk 1
```

### Automations (with Buttons)

**Button: Create Sprint Tasks:**
```
Action: Create pages in Tasks database
Template: Task template
Properties:
  Sprint: Current sprint
  Status: Backlog
```

**Button: Complete Sprint:**
```
Action:
  1. Move incomplete tasks to next sprint
  2. Archive current sprint
  3. Create retrospective page
```

### Integrations

| Integration | Features |
|-------------|----------|
| **Slack** | Page updates, notifications |
| **GitHub** | Link PRs, sync issues |
| **Figma** | Embed designs |
| **Loom** | Embed videos |
| **Google Drive** | Embed docs |

---

## M-PMT-008: Trello Kanban

### Overview

Trello provides simple, visual kanban boards with powerful automation through Butler.

### Board Structure

```
Board: Product Development
├── Lists
│   ├── Backlog
│   ├── To Do (This Sprint)
│   ├── In Progress
│   ├── Review
│   └── Done
├── Labels
│   ├── Bug (Red)
│   ├── Feature (Green)
│   ├── Improvement (Yellow)
│   └── Urgent (Orange)
└── Cards
    └── Card content, checklists, attachments
```

### Card Best Practices

**Card Structure:**
```markdown
# Card Title
[Verb] + [Object] + [Context]
Example: "Implement user login with OAuth"

# Description
## Problem
What problem does this solve?

## Solution
High-level approach

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Notes
Additional context
```

**Checklists:**
```
[ ] Design approved
[ ] Implementation complete
[ ] Tests written
[ ] Code reviewed
[ ] Documentation updated
```

### Labels Strategy

| Label | Color | Use |
|-------|-------|-----|
| **Bug** | Red | Defects |
| **Feature** | Green | New functionality |
| **Improvement** | Yellow | Enhancements |
| **Tech Debt** | Purple | Refactoring |
| **Blocked** | Orange | Waiting on something |
| **Quick Win** | Blue | < 2 hours |

### Butler Automation

**When card moved to Done:**
```yaml
Trigger: When a card is moved to list "Done"
Actions:
  - Mark due date complete
  - Remove all members
  - Add comment "@board Done!"
```

**Daily cleanup:**
```yaml
Trigger: Every day at 9:00 AM
Actions:
  - Move cards with due date in the past from "To Do" to "Overdue"
  - Sort "Backlog" by due date
```

**Card button - Start Working:**
```yaml
Button: Start Working
Actions:
  - Move card to "In Progress"
  - Add me to card
  - Set due date to 3 days from now
```

**Board button - Create Sprint:**
```yaml
Button: Create Sprint
Actions:
  - Create list "Sprint [date]"
  - Move top 10 cards from "Backlog" to new list
```

### Power-Ups

| Power-Up | Purpose |
|----------|---------|
| **Calendar** | View cards by due date |
| **Custom Fields** | Add estimates, priorities |
| **Card Aging** | Visualize stale cards |
| **Voting** | Prioritization |
| **GitHub** | Link PRs and commits |
| **Slack** | Notifications |

### Custom Fields

```yaml
Fields:
  - Story Points (Number): 1, 2, 3, 5, 8, 13
  - Priority (Dropdown): Critical, High, Medium, Low
  - Sprint (Dropdown): Sprint 1, Sprint 2, Sprint 3
  - Assignee (Dropdown): Team members
```

### Views

| View | Purpose |
|------|---------|
| **Board** | Default kanban |
| **Timeline** | Gantt-style (Premium) |
| **Calendar** | Due date view |
| **Table** | Spreadsheet view |
| **Dashboard** | Metrics (Premium) |

---

## M-PMT-009: Cross-Tool Migration

### Overview

Migrate data between PM tools while preserving history, relationships, and workflows.

### Migration Planning

```
1. Audit Source Data
   ├── Issue count
   ├── Custom fields
   ├── Attachments
   ├── Comments
   └── Links/relations

2. Map Data Model
   ├── Issue types → Work item types
   ├── Statuses → Statuses
   ├── Fields → Fields
   └── Users → Users

3. Test Migration
   └── Small subset first

4. Execute Migration
   └── Full data transfer

5. Validate
   ├── Data integrity
   ├── Link preservation
   └── User mapping
```

### Common Migrations

**Jira to Linear:**
```yaml
Mapping:
  Issue Types:
    Story → Issue
    Bug → Issue (label: bug)
    Epic → Project
    Task → Issue

  Statuses:
    To Do → Todo
    In Progress → In Progress
    In Review → In Review
    Done → Done

  Fields:
    Story Points → Estimate
    Sprint → Cycle
    Priority → Priority
    Labels → Labels
```

**Trello to ClickUp:**
```yaml
Mapping:
  Board → Space
  List → Status
  Card → Task
  Checklist → Subtasks
  Labels → Tags
  Due Date → Due Date
  Members → Assignees
```

**Asana to Notion:**
```yaml
Mapping:
  Project → Database
  Section → Status (property)
  Task → Page
  Subtask → Sub-page or Checkbox
  Tags → Multi-select
  Custom Fields → Properties
```

### Export Formats

| Tool | Export Format | Method |
|------|---------------|--------|
| **Jira** | JSON, CSV | Project settings → Export |
| **Trello** | JSON | Board menu → Export |
| **Asana** | CSV, JSON (API) | Project → Export |
| **Linear** | JSON (API) | GraphQL API |
| **GitHub** | JSON (API) | REST/GraphQL API |
| **ClickUp** | CSV | Space → Export |

### Jira Export Script

```python
import requests
from requests.auth import HTTPBasicAuth

JIRA_URL = "https://your-domain.atlassian.net"
EMAIL = "your@email.com"
API_TOKEN = "your-api-token"

auth = HTTPBasicAuth(EMAIL, API_TOKEN)

# Export all issues
response = requests.get(
    f"{JIRA_URL}/rest/api/3/search",
    auth=auth,
    params={
        "jql": "project = PROJ",
        "maxResults": 100,
        "expand": "changelog,comments"
    }
)

issues = response.json()["issues"]
```

### Import Strategies

**Batch Import:**
```python
# Create issues in batches
BATCH_SIZE = 50
for i in range(0, len(issues), BATCH_SIZE):
    batch = issues[i:i + BATCH_SIZE]
    create_issues(batch)
    time.sleep(1)  # Rate limiting
```

**Maintain References:**
```python
# Create mapping table
old_to_new_ids = {}

for old_issue in old_issues:
    new_issue = create_issue(transform(old_issue))
    old_to_new_ids[old_issue.id] = new_issue.id

# Update links
for old_id, new_id in old_to_new_ids.items():
    update_links(new_id, old_to_new_ids)
```

### Migration Checklist

- [ ] Export all data from source
- [ ] Map all fields and statuses
- [ ] Map users (handle inactive)
- [ ] Test with subset (10-20 items)
- [ ] Validate test migration
- [ ] Schedule full migration
- [ ] Notify team of downtime
- [ ] Execute full migration
- [ ] Validate data integrity
- [ ] Fix any issues
- [ ] Train team on new tool
- [ ] Deprecate old tool access

---

## M-PMT-010: PM Tool Selection

### Overview

Framework for choosing the right PM tool based on team needs, scale, and workflows.

### Selection Criteria

| Criterion | Weight | Questions |
|-----------|--------|-----------|
| **Team Size** | High | 5? 50? 500+ users? |
| **Methodology** | High | Scrum, Kanban, or hybrid? |
| **Integration** | High | What tools must it connect with? |
| **Budget** | Medium | Per user cost acceptable? |
| **Complexity** | Medium | Simple or highly customizable? |
| **Learning Curve** | Medium | Time to onboard? |
| **Security** | High | Compliance requirements? |

### Decision Matrix

```
                    Simple ←───────────────────→ Complex
                      │                              │
        Trello ───────┤                              │
                      │                              │
        ClickUp ──────┼───────────────────┐          │
                      │                   │          │
        Linear ───────┼───────────────────┤          │
                      │                   │          │
        GitHub ───────┼───────────────────┤          │
                      │                   │          │
        Notion ───────┼───────────────────┼──────────┤
                      │                   │          │
        GitLab ───────┼───────────────────┼──────────┤
                      │                   │          │
        Jira ─────────┼───────────────────┴──────────┤
                      │                              │
        Azure DevOps ─┼──────────────────────────────┤
                      │                              │
        Small Team    │                   Enterprise │
```

### Tool Comparison

| Tool | Best For | Avoid If |
|------|----------|----------|
| **Trello** | Simple projects, small teams | Complex workflows, reporting |
| **ClickUp** | All-in-one needs, flexibility | Need Jira integrations |
| **Linear** | Engineering teams, speed | Non-technical users |
| **GitHub Projects** | Open source, developers | Non-GitHub workflows |
| **GitLab** | DevOps focus, self-hosted | No CI/CD needs |
| **Jira** | Enterprise, scaled agile | Budget-constrained |
| **Azure DevOps** | Microsoft shops | Non-Microsoft stack |
| **Notion** | Docs + PM hybrid | Pure PM focus |

### Team Size Recommendations

| Size | Recommended | Notes |
|------|-------------|-------|
| **1-5** | Trello, Linear, Notion | Keep it simple |
| **5-20** | ClickUp, Linear, GitHub | Balance features/simplicity |
| **20-100** | Jira, ClickUp, GitLab | Need customization |
| **100+** | Jira, Azure DevOps | Enterprise features |

### Questions Checklist

**Workflow:**
- [ ] Scrum with sprints?
- [ ] Kanban continuous flow?
- [ ] Hybrid approach?
- [ ] Multiple teams/projects?

**Integration:**
- [ ] Git platform (GitHub/GitLab/Bitbucket)?
- [ ] Communication (Slack/Teams)?
- [ ] Documentation (Confluence/Notion)?
- [ ] CI/CD (Jenkins/GitHub Actions)?

**Features:**
- [ ] Time tracking needed?
- [ ] Roadmap planning?
- [ ] Resource management?
- [ ] Custom workflows?
- [ ] Reporting/dashboards?

**Constraints:**
- [ ] Budget per user?
- [ ] Self-hosted requirement?
- [ ] Compliance (SOC2, HIPAA)?
- [ ] SSO/SAML requirement?

### Migration Considerations

| From | To | Difficulty |
|------|-----|------------|
| Trello → ClickUp | Easy | Native import |
| Jira → Linear | Medium | API migration |
| Asana → Notion | Medium | Manual/API |
| Any → Jira | Medium | Good importers |
| Jira → Any | Hard | Complex data model |

---

## M-PMT-011: Agile Ceremonies Setup

### Overview

Configure and run effective agile ceremonies across any PM tool.

### Ceremony Overview

| Ceremony | Frequency | Duration | Purpose |
|----------|-----------|----------|---------|
| **Sprint Planning** | Start of sprint | 2-4 hours | Plan sprint work |
| **Daily Standup** | Daily | 15 min | Sync, blockers |
| **Sprint Review** | End of sprint | 1-2 hours | Demo to stakeholders |
| **Retrospective** | End of sprint | 1-1.5 hours | Improve process |
| **Backlog Refinement** | Weekly | 1 hour | Prepare future work |

### Sprint Planning

**Before Meeting:**
```yaml
Preparation:
  - Backlog is prioritized (PO)
  - Stories have acceptance criteria
  - Stories are estimated
  - Team capacity calculated
```

**Meeting Structure:**
```
1. Review sprint goal (5 min)
2. Team capacity check (10 min)
3. Select items from backlog (30 min)
4. Break down into tasks (60 min)
5. Confirm commitment (15 min)
```

**Tool Setup (Example: Jira):**
```yaml
Sprint Planning View:
  - Filter: project = PROJ AND sprint is EMPTY
  - Sort: Rank ascending
  - Visible fields: Key, Summary, Story Points, Priority

Sprint Board:
  - Quick filters: "Only My Issues", "Unassigned"
  - Swimlanes: By Assignee
```

### Daily Standup

**Format (15 min max):**
```
Each team member:
1. What I completed yesterday
2. What I'm working on today
3. Any blockers

Walk the board (alternative):
1. Review "In Review" column
2. Review "In Progress" column
3. Review "To Do" for priorities
```

**Tool Setup:**
```yaml
Standup Dashboard:
  Widgets:
    - Sprint Burndown
    - Active Sprint Items (by status)
    - Blocked Items
    - Items without estimates
```

**Async Standup (Remote Teams):**
```yaml
Slack Bot Schedule: 9:00 AM daily
Questions:
  1. What did you accomplish yesterday?
  2. What will you work on today?
  3. Any blockers?
Post to: #team-standup
```

### Sprint Review

**Agenda:**
```
1. Sprint goal achievement (5 min)
2. Demo completed features (30-45 min)
3. Metrics review (10 min)
4. Stakeholder feedback (15 min)
5. Next sprint preview (10 min)
```

**Demo Checklist:**
```
For each completed story:
- [ ] Feature name and user value
- [ ] Live demonstration
- [ ] Edge cases handled
- [ ] Questions from stakeholders
```

### Retrospective

**Formats:**

**Start/Stop/Continue:**
```
Start doing:
- [Team suggestions]

Stop doing:
- [Team suggestions]

Continue doing:
- [Team suggestions]
```

**4Ls (Liked/Learned/Lacked/Longed For):**
```
Liked:
- What went well

Learned:
- New insights

Lacked:
- Missing resources/support

Longed For:
- Wished we had
```

**Mad/Sad/Glad:**
```
Mad (frustrated):
- [Issues]

Sad (disappointed):
- [Issues]

Glad (happy):
- [Positives]
```

**Tool Setup (Example: Notion):**
```yaml
Retrospective Database:
  Properties:
    - Sprint (Relation)
    - Category (Select): Start, Stop, Continue
    - Item (Title)
    - Action Owner (Person)
    - Status (Select): Open, Done

Template:
  - Section for each category
  - Voting enabled
  - Timer for timeboxing
```

### Backlog Refinement

**Agenda (1 hour):**
```
1. Review upcoming priorities (10 min)
2. Discuss unclear stories (20 min)
3. Estimate stories (20 min)
4. Update acceptance criteria (10 min)
```

**Definition of Ready:**
```
Story is ready when:
- [ ] Has clear acceptance criteria
- [ ] Is estimated
- [ ] Dependencies identified
- [ ] No open questions
- [ ] Small enough for one sprint
```

### Ceremony Calendar

```
Monday:    Sprint Planning (Week 1)
           Backlog Refinement (Week 2)

Tuesday:   Standup
Wednesday: Standup
Thursday:  Standup
Friday:    Standup
           Sprint Review + Retro (Week 2)
```

---

## M-PMT-012: Reporting & Dashboards

### Overview

Build effective dashboards for tracking progress, velocity, and team health.

### Key Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Velocity** | Story points per sprint | Stable +/- 10% |
| **Burndown** | Work remaining over time | Linear decline |
| **Cycle Time** | Start to done duration | Decreasing |
| **Lead Time** | Created to done duration | Depends on type |
| **Throughput** | Items completed per period | Stable/increasing |
| **WIP** | Items in progress | Within limits |
| **Escaped Defects** | Bugs found in production | Decreasing |

### Burndown Chart

**Reading the Chart:**
```
Points
  │
30├──●
  │    ●─Ideal line
20├──────●
  │        ●
10├──────────●──Actual line
  │            ●
 0├──────────────●
  └─────────────────
  Day 1  5    10   14
```

**Interpretation:**
- Above ideal: Behind schedule
- Below ideal: Ahead of schedule
- Flat line: No work completed (blocked?)
- Steep drop: Large item completed

### Velocity Chart

```
Points
  │
40├        ▓▓▓▓▓
  │   ▓▓▓▓▓▓▓▓▓▓     ▓▓▓▓▓
30├───▓▓▓▓▓▓▓▓▓▓─────▓▓▓▓▓─── Average
  │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
20├   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
10├
  │
  └──────────────────────────
    S1  S2  S3  S4  S5  S6
```

**Use for:**
- Sprint capacity planning
- Forecasting release dates
- Identifying trend changes

### Cumulative Flow Diagram

```
Items
  │        Done ████████████████
50├       ██████████████████████
  │    Review ██████████████████
40├    ████████████████████████
  │  Progress ██████████████████
30├  ██████████████████████████
  │  To Do ████████████████████
20├  ██████████████████████████
  │  Backlog ██████████████████
10├
  │
  └──────────────────────────────
    Week 1    Week 2    Week 3
```

**Interpretation:**
- Band width = WIP in that state
- Vertical slice = All work at that time
- Narrowing bands = Items moving through

### Dashboard Templates

**Sprint Dashboard:**
```yaml
Layout: 2x3 grid

Row 1:
  - Sprint Burndown (50%)
  - Sprint Goal + Days Remaining (50%)

Row 2:
  - Sprint Backlog by Status (33%)
  - Blocked Items (33%)
  - Team Capacity (33%)

Row 3:
  - Items by Assignee (50%)
  - Story Points by Type (50%)
```

**Release Dashboard:**
```yaml
Layout: 2x2 grid

Row 1:
  - Release Burnup (50%)
  - Velocity Trend (50%)

Row 2:
  - Features by Status (50%)
  - Bug Trend (50%)
```

**Team Health Dashboard:**
```yaml
Layout: 3x2 grid

Row 1:
  - Velocity (last 6 sprints)
  - Escaped Defects

Row 2:
  - Cycle Time Distribution
  - PR Review Time

Row 3:
  - Team Availability
  - Action Items from Retros
```

### Tool-Specific Dashboards

**Jira Dashboard:**
```yaml
Gadgets:
  - Sprint Burndown Chart
  - Sprint Health Gadget
  - Pie Chart (Issues by Status)
  - Filter Results (My Open Issues)
  - Two Dimensional Filter (Type vs Priority)
```

**Linear Insights:**
```yaml
Metrics:
  - Completed issues trend
  - Cycle time by team
  - SLA compliance
  - Issue age distribution
```

**ClickUp Dashboard:**
```yaml
Widgets:
  - Sprint progress bar
  - Time tracked vs estimated
  - Workload by member
  - Custom charts
```

### Report Templates

**Weekly Status Report:**
```markdown
# Week [N] Status Report

## Sprint Progress
- Sprint: [Name]
- Days remaining: [N]
- Velocity (target/actual): [X]/[Y] points

## Completed This Week
- [Item 1]
- [Item 2]

## In Progress
- [Item 1] - 80% complete
- [Item 2] - 50% complete

## Blockers
- [Blocker 1] - Owner: [Name], ETA: [Date]

## Risks
- [Risk 1] - Mitigation: [Plan]

## Next Week
- [Priority 1]
- [Priority 2]
```

**Monthly Metrics Report:**
```markdown
# [Month] Metrics Report

## Velocity Trend
| Sprint | Committed | Completed | % |
|--------|-----------|-----------|---|
| S1     | 40        | 38        | 95% |
| S2     | 42        | 40        | 95% |
| S3     | 45        | 42        | 93% |

## Quality Metrics
- Bugs created: [N]
- Bugs resolved: [N]
- Escaped defects: [N]

## Cycle Time
- Average: [N] days
- P90: [N] days

## Team Highlights
- [Achievement 1]
- [Achievement 2]

## Areas for Improvement
- [Area 1]
- [Area 2]
```

---

## References

- [Atlassian Agile Coach](https://www.atlassian.com/agile)
- [Linear Method](https://linear.app/method)
- [ClickUp University](https://university.clickup.com/)
- [GitHub Projects Docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Azure DevOps Docs](https://learn.microsoft.com/en-us/azure/devops/)
- [Notion Templates](https://www.notion.so/templates)
- [Agile Alliance](https://www.agilealliance.org/agile101/)


---

## Methodologies

| ID | Name | File |
|----|------|------|
| M-PMT-001 | Jira Workflow Management | [methodologies/M-PMT-001_jira_workflow_management.md](methodologies/M-PMT-001_jira_workflow_management.md) |
| M-PMT-002 | Clickup Setup | [methodologies/M-PMT-002_clickup_setup.md](methodologies/M-PMT-002_clickup_setup.md) |
| M-PMT-003 | Linear Issue Tracking | [methodologies/M-PMT-003_linear_issue_tracking.md](methodologies/M-PMT-003_linear_issue_tracking.md) |
| M-PMT-004 | Github Projects | [methodologies/M-PMT-004_github_projects.md](methodologies/M-PMT-004_github_projects.md) |
| M-PMT-005 | Gitlab Boards | [methodologies/M-PMT-005_gitlab_boards.md](methodologies/M-PMT-005_gitlab_boards.md) |
| M-PMT-006 | Azure Devops Boards | [methodologies/M-PMT-006_azure_devops_boards.md](methodologies/M-PMT-006_azure_devops_boards.md) |
| M-PMT-007 | Notion Pm | [methodologies/M-PMT-007_notion_pm.md](methodologies/M-PMT-007_notion_pm.md) |
| M-PMT-008 | Trello Kanban | [methodologies/M-PMT-008_trello_kanban.md](methodologies/M-PMT-008_trello_kanban.md) |
| M-PMT-009 | Cross Tool Migration | [methodologies/M-PMT-009_cross_tool_migration.md](methodologies/M-PMT-009_cross_tool_migration.md) |
| M-PMT-010 | Pm Tool Selection | [methodologies/M-PMT-010_pm_tool_selection.md](methodologies/M-PMT-010_pm_tool_selection.md) |
| M-PMT-011 | Agile Ceremonies Setup | [methodologies/M-PMT-011_agile_ceremonies_setup.md](methodologies/M-PMT-011_agile_ceremonies_setup.md) |
| M-PMT-012 | Reporting Dashboards | [methodologies/M-PMT-012_reporting_dashboards.md](methodologies/M-PMT-012_reporting_dashboards.md) |
