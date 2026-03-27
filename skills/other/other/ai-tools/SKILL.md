---
name: ai-tools
description: Reference for all AI tools available in DBX Studio's AI chat system. Use when adding, modifying, or debugging AI tool definitions, tool execution, or provider integrations.
user-invocable: false
---

# DBX Studio AI Tools Reference

## Tool Definitions Location
[apps/api/src/orpc/routers/ai/tools.ts](apps/api/src/orpc/routers/ai/tools.ts)

## Tool Executor Location
[apps/api/src/orpc/routers/ai/toolExecutor.ts](apps/api/src/orpc/routers/ai/toolExecutor.ts)

## Available Tools (AI_TOOLS array)

| Tool Name | Purpose | Required Params |
|-----------|---------|-----------------|
| `read_schema` | Get all tables and structure from schema store | `schema_name` |
| `get_table_data` | Preview rows from a table (generates SELECT) | `table_name` |
| `execute_query` | Run a SELECT/WITH query | `sql` |
| `generate_chart` | Create chart config (bar/line/pie/scatter/area/histogram) | `chart_type`, `title`, `data_query` |
| `describe_table` | Get table metadata from `schemaTables` DB table | `table_name` |
| `get_table_stats` | Get statistics summary for a table | `table_name` |

## AI Providers

| Service ID | Provider | File |
|------------|----------|------|
| 1 | AWS Bedrock | `ai-stream.ts` (streaming) + `providersWithTools.ts` |
| 2 | OpenAI | `providersWithTools.ts` → `callOpenAIWithTools` |
| 3 | Anthropic | `providersWithTools.ts` → `callAnthropicWithTools` |
| 4 | Qwen | `index.ts` |
| 5 | Ollama | `index.ts` |
| 6 | Gemini | `index.ts` |
| 7 | Groq | `index.ts` |
| 8 | DBX Agent | External → `MAIN_SERVER_URL` |

## Tool Format Conversions

```typescript
// Anthropic format
getAnthropicTools() → { name, description, input_schema }

// OpenAI format
getOpenAITools() → { type: 'function', function: { name, description, parameters } }

// Bedrock format (in ai-stream.ts)
{ toolSpec: { name, description, inputSchema: { json: input_schema } } }
```

## Adding a New Tool

1. Add to `AI_TOOLS` array in `tools.ts`
2. Add execution logic in `toolExecutor.ts` → `executeTool` switch
3. Implement the handler function `executeMyNewTool(input, context)`
4. Both `getAnthropicTools()` and `getOpenAITools()` will pick it up automatically
5. For Bedrock, the conversion in `ai-stream.ts` is also automatic

## System Prompt Location
Main streaming system prompt: [apps/api/src/routes/ai-stream.ts](apps/api/src/routes/ai-stream.ts) around line 132–172

oRPC chat system prompt: [apps/api/src/orpc/routers/ai/providersWithTools.ts](apps/api/src/orpc/routers/ai/providersWithTools.ts) — `SYSTEM_PROMPT_WITH_TOOLS` constant
