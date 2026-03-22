---
name: shadcn
description: Use for shadcn/ui component library - searching components, viewing examples, getting add commands. Triggers on "shadcn", "UI components", "React components", "Tailwind components", "component registry", "add component", "component examples", "button", "card", "dialog", "form", "table", "input", "select", "tabs", "accordion", "alert", "badge", "checkbox", "dropdown", "modal", "popover", "slider", "switch", "toast", "tooltip".
version: 1.0.0
title: "Shadcn"
status: active
---

# shadcn Skill

Access shadcn/ui component library - search, view examples, and get installation commands for React/Tailwind components.

## Context Efficiency

Traditional MCP approach:
- All 7 tools loaded at startup
- Estimated context: 3500 tokens

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

- `get_project_registries`: Get configured registry names from components.json - Returns error if no components.json exists (use init_project to create one)
- `list_items_in_registries`: List items from registries (requires components.json - use init_project if missing)
- `search_items_in_registries`: Search for components in registries using fuzzy matching (requires components.json). After finding an item, use get_item_examples_from_registries to see usage examples.
- `view_items_in_registries`: View detailed information about specific registry items including the name, description, type and files content. For usage examples, use get_item_examples_from_registries instead.
- `get_item_examples_from_registries`: Find usage examples and demos with their complete code. Search for patterns like 'accordion-demo', 'button example', 'card-demo', etc. Returns full implementation code with dependencies.
- `get_add_command_for_items`: Get the shadcn CLI add command for specific items in a registry. This is useful for adding one or more components to your project.
- `get_audit_checklist`: After creating new components or generating new code files, use this tool for a quick checklist to verify that everything is working as expected. Make sure to run the tool after all required steps have been completed.

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

**Step 3: Execute via bash** (from project root):

```bash
python .claude/skills/mcp-skills/executor.py --skill shadcn --call 'YOUR_JSON_HERE'
```

## Getting Tool Details

If you need detailed information about a specific tool's parameters:

```bash
python .claude/skills/mcp-skills/executor.py --skill shadcn --describe tool_name
```

This loads ONLY that tool's schema, not all tools.

## Examples

### Example 1: Simple tool call

User: "Search for button components in shadcn"

Your workflow:
1. Identify tool: `search_items_in_registries`
2. Generate call JSON
3. Execute:

```bash
python .claude/skills/mcp-skills/executor.py --skill shadcn --call '{"tool": "search_items_in_registries", "arguments": {"registries": ["@shadcn"], "query": "button"}}'
```

### Example 2: Get tool details first

```bash
python .claude/skills/mcp-skills/executor.py --skill shadcn --describe search_items_in_registries
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
| Idle | 3500 tokens | 100 tokens |
| Active | 3500 tokens | 5k tokens |
| Executing | 3500 tokens | 0 tokens |

Savings: ~-42% reduction in typical usage

---

*This skill was auto-generated from an MCP server configuration.*
*Generator: mcp_to_skill.py*
