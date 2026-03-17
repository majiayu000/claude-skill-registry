---
name: implementation-planner
description: Generate technical design and tasks from feature spec. Triggers on "implement FEAT-XXX", "plan implementation for FEAT-XXX", "create implementation plan for FEAT-XXX". Works in Claude plan mode or normal mode.
globs: ["docs/features/**/spec.md", "docs/features/**/design.md", "docs/features/**/tasks.md", "docs/features/**/status.md"]
---

# Implementation Planner

Transform a feature specification into actionable technical design and tasks.

## Triggers

- "implement FEAT-XXX" (in plan mode or normal)
- "plan implementation for FEAT-XXX"
- "create implementation plan for FEAT-XXX"
- "generate tasks for FEAT-XXX"
- "create technical design for FEAT-XXX"

## Prerequisites

- Feature folder must exist: `docs/features/FEAT-XXX/`
- `spec.md` must be completed (interview done)
- `analysis.md` should exist (think critically done)
- If spec incomplete: "Let's first interview about this feature"

## Purpose

Create:
1. **design.md** - Technical architecture for the feature
2. **tasks.md** - Granular, actionable implementation tasks
3. Update **status.md** - Mark phase as "Plan complete"

## Process

### 1. Read Context

```bash
# Read feature spec
cat docs/features/FEAT-XXX/spec.md

# Read analysis (from Think Critically phase)
cat docs/features/FEAT-XXX/analysis.md

# Read project architecture for consistency
cat docs/architecture/_index.md 2>/dev/null

# Read project context
cat docs/project.md 2>/dev/null

# Check current status
cat docs/features/FEAT-XXX/status.md
```

### 2. Generate design.md

Based on spec.md and analysis.md, create technical design covering:

**Required sections:**
- Overview (brief technical approach)
- Architecture (ASCII diagram + components table)
- Data Model (models, relationships)
- API Design (endpoints, request/response examples)
- Service Layer (services, business logic)
- Error Handling (error cases, responses)
- Security Considerations
- Performance Considerations
- Dependencies (external + internal)
- File Structure (new files + modified files)
- Implementation Order

### 3. Generate tasks.md

Break design into granular, actionable tasks:

**Task rules:**
- Each task = 15-60 minutes of work
- Each task = ONE commit
- Tasks ordered by dependency
- Each task starts with a verb (Create, Add, Implement, Update, Test)
- Each task has clear "done" criteria

### 4. Update status.md

**CRITICAL: Always update status after generating plan**

### 5. Update Global Status

**CRITICAL: Update docs/features/_index.md**

### 6. Completion Message

After generating plan:

```
Implementation plan created for FEAT-XXX

Generated:
- docs/features/FEAT-XXX/design.md (technical design)
- docs/features/FEAT-XXX/tasks.md (X tasks)

Updated:
- docs/features/FEAT-XXX/status.md (Phase: Plan complete)
- docs/features/_index.md (global status)

Next steps:
1. Create branch: git checkout -b feature/XXX-name
2. Start implementation: "Execute FEAT-XXX tasks"
   Or fork for parallel: /fork-feature FEAT-XXX full
```
