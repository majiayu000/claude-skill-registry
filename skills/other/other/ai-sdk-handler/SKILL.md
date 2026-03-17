---
description: Integrate Vercel AI SDK for LLMs, Chatbots, Generative UI, and Agentic Workflows.
deps: ["auth-handler", "inngest-handler"]
---

# AI SDK Handler

This skill defines how to implement Large Language Model (LLM) features using the Vercel AI SDK. It covers streaming chat, structured object generation, generative UI, and background agents.

**Note**: For Image/Video generation (Replicate, Fal.ai), continue to use `ai-handler`. Use `ai-sdk-handler` specifically for text, chat, and agentic text/JSON workflows.

## When to Use
- **Chatbots**: Building interactive chat interfaces (`useChat`, `streamText`).
- **Structured Data**: Extracting JSON from text (`generateObject`).
- **Generative UI**: Streaming React components directly from the server (`streamUI`).
- **Agents**: Complex, multi-step reasoning tasks (often combined with Inngest).
- **Multimodal**: Handling image inputs with text.

## Capabilities

### 1. Streaming Chat
- **Tool**: `streamText` (Server), `useChat` (Client).
- **Pattern**: Create a route handler at `src/app/api/chat/route.ts`.
- **Auth**: Wrap with `withAuthRequired` to protect the route.
- **UI**: Use `src/components/chat-ui/` for chat components.

### 2. Generative UI (RSC)
- **Tool**: `streamUI` (Server).
- **Pattern**: Return React components based on tool calls.
- **Use Case**: Dashboards that build themselves, dynamic reports.

### 3. Structured Object Generation
- **Tool**: `generateObject`.
- **Pattern**: Define a Zod schema and get strictly typed JSON back.
- **Use Case**: Populating database forms, extracting itinerary details, categorizing content.

### 4. Background Agents (with Inngest)
- **Tool**: `generateText` / `generateObject` inside Inngest steps.
- **Why**: Next.js Server Actions/Routes have timeouts (max 60s usually). Agents taking longer must run in the background.
- **Pattern**:
    1. Trigger Inngest event from UI.
    2. Inngest function runs the LLM logic (loops, multi-step).
    3. Store result in DB or notify user.
    4. **Docs**: [AI SDK Agents](https://ai-sdk.dev/docs/agents/overview).

## Best Practices

1.  **Streaming**: Always prefer streaming for text generation > 2 seconds to improve perceived latency.
2.  **Auth**: Never expose open AI routes. Always verify `session.user.id`.
3.  **Providers**: Use `@ai-sdk/openai` or `@ai-sdk/anthropic`. Abstract the provider configuration in `src/lib/ai/index.ts`.
4.  **Backpressure**: The AI SDK handles this automatically in `streamText`.
5.  **Caching**: Use `unstable_cache` or KV stores if queries are repetitive.
6.  **Prompt Engineering**: Keep prompts in a dedicated folder or constant file if they are complex.

## Documentation & Examples

-   **`reference.md`**: Core setup and essential code snippets.
-   **`examples.md`**: Exhaustive examples covering:
    1.  Basic Chat
    2.  Generative UI
    3.  Structured Object Generation
    4.  Agents & Workflows (Loop Control)
    5.  Caching
    6.  Streaming Data
    7.  Reading UI Streams
    8.  Handling Backpressure
    9.  Multimodal Chat
