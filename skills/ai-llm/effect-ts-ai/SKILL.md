---
name: effect-ts-ai
description: @effect/ai integration patterns for categorical AI composition, typed error handling, and production prompt pipelines. Use when building AI applications with Effect-TS, composing LLM calls with typed errors, creating tool-augmented AI systems, or integrating multiple AI providers.
---

# Effect-TS AI Integration

Production-ready categorical AI composition using `@effect/ai` and the Effect ecosystem.

## Installation

```bash
npm install effect @effect/ai @effect/ai-openai @effect/ai-anthropic @effect/platform
```

## Core Architecture

The `@effect/ai` package provides categorical abstractions for AI operations:

- **AiLanguageModel**: Functor over text/structured generation
- **AiToolkit**: Product type of available tools
- **AiResponse**: Coproduct capturing success/failure outcomes
- **AiTool**: Exponential object `Parameters → Effect<Success, Failure>`

## Provider Setup

### OpenAI Configuration

```typescript
import { OpenAiClient, OpenAiLanguageModel } from "@effect/ai-openai"
import { Layer, Config } from "effect"

const OpenAiLive = OpenAiClient.layerConfig({
  apiKey: Config.secret("OPENAI_API_KEY")
})

const ModelLive = OpenAiLanguageModel.model("gpt-4o").pipe(
  Layer.provide(OpenAiLive)
)
```

### Anthropic Configuration

```typescript
import { AnthropicClient, AnthropicLanguageModel } from "@effect/ai-anthropic"
import { Layer, Config } from "effect"

const AnthropicLive = AnthropicClient.layerConfig({
  apiKey: Config.secret("ANTHROPIC_API_KEY")
})

const ModelLive = AnthropicLanguageModel.model("claude-sonnet-4-20250514").pipe(
  Layer.provide(AnthropicLive)
)
```

## Text Generation

### Basic Generation

```typescript
import { AiLanguageModel } from "@effect/ai"
import { Effect } from "effect"

const generateText = Effect.gen(function*() {
  const model = yield* AiLanguageModel.AiLanguageModel
  const response = yield* model.generateText({
    prompt: "Explain monads in one sentence"
  })
  return response.text
})
```

### Streaming Generation

```typescript
import { AiLanguageModel } from "@effect/ai"
import { Effect, Stream } from "effect"

const streamText = Effect.gen(function*() {
  const model = yield* AiLanguageModel.AiLanguageModel
  const stream = yield* model.streamText({
    prompt: "Write a haiku about functional programming"
  })

  yield* Stream.runForEach(stream.textStream, (chunk) =>
    Effect.sync(() => process.stdout.write(chunk))
  )
})
```

## Structured Output Generation

Generate typed objects using Schema validation:

```typescript
import { AiLanguageModel } from "@effect/ai"
import { Effect, Schema } from "effect"

class Sentiment extends Schema.Class<Sentiment>("Sentiment")({
  score: Schema.Number.pipe(
    Schema.greaterThanOrEqualTo(-1),
    Schema.lessThanOrEqualTo(1)
  ),
  label: Schema.Literal("positive", "negative", "neutral"),
  confidence: Schema.Number.pipe(
    Schema.greaterThanOrEqualTo(0),
    Schema.lessThanOrEqualTo(1)
  )
}) {}

const analyzeSentiment = (text: string) =>
  Effect.gen(function*() {
    const model = yield* AiLanguageModel.AiLanguageModel
    const response = yield* model.generateObject({
      prompt: `Analyze sentiment: "${text}"`,
      schema: Sentiment
    })
    return response.value
  })
```

## Tool-Augmented Generation

### Defining Tools

```typescript
import { AiTool, AiToolkit } from "@effect/ai"
import { Schema, Effect } from "effect"

const WeatherTool = AiTool.make("get_weather", {
  description: "Get current weather for a location",
  parameters: Schema.Struct({
    location: Schema.String,
    unit: Schema.optional(Schema.Literal("celsius", "fahrenheit"))
  }),
  success: Schema.Struct({
    temperature: Schema.Number,
    condition: Schema.String
  })
})

const CalculatorTool = AiTool.make("calculate", {
  description: "Perform mathematical calculations",
  parameters: Schema.Struct({
    expression: Schema.String
  }),
  success: Schema.Number
})
```

### Creating Toolkits

```typescript
const MyToolkit = AiToolkit.make(WeatherTool, CalculatorTool)

const ToolkitLive = MyToolkit.toLayer(
  Effect.succeed({
    get_weather: ({ location, unit }) =>
      Effect.succeed({
        temperature: 22,
        condition: "sunny"
      }),
    calculate: ({ expression }) =>
      Effect.try(() => eval(expression) as number)
  })
)
```

### Using Tools in Generation

```typescript
const generateWithTools = Effect.gen(function*() {
  const model = yield* AiLanguageModel.AiLanguageModel
  const response = yield* model.generateText({
    prompt: "What's the weather in Tokyo and what is 42 * 17?",
    toolkit: MyToolkit
  })
  return response.text
})

// Execute with all layers
const program = generateWithTools.pipe(
  Effect.provide(ModelLive),
  Effect.provide(ToolkitLive)
)
```

## Categorical Composition Patterns

### Functor: Mapping Over Responses

```typescript
import { AiResponse } from "@effect/ai"
import { Effect } from "effect"

const mapResponse = <A, B>(
  response: Effect.Effect<AiResponse.AiResponse, Error>,
  f: (text: string) => B
) =>
  Effect.map(response, (r) => f(r.text))
```

### Monad: Sequencing AI Operations

```typescript
const chainedGeneration = Effect.gen(function*() {
  const model = yield* AiLanguageModel.AiLanguageModel

  // First call: generate outline
  const outline = yield* model.generateText({
    prompt: "Create an outline for an essay on category theory"
  })

  // Second call: expand each section (dependent on first)
  const expanded = yield* model.generateText({
    prompt: `Expand this outline into full paragraphs:\n${outline.text}`
  })

  return expanded.text
})
```

### Applicative: Parallel AI Operations

```typescript
import { Effect } from "effect"

const parallelGeneration = Effect.gen(function*() {
  const model = yield* AiLanguageModel.AiLanguageModel

  const [summary, keywords, sentiment] = yield* Effect.all([
    model.generateText({ prompt: "Summarize: ..." }),
    model.generateObject({ prompt: "Extract keywords", schema: KeywordsSchema }),
    model.generateObject({ prompt: "Analyze sentiment", schema: Sentiment })
  ], { concurrency: 3 })

  return { summary: summary.text, keywords: keywords.value, sentiment: sentiment.value }
})
```

### Natural Transformation: Provider Switching

```typescript
import { Layer } from "effect"

// Natural transformation: OpenAI → Anthropic
const switchProvider = <R, E, A>(
  program: Effect.Effect<A, E, R | AiLanguageModel.AiLanguageModel>
): Effect.Effect<A, E, R | AnthropicClient.AnthropicClient> =>
  program.pipe(
    Effect.provide(AnthropicLanguageModel.model("claude-sonnet-4-20250514"))
  )
```

## Error Handling

### Typed AI Errors

```typescript
import { AiError } from "@effect/ai"
import { Effect, Match } from "effect"

const handleAiErrors = <A>(effect: Effect.Effect<A, AiError.AiError>) =>
  effect.pipe(
    Effect.catchTag("AiError", (error) =>
      Match.value(error.reason).pipe(
        Match.when({ _tag: "RateLimitExceeded" }, () =>
          Effect.fail(new Error("Rate limited, retry later"))
        ),
        Match.when({ _tag: "InvalidRequest" }, ({ message }) =>
          Effect.fail(new Error(`Invalid request: ${message}`))
        ),
        Match.orElse(() => Effect.fail(new Error("Unknown AI error")))
      )
    )
  )
```

### Retry with Exponential Backoff

```typescript
import { Effect, Schedule } from "effect"

const withRetry = <A, E, R>(effect: Effect.Effect<A, E, R>) =>
  effect.pipe(
    Effect.retry(
      Schedule.exponential("100 millis").pipe(
        Schedule.compose(Schedule.recurs(3))
      )
    )
  )
```

## Production Patterns

### Telemetry Integration

```typescript
import { AiTelemetry } from "@effect/ai"
import { Effect } from "effect"

const withTelemetry = <A, E, R>(
  operation: string,
  effect: Effect.Effect<A, E, R>
) =>
  effect.pipe(
    Effect.tap(() =>
      Effect.logInfo(`AI operation: ${operation}`)
    ),
    Effect.withSpan(`ai.${operation}`)
  )
```

### Resource Management

```typescript
import { Effect, Scope } from "effect"

const managedAiSession = Effect.scoped(
  Effect.gen(function*() {
    const model = yield* AiLanguageModel.AiLanguageModel

    // Resources automatically cleaned up
    yield* Effect.addFinalizer(() =>
      Effect.logInfo("AI session closed")
    )

    return yield* model.generateText({
      prompt: "Hello, world!"
    })
  })
)
```

### Configuration Management

```typescript
import { Config, Effect, Layer } from "effect"

const AiConfigLive = Layer.effect(
  AiConfig,
  Effect.gen(function*() {
    return {
      maxTokens: yield* Config.integer("AI_MAX_TOKENS").pipe(
        Config.withDefault(4096)
      ),
      temperature: yield* Config.number("AI_TEMPERATURE").pipe(
        Config.withDefault(0.7)
      ),
      model: yield* Config.string("AI_MODEL").pipe(
        Config.withDefault("gpt-4o")
      )
    }
  })
)
```

## MCP Integration

Register tools with MCP servers:

```typescript
import { McpServer } from "@effect/ai"
import { Layer } from "effect"

const McpToolsLive = McpServer.toolkit(MyToolkit).pipe(
  Layer.provide(ToolkitLive)
)
```

## Testing

### Mock Language Model

```typescript
import { AiLanguageModel } from "@effect/ai"
import { Layer, Effect } from "effect"

const MockModelLive = Layer.succeed(
  AiLanguageModel.AiLanguageModel,
  AiLanguageModel.make({
    generateText: (options) =>
      Effect.succeed({
        text: `Mock response for: ${options.prompt}`,
        toolCalls: [],
        finishReason: "stop"
      }),
    generateObject: (options) =>
      Effect.succeed({
        value: { mocked: true },
        finishReason: "stop"
      })
  })
)
```

## Categorical Guarantees

The @effect/ai library preserves these categorical properties:

1. **Functor Laws**: `map(id) ≡ id`, `map(f ∘ g) ≡ map(f) ∘ map(g)`
2. **Monad Laws**: `flatMap(pure) ≡ id`, `pure(a).flatMap(f) ≡ f(a)`
3. **Natural Transformation**: Provider switching preserves structure
4. **Resource Safety**: Scoped effects guarantee cleanup via finalizers
5. **Type Safety**: Schema validation at compile-time and runtime
