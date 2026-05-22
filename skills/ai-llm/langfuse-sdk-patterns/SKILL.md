---
name: langfuse-sdk-patterns
description: |
  Langfuse SDK best practices, patterns, and idiomatic usage.
  Use when learning Langfuse SDK patterns, implementing proper tracing,
  or following best practices for LLM observability.
  Trigger with phrases like "langfuse patterns", "langfuse best practices",
  "langfuse SDK guide", "how to use langfuse", "langfuse idioms".
allowed-tools: Read, Write, Edit
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Langfuse SDK Patterns

## Overview
Best practices and idiomatic patterns for using the Langfuse SDK effectively.

## Prerequisites
- Completed `langfuse-install-auth` setup
- Understanding of async/await patterns
- Familiarity with LLM application structure

## Core Concepts

### Trace Hierarchy
```
Trace (top-level, represents complete operation)
├── Span (child operation, any processing step)
│   ├── Span (nested spans allowed)
│   └── Generation (LLM call)
├── Generation (LLM call)
└── Event (point-in-time occurrence)
```

## Instructions

### Pattern 1: Singleton Client Instance

```typescript
// lib/langfuse.ts - Single instance, reused everywhere
import { Langfuse } from "langfuse";

let langfuseInstance: Langfuse | null = null;

export function getLangfuse(): Langfuse {
  if (!langfuseInstance) {
    langfuseInstance = new Langfuse({
      publicKey: process.env.LANGFUSE_PUBLIC_KEY!,
      secretKey: process.env.LANGFUSE_SECRET_KEY!,
      baseUrl: process.env.LANGFUSE_HOST,
    });
  }
  return langfuseInstance;
}

// Clean shutdown
export async function shutdownLangfuse(): Promise<void> {
  if (langfuseInstance) {
    await langfuseInstance.shutdownAsync();
    langfuseInstance = null;
  }
}
```

### Pattern 2: Proper Trace Lifecycle

```typescript
import { getLangfuse } from "./lib/langfuse";

async function handleRequest(request: Request) {
  const langfuse = getLangfuse();

  // 1. Create trace at operation start
  const trace = langfuse.trace({
    name: "api/chat",
    userId: request.userId,
    sessionId: request.sessionId,
    input: request.body,
    metadata: {
      endpoint: "/api/chat",
      method: "POST",
    },
  });

  try {
    // 2. Do work with spans/generations
    const result = await processRequest(trace, request);

    // 3. Update trace with success output
    trace.update({
      output: result,
      metadata: { status: "success" },
    });

    return result;
  } catch (error) {
    // 4. Update trace with error
    trace.update({
      output: { error: String(error) },
      level: "ERROR",
      statusMessage: String(error),
    });
    throw error;
  }
  // Note: Don't await flush here in request handlers
  // Langfuse batches and flushes automatically
}
```

### Pattern 3: Nested Spans for Complex Operations

```typescript
async function processRequest(
  trace: ReturnType<typeof langfuse.trace>,
  request: Request
) {
  // Parent span for the entire process
  const processSpan = trace.span({
    name: "process-request",
    input: request.body,
  });

  // Child span for validation
  const validateSpan = processSpan.span({
    name: "validate-input",
    input: request.body,
  });

  const validatedInput = await validateInput(request.body);
  validateSpan.end({ output: validatedInput });

  // Child span for retrieval (e.g., RAG)
  const retrieveSpan = processSpan.span({
    name: "retrieve-context",
    input: { query: validatedInput.query },
  });

  const context = await retrieveContext(validatedInput.query);
  retrieveSpan.end({
    output: { documentCount: context.length },
    metadata: { source: "vector-db" },
  });

  // Generation for LLM call
  const generation = processSpan.generation({
    name: "generate-response",
    model: "gpt-4",
    input: {
      messages: buildMessages(validatedInput, context),
    },
  });

  const response = await callLLM(validatedInput, context);

  generation.end({
    output: response.content,
    usage: {
      promptTokens: response.usage.prompt_tokens,
      completionTokens: response.usage.completion_tokens,
    },
  });

  processSpan.end({ output: response });
  return response;
}
```

### Pattern 4: Decorators for Clean Code (Python)

```python
from langfuse.decorators import observe, langfuse_context

@observe()
def process_request(user_input: str) -> str:
    """Automatically creates a trace with function name."""
    # Add metadata to current observation
    langfuse_context.update_current_observation(
        metadata={"input_length": len(user_input)}
    )

    validated = validate_input(user_input)
    context = retrieve_context(validated)
    response = generate_response(validated, context)

    return response

@observe()
def validate_input(user_input: str) -> dict:
    """Creates a child span automatically."""
    return {"query": user_input.strip(), "valid": True}

@observe()
def retrieve_context(query: dict) -> list:
    """Another child span."""
    langfuse_context.update_current_observation(
        metadata={"query": query}
    )
    return ["context1", "context2"]

@observe(as_type="generation")
def generate_response(query: dict, context: list) -> str:
    """Creates a generation observation."""
    langfuse_context.update_current_observation(
        model="gpt-4",
        model_parameters={"temperature": 0.7},
        usage={"prompt_tokens": 100, "completion_tokens": 50},
    )
    return "Generated response"
```

### Pattern 5: Session and User Tracking

```typescript
// Track conversations across multiple requests
function createConversationTrace(
  userId: string,
  sessionId: string,
  turn: number
) {
  return langfuse.trace({
    name: "conversation-turn",
    userId,
    sessionId, // Links traces into a session view
    metadata: {
      turn,
      timestamp: new Date().toISOString(),
    },
    tags: ["conversation"],
  });
}

// Usage
const trace = createConversationTrace(
  "user-123",
  "session-abc", // Same session across turns
  3 // Turn number
);
```

### Pattern 6: Scores and Evaluation

```typescript
// Add scores to traces for evaluation
const trace = langfuse.trace({ name: "scored-operation" });

// After operation completes, add scores
langfuse.score({
  traceId: trace.id,
  name: "accuracy",
  value: 0.95, // Numeric score
  comment: "High accuracy response",
});

langfuse.score({
  traceId: trace.id,
  name: "user-feedback",
  value: 1, // Boolean as 0/1
  comment: "User thumbs up",
});

langfuse.score({
  traceId: trace.id,
  observationId: generation.id, // Score specific generation
  name: "relevance",
  value: 0.8,
});
```

## Output
- Singleton client pattern for consistent tracing
- Proper trace lifecycle management
- Nested spans for complex operations
- Clean decorator-based tracing (Python)
- Session and user tracking
- Evaluation and scoring integration

## Error Handling
| Pattern | Issue | Best Practice |
|---------|-------|---------------|
| Client creation | Multiple instances | Use singleton pattern |
| Trace updates | Missing outputs | Always update on success/error |
| Span nesting | Orphaned spans | Always call `.end()` |
| Flush timing | Lost data | Use `shutdownAsync()` on exit |
| Scoring | Invalid values | Use 0-1 range for consistency |

## Examples

### Complete TypeScript Pattern
```typescript
import { Langfuse } from "langfuse";

const langfuse = new Langfuse();

interface ChatRequest {
  userId: string;
  sessionId: string;
  message: string;
}

async function chat(request: ChatRequest) {
  const trace = langfuse.trace({
    name: "chat",
    userId: request.userId,
    sessionId: request.sessionId,
    input: { message: request.message },
  });

  const span = trace.span({ name: "process" });

  try {
    const generation = span.generation({
      name: "llm-call",
      model: "gpt-4",
      input: [{ role: "user", content: request.message }],
    });

    const response = await callOpenAI(request.message);

    generation.end({
      output: response.content,
      usage: response.usage,
    });

    span.end({ output: { response: response.content } });
    trace.update({ output: { response: response.content } });

    return response.content;
  } catch (error) {
    span.end({ level: "ERROR", statusMessage: String(error) });
    trace.update({ level: "ERROR", output: { error: String(error) } });
    throw error;
  }
}
```

## Resources
- [Langfuse Tracing Guide](https://langfuse.com/docs/tracing)
- [Langfuse Python Decorators](https://langfuse.com/docs/sdk/python/decorators)
- [Langfuse Scores](https://langfuse.com/docs/scores)

## Next Steps
For core tracing workflows, see `langfuse-core-workflow-a`.
