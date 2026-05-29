---
description: Validate implementation approaches against Brief decisions
---

# Decision Guard Skill

Automatically checks proposed approaches against existing architectural and business decisions.

## Usage Pattern

Before implementing significant changes:

```typescript
// Agent calls:
mcp__brief__brief_execute_operation({
  operation: "guard_approach",
  parameters: {
    approach: "Refactor authentication to use OAuth2 instead of API keys"
  }
})
```

Returns:
- ✅ **Proceed**: No conflicts with existing decisions
- ⚠️ **Review**: Potential conflicts with D-123, D-456
- ❌ **Blocked**: Direct conflict with D-789 (decided to keep API keys for backwards compatibility)

## When to Use

Call `guard_approach` before:
- Architectural changes (auth, database, API design)
- Dependency changes (switching libraries)
- Breaking changes to public APIs
- Changes to core workflows

## Integration Points

- **task-planner agent**: Calls during planning phase (REQUIRED)
- **implementation agent**: Calls before major refactors
- **/onboard**: Could optionally call to check if task conflicts with decisions

## Example Workflow

```text
User: "Refactor auth to use OAuth2"

task-planner agent:
1. Calls guard_approach("Switch from API keys to OAuth2 for authentication")
2. Response: "⚠️ Conflicts with D-234: Keep API keys for MCP server compatibility"
3. Asks user: "Existing decision D-234 requires API keys for MCP. Proceed anyway?"
4. User decides: proceed, modify approach, or cancel
```

## Best Practices

- Call early (during planning, not after implementation)
- Be specific in approach description
- If conflict found, present options to user
- Document override reason if proceeding despite conflict
