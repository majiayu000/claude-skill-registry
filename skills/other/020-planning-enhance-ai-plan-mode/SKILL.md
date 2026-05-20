---
name: 020-planning-enhance-ai-plan-mode
description: Use when creating a plan using Plan model and enhancing structured design plans in Cursor Plan mode for Java implementations. Use when the user wants to create a plan, design an implementation, structure a development plan, or use plan mode for outside-in TDD, feature implementation, or refactoring work. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.13.0-SNAPSHOT
---
# Java Design Plan Creation for Cursor Plan Mode

Guide the process of creating a structured plan using Cursor Plan mode. **This is an interactive SKILL**. Plans follow a consistent section structure suitable for Java feature implementation, refactoring, or API design.

**What is covered in this Skill?**

- Plan mode workflow: enter Plan mode, gather context, draft plan, iterate
- YAML frontmatter: name, overview, todos, isProject
- Required sections: Requirements Summary, Approach (with Mermaid), Task List, Execution Instructions, File Checklist, Notes
- London Style (outside-in) TDD pattern
- Plan execution discipline: update Status after each task before advancing
- Plan file path: .cursor/plans/YYYY-MM-DD_&lt;name&gt;.plan.md

## Constraints

Gather context before drafting. Include Execution Instructions in every plan. Never advance to next task without updating the plan's Status column.

- **MANDATORY**: Run `date` before starting to get date prefix for plan filename
- **MUST**: Read the reference template fresh—do not use cached content
- **MUST**: Ask one or two questions at a time; never all at once
- **MUST**: Validate summary ("Does this capture what you need?") before proposing plan creation
- **MUST**: Wait for user to confirm "proceed" before generating the plan
- **MUST**: Include Execution Instructions section in every generated plan

## When to use this skill

- Create a plan with Cursor Plan mode
- Write a plan with Claude Plan mode

## Reference

For detailed guidance, examples, and constraints, see [references/020-planning-enhance-ai-plan-mode.md](references/020-planning-enhance-ai-plan-mode.md).
