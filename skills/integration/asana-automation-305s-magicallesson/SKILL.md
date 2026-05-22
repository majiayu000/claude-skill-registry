---
name: Asana Automation
description: Automate Asana project management workflows, task tracking, team collaboration, and reporting
version: 1.0.0
author: Claude Office Skills
category: project-management
tags:
  - asana
  - tasks
  - project-management
  - collaboration
  - automation
department: operations
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: project-mcp
  tools:
    - asana_create_task
    - asana_update_task
    - asana_search
    - asana_sections
capabilities:
  - Task creation and management
  - Project automation
  - Team workload tracking
  - Custom field workflows
input:
  - Task details
  - Project configurations
  - Workflow rules
  - Team assignments
output:
  - Created/updated tasks
  - Project reports
  - Workload views
  - Timeline updates
languages:
  - en
related_skills:
  - jira-automation
  - monday-automation
  - notion-automation
---

# Asana Automation

Comprehensive skill for automating Asana project management and team collaboration.

## Core Workflows

### 1. Task Management Pipeline

```
TASK LIFECYCLE:
┌─────────────────┐
│   New Request   │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Triage &      │
│   Prioritize    │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Assign &      │
│   Schedule      │
└────────┬────────┘
         ▼
┌─────────────────┐
│   In Progress   │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Review        │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Complete      │
└─────────────────┘
```

### 2. Automation Rules

```yaml
automation_rules:
  - name: auto_assign_by_section
    trigger:
      type: task_moved_to_section
      section: "Design"
    action:
      assign_to: "design_team"
      add_followers: ["design_lead"]
      set_custom_field:
        Department: "Design"

  - name: due_date_reminder
    trigger:
      type: due_date_approaching
      days_before: 2
    action:
      add_comment: "@{{assignee}} Reminder: This task is due in 2 days"
      add_to_project: "Due This Week"

  - name: completion_notification
    trigger:
      type: task_completed
    action:
      notify_followers: true
      move_to_section: "Done"
      add_comment: "✅ Completed on {{completion_date}}"

  - name: subtask_creation
    trigger:
      type: task_added_to_project
      project: "New Features"
    action:
      add_subtasks:
        - "Requirements gathering"
        - "Design mockups"
        - "Development"
        - "Testing"
        - "Documentation"
```

## Project Templates

### Feature Launch Template

```yaml
project_template:
  name: "Feature Launch - {{feature_name}}"
  team: "Product"
  
  sections:
    - name: "Planning"
      tasks:
        - name: "Define requirements"
          assignee: "product_manager"
          subtasks:
            - "User stories"
            - "Acceptance criteria"
            - "Success metrics"
        - name: "Technical spec"
          assignee: "tech_lead"
          
    - name: "Design"
      tasks:
        - name: "UX research"
          duration: 5
        - name: "Wireframes"
          duration: 3
        - name: "Visual design"
          duration: 5
          
    - name: "Development"
      tasks:
        - name: "Backend implementation"
          duration: 10
        - name: "Frontend implementation"
          duration: 10
        - name: "API integration"
          duration: 5
          
    - name: "Testing"
      tasks:
        - name: "QA testing"
          duration: 5
        - name: "Bug fixes"
          duration: 3
        - name: "UAT"
          duration: 3
          
    - name: "Launch"
      tasks:
        - name: "Documentation"
          duration: 3
        - name: "Marketing materials"
          duration: 5
        - name: "Release notes"
          duration: 1
        - name: "Go live"
          milestone: true
```

### Sprint Template

```yaml
sprint_template:
  name: "Sprint {{number}} - {{dates}}"
  
  sections:
    - "Backlog"
    - "To Do"
    - "In Progress"
    - "Review"
    - "Done"
    
  custom_fields:
    - name: "Story Points"
      type: number
    - name: "Priority"
      type: dropdown
      options: ["P0", "P1", "P2", "P3"]
    - name: "Type"
      type: dropdown
      options: ["Feature", "Bug", "Tech Debt", "Research"]
```

## Custom Fields

### Field Configurations

```yaml
custom_fields:
  - name: Priority
    type: dropdown
    options:
      - name: "🔴 Urgent"
        color: red
      - name: "🟠 High"
        color: orange
      - name: "🟡 Medium"
        color: yellow
      - name: "🟢 Low"
        color: green
    
  - name: Status
    type: dropdown
    options:
      - "Not Started"
      - "In Progress"
      - "Blocked"
      - "In Review"
      - "Complete"
    
  - name: Estimated Hours
    type: number
    precision: 1
    
  - name: Department
    type: dropdown
    options:
      - "Engineering"
      - "Design"
      - "Marketing"
      - "Sales"
      - "Operations"
    
  - name: Due Week
    type: date
    format: week
```

## Workload Management

### Team Capacity

```
TEAM WORKLOAD - THIS WEEK
═══════════════════════════════════════

Sarah (Designer)
██████████████████░░ 85% | 8 tasks
Capacity: 40 hrs | Assigned: 34 hrs

Mike (Engineer)
████████████████░░░░ 78% | 12 tasks
Capacity: 40 hrs | Assigned: 31 hrs

Lisa (PM)
██████████████████████ 110% ⚠️ | 15 tasks
Capacity: 40 hrs | Assigned: 44 hrs

REBALANCING SUGGESTIONS:
• Move "API docs" from Lisa to Mike
• Extend deadline for "Research report"
• Add resources to "Launch prep"
```

### Timeline View

```yaml
timeline_config:
  view: gantt
  date_range: "this_quarter"
  
  grouping: 
    primary: project
    secondary: assignee
    
  milestones:
    show: true
    style: diamond
    
  dependencies:
    show: true
    type: finish_to_start
    
  color_by: custom_field.priority
```

## Forms & Intake

### Request Form

```yaml
intake_form:
  name: "Work Request"
  project: "Incoming Requests"
  
  fields:
    - name: "Request Title"
      type: single_line
      required: true
      
    - name: "Description"
      type: multi_line
      required: true
      
    - name: "Request Type"
      type: dropdown
      options:
        - "New Feature"
        - "Bug Fix"
        - "Content Update"
        - "Design Request"
      required: true
      
    - name: "Priority"
      type: dropdown
      options: ["Low", "Medium", "High", "Urgent"]
      required: true
      
    - name: "Due Date"
      type: date
      required: false
      
    - name: "Attachments"
      type: attachment
      
  routing:
    - condition:
        field: "Request Type"
        equals: "Design Request"
      action:
        assign_to: "design_team"
        add_to_project: "Design Requests"
```

## Reporting

### Portfolio Dashboard

```
PROJECT PORTFOLIO STATUS
═══════════════════════════════════════

Active Projects: 12
On Track: 8 (67%)
At Risk: 3 (25%)
Off Track: 1 (8%)

BY STATUS:
┌────────────────────┬────────┬─────────┐
│ Project            │ Status │ % Done  │
├────────────────────┼────────┼─────────┤
│ Website Redesign   │ 🟢     │ 78%     │
│ Mobile App v2      │ 🟡     │ 45%     │
│ CRM Integration    │ 🟢     │ 92%     │
│ Q2 Marketing       │ 🔴     │ 23%     │
│ Security Audit     │ 🟢     │ 65%     │
└────────────────────┴────────┴─────────┘

UPCOMING MILESTONES:
• Jan 25: Website Beta Launch
• Jan 30: Mobile App QA Complete
• Feb 5: CRM Go-Live
```

### Team Metrics

```yaml
reports:
  - name: "Weekly Team Report"
    metrics:
      - tasks_completed
      - tasks_created
      - overdue_tasks
      - completion_rate
    group_by: assignee
    period: last_7_days
    
  - name: "Project Progress"
    metrics:
      - total_tasks
      - completed_percentage
      - days_remaining
      - blockers_count
    group_by: project
    
  - name: "Burnup Chart"
    type: chart
    x_axis: date
    y_axis:
      - total_scope
      - completed_tasks
    period: current_sprint
```

## Integration Workflows

### Slack Integration

```yaml
slack_integration:
  notifications:
    - trigger: task_assigned_to_me
      channel: dm
      message: "📋 New task assigned: {{task.name}}"
      
    - trigger: task_completed
      channel: "#team-updates"
      message: "✅ {{user}} completed: {{task.name}}"
      
    - trigger: comment_added
      channel: dm
      message: "💬 New comment on {{task.name}}"
      
  commands:
    /asana:
      - create_task
      - list_my_tasks
      - mark_complete
```

### GitHub Integration

```yaml
github_integration:
  sync_rules:
    - github_event: issue_opened
      asana_action:
        create_task:
          project: "GitHub Issues"
          name: "{{issue.title}}"
          description: "{{issue.body}}"
          custom_fields:
            GitHub_Issue: "{{issue.number}}"
            
    - github_event: pr_merged
      asana_action:
        complete_task:
          match_field: "GitHub_PR"
          value: "{{pr.number}}"
```

## Best Practices

1. **Clear Task Names**: Use action verbs, be specific
2. **Single Assignee**: One person accountable per task
3. **Due Dates**: Always set realistic deadlines
4. **Subtasks**: Break complex work into smaller pieces
5. **Custom Fields**: Use consistently across projects
6. **Templates**: Create reusable project structures
7. **Regular Reviews**: Weekly project check-ins
8. **Archive Completed**: Keep workspace organized
