---
name: memory
description: Claude Mind - Search and manage Claude's persistent memory stored in a single portable .mv2 file
---

# Claude Mind

You have access to a persistent memory system powered by Claude Mind. All your observations, discoveries, and learnings are stored in a single `.claude/mind.mv2` file.

## How to Execute Memory Commands

Use the bundled SDK scripts via Node.js (NOT the CLI). The scripts are at `${CLAUDE_PLUGIN_ROOT}/dist/scripts/`.

### Search Memories
```bash
node "${CLAUDE_PLUGIN_ROOT}/dist/scripts/find.js" "<query>" [limit]
```

Examples:
- `node "${CLAUDE_PLUGIN_ROOT}/dist/scripts/find.js" "authentication" 5`
- `node "${CLAUDE_PLUGIN_ROOT}/dist/scripts/find.js" "database schema" 10`

### Ask Questions
```bash
node "${CLAUDE_PLUGIN_ROOT}/dist/scripts/ask.js" "<question>"
```

Examples:
- `node "${CLAUDE_PLUGIN_ROOT}/dist/scripts/ask.js" "Why did we choose React?"`
- `node "${CLAUDE_PLUGIN_ROOT}/dist/scripts/ask.js" "What was the CORS solution?"`

### View Statistics
```bash
node "${CLAUDE_PLUGIN_ROOT}/dist/scripts/stats.js"
```

### View Recent Memories
```bash
node "${CLAUDE_PLUGIN_ROOT}/dist/scripts/timeline.js" [count]
```

## Memory Types

Memories are automatically classified into these types:
- **discovery** - New information discovered
- **decision** - Important decisions made
- **problem** - Problems or errors encountered
- **solution** - Solutions implemented
- **pattern** - Patterns recognized in code/data
- **warning** - Warnings or concerns noted
- **success** - Successful outcomes
- **refactor** - Code refactoring done
- **bugfix** - Bugs fixed
- **feature** - Features added

## File Location

Your memory is stored at: `.claude/mind.mv2`

This file is:
- **Portable** - Copy it anywhere, share with teammates
- **Git-friendly** - Commit to version control
- **Self-contained** - Everything in ONE file
- **Searchable** - Instant semantic search

## Usage Tips

1. **Start of session**: Recent memories are automatically injected as context
2. **During coding**: Observations are captured automatically from tool use
3. **Searching**: Use natural language queries to find relevant past context
4. **Sharing**: Send the `.mind.mv2` file to teammates for instant onboarding
