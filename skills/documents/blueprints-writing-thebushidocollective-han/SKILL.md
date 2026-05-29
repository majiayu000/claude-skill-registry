---
name: blueprints-writing
description: Use when creating or updating technical blueprint documentation for new features, API changes, or architectural modifications. Always use search_blueprints first to avoid duplication, then write_blueprint with proper structure.
allowed-tools: [Read, Write, Edit, Grep, Glob, mcp__plugin_hashi-blueprints_blueprints__search_blueprints, mcp__plugin_hashi-blueprints_blueprints__read_blueprint, mcp__plugin_hashi-blueprints_blueprints__write_blueprint]
---

# Writing Technical Blueprints

## Purpose

Technical blueprints document **how systems work internally**. They differ from user documentation (how to use) and README files (project overview).

## When to Write Blueprints

Write blueprints for:

- Complex systems with multiple components
- Public APIs and their contracts
- Architecture decisions and their rationale
- Behavior that isn't obvious from code
- Integration points between systems

Skip blueprints for:

- Self-documenting code (simple utilities)
- Test files (tests ARE the documentation)
- External dependencies (link to their docs)

## Creating Blueprints

**IMPORTANT:** Always use the `write_blueprint` MCP tool to create or update blueprints. This automatically adds the required frontmatter.

```typescript
// Before writing, search for existing blueprints
const existing = await search_blueprints({ keyword: "auth" });

// Read existing blueprint if updating
const current = await read_blueprint({ name: "authentication" });

// Write or update the blueprint
await write_blueprint({
  name: "system-name",
  summary: "Brief one-line description",
  content: "# System Name\n\n## Overview\n..."
});
```

The MCP tool handles frontmatter automatically - you just provide the content.

## Blueprint File Structure

When writing blueprint content (passed to `write_blueprint`), use this structure:

```markdown
# System Name

One-line description of what this system does.

## Overview

2-3 paragraphs covering:
- Why this system exists (problem it solves)
- What it does at a high level
- Where it fits in the larger architecture

## Architecture

### Components

List major components:
- **ComponentA** - Purpose and responsibility
- **ComponentB** - Purpose and responsibility

### Data Flow

Describe how data moves through the system:
1. Input arrives via X
2. ComponentA processes and transforms
3. Result passed to ComponentB
4. Output returned/stored

### Dependencies

- **Dependency** - Why it's needed, what it provides

## API / Interface

### Functions

#### `functionName(param1, param2)`

Clear description of what the function does.

**Parameters:**
- `param1` (Type) - What this parameter controls
- `param2` (Type, optional) - Default behavior if omitted

**Returns:** Type - Description of return value

**Throws:** ErrorType - When this error occurs

**Example:**
```typescript
const result = functionName('value', { option: true });
```

### Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `optionA` | boolean | false | What it controls |

## Behavior

### Normal Operation

Step-by-step description of typical execution flow.

### Error Handling

How the system responds to:

- Invalid input
- Missing dependencies
- External failures

### Edge Cases

Document non-obvious behaviors:

- Empty input handling
- Concurrent access
- Resource limits

## Files

Key files and their roles:

- `src/main.ts:1-50` - Entry point, initialization
- `src/processor.ts` - Core processing logic
- `src/types.ts` - Type definitions

## Related Systems

- [Related System](./related-system.md) - How they interact

```

## Writing Style

### Be Precise

Bad: "The system handles errors gracefully"
Good: "Invalid input returns a ValidationError with the field name and reason"

### Document Behavior, Not Implementation

Bad: "Uses a for loop to iterate through items"
Good: "Processes items sequentially, stopping at the first failure"

### Include Examples

Show, don't just tell:
```typescript
// Good: concrete example
const result = processItems(['a', 'b', 'c'], { parallel: true });
// Returns: { processed: 3, failed: 0 }
```

### Keep Current

- Update blueprints alongside code changes
- Remove documentation for deleted features
- Mark deprecated features clearly

## Common Mistakes

1. **Too much detail** - Don't document every line of code
2. **Too little context** - Explain why, not just what
3. **Stale documentation** - Outdated docs are worse than none
4. **Duplicate content** - Link instead of copying
5. **Implementation focus** - Document contracts, not internals
