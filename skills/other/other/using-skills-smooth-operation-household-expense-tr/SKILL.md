---
name: using-skills
description: "Check for relevant skills before starting any task"
---

# Using CodeAssist Skills

## Core Principle

Before starting a task, check if any skills apply. Skills are documented best practices that help you work more effectively.

## First Response Protocol

For each request:

1. **Check**: Review available skills in `.claude/skills/`
2. **Read**: If a skill applies, read the skill file
3. **Announce**: State which skill you're using
   - Example: "I'm using the code-review skill to review these changes"
4. **Follow**: Execute the skill's protocol

## Why Use Skills

Skills represent tested approaches that:
- Provide consistent patterns across projects
- Include important safety checks
- Prevent common mistakes
- Save time by avoiding rework

## Skill Categories

### Core Workflow
- `brainstorming` - Discuss approach before implementation
- `writing-plans` - Break work into tasks
- `executing-plans` - Execute with verification
- `code-review` - Review before completing

### Safety
- `database-backup` - Backup before database operations
- `verification-before-completion` - Final checks before declaring done

### Testing
- `test-driven-development` - Write tests first
- `condition-based-waiting` - Avoid flaky tests
- `testing-anti-patterns` - Common mistakes to avoid

### Workflow
- `git-workflow` - Branching and commits
- `git-worktrees` - Parallel development

## Skill Discovery

| Task | Relevant Skills |
|------|-----------------|
| Starting a new feature | brainstorming → writing-plans |
| Running tests/migrations | database-backup |
| Adding functionality | test-driven-development |
| Finishing work | code-review → verification-before-completion |
| Multiple features | git-worktrees |

## Tips

- Read the skill file rather than relying on memory
- Announce which skill you're using for transparency
- Follow the skill's checklist if it has one
- Skills work best when used consistently

## Full Skills Index

See `.claude/skills/README.md` for the complete list of available skills.
