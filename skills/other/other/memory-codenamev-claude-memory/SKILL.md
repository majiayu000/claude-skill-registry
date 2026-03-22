---
name: memory
description: Store and recall long-term memory. Use when persisting facts learned during conversations or recalling stored knowledge about projects and preferences.
---

# Memory Skill

You have access to a long-term memory system. Use it to remember important facts across sessions.

## When to Store Facts

After completing a task or learning something important about the project, store durable facts using `memory.store_extraction`. Look for:

- **Tech stack**: databases, frameworks, languages, platforms
- **Conventions**: coding standards, naming patterns, preferences
- **Decisions**: architectural choices, design decisions
- **Preferences**: user preferences that should persist

## How to Store Facts

Call the `memory.store_extraction` MCP tool with:

```json
{
  "entities": [
    {"type": "database", "name": "postgresql"}
  ],
  "facts": [
    {
      "subject": "repo",
      "predicate": "uses_database",
      "object": "postgresql",
      "quote": "We use PostgreSQL for persistence",
      "strength": "stated",
      "scope_hint": "project"
    }
  ]
}
```

### Predicates

| Predicate | Use for | Example |
|-----------|---------|---------|
| `uses_database` | Database choice | postgresql, redis |
| `uses_framework` | Framework | rails, react, nextjs |
| `deployment_platform` | Where deployed | vercel, aws, heroku |
| `convention` | Coding standard | "4-space indentation" |
| `decision` | Architectural choice | "Use microservices" |
| `auth_method` | Auth approach | "JWT tokens" |

### Scope

- `project`: Only this project (default)
- `global`: All projects (user preferences)

Use `global` when user says "always", "in all projects", or "my preference".

## How to Recall Facts

Use `memory.recall` to search for relevant facts:

```json
{"query": "database", "limit": 10}
```

## Available Tools

- `memory.recall` - Search facts by query
- `memory.store_extraction` - Store new facts
- `memory.explain` - Get fact details with provenance
- `memory.promote` - Promote project fact to global
- `memory.status` - Check database health
- `memory.changes` - Recent updates
- `memory.conflicts` - Open contradictions

## Best Practices

1. **Be selective**: Only store durable facts that will be useful later
2. **Include quotes**: Add the source text for provenance
3. **Set scope correctly**: Project-specific vs global preferences
4. **Check before storing**: Use `memory.recall` to avoid duplicates
