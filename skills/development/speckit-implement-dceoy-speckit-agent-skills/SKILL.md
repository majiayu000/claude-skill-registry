---
name: speckit-implement
description: Execute the implementation plan by processing and executing all tasks defined in tasks.md
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Spec-Kit Implement

Execute the implementation by processing tasks from tasks.md in phases. Fourth step in spec-kit workflow.

## When to Use

- After creating tasks.md with `speckit-tasks`
- Ready to start implementation
- Want to execute tasks systematically

## Execution Workflow

1. **Setup**: Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` to get FEATURE_DIR and AVAILABLE_DOCS
2. **Check checklists status** (if FEATURE_DIR/checklists/ exists):
   - **VALIDATION GATE**: Scan all checklist files and count total, completed, incomplete items
   - Create status table showing pass/fail for each checklist
   - **If any checklist incomplete**: STOP and ask user if they want to proceed anyway
     - User must explicitly approve to continue
   - **If all complete**: Automatically proceed to implementation
3. **Load implementation context**:
   - **REQUIRED**: tasks.md (complete task list), plan.md (tech stack, architecture)
   - **IF EXISTS**: data-model.md, contracts/, research.md, quickstart.md
4. **Project setup verification**:
   - Create/verify ignore files based on actual project setup (gitignore, dockerignore, eslintignore, etc.)
   - Detect technology from plan.md and add appropriate patterns
   - Only append missing critical patterns to existing ignore files
5. **Parse tasks.md structure**:
   - Extract task phases, dependencies, details (ID, description, file paths)
   - Identify parallel markers `[P]` and sequential vs parallel execution rules
6. **Execute implementation** following task plan:
   - Phase-by-phase execution (complete each phase before next)
   - Respect dependencies (sequential tasks in order, parallel tasks `[P]` can run together)
   - Follow TDD approach if tests exist (execute test tasks before implementation)
   - File-based coordination (tasks on same files run sequentially)
   - Validation checkpoints after each phase
7. **Implementation execution order**:
   - Setup first (initialize structure, dependencies, configuration)
   - Tests before code (if test tasks exist)
   - Core development (models, services, CLI commands, endpoints)
   - Integration work (database, middleware, logging, external services)
   - Polish and validation (unit tests, optimization, documentation)
8. **Progress tracking and task completion**:
   - Report progress after each completed task
   - Halt execution if non-parallel task fails
   - For parallel tasks, continue with successful ones, report failures
   - **CRITICAL**: Mark completed tasks **immediately** with `[X]` in tasks.md
     - Change `- [ ] T001` to `- [X] T001` after completion
     - Do NOT batch task updates - mark each one as you complete it

## Key Points

- **Load only required context** - Don't read every artifact, only what's needed
- **Respect task dependencies** - Sequential vs parallel execution
- **Mark tasks complete** immediately with `[X]` in tasks.md
- **Create ignore files** based on detected technology (from plan.md)
- **Phase-by-phase execution** - Complete each phase before moving to next
- **Error handling** - Halt on critical failures, report parallel task failures
- **Checklist validation** - Warn if checklists incomplete before starting

## Next Steps

After implementation:

- Manual testing and QA
- Code review
- Deployment planning

## See Also

- `speckit-tasks` - Break plan into actionable tasks
- `speckit-checklist` - Generate custom validation checklists
- `speckit-analyze` - Validate cross-artifact consistency
