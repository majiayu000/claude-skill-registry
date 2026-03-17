---
name: tanstack-ai
description: TanStack AI (alpha) provider-agnostic type-safe chat with streaming for OpenAI, Anthropic, Gemini, Ollama. Use for chat APIs, React/Solid frontends with useChat/ChatClient, isomorphic tools, tool approval flows, agent loops, multimodal inputs, or troubleshooting streaming and tool definitions.

  Keywords: TanStack AI, @tanstack/ai, @tanstack/ai-react, @tanstack/ai-client, @tanstack/ai-solid, @tanstack/ai-openai, @tanstack/ai-anthropic, @tanstack/ai-gemini, @tanstack/ai-ollama, toolDefinition, client tools, server tools, tool approval, agent loop, streaming, SSE, connection adapters, multimodal, type-safe models, TanStack Start, Next.js API, toStreamResponse, fetchServerSentEvents, chat, useChat, ChatClient, needsApproval
license: MIT
---

# TanStack AI (Provider-Agnostic LLM SDK)

**Status**: Production Ready ✅  
**Last Updated**: 2025-12-09  
**Dependencies**: Node.js 18+, TypeScript 5+; React 18+ for `@tanstack/ai-react`; Solid 1.8+ for `@tanstack/ai-solid`  
**Latest Versions**: @tanstack/ai@latest (alpha), @tanstack/ai-react@latest, @tanstack/ai-client@latest, adapters: @tanstack/ai-openai@latest @tanstack/ai-anthropic@latest @tanstack/ai-gemini@latest @tanstack/ai-ollama@latest

---

## Quick Start (7 Minutes)

### 1) Install core + adapter

```bash
pnpm add @tanstack/ai @tanstack/ai-react @tanstack/ai-openai
# swap adapters as needed: @tanstack/ai-anthropic @tanstack/ai-gemini @tanstack/ai-ollama
pnpm add zod              # recommended for tool schemas
```

**Why this matters:**
- Core is framework-agnostic; React binding just wraps the headless client. citeturn1search3
- Adapters abstract provider quirks so you can change models without rewriting code. citeturn1search3

### 2) Ship a streaming chat endpoint (Next.js or TanStack Start)

```ts
// app/api/chat/route.ts (Next.js) or src/routes/api/chat.ts (TanStack Start)
import { chat, toStreamResponse } from '@tanstack/ai'
import { openai } from '@tanstack/ai-openai'
import { tools } from '@/tools/definitions' // definitions only

export async function POST(request: Request) {
  const { messages, conversationId } = await request.json()
  const stream = chat({
    adapter: openai(),
    messages,
    model: 'gpt-4o',
    tools,
  })
  return toStreamResponse(stream)
}
```

**CRITICAL:**
- Pass tool **definitions** to the server so the LLM can request them; implementations live in their runtimes. citeturn0search7
- Always stream; chunked responses keep UIs responsive and reduce token waste. citeturn0search1

### 3) Wire the client with `useChat` + SSE

```tsx
// components/Chat.tsx
import { useChat, fetchServerSentEvents } from '@tanstack/ai-react'
import { clientTools } from '@tanstack/ai-client'
import { updateUIDef } from '@/tools/definitions'

const updateUI = updateUIDef.client(({ message }) => {
  alert(message)
  return { success: true }
})

export function Chat() {
  const tools = clientTools(updateUI)
  const { messages, sendMessage, isLoading, approval } = useChat({
    connection: fetchServerSentEvents('/api/chat'),
    tools,
  })

  return (
    <form onSubmit={e => { e.preventDefault(); sendMessage(e.currentTarget.prompt.value) }}>
      <textarea name="prompt" disabled={isLoading} />
      {approval?.pending && (
        <button type="button" onClick={() => approval.approve()}>
          Approve tool
        </button>
      )}
    </form>
  )
}
```

**CRITICAL:**
- Use `fetchServerSentEvents` (or matching adapter) to mirror the streaming response. citeturn0search0
- Keep client tool names identical to definitions to avoid “tool not found” errors. citeturn0search7

---

## The 4-Step Setup Process

### Step 1: Choose provider + model safely
- Add the correct adapter and set the matching API key (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, or Ollama host).
- Prefer per-model option typing from adapters to avoid invalid options (e.g., vision-only fields). citeturn1search3

### Step 2: Define tools once, implement per runtime

```ts
// tools/definitions.ts
import { z, toolDefinition } from '@tanstack/ai'

export const getWeatherDef = toolDefinition({
  name: 'getWeather',
  description: 'Get current weather for a city',
  inputSchema: z.object({ city: z.string() }),
  needsApproval: true,
})

export const getWeather = getWeatherDef.server(async ({ city }) => {
  const data = await fetch(`https://api.weather.gov/points?q=${city}`).then(r => r.json())
  return { summary: data.properties?.relativeLocation?.properties?.city ?? city }
})

export const showToast = getWeatherDef.client(({ city }) => {
  console.log(`Showing toast for ${city}`)
  return { acknowledged: true }
})
```

**Key Points:**
- `needsApproval: true` forces explicit user approval for sensitive actions. citeturn0search1
- Keep tools single-purpose and idempotent; return structured objects instead of throwing errors. citeturn0search1

### Step 3: Create connection adapter + chat options
- Server: `toStreamResponse(stream)` for HTTP streaming; `toServerSentEventsStream` helper for Server-Sent Events. citeturn0search3turn0search4
- Client: `fetchServerSentEvents('/api/chat')` or a custom adapter for websockets if needed. citeturn0search0
- Configure `agentLoopStrategy` (e.g., `maxIterations(8)`) to cap tool recursion. citeturn1search4

### Step 4: Add observability + guardrails
- Log tool executions and stream chunks for debugging; alpha exposes hooks while devtools are in progress. citeturn0search1
- Validate inputs with Zod; fail fast and return typed error objects.
- Enforce timeouts on external API calls inside tools to prevent stuck agent loops.

---

## Critical Rules

### Always Do

✅ Stream responses; avoid waiting for full completions. citeturn0search1  
✅ Pass **definitions** to the server and **implementations** to the correct runtime. citeturn0search7  
✅ Use Zod schemas for tool inputs/outputs to keep type safety across providers. citeturn0search1  
✅ Cap agent loops with `maxIterations` to prevent runaway tool calls. citeturn1search4  
✅ Require `needsApproval` for destructive or billing-sensitive tools. citeturn0search1  

### Never Do

❌ Mix provider adapters in a single request—instantiate one adapter per call.  
❌ Throw raw errors from tools; return structured error payloads.  
❌ Send client tool **implementations** to the server (definitions only).  
❌ Hardcode model capabilities; rely on adapter typings for per-model options. citeturn0search1  
❌ Skip API key checks; fail fast with helpful messages on the server. citeturn0search1  

---

## Known Issues Prevention

This skill prevents **3** documented issues:

### Issue #1: “tool not found” / silent tool failures
**Why it happens**: Definitions aren’t passed to `chat()`; only implementations exist locally.  
**Prevention**: Export definitions separately and include them in the server `tools` array; keep names stable. citeturn0search7

### Issue #2: Streaming stalls in the UI
**Why it happens**: Mismatch between server response type and client adapter (HTTP chunked vs SSE).  
**Prevention**: Use `toStreamResponse` on the server + `fetchServerSentEvents` (or matching adapter) on the client. citeturn0search1turn0search0

### Issue #3: Model option validation errors
**Why it happens**: Provider-specific options (e.g., vision params) sent to unsupported models.  
**Prevention**: Use adapter-provided types; rely on per-model option typing to surface invalid fields at compile time. citeturn1search3

---

## Configuration Files Reference

### .env.local (Full Example)

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=
GEMINI_API_KEY=
OLLAMA_HOST=http://localhost:11434
AI_STREAM_STRATEGY=immediate
```

**Why these settings:**
- Keep non-active providers empty to avoid accidental multi-provider calls.
- `AI_STREAM_STRATEGY` is read by the sample client to pick chunk strategies (immediate vs buffered).

---

## Common Patterns

### Pattern 1: Agentic cycle with bounded tools

```ts
import { chat, maxIterations } from '@tanstack/ai'
import { openai } from '@tanstack/ai-openai'

const stream = chat({
  adapter: openai(),
  messages,
  tools,
  agentLoopStrategy: maxIterations(8), // hard cap
})
```

**When to use**: Any flow where the LLM could recurse across tools (search → summarize → fetch detail). citeturn1search4

### Pattern 2: Hybrid server + client tools

```ts
// server: data fetch
const fetchUser = fetchUserDef.server(async ({ id }) => db.user.find(id))

// client: UI update
const highlightUser = highlightUserDef.client(({ id }) => {
  document.querySelector(`#user-${id}`)?.classList.add('ring')
  return { highlighted: true }
})

chat({ tools: [fetchUser, highlightUser] })
```

**When to use**: When the model must both fetch data and mutate UI state in one loop. citeturn0search1

---

## Using Bundled Resources

### Scripts (scripts/)

- `scripts/check-ai-env.sh` — verifies required provider keys are present before running dev servers.

**Example Usage:**
```bash
./scripts/check-ai-env.sh
```

### References (references/)

- `references/tanstack-ai-cheatsheet.md` — condensed server/client/tool patterns plus troubleshooting cues.

**When Claude should load these**: When debugging tool routing, streaming issues, or recalling exact API calls.

### Assets (assets/)

- `assets/api-chat-route.ts` — copy/paste API route template with streaming + tools.  
- `assets/tool-definitions.ts` — ready-to-use toolDefinition examples with approval + zod schemas.

---

## When to Load References

Load reference files for specific implementation scenarios:

- **Adapter Comparison**: Load `references/adapter-matrix.md` when choosing between OpenAI, Anthropic, Gemini, or Ollama adapters, or when debugging provider-specific quirks.

- **React Integration Details**: Load `references/react-integration.md` when implementing useChat hooks, handling SSE streams in React components, or managing client-side tool state.

- **Routing Setup**: Load `references/start-vs-next-routing.md` when setting up API routes in Next.js vs TanStack Start, or troubleshooting streaming response setup.

- **Streaming Issues**: Load `references/streaming-troubleshooting.md` when debugging SSE connection problems, chunk delivery issues, or HTTP streaming configuration.

- **Quick Reference**: Load `references/tanstack-ai-cheatsheet.md` for condensed API patterns, tool definition syntax, or rapid troubleshooting cues.

- **Tool Architecture**: Load `references/tool-patterns.md` when implementing complex client/server tool workflows, approval flows, or hybrid tool patterns.

- **Type Safety Details**: Load `references/type-safety.md` when working with per-model option typing, multimodal inputs, or debugging type errors across adapters.

---

## Advanced Topics

### Per-model type safety
- Use adapter typings to pick valid options per model; avoid generic `any` options on `chat()`. citeturn1search3
- For multimodal models, send `parts` with correct MIME types; unsupported modalities are caught at compile time. citeturn1search3

### Tool approval UX
- Surfaced via `approval` object in `useChat`; render approve/reject UI and persist decision per tool call. citeturn0search1
- For auditable actions, log approval decisions alongside tool inputs.

### Connection adapters
- Default to `fetchServerSentEvents` (SSE) for minimal setup; switch to custom adapters for websockets or HTTP chunking. citeturn0search0
- Use `ImmediateStrategy` in the client to emit every chunk for typing indicator UIs. citeturn0search0

---

## Dependencies

**Required**:
- @tanstack/ai@latest — core chat + tool engine  
- @tanstack/ai-react@latest — React bindings (skip for headless usage)  
- @tanstack/ai-client@latest — headless chat client + adapters  
- Adapter: one of @tanstack/ai-openai@latest | @tanstack/ai-anthropic@latest | @tanstack/ai-gemini@latest | @tanstack/ai-ollama@latest  
- zod@latest — schema validation for tools

**Optional**:
- @tanstack/ai-solid@latest — Solid bindings  
- @tanstack/react-query@latest — cache data fetched inside tools  
- @tanstack/start@latest — co-locate AI tools with server functions

---

## Official Documentation

- **TanStack AI Overview**: https://tanstack.com/ai/latest/docs/getting-started/overview  
- **Quick Start**: https://tanstack.com/ai/latest/docs/getting-started/quick-start  
- **Tool Architecture & Approval**: https://tanstack.com/ai/latest/docs/guides/tool-architecture  
- **Client Tools**: https://tanstack.com/ai/latest/docs/guides/client-tools  
- **API Reference**: https://tanstack.com/ai/latest/docs/api/ai

---

## Package Versions (Verified 2025-12-09)

```json
{
  "dependencies": {
    "@tanstack/ai": "latest",
    "@tanstack/ai-react": "latest",
    "@tanstack/ai-client": "latest",
    "@tanstack/ai-openai": "latest"
  },
  "devDependencies": {
    "zod": "latest"
  }
}
```

---

## Troubleshooting

### Problem: UI never receives tool output
**Solution**: Ensure tool implementations return serializable objects; avoid returning undefined. Register client implementations via `clientTools(...)`.

### Problem: “Missing API key” responses
**Solution**: Run `./scripts/check-ai-env.sh` and set the relevant provider key in `.env.local`. Fail fast in the route before invoking `chat()`. citeturn0search1

### Problem: Streaming stops after first chunk
**Solution**: Confirm the server returns `toStreamResponse(stream)` (or SSE helper) and that any reverse proxy allows chunked transfer.

---

## Complete Setup Checklist

Use this checklist to verify your setup:

- [ ] Installed core + one adapter and zod
- [ ] API route returns `toStreamResponse(stream)` with tool **definitions** included
- [ ] Client uses `fetchServerSentEvents` (or matching adapter) and registers client tool implementations
- [ ] `needsApproval` paths render approve/reject UI
- [ ] Agent loop capped (e.g., `maxIterations`)
- [ ] Environment keys validated with `check-ai-env.sh`
- [ ] Multimodal inputs tested if targeting vision/audio models

---

**Questions? Issues?**

1. Load `references/tanstack-ai-cheatsheet.md` for deeper examples  
2. Re-run quick start steps with a single provider adapter  
3. Review official docs above for API surface updates

---
