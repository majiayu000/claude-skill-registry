---
name: ai-sdk-best-practices
description: Production best practices for building AI agents with Vercel AI SDK v5. Covers security, performance, error handling, testing, deployment patterns, and real-world implementation guidelines.
---

# AI SDK v5 Best Practices

Comprehensive guide for building production-ready AI agents with Vercel AI SDK v5.

## Core Principles

### 1. The No-Nonsense Approach (Vercel's Philosophy)

```
1. Prototype by hand → Understand the problem
2. Automate the loop → Let LLM handle decisions
3. Optimize for reliability → Add guardrails, fallbacks
```

**Key insight**: Use LLMs for judgment, plain code for deterministic logic.

```typescript
// BAD: LLM for deterministic task
const { text } = await generateText({
  prompt: 'Calculate 2 + 2'
});

// GOOD: Code for deterministic, LLM for judgment
const sum = 2 + 2;
const { text } = await generateText({
  prompt: `Explain why ${sum} is the answer`
});
```

## Security Best Practices

### API Key Management

```typescript
// .env.local (NEVER commit)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...

// Validate at startup
function validateEnv() {
  const required = ['OPENAI_API_KEY'];
  for (const key of required) {
    if (!process.env[key]) {
      throw new Error(`Missing required env var: ${key}`);
    }
  }
}

// Use server-side only
// app/api/chat/route.ts
import { openai } from '@ai-sdk/openai';

export async function POST(req: Request) {
  // Key is server-side only, never exposed to client
  const model = openai('gpt-4o');
  // ...
}
```

### Prompt Injection Prevention

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

// BAD: Direct user input in system prompt
const badPrompt = `You are a ${userInput} assistant`; // DANGEROUS

// GOOD: Sanitize and constrain
function sanitizeInput(input: string): string {
  return input
    .replace(/ignore previous|system prompt|you are now/gi, '[FILTERED]')
    .slice(0, 1000); // Length limit
}

// BETTER: Structured separation
const { text } = await generateText({
  model: openai('gpt-4o'),
  system: 'You are a helpful assistant. Only answer questions about our product.',
  messages: [
    { role: 'user', content: sanitizeInput(userInput) }
  ]
});
```

### Tool Security (Assume Total Compromise)

```typescript
import { tool } from 'ai';
import { z } from 'zod';

// BAD: Tool with too much power
const badTool = tool({
  description: 'Execute any SQL query',
  parameters: z.object({ query: z.string() }),
  execute: async ({ query }) => db.raw(query) // SQL INJECTION!
});

// GOOD: Scoped, parameterized tool
const goodTool = tool({
  description: 'Get user by ID',
  parameters: z.object({
    userId: z.string().uuid() // Validated format
  }),
  execute: async ({ userId }) => {
    // Parameterized query
    return db.users.findUnique({ where: { id: userId } });
  }
});

// BEST: Bind sensitive params server-side
function createUserTool(authenticatedUserId: string) {
  return tool({
    description: 'Get current user profile',
    parameters: z.object({}), // No user-controllable params
    execute: async () => {
      // User ID bound at tool creation, not from LLM
      return db.users.findUnique({ where: { id: authenticatedUserId } });
    }
  });
}
```

### Output Sanitization

```typescript
import DOMPurify from 'dompurify';

// Sanitize before rendering
function sanitizeOutput(llmOutput: string): string {
  // Remove potential XSS in markdown/HTML
  return DOMPurify.sanitize(llmOutput, {
    ALLOWED_TAGS: ['p', 'b', 'i', 'em', 'strong', 'code', 'pre'],
    ALLOWED_ATTR: []
  });
}

// For code execution contexts
function sanitizeForExecution(output: string): string {
  // Strip anything that looks like code injection
  return output.replace(/[`${}]/g, '');
}
```

## Error Handling

### Tool-Specific Errors

```typescript
import {
  generateText,
  NoSuchToolError,
  InvalidToolArgumentsError,
  ToolExecutionError
} from 'ai';

async function robustAgent(prompt: string) {
  try {
    const { text } = await generateText({
      model: openai('gpt-4o'),
      tools: myTools,
      prompt
    });
    return { success: true, text };
  } catch (error) {
    if (error instanceof NoSuchToolError) {
      console.error(`Unknown tool: ${error.toolName}`);
      return { success: false, error: 'Tool not found' };
    }
    if (error instanceof InvalidToolArgumentsError) {
      console.error(`Invalid args for ${error.toolName}:`, error.message);
      return { success: false, error: 'Invalid tool parameters' };
    }
    if (error instanceof ToolExecutionError) {
      console.error(`Tool ${error.toolName} failed:`, error.cause);
      return { success: false, error: 'Tool execution failed' };
    }
    throw error; // Unknown error
  }
}
```

### Streaming Error Handling

```typescript
import { streamText } from 'ai';

async function streamWithErrorHandling(prompt: string) {
  const result = await streamText({
    model: openai('gpt-4o'),
    prompt,
    onError: ({ error }) => {
      console.error('Stream error:', error);
      // Could send to error tracking service
    }
  });

  // Handle errors in stream consumption
  try {
    for await (const chunk of result.textStream) {
      process.stdout.write(chunk);
    }
  } catch (error) {
    console.error('Stream consumption error:', error);
  }
}
```

### Retry with Exponential Backoff

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      // Don't retry on validation errors
      if (error instanceof InvalidToolArgumentsError) {
        throw error;
      }

      // Exponential backoff
      const delay = baseDelay * Math.pow(2, attempt);
      console.log(`Attempt ${attempt + 1} failed, retrying in ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw lastError!;
}

// Usage
const result = await withRetry(() =>
  generateText({ model: openai('gpt-4o'), prompt: 'Hello' })
);
```

## Performance Optimization

### Streaming Best Practices

```typescript
import { streamText } from 'ai';

// Server-side streaming endpoint
export async function POST(req: Request) {
  const { prompt } = await req.json();

  const result = await streamText({
    model: openai('gpt-4o'),
    prompt,
    // Throttle UI updates for smooth rendering
    experimental_throttleTimeMilliseconds: 50
  });

  // Return SSE stream
  return result.toDataStreamResponse();
}
```

### Parallel Tool Execution

```typescript
import { generateText, tool } from 'ai';
import { z } from 'zod';

// Tools that can run in parallel
const tools = {
  fetchWeather: tool({
    description: 'Get weather for a city',
    parameters: z.object({ city: z.string() }),
    execute: async ({ city }) => fetchWeather(city)
  }),
  fetchNews: tool({
    description: 'Get news for a topic',
    parameters: z.object({ topic: z.string() }),
    execute: async ({ topic }) => fetchNews(topic)
  })
};

// AI SDK automatically parallelizes independent tool calls
const { text } = await generateText({
  model: openai('gpt-4o'),
  tools,
  prompt: 'What\'s the weather in NYC and latest tech news?'
  // Both tools run in parallel when LLM requests them together
});
```

### Context Window Management

```typescript
import { generateText } from 'ai';

// Estimate tokens (rough: 1 token ≈ 4 chars)
function estimateTokens(text: string): number {
  return Math.ceil(text.length / 4);
}

// Truncate to fit context
function fitToContext(
  messages: string[],
  maxTokens: number,
  reserveForResponse: number = 1000
): string[] {
  const available = maxTokens - reserveForResponse;
  const result: string[] = [];
  let used = 0;

  // Keep most recent messages
  for (let i = messages.length - 1; i >= 0; i--) {
    const tokens = estimateTokens(messages[i]);
    if (used + tokens > available) break;
    result.unshift(messages[i]);
    used += tokens;
  }

  return result;
}
```

### Caching Strategies

```typescript
import { generateText } from 'ai';

// Simple in-memory cache
const cache = new Map<string, { result: string; timestamp: number }>();
const CACHE_TTL = 60 * 60 * 1000; // 1 hour

async function cachedGeneration(prompt: string): Promise<string> {
  const cacheKey = prompt; // In production, use hash

  const cached = cache.get(cacheKey);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.result;
  }

  const { text } = await generateText({
    model: openai('gpt-4o'),
    prompt
  });

  cache.set(cacheKey, { result: text, timestamp: Date.now() });
  return text;
}
```

## Testing Patterns

### Unit Testing Tools

```typescript
import { tool } from 'ai';
import { z } from 'zod';
import { describe, it, expect } from 'vitest';

const calculatorTool = tool({
  description: 'Perform calculations',
  parameters: z.object({
    expression: z.string()
  }),
  execute: async ({ expression }) => {
    return { result: eval(expression) };
  }
});

describe('Calculator Tool', () => {
  it('should calculate correctly', async () => {
    const result = await calculatorTool.execute({ expression: '2 + 2' });
    expect(result.result).toBe(4);
  });

  it('should handle complex expressions', async () => {
    const result = await calculatorTool.execute({ expression: '(10 + 5) * 2' });
    expect(result.result).toBe(30);
  });
});
```

### Integration Testing Agents

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { describe, it, expect } from 'vitest';

describe('Weather Agent', () => {
  it('should use weather tool for weather queries', async () => {
    const toolCalls: string[] = [];

    const { text } = await generateText({
      model: openai('gpt-4o'),
      tools: {
        getWeather: tool({
          description: 'Get weather',
          parameters: z.object({ city: z.string() }),
          execute: async ({ city }) => {
            toolCalls.push('getWeather');
            return { temp: 72, condition: 'sunny' };
          }
        })
      },
      prompt: 'What\'s the weather in NYC?'
    });

    expect(toolCalls).toContain('getWeather');
    expect(text).toContain('72'); // Or appropriate assertion
  });
});
```

### Mocking for Tests

```typescript
import { createMockModel } from './test-utils';

// Create mock model for testing
function createMockModel(responses: string[]) {
  let index = 0;
  return {
    doGenerate: async () => ({
      text: responses[index++] || 'Default response'
    })
  };
}

// Test with mock
it('should handle multi-turn conversation', async () => {
  const mockModel = createMockModel([
    'Hello! How can I help?',
    'I can help with that task.'
  ]);

  const result1 = await generateText({ model: mockModel, prompt: 'Hi' });
  const result2 = await generateText({ model: mockModel, prompt: 'Help me' });

  expect(result1.text).toBe('Hello! How can I help?');
  expect(result2.text).toBe('I can help with that task.');
});
```

## Deployment Patterns

### Edge Runtime Configuration

```typescript
// app/api/chat/route.ts
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export const runtime = 'edge'; // Deploy to edge

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = await streamText({
    model: openai('gpt-4o'),
    messages
  });

  return result.toDataStreamResponse();
}
```

### Long-Running with Background Tasks

```typescript
// For Vercel: Use maxDuration for longer operations
export const maxDuration = 300; // 5 minutes

export async function POST(req: Request) {
  const { task } = await req.json();

  // Long-running agent task
  const { text } = await generateText({
    model: openai('gpt-4o'),
    tools: complexTools,
    maxSteps: 20,
    prompt: task
  });

  return Response.json({ result: text });
}
```

## Observability

### Logging Best Practices

```typescript
import { generateText } from 'ai';

async function observableAgent(prompt: string) {
  const startTime = Date.now();

  const { text, steps, usage } = await generateText({
    model: openai('gpt-4o'),
    tools: myTools,
    prompt,
    onStepFinish: ({ stepType, toolCalls, toolResults }) => {
      console.log(JSON.stringify({
        event: 'step_complete',
        stepType,
        tools: toolCalls?.map(t => t.toolName),
        timestamp: Date.now()
      }));
    }
  });

  console.log(JSON.stringify({
    event: 'generation_complete',
    duration: Date.now() - startTime,
    steps: steps.length,
    tokens: usage
  }));

  return text;
}
```

## Quick Reference

### Import Patterns

```typescript
// Core functions
import { generateText, streamText, generateObject } from 'ai';

// Providers
import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';
import { google } from '@ai-sdk/google';

// Tools and schemas
import { tool } from 'ai';
import { z } from 'zod';

// Errors
import {
  NoSuchToolError,
  InvalidToolArgumentsError,
  ToolExecutionError
} from 'ai';

// Embeddings
import { embed, embedMany, cosineSimilarity } from 'ai';
```

### Common Patterns Cheatsheet

| Need | Function | Key Options |
|------|----------|-------------|
| Single response | `generateText()` | `maxSteps`, `tools` |
| Streaming | `streamText()` | `onStepFinish`, `throttle` |
| Structured data | `generateObject()` | `schema` (Zod) |
| Embeddings | `embed()` / `embedMany()` | model |
| Tool forcing | `toolChoice` | `'required'`, `{ type: 'tool', toolName }` |
| Loop control | `stopWhen` | `stepCountIs(n)` |

## Related Skills

- `agentic-patterns` - Design patterns for building agents
- `ai-sdk-planner` - Planning agent for AI SDK architectures
