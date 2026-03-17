---
name: planning
description: Break features into phased implementation plans. Triggers on "plan", "break down", "phase", "roadmap".
---

# Planning

A structured workflow for breaking features or projects into phased, actionable plans.

## When to Use

- Large features that span multiple pages or components
- Redesigns or major refactors
- New sections with unclear scope
- When the user asks "how should we approach this?"

## When NOT to Use

- Single-component tasks
- Bug fixes
- Simple content updates

## Core Principles

- Break work into shippable increments
- Each phase should be independently deployable
- Identify dependencies between phases
- Estimate relative complexity (S/M/L)

## The 6 Phases

### Phase 1: Discovery

**Goal**: Understand the full scope.

1. Read the user's request and any reference materials
2. Identify all deliverables
3. List assumptions and open questions

### Phase 2: Exploration

**Goal**: Understand what exists.

1. Survey the current codebase structure
2. Identify reusable components and patterns
3. Note technical constraints (stack, dependencies)
4. Check for similar implementations to reference

### Phase 3: Questions

**Goal**: Resolve ambiguity.

1. List open questions (max 5)
2. Propose defaults for minor decisions
3. Confirm priorities and must-haves vs. nice-to-haves

### Phase 4: Plan Design

**Goal**: Structure the work into phases.

1. Group deliverables into logical phases
2. Order phases by dependency and priority
3. Identify shared components to build first
4. Estimate complexity per phase (S/M/L)

### Phase 5: Plan Output

**Goal**: Produce the actionable plan.

**Format**:

```markdown
# Implementation Plan: [Feature Name]

## Overview
[1-2 sentence summary]

## Phases

### Phase 1: [Name] (Size: S/M/L)
**Goal**: [What this achieves]
**Files**:
- [ ] `path/to/file.tsx` — [what to do]
**Dependencies**: None

### Phase 2: [Name] (Size: S/M/L)
**Goal**: [What this achieves]
**Files**:
- [ ] `path/to/file.tsx` — [what to do]
**Dependencies**: Phase 1

## Shared Components
- [Component]: [used in phases X, Y]

## Risks
- [risk]: [mitigation]
```

### Phase 6: Summary

**Goal**: Confirm the plan with the user.

1. Present the plan
2. Ask for approval or adjustments
3. Identify which phase to start with

## Related Skills

| Skill | When to Chain |
|-------|--------------|
| feature-dev | After planning, to implement each phase |
| web-test | After each phase, to verify |
