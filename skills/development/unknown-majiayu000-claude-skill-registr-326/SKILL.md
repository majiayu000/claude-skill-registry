---
name: generate-tasks
description: Convert PRD to structured task list with automatic linking
argument-hint: <prd-file> [--output-dir <directory>]
---

# generate-tasks

**Category**: Task Management

## Usage

```bash
generate-tasks <prd-file> [--output-dir <directory>]
```

## Arguments

- `<prd-file>`: Required - Path to the PRD file to convert
- `--output-dir`: Optional - Directory for task file (default: ./tasks/)

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

1. Read the PRD file and extract metadata
2. Analyze PRD content to generate a comprehensive task list
3. Create task file with proper naming convention:
   - For `*-prd.md`: create `*-prd-tasks.md`
   - For `*-frd.md`: create `*-frd-tasks.md`
   - For `*-simple-frd.md`: create `*-simple-frd-tasks.md`
4. Save task file in the specified output directory (create if needed)
5. Update the PRD with a reference to the generated task file:
   - Add or update the "Implementation Tracking" section
   - Include task file path and generation date
6. Follow any additional process in the source documentation

## Task File Format

Generated task file should include:
```markdown
# [PRD Title] Implementation Tasks

Source PRD: [relative path to PRD]
Generated: [date]
Total Tasks: [count]
Completed: 0

## Tasks

- [ ] 1.0 Setup and Configuration
  - [ ] 1.1 Review relevant documentation
  - [ ] 1.2 Set up development environment

- [ ] 2.0 Core Implementation
  - [ ] 2.1 [Specific task based on PRD]
  ...
```

## PRD Update

Add to PRD under "Implementation Tracking" section:
```markdown
## Implementation Tracking

Task List: ./tasks/[filename]-tasks.md
Generated: 2025-01-06
Status: See task file for current progress
```

## Source Content Location

The full process documentation can be found at:
`claude_settings/python/shared/processes/task-generation.md`

Claude Code should read this file and follow the documented process exactly.

## Example

```bash
# Generate tasks in default location
generate-tasks user-auth-frd.md

# Generate tasks in specific directory
generate-tasks inventory-prd.md --output-dir ../tasks/

# Generate from PRD in another directory
generate-tasks ./drafts/feature-prd.md
```

## Implementation Tips for Claude Code

1. **Smart Task Generation**: Analyze PRD sections to create relevant tasks
2. **Task Grouping**: Organize tasks by implementation phases
3. **Documentation First**: Always include doc review as first subtask
4. **Path Management**: Use relative paths for portability
5. **Metadata Preservation**: Extract PRD title and key info for task file header
