---
name: libagent
description: >
  libagent - Agent orchestration library for conversational AI. AgentMind class
  coordinates LLM completions, memory management, tool execution, and multi-turn
  conversations. AgentAction handles tool calls and action processing. Use for
  building chat agents, RAG pipelines, and AI assistants. Integrates with
  libmemory, librpc, and libllm
---

# libagent Skill

## When to Use

- Building conversational AI agents with tool capabilities
- Coordinating LLM completions with memory context
- Processing multi-turn conversations with state
- Implementing RAG (retrieval-augmented generation) pipelines

## Key Concepts

**AgentMind**: Core reasoning engine that processes requests through LLM
completions, manages conversation state, and coordinates tool execution.

**AgentAction**: Handles individual tool calls, executes actions, and returns
results to the conversation flow.

## Usage Patterns

### Pattern 1: Basic agent request

```javascript
import { AgentMind } from "@copilot-ld/libagent";

const mind = new AgentMind(memoryClient, llmClient, toolClient);
const response = await mind.process({
  resourceId: conversationId,
  content: "What is the weather?",
});
```

### Pattern 2: Streaming responses

```javascript
for await (const chunk of mind.stream(request)) {
  process.stdout.write(chunk.content);
}
```

## Integration

Works with `libmemory` for context windows, `librpc` for gRPC clients, and
`libllm` for completions. Used by the Agent service.
