---
name: faion-project-bootstrap
user-invocable: false
description: "Full project bootstrap: idea → constitution → TASK_000. Triggers: bootstrap, new project."
allowed-tools: Read, Write, Edit, Glob, Bash(ls:*), Bash(mkdir:*), AskUserQuestion
---

# Project Bootstrap

**Communication: User's language. Docs: English.**

## Pipeline

```
IDEA → CONCEPT → TECH STACK → MVP SCOPE → CONFIRMATION → BACKLOG → CONSTITUTION → TASK_000
```

## Output

```
aidocs/sdd/{project}/
├── constitution.md
├── roadmap.md
└── features/
    ├── backlog/{NN}-{feature}/spec.md
    └── 00-setup/tasks/todo/TASK_000_project_setup.md
```

## Phases

### Phase 1: Vision Brainstorm

Ask: "Розкажи про проект"

Apply **Five Whys** to get to real need. Clarify: target users, core problem, unique angle.

### Phase 2: Tech Stack

```python
AskUserQuestion([
    {"question": "Frontend?", "options": [
        {"label": "React + TypeScript"},
        {"label": "Next.js"},
        {"label": "None (API only)"}
    ]},
    {"question": "Backend?", "options": [
        {"label": "Python + Django"},
        {"label": "Python + FastAPI"},
        {"label": "Go"},
        {"label": "Node.js"}
    ]},
    {"question": "Database?", "options": [
        {"label": "PostgreSQL"},
        {"label": "SQLite"},
        {"label": "MongoDB"}
    ]}
])
```

### Phase 3: MVP Definition

Use agent: `faion-mvp-scope-analyzer-agent`

Rules: Max 3-5 features, each solves a problem, cut 50% nice-to-haves.

### Phase 4: Confirmation (MANDATORY!)

```
**Проект:** {name}
**Проблема:** {problem}
**Tech:** {stack}
**MVP Features:** 1. ... 2. ... 3. ...
Все вірно?
```

### Phase 5: Backlog

For each feature → `backlog/{NN}-{name}/spec.md`:

```markdown
# {Feature}
## Problem
## User Stories
## Requirements (FR-{NN}.X)
## Acceptance Criteria (AC-{NN}.X)
```

### Phase 6: Constitution

Create `constitution.md` — identity, architecture, standards, testing, CI/CD.

Template: `templates/CONSTITUTION_TEMPLATE.md`

### Phase 7: TASK_000

Setup task with goals: init project, dev env, CI/CD, structure.

Templates: `templates/TASK_000_{stack}.md`

## Numbering

- Features: `{NN}-{name}` (00, 01, 02)
- Tasks: `TASK_{NNN}_*`
- Requirements: `FR-{NN}.{N}`
- Criteria: `AC-{NN}.{N}`

## After Bootstrap

Offer: "Виконати TASK_000?" → execute via faion-execute-task
