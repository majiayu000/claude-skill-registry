---
name: faion-backlog-grooming
description: "SDD Backlog Grooming - prioritize features, refine specs, create designs and tasks"
user-invocable: false
argument-hint: "[project-name]"
allowed-tools: Read, Write, Edit, Glob, Grep, Task, AskUserQuestion, TodoWrite
---

# SDD: Backlog Grooming

**Communication: User's language. Docs: English.**

## Purpose

Interactive grooming session: prioritize → refine spec → create design → generate tasks.

## Pipeline

```
READ BACKLOG → PRIORITIZE → SELECT FEATURE → REFINE SPEC → CREATE DESIGN → GENERATE TASKS → MOVE TO TODO
```

## Phase 1: Load Context

Read: `roadmap.md`, `constitution.md`
List features by status: backlog, todo, in-progress, done

## Phase 2: Display Status

```markdown
## 📊 Feature Status

### 🚧 In Progress (n)
- feature — summary

### 📋 Todo (n)
- feature — summary

### 📝 Backlog (n)
- feature — summary [P0/P1/P2]
```

## Phase 3: Action Selection

AskUserQuestion: "Що хочеш зробити?"
1. Переглянути пріоритети
2. Взяти фічу в роботу
3. Додати нову фічу
4. Видалити фічу
5. Завершити grooming

## Phase 4: Feature Selection

Show backlog with: Name, Spec status, Design status, Dependencies

```markdown
| # | Feature | Spec | Design | Dependencies |
|---|---------|------|--------|--------------|
| 1 | auth | ✅ | ❌ | none |
| 2 | transactions | ✅ | ❌ | auth |
```

## Phase 5: Spec Refinement

If no spec or needs update:
- Show existing spec
- Ask clarifying questions
- Call `faion-writing-specifications` if needed

## Phase 6: Design Creation

If spec approved:
- Call `faion-writing-design-docs`
- Present for review

## Phase 7: Task Generation

If design approved:
- Call `faion-writing-implementation-plan`
- Call `faion-task-creator-agent` for each task
- Present tasks for review

## Phase 8: Move to Todo

If approved:
```bash
mv features/backlog/{feature}/ features/todo/{feature}/
```

Report: "✅ Фіча готова! /faion-execute-task {project}/{feature} TASK_001"

## Feature Lifecycle

```
backlog/ → todo/ → in-progress/ → done/
   ↓         ↓           ↓           ↓
spec.md  +design.md  executing    archived
         +impl-plan
         +tasks/
```

## Integration

Called from `/faion-net` or directly.
Calls: faion-writing-specifications, faion-writing-design-docs, faion-writing-implementation-plan, faion-task-creator-agent

## Anti-patterns

- ❌ Skip spec refinement
- ❌ Create tasks without design
- ❌ Move to todo without all artifacts
- ❌ Take feature with unsatisfied dependencies
