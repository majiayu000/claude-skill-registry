---
name: faion-pm-traditional
user-invocable: false
description: "Traditional PM specialist: PMBoK knowledge areas (scope, schedule, cost, risk, quality, stakeholder, resources), EVM, WBS, project lifecycle, PMBoK 7/8 framework. 22 methodologies."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---

# Traditional PM Sub-Skill

**Communication: User's language. Docs/code: English.**

## Purpose

Traditional/predictive project management based on PMBoK 7th Edition and PMBoK 8 updates. Core knowledge areas, processes, and project lifecycle management.

---

## Context Discovery

### Auto-Investigation

Detect existing PM artifacts from project:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| WBS | `Glob("**/wbs*.md")` or `Glob("**/work-breakdown/*")` | Work breakdown documented |
| Risk register | `Glob("**/risk*.md")` or `Grep("Risk ID")` | Risk management in place |
| Stakeholder register | `Glob("**/stakeholder*.md")` or `Grep("Power/Interest")` | Stakeholder management active |
| Project charter | `Glob("**/charter*.md")` or `Glob("**/project-charter/*")` | Formal project initiation |
| EVM metrics | `Grep("CPI\\|SPI\\|EAC\\|BAC")` | Earned value tracking |
| Change log | `Glob("**/change*.md")` or `Glob("**/changes/*")` | Change control process |
| Schedule | `Glob("**/schedule*.md")` or `Grep("critical path")` | Schedule management |
| Lessons learned | `Glob("**/lessons*.md")` or `Glob("**/retrospectives/*")` | Knowledge capture |

**Read existing PM documentation:**
- Project charter
- WBS or scope statement
- Risk register
- Stakeholder register
- Schedule or Gantt charts
- Change control board decisions

### Discovery Questions

#### Q1: Project Phase

```yaml
question: "What phase is your project in?"
header: "Lifecycle"
multiSelect: false
options:
  - label: "Initiation (charter, stakeholders)"
    description: "Starting new project, need structure"
  - label: "Planning (scope, schedule, budget)"
    description: "Defining what to build, when, and at what cost"
  - label: "Execution (delivering work)"
    description: "Active development, need monitoring and control"
  - label: "Closing (lessons learned, handoff)"
    description: "Project ending, documenting outcomes"
```

#### Q2: Knowledge Area Focus

```yaml
question: "Which PMBoK knowledge area do you need help with?"
header: "Focus"
multiSelect: false
options:
  - label: "Scope (WBS, requirements)"
    description: "Define what's included and excluded"
  - label: "Schedule (timeline, dependencies)"
    description: "Critical path, milestones, Gantt charts"
  - label: "Cost (estimation, budget, EVM)"
    description: "Budget planning and performance tracking"
  - label: "Risk (identify, assess, mitigate)"
    description: "Risk register and response strategies"
  - label: "Stakeholder (identify, engage)"
    description: "Stakeholder analysis and communication"
  - label: "Integration (overall coordination)"
    description: "Change control, integration across areas"
```

#### Q3: Formality Level

```yaml
question: "How formal does your process need to be?"
header: "Context"
multiSelect: false
options:
  - label: "Lightweight (small team, startup)"
    description: "Essential PMBoK practices only"
  - label: "Standard (mid-size project)"
    description: "Core knowledge areas, documented processes"
  - label: "Formal (enterprise, compliance)"
    description: "Full PMBoK rigor, auditable artifacts"
  - label: "Hybrid (agile + predictive)"
    description: "Blend waterfall planning with agile execution"
```

---

## Methodology Categories

### Stakeholder Management (3)

| Methodology | File | Focus |
|-------------|------|-------|
| Stakeholder Register | stakeholder-register.md | Identify stakeholders, document info |
| Stakeholder Engagement | stakeholder-engagement.md | Power/interest analysis, engagement |
| Stakeholder Advanced | stakeholder-engagement-advanced.md | Influence strategies, mapping |

### Planning (6)

| Methodology | File | Knowledge Area |
|-------------|------|----------------|
| Scope Management | scope-management.md | Scope definition, validation |
| WBS Creation | wbs-creation.md | Work packages, decomposition |
| Work Breakdown Structure | work-breakdown-structure.md | WBS dictionary, templates |
| Schedule Development | schedule-development.md | Critical path, dependencies |
| Cost Estimation | cost-estimation.md | Bottom-up, parametric, analogous |
| Resource Management | resource-management.md | Resource allocation, leveling |

### Risk Management (2)

| Methodology | File | Focus |
|-------------|------|-------|
| Risk Register | risk-register.md | Risk identification, assessment |
| Risk Management | risk-management.md | Risk responses, monitoring |

### Execution & Control (3)

| Methodology | File | Knowledge Area |
|-------------|------|----------------|
| Quality Management | quality-management.md | Quality planning, assurance, control |
| Communications | communications-management.md | Communication planning, distribution |
| Change Control | change-control.md | Change requests, CCB, baselines |

### Monitoring (2)

| Methodology | File | Focus |
|-------------|------|-------|
| Earned Value Mgmt | earned-value-management.md | EVM metrics (CPI, SPI, EAC) |
| Project Integration | project-integration.md | Integration across knowledge areas |

### Closure (3)

| Methodology | File | Focus |
|-------------|------|-------|
| Project Closure | project-closure.md | Administrative, contract closure |
| Lessons Learned | lessons-learned.md | Knowledge capture, retrospectives |
| Benefits Realization | benefits-realization.md | Value tracking, benefits mgmt |

### Specialized (1)

| Methodology | File | Focus |
|-------------|------|-------|
| Procurement | procurement-management.md | Vendor selection, contracts |

### Certification (2)

| Reference | File | Content |
|-----------|------|---------|
| Alignment 2026 | pm-certification-alignment-2026.md | PMP/CAPM exam mapping |
| Changes 2026 | pm-certification-changes-2026.md | Exam updates |

## Quick Selector

| Need | Use |
|------|-----|
| Identify stakeholders | stakeholder-register.md |
| Plan scope | scope-management.md |
| Break down work | wbs-creation.md |
| Create timeline | schedule-development.md |
| Estimate costs | cost-estimation.md |
| Manage risks | risk-register.md → risk-management.md |
| Track performance | earned-value-management.md |
| Close project | project-closure.md → lessons-learned.md |

## PMBoK Mapping

| Performance Domain | Methodologies |
|--------------------|---------------|
| Stakeholder | stakeholder-* (3) |
| Planning | scope, wbs, schedule, cost, resources (6) |
| Work | integration, communications, change (3) |
| Delivery | quality, benefits (2) |
| Measurement | earned-value (1) |
| Uncertainty | risk-* (2) |

## Integration

| Skill | Integration |
|-------|-------------|
| faion-agile-pm | Provides planning inputs for agile execution |
| faion-business-analyst | Requirements feed into scope |
| faion-sdd | Task planning uses scheduling methods |

---

*Traditional PM Sub-Skill v1.0 - 22 methodologies*
