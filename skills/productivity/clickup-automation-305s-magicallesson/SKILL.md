---
name: ClickUp Automation
description: Automate ClickUp workspace management, task workflows, time tracking, and team productivity
version: 1.0.0
author: Claude Office Skills
category: project-management
tags:
  - clickup
  - tasks
  - productivity
  - project-management
  - automation
department: operations
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: project-mcp
  tools:
    - clickup_task
    - clickup_list
    - clickup_space
    - clickup_automation
capabilities:
  - Task management
  - Workflow automation
  - Time tracking
  - Goal tracking
input:
  - Task details
  - Space configurations
  - Automation rules
  - Time entries
output:
  - Created/updated tasks
  - Workspace reports
  - Time reports
  - Goal progress
languages:
  - en
related_skills:
  - asana-automation
  - jira-automation
  - monday-automation
---

# ClickUp Automation

Comprehensive skill for automating ClickUp workspace and task management.

## Core Concepts

### Workspace Hierarchy

```
CLICKUP HIERARCHY:
┌─────────────────────────────────────────────────────────┐
│ 🏢 WORKSPACE                                            │
├─────────────────────────────────────────────────────────┤
│   ├── 📁 SPACE: Engineering                             │
│   │   ├── 📂 FOLDER: Q1 Projects                       │
│   │   │   ├── 📋 LIST: Feature Development             │
│   │   │   │   ├── ✅ Task: Implement Auth              │
│   │   │   │   │   └── ☑️ Subtask: OAuth setup          │
│   │   │   │   └── ✅ Task: Build API                   │
│   │   │   └── 📋 LIST: Bug Fixes                       │
│   │   └── 📂 FOLDER: Infrastructure                    │
│   │                                                     │
│   ├── 📁 SPACE: Marketing                               │
│   │   └── 📋 LIST: Content Calendar                    │
│   │                                                     │
│   └── 📁 SPACE: Operations                              │
└─────────────────────────────────────────────────────────┘
```

### Task Structure

```yaml
task_structure:
  required:
    name: "{{task_name}}"
    list_id: "{{list_id}}"
    
  optional:
    description: "{{description}}"
    assignees: ["user_id_1", "user_id_2"]
    tags: ["feature", "priority"]
    status: "Open"
    priority: 2  # 1=Urgent, 2=High, 3=Normal, 4=Low
    due_date: "2024-01-20"
    start_date: "2024-01-15"
    time_estimate: 28800000  # milliseconds (8 hours)
    
  custom_fields:
    - id: "field_id"
      value: "custom_value"
      
  checklists:
    - name: "Acceptance Criteria"
      items:
        - name: "Requirement 1"
          resolved: false
```

## Automation Rules

### Built-in Automations

```yaml
automations:
  - name: auto_assign_on_create
    trigger:
      type: task_created
      list_id: "list_123"
    conditions:
      - tag_contains: "design"
    actions:
      - add_assignee: "design_lead_id"
      - set_priority: high
      
  - name: due_date_reminder
    trigger:
      type: due_date
      before: 1_day
    actions:
      - send_notification:
          to: assignees
          message: "Task due tomorrow: {{task.name}}"
      - add_tag: "due-soon"
      
  - name: status_change_workflow
    trigger:
      type: status_changed
      to: "In Review"
    actions:
      - remove_assignee: "{{previous_assignee}}"
      - add_assignee: "reviewer_id"
      - add_comment: "Ready for review @reviewer"
      
  - name: complete_parent_task
    trigger:
      type: all_subtasks_done
    actions:
      - set_status: "Complete"
      - add_comment: "All subtasks completed ✓"
```

### Advanced Automations

```yaml
advanced_rules:
  - name: sprint_rollover
    trigger:
      type: schedule
      cron: "0 0 * * 1"  # Monday midnight
    conditions:
      - status_not: "Complete"
      - due_date_passed: true
    actions:
      - move_to_list: "{{next_sprint_list}}"
      - update_due_date: "+7 days"
      - add_comment: "Rolled over from previous sprint"
      
  - name: escalation_workflow
    trigger:
      type: task_blocked
      duration: 48_hours
    actions:
      - set_priority: urgent
      - notify: manager
      - add_watcher: "manager_id"
      - add_tag: "escalated"
```

## Views & Layouts

### View Types

```yaml
views:
  list_view:
    type: list
    group_by: status
    sort_by: priority
    columns:
      - name
      - assignees
      - due_date
      - priority
      - time_estimate
      
  board_view:
    type: board
    group_by: status
    card_fields:
      - assignees
      - due_date
      - tags
      - subtasks_count
      
  calendar_view:
    type: calendar
    date_field: due_date
    color_by: priority
    
  timeline_view:
    type: timeline
    start_field: start_date
    end_field: due_date
    dependencies: true
    
  workload_view:
    type: workload
    capacity_field: time_estimate
    group_by: assignee
```

### Dashboard Widgets

```yaml
dashboard:
  widgets:
    - type: sprint_burndown
      list_id: "current_sprint"
      
    - type: workload
      space_id: "engineering"
      period: this_week
      
    - type: task_status
      filter:
        assignee: me
        
    - type: time_tracked
      group_by: project
      period: this_month
      
    - type: goals_progress
      folder_id: "q1_goals"
```

## Time Tracking

### Time Entry Configuration

```yaml
time_tracking:
  settings:
    billable_default: true
    rounding: 15_minutes
    require_description: false
    
  entry:
    task_id: "task_123"
    start: "2024-01-15T09:00:00Z"
    end: "2024-01-15T11:30:00Z"
    duration: 9000000  # 2.5 hours in ms
    billable: true
    description: "Development work"
    
  reports:
    - type: user_summary
      period: this_week
      group_by: task
      
    - type: project_summary
      period: this_month
      group_by: user
```

### Time Reports Dashboard

```
TIME TRACKING - THIS WEEK
═══════════════════════════════════════

TOTAL: 32h 45m

BY PROJECT:
Feature Dev   ████████████████ 18h 30m
Bug Fixes     ████████░░░░░░░░ 8h 15m
Meetings      ████░░░░░░░░░░░░ 4h 00m
Admin         ██░░░░░░░░░░░░░░ 2h 00m

BY DAY:
Mon    █████████████████ 7h 30m
Tue    ███████████████░░ 6h 45m
Wed    ██████████████░░░ 6h 15m
Thu    ████████████████░ 7h 00m
Fri    ███████████░░░░░░ 5h 15m

BILLABLE: 28h 00m (85%)
```

## Goals & OKRs

### Goal Structure

```yaml
goals:
  - name: "Q1 Product Goals"
    type: folder
    
    targets:
      - name: "Ship v2.0"
        type: true_false
        due_date: "2024-03-31"
        
      - name: "Reduce bug count"
        type: number
        start: 45
        target: 10
        unit: "open bugs"
        
      - name: "Increase test coverage"
        type: percentage
        start: 65
        target: 85
        
    key_results:
      - task_list: "v2.0_features"
        measure: tasks_completed
```

### Goal Dashboard

```
Q1 GOALS PROGRESS
═══════════════════════════════════════

Ship v2.0
████████████████████ 100% ✓
Completed on March 28

Reduce Bug Count
████████████████░░░░ 78%
Current: 15 | Target: 10

Increase Test Coverage
██████████████░░░░░░ 72%
Current: 79% | Target: 85%

OVERALL Q1: 83% Complete
```

## Templates

### Task Templates

```yaml
task_templates:
  - name: "Bug Report"
    status: "Open"
    priority: high
    tags: ["bug"]
    description: |
      ## Bug Description
      {{description}}
      
      ## Steps to Reproduce
      1. 
      2. 
      3. 
      
      ## Expected Behavior
      
      ## Actual Behavior
      
      ## Environment
      - Browser: 
      - OS: 
      - Version: 
      
    checklists:
      - name: "Bug Fix Workflow"
        items:
          - "Reproduce bug"
          - "Identify root cause"
          - "Implement fix"
          - "Write tests"
          - "Code review"
          - "Deploy"
          
  - name: "Feature Request"
    status: "Backlog"
    custom_fields:
      story_points: null
    checklists:
      - name: "Feature Workflow"
        items:
          - "Requirements defined"
          - "Design approved"
          - "Implementation"
          - "Testing"
          - "Documentation"
```

## Integrations

### Slack Integration

```yaml
slack_integration:
  notifications:
    - trigger: task_created
      channel: "#project-updates"
      include: [name, assignees, due_date]
      
    - trigger: status_changed
      to: "Complete"
      channel: "#wins"
      message: "✅ {{task.name}} completed by {{user.name}}"
      
  commands:
    /clickup:
      - create_task
      - my_tasks
      - log_time
```

### GitHub Integration

```yaml
github_integration:
  branch_naming:
    pattern: "{{task.id}}-{{task.slug}}"
    
  automations:
    - trigger: branch_created
      actions:
        - set_status: "In Progress"
        - add_comment: "Branch created: {{branch.name}}"
        
    - trigger: pr_opened
      actions:
        - set_status: "In Review"
        - link_pr: "{{pr.url}}"
        
    - trigger: pr_merged
      actions:
        - set_status: "Complete"
```

## API Examples

### Task Operations

```javascript
// Create Task
const task = await clickup.tasks.create(listId, {
  name: "Implement user authentication",
  description: "Add OAuth2 support",
  assignees: [userId],
  priority: 2,
  due_date: Date.now() + 7 * 24 * 60 * 60 * 1000,
  time_estimate: 28800000,
  custom_fields: [
    { id: "field_id", value: "5" }
  ]
});

// Update Task
await clickup.tasks.update(taskId, {
  status: "In Progress",
  assignees: { add: [newUserId] }
});

// Add Time Entry
await clickup.timeEntries.create(taskId, {
  start: Date.now() - 3600000,
  duration: 3600000,
  billable: true
});

// Create Checklist
await clickup.checklists.create(taskId, {
  name: "Acceptance Criteria"
});
```

## Best Practices

1. **Hierarchy Design**: Spaces → Folders → Lists
2. **Consistent Statuses**: Standardize across lists
3. **Custom Fields**: Track key metrics
4. **Automations**: Reduce manual work
5. **Time Tracking**: Enable for capacity planning
6. **Templates**: Standardize task creation
7. **Goals**: Align tasks with objectives
8. **Views**: Configure for different needs
