---
name: story-create
description: Create structured story files for planning user-facing features. Use when user asks to "create a story", "add a story", "plan a story", or needs to document user value. Creates numbered markdown files in docs/planning/stories/.
---

# Story Create

Create story files using the `aaa` CLI.

## Workflow

1. Run: `aaa story create <name>`
2. Write content using template
3. **Prompt user:** "Create tasks for this story?"
4. If yes, create tasks with `--story NNN` flag

## References

- **CLI & workflow:** @context/blocks/docs/task-management.md
- **Template:** @context/blocks/docs/story-template.md
