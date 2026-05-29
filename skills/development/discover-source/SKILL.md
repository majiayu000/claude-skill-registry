---
name: discover-source
description: Guidelines for exploring source code to understand context.
user-invocable: false
---

# Discover Source

Guidelines for finding and analyzing source code related to a ticket.

## Search Strategy

1. **File patterns**: Search for files matching keywords from the request
2. **Code patterns**: Grep for function names, class names, imports
3. **Dependencies**: Trace imports to understand relationships

## Analysis Focus

- Entry points and main flows
- Data structures and types
- Integration points
- Existing patterns to follow

## Output Format

Provide structured JSON with:
- `summary`: High-level synthesis
- `files`: List of relevant files with purpose and relevance
- `code_flow`: How components interact
