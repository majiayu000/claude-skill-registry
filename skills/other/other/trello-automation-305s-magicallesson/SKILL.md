---
name: Trello Automation
description: Automate Trello board management, card workflows, power-ups, and team collaboration
version: 1.0.0
author: Claude Office Skills
category: project-management
tags:
  - trello
  - kanban
  - project-management
  - cards
  - automation
department: operations
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: project-mcp
  tools:
    - trello_card
    - trello_list
    - trello_board
    - trello_automation
capabilities:
  - Card management
  - Board automation (Butler)
  - Workflow templates
  - Cross-board sync
input:
  - Card details
  - Board configurations
  - Automation rules
  - Labels and members
output:
  - Created/updated cards
  - Board reports
  - Activity logs
  - Automation results
languages:
  - en
related_skills:
  - asana-automation
  - jira-automation
  - notion-automation
---

# Trello Automation

Comprehensive skill for automating Trello board management and kanban workflows.

## Core Concepts

### Board Structure

```
TRELLO BOARD ANATOMY:
┌─────────────────────────────────────────────────────────┐
│ 📋 Project Board                                        │
├───────────┬───────────┬───────────┬───────────┬────────┤
│  Backlog  │   To Do   │   Doing   │  Review   │  Done  │
├───────────┼───────────┼───────────┼───────────┼────────┤
│ ┌───────┐ │ ┌───────┐ │ ┌───────┐ │ ┌───────┐ │        │
│ │Card 1 │ │ │Card 3 │ │ │Card 5 │ │ │Card 7 │ │        │
│ │Labels │ │ │@Mike  │ │ │@Sarah │ │ │@Lisa  │ │        │
│ │Due    │ │ │Due:3d │ │ │       │ │ │       │ │        │
│ └───────┘ │ └───────┘ │ └───────┘ │ └───────┘ │        │
│ ┌───────┐ │ ┌───────┐ │ ┌───────┐ │           │        │
│ │Card 2 │ │ │Card 4 │ │ │Card 6 │ │           │        │
│ └───────┘ │ └───────┘ │ └───────┘ │           │        │
└───────────┴───────────┴───────────┴───────────┴────────┘
```

### Card Components

```yaml
card_structure:
  title: "{{task_name}}"
  description: "{{detailed_description}}"
  
  metadata:
    labels:
      - name: "Bug"
        color: red
      - name: "Feature"
        color: green
      - name: "Urgent"
        color: orange
        
    members: ["@member1", "@member2"]
    due_date: "2024-01-20"
    start_date: "2024-01-15"
    
  attachments:
    - type: file
      url: "{{attachment_url}}"
    - type: link
      url: "{{external_link}}"
      
  checklists:
    - name: "Acceptance Criteria"
      items:
        - "Requirement 1"
        - "Requirement 2"
        - "Requirement 3"
        
  custom_fields:
    story_points: 5
    sprint: "Sprint 15"
```

## Butler Automation

### Automation Rules

```yaml
butler_rules:
  - name: auto_assign_on_move
    trigger:
      type: card_moved_to_list
      list: "Doing"
    action:
      - join_card
      - set_due_date: "+3 days"
      - add_label: "In Progress"
      
  - name: due_date_reminder
    trigger:
      type: due_date_approaching
      days: 1
    action:
      - post_comment: "@card Reminder: Due tomorrow!"
      - move_to_list: "Urgent"
      
  - name: completion_cleanup
    trigger:
      type: card_moved_to_list
      list: "Done"
    action:
      - mark_due_complete
      - remove_all_members
      - add_label: "Completed"
      
  - name: scheduled_archive
    trigger:
      type: schedule
      frequency: weekly
      day: sunday
    action:
      - archive_cards_in_list: "Done"
      - older_than: 7_days
```

### Button Commands

```yaml
card_buttons:
  - name: "Start Working"
    actions:
      - move_to_list: "Doing"
      - join_card
      - set_due_date: "+3 days"
      - remove_label: "Backlog"
      - add_label: "In Progress"
      
  - name: "Submit for Review"
    actions:
      - move_to_list: "Review"
      - add_checklist:
          name: "Review Checklist"
          items:
            - "Code reviewed"
            - "Tests passing"
            - "Documentation updated"
      - mention: "@reviewer"
      
  - name: "Mark Complete"
    actions:
      - check_all_items
      - move_to_list: "Done"
      - mark_due_complete
      - post_comment: "✅ Completed!"
```

## Board Templates

### Sprint Board

```yaml
sprint_board_template:
  name: "Sprint {{number}}"
  
  lists:
    - name: "Sprint Backlog"
      position: 1
    - name: "To Do"
      position: 2
    - name: "In Progress"
      position: 3
      wip_limit: 5
    - name: "Code Review"
      position: 4
      wip_limit: 3
    - name: "Testing"
      position: 5
    - name: "Done"
      position: 6
      
  labels:
    - name: "Bug"
      color: red
    - name: "Feature"
      color: green
    - name: "Tech Debt"
      color: yellow
    - name: "Blocked"
      color: purple
      
  custom_fields:
    - name: "Story Points"
      type: number
    - name: "Priority"
      type: dropdown
      options: ["High", "Medium", "Low"]
```

### Content Calendar

```yaml
content_calendar_template:
  name: "Content Calendar - {{month}}"
  
  lists:
    - name: "Ideas"
    - name: "Planning"
    - name: "Writing"
    - name: "Editing"
    - name: "Scheduled"
    - name: "Published"
    
  labels:
    - name: "Blog"
      color: blue
    - name: "Social"
      color: pink
    - name: "Video"
      color: purple
    - name: "Newsletter"
      color: green
      
  card_template:
    name: "{{content_title}}"
    description: |
      **Topic:** {{topic}}
      **Target Audience:** {{audience}}
      **Keywords:** {{keywords}}
      **Publish Date:** {{date}}
    checklists:
      - name: "Content Workflow"
        items:
          - "Research complete"
          - "Outline approved"
          - "First draft"
          - "Edit pass"
          - "Graphics ready"
          - "SEO optimized"
          - "Scheduled"
```

## Workflow Automation

### Card Movement Rules

```yaml
workflow_rules:
  to_do:
    entry_actions:
      - require_due_date
      - require_labels
    exit_requirements:
      - has_assignee
      
  in_progress:
    entry_actions:
      - start_timer
      - add_comment: "Work started"
    constraints:
      wip_limit: 3
      
  review:
    entry_actions:
      - notify_reviewers
      - add_checklist: review_checklist
    exit_requirements:
      - all_checklist_complete
      
  done:
    entry_actions:
      - stop_timer
      - calculate_cycle_time
      - notify_stakeholders
```

### Checklist Templates

```yaml
checklist_templates:
  bug_fix:
    name: "Bug Fix Checklist"
    items:
      - "Reproduce the bug"
      - "Identify root cause"
      - "Write fix"
      - "Add tests"
      - "Test locally"
      - "Code review"
      - "Deploy to staging"
      - "Verify fix"
      
  feature:
    name: "Feature Checklist"
    items:
      - "Requirements documented"
      - "Design approved"
      - "Implementation complete"
      - "Unit tests written"
      - "Integration tested"
      - "Documentation updated"
      - "Demo prepared"
```

## Power-Up Integrations

### Popular Power-Ups

```yaml
power_ups:
  calendar:
    description: "Visualize cards with due dates"
    view: calendar
    sync: true
    
  custom_fields:
    fields:
      - name: "Priority"
        type: dropdown
      - name: "Estimate"
        type: number
      - name: "Client"
        type: text
        
  card_aging:
    enable: true
    mode: regular  # or pirate mode
    
  voting:
    enable: true
    one_vote_per_member: true
```

### Slack Integration

```yaml
slack_integration:
  notifications:
    - trigger: card_created
      channel: "#project-updates"
      
    - trigger: card_moved_to
      list: "Done"
      channel: "#wins"
      
    - trigger: comment_added
      notify: card_members
      
  commands:
    /trello:
      - add_card
      - search_cards
      - my_cards
```

## Reporting & Analytics

### Board Metrics

```
BOARD ANALYTICS - SPRINT 15
═══════════════════════════════════════

CARDS:
Total:        45
Completed:    28 (62%)
In Progress:  12
Blocked:      2

VELOCITY:
This Sprint:  28 cards
Average:      25 cards
Trend:        +12%

CYCLE TIME:
Average:      3.2 days
Shortest:     0.5 days
Longest:      8 days

BY LABEL:
Feature    █████████████░░░ 18
Bug        ████████░░░░░░░░ 12
Tech Debt  █████░░░░░░░░░░░ 8
Other      ███░░░░░░░░░░░░░ 7

BY MEMBER:
Sarah     ████████████░░░░ 15
Mike      ██████████░░░░░░ 12
Lisa      ████████░░░░░░░░ 10
Alex      ██████░░░░░░░░░░ 8
```

### Burndown Chart

```
SPRINT BURNDOWN
│ 45 ┤ ▪
│    │  ▪▪
│    │    ▪▪ ← Ideal
│    │      ▪▪
│ 22 ┤        ●●
│    │          ●● ← Actual
│    │            ▪▪●●
│    │              ▪▪●●
│  0 ┤                ▪▪●●
└────┴────────────────────────
     Day 1              Day 14

On Track: ✓ 2 cards ahead of schedule
```

## API Examples

### Create Card

```javascript
// Create Card with full details
const card = await trello.cards.create({
  name: "Implement user authentication",
  desc: "Add OAuth2 support for Google and GitHub",
  idList: "list_id",
  idLabels: ["label_id_1", "label_id_2"],
  idMembers: ["member_id"],
  due: "2024-01-20T17:00:00.000Z",
  pos: "top"
});

// Add Checklist
await trello.cards.createChecklist(card.id, {
  name: "Implementation Tasks"
});

// Add Checklist Item
await trello.checklists.createCheckItem(checklistId, {
  name: "Set up OAuth provider",
  checked: false
});
```

### Move Card

```javascript
// Move card to different list
await trello.cards.update(cardId, {
  idList: "new_list_id",
  pos: "bottom"
});

// Add comment
await trello.cards.createComment(cardId, {
  text: "Moving to review. @reviewer please check."
});
```

## Best Practices

1. **Simple Lists**: 5-7 lists maximum
2. **Clear Labels**: Consistent color coding
3. **Due Dates**: Set realistic deadlines
4. **WIP Limits**: Prevent bottlenecks
5. **Regular Cleanup**: Archive completed cards
6. **Checklists**: Break down complex tasks
7. **Butler Rules**: Automate repetitive actions
8. **Board Templates**: Standardize workflows
