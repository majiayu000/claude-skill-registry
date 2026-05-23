---
name: tool-executor-registry-migration
description: 'Guide for migrating tools from legacy switch statements to ToolExecutorRegistry handlers in Orient'
---

# Tool Executor Registry Migration

This skill documents the migration pattern from legacy switch-statement tools to ToolExecutorRegistry handlers in Orient.

## Triggers

Use this skill when:

- Migrating a tool from the legacy `mcp-server.ts` switch statement to the modern handler pattern
- Debugging why a tool appears in `discover_tools` but returns "Unknown tool" at runtime
- Understanding the two-registry architecture (ToolRegistry vs ToolExecutorRegistry)
- Setting up new tools that need to work with all MCP server types

## The Two-Registry Architecture

Orient has two separate systems for tools:

### 1. ToolRegistry (Discovery Only)

**Purpose**: Metadata for tool discovery via `discover_tools`
**Location**: `packages/agents/src/services/toolRegistry.ts`
**Function**: `getToolRegistry()`

This registry stores tool definitions and metadata for search/discovery. It does NOT execute tools.

```typescript
// Tools are registered here for discovery
registry.registerTool({
  tool: { name: 'my_tool', description: '...', inputSchema: {...} },
  category: 'google',
  keywords: ['calendar', 'events'],
  useCases: ['List upcoming meetings'],
});
```

### 2. ToolExecutorRegistry (Execution)

**Purpose**: Actually run tool code when called
**Location**: `packages/agents/src/services/toolRegistry.ts`
**Function**: `getToolExecutorRegistry()`

This registry maps tool names to handler functions that execute the tool logic.

```typescript
// Tools are registered here for execution
registry.registerHandler('my_tool', async (args) => {
  // Actual tool implementation
  return createToolResult(JSON.stringify({ success: true }));
});
```

## Identifying the Problem

When a tool returns `{"error":"Unknown tool: tool_name"}`:

### Step 1: Check Discovery

```bash
# If tool appears here, it's in ToolRegistry
curl -X POST ... -d '{"tool":"discover_tools","args":{"mode":"search","query":"tool_name"}}'
```

### Step 2: Check Executor

Look in `packages/agents/src/services/toolRegistry.ts` for:

```typescript
registry.registerHandler('tool_name', ...);
```

If found in discovery but not in executor, the tool needs migration.

## Server Architecture

### assistant-server (Used by Slack/WhatsApp bots)

```
assistant-server.ts
    └── base-server.ts
        └── executeToolCallFromRegistry()
            └── ToolExecutorRegistry.execute()  ← ONLY checks here
                ↓ (if not found)
            └── legacyExecutor  ← ONLY if setLegacyExecutor() was called
                ↓ (if not found)
            └── Returns "Unknown tool" error
```

**CRITICAL**: `base-server.ts` does NOT automatically have access to the legacy `mcp-server.ts` switch statement. Tools MUST be in `ToolExecutorRegistry` to work with assistant-server.

### coding-server / core-server

Same architecture as assistant-server.

### Direct mcp-server.ts (Legacy)

The original monolithic server has a giant switch statement with all tools. But this is only used when running `mcp-server.ts` directly, not via the modular servers.

## Migration Steps

### Step 1: Find the Legacy Implementation

Look in `packages/mcp-servers/src/mcp-server.ts` for:

```typescript
case 'tool_name': {
  // Legacy implementation
}
```

### Step 2: Create Handler in ToolExecutorRegistry

Add to `packages/agents/src/services/toolRegistry.ts`:

```typescript
// In registerXyzToolHandlers() function
registry.registerHandler('tool_name', async (args: Record<string, unknown>) => {
  const { param1, param2 } = args as { param1: string; param2?: number };

  try {
    // Your implementation
    const result = await doSomething(param1, param2);
    return createToolResult(JSON.stringify(result, null, 2));
  } catch (error) {
    return createToolError(`Failed: ${error instanceof Error ? error.message : String(error)}`);
  }
});
```

### Step 3: Call Registration Function

Ensure your registration function is called in `getToolExecutorRegistry()`:

```typescript
export function getToolExecutorRegistry(): ToolExecutorRegistry {
  if (!executorInstance) {
    executorInstance = new ToolExecutorRegistry();
    registerMediaToolHandlers(executorInstance);
    registerConfigToolHandlers(executorInstance);
    registerGoogleToolHandlers(executorInstance); // Add your function here
  }
  return executorInstance;
}
```

### Step 4: Build and Deploy

```bash
# Build affected packages
pnpm --filter @orient/agents build
pnpm --filter @orient/mcp-servers build

# Copy to root dist (CRITICAL - often forgotten!)
cp packages/mcp-servers/dist/*.js dist/mcp-servers/

# Kill old MCP server processes
ps aux | grep "assistant-server\|coding-server" | grep -v grep | awk '{print $2}' | xargs kill

# Test - OpenCode will spawn fresh processes
```

## Common Pitfalls

### 1. Async Registration Race Condition

**WRONG** - Handlers registered asynchronously may not be ready:

```typescript
function registerMyHandlers(registry: ToolExecutorRegistry): void {
  const registerAsync = async () => {
    const service = await import('my-service');
    registry.registerHandler('my_tool', ...);  // May not be ready!
  };
  void registerAsync();  // Fire and forget = race condition
}
```

**CORRECT** - Register synchronously, import lazily inside handler:

```typescript
function registerMyHandlers(registry: ToolExecutorRegistry): void {
  registry.registerHandler('my_tool', async (args) => {
    const service = await import('my-service'); // Lazy import on call
    // ...
  });
}
```

### 2. Forgetting to Copy dist Files

OpenCode's config points to `./dist/mcp-servers/assistant-server.js` (root dist).
Package builds go to `packages/mcp-servers/dist/`.

**Always copy after building:**

```bash
cp packages/mcp-servers/dist/*.js dist/mcp-servers/
```

### 3. Not Killing Old Processes

MCP servers run as child processes of OpenCode. If you don't kill them, they keep running with old code:

```bash
ps aux | grep "assistant-server\|coding-server" | grep -v grep | awk '{print $2}' | xargs kill
```

### 4. Missing from Server Tool Config

Check `packages/mcp-servers/src/types.ts` to ensure the tool's category is included:

```typescript
assistant: {
  tools: {
    categories: ['jira', 'messaging', 'whatsapp', 'docs', 'google', 'context', 'system'],
    //                                                     ^^^^^^^^ Must include your category
  }
}
```

## Verification Checklist

After migration, verify:

1. **Build succeeds**:

   ```bash
   pnpm --filter @orient/agents build
   ```

2. **Handler is registered** (check built file):

   ```bash
   grep "registerHandler.*tool_name" packages/agents/dist/services/toolRegistry.js
   ```

3. **Files copied to root dist**:

   ```bash
   ls -la dist/mcp-servers/base-server.js  # Check timestamp is recent
   ```

4. **Old processes killed**:

   ```bash
   ps aux | grep "assistant-server" | grep -v grep  # Should return nothing
   ```

5. **Tool works in MCP logs**:
   ```bash
   tail -f logs/mcp-debug-*.log | grep tool_name
   # Should NOT see "Unknown tool" error
   ```

## Files Reference

| File                                           | Purpose                               |
| ---------------------------------------------- | ------------------------------------- |
| `packages/agents/src/services/toolRegistry.ts` | Both registries, handler registration |
| `packages/mcp-servers/src/mcp-server.ts`       | Legacy switch statement (DEPRECATED)  |
| `packages/mcp-servers/src/base-server.ts`      | Uses ToolExecutorRegistry             |
| `packages/mcp-servers/src/tool-executor.ts`    | Execution routing logic               |
| `packages/mcp-servers/src/types.ts`            | Server tool configurations            |
| `dist/mcp-servers/*.js`                        | Root dist used by OpenCode            |
