---
name: spec-driven-workflow-skill
description: Follow spec-driven development (constitution → spec → plan → tasks → implement)
when-to-use: Any new feature development
---
# Spec-Driven Workflow Skill

## Instructions

This skill provides guidance for following the Spec-Driven Development (SDD) workflow used in this project.

### SDD Workflow Overview

```
1. CONSTITUTION    → Define project principles and values
2. SPEC            → Create feature specification
3. PLAN            → Design architecture and tech stack
4. TASKS           → Break down into testable tasks
5. IMPLEMENT       → Code with test-driven approach
   - RED   → Write failing tests
   - GREEN → Write minimal code to pass
   - REFACTOR → Improve code quality
6. POLISH         → Finalize and document
```

### Project Structure

```
.specify/
├── memory/
│   └── constitution.md    # Project principles
├── templates/
│   ├── spec-template.md
│   ├── plan-template.md
│   ├── tasks-template.md
│   ├── adr-template.md
│   └── phr-template.prompt.md
└── scripts/
    ├── bash/
    └── powershell/

specs/
└── <feature-name>/
    ├── spec.md            # Feature requirements
    ├── plan.md            # Architecture decisions
    ├── tasks.md           # Implementation tasks
    ├── data-model.md      # Entities and relationships
    ├── research.md        # Technical decisions
    ├── quickstart.md      # Integration scenarios
    └── checklists/
        └── requirements.md # Acceptance criteria

history/
├── prompts/
│   ├── constitution/
│   ├── <feature-name>/
│   └── general/
└── adr/
    └── <decision-title>.md
```

### Step 1: Constitution

**When:** Project initialization or fundamental principle changes

The constitution defines project values. Reference it when:
- Making architectural decisions
- Setting code quality standards
- Defining security requirements

```markdown
.constitution/memory/constitution.md contains:
- Code quality standards
- Testing requirements
- Performance budgets
- Security principles
- Architecture guidelines
```

### Step 2: Create Feature Specification

**Command:** `/sp.specify` or `sp.specify`

```markdown
# spec.md template

## Feature Overview
- **Name**: Feature name
- **Description**: Brief description
- **Goals**: What we want to achieve
- **Out of Scope**: What's excluded

## User Stories
As a [role], I want [capability], so that [benefit].

## Requirements
### Functional
1. Must have...
2. Should have...
3. Could have...

### Non-Functional
- Performance: p95 latency < 200ms
- Availability: 99.9% uptime
- Security: OAuth2 + JWT

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### Step 3: Create Architecture Plan

**Command:** `/sp.plan` or `sp.plan`

```markdown
# plan.md template

## Tech Stack
- **Frontend**: Next.js 14, TypeScript, Tailwind
- **Backend**: FastAPI, Python 3.11+
- **Database**: Neon PostgreSQL, SQLModel
- **Auth**: Better Auth, JWT
- **AI**: OpenAI, Groq

## Architecture
[Diagrams and component descriptions]

## File Structure
```
src/
app/
backend/
```

## API Contracts
### POST /api/v1/tasks
- Input: TaskCreate
- Output: TaskResponse
- Errors: 400, 401, 404
```

### Step 4: Create Tasks

**Command:** `/sp.tasks` or `sp.tasks`

```markdown
# tasks.md template

## Phase: Setup
- [ ] Task 1
- [ ] Task 2

## Phase: Tests
- [ ] Task 3
- [ ] Task 4

## Phase: Core
- [ ] Task 5
- [ ] Task 6

## Phase: Integration
- [ ] Task 7

## Phase: Polish
- [ ] Task 8
```

### Step 5: Implement

**Command:** `/sp.implement` or `sp.implement`

Follow TDD approach:

#### RED Phase - Write Failing Tests
```python
# tests/test_tasks.py
import pytest
from datetime import datetime

def test_create_task_requires_title():
    """Task must have a title."""
    with pytest.raises(ValueError):
        Task(title="", description="Test")

def test_task_defaults_to_incomplete():
    """New tasks should be incomplete by default."""
    task = Task(title="Test Task")
    assert task.completed is False
```

#### GREEN Phase - Write Minimal Code
```python
# backend/models/task.py
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1)
    completed: bool = Field(default=False)
```

#### REFACTOR Phase - Improve Code
- Extract constants
- Add type hints
- Optimize performance
- Improve readability

### Step 6: Polish

- Run full test suite
- Check linting and formatting
- Update documentation
- Create quickstart guide
- Verify against requirements

## Using SDD Commands

### Available Commands

| Command | Purpose | Stage |
|---------|---------|-------|
| `/sp.specify` | Create feature spec | spec |
| `/sp.plan` | Design architecture | plan |
| `/sp.tasks` | Break into tasks | tasks |
| `/sp.implement` | Execute tasks | implement |
| `/sp.analyze` | Check consistency | any |
| `/sp.checklist` | Generate checklist | any |
| `/sp.clarify` | Ask clarifying questions | spec |
| `/sp.adr` | Document architecture decision | plan |
| `/sp.phr` | Create prompt history record | any |
| `/sp.git.commit_pr` | Commit and create PR | polish |

### Quick Start for New Feature

```bash
# 1. Create specification
/sp.specify

# 2. Design plan
/sp.plan

# 3. Generate tasks
/sp.tasks

# 4. Implement
/sp.implement

# 5. Document decision if significant
/sp.adr "decision-title"
```

## Examples

### Example: Adding a New Feature

1. **Define the feature** (conversation with product owner)

2. **Create specification**
```markdown
# Feature: Task Labels
## Goal
Allow users to organize tasks with color-coded labels

## Requirements
- Create, edit, delete labels
- Assign multiple labels to tasks
- Filter tasks by label

## API
POST /api/v1/labels
GET /api/v1/labels
POST /api/v1/tasks/{id}/labels
```

3. **Plan architecture**
```markdown
## Label Model
- id, name, color, user_id
- Many-to-many with tasks

## API Design
- RESTful endpoints
- Validation with Pydantic
- Auth required
```

4. **Create tasks**
```
## Phase: Core
- [ ] Create Label SQLModel
- [ ] Create Label CRUD routes
- [ ] Create label-task association

## Phase: Tests
- [ ] Test label CRUD
- [ ] Test task-label relationship

## Phase: Integration
- [ ] Add to frontend task view
```

5. **Implement**
```python
# backend/models/label.py
class Label(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    color: str
    user_id: int = Field(foreign_key="users.id")
```

6. **Validate**
```bash
pytest tests/
npm run lint
```

### Decision Recording (ADR)

When making significant decisions:

```markdown
# ADR: Label Color Storage Format

## Status
Accepted

## Context
Need to store label colors for the new labels feature.

## Decision
Use hex color string (e.g., "#FF5733") with validation.

## Consequences
### Positive
- Simple storage (string)
- Flexible color selection
- Easy to serialize/display

### Negative
- No color picker constraints
- Users can enter invalid colors (validated)

## Alternatives Considered
- PostgreSQL citext: More complex, no benefit
- ENUM: Inflexible, requires migration
```

## Quality Gates

Before moving to next phase:
- [ ] All tests pass
- [ ] Code follows constitution
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] Performance within budget

## Prompt History Records (PHRs)

Every significant interaction is recorded:

```
history/prompts/
├── constitution/
│   └── 001-create-constitution.constitution.prompt.md
├── todo-app/
│   └── 001-create-spec.spec.prompt.md
└── general/
    └── 001-question.general.prompt.md
```

PHRs capture:
- Full user prompt
- Assistant response
- Files created/modified
- Tests run
- Model used
- Links to specs/ADRs
