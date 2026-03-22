---
name: notion-automation
description: "Notion database automation - sync, templates, workflows, and cross-platform integrations"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: productivity
tags:
  - notion
  - automation
  - database
  - workflow
  - n8n
department: Operations

models:
  recommended:
    - claude-sonnet-4

mcp:
  server: notion-mcp
  tools:
    - notion_create_page
    - notion_update_database
    - notion_query

capabilities:
  - database_automation
  - template_creation
  - cross_platform_sync
  - workflow_triggers
  - content_management

languages:
  - en
  - zh

related_skills:
  - sheets-automation
  - slack-workflows
  - crm-automation
---

# Notion Automation

Automate Notion databases and workflows with cross-platform integrations, templates, and intelligent triggers. Based on n8n's Notion workflow templates.

## Overview

This skill covers:
- Database automation and triggers
- Template and page creation
- Cross-platform sync (Slack, Calendar, CRM)
- Content management workflows
- Team collaboration automation

---

## Core Workflows

### 1. Form → Notion Database

```yaml
workflow: "Form to Notion"
trigger: typeform_submission OR google_form

steps:
  1. capture_data:
      fields: [name, email, company, message, source]
      
  2. enrich_data:
      clearbit: lookup_by_email
      append: [company_size, industry]
      
  3. create_notion_page:
      database_id: "leads_database"
      properties:
        Name: "{name}"
        Email: "{email}"
        Company: "{company}"
        Status: "New"
        Source: "{source}"
        Created: "{timestamp}"
      content:
        - heading: "Contact Details"
        - text: "{message}"
        - divider
        - heading: "Enriched Data"
        - text: "Industry: {industry}, Size: {company_size}"
        
  4. notify:
      slack:
        channel: "#new-leads"
        message: "New lead: {name} from {company}"
```

### 2. Notion → Email Digest

```yaml
workflow: "Weekly Notion Digest"
schedule: "Monday 9am"

steps:
  1. query_notion:
      database: "Tasks"
      filter:
        - property: "Due Date"
          date: this_week
        - property: "Status"
          not_equals: "Done"
          
  2. group_by_assignee:
      method: aggregate
      
  3. generate_digest:
      for_each: assignee
      template: |
        Hi {assignee},
        
        Here are your tasks for this week:
        
        {for task in tasks}
        • {task.title} - Due: {task.due_date}
        {endfor}
        
        Total: {task_count} tasks
        
  4. send_emails:
      to: each_assignee
      subject: "Your Weekly Task Digest"
```

### 3. Slack → Notion Task

```yaml
workflow: "Slack to Notion Task"
trigger: slack_reaction (✅ emoji)

steps:
  1. capture_message:
      extract: [text, author, channel, timestamp, thread]
      
  2. parse_task:
      ai_extraction:
        title: extract_action_item
        due_date: extract_date_if_mentioned
        priority: infer_from_context
        
  3. create_notion_task:
      database: "Tasks"
      properties:
        Title: "{extracted_title}"
        Status: "To Do"
        Source: "Slack - #{channel}"
        Assignee: "{slack_user_to_notion_user}"
        Due Date: "{due_date}"
        Priority: "{priority}"
      content:
        - quote: "{original_message}"
        - text: "Created from Slack message"
        - link: "{slack_permalink}"
        
  4. thread_reply:
      slack:
        thread_ts: "{timestamp}"
        message: "✅ Task created in Notion: {notion_url}"
```

### 4. Calendar Sync

```yaml
workflow: "Google Calendar ↔ Notion"
trigger: bidirectional

google_to_notion:
  trigger: calendar_event_created
  action:
    - create_notion_page:
        database: "Meetings"
        properties:
          Title: "{event.title}"
          Date: "{event.start}"
          Attendees: "{event.attendees}"
          Location: "{event.location}"
          Calendar Link: "{event.link}"

notion_to_google:
  trigger: notion_page_created
  filter: database == "Meetings"
  action:
    - create_calendar_event:
        title: "{page.Title}"
        start: "{page.Date}"
        description: "{page.Notes}"
        attendees: "{page.Attendees}"
```

### 5. Content Pipeline

```yaml
workflow: "Content Publishing Pipeline"

database_structure:
  properties:
    - Title: title
    - Status: select [Idea, Writing, Review, Published]
    - Author: person
    - Due Date: date
    - Platform: multi_select [Blog, LinkedIn, Twitter]
    - Content: rich_text
    
automations:
  status_changed_to_review:
    - notify_slack: "#content-review"
    - assign_reviewer: round_robin
    - set_due_date: 3_days_from_now
    
  status_changed_to_published:
    - post_to_platforms: based_on_Platform_property
    - update_analytics_tracker: add_row
    - archive_after: 7_days
```

---

## Database Templates

### Project Management

```yaml
project_database:
  name: "Projects"
  properties:
    - Name: title
    - Status: select
        options: [Planning, In Progress, Review, Complete]
    - Priority: select
        options: [P0, P1, P2, P3]
    - Owner: person
    - Team: multi_select
    - Start Date: date
    - Due Date: date
    - Progress: number (percent)
    - Related Tasks: relation → Tasks
    
  views:
    - Board: group_by Status
    - Timeline: gantt chart
    - Calendar: by Due Date
    - Table: all properties
    
  automations:
    - when: all_tasks_complete
      then: set_status "Complete"
    - when: due_date_approaching (3 days)
      then: slack_reminder to Owner
```

### CRM Database

```yaml
crm_database:
  name: "Contacts"
  properties:
    - Name: title
    - Email: email
    - Company: text
    - Stage: select
        options: [Lead, Qualified, Proposal, Negotiation, Closed]
    - Value: number (currency)
    - Last Contact: date
    - Next Action: text
    - Owner: person
    - Related Deals: relation → Deals
    
  automations:
    - when: stage_changed
      then: log_activity + notify_owner
    - when: no_contact_14_days
      then: slack_alert "Follow up needed"
```

### Content Calendar

```yaml
content_calendar:
  name: "Content"
  properties:
    - Title: title
    - Type: select [Blog, Video, Social, Newsletter]
    - Status: select [Idea, Draft, Review, Scheduled, Published]
    - Publish Date: date
    - Author: person
    - Platform: multi_select
    - SEO Keywords: multi_select
    - Engagement: number
    
  views:
    - Calendar: by Publish Date
    - Kanban: by Status
    - By Platform: grouped table
```

---

## API Patterns

### Query Database

```javascript
// n8n Notion Query
{
  "database_id": "abc123",
  "filter": {
    "and": [
      {
        "property": "Status",
        "select": {
          "equals": "In Progress"
        }
      },
      {
        "property": "Due Date",
        "date": {
          "on_or_before": "{{$today}}"
        }
      }
    ]
  },
  "sorts": [
    {
      "property": "Priority",
      "direction": "ascending"
    }
  ]
}
```

### Create Page

```javascript
// n8n Notion Create Page
{
  "parent": { "database_id": "abc123" },
  "properties": {
    "Name": {
      "title": [{ "text": { "content": "{{$json.title}}" }}]
    },
    "Status": {
      "select": { "name": "New" }
    },
    "Tags": {
      "multi_select": [
        { "name": "{{$json.tag1}}" },
        { "name": "{{$json.tag2}}" }
      ]
    }
  },
  "children": [
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": {
        "rich_text": [{ "text": { "content": "Overview" }}]
      }
    },
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{ "text": { "content": "{{$json.content}}" }}]
      }
    }
  ]
}
```

---

## Integration Recipes

### Notion + Slack + Calendar

```yaml
meeting_workflow:
  trigger: notion_page_created
  database: "Meetings"
  
  actions:
    1. create_calendar_event:
        google_calendar:
          title: "{Title}"
          date: "{Date}"
          
    2. create_slack_channel:
        if: "{Type}" == "Project Kickoff"
        name: "proj-{project_name}"
        
    3. send_invites:
        to: "{Attendees}"
        include: [calendar_link, notion_link, slack_channel]
        
    4. create_meeting_doc:
        notion:
          template: "Meeting Notes Template"
          link_to: original_page
```

### Notion + GitHub

```yaml
github_sync:
  trigger: github_issue_created
  
  actions:
    - create_notion_page:
        database: "Engineering Tasks"
        properties:
          Title: "{issue.title}"
          GitHub: "{issue.url}"
          Labels: "{issue.labels}"
          Assignee: map_github_to_notion("{issue.assignee}")
          
  reverse_sync:
    trigger: notion_status_changed
    to: "Done"
    action: close_github_issue
```

---

## Output Example

**Request**: "Set up Notion automation for a content team"

**Output**:

```markdown
# Content Team Notion Setup

## Database: Content Calendar

### Properties
| Property | Type | Options |
|----------|------|---------|
| Title | Title | - |
| Status | Select | Idea, Writing, Editing, Ready, Published |
| Author | Person | - |
| Publish Date | Date | - |
| Platform | Multi-select | Blog, LinkedIn, Twitter, Newsletter |
| Type | Select | Article, Video, Infographic, Thread |

### Automations

**1. New Content Idea → Slack**
```yaml
trigger: page_created, Status = "Idea"
action: post_to_slack("#content-ideas")
message: "💡 New content idea: {Title} by {Author}"
```

**2. Ready for Review → Assign Editor**
```yaml
trigger: status_changed_to "Editing"
action: 
  - assign_editor (round_robin)
  - set_due_date (+3 days)
  - slack_dm_editor
```

**3. Published → Update Tracker**
```yaml
trigger: status_changed_to "Published"
action:
  - add_to_analytics_sheet
  - post_celebration_slack
  - schedule_engagement_check (+7 days)
```

### Views
1. **Calendar** - See publishing schedule
2. **Kanban** - Track status
3. **By Author** - Individual workload
4. **This Week** - Filtered view

### Templates
- Blog Post Template
- Social Thread Template
- Newsletter Template
```

---

*Notion Automation Skill - Part of Claude Office Skills*
