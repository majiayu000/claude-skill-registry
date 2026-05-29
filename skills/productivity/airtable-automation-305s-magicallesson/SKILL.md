---
name: airtable-automation
description: "Airtable database automation - views, automations, integrations, and workflow triggers"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: productivity
tags:
  - airtable
  - automation
  - database
  - workflow
  - n8n
department: Operations

models:
  recommended:
    - claude-sonnet-4

mcp:
  server: airtable-mcp
  tools:
    - airtable_create_record
    - airtable_update_record
    - airtable_query

capabilities:
  - database_automation
  - view_creation
  - integration_workflows
  - formula_design
  - reporting

languages:
  - en
  - zh

related_skills:
  - notion-automation
  - sheets-automation
  - crm-automation
---

# Airtable Automation

Automate Airtable bases with views, automations, integrations, and cross-platform workflows. Based on n8n's Airtable integration templates.

## Overview

This skill covers:
- Database design and views
- Built-in automations
- n8n integration workflows
- Formula and rollup design
- Reporting and dashboards

---

## Database Design

### Base Structure Template

```yaml
base: "Project Management"

tables:
  Projects:
    fields:
      - Name: single_line_text (primary)
      - Status: single_select [Planning, Active, On Hold, Complete]
      - Priority: single_select [P0, P1, P2, P3]
      - Owner: collaborator
      - Start Date: date
      - Due Date: date
      - Budget: currency
      - Tasks: link_to_records (Tasks)
      - Progress: rollup (Tasks.Status, COUNTIF(Done)/COUNT)
      - Days Remaining: formula (DATETIME_DIFF(Due Date, TODAY(), 'days'))
      
  Tasks:
    fields:
      - Task Name: single_line_text (primary)
      - Project: link_to_records (Projects)
      - Status: single_select [To Do, In Progress, Review, Done]
      - Assignee: collaborator
      - Due Date: date
      - Hours Estimated: number
      - Hours Actual: number
      - Attachments: attachment
      
  Team:
    fields:
      - Name: single_line_text (primary)
      - Email: email
      - Role: single_select [PM, Developer, Designer, QA]
      - Current Projects: link_to_records (Projects)
      - Capacity: number (hours/week)
      - Utilization: rollup (calculate from Tasks)
```

### Views Configuration

```yaml
views:
  Projects:
    - Grid: All Projects
        fields: [Name, Status, Owner, Due Date, Progress]
        sort: Due Date (ascending)
        
    - Kanban: By Status
        group_by: Status
        card_fields: [Name, Owner, Due Date]
        
    - Calendar: Timeline
        date_field: Due Date
        
    - Gallery: Project Cards
        cover: Attachments
        
  Tasks:
    - Grid: My Tasks
        filter: Assignee = {Current User}
        sort: Due Date
        
    - Kanban: Sprint Board
        group_by: Status
        
    - Calendar: Task Calendar
        date_field: Due Date
```

---

## Automations

### Built-in Airtable Automations

```yaml
automation_1:
  name: "New Task Notification"
  trigger:
    when: record_created
    table: Tasks
  actions:
    - send_slack:
        channel: "#project-updates"
        message: |
          📋 New task created!
          Task: {Task Name}
          Project: {Project}
          Assignee: {Assignee}
          Due: {Due Date}

automation_2:
  name: "Overdue Task Alert"
  trigger:
    when: record_matches_conditions
    table: Tasks
    conditions:
      - Status: not "Done"
      - Due Date: before today
  actions:
    - send_email:
        to: "{Assignee.email}"
        subject: "⚠️ Overdue Task: {Task Name}"
        body: "Your task '{Task Name}' was due on {Due Date}."
    - update_record:
        field: Status
        value: "Overdue"

automation_3:
  name: "Project Complete"
  trigger:
    when: record_updated
    table: Projects
    field: Progress
    condition: equals 100%
  actions:
    - update_record:
        field: Status
        value: "Complete"
    - send_slack:
        channel: "#wins"
        message: "🎉 Project '{Name}' completed!"
```

### n8n Integration Workflows

```yaml
workflow: "Form to Airtable to CRM"

trigger: typeform_submission

steps:
  1. create_airtable_record:
      base: "Leads"
      table: "Contacts"
      fields:
        Name: "{form.name}"
        Email: "{form.email}"
        Company: "{form.company}"
        Source: "Website Form"
        Created: "{timestamp}"
        
  2. enrich_data:
      clearbit: lookup_email
      update_record:
        Company Size: "{clearbit.company_size}"
        Industry: "{clearbit.industry}"
        
  3. sync_to_hubspot:
      create_contact:
        email: "{email}"
        properties: from_airtable
        
  4. notify_sales:
      slack:
        channel: "#new-leads"
        message: "New lead: {Name} from {Company}"
```

---

## Formula Reference

### Common Formulas

```yaml
formulas:
  days_until_due:
    formula: "DATETIME_DIFF({Due Date}, TODAY(), 'days')"
    output: number
    
  is_overdue:
    formula: "IF(AND({Status}!='Done', {Due Date}<TODAY()), 'Yes', 'No')"
    output: text
    
  full_name:
    formula: "CONCATENATE({First Name}, ' ', {Last Name})"
    output: text
    
  progress_bar:
    formula: |
      REPT('▓', ROUND({Progress}/10, 0)) & 
      REPT('░', 10-ROUND({Progress}/10, 0)) & 
      ' ' & ROUND({Progress}, 0) & '%'
    output: text (visual progress)
    
  status_emoji:
    formula: |
      SWITCH({Status},
        'To Do', '⬜',
        'In Progress', '🔵',
        'Review', '🟡',
        'Done', '✅',
        '❓'
      )
    output: text
    
  workdays_remaining:
    formula: "WORKDAY_DIFF(TODAY(), {Due Date})"
    output: number
    
  quarter:
    formula: |
      'Q' & CEILING(MONTH({Date})/3) & ' ' & YEAR({Date})
    output: text
```

### Rollup Examples

```yaml
rollups:
  task_count:
    linked_field: Tasks
    aggregation: COUNT(values)
    
  total_hours:
    linked_field: Tasks
    rollup_field: Hours Estimated
    aggregation: SUM(values)
    
  completion_rate:
    linked_field: Tasks
    rollup_field: Status
    aggregation: |
      COUNTALL(IF(values='Done', 1)) / COUNT(values) * 100
      
  average_rating:
    linked_field: Reviews
    rollup_field: Rating
    aggregation: AVERAGE(values)
```

---

## Integration Patterns

### Airtable + Slack

```yaml
slack_integration:
  new_record_notification:
    trigger: record_created
    action: post_to_channel
    template: |
      *New {Table} Record*
      {Field1}: {value1}
      {Field2}: {value2}
      <{record_url}|View in Airtable>
      
  daily_digest:
    schedule: "9am weekdays"
    query: records_due_today
    action: post_summary
    
  slash_command:
    command: /airtable-add
    action: create_record_from_slack
```

### Airtable + Calendar

```yaml
calendar_sync:
  airtable_to_google:
    trigger: record_with_date_created
    action: create_calendar_event
    mapping:
      title: "{Name}"
      start: "{Date}"
      description: "{Notes}"
      
  google_to_airtable:
    trigger: calendar_event_created
    action: create_airtable_record
    mapping:
      Name: "{event.title}"
      Date: "{event.start}"
      Type: "Meeting"
```

### Airtable + Zapier/n8n

```yaml
multi_step_workflow:
  name: "Lead Processing Pipeline"
  
  trigger:
    platform: airtable
    event: new_record
    table: Raw Leads
    
  steps:
    - enrich:
        service: clearbit
        input: email
        output: company_data
        
    - score:
        service: ai_scoring
        criteria: [company_size, industry, title]
        output: lead_score
        
    - route:
        condition: lead_score
        high: assign_to_sales
        medium: add_to_nurture
        low: mark_as_cold
        
    - update_airtable:
        table: Qualified Leads
        fields: [enriched_data, score, assignment]
        
    - notify:
        if: high_score
        slack: dm_sales_rep
```

---

## Reporting Templates

### Weekly Status Report

```yaml
report_automation:
  schedule: "Friday 5pm"
  
  queries:
    completed_this_week:
      table: Tasks
      filter: 
        - Status: Done
        - Completed Date: this_week
        
    in_progress:
      table: Tasks
      filter:
        - Status: In Progress
        
    overdue:
      table: Tasks
      filter:
        - Status: not Done
        - Due Date: before today
        
  output:
    format: markdown
    destination: [slack, email]
    template: |
      # Weekly Status Report - {week}
      
      ## Completed ({completed_count})
      {completed_list}
      
      ## In Progress ({in_progress_count})
      {in_progress_list}
      
      ## Overdue ({overdue_count}) ⚠️
      {overdue_list}
      
      ## Metrics
      - Completion rate: {rate}%
      - On-time delivery: {on_time}%
```

### Dashboard View

```yaml
dashboard:
  name: "Project Dashboard"
  
  widgets:
    - summary_bar:
        metrics:
          - Total Projects: COUNT(Projects)
          - Active: COUNT(Status='Active')
          - At Risk: COUNT(Days Remaining < 7)
          
    - progress_chart:
        type: bar
        data: Projects grouped by Status
        
    - upcoming_deadlines:
        type: list
        query: Projects where Due Date in next 14 days
        sort: Due Date ascending
        limit: 10
        
    - team_utilization:
        type: horizontal_bar
        data: Team members by task count
```

---

## Output Example

**Request**: "Design an Airtable base for content marketing"

**Output**:

```markdown
# Content Marketing Base

## Tables

### 1. Content Calendar
| Field | Type | Purpose |
|-------|------|---------|
| Title | Text | Content title |
| Status | Select | Idea → Draft → Review → Published |
| Type | Select | Blog, Video, Social, Email |
| Author | Collaborator | Assigned writer |
| Publish Date | Date | Target publish date |
| Platform | Multi-select | Blog, LinkedIn, Twitter |
| Keywords | Multi-select | SEO keywords |
| Performance | Link | → Analytics |

### 2. Analytics
| Field | Type | Purpose |
|-------|------|---------|
| Content | Link | → Content Calendar |
| Views | Number | Page views |
| Engagement | Number | Likes + comments |
| Conversions | Number | CTAs clicked |
| Date | Date | Measurement date |

## Automations

**1. New Content Idea**
```
Trigger: Record created
Action: Slack to #content-ideas
```

**2. Ready for Review**
```
Trigger: Status → Review
Action: Email editor + set due date
```

**3. Published**
```
Trigger: Status → Published
Action: 
- Post to social scheduler
- Add analytics tracking row
- Celebrate in Slack 🎉
```

## Views
- 📅 Calendar View (by Publish Date)
- 📊 Kanban (by Status)
- 👤 My Content (filtered by Author)
- 📈 Performance Dashboard
```

---

*Airtable Automation Skill - Part of Claude Office Skills*
