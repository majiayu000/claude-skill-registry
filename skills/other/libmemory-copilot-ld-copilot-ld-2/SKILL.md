---
name: libmemory
description: >
  libmemory - Memory management for LLM context windows. WindowBuilder
  constructs token-limited context from conversation history and tools.
  createWindow factory simplifies window creation. MemoryIndex stores
  conversation identifiers. Use for managing chat history, building LLM prompts,
  and context window optimization.
---

# libmemory Skill

## When to Use

- Building context windows for LLM calls
- Managing conversation history with token limits
- Constructing prompts from messages and tools
- Optimizing context for model token budgets

## Key Concepts

**WindowBuilder**: Constructs context windows by selecting messages and tools
that fit within token budget.

**MemoryIndex**: Stores conversation message identifiers for retrieval.

**Token budgeting**: Allocates tokens across system prompt, history, and tools.

## Usage Patterns

### Pattern 1: Build context window

```javascript
import { WindowBuilder } from "@copilot-ld/libmemory";

const builder = new WindowBuilder(tokenizer);
const window = await builder.build({
  messages: conversationHistory,
  tools: availableTools,
  budget: 4000,
});
```

### Pattern 2: Factory usage

```javascript
import { createWindow } from "@copilot-ld/libmemory";

const window = await createWindow(resourceId, {
  maxTokens: 4000,
  systemPrompt: "You are a helpful assistant.",
});
```

## Integration

Used by Memory service and Agent service. Works with libllm for token counting.
