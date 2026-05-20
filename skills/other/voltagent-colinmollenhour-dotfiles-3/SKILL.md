---
name: "VoltAgent Development"
description: "Create and configure VoltAgent AI agents with tools, memory, hooks, and sub-agents. Use when building AI agents, adding agent tools, configuring VoltAgent memory, creating multi-agent workflows, or debugging VoltAgent integrations."
---

# VoltAgent Development

## What This Skill Does

Guides development of VoltAgent-based AI agents including:
- Agent creation and configuration
- Tool development with Zod schemas
- Memory persistence with LibSQL
- Multi-agent orchestration with sub-agents
- Lifecycle hooks and guardrails
- Streaming and structured output

## Prerequisites

- `@voltagent/core` package
- AI SDK provider (e.g., `@ai-sdk/anthropic`, `@ai-sdk/openai`)
- `zod` for schema validation

---

## Quick Start

### Basic Agent

```typescript
import { Agent } from '@voltagent/core'
import { anthropic } from '@ai-sdk/anthropic'

const agent = new Agent({
  name: 'Assistant',
  instructions: 'You are a helpful assistant.',
  model: anthropic('claude-3-5-haiku-20241022'),
})

const result = await agent.generateText('Hello!')
console.log(result.text)
```

### Agent with Tools

```typescript
import { Agent, createTool } from '@voltagent/core'
import { z } from 'zod'

const weatherTool = createTool({
  name: 'get_weather',
  description: 'Get current weather for a location',
  parameters: z.object({
    location: z.string().describe('The city name'),
  }),
  execute: async ({ location }) => {
    return { location, temperature: 72, conditions: 'sunny' }
  },
})

const agent = new Agent({
  name: 'Weather Assistant',
  instructions: 'Help users with weather information.',
  model: anthropic('claude-3-5-haiku-20241022'),
  tools: [weatherTool],
})
```

---

## Tool Development

### Basic Tool Pattern

```typescript
import { createTool } from '@voltagent/core'
import { z } from 'zod'

export const myTool = createTool({
  name: 'tool_name',           // snake_case convention
  description: 'Clear description of what this tool does',
  parameters: z.object({
    param: z.string().describe('What this parameter is for'),
    optional: z.number().optional().describe('Optional parameter'),
  }),
  execute: async (args, options) => {
    // Access context from options
    const userId = options?.context?.get('userId')
    const isAdmin = options?.context?.get('isAdmin') === 'true'

    // Implement tool logic
    return { result: 'data' }
  },
})
```

### Tool with Database Access (Project Pattern)

```typescript
import { createTool } from '@voltagent/core'
import { z } from 'zod'

export const fetchClientsTool = createTool({
  name: 'fetch_clients',
  description: 'Get list of clients for the current trainer',
  parameters: z.object({
    limit: z.number().optional().describe('Max clients to return'),
  }),
  execute: async ({ limit = 10 }, options) => {
    const db = useDB()
    const trainerId = options?.context?.get('trainerId')
    const isSuperAdmin = options?.context?.get('isSuperAdmin') === 'true'

    // Super admins see all clients, trainers see only assigned
    const clients = isSuperAdmin
      ? await db.select().from(users).limit(limit)
      : await db.select().from(users)
          .innerJoin(clientsTrainers, eq(users.id, clientsTrainers.clientId))
          .where(eq(clientsTrainers.trainerId, trainerId))
          .limit(limit)

    return { clients, count: clients.length }
  },
})
```

### Tool with Cancellation Support

```typescript
const longRunningTool = createTool({
  name: 'search_web',
  description: 'Search the web (supports cancellation)',
  parameters: z.object({
    query: z.string().describe('Search query'),
  }),
  execute: async ({ query }, options) => {
    const signal = options?.abortController?.signal

    if (signal?.aborted) {
      throw new Error('Search cancelled before start')
    }

    const response = await fetch(`https://api.search.com?q=${query}`, { signal })
    return await response.json()
  },
})
```

See [tool-template.ts](resources/templates/tool-template.ts) for a complete template.

---

## Critical Rules

### ✅ DO

- Use `model` directly with ai-sdk LanguageModel instances
- Use `instructions` (string or function), NOT `systemPrompt`
- Provide detailed descriptions for tools AND parameters
- Use Zod `.describe()` for all parameters
- Always provide `userId` and `conversationId` for memory
- Use LibSQL/Turso for production memory persistence

### ❌ DON'T

- Use deprecated `llm` + `model` pattern from v0.x
- Use `generateObject`/`streamObject` if you need tool calling
- Assume memory persists by default (it's in-memory only)
- Skip parameter descriptions (LLM needs these)
- Let tools throw unhandled errors

---

## Project Architecture

```
server/
  agents/
    client-insights/          # Main agent
      index.ts               # Agent definition
      tools/                 # Agent tools
        fetchClients.ts
        fetchClientDetails.ts
        searchExercises.ts
  services/
    voltagent.ts            # VoltAgent initialization
  api/
    agents/
      client-insights/
        text.post.ts        # Sync endpoint
        stream.post.ts      # Streaming endpoint
```

---

## Environment Variables

```bash
# Required for Anthropic (accessed directly by AI SDK)
ANTHROPIC_API_KEY=sk-ant-...

# Optional: For observability
VOLTAGENT_PUBLIC_KEY=pk_...
VOLTAGENT_SECRET_KEY=sk_...

# Optional: For Turso remote memory
TURSO_DATABASE_URL=libsql://...
TURSO_AUTH_TOKEN=...
```

---

## Advanced Topics

- [Memory Configuration](docs/MEMORY.md) - Persistent storage with LibSQL/Turso
- [Multi-Agent Orchestration](docs/MULTI-AGENT.md) - Sub-agents and supervisor patterns
- [Streaming & Structured Output](docs/STREAMING.md) - Real-time responses and Zod schemas
- [Lifecycle Hooks](docs/HOOKS.md) - onStart, onToolStart, onEnd callbacks
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and debugging

---

## Reference

- [VoltAgent Docs](https://voltagent.dev/docs/quick-start)
- [Agent Overview](https://voltagent.dev/docs/agents/overview)
- [Tools Documentation](https://voltagent.dev/docs/agents/tools)
- [Full Project Reference](AUTHORING-voltagent.md)
