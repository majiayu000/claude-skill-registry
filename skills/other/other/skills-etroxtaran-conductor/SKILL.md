---
name: skills
description: List and categorize all available skills in the Conductor system.
version: 1.1.0
tags: [discovery, skills, workflow]
owner: orchestration
status: active
---

# Skills Discovery Skill

List all available skills in the Conductor system.

## Usage

```
/skills
```

## Overview

Help users and Claude discover what capabilities are available, grouped by workflow phase.

## Prerequisites

- None beyond access to the repository and skill docs.

## Outputs

Displays:
- All available commands organized by category
- Brief descriptions of each
- Recommended workflow order
- Links to detailed documentation

## Workflow Steps

1. Read available skill directories in `.claude/skills`.
2. Group commands into workflow categories.
3. Present command, purpose, and related documentation paths.

## Categories

### Human-Guided Workflow
Commands for step-by-step development with user control:
- `/discover` - Understand project, create spec
- `/plan` - Create task breakdown
- `/task <id>` - Implement single task
- `/status` - Check progress

### Automated Workflow
Commands for hands-off execution:
- `/orchestrate` - Full automated workflow

### Agent Invocation
Commands to directly call agents:
- `/validate` - Plan validation
- `/verify` - Code review
- `/call-cursor` - Cursor agent
- `/call-gemini` - Gemini agent

### Utility
Support commands:
- `/skills` - This command
- `/phase-status` - Detailed status
- `/resolve-conflict` - Conflict resolution
- `/list-projects` - Project listing
- `/sync-rules` - Rule synchronization
- `/add-lesson` - Add lessons learned

## Error Handling

- If skill docs are missing or unreadable, report which paths failed and return partial results.

## Examples

```
/skills
```

## Related Skills

- `/discover` - Create or discover project documentation
- `/plan` - Create a task breakdown
- `/orchestrate` - Full workflow execution
