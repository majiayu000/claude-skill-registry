---
description: Developing and testing MCP tools for Brief
---

# MCP Tool Development

## Adding New MCP Tools

1. **Define tool** in `mcp-server/src/tools/[domain]/[tool-name].ts`
2. **Add to registry** in `mcp-server/src/tools/index.ts`
3. **Update types** in `mcp-server/src/types.ts`
4. **Test with Claude Code** MCP inspector
5. **Document** in `.brief/brief-guidelines.md`
6. **Add to allowlist** in `.claude/settings.local.json` if needs preapproval

## Tool Structure

```typescript
export const myTool: Tool = {
  name: 'brief_my_operation',
  description: 'Clear description of what it does',
  inputSchema: {
    type: 'object',
    properties: {
      // Zod-like schema
    },
    required: ['field1']
  },
  handler: async (args, context) => {
    // Implementation
    return { success: true, data: result };
  }
};
```

## Testing MCP Tools

- Use MCP inspector: `npx @modelcontextprotocol/inspector`
- Test error cases (missing params, invalid auth, not found)
- Validate against OpenAPI spec if API-backed
- Test from Claude Code with actual workflows

## Documentation Pattern

Update `.brief/brief-guidelines.md`:

```markdown
### New Operation Category
- `operation_name` - Description of operation
  - Required params: param1, param2
  - Optional params: param3
  - Returns: what it returns
  - Example: JSON example
```

## Common Mistakes

- ❌ Not validating input schema
- ❌ Not handling authentication errors
- ❌ Not documenting in guidelines
- ❌ Not adding to allowlist if needed
- ✅ Test happy path AND error paths
