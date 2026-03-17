---
name: generate-sdk-types
description: Generates TypeScript type definitions for SDK from Rust tool schemas, ensuring type safety between server and client
user-invocable: true
---

# Generate SDK Types Skill

## Purpose
Generates TypeScript type definitions for the SDK from Rust tool schemas, ensuring type safety between server and client.

## CLAUDE.md Compliance
- ✅ Automated type generation (no manual sync)
- ✅ Validates type consistency
- ✅ Prevents type drift between Rust and TypeScript

## Usage
Run this skill:
- After adding/modifying MCP tools
- After changing tool parameter schemas
- Before SDK releases
- After protocol changes

## Prerequisites
- Bun runtime installed
- Pierre server must be runnable
- `sdk/` directory with dependencies installed

## Commands

### Standard Type Generation
```bash
# 1. Ensure server is running
cargo run --bin pierre-mcp-server &
SERVER_PID=$!
sleep 3

# 2. Generate TypeScript types
cd sdk
bun run generate-types

# 3. Verify types changed
git diff src/types.ts

# 4. Cleanup
kill $SERVER_PID
cd ..
```

### One-Command Generation
```bash
# Run from project root (handles server lifecycle)
./scripts/sdk/generate-sdk-types.js
```

### Manual Generation Process
```bash
# 1. Start server
cargo run --bin pierre-mcp-server &
SERVER_PID=$!
sleep 3

# 2. Fetch tool schemas via MCP
curl -X POST http://localhost:8081/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' \
  > /tmp/tools.json

# 3. Parse and generate types
cd sdk
node scripts/generate-types.js /tmp/tools.json

# 4. Format generated code
bun run format

# 5. Cleanup
kill $SERVER_PID
cd ..
```

## Generated Type Structure

### Tool Definitions
```typescript
// Generated from Rust ToolDefinition structs
export interface Tool {
  name: string;
  description: string;
  inputSchema: {
    type: 'object';
    properties: Record<string, JsonSchema>;
    required?: string[];
  };
}

// Example: get_activities tool
export interface GetActivitiesParams {
  start_date?: string;
  end_date?: string;
  limit?: number;
  provider?: 'strava' | 'garmin' | 'fitbit';
}
```

### Tool Registry
```typescript
// All available tools
export const TOOLS: Tool[] = [
  {
    name: 'get_activities',
    description: 'Retrieves fitness activities...',
    inputSchema: { /* ... */ }
  },
  // ... 35+ tools
];
```

## Type Validation

### Pre-Generation Check
```bash
# Verify Rust tools compile
cargo build --lib

# Check tool count
rg "^pub const TOOL_" src/protocols/universal/tool_registry.rs --type rust | wc -l
```

### Post-Generation Validation
```bash
# Verify types compile
cd sdk
bun run build

# Run type tests
bun test -- test/unit/types.test.ts

# Check type coverage
bun run type-check
cd ..
```

### Diff Analysis
```bash
# Compare generated types with committed version
git diff sdk/src/types.ts

# Expected changes after adding a tool:
# + New tool interface
# + New tool definition in TOOLS array
# + Updated tool count comment
```

## Type Generation Workflow

### 1. Add New Tool in Rust
```rust
// src/protocols/universal/tool_registry.rs
pub const TOOL_MY_NEW_FEATURE: ToolDefinition = ToolDefinition {
    name: "my_new_feature",
    description: "Does something useful",
    input_schema: json!({
        "type": "object",
        "properties": {
            "param1": { "type": "string" },
            "param2": { "type": "number" }
        },
        "required": ["param1"]
    }),
};
```

### 2. Register Tool
```rust
// src/protocols/universal/mod.rs
impl UniversalToolExecutor {
    pub fn register_tools(&mut self) {
        self.register(TOOL_MY_NEW_FEATURE, handle_my_new_feature);
    }
}
```

### 3. Generate TypeScript Types
```bash
cd sdk
bun run generate-types
```

### 4. Verify Generated Types
```typescript
// sdk/src/types.ts (auto-generated)
export interface MyNewFeatureParams {
  param1: string;
  param2?: number;
}

export const TOOL_MY_NEW_FEATURE: Tool = {
  name: 'my_new_feature',
  description: 'Does something useful',
  inputSchema: { /* ... */ }
};
```

### 5. Commit Changes
```bash
git add src/protocols/universal/tool_registry.rs
git add sdk/src/types.ts
git commit -m "feat: add my_new_feature tool with TypeScript types"
```

## Success Criteria
- ✅ TypeScript types match Rust tool definitions
- ✅ All tools have corresponding TypeScript interfaces
- ✅ Generated code compiles without errors
- ✅ Type tests pass
- ✅ No manual type definitions (all auto-generated)
- ✅ Git diff shows expected changes only

## Related Files
- `scripts/sdk/generate-sdk-types.js` - Type generation script
- `sdk/src/types.ts` - Generated TypeScript types
- `src/protocols/universal/tool_registry.rs` - Rust tool definitions
- `sdk/TYPE_GENERATION.md` - Type generation documentation

## Related Skills
- `test-mcp-compliance` - MCP protocol validation
