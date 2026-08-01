---
name: templates
description: 'description: Dynamic access to {servername} MCP server ({toolcount}
  tools)'
---

name: {server_name}
description: Dynamic access to {server_name} MCP server ({tool_count} tools)
version: 1.0.0
---

# {server_name} Skill

This skill provides dynamic access to the {server_name} MCP server without loading all tool definitions into context.

## Context Efficiency

Traditional MCP approach:
- All {tool_count} tools loaded at startup
- Estimated context: {estimated_tokens} tokens

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

{tool_list}

## Usage Pattern

When the user's request matches this skill's capabilities:

**Step 1: Identify the right tool** from the list above

**Step 2: ALWAYS get tool details first** to obtain correct parameter names and types:

```bash
cd $SKILL_DIR
python executor.py --describe tool_name
```

This loads ONLY that tool's schema, not all tools.

**Step 3: Generate a tool call** using the exact parameter names from Step 2:

```json
{{
  "tool": "tool_name",
  "arguments": {{
    "param1": "value1",
    "param2": "value2"
  }}
}}
```

**Step 4: Execute via bash:**

```bash
cd $SKILL_DIR
python executor.py --call 'YOUR_JSON_HERE'
```

IMPORTANT: Replace $SKILL_DIR with the actual discovered path of this skill directory.

## Important Note

You MUST use `--describe` before calling any tool to get the correct parameter names and types. Do not guess parameter names as this will result in errors.

## Examples

### Example 1: Complete workflow

User: "Use {server_name} to do X"

Your workflow:
1. Identify tool: `{first_tool_name}`
2. Get tool details: `python executor.py --describe {first_tool_name}`
3. Generate call JSON using exact parameter names from Step 2
4. Execute:

```bash
cd $SKILL_DIR
python executor.py --call '{{"tool": "{first_tool_name}", "arguments": {{"param1": "value"}}}}'
```

### Example 2: Tool details output

```bash
cd $SKILL_DIR
python executor.py --describe {first_tool_name}
```

Returns the full schema with parameter names, types, and requirements.

## Error Handling

If the executor returns an error:
- Check the tool name is correct
- Verify you used `--describe` to get the exact parameter names
- Ensure all required arguments are provided
- Check that parameter types match what's expected
- Ensure the MCP server is accessible

Common error: "Invalid arguments for tool" - This usually means you used an incorrect parameter name. Always run `--describe` first to get the correct parameter names.

## Performance Notes

Context usage comparison for this skill:

| Scenario | MCP (preload) | Skill (dynamic) |
|----------|---------------|-----------------|
| Idle | {estimated_tokens} tokens | 100 tokens |
| Active | {estimated_tokens} tokens | 5k tokens |
| Executing | {estimated_tokens} tokens | 0 tokens |

Savings: ~{savings_percentage}% reduction in typical usage

---

*This skill was auto-generated from an MCP server configuration.*
*Generator: mcp_to_skill.py*
