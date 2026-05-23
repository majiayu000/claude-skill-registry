---
name: task-implementation
description: Implement a single sub-task from a task list. Use when working on feature development with existing task lists.
---

# Task Implementation

Implement a single sub-task from a task list while adhering to project quality controls.

## When to Use This Skill

Use this skill when:
- Working on feature development with existing task lists in `.ai/[feature_name]/tasks.md`
- Implementing a specific sub-task assigned to you
- Following a structured development workflow

## Input

This skill expects:
1. `feature_name` - Locates task list at `.ai/[feature_name]/tasks.md`
2. `subtask_number` - The specific sub-task number to implement

If not provided, ask the user to clarify.

## Approach

You are a junior engineer implementing a sub-task. Do your best to ensure
the implementation adheres to the project's quality controls. Run linters
and tests appropriately during iterative development.

## Prohibited Actions

**IMPORTANT! You must NOT attempt to commit or even stage your changes in git,
as that will be handled elsewhere.**

While you can update details in the task list as you work, **you must NOT mark
tasks as completed**. It is not your responsibility to judge whether a task
is completed.

## Process

**Follow these steps EXACTLY! NO EXCEPTIONS!**

1. **Implement** the sub-task according to your best judgment

2. **Add test coverage** according to repository guidelines

3. **Run linters** according to repository guidelines:
   - First look for linting commands in: `CLAUDE.md`, `.cursorrules`,
     `AGENTS.md`, `AGENT.md`, `GEMINI.md`
   - Then repository documentation (`README.md`, `docs/`)
   - Then package configuration (`package.json`, `Makefile`, etc.)
   - Then standard linter patterns
   
   For each linter found:
   a. Run auto-fix mode if available (e.g., `prettier`, `eslint --fix`)
   b. Run check mode to see remaining issues
   c. If issues can't be fixed, stop and ask the user what to do next
   
   If not passing, go back to step 1.

4. **Run tests** according to repository guidelines:
   - Look for test commands in documentation, package config, or standard patterns
   - For each test command found: run it, fix issues if possible, ask user if not
   
   If not passing, go back to step 1.

## Context Maintenance

- Update details in the task list as you work
- **Do NOT mark tasks as completed**
- Add new tasks if they emerge during implementation
- Update the corresponding `prp.txt` if appropriate
- Maintain the "Relevant Files" section:
  - List every file created or modified
  - Give each file a one-line description of its purpose

## Quality Gates

Before considering the sub-task complete:
- [ ] Implementation matches the sub-task description
- [ ] Linting passes (auto-fixable issues resolved)
- [ ] Tests pass (100% success)
- [ ] Code follows project conventions
