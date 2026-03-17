---
name: faion-project-manager
description: "PM orchestrator: coordinates agile and traditional PM approaches."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# PM Domain Skill (Orchestrator)

**Communication: User's language. Docs/code: English.**

## Purpose

Orchestrates project management activities using PMBoK 7/8 framework. Coordinates two specialized sub-skills for comprehensive PM coverage.

---

## Context Discovery

### Auto-Investigation

Check for existing PM artifacts and project setup:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| `.aidocs/` | `Glob("**/.aidocs/*")` | SDD project structure |
| `roadmap.md` | `Glob("**/roadmap.md")` | Roadmap exists |
| `constitution.md` | `Glob("**/constitution.md")` | Project standards defined |
| Jira/Linear refs | `Grep("jira\|linear\|clickup", "**/*.md")` | PM tool in use |
| Sprint folders | `Glob("**/sprint-*/**")` | Agile sprints used |
| Risk register | `Glob("**/risk*.md")` | Risk management in place |

**Read existing artifacts:**
- constitution.md for project scope and constraints
- roadmap.md for current plans
- Any existing sprint/planning docs

### Discovery Questions

Use `AskUserQuestion` to understand PM needs.

#### Q1: PM Approach

```yaml
question: "What project management approach do you prefer?"
header: "Approach"
multiSelect: false
options:
  - label: "Agile (Scrum, Kanban)"
    description: "Iterative, sprints, flexible scope"
  - label: "Traditional (Waterfall, PMBoK)"
    description: "Sequential, fixed scope, detailed planning"
  - label: "Hybrid"
    description: "Mix of agile and traditional"
  - label: "Not sure / recommend"
    description: "I'll suggest based on your project"
```

**Routing:**
- "Agile" → `Skill(faion-pm-agile)`
- "Traditional" → `Skill(faion-pm-traditional)`
- "Hybrid" → Both skills as needed
- "Not sure" → Ask Q2 to determine

#### Q2: Project Characteristics (if "Not sure")

```yaml
question: "What describes your project best?"
header: "Project"
multiSelect: false
options:
  - label: "Requirements likely to change"
    description: "User feedback, evolving product"
  - label: "Requirements are fixed"
    description: "Clear deliverables, contract"
  - label: "Small team (1-5 people)"
    description: "Lightweight process needed"
  - label: "Large team / multiple teams"
    description: "Coordination, dependencies"
```

**Recommendation:**
- "Change" → Agile (Scrum or Kanban)
- "Fixed" → Traditional (WBS, schedule)
- "Small team" → Kanban or lightweight Scrum
- "Large team" → Scaled Agile or traditional PMBoK

#### Q3: PM Task Type

```yaml
question: "What PM help do you need right now?"
header: "Task"
multiSelect: true
options:
  - label: "Planning (scope, schedule, WBS)"
    description: "Define what, when, how"
  - label: "Team coordination (RACI, ceremonies)"
    description: "Roles, meetings, communication"
  - label: "Risk management"
    description: "Identify and mitigate risks"
  - label: "Progress tracking (EVM, metrics)"
    description: "Monitor and report status"
  - label: "Tool setup (Jira, Linear, etc.)"
    description: "Configure PM tooling"
```

**Routing:**
- "Planning" → wbs-creation, schedule-development
- "Team" → team-charter, raci-matrix, ceremonies
- "Risk" → risk-register, risk-response-planning
- "Progress" → earned-value-management, dashboards
- "Tool" → pm-tools-setup

#### Q4: Current PM Maturity

```yaml
question: "What's your current PM setup?"
header: "Maturity"
multiSelect: false
options:
  - label: "No formal process"
    description: "Ad-hoc, need structure"
  - label: "Basic process exists"
    description: "Have backlog, need improvement"
  - label: "Established process"
    description: "Working well, need optimization"
```

**Context impact:**
- "No formal" → Start with basics, don't overwhelm
- "Basic exists" → Build on what works, fill gaps
- "Established" → Optimize, metrics, continuous improvement

---

## Architecture

```
faion-project-manager (orchestrator)
    |
    +-> faion-project-manager:agile (28 methodologies)
    |   - Scrum, Kanban, SAFe ceremonies
    |   - PM tools (Jira, Linear, ClickUp, GitHub, etc.)
    |   - Dashboards, reporting, metrics
    |   - Team development, RACI
    |   - AI in PM, hybrid delivery
    |
    +-> faion-project-manager:traditional (22 methodologies)
        - PMBoK knowledge areas
        - Stakeholder management
        - Planning (scope, schedule, cost, WBS)
        - Risk management
        - EVM, quality, change control
        - Project closure, lessons learned
```

## References

| Reference | Content |
|-----------|---------|
| [ref-pmbok.md](ref-pmbok.md) | PMBoK 7/8 overview, 8 domains, 12/6 principles |
| [ref-CLAUDE.md](ref-CLAUDE.md) | External resources, tools, certifications |

## Sub-Skills

### faion-project-manager:agile (28 methodologies)

**Use when:**
- Planning sprints or ceremonies
- Selecting or setting up PM tools
- Building dashboards and reports
- Implementing agile/hybrid approaches
- Team development and roles

**Key methodologies:**
- Scrum/Kanban ceremonies
- Jira, Linear, ClickUp, GitHub Projects
- Dashboard setup, reporting
- Team development, RACI matrix
- AI in PM, hybrid delivery

**Location:** `~/.claude/skills/faion-project-manager:agile/`

### faion-project-manager:traditional (22 methodologies)

**Use when:**
- Planning project scope, schedule, cost
- Managing stakeholders
- Handling risks and uncertainty
- Tracking performance with EVM
- Closing projects and capturing lessons

**Key methodologies:**
- Stakeholder register and engagement
- Scope, WBS, schedule, cost, resources
- Risk register and management
- EVM, quality, change control
- Project closure, lessons learned

**Location:** `~/.claude/skills/faion-project-manager:traditional/`

## Decision Guide

| Task Type | Sub-Skill | Examples |
|-----------|-----------|----------|
| **Agile Execution** | faion-agile-pm | Sprint planning, standups, retros |
| **Tool Selection** | faion-agile-pm | Which PM tool? How to setup? |
| **Reporting** | faion-agile-pm | Dashboards, burn charts, velocity |
| **Team Structure** | faion-agile-pm | RACI, team development |
| **Project Planning** | faion-traditional-pm | Scope, WBS, schedule, cost |
| **Stakeholders** | faion-traditional-pm | Identify, analyze, engage |
| **Risk Management** | faion-traditional-pm | Risk register, responses |
| **Performance** | faion-traditional-pm | EVM (CPI, SPI, EAC) |
| **Project Closure** | faion-traditional-pm | Close, lessons learned, benefits |

## PMBoK 8 Overview

### 8 Performance Domains

| Domain | Sub-Skill |
|--------|-----------|
| Stakeholder | faion-traditional-pm |
| Team | faion-agile-pm |
| Development Approach | faion-agile-pm |
| Planning | faion-traditional-pm |
| Project Work | faion-traditional-pm |
| Delivery | Both |
| Measurement | faion-traditional-pm (EVM) + faion-agile-pm (dashboards) |
| Uncertainty | faion-traditional-pm |

### 12 Core Principles (PMBoK 7)

Stewardship, Team, Stakeholders, Value, Systems Thinking, Leadership, Tailoring, Quality, Complexity, Risk, Adaptability, Change.

## Common Workflows

### New Project

```
1. faion-traditional-pm: stakeholder-register
2. faion-agile-pm: raci-matrix
3. faion-traditional-pm: scope-management, wbs-creation
4. faion-traditional-pm: schedule-development, cost-estimation
5. faion-traditional-pm: risk-register
6. faion-agile-pm: pm-tools-overview (select tool)
```

### Sprint/Iteration

```
1. faion-agile-pm: scrum-ceremonies (planning)
2. faion-agile-pm: dashboard-setup
3. faion-traditional-pm: earned-value-management (track)
4. faion-agile-pm: scrum-ceremonies (review, retro)
```

### Health Check

```
1. faion-traditional-pm: earned-value-management
2. faion-traditional-pm: risk-management
3. faion-traditional-pm: stakeholder-engagement
4. faion-agile-pm: reporting-basics
```

## Integration Points

| Domain Skill | Integration |
|--------------|-------------|
| faion-sdd | Task planning uses PMBoK scheduling |
| faion-business-analyst | Requirements feed into scope |
| faion-product-manager | Roadmap aligns with schedule |
| faion-software-developer | Developer tools (GitHub, Linear) |

---

*PM Domain Skill v4.0 - Orchestrator*
*2 sub-skills | 50 methodologies | PMBoK 7/8*
