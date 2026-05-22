---
name: ai-sdk
description: Comprehensive guide to AI SDK v6 for agent development, tool definitions, multi-step agentic workflows, and result extraction patterns
---

# Vercel AI SDK v6 Patterns

## Zod 4.x

This repo uses **Zod 4.x** (4.3.5+) directly:

```typescript
// ✅ Standard Zod 4 import
import { z } from 'zod'
```

Zod 4's optimized types work well with AI SDK v6's recursive generics.

---

Comprehensive guide for Vercel AI SDK v6 (6.0+) patterns used in agent-first applications. Contains rules for provider setup, tool definitions, multi-step workflows, and result extraction.

## When to Apply

Reference these guidelines when:
- Setting up AI model providers
- Defining agent tools with tool()
- Implementing multi-step agentic workflows
- Extracting results from generateText/streamText
- Migrating from AI SDK v5 to v6

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Provider Setup | CRITICAL | `provider-` |
| 2 | Text Generation | HIGH | `generate-` |
| 3 | Tool Definitions | HIGH | `tool-` |
| 4 | Multi-Step Agents | HIGH | `agent-` |
| 5 | Result Extraction | MEDIUM | `result-` |
| 6 | Message Types | MEDIUM | `message-` |
| 7 | Error Handling | MEDIUM | `error-` |

## Quick Reference

### Critical v6 Breaking Changes

```typescript
// ❌ v5 patterns that FAIL in v6:
import { type CoreMessage } from 'ai'     // → ModelMessage
parameters: z.object({...})               // → inputSchema
maxSteps: 5                               // → stopWhen: stepCountIs(5)
call.args                                 // → call.input
call.toolResult                           // → step.toolResults[].output
```

### 1. Provider Setup (CRITICAL)

- `provider-gateway` - Use AI Gateway model strings (recommended)

```typescript
import { generateText } from 'ai'

const result = await generateText({
  model: 'anthropic/claude-opus-4-5',  // AI Gateway string
  prompt: 'Hello',
})
```

**No provider wrapper is required** when using AI Gateway model strings.

### 2. Text Generation (HIGH)

- `generate-basic` - Core generateText pattern

### 3. Tool Definitions (HIGH)

- `tool-input-schema` - v6 uses inputSchema not parameters
- `tool-definition` - Complete tool() pattern

```typescript
import { tool } from 'ai'
import { z } from 'zod'

const myTool = tool({
  description: 'What this does',
  inputSchema: z.object({  // ✅ inputSchema not parameters
    param: z.string().describe('Description'),
  }),
  execute: async ({ param }) => {
    return { result: 'done' }
  },
})
```

### 4. Multi-Step Agents (HIGH)

- `agent-stop-when` - v6 uses stopWhen not maxSteps
- `agent-multi-step` - Complete agent pattern

```typescript
import { generateText, stepCountIs } from 'ai'

const result = await generateText({
  model: 'anthropic/claude-opus-4-5',
  messages,
  tools: agentTools,
  stopWhen: stepCountIs(5),  // ✅ not maxSteps: 5
})
```

### 5. Result Extraction (MEDIUM)

- `result-tool-access` - Access tool calls and results correctly

```typescript
// ✅ Correct v6 pattern
const toolCalls = result.steps.flatMap((step) => {
  const resultsMap = new Map(
    (step.toolResults || []).map((r) => [r.toolCallId, r.output])
  )
  return (step.toolCalls || []).map((tc) => ({
    name: tc.toolName,
    args: tc.input,  // ✅ input not args
    result: resultsMap.get(tc.toolCallId),  // ✅ from toolResults
  }))
})
```

### 6. Message Types (MEDIUM)

- `message-model-message` - Use ModelMessage type

```typescript
import { type ModelMessage } from 'ai'  // ✅ not CoreMessage

const messages: ModelMessage[] = [
  { role: 'user', content: 'Hello' },
]
```

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/provider-gateway.md
rules/tool-input-schema.md
rules/agent-stop-when.md
rules/result-tool-access.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Reference links

## Key Imports

```typescript
import {
  generateText,
  generateObject,
  streamText,
  streamObject,
  tool,
  stepCountIs,
  hasToolCall,
  type ModelMessage,
} from 'ai'
import { z } from 'zod'  // Zod 4.x
```

## Model Strings (AI Gateway)

```
anthropic/claude-opus-4-5
anthropic/claude-sonnet-4
openai/gpt-4o
google/gemini-2.0-flash
```

Auth: Set `AI_GATEWAY_API_KEY` environment variable.
