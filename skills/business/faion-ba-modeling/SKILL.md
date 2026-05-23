---
name: faion-ba-modeling
user-invocable: false
description: "BA Modeling: Use cases, user stories, process models (BPMN), data models, decision tables, interfaces, acceptance criteria. 7 methodologies."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---

# BA Modeling Sub-Skill

**Parent:** faion-business-analyst
**Focus:** Requirements analysis and design modeling techniques

---

## Context Discovery

### Auto-Investigation

| Signal | Check For | Why |
|--------|-----------|-----|
| `.md` files with scenarios | Use case patterns (Actor, Precondition, Main Flow) | Use case modeling in use |
| `*.bpmn` or process diagrams | BPMN process models | Process analysis present |
| `user-stories/` or backlog | User story format | Agile modeling approach |
| Database schema files | ERD or data models | Data modeling needed |
| `acceptance-criteria/` | Given-When-Then format | BDD approach |

### Discovery Questions

```yaml
questions:
  - question: "What type of system are you modeling?"
    options:
      - label: "Business processes"
        description: "Use business-process-analysis (BPMN)"
      - label: "User interactions"
        description: "Use use-case-modeling or user-story-mapping"
      - label: "Data structures"
        description: "Use data-analysis (ERD)"
      - label: "Complex logic/rules"
        description: "Use decision-analysis"

  - question: "What's your development methodology?"
    options:
      - label: "Agile/iterative"
        description: "Favor user-story-mapping, acceptance-criteria"
      - label: "Waterfall/formal"
        description: "Favor use-case-modeling, detailed docs"

  - question: "Are you defining system interfaces/APIs?"
    options:
      - label: "Yes, integration requirements"
        description: "Use interface-analysis"
      - label: "No, internal logic only"
        description: "Skip interface analysis"
```

---

## Methodologies (7)

### Behavioral Models (2)
- use-case-modeling.md - User-system interactions, detailed flows
- user-story-mapping.md - Agile user stories, story mapping

### Process Models (1)
- business-process-analysis.md - BPMN, process flows, swimlanes

### Data Models (1)
- data-analysis.md - ERD, data requirements, data dictionary

### Decision Models (1)
- decision-analysis.md - Decision tables, business rules

### Interface Models (1)
- interface-analysis.md - System interfaces, API requirements

### Validation Models (1)
- acceptance-criteria.md - Given-When-Then, BDD, definition of done

---

## When to Use

| If you need... | Methodology |
|----------------|-------------|
| Model user interactions | use-case-modeling |
| Create agile user stories | user-story-mapping |
| Map business processes | business-process-analysis |
| Define data structures | data-analysis |
| Model business rules | decision-analysis |
| Define system interfaces | interface-analysis |
| Write acceptance criteria | acceptance-criteria |

---

## Modeling Technique Selection

| Context | Use |
|---------|-----|
| Detailed functional requirements | Use Case Modeling |
| Agile/iterative development | User Story Mapping |
| Process improvement | Business Process Analysis |
| Database design | Data Analysis |
| Complex business logic | Decision Analysis |
| Integration requirements | Interface Analysis |
| Test preparation | Acceptance Criteria |

---

*BA Modeling Sub-Skill v1.0*
