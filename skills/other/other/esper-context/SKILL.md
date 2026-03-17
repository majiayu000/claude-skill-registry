---
name: esper:context
description: Show the current project context. Summarizes active increment, spec root, commands, and suggests the next safe action.
---

You are displaying the current esper project context.

## Step 1: Read context

Run `esperkit context get`. If it fails, tell the user to run `esper:init` first and stop.

Parse the JSON output.

## Step 2: Read active increment (if any)

If `active_increment` is not null:
- Read the increment file from `.esper/increments/active/<filename>`
- Parse its frontmatter and body
- Note its title, type, lane, spec references, and progress

## Step 3: Present summary

Print a clear, structured summary:

```
Project Context
  Spec root:        [spec_root]
  Schema version:   [schema_version]
  Workflow mode:    [workflow_mode]
  Constitution:     [constitution_path or "not set"]

Active Increment
  [title] ([type], [lane])
  Spec: [spec reference or "none"]
  Progress: [summary of ## Progress section]

Commands
  test:      [command or "not configured"]
  lint:      [command or "not configured"]
  typecheck: [command or "not configured"]
  dev:       [command or "not configured"]
```

## Step 4: Suggest next action

Based on the context, suggest what the user can do next:

- **No active increment, specs exist**: "Run `esper:atom` to create an increment, or `esper:spec` to work on specs."
- **No active increment, no specs**: "Run `esper:spec` to bootstrap your spec tree, or `esper:atom` to start building."
- **Active increment, not started**: "Run `esper:go` to begin implementation."
- **Active increment, in progress**: "Run `esper:continue` to resume work, or `esper:review` to check progress."
- **Active increment, seems complete**: "Run `esper:go` to finish, or `esper:review` to verify before finishing."

## Available CLI commands

- `esperkit context get` — read context.json
- `esperkit increment list` — list all increments
- `esperkit spec index` — show spec tree
