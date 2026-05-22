---
name: Effect AI
description: This skill should be used when the user asks about "Effect AI", "@effect/ai", "LLM integration", "AI tool use", "AI execution planning", "building AI agents", "AI providers", "structured AI output", "AI completions", "Effect OpenAI", "Effect Anthropic", or needs to understand how Effect integrates with AI/LLM services.
version: 1.0.0
---

# Effect AI

## Overview

Effect AI (`@effect/ai`) provides type-safe integration with AI/LLM services:

- **Provider abstraction** - Unified API for OpenAI, Anthropic, etc.
- **Tool use** - Type-safe function calling with Schema
- **Execution planning** - Multi-step AI workflows
- **Structured output** - Schema-validated responses

## Installation

```bash
npm install @effect/ai @effect/ai-openai
# or
npm install @effect/ai @effect/ai-anthropic
```

## Basic Usage

### Creating a Provider

```typescript
import { AiChat } from "@effect/ai"
import { OpenAiChat } from "@effect/ai-openai"
import { Effect, Layer } from "effect"

const OpenAiLive = OpenAiChat.layer({
  apiKey: Config.redacted("OPENAI_API_KEY"),
  model: "gpt-4"
})

import { AnthropicChat } from "@effect/ai-anthropic"

const AnthropicLive = AnthropicChat.layer({
  apiKey: Config.redacted("ANTHROPIC_API_KEY"),
  model: "claude-3-opus-20240229"
})
```

### Simple Completion

```typescript
const program = Effect.gen(function* () {
  const ai = yield* AiChat.AiChat

  const response = yield* ai.generateText({
    prompt: "Explain functional programming in one sentence."
  })

  return response.text
})

const result = yield* program.pipe(
  Effect.provide(OpenAiLive)
)
```

### Chat with Messages

```typescript
const chat = Effect.gen(function* () {
  const ai = yield* AiChat.AiChat

  const response = yield* ai.generateText({
    messages: [
      { role: "system", content: "You are a helpful assistant." },
      { role: "user", content: "What is Effect-TS?" }
    ]
  })

  return response.text
})
```

## Tool Use

Define tools that AI can call:

### Defining Tools with Schema

```typescript
import { AiTool } from "@effect/ai"
import { Schema } from "effect"

const WeatherInput = Schema.Struct({
  city: Schema.String,
  unit: Schema.optional(Schema.Literal("celsius", "fahrenheit"))
})

const getWeather = AiTool.make({
  name: "get_weather",
  description: "Get current weather for a city",
  input: WeatherInput,
  handler: (input) =>
    Effect.succeed({
      city: input.city,
      temperature: 22,
      unit: input.unit ?? "celsius",
      conditions: "sunny"
    })
})
```

### Using Tools in Chat

```typescript
const programWithTools = Effect.gen(function* () {
  const ai = yield* AiChat.AiChat

  const response = yield* ai.generateText({
    prompt: "What's the weather in Tokyo?",
    tools: [getWeather]
  })

  return response.text
})
```

### Multiple Tools

```typescript
const searchTool = AiTool.make({
  name: "search",
  description: "Search the web",
  input: Schema.Struct({ query: Schema.String }),
  handler: ({ query }) => performSearch(query)
})

const calculatorTool = AiTool.make({
  name: "calculator",
  description: "Perform calculations",
  input: Schema.Struct({
    expression: Schema.String
  }),
  handler: ({ expression }) => evaluate(expression)
})

const response = yield* ai.generateText({
  prompt: "Search for Effect-TS and calculate 2+2",
  tools: [searchTool, calculatorTool]
})
```

## Structured Output

Get typed, validated responses:

```typescript
const ProductReview = Schema.Struct({
  sentiment: Schema.Literal("positive", "negative", "neutral"),
  score: Schema.Number.pipe(Schema.between(1, 5)),
  summary: Schema.String,
  keywords: Schema.Array(Schema.String)
})

const analyzeReview = Effect.gen(function* () {
  const ai = yield* AiChat.AiChat

  const review = yield* ai.generateObject({
    prompt: "Analyze this product review: 'Great product, highly recommend!'",
    schema: ProductReview
  })

  return review
})
```

## Execution Planning

For complex multi-step AI workflows:

```typescript
import { AiPlan } from "@effect/ai"

const researchPlan = AiPlan.make({
  name: "research",
  description: "Research a topic and summarize findings",
  steps: [
    {
      name: "search",
      description: "Search for relevant information",
      tool: searchTool
    },
    {
      name: "analyze",
      description: "Analyze search results",
      handler: (context) =>
        Effect.gen(function* () {
          const ai = yield* AiChat.AiChat
          return yield* ai.generateText({
            prompt: `Analyze these results: ${context.previousResults}`
          })
        })
    },
    {
      name: "summarize",
      description: "Create final summary",
      handler: (context) =>
        Effect.gen(function* () {
          const ai = yield* AiChat.AiChat
          return yield* ai.generateObject({
            prompt: `Summarize: ${context.analysis}`,
            schema: ResearchSummary
          })
        })
    }
  ]
})

const result = yield* AiPlan.execute(researchPlan, {
  topic: "Effect-TS benefits"
})
```

## Streaming Responses

```typescript
import { Stream } from "effect"

const streamProgram = Effect.gen(function* () {
  const ai = yield* AiChat.AiChat

  const stream = yield* ai.streamText({
    prompt: "Write a short story about a robot."
  })

  yield* Stream.runForEach(stream, (chunk) =>
    Effect.sync(() => process.stdout.write(chunk))
  )
})
```

## Provider Configuration

### OpenAI Options

```typescript
const OpenAiLive = OpenAiChat.layer({
  apiKey: Config.redacted("OPENAI_API_KEY"),
  model: "gpt-4-turbo",
  temperature: 0.7,
  maxTokens: 1000,
  organizationId: Config.string("OPENAI_ORG_ID").pipe(Config.option)
})
```

### Anthropic Options

```typescript
const AnthropicLive = AnthropicChat.layer({
  apiKey: Config.redacted("ANTHROPIC_API_KEY"),
  model: "claude-3-opus-20240229",
  maxTokens: 4096
})
```

## Error Handling

```typescript
import { AiError } from "@effect/ai"

const safeChat = program.pipe(
  Effect.catchTag("AiRateLimitError", (error) =>
    Effect.gen(function* () {
      yield* Effect.sleep(error.retryAfter)
      return yield* program
    })
  ),
  Effect.catchTag("AiAuthenticationError", () =>
    Effect.fail(new ConfigurationError())
  ),
  Effect.catchTag("AiError", (error) =>
    Effect.gen(function* () {
      yield* Effect.logError("AI error", error)
      return "Sorry, I couldn't process that request."
    })
  )
)
```

## Testing

```typescript
const MockAiLive = Layer.succeed(
  AiChat.AiChat,
  {
    generateText: () =>
      Effect.succeed({ text: "Mock response" }),
    generateObject: (options) =>
      Effect.succeed(mockData),
    streamText: () =>
      Effect.succeed(Stream.make("Mock", " ", "stream"))
  }
)

const testProgram = program.pipe(
  Effect.provide(MockAiLive)
)
```

## Best Practices

1. **Use Schema for tools** - Type-safe tool definitions
2. **Handle rate limits** - Implement retry with backoff
3. **Validate responses** - Use generateObject with Schema
4. **Stream long responses** - Better UX for long generations
5. **Mock in tests** - Don't call real APIs in tests

## Additional Resources

For comprehensive Effect AI documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Introduction to Effect AI" for overview
- "Tool Use" for function calling
- "Execution Planning" for multi-step workflows
