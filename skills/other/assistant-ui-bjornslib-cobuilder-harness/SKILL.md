---
name: assistant-ui
description: Use for assistant-ui documentation, ToolUI, generative UI, chat components, Thread, Composer, Message primitives, runtime integrations. Get docs and code examples for building AI chat interfaces.
version: 1.0.0
title: "Assistant Ui"
status: active
---

# assistant-ui Skill

Access assistant-ui documentation and code examples for building AI chat interfaces with React.

## Context Efficiency

Traditional MCP approach:
- All 2 tools loaded at startup
- Estimated context: 1000 tokens

This skill approach:
- Metadata only: ~100 tokens
- Full instructions (when used): ~5k tokens
- Tool execution: 0 tokens (runs externally)

## How This Works

Instead of loading all MCP tool definitions upfront, this skill:
1. Tells you what tools are available (just names and brief descriptions)
2. You decide which tool to call based on the user's request
3. Generate a JSON command to invoke the tool
4. The executor handles the actual MCP communication

## Available Tools

- `assistantUIDocs`: Retrieve assistant-ui documentation by path. Use "/" to list all sections. Supports multiple paths in a single request.
- `assistantUIExamples`: List available examples or retrieve complete code for a specific example

## Usage Pattern

When the user's request matches this skill's capabilities:

**Step 1: Identify the right tool** from the list above

**Step 2: Generate a tool call** in this JSON format:

```json
{
  "tool": "tool_name",
  "arguments": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

**Step 3: Execute via bash:**

```bash
python .claude/skills/mcp-skills/executor.py --skill assistant-ui --call 'YOUR_JSON_HERE'
```


## Getting Tool Details

If you need detailed information about a specific tool's parameters:

```bash
python .claude/skills/mcp-skills/executor.py --skill assistant-ui --describe tool_name
```

This loads ONLY that tool's schema, not all tools.

## Examples

### Example 1: Simple tool call

User: "Get assistant-ui documentation"

Your workflow:
1. Identify tool: `assistantUIDocs`
2. Generate call JSON
3. Execute:

```bash
python .claude/skills/mcp-skills/executor.py --skill assistant-ui --call '{"tool": "assistantUIDocs", "arguments": {"paths": ["/"]}}'
```

### Example 2: Get tool details first

```bash
python .claude/skills/mcp-skills/executor.py --skill assistant-ui --describe assistantUIDocs
```

Returns the full schema, then you can generate the appropriate call.

## Error Handling

If the executor returns an error:
- Check the tool name is correct
- Verify required arguments are provided
- Ensure the MCP server is accessible

## Performance Notes

Context usage comparison for this skill:

| Scenario | MCP (preload) | Skill (dynamic) |
|----------|---------------|-----------------|
| Idle | 1000 tokens | 100 tokens |
| Active | 1000 tokens | 5k tokens |
| Executing | 1000 tokens | 0 tokens |

Savings: ~-400% reduction in typical usage

---

*This skill was auto-generated from an MCP server configuration.*
*Generator: mcp_to_skill.py*
