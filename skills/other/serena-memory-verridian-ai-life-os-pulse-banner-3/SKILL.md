---
name: Serena Memory System
description: Interface for long-term memory and context management. Use to store and retrieve user preferences, project context, and past learnings.
---

# Serena Memory System Skill

This skill grants access to the `serena` MCP tools, which provide persistent memory and context awareness for the agent.

## When to use

- Recalling user preferences or project history.
- Storing new "memories" or learnings for future sessions.
- searching for files or symbols using Serena's semantic index.

## Available Tools (Context Loaded)

The following tools are available via the `serena` MCP server:

### Memory Management

- `mcp__serena__list_memories`: Retrieve stored memories.
- `mcp__serena__think_about_collected_information`: Process and synthesize information.
- `mcp__serena__onboarding`: Access onboarding information.

### Semantic Search

- `mcp__serena__find_file`: Find files semantically.
- `mcp__serena__find_symbol`: Find code symbols semantically.

## Best Practices

1. **Check Memory First**: Before asking the user for repetitive info, check if it's stored in memory.
2. **Synthesize**: Use `think_about_collected_information` to consolidate complex context.

## Example Workflow

1. User: "What was the design pattern we decided on?"
2. Agent: Calls `mcp__serena__list_memories` to search for design decisions.
