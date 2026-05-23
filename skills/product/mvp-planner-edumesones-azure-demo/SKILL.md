---
name: mvp-planner
description: Define and prioritize MVP features. Triggers on "Define MVP features", "Help me plan the MVP", "What features for MVP", "Let's define the features".
globs: ["docs/project.md", "docs/features/**"]
---

# MVP Planner (Fase 0)

Transform project vision into concrete, prioritized features ready for implementation.

## Triggers

- "Define MVP features"
- "Help me plan the MVP"
- "What features should we build?"
- "Let's define the features"
- "Plan the MVP"
- `/mvp`

## Prerequisites

- `docs/project.md` should exist
- `docs/architecture/_index.md` ideally exists
- If not: "Let's first define the project and architecture"

## Purpose

Create:
1. **Prioritized feature list** in `docs/features/_index.md`
2. **Feature folders** for top 3-5 MVP features
3. **Clear scope** of what's in/out of MVP

## Process

### 1. Read Context

```bash
# Read project definition
cat docs/project.md

# Read architecture (if exists)
cat docs/architecture/_index.md 2>/dev/null

# Check existing features
ls -la docs/features/ 2>/dev/null
```

### 2. Extract Core Value

From project.md, identify:
- What's the ONE thing that makes this valuable?
- What's the minimum a user needs to get value?
- What can wait until v1.1?

### 3. Feature Brainstorm Interview

```
"Based on your project, I see these potential features:

CORE (likely MVP):
1. [Feature] - [Why it's core]
2. [Feature] - [Why it's core]
3. [Feature] - [Why it's core]

IMPORTANT (maybe MVP):
4. [Feature] - [Value add]
5. [Feature] - [Value add]

NICE TO HAVE (post-MVP):
6. [Feature] - [Can wait because...]
7. [Feature] - [Can wait because...]

Questions:
1. Did I miss any critical features?
2. Which of the 'important' ones are must-have for launch?
3. Anything in 'core' that could actually wait?"
```

### 4. Prioritization Framework

Use MoSCoW or similar:

| Priority | Meaning | MVP? |
|----------|---------|------|
| **Must** | Won't work without it | Yes |
| **Should** | Important but workaround exists | Maybe |
| **Could** | Nice to have | No |
| **Won't** | Explicitly out of scope | No |

### 5. Interview Rules

```
MVP PLANNING RULES

1. Ruthlessly cut scope
   "Can you launch without this? Yes? -> Post-MVP"

2. Maximum 5 features for MVP
   More than 5 = you're not building an MVP

3. Each feature must have clear "done" criteria
   "User can X" not "Implement X"

4. Identify dependencies early
   Which features block others?

5. Time-box the MVP
   "If it takes more than X weeks, we're doing too much"

6. The first feature should prove the core value
   Start with what makes this product unique
```

### 6. Create Feature Folders

After prioritization, create each MVP feature:

```
For each MVP feature:
1. Create folder: docs/features/FEAT-00X-name/
2. Copy templates from docs/features/_template/
3. Pre-fill spec.md with scope from this discussion
4. Update status.md to "Pending - Spec needed"
```

### 7. Handoff

When complete:

```
MVP planned. Created:
- docs/features/_index.md (dashboard)
- docs/features/FEAT-001-[name]/ (folder + templates)
- docs/features/FEAT-002-[name]/ (folder + templates)
- docs/features/FEAT-003-[name]/ (folder + templates)

Recommended order:
1. FEAT-001 - [name] (no dependencies)
2. FEAT-002 - [name] (depends on FEAT-001)
3. FEAT-003 - [name] (depends on FEAT-001, FEAT-002)

Next step:
"Interview me about FEAT-001-[name]" -> Deep dive into first feature spec

Or: /interview FEAT-001-[name]
```
