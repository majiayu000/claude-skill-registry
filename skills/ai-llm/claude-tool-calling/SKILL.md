---
name: "Claude Tool Calling Patterns"
description: "Comprehensive guide for AI agents on proper Claude-style tool calling with correct syntax, patterns, and examples"
approved: Yes
created: 2026-01-22
license: "MIT"
metadata:
  author: "Main Agent"
  version: "1.1"
  last_updated: "2026-01-22"
  tags:
    - claude
    - tool-calling
    - api
    - anthropic
    - function-calling
    - xml-syntax
tools:
  - Claude API
  - XML formatting
files: []
assets:
  - examples/tool-calling-examples.md: "Complete examples of tool calling patterns"
  - examples/common-mistakes.md: "Common tool calling mistakes and fixes"
---

# Claude Tool Calling Patterns

## Overview

This skill provides comprehensive guidance on proper Claude-style tool calling syntax for AI agents building systems that interact with Claude's API. Claude uses a unique XML-based tool calling format that differs from other LLM APIs.

**Key Insight**: Claude's tool calling uses XML-style function_calls blocks with nested invoke and parameter tags. Understanding this structure is critical for building reliable agent systems.

## When to Use This Skill

- **Building AI agent systems** that need to call tools via Claude API
- **Implementing function calling** in Claude-powered applications
- **Debugging tool calling issues** in existing Claude integrations
- **Training other AI agents** to properly format tool calls
- **Migrating from OpenAI function calling** to Claude tool use

## Prerequisites

- **Claude API access**: Anthropic API key
- **XML/HTML familiarity**: Understanding of tag structure
- **JSON knowledge**: Tool parameters use JSON format
- **Programming basics**: Calling APIs from your language of choice

## Skill Usage Type

**EDUCATIONAL** - Study the patterns and examples, implement in your Claude API integration. The examples are reference implementations showing correct syntax.

## Core Concepts

### Tool Calling Structure

Claude's tool calling format uses three layers - see examples directory for complete working examples.

### Key Differences from OpenAI

| Aspect | OpenAI Function Calling | Claude Tool Use |
|--------|------------------------|-----------------|
| **Format** | JSON in tool_calls array | XML-style function_calls block |
| **Multiple calls** | Array of tool call objects | Multiple invoke tags in same block |
| **Parameters** | JSON object | Individual parameter tags |
| **Response** | tool_call_id required | Implicit response matching |
| **Syntax** | Pure JSON | XML with JSON for complex parameters |

## Critical Rules

### Rule 1: Always Use function_calls Block

Every tool call MUST be wrapped in a function_calls block, even for single calls.

### Rule 2: One invoke Per Tool

Each tool gets its own invoke tag with the tool name in the name attribute.

### Rule 3: Individual parameter Tags

Each parameter gets its own tag - do NOT pass all parameters as JSON unless they are nested objects.

### Rule 4: JSON for Complex Types

Use JSON format within parameter tags for:
- Arrays
- Objects/nested structures
- Complex data types

### Rule 5: Parallel Tool Calls

Multiple invoke tags in the same function_calls block execute in parallel.

### Rule 6: Sequential Tool Calls

Use multiple separate function_calls blocks for sequential operations that depend on previous results.

## Common Patterns

### Pattern 1: Single Tool Call

See examples/tool-calling-examples.md for working code.

### Pattern 2: Multiple Parallel Calls

Multiple invoke tags within ONE function_calls block.

### Pattern 3: JSON Parameters

Complex parameters use JSON format within parameter tags.

### Pattern 4: Sequential Calls

Separate function_calls blocks when you need results from first call before making second call.

## Common Mistakes

### Mistake 1: Missing function_calls Wrapper

NEVER write invoke tags without the function_calls container.

### Mistake 2: Wrong Parameter Format

Do NOT pass all parameters as single JSON blob - use individual parameter tags.

### Mistake 3: Unclosed Tags

Always properly close all tags in correct order.

### Mistake 4: Mixing Sequential and Parallel

Don't mix calls that need sequential execution in parallel block.

## Tool Result Handling

When Claude calls your tools, your system must:

1. **Execute the requested tools**
2. **Format results properly**
3. **Return in correct structure**
4. **Handle errors gracefully**

See examples directory for complete request-response cycles.

## Best Practices

### Practice 1: Validate Tool Schemas

Always validate that tool names and parameters match your schema.

### Practice 2: Handle Missing Tools

Gracefully handle cases where Claude requests non-existent tools.

### Practice 3: Error Messages

Return clear error messages in tool results for debugging.

### Practice 4: Type Checking

Validate parameter types match what your tools expect.

### Practice 5: Parallel Where Possible

Use parallel calls when tools don't depend on each other for better performance.

## Integration Patterns

### Pattern A: Tool Schema Definition

Define your tools clearly in the API request with proper JSON Schema.

### Pattern B: Result Formatting

Format tool results consistently for Claude to parse.

### Pattern C: Error Handling

Handle tool execution errors and return useful messages.

## Claude Code-Specific Behaviors

### API Integration Points

When integrating Claude tool calling:

1. **Define tools in API request** using JSON Schema
2. **Parse function_calls blocks** from Claude's response
3. **Execute requested tools** in your system
4. **Format results** as function_results XML blocks
5. **Continue conversation** by sending results back
6. **Loop until completion** (Claude stops making tool calls)

### Tool Results Format

Return results to Claude in this format:

```
<function_results>
<result>
<name>tool_name</name>
<output>Tool output or error message</output>
</result>
</function_results>
```

For errors, use `<tool_use_error>` tags within output.

### Stop Reason Detection

Claude API returns `stop_reason` field:
- `"tool_use"` → Execute tools and continue
- `"end_turn"` → Normal completion, no more tools needed
- `"max_tokens"` → Hit token limit
- `"stop_sequence"` → Custom stop sequence hit

### Thinking Tags

Claude may include `<thinking>` tags for internal reasoning - these are NOT tool calls. Parse and ignore them when extracting tool calls.

### Text Around Tool Calls

Claude can include explanatory text before/after tool calls. Preserve this text for user experience, but only execute the function_calls blocks.

## Examples Directory

Complete working examples are in the examples/ subdirectory:

- `tool-calling-examples.md` - Full examples of all patterns + Claude Code-specific behaviors
- `common-mistakes.md` - Detailed mistake examples with fixes

These examples show the actual XML syntax that would be interpreted if included directly in this file.

## Implementation Checklist

When implementing Claude tool calling:

- [ ] Define tool schemas with proper JSON Schema
- [ ] Parse function_calls blocks from Claude responses
- [ ] Filter out thinking tags (don't execute as tools)
- [ ] Extract invoke tags and parameter tags
- [ ] Execute requested tools (parallel or sequential)
- [ ] Format results as function_results XML blocks
- [ ] Handle errors with tool_use_error tags
- [ ] Check stop_reason to detect tool_use vs end_turn
- [ ] Preserve explanatory text around tool calls
- [ ] Continue conversation loop until completion
- [ ] Validate all tool names and parameters
- [ ] Test parallel tool calling
- [ ] Test sequential tool calling (multi-turn)
- [ ] Test error cases and recovery
- [ ] Test mixed text and tool call responses

## References

- [Claude API Documentation](https://docs.anthropic.com/claude/docs/tool-use)
- [Tool Use Guide](https://docs.anthropic.com/claude/docs/tool-use-examples)
- [API Reference](https://docs.anthropic.com/claude/reference)

## See examples/ Directory

**IMPORTANT**: All concrete XML examples are in the examples/ subdirectory to prevent accidental tool execution when this skill file is read. Always refer to examples/ for actual syntax.

---
*Created: 2026-01-22*
*Last Updated: 2026-01-22 v1.1*
*Changes in v1.1: Added Claude Code-specific behaviors, API integration patterns, thinking tags, stop_reason handling, conversation flow*
