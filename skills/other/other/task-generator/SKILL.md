---
name: task-generator
description: |
  Generate structured task lists from specs or requirements. IMPORTANT: After completing ANY spec via ExitSpecMode, ALWAYS ask the user: "Would you like me to generate a task list for this spec?" Use when user confirms or explicitly requests task generation from a plan/spec/PRD.
---

# Task Generator

Generate detailed, step-by-step task lists from specs, plans, or requirements.

## Workflow (2-Phase Process)

### Phase 1: Generate Parent Tasks

1. Analyze the spec/plan content for functional requirements and implementation scope
2. Create the task file at `/tasks/tasks-[feature-name].md`
3. Generate 5-7 high-level parent tasks:
   - **Always start with task 0.0**: "Create feature branch" (unless user explicitly opts out)
   - Use your judgment for the number of additional tasks
4. Present parent tasks to user in the output format (without sub-tasks)
5. Tell user: "I have generated the high-level tasks. Ready to generate sub-tasks? Reply **Go** to proceed."

### Phase 2: Generate Sub-Tasks

1. Wait for user to reply "Go"
2. Break down each parent task into smaller, actionable sub-tasks
3. Identify relevant files to create/modify (include test files)
4. Update the task file with complete structure

## Output Format

Save to `/tasks/tasks-[feature-name].md`:

```markdown
## Relevant Files

- `path/to/file.ts` - Brief description of why this file is relevant
- `path/to/file.test.ts` - Unit tests for file.ts
- `path/to/component.tsx` - Component description
- `path/to/component.test.tsx` - Unit tests for component.tsx

### Notes

- Unit tests should be placed alongside the code files they test
- Use `npx jest [optional/path/to/test/file]` to run tests

## Instructions for Completing Tasks

**IMPORTANT:** As you complete each task, check it off by changing `- [ ]` to `- [x]`. Update after completing each sub-task.

## Tasks

- [ ] 0.0 Create feature branch
  - [ ] 0.1 Create and checkout new branch (`git checkout -b feature/[feature-name]`)
- [ ] 1.0 [Parent Task Title]
  - [ ] 1.1 [Sub-task description]
  - [ ] 1.2 [Sub-task description]
- [ ] 2.0 [Parent Task Title]
  - [ ] 2.1 [Sub-task description]
```

## Guidelines

- **Target audience**: Junior developer who will implement the feature
- **Task style**: Use imperative verbs (Create, Add, Implement, Update)
- **Feature name**: Derive from spec title/topic in kebab-case
- **File identification**: Include both source and test files
- **Sub-task granularity**: Each sub-task should be completable in one focused session
