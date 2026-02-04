---
name: todo
description: Manage project TODO tasks (show, add, complete)
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion]
---
# TODO Manager

Manage project-level TODO tasks stored in `.bluera/bluera-base/TODO.txt`.

## Context

!`echo "TODO file: ${CLAUDE_PROJECT_DIR:-.}/.bluera/bluera-base/TODO.txt"`
!`test -f "${CLAUDE_PROJECT_DIR:-.}/.bluera/bluera-base/TODO.txt" && echo "Status: exists" || echo "Status: not created yet"`

## Usage

```bash
/bluera-base:todo [show|add|complete]
```

- **show** (default): Display current TODO list
- **add**: Interview user and add a new task
- **complete**: Mark a task as complete

## File Location

`<project root>/.bluera/bluera-base/TODO.txt`

This file is NOT gitignored by default - it's meant to be committed and shared with the team.

## Workflow

### Mode: show (default)

1. Read and display the TODO file contents
2. If file doesn't exist, show a message suggesting `/bluera-base:todo add`

### Mode: add

Interview the user to gather task details:

1. **Task name** (required): Short, descriptive name
2. **Description** (required): What needs to be done
3. **Requirements** (required): Acceptance criteria / definition of done
4. **Notes** (optional): Additional context or considerations
5. **References** (optional): Related files, issues, PRs, docs
6. **Resources** (optional): External links, examples, tutorials
7. **Outcomes** (required): Expected results when complete

After gathering details, append the task to the TODO file:

```markdown
[ ] <task name>
description: <description>
requirements: <requirements>
notes: <notes>
references: <references>
resources: <resources>
outcomes: <outcomes>
learnings: (to be filled on completion)
```

### Mode: complete

1. Show numbered list of incomplete tasks
2. Ask user which task to complete
3. Ask for learnings from the task
4. Move task to COMPLETED TASKS section with:
   - Change `[ ]` to `[x]`
   - Fill in the `learnings:` field
   - Add completion date

## File Format

```markdown
# bluera-base TODOs

## IMPORTANT

* for any/all work, ensure we're fully utilizing all best practices and optimizations per project conventions and documentation
* write proper tests as applicable
* utilize TDD for bug-fixes
* maintain documentation as relevant (README.md, docs/*, CLAUDE.md, **/CLAUDE.md, etc.)
* move tasks to "## COMPLETED TASKS" once complete

## TODO TASKS

[ ] Example task
description: What needs to be done
requirements: Definition of done
notes: Additional context (OPTIONAL)
references: Related files, issues (OPTIONAL)
resources: External links (OPTIONAL)
outcomes: Expected results
learnings: (filled on completion)

## COMPLETED TASKS

[x] Completed example
description: What was done
requirements: What was required
outcomes: What was achieved
learnings: What was learned
completed: 2025-01-17
```

## Implementation Notes

1. Create the `.bluera/bluera-base/` directory if it doesn't exist
2. Create the TODO.txt file with the header template if it doesn't exist
3. Parse the file to identify tasks by the `[ ]` or `[x]` prefix
4. Preserve all formatting and content when editing

## Template for New File

When creating a new TODO.txt, use this template:

```markdown
# bluera-base TODOs

## IMPORTANT

* for any/all work, ensure we're fully utilizing all best practices and optimizations per project conventions and documentation
* write proper tests as applicable
* utilize TDD for bug-fixes
* maintain documentation as relevant (README.md, docs/*, CLAUDE.md, **/CLAUDE.md, etc.)
* move tasks to "## COMPLETED TASKS" once complete

## TODO TASKS

(no tasks yet - use `/bluera-base:todo add` to create one)

## COMPLETED TASKS

(none yet)
```
