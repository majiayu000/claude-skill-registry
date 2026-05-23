---
name: faion-pm-agile
user-invocable: false
description: "Agile PM specialist: Scrum, Kanban, SAFe ceremonies, PM tools (Jira, Linear, ClickUp, GitHub, Azure DevOps), dashboards, team development, AI in PM, hybrid delivery. 28 methodologies."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---

# Agile PM Sub-Skill

**Communication: User's language. Docs/code: English.**

## Purpose

Agile project management methodologies, tools, ceremonies, and modern PM practices. Supports Scrum, Kanban, SAFe, and hybrid approaches.

---

## Context Discovery

### Auto-Investigation

Detect existing agile setup from project:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| Jira config | `Glob("**/.jira/*")` or `Grep("jira.atlassian.com")` | Jira in use |
| GitHub Projects | `Grep("projects/", "**/.github/*")` | GitHub Projects setup |
| Linear config | `Glob("**/.linear/*")` or `Grep("linear.app")` | Linear tracking |
| Sprint docs | `Grep("sprint", "**/*.md")` | Sprint ceremonies documented |
| Kanban board | `Grep("kanban", "**/*.md")` or `Grep("WIP limit")` | Kanban in use |
| Retrospectives | `Glob("**/retro*.md")` or `Glob("**/retrospectives/*")` | Retros documented |
| Velocity metrics | `Grep("velocity", "**/*.md")` | Metrics tracked |
| Standup notes | `Glob("**/standup*.md")` or `Glob("**/daily/*")` | Daily standups documented |

**Read existing agile artifacts:**
- Any sprint planning docs
- Retrospective notes
- Dashboard configs
- Team charter or working agreements
- Definition of Done

### Discovery Questions

#### Q1: Agile Maturity

```yaml
question: "What's your current agile setup?"
header: "Maturity"
multiSelect: false
options:
  - label: "No agile process yet"
    description: "Starting from scratch, need to choose approach"
  - label: "Basic ceremonies (standups, planning)"
    description: "Have ceremonies but inconsistent or need improvement"
  - label: "Established Scrum/Kanban"
    description: "Working process, optimizing or scaling"
  - label: "SAFe or scaled agile"
    description: "Multiple teams, program increments, coordination"
```

#### Q2: PM Tool Status

```yaml
question: "What PM tool are you using or considering?"
header: "Tooling"
multiSelect: false
options:
  - label: "No tool yet, need to select one"
    description: "Need tool comparison and recommendation"
  - label: "Jira (cloud or server)"
    description: "Using Jira, need workflow optimization"
  - label: "GitHub Projects or GitLab Boards"
    description: "Developer-centric tool, integrated with git"
  - label: "Linear, ClickUp, Notion, or Trello"
    description: "Modern agile tool for team collaboration"
  - label: "Migrating between tools"
    description: "Moving from one PM tool to another"
```

#### Q3: Team Challenge

```yaml
question: "What's your main agile challenge?"
header: "Focus"
multiSelect: false
options:
  - label: "Setup ceremonies and workflows"
    description: "Need structure for sprints, standups, retros"
  - label: "Improve velocity or predictability"
    description: "Metrics, estimation, sprint commitment issues"
  - label: "Tool configuration or automation"
    description: "Setup dashboards, workflows, integrations"
  - label: "Hybrid approach (agile + waterfall)"
    description: "Blending predictive and agile practices"
```

---

## Methodology Categories

### Agile Ceremonies (2)

| Methodology | File | Focus |
|-------------|------|-------|
| Scrum Ceremonies | scrum-ceremonies.md | Sprint planning, daily standups, reviews, retros |
| Kanban & SAFe Ceremonies | kanban-scaled-agile-ceremonies.md | Kanban cadences, SAFe PI planning, inspect & adapt |

### PM Tools (8)

| Tool | File | Best For |
|------|------|----------|
| Jira | jira-workflow-management.md | Enterprise agile, scaled teams |
| ClickUp | clickup-setup.md | All-in-one workspace |
| Linear | linear-issue-tracking.md | Engineering teams, velocity |
| GitHub Projects | github-projects.md | Developer workflow |
| GitLab Boards | gitlab-boards.md | DevOps integration |
| Azure DevOps | azure-devops-boards.md | Microsoft ecosystem |
| Notion | notion-pm.md | Knowledge + PM |
| Trello | trello-kanban.md | Simple kanban |

### Tool Management (4)

| Methodology | File | Purpose |
|-------------|------|---------|
| PM Tools Overview | pm-tools-overview.md | Tool profiles, requirements |
| PM Tools Comparison | pm-tools-comparison.md | Evaluation matrix, TCO |
| Tool Migration Basics | tool-migration-basics.md | Migration planning |
| Tool Migration Process | tool-migration-process.md | Step-by-step migration |

### Reporting & Metrics (2)

| Methodology | File | Focus |
|-------------|------|-------|
| Dashboard Setup | dashboard-setup.md | Metrics, KPIs, velocity charts |
| Reporting Basics | reporting-basics.md | Sprint reports, burn charts |

### Team & Organization (2)

| Methodology | File | Focus |
|-------------|------|-------|
| Team Development | team-development.md | Team building, psychological safety |
| RACI Matrix | raci-matrix.md | Roles and responsibilities |

### Modern PM (3)

| Methodology | File | Focus |
|-------------|------|-------|
| AI in PM | ai-in-project-management.md | AI tools overview |
| AI Powered Tools | ai-powered-pm-tools.md | Tool automation |
| Predictive Analytics | predictive-analytics-pm.md | ML forecasting |

### Hybrid & Advanced (4)

| Methodology | File | Focus |
|-------------|------|-------|
| Agile Hybrid | agile-hybrid-approaches.md | Combining predictive/agile |
| Hybrid Delivery | hybrid-delivery.md | Water-Scrum-Fall |
| Value Stream Mgmt | value-stream-management.md | DORA metrics, flow |
| Performance Domains | performance-domains-overview.md | PMBoK 8 domains |

### Framework References (3)

| Reference | File | Content |
|-----------|------|---------|
| Seven Domains | seven-performance-domains.md | PMBoK 8 domain list |
| Six Principles | six-core-principles.md | PMBoK 8 principles |
| Framework Focus | pm-framework-focus-areas.md | PMBoK 8 focus areas |

## Quick Selector

| Need | Use |
|------|-----|
| Sprint planning | scrum-ceremonies.md |
| Select PM tool | pm-tools-overview.md → pm-tools-comparison.md |
| Setup Jira | jira-workflow-management.md |
| Dashboard | dashboard-setup.md |
| Migrate tools | tool-migration-basics.md → tool-migration-process.md |
| Team roles | raci-matrix.md |
| Hybrid approach | agile-hybrid-approaches.md |

## Integration

| Skill | Integration |
|-------|-------------|
| faion-traditional-pm | Ceremonies execute PMBoK plans |
| faion-sdd | Tool workflows support task lifecycle |
| faion-software-developer | Developer tools (GitHub, GitLab, Linear) |

---

*Agile PM Sub-Skill v1.0 - 28 methodologies*
