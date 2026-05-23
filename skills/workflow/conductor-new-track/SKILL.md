---
version: 4.1.0-fractal
name: conductor-new-track
description: Create a new track with specification and phased implementation plan
metadata:
  argument-hint: <feature|bug|chore|refactor> <name>
---

# New Track

Create a new track (feature, bug fix, chore, or refactor) with a detailed specification and phased implementation plan.

## Use this skill when

- Working on new track tasks or workflows
- Needing guidance, best practices, or checklists for new track

## Do not use this skill when

- The task is unrelated to new track
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Pre-flight Checks

1. Verify Conductor is initialized:
   - Check `conductor/product.md` exists
   - Check `conductor/tech-stack.md` exists
   - Check `conductor/workflow.md` exists
   - If missing: Display error and suggest running `/conductor:setup` first

2. Load context files:
   - Read `conductor/product.md` for product context
   - Read `conductor/tech-stack.md` for technical context
   - Read `conductor/workflow.md` for TDD/commit preferences

## Track Classification

Determine track type based on description or ask user:

```
What type of track is this?

1. Feature - New functionality
2. Bug - Fix for existing issue
3. Chore - Maintenance, dependencies, config
4. Refactor - Code improvement without behavior change
```

## Interactive Specification Gathering

**CRITICAL RULES:**

- Ask ONE question per turn
- Wait for user response before proceeding
- Tailor questions based on track type
- Maximum 6 questions total

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [For Feature Tracks](./sub-skills/for-feature-tracks.md)
### 2. [For Bug Tracks](./sub-skills/for-bug-tracks.md)
### 3. [For Chore/Refactor Tracks](./sub-skills/for-chorerefactor-tracks.md)
### 4. [Plan Structure](./sub-skills/plan-structure.md)
### 5. [Tasks](./sub-skills/tasks.md)
### 6. [Verification](./sub-skills/verification.md)
### 7. [Tasks](./sub-skills/tasks.md)
### 8. [Verification](./sub-skills/verification.md)
### 9. [Phase Guidelines](./sub-skills/phase-guidelines.md)
