---
name: Linear Automation
description: Automate Linear issue tracking, cycle planning, roadmap management, and engineering workflows
version: 1.0.0
author: Claude Office Skills
category: project-management
tags:
  - linear
  - issue-tracking
  - engineering
  - agile
  - automation
department: engineering
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: project-mcp
  tools:
    - linear_create_issue
    - linear_update_issue
    - linear_search
    - linear_cycles
capabilities:
  - Issue creation and management
  - Cycle planning
  - Roadmap tracking
  - GitHub integration
input:
  - Issue details
  - Cycle configurations
  - Project milestones
  - Team assignments
output:
  - Created/updated issues
  - Cycle reports
  - Roadmap views
  - Velocity metrics
languages:
  - en
related_skills:
  - jira-automation
  - github-integration
  - asana-automation
---

# Linear Automation

Comprehensive skill for automating Linear issue tracking and engineering workflows.

## Core Workflows

### 1. Issue Lifecycle

```
LINEAR ISSUE FLOW:
┌─────────────────┐
│    Triage       │
│   (Backlog)     │
└────────┬────────┘
         ▼
┌─────────────────┐
│    Todo         │
│  (Prioritized)  │
└────────┬────────┘
         ▼
┌─────────────────┐
│  In Progress    │
│   (Active)      │
└────────┬────────┘
         ▼
┌─────────────────┐
│   In Review     │
│  (PR Created)   │
└────────┬────────┘
         ▼
┌─────────────────┐
│     Done        │
│   (Merged)      │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Cancelled     │
│  (If needed)    │
└─────────────────┘
```

### 2. Automation Triggers

```yaml
automations:
  - name: auto_assign_on_start
    trigger:
      type: status_changed
      to: "In Progress"
    condition:
      assignee: null
    action:
      set_assignee: "{{trigger_user}}"
      
  - name: add_to_cycle
    trigger:
      type: issue_created
      labels: ["sprint-ready"]
    action:
      add_to_cycle: current
      set_priority: urgent
      
  - name: create_pr_reminder
    trigger:
      type: status_changed
      to: "In Progress"
      duration: "48 hours"
    condition:
      no_linked_pr: true
    action:
      add_comment: "@{{assignee}} Please link your PR"
      
  - name: close_on_merge
    trigger:
      type: github_pr_merged
    action:
      set_status: "Done"
      add_comment: "Closed via PR merge"
```

## Issue Templates

### Bug Report

```yaml
bug_template:
  title: "[Bug] {{summary}}"
  team: "Engineering"
  
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
    - OS: {{os}}
    - Browser: {{browser}}
    - Version: {{version}}
    
    ## Logs/Screenshots
    {{attachments}}
    
  labels: ["bug", "needs-triage"]
  priority: "{{severity}}"
  estimate: null
```

### Feature Request

```yaml
feature_template:
  title: "[Feature] {{summary}}"
  team: "Product"
  
  description: |
    ## Overview
    {{overview}}
    
    ## User Story
    As a {{user_type}}, I want to {{action}} so that {{benefit}}.
    
    ## Acceptance Criteria
    - [ ] {{criteria1}}
    - [ ] {{criteria2}}
    - [ ] {{criteria3}}
    
    ## Design
    {{design_link}}
    
    ## Technical Considerations
    {{tech_notes}}
    
  labels: ["feature", "needs-refinement"]
  project: "{{roadmap_project}}"
```

### Sub-Issue Structure

```yaml
epic_breakdown:
  parent:
    title: "{{epic_name}}"
    type: "Project"
    
  sub_issues:
    - title: "Design: {{epic_name}}"
      labels: ["design"]
      estimate: 3
      
    - title: "Backend: {{epic_name}}"
      labels: ["backend"]
      estimate: 5
      
    - title: "Frontend: {{epic_name}}"
      labels: ["frontend"]
      estimate: 5
      
    - title: "Testing: {{epic_name}}"
      labels: ["qa"]
      estimate: 2
      
    - title: "Documentation: {{epic_name}}"
      labels: ["docs"]
      estimate: 1
```

## Cycle Management

### Cycle Planning

```yaml
cycle_config:
  duration: 2_weeks
  
  planning:
    capacity_per_engineer: 8  # points
    buffer_percentage: 20
    
  milestones:
    - day: 1
      event: "Cycle Start"
    - day: 10
      event: "Feature Freeze"
    - day: 12
      event: "Code Freeze"
    - day: 14
      event: "Release"
      
  auto_rollover:
    enabled: true
    statuses: ["Backlog", "Todo"]
    exclude_labels: ["blocked"]
```

### Cycle Dashboard

```
CYCLE 24 - WEEK 2/2
═══════════════════════════════════════

Progress:
████████████████░░░░ 78% Complete

Story Points:
Planned:    42
Completed:  33  ████████████████░░░░
Remaining:   9  ████░░░░░░░░░░░░░░░░

BY STATUS:
Done         ████████████████ 18
In Review    ████░░░░░░░░░░░░ 5
In Progress  ██░░░░░░░░░░░░░░ 3
Todo         ██░░░░░░░░░░░░░░ 2

TEAM PROGRESS:
Sarah    ██████████████░░ 8/10 pts
Mike     ████████████████ 12/12 pts
Alex     ██████████░░░░░░ 7/10 pts
Lisa     ████████████░░░░ 6/10 pts

BLOCKERS:
• LIN-234: Waiting for API access
• LIN-256: Design review pending
```

## GitHub Integration

### Branch & PR Sync

```yaml
github_sync:
  branch_format: "{{username}}/lin-{{issue_number}}-{{issue_slug}}"
  
  on_branch_created:
    - set_status: "In Progress"
    - add_assignee: branch_creator
    
  on_pr_opened:
    - set_status: "In Review"
    - add_link: pr_url
    - add_comment: "PR opened: {{pr_url}}"
    
  on_pr_merged:
    - set_status: "Done"
    - add_comment: "Merged in {{pr_url}}"
    
  on_pr_closed:
    - add_comment: "PR closed without merge"
    
  commit_linking:
    patterns:
      - "LIN-{{number}}"
      - "lin-{{number}}"
      - "Fixes LIN-{{number}}"
```

### CI/CD Integration

```yaml
cicd_integration:
  on_build_failed:
    - add_label: "ci-failed"
    - add_comment: |
        ❌ Build failed
        {{build_url}}
        
  on_build_passed:
    - remove_label: "ci-failed"
    
  on_deploy_staging:
    - add_label: "on-staging"
    - add_comment: "Deployed to staging: {{staging_url}}"
    
  on_deploy_production:
    - add_label: "released"
    - add_comment: "Released to production 🚀"
```

## Labels & Organization

### Label System

```yaml
labels:
  type:
    - name: "bug"
      color: "#eb5757"
    - name: "feature"
      color: "#5e6ad2"
    - name: "improvement"
      color: "#26b5ce"
    - name: "chore"
      color: "#bec2c8"
      
  priority:
    - name: "urgent"
      color: "#eb5757"
    - name: "high"
      color: "#f2994a"
    - name: "medium"
      color: "#f2c94c"
    - name: "low"
      color: "#bec2c8"
      
  area:
    - name: "frontend"
      color: "#5e6ad2"
    - name: "backend"
      color: "#26b5ce"
    - name: "infrastructure"
      color: "#bb87fc"
    - name: "design"
      color: "#f7b500"
      
  status:
    - name: "blocked"
      color: "#eb5757"
    - name: "needs-review"
      color: "#f2994a"
    - name: "ready"
      color: "#0e7a42"
```

## Reporting

### Velocity Tracking

```yaml
velocity_report:
  metrics:
    - completed_points_per_cycle
    - issues_closed_per_cycle
    - cycle_completion_rate
    - carryover_percentage
    
  chart_data:
    cycles: last_6
    show_trend: true
    show_commitment: true
```

### Team Analytics

```
TEAM VELOCITY - LAST 6 CYCLES
═══════════════════════════════════════

│  50 ┤
│     │              ▓▓
│  40 ┤    ▓▓  ▓▓    ▓▓  ▓▓
│     │    ▓▓  ▓▓    ▓▓  ▓▓  ▓▓
│  30 ┤ ▓▓ ▓▓  ▓▓ ▓▓ ▓▓  ▓▓  ▓▓
│     │ ▓▓ ▓▓  ▓▓ ▓▓ ▓▓  ▓▓  ▓▓
│  20 ┤ ▓▓ ▓▓  ▓▓ ▓▓ ▓▓  ▓▓  ▓▓
│     │ ▓▓ ▓▓  ▓▓ ▓▓ ▓▓  ▓▓  ▓▓
│  10 ┤ ▓▓ ▓▓  ▓▓ ▓▓ ▓▓  ▓▓  ▓▓
│     │ ▓▓ ▓▓  ▓▓ ▓▓ ▓▓  ▓▓  ▓▓
│   0 ┴─────────────────────────
       C19 C20 C21 C22 C23 C24

Average: 38 pts | Trend: +8%
Completion Rate: 92%
```

## API Examples

### GraphQL Queries

```graphql
# Create Issue
mutation CreateIssue {
  issueCreate(input: {
    teamId: "team-id"
    title: "New Feature Request"
    description: "Description here"
    priority: 2
    labelIds: ["label-id"]
  }) {
    success
    issue {
      id
      identifier
      url
    }
  }
}

# Update Issue Status
mutation UpdateIssue {
  issueUpdate(
    id: "issue-id"
    input: {
      stateId: "state-id"
      assigneeId: "user-id"
    }
  ) {
    success
  }
}

# Query Cycle Issues
query CycleIssues {
  cycle(id: "cycle-id") {
    name
    issues {
      nodes {
        identifier
        title
        state {
          name
        }
        assignee {
          name
        }
        estimate
      }
    }
  }
}
```

## Best Practices

1. **Quick Triage**: Process new issues daily
2. **Consistent Estimates**: Use planning poker
3. **Link Everything**: Connect PRs, commits, docs
4. **Use Projects**: Organize related work
5. **Cycle Commitment**: Protect sprint scope
6. **Regular Grooming**: Keep backlog healthy
7. **Automate Status**: Let integrations update
8. **Measure Velocity**: Track team capacity
