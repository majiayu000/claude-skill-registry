---
name: Monday.com Automation
description: Automate Monday.com workflows, board management, team collaboration, and cross-board integrations
version: 1.0.0
author: Claude Office Skills
category: project-management
tags:
  - monday
  - workflow
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
    - monday_create_item
    - monday_update_item
    - monday_query
    - monday_webhooks
capabilities:
  - Board and item management
  - Workflow automation
  - Dashboard creation
  - Cross-board sync
input:
  - Item details
  - Board configurations
  - Automation recipes
  - Integration settings
output:
  - Created/updated items
  - Board views
  - Dashboard reports
  - Automation logs
languages:
  - en
related_skills:
  - asana-automation
  - jira-automation
  - notion-automation
---

# Monday.com Automation

Comprehensive skill for automating Monday.com work management and team workflows.

## Core Concepts

### Board Structure

```
BOARD ANATOMY:
┌─────────────────────────────────────────────────┐
│ 📋 Project Board                                │
├─────────────────────────────────────────────────┤
│ Group: Sprint 1                                 │
│ ┌─────────┬────────┬────────┬────────┬────────┐│
│ │ Item    │ Status │ Person │ Date   │ Budget ││
│ ├─────────┼────────┼────────┼────────┼────────┤│
│ │ Task 1  │ 🟢 Done│ Sarah  │ Jan 15 │ $500   ││
│ │ Task 2  │ 🟡 WIP │ Mike   │ Jan 20 │ $800   ││
│ │ Task 3  │ 🔴 Stuck│ Lisa  │ Jan 18 │ $300   ││
│ └─────────┴────────┴────────┴────────┴────────┘│
│                                                 │
│ Group: Sprint 2                                 │
│ ┌─────────┬────────┬────────┬────────┬────────┐│
│ │ Task 4  │ ⚪ New │        │ Jan 25 │ $600   ││
│ │ Task 5  │ ⚪ New │        │ Jan 28 │ $400   ││
│ └─────────┴────────┴────────┴────────┴────────┘│
└─────────────────────────────────────────────────┘
```

### Column Types

```yaml
column_types:
  status:
    labels:
      - label: "Done"
        color: green
      - label: "Working on it"
        color: yellow
      - label: "Stuck"
        color: red
      - label: "Not Started"
        color: grey
  
  person:
    allow_multiple: true
    
  date:
    include_time: false
    
  timeline:
    show_weeks: true
    
  numbers:
    unit: "$"
    
  text:
    multiline: false
    
  dropdown:
    options: ["Option A", "Option B", "Option C"]
    
  formula:
    expression: "{Numbers} * 1.1"
```

## Automation Recipes

### Built-in Automations

```yaml
automations:
  - name: "Status Change Notification"
    trigger:
      type: status_change
      column: "Status"
      to: "Done"
    action:
      type: notify
      target: item_subscribers
      message: "✅ {{item.name}} has been completed!"

  - name: "Due Date Assignment"
    trigger:
      type: date_arrived
      column: "Due Date"
    action:
      type: change_status
      column: "Status"
      to: "Overdue"

  - name: "Auto-Assign New Items"
    trigger:
      type: item_created
      group: "Incoming"
    action:
      type: assign_person
      column: "Owner"
      value: "team_lead"

  - name: "Move When Status Changes"
    trigger:
      type: status_change
      column: "Status"
      to: "Done"
    action:
      type: move_to_group
      target: "Completed"

  - name: "Create Dependent Task"
    trigger:
      type: status_change
      column: "Status"
      to: "Ready for Review"
    action:
      type: create_item
      board: "Review Board"
      values:
        Name: "Review: {{item.name}}"
        Link: "{{item.link}}"
```

### Custom Automations

```yaml
custom_recipes:
  - name: "SLA Warning"
    trigger:
      type: every_time_period
      interval: "1 hour"
    condition:
      - column: "Status"
        not_equals: "Done"
      - column: "Due Date"
        within: "24 hours"
    action:
      - type: change_status
        column: "Priority"
        to: "Urgent"
      - type: notify
        channel: "#alerts"
        message: "⚠️ SLA at risk: {{item.name}}"

  - name: "Budget Rollup"
    trigger:
      type: column_change
      column: "Budget"
    action:
      type: update_parent
      column: "Total Budget"
      formula: "SUM(subitems.Budget)"
```

## Board Templates

### CRM Board

```yaml
crm_board:
  name: "Sales CRM"
  
  groups:
    - "New Leads"
    - "Contacted"
    - "Qualified"
    - "Proposal"
    - "Negotiation"
    - "Won"
    - "Lost"
    
  columns:
    - name: "Company"
      type: text
    - name: "Contact"
      type: text
    - name: "Email"
      type: email
    - name: "Phone"
      type: phone
    - name: "Deal Value"
      type: numbers
      unit: "$"
    - name: "Stage"
      type: status
    - name: "Owner"
      type: person
    - name: "Next Action"
      type: date
    - name: "Lead Source"
      type: dropdown
    - name: "Notes"
      type: long_text
```

### Project Tracker

```yaml
project_board:
  name: "Project Tracker"
  
  groups:
    - "Backlog"
    - "This Sprint"
    - "In Progress"
    - "In Review"
    - "Done"
    
  columns:
    - name: "Task"
      type: text
    - name: "Status"
      type: status
    - name: "Assignee"
      type: person
    - name: "Priority"
      type: status
      labels: ["Critical", "High", "Medium", "Low"]
    - name: "Timeline"
      type: timeline
    - name: "Estimated Hours"
      type: numbers
    - name: "Actual Hours"
      type: numbers
    - name: "Tags"
      type: tags
    - name: "Dependencies"
      type: dependency
```

## Views & Dashboards

### View Types

```yaml
views:
  main_table:
    type: table
    default: true
    columns: all
    
  kanban:
    type: kanban
    group_by: "Status"
    card_fields:
      - "Assignee"
      - "Due Date"
      - "Priority"
    
  timeline:
    type: timeline
    date_column: "Timeline"
    color_by: "Status"
    
  calendar:
    type: calendar
    date_column: "Due Date"
    color_by: "Priority"
    
  chart:
    type: chart
    chart_type: bar
    x_axis: "Status"
    y_axis: count
    
  workload:
    type: workload
    person_column: "Assignee"
    effort_column: "Estimated Hours"
```

### Dashboard Widgets

```yaml
dashboard:
  name: "Project Overview"
  
  widgets:
    - type: numbers
      title: "Total Tasks"
      board: "Project Board"
      column: count
      
    - type: chart
      title: "Tasks by Status"
      board: "Project Board"
      chart_type: pie
      group_by: "Status"
      
    - type: battery
      title: "Sprint Progress"
      board: "Project Board"
      group: "This Sprint"
      
    - type: timeline
      title: "Project Timeline"
      boards: ["Project Board"]
      
    - type: workload
      title: "Team Workload"
      board: "Project Board"
      person_column: "Assignee"
```

## Integration Workflows

### Slack Integration

```yaml
slack_automations:
  - trigger: status_change_to_done
    action:
      post_to_channel: "#wins"
      message: "🎉 {{person}} completed {{item}}!"
      
  - trigger: item_stuck
    action:
      post_to_channel: "#blockers"
      message: "🚧 {{item}} is stuck. Owner: {{person}}"
      
  - trigger: new_item_created
    action:
      post_to_channel: "#tasks"
      message: "📋 New task: {{item}} ({{board}})"
```

### Email Integration

```yaml
email_automations:
  - trigger: due_date_approaching
    days_before: 3
    action:
      send_email:
        to: "{{item.person.email}}"
        subject: "Task Due Soon: {{item.name}}"
        body: |
          Hi {{item.person.name}},
          
          Your task "{{item.name}}" is due on {{item.due_date}}.
          
          Please update the status or reach out if you need help.
```

### API Workflows

```javascript
// Monday.com GraphQL API Examples

// Create Item
const createItem = `
  mutation {
    create_item (
      board_id: 123456789,
      group_id: "new_group",
      item_name: "New Task",
      column_values: "{\"status\":\"Working on it\",\"person\":\"12345\"}"
    ) {
      id
    }
  }
`;

// Update Status
const updateStatus = `
  mutation {
    change_column_value (
      board_id: 123456789,
      item_id: 987654321,
      column_id: "status",
      value: "{\"label\":\"Done\"}"
    ) {
      id
    }
  }
`;

// Query Items
const queryItems = `
  query {
    boards (ids: 123456789) {
      items_page (limit: 50) {
        items {
          id
          name
          column_values {
            id
            value
          }
        }
      }
    }
  }
`;
```

## Best Practices

1. **Group Organization**: Use groups for workflow stages
2. **Consistent Columns**: Standardize across boards
3. **Automation Rules**: Reduce manual updates
4. **Mirror Columns**: Connect related boards
5. **Dashboard Views**: Provide executive visibility
6. **Templates**: Reuse board structures
7. **Subitems**: Break down complex tasks
8. **Dependencies**: Show task relationships
