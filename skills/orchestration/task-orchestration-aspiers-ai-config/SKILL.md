---
name: task-orchestration
description: Orchestrate the complete development workflow for implementing sub-tasks from a task list. Use for end-to-end feature implementation with quality controls.
---

# Task Orchestration

Orchestrate the complete development workflow for implementing sub-tasks from a task list.

## When to Use This Skill

Use this skill when:
- You need to implement a specific sub-task from a task list
- You want to follow a structured development workflow with quality controls
- Working on features with existing task lists in `.ai/[feature_name]/tasks.md`
- You need to ensure code quality through linting and testing before committing

Don't use this skill:
- When there are no existing task lists
- For ad-hoc code changes without structured task management
- When you need to work on multiple tasks simultaneously

## What This Agent Does

1. **Task Selection**: Identifies and selects the appropriate sub-task from a task list
2. **Implementation**: Uses the task-implementer skill to implement the selected sub-task
3. **Quality Control**: Runs code linters and tests to ensure code quality
4. **Task Management**: Updates task completion status in the task list
5. **Version Control**: Stages and commits changes following proper git workflow
6. **Iterative Process**: Continues with the next incomplete sub-task until all are done

## Task Selection Process

### Command Arguments

- `feature_name` - Locates the relevant task list at `.ai/[feature_name]/tasks.md`
- `subtask_number` - The specific sub-task number to implement

### Selection Logic

1. If `feature_name` is not provided:
   - List all available task lists in `.ai/*/tasks.md`
   - Show feature names as a numbered list
   - Ask user to pick one to work on (excluding completed ones)

2. If `subtask_number` is not provided:
   - Show all unimplemented sub-tasks
   - Identify the first incomplete sub-task
   - Ask user if they want to implement that one, or select another

## Sub-task Completion Protocol

**CRITICAL: Follow this exact sequence. NO EXCEPTIONS!**

1. **Implement**: Use the task-implementer skill to implement the selected sub-task

2. **Lint**: Use the code-linter skill to run all appropriate linters according to repository guidelines

3. **Test**: Use the test-runner skill to run all appropriate tests according to repository guidelines

4. **Fix Issues**: If linting or testing fails, attempt to fix the issues. Do NOT proceed until both pass

5. **Mark Complete**: Update the task list by changing `[ ]` to `[x]` for the completed sub-task. If all sub-tasks under a parent task are complete, also mark the parent task as complete

6. **Stage Changes**: Use the git-stager skill to stage relevant changes, ensuring to include the updated `tasks.md` file

7. **User Review**: Ask the user to review changes and approve with "good" or "vibe". If user responds with "vibe", skip this step for future iterations in the session

8. **Commit**: ONLY after user approval, use the git-committer skill to commit with a proper message

9. **Continue**: Select the next incomplete sub-task and repeat from step 1

## Quality Gates

- **Linting**: All linters must pass before proceeding
- **Testing**: All tests must pass before proceeding
- **User Approval**: Changes must be reviewed and approved before committing
- **Task Tracking**: Task completion must be properly recorded

## Error Handling

- If linting fails: Attempt to auto-fix, then ask user if manual fixes are needed
- If testing fails: Attempt to fix issues, then ask user for guidance
- If user rejects changes: Ask for specific feedback and iterate
- If no more tasks: Inform user that all tasks are complete

## Integration with Other Skills

This orchestrator works closely with:
- `task-implementation` - For actual code implementation
- `code-linting` - For code quality checks
- `test-running` - For test execution
- `git-staging` - For staging changes
- `git-commit` - For creating commits
