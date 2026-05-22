---
name: refactor-plan
description: Create structured refactoring plans. Use when user wants to plan a refactor, needs a refactoring strategy, or mentions breaking down large changes into small commits.
---

# Refactor Planning

## Process

### 1. Understand Problem
- Get detailed description from user
- Ask about potential solutions they've considered
- Explore codebase to verify current state

### 2. Define Scope
- Interview user about implementation details
- Present alternative approaches
- Define exactly what changes and what stays
- Check test coverage in affected areas

### 3. Break Down Work
Apply Martin Fowler's principle: "Make each refactoring step as small as possible, so that you can always see the program working."

- Create list of tiny commits
- Each commit leaves codebase working
- Sequential, not parallel changes

### 4. Create GitHub Issue
Use `gh issue create` with template (see `template.md`)

Include:
- Problem statement
- Solution approach
- Detailed commit plan
- Implementation decisions
- Testing strategy
- Out of scope items

## Rules

- Each commit must keep codebase functional
- No implementation details in plan (focus on behavior)
- Verify test coverage before starting
- Get user approval on approach
