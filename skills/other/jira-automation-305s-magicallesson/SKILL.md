---
name: Jira Automation
description: Automate Jira project management workflows, sprint planning, issue tracking, and reporting
version: 1.0.0
author: Claude Office Skills
category: project-management
tags:
  - jira
  - agile
  - sprint
  - project-management
  - automation
department: engineering
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: project-mcp
  tools:
    - jira_create_issue
    - jira_update_issue
    - jira_search
    - jira_transition
capabilities:
  - Issue creation and management
  - Sprint planning automation
  - Workflow automation
  - Reporting and analytics
input:
  - Issue details
  - Sprint configurations
  - Workflow rules
  - Report parameters
output:
  - Created/updated issues
  - Sprint reports
  - Burndown charts
  - Velocity metrics
languages:
  - en
related_skills:
  - asana-automation
  - linear-automation
  - github-integration
---

# Jira Automation

Comprehensive skill for automating Jira project management and agile workflows.

## Core Workflows

### 1. Issue Management Pipeline

```
ISSUE LIFECYCLE:
┌─────────────────┐
│    Backlog      │
└────────┬────────┘
         ▼
┌─────────────────┐
│   To Do         │──────┐
└────────┬────────┘      │
         ▼               │
┌─────────────────┐      │ Blocked
│   In Progress   │◄─────┘
└────────┬────────┘
         ▼
┌─────────────────┐
│   In Review     │
└────────┬────────┘
         ▼
┌─────────────────┐
│     Done        │
└─────────────────┘
```

### 2. Automation Rules

```yaml
automation_rules:
  - name: auto_assign_on_transition
    trigger:
      type: issue_transitioned
      to_status: "In Progress"
    condition:
      assignee: unassigned
    action:
      assign_to: trigger_user

  - name: add_label_on_priority
    trigger:
      type: issue_created
      priority: highest
    action:
      - add_label: "urgent"
      - send_slack: "#dev-alerts"

  - name: auto_close_subtasks
    trigger:
      type: issue_transitioned
      to_status: "Done"
      issue_type: Story
    action:
      transition_subtasks: "Done"

  - name: sla_warning
    trigger:
      type: scheduled
      cron: "0 9 * * 1-5"
    condition:
      jql: "status = 'In Progress' AND updated < -3d"
    action:
      - add_comment: "@assignee Please update this issue"
      - send_notification: assignee
```

## Sprint Management

### Sprint Planning Template

```yaml
sprint_planning:
  name: "Sprint {{sprint_number}}"
  duration: 14  # days
  
  capacity_planning:
    team_size: 6
    hours_per_day: 6
    total_capacity: 504  # hours
    
  story_points:
    target: 42
    buffer: 10%  # for unplanned work
    
  ceremonies:
    - name: Sprint Planning
      day: 1
      duration: 2h
    - name: Daily Standup
      day: "daily"
      duration: 15m
    - name: Sprint Review
      day: 14
      duration: 1h
    - name: Retrospective
      day: 14
      duration: 1h
```

### Sprint Board Configuration

```yaml
board_config:
  type: scrum
  columns:
    - name: Backlog
      statuses: ["Backlog"]
    - name: To Do
      statuses: ["To Do", "Selected for Development"]
      wip_limit: null
    - name: In Progress
      statuses: ["In Progress"]
      wip_limit: 6
    - name: In Review
      statuses: ["Code Review", "QA"]
      wip_limit: 4
    - name: Done
      statuses: ["Done"]
      
  swimlanes:
    type: assignee
    show_epics: true
```

## Issue Templates

### Bug Report

```yaml
bug_template:
  project: DEV
  issue_type: Bug
  fields:
    summary: "[BUG] {{title}}"
    description: |
      ## Description
      {{description}}
      
      ## Steps to Reproduce
      1. {{step1}}
      2. {{step2}}
      3. {{step3}}
      
      ## Expected Behavior
      {{expected}}
      
      ## Actual Behavior
      {{actual}}
      
      ## Environment
      - Browser: {{browser}}
      - OS: {{os}}
      - Version: {{app_version}}
      
      ## Screenshots
      {{attachments}}
    
    priority: {{severity}}
    labels: ["bug", "needs-triage"]
    components: ["{{component}}"]
```

### Feature Request

```yaml
feature_template:
  project: DEV
  issue_type: Story
  fields:
    summary: "[FEATURE] {{title}}"
    description: |
      ## User Story
      As a {{user_type}}, I want to {{action}} so that {{benefit}}.
      
      ## Acceptance Criteria
      - [ ] {{criteria1}}
      - [ ] {{criteria2}}
      - [ ] {{criteria3}}
      
      ## Technical Notes
      {{tech_notes}}
      
      ## Design Mockups
      {{mockups}}
    
    labels: ["feature", "needs-refinement"]
    story_points: null  # To be estimated
```

### Epic Structure

```yaml
epic_template:
  project: DEV
  issue_type: Epic
  fields:
    summary: "{{epic_name}}"
    description: |
      ## Overview
      {{overview}}
      
      ## Goals
      - {{goal1}}
      - {{goal2}}
      
      ## Success Metrics
      | Metric | Current | Target |
      |--------|---------|--------|
      | {{metric1}} | {{current1}} | {{target1}} |
      
      ## Timeline
      Start: {{start_date}}
      Target Completion: {{end_date}}
      
      ## Dependencies
      {{dependencies}}
      
    child_issues:
      - type: Story
        count: "auto"
```

## JQL Queries Library

### Common Queries

```jql
# My open issues
assignee = currentUser() AND resolution = Unresolved ORDER BY priority DESC

# Sprint progress
project = DEV AND Sprint = "Sprint 15" ORDER BY status

# Bugs by severity
project = DEV AND type = Bug AND resolution = Unresolved 
ORDER BY priority DESC, created ASC

# Stale issues
project = DEV AND status = "In Progress" AND updated < -7d

# Ready for review
project = DEV AND status = "Code Review" AND "Code Reviewer" is EMPTY

# Release scope
fixVersion = "v2.5.0" AND resolution = Unresolved

# Team velocity
project = DEV AND type = Story AND Sprint in closedSprints() 
AND resolved >= -90d

# Blockers
project = DEV AND (priority = Blocker OR labels = blocked)
AND resolution = Unresolved
```

## Reporting & Dashboards

### Sprint Dashboard

```
SPRINT 15 DASHBOARD
═══════════════════════════════════════

Progress:
Day 8 of 14 │ ████████░░░░░░ 57%

Story Points:
Committed: 42
Completed: 24  │ ████████████░░░░░░░░ 57%
Remaining: 18

Burndown:
│ 42 ┤ ▪
│    │  ▪▪
│    │    ▪▪
│    │      ▪▪▪
│ 21 ┤         ▪ ← Ideal
│    │          ▪▪
│    │            ▪▪
│    │              ▪▪
│  0 ┤                ▪
└────┴────────────────────
     Day 1           Day 14

Issue Status:
To Do        ███░░░░░░░ 6
In Progress  █████░░░░░ 8
In Review    ████░░░░░░ 5
Done         █████████░ 12
```

### Velocity Chart

```
TEAM VELOCITY (Last 6 Sprints)
═══════════════════════════════════════

│  50 ┤
│     │           ▓▓
│  40 ┤    ▓▓     ▓▓     ▓▓     ▓▓
│     │    ▓▓ ▓▓  ▓▓     ▓▓ ▓▓  ▓▓
│  30 ┤ ▓▓ ▓▓ ▓▓  ▓▓ ▓▓  ▓▓ ▓▓  ▓▓
│     │ ▓▓ ▓▓ ▓▓  ▓▓ ▓▓  ▓▓ ▓▓  ▓▓
│  20 ┤ ▓▓ ▓▓ ▓▓  ▓▓ ▓▓  ▓▓ ▓▓  ▓▓
│     │ ▓▓ ▓▓ ▓▓  ▓▓ ▓▓  ▓▓ ▓▓  ▓▓
│  10 ┤ ▓▓ ▓▓ ▓▓  ▓▓ ▓▓  ▓▓ ▓▓  ▓▓
│     │ ▓▓ ▓▓ ▓▓  ▓▓ ▓▓  ▓▓ ▓▓  ▓▓
│   0 ┴─────────────────────────────
       S10 S11 S12 S13 S14 S15

Average: 38 points | Trend: +5%
```

## Integration Workflows

### GitHub Integration

```yaml
github_integration:
  branch_creation:
    trigger: issue_transitioned_to_in_progress
    pattern: "{{issue_type}}/{{issue_key}}-{{summary_slug}}"
    
  commit_linking:
    patterns:
      - "{{issue_key}}"
      - "#{{issue_key}}"
    action: add_comment_with_link
    
  pr_automation:
    on_pr_open:
      - transition_issue: "Code Review"
      - add_pr_link_to_issue
    on_pr_merge:
      - transition_issue: "Done"
      - add_comment: "Merged in {{pr_url}}"
```

### Slack Integration

```yaml
slack_integration:
  channels:
    dev_updates: "#dev-updates"
    alerts: "#dev-alerts"
    
  notifications:
    - event: blocker_created
      channel: alerts
      message: "🚨 Blocker: {{issue.key}} - {{issue.summary}}"
      
    - event: sprint_started
      channel: dev_updates
      message: "🏃 Sprint {{sprint.name}} has started! Goal: {{sprint.goal}}"
      
    - event: release_completed
      channel: dev_updates
      message: "🚀 Release {{version}} is live!"
```

## Workflow Customization

### Custom Workflow

```yaml
workflow:
  name: Development Workflow
  statuses:
    - Backlog
    - Ready for Dev
    - In Progress
    - Code Review
    - QA
    - Ready for Release
    - Done
    
  transitions:
    - from: Backlog
      to: Ready for Dev
      name: "Refine"
      conditions:
        - story_points_set
        
    - from: Ready for Dev
      to: In Progress
      name: "Start Work"
      post_functions:
        - assign_to_current_user
        
    - from: In Progress
      to: Code Review
      name: "Submit for Review"
      validators:
        - has_linked_pr
        
    - from: Code Review
      to: QA
      name: "Pass Review"
      conditions:
        - all_reviewers_approved
        
    - from: QA
      to: Done
      name: "Pass QA"
      post_functions:
        - resolve_issue
```

## Best Practices

1. **Keep Issues Small**: Break down to complete in 1-2 days
2. **Write Clear Descriptions**: Include all context needed
3. **Link Related Issues**: Use proper issue linking
4. **Update Status Regularly**: Move cards as work progresses
5. **Use Labels Consistently**: Establish team conventions
6. **Estimate in Points**: Use relative sizing
7. **Review Backlog Weekly**: Keep backlog groomed
