---
name: faion-business-analyst
description: "Business analysis: requirements engineering, stakeholder analysis, process modeling."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# BA Domain Skill

**Orchestrator for Business Analysis Framework (BABOK) practices**

---

## Context Discovery

### Auto-Investigation

Check for existing BA artifacts:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| Requirements docs | `Glob("**/requirements*.md")` | Requirements exist |
| Use cases | `Glob("**/use-case*.md")` | Use cases defined |
| User stories | `Glob("**/user-stories*.md")` | Stories written |
| BPMN diagrams | `Glob("**/*.bpmn")` | Process models exist |
| Stakeholder docs | `Glob("**/stakeholder*.md")` | Stakeholders mapped |
| `.aidocs/` | `Glob("**/.aidocs/")` | SDD structure |

**Read existing artifacts:**
- Any requirements or spec documents
- constitution.md for business context
- Existing user stories or use cases

### Discovery Questions

#### Q1: BA Activity Type

```yaml
question: "What BA activity do you need help with?"
header: "Activity"
multiSelect: false
options:
  - label: "Understand stakeholders"
    description: "Map stakeholders, plan engagement"
  - label: "Gather requirements"
    description: "Elicitation, interviews, workshops"
  - label: "Document requirements"
    description: "Use cases, user stories, specs"
  - label: "Model processes"
    description: "BPMN, workflows, data models"
  - label: "Analyze strategy"
    description: "Current state, future state, gaps"
```

**Routing:**
- "Stakeholders" → `Skill(faion-ba-core)` → stakeholder-analysis
- "Gather" → `Skill(faion-ba-core)` → elicitation-techniques
- "Document" → `Skill(faion-ba-modeling)` → use-cases, user-stories
- "Model" → `Skill(faion-ba-modeling)` → bpmn, data-models
- "Strategy" → `Skill(faion-ba-core)` → strategy-analysis

#### Q2: Requirements Format

```yaml
question: "How should requirements be documented?"
header: "Format"
multiSelect: false
options:
  - label: "User stories (Agile)"
    description: "As a... I want... So that..."
  - label: "Use cases (detailed)"
    description: "Actor, preconditions, flow"
  - label: "Functional requirements"
    description: "System shall... statements"
  - label: "Mixed / not sure"
    description: "I'll recommend based on context"
```

#### Q3: Stakeholder Access

```yaml
question: "Can you access stakeholders for elicitation?"
header: "Access"
multiSelect: false
options:
  - label: "Yes, can interview/workshop"
    description: "Direct stakeholder engagement"
  - label: "Limited (email, async)"
    description: "Remote, asynchronous"
  - label: "No access (documents only)"
    description: "Work from existing docs"
```

**Context impact:**
- "Direct" → Full elicitation techniques
- "Limited" → Surveys, document analysis
- "No access" → Document analysis, assumptions log

---

## Architecture

```
faion-business-analyst (orchestrator)
├── faion-business-analyst:core (21 methodologies)
│   ├── Planning & Governance
│   ├── Elicitation
│   ├── Requirements Lifecycle
│   ├── Strategy Analysis
│   ├── Solution Evaluation
│   └── Modern Practices
└── faion-business-analyst:modeling (7 methodologies)
    ├── Behavioral Models (use cases, user stories)
    ├── Process Models (BPMN)
    ├── Data Models (ERD)
    ├── Decision Models (business rules)
    ├── Interface Models
    └── Validation Models (acceptance criteria)
```

---

## Quick Decision

| If you need... | Sub-Skill | Key File |
|----------------|-----------|----------|
| Define BA approach | ba-core | ba-planning.md |
| Map stakeholders | ba-core | stakeholder-analysis.md |
| Gather requirements | ba-core | elicitation-techniques.md |
| Track/prioritize requirements | ba-core | requirements-traceability.md, requirements-prioritization.md |
| Analyze strategy | ba-core | strategy-analysis.md |
| Evaluate solution | ba-core | solution-assessment.md |
| Model user interactions | ba-modeling | use-case-modeling.md, user-story-mapping.md |
| Map processes | ba-modeling | business-process-analysis.md |
| Model data | ba-modeling | data-analysis.md |
| Define business rules | ba-modeling | decision-analysis.md |
| Design interfaces | ba-modeling | interface-analysis.md |
| Write acceptance criteria | ba-modeling | acceptance-criteria.md |

---

## 6 Knowledge Areas

| # | Knowledge Area | Focus | Sub-Skill |
|---|----------------|-------|-----------|
| 1 | BA Planning & Monitoring | Approach, stakeholders, governance | ba-core |
| 2 | Elicitation & Collaboration | Gather information | ba-core |
| 3 | Requirements Lifecycle | Trace, maintain, prioritize | ba-core |
| 4 | Strategy Analysis | Current/future state, gaps | ba-core |
| 5 | Requirements Analysis & Design | Model, verify, validate | ba-modeling |
| 6 | Solution Evaluation | Measure, assess, improve | ba-core |

---

## Sub-Skills

### faion-business-analyst:core (21 files)
Planning, elicitation, requirements lifecycle, strategy, evaluation, modern practices

**Location:** `~/.claude/skills/faion-business-analyst:core/`

### faion-business-analyst:modeling (7 files)
Use cases, user stories, BPMN, ERD, decision tables, interfaces, acceptance criteria

**Location:** `~/.claude/skills/faion-business-analyst:modeling/`

---

## Navigation

- Main orchestrator: This file
- Detailed overview: [CLAUDE.md](CLAUDE.md)
- Knowledge Areas: [knowledge-areas-detail.md](knowledge-areas-detail.md)
- References: [ref-CLAUDE.md](ref-CLAUDE.md)

---

*BA Domain Skill v3.0 | 28 Methodologies | 2 Sub-Skills | 6 Knowledge Areas*
