---
name: project-maps
description: 'Use for project architecture, codebase structure, dependencies, components,
  tech stack. Explicit triggers: @map, map-ask, explore map, -map. Pre-computed maps
  faster than Glob for structural queries.'
---

---
name: project-maps
description: Use for project architecture, codebase structure, dependencies, components, tech stack. Explicit triggers: @map, map-ask, explore map, -map. Pre-computed maps faster than Glob for structural queries.
allowed-tools: [Bash, Read]
---

# Project Maps Skill

Pre-computed codebase analysis. Use instead of Glob for architecture questions.

## When This Skill is Invoked

When the user asks about project architecture, structure, dependencies, components, or tech stack, execute the appropriate command below.

## Execution Instructions

### For Natural Language Questions

Run the ask command with the user's question:

```bash
node ${CLAUDE_PLUGIN_ROOT}/cli/session-cli.js project-maps ask "{user_question}"
```

If `CLAUDE_PLUGIN_ROOT` is not set, use the plugin cache path:
```bash
node /Users/prajyot/.claude/plugins/cache/automatewithus-plugins/session/3.38.0/cli/session-cli.js project-maps ask "{user_question}"
```

### For Specific Query Types

Use query command for structured data:

```bash
# Architecture/structure
node ${CLAUDE_PLUGIN_ROOT}/cli/session-cli.js project-maps query summary

# Dependencies
node ${CLAUDE_PLUGIN_ROOT}/cli/session-cli.js project-maps query deps

# Components (React/Vue/etc)
node ${CLAUDE_PLUGIN_ROOT}/cli/session-cli.js project-maps query components

# Database schema
node ${CLAUDE_PLUGIN_ROOT}/cli/session-cli.js project-maps query database

# Modules
node ${CLAUDE_PLUGIN_ROOT}/cli/session-cli.js project-maps query modules
```

### For Different Project Paths

Add `--path` for projects other than current directory:

```bash
node ${CLAUDE_PLUGIN_ROOT}/cli/session-cli.js project-maps ask "{question}" --path /path/to/project
```

## When Maps Don't Exist

If command returns "No maps found", instruct user to generate:

```
Maps not found. Run: /session:project-maps-generate
```

## Query Types Reference

| Query Type | Returns |
|------------|---------|
| `summary` | Project overview, tech stack, structure |
| `deps` | Import/export relationships |
| `components` | UI components and props |
| `database` | Tables, columns, relationships |
| `modules` | Logical module boundaries |
| `tree` | File tree structure |
| `issues` | Code quality issues |

## Example Usage

User: "What framework does this project use?"
Action: Run `project-maps ask "what framework does this project use"`

User: "Show me the database schema"
Action: Run `project-maps query database`

User: "What would break if I change auth.js?"
Action: Run `project-maps ask "what would break if I change auth.js"`
