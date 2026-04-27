---
name: 041-planning-plan-mode
description: Use when creating a plan using Plan model and enhancing structured design plans in Cursor Plan mode for Java implementations. Use when the user wants to create a plan, design an implementation, structure a development plan, or use plan mode for outside-in TDD, feature implementation, or refactoring work. This should trigger for requests such as Create a plan with Cursor Plan mode; Write a plan with Claude Plan mode; Design an implementation plan; Structure a development plan. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java Design Plan Creation for Cursor Plan Mode

Guide the process of creating a structured plan using Cursor Plan mode. **This is an interactive SKILL**. Plans follow a consistent section structure suitable for Java feature implementation, refactoring, or API design.

**What is covered in this Skill?**

- Plan mode workflow: enter Plan mode, gather context, draft plan, iterate
- YAML frontmatter: name, overview, todos, isProject
- Required sections: Requirements Summary, Approach (with Mermaid), Task List, Execution Instructions, File Checklist, Notes
- London Style (outside-in) TDD pattern
- Plan execution discipline: update Status after each task before advancing
- Plan storage: ask user for preferred folder and filename convention before creating artifact

## Constraints

Gather context before drafting. Include Execution Instructions in every plan. Never advance to next task without updating the plan's Status column.

- **MANDATORY**: Run `date` before starting to get date prefix for plan filename
- **MUST**: Read the reference template fresh—do not use cached content
- **MUST**: Ask one or two questions at a time; never all at once
- **MUST**: Validate summary (Does this capture what you need?) before proposing plan creation
- **MUST**: Wait for user to confirm proceed before generating the plan
- **MUST**: Ask the user where they want to store the plan before generating the plan artifact
- **MUST**: Include Execution Instructions section in every generated plan

## When to use this skill

- Create a plan with Cursor Plan mode
- Write a plan with Claude Plan mode
- Design an implementation plan
- Structure a development plan
- Create a structured design plan
- Refactor the plan
- Improve the plan
- Update the plan

## Workflow

0. **Get current date**

Run `date` before planning and use it to derive the plan filename prefix `YYYY-MM-DD`.

1. **Read reference and gather context**

Read `references/041-planning-plan-mode.md` and ask one or two questions at a time to clarify requirements, constraints, and target scope.

2. **Validate summary and confirm proceed**

Summarize understanding, ask Does this capture what you need?, and wait for explicit proceed before creating the plan artifact.

3. **Confirm plan storage location**

Ask where the user wants to store the plan (for example, `.cursor/plans/` or another folder) and confirm the target filename pattern before writing.

4. **Generate structured plan artifact**

Create the plan at the confirmed location using required sections and YAML frontmatter, including Execution Instructions.

5. **Apply execution discipline**

When executing tasks from the plan, update the Status column after each task before moving to the next one.

## Reference

For detailed guidance, examples, and constraints, see [references/041-planning-plan-mode.md](references/041-planning-plan-mode.md).
