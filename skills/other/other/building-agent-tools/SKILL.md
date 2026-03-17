---
name: building-agent-tools
description: Guide for creating effective tools for AI agents. Use when building MCP tools, agent APIs, or any tool interface that agents will consume. Focuses on token efficiency, meaningful context, and proper namespacing.
---

# Building Tools for AI Agents

## Workflow

1. **Define Purpose**
   - Identify what agents need to accomplish with this tool
   - Determine if existing tools can be consolidated
   - Plan the tool's interface for agent consumption

2. **Design Interface**
   - Choose descriptive, namespaced tool names
   - Define parameters with clear types and descriptions
   - Design output format for maximum signal, minimum tokens

3. **Implement**
   - Build with token efficiency in mind
   - Add pagination, filtering, sensible defaults
   - Return semantic identifiers, not raw IDs

4. **Validate**
   - Test with real agent workflows
   - Check token consumption patterns
   - Verify error messages guide agents toward solutions

## Design Principles

**Tool Consolidation**
- More tools don't lead to better outcomes
- Combine related operations into single tools
- Example: `schedule_event` that checks availability AND creates event
- Avoid simple CRUD-style tools that require multiple calls

**Namespacing**
- Prefix related tools with service name: `asana_projects_search`, `asana_users_search`
- Group by domain to help agents distinguish functionality
- Use consistent naming patterns across tool families

**Meaningful Context**
- Return high-signal information, not raw data dumps
- Resolve cryptic UUIDs to human-readable identifiers
- Include `response_format` parameter (concise/detailed) for flexibility
- Surface relevant metadata agents need for next steps

**Token Efficiency**
- Implement pagination with sensible defaults
- Add filtering parameters to reduce unnecessary data
- Truncate large responses intelligently
- Prefer structured output over verbose prose

**Tool Descriptions**
- Invest heavily in clear, explicit descriptions
- Describe what the tool does, when to use it, and what it returns
- Include parameter constraints and valid values
- Small description improvements yield large performance gains

## Anti-Patterns

- Creating many granular tools instead of consolidated operations
- Returning raw IDs that agents can't interpret
- Omitting pagination on potentially large result sets
- Vague tool descriptions that leave agents guessing
- Error messages that don't help agents recover
- Requiring agents to make multiple calls for common workflows

## MCP-Specific Patterns

**Tool Registration**
- Use descriptive `name` and `description` in tool schema
- Define `inputSchema` with JSON Schema for parameters
- Mark required vs optional parameters explicitly

**Response Format**
- Return structured JSON for predictable parsing
- Include success/error indicators
- Provide actionable error messages
