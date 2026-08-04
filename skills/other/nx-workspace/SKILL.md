---
name: nx-workspace
description: "Explore and understand Nx workspaces. USE WHEN answering questions about the workspace, projects, or tasks. ALSO USE WHEN an nx command fails or you need to check available targets/configuration before running a task. EXAMPLES: 'What projects are in this workspace?', 'How is project X configured?', 'What depends on library Y?', 'What targets can I run?', 'Cannot find configuration for task', 'debug nx task failure'."
---

# Nx Workspace Exploration

This skill provides read-only exploration of Nx workspaces. Use it to understand workspace structure, project configuration, available targets, and dependencies.

Run all commands via `pnpm nx` (Hedgehog workspaces are pnpm-only).

## Listing Projects

Use `pnpm nx show projects` to list projects in the workspace.

The project filtering syntax (`-p`/`--projects`) works across many Nx commands including `nx run-many`, `nx release`, `nx show projects`, and more. Filters support explicit names, glob patterns, tag references (e.g. `tag:name`), directories, and negation (e.g. `!project-name`).

```bash
# List all projects
pnpm nx show projects

# Filter by pattern (glob)
pnpm nx show projects --projects "apps/*"
pnpm nx show projects --projects "shared-*"

# Filter by tag
pnpm nx show projects --projects "tag:publishable"
pnpm nx show projects -p 'tag:publishable,!tag:internal'

# Filter by target (projects that have a specific target)
pnpm nx show projects --withTarget build

# Combine filters
pnpm nx show projects --type lib --withTarget test
pnpm nx show projects --affected --exclude="*-e2e"
pnpm nx show projects -p "tag:scope:client,packages/*"

# Negate patterns
pnpm nx show projects -p '!tag:private'
pnpm nx show projects -p '!*-e2e'

# Output as JSON
pnpm nx show projects --json
```

## Project Configuration

Use `pnpm nx show project <name> --json` to get the full resolved configuration for a project.

**Important**: Do NOT read `project.json` directly - it only contains partial configuration. The `nx show project --json` command returns the full resolved config including inferred targets from plugins.

You can read the full project schema at `node_modules/nx/schemas/project-schema.json` to understand nx project configuration options.

```bash
# Get full project configuration
pnpm nx show project my-app --json

# Extract specific parts from the JSON
pnpm nx show project my-app --json | jq '.targets'
pnpm nx show project my-app --json | jq '.targets.build'
pnpm nx show project my-app --json | jq '.targets | keys'

# Check project metadata
pnpm nx show project my-app --json | jq '{name, root, sourceRoot, projectType, tags}'
```

## Target Information

Targets define what tasks can be run on a project.

```bash
# List all targets for a project
pnpm nx show project my-app --json | jq '.targets | keys'

# Get full target configuration
pnpm nx show project my-app --json | jq '.targets.build'

# Check target executor/command
pnpm nx show project my-app --json | jq '.targets.build.executor'
pnpm nx show project my-app --json | jq '.targets.build.command'

# View target options
pnpm nx show project my-app --json | jq '.targets.build.options'

# Check target inputs/outputs (for caching)
pnpm nx show project my-app --json | jq '.targets.build.inputs'
pnpm nx show project my-app --json | jq '.targets.build.outputs'

# Find projects with a specific target
pnpm nx show projects --withTarget serve
pnpm nx show projects --withTarget e2e
```

## Workspace Configuration

Read `nx.json` directly for workspace-level configuration.
You can read the full project schema at `node_modules/nx/schemas/nx-schema.json` to understand nx project configuration options.

```bash
# Read the full nx.json
cat nx.json

# Or use jq for specific sections
cat nx.json | jq '.targetDefaults'
cat nx.json | jq '.namedInputs'
cat nx.json | jq '.plugins'
cat nx.json | jq '.generators'
```

Key nx.json sections:

- `targetDefaults` - Default configuration applied to all targets of a given name
- `namedInputs` - Reusable input definitions for caching
- `plugins` - Nx plugins and their configuration
- ...and much more, read the schema or nx.json for details

## Affected Projects

If the user is asking about affected projects, read the [affected projects reference](references/AFFECTED.md) for detailed commands and examples.

## Common Exploration Patterns

### "What's in this workspace?"

```bash
pnpm nx show projects
pnpm nx show projects --type app
pnpm nx show projects --type lib
```

### "How do I build/test/lint project X?"

```bash
pnpm nx show project X --json | jq '.targets | keys'
pnpm nx show project X --json | jq '.targets.build'
```

### "What depends on library Y?"

```bash
# Use the project graph to find dependents
pnpm nx graph --print | jq '.graph.dependencies | to_entries[] | select(.value[].target == "Y") | .key'
```

## Programmatic Answers

When processing nx CLI results, use command-line tools to compute the answer programmatically rather than counting or parsing output manually. Always use `--json` flags to get structured output that can be processed with `jq`, `grep`, or other tools you have installed locally.

### Listing Projects

```bash
pnpm nx show projects --json
```

Example output:

```json
["my-app", "my-app-e2e", "shared-ui", "shared-utils", "api"]
```

Common operations:

```bash
# Count projects
pnpm nx show projects --json | jq 'length'

# Filter by pattern
pnpm nx show projects --json | jq '.[] | select(startswith("shared-"))'

# Get affected projects as array
pnpm nx show projects --affected --json | jq '.'
```

### Project Details

```bash
pnpm nx show project my-app --json
```

Example output:

```json
{
  "root": "apps/my-app",
  "name": "my-app",
  "sourceRoot": "apps/my-app/src",
  "projectType": "application",
  "tags": ["type:app", "scope:client"],
  "targets": {
    "build": {
      "executor": "@nx/vite:build",
      "options": { "outputPath": "dist/apps/my-app" }
    },
    "serve": {
      "executor": "@nx/vite:dev-server",
      "options": { "buildTarget": "my-app:build" }
    },
    "test": {
      "executor": "@nx/vite:test",
      "options": {}
    }
  },
  "implicitDependencies": []
}
```

Common operations:

```bash
# Get target names
pnpm nx show project my-app --json | jq '.targets | keys'

# Get specific target config
pnpm nx show project my-app --json | jq '.targets.build'

# Get tags
pnpm nx show project my-app --json | jq '.tags'

# Get project root
pnpm nx show project my-app --json | jq -r '.root'
```

### Project Graph

```bash
pnpm nx graph --print
```

Example output:

```json
{
  "graph": {
    "nodes": {
      "my-app": {
        "name": "my-app",
        "type": "app",
        "data": { "root": "apps/my-app", "tags": ["type:app"] }
      },
      "shared-ui": {
        "name": "shared-ui",
        "type": "lib",
        "data": { "root": "libs/shared-ui", "tags": ["type:ui"] }
      }
    },
    "dependencies": {
      "my-app": [
        { "source": "my-app", "target": "shared-ui", "type": "static" }
      ],
      "shared-ui": []
    }
  }
}
```

Common operations:

```bash
# Get all project names from graph
pnpm nx graph --print | jq '.graph.nodes | keys'

# Find dependencies of a project
pnpm nx graph --print | jq '.graph.dependencies["my-app"]'

# Find projects that depend on a library
pnpm nx graph --print | jq '.graph.dependencies | to_entries[] | select(.value[].target == "shared-ui") | .key'
```

## Troubleshooting

### "Cannot find configuration for task X:target"

```bash
# Check what targets exist on the project
pnpm nx show project X --json | jq '.targets | keys'

# Check if any projects have that target
pnpm nx show projects --withTarget target
```

### "The workspace is out of sync"

```bash
pnpm nx sync
pnpm nx reset  # if sync doesn't fix stale cache
```
