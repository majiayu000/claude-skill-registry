---
name: agent-builder-vercel-sdk
description: Build conversational AI agents using Vercel AI SDK + OpenRouter. Use when creating Next.js frontends with streaming UI, tool calling, and multi-provider support.
license: MIT
---

# Vercel AI SDK Agent Builder

## Purpose
Create streaming AI chat interfaces with minimal code using Vercel AI SDK and OpenRouter provider.

## When to Use
- Building Next.js frontend with chat UI
- Need streaming responses with SSE
- Want type-safe tool calling in TypeScript
- Switching between multiple AI providers
- Building agentic loops with stopWhen/prepareStep

## Quick Start

### Installation
```bash
npm install ai @openrouter/ai-sdk-provider zod
```

### Environment Variables
```env
OPENROUTER_API_KEY=sk-or-v1-...
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

## Backend Setup (Route Handler)

### Basic Chat Endpoint
```typescript
// app/api/chat/route.ts
import { OpenRouter } from '@openrouter/ai-sdk-provider'
import { streamText } from 'ai'

const openrouter = new OpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY
})

export async function POST(req: Request) {
  const { messages } = await req.json()

  const result = streamText({
    model: openrouter('openai/gpt-4o'),
    system: 'You are a helpful assistant',
    messages,
  })

  return result.toDataStreamResponse()
}
```

### With Tool Calling
```typescript
import { z } from 'zod'
import { tool } from 'ai'

const tools = {
  generateImage: tool({
    description: 'Generate images using AI',
    parameters: z.object({
      prompt: z.string().describe('Image description'),
      numImages: z.number().min(1).max(10).default(1)
    }),
    execute: async ({ prompt, numImages }) => {
      // Your implementation
      const images = await generateImages(prompt, numImages)
      return { images }
    }
  })
}

export async function POST(req: Request) {
  const { messages } = await req.json()

  const result = streamText({
    model: openrouter('openai/gpt-4o'),
    system: 'You are a helpful assistant',
    messages,
    tools,
    maxSteps: 5 // Enable agentic loop
  })

  return result.toDataStreamResponse()
}
```

## Frontend Integration

### Using useChat Hook
```typescript
'use client'

import { useChat } from 'ai/react'

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat()

  return (
    <div className="flex flex-col h-screen">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map(m => (
          <div key={m.id} className={m.role === 'user' ? 'text-right' : 'text-left'}>
            <div className="inline-block p-3 rounded-lg">
              {m.content}
            </div>
          </div>
        ))}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Type a message..."
          disabled={isLoading}
          className="w-full px-4 py-2 border rounded"
        />
      </form>
    </div>
  )
}
```

### With Tool Results Display
```typescript
'use client'

import { useChat } from 'ai/react'

export default function ChatWithTools() {
  const { messages, input, handleInputChange, handleSubmit } = useChat()

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          {m.content}

          {/* Display tool calls */}
          {m.toolInvocations?.map(tool => (
            <div key={tool.toolCallId} className="bg-gray-100 p-2 rounded">
              <strong>{tool.toolName}</strong>
              {tool.state === 'result' && (
                <pre>{JSON.stringify(tool.result, null, 2)}</pre>
              )}
            </div>
          ))}
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
      </form>
    </div>
  )
}
```

## Advanced Patterns

### Multi-Step Agentic Loop
```typescript
const result = streamText({
  model: openrouter('openai/gpt-4o'),
  messages,
  tools,
  maxSteps: 5,

  // Control loop behavior
  onStepFinish: ({ stepType, text, toolCalls }) => {
    console.log(`Step finished: ${stepType}`)
  },

  // Stop condition
  experimental_continueSteps: true
})
```

### Custom Streaming with streamUI
```typescript
import { streamUI } from 'ai/rsc'

export async function generateUI(prompt: string) {
  const result = streamUI({
    model: openrouter('openai/gpt-4o'),
    prompt,
    text: ({ content }) => <p>{content}</p>,
    tools: {
      showImage: {
        description: 'Display an image',
        parameters: z.object({ url: z.string() }),
        generate: async ({ url }) => <img src={url} />
      }
    }
  })

  return result.value
}
```

## tldraw Agent Pattern

Based on: `/Users/danielcarreon/Documents/AI/software/tldraw-agent/`

```typescript
// Incremental JSON parsing pattern
async function* streamActions(model, prompt) {
  const { textStream } = streamText({
    model,
    system: systemPrompt,
    messages,
    maxOutputTokens: 8192,
    temperature: 0
  })

  let buffer = '{"actions": [{"_type":'

  for await (const text of textStream) {
    buffer += text

    // Parse incremental JSON
    const partialObject = closeAndParseJson(buffer)
    if (!partialObject) continue

    const actions = partialObject.actions
    if (!Array.isArray(actions)) continue

    // Yield actions as they complete
    for (const action of actions) {
      if (action.complete) {
        yield action
      }
    }
  }
}
```

## OpenRouter Provider Setup

```typescript
import { OpenRouter } from '@openrouter/ai-sdk-provider'

const openrouter = new OpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY,
  // Optional: customize
  baseURL: 'https://openrouter.ai/api/v1',
  headers: {
    'HTTP-Referer': process.env.NEXT_PUBLIC_SITE_URL,
    'X-Title': 'My App'
  }
})

// Use different models
const gpt4 = openrouter('openai/gpt-4o')
const claude = openrouter('anthropic/claude-3-5-sonnet')
const gemini = openrouter('google/gemini-2.0-flash-exp')
```

## Error Handling

```typescript
export async function POST(req: Request) {
  try {
    const { messages } = await req.json()

    const result = streamText({
      model: openrouter('openai/gpt-4o'),
      messages,
      onError: (error) => {
        console.error('Stream error:', error)
      }
    })

    return result.toDataStreamResponse()
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500 }
    )
  }
}
```

## Testing

```typescript
import { streamText } from 'ai'
import { OpenRouter } from '@openrouter/ai-sdk-provider'

describe('Chat API', () => {
  it('should stream response', async () => {
    const openrouter = new OpenRouter({
      apiKey: process.env.OPENROUTER_API_KEY
    })

    const result = streamText({
      model: openrouter('openai/gpt-4o'),
      prompt: 'Say hello'
    })

    const chunks = []
    for await (const chunk of result.textStream) {
      chunks.push(chunk)
    }

    expect(chunks.length).toBeGreaterThan(0)
  })
})
```

## Best Practices

1. **Type Safety**: Use Zod for tool parameters
2. **Error Boundaries**: Wrap chat UI in ErrorBoundary
3. **Loading States**: Show loading UI during streaming
4. **Optimistic Updates**: Update UI before server response
5. **Tool Results**: Display tool executions to user
6. **Rate Limiting**: Implement rate limits on API routes
7. **Context Management**: Limit message history to avoid token overflow

## Common Patterns

### Image Generation Agent
```typescript
const tools = {
  generateAvatar: tool({
    description: 'Generate avatar with DANI identity',
    parameters: z.object({
      prompt: z.string(),
      numImages: z.number().default(3)
    }),
    execute: async ({ prompt, numImages }) => {
      const response = await fetch('/api/generate', {
        method: 'POST',
        body: JSON.stringify({ prompt, numImages })
      })
      return await response.json()
    }
  }),

  combineImages: tool({
    description: 'Combine multiple images',
    parameters: z.object({
      imageUrls: z.array(z.string()),
      prompt: z.string()
    }),
    execute: async ({ imageUrls, prompt }) => {
      // Nano Banana integration
      return await combineWithNanoBanana(imageUrls, prompt)
    }
  })
}
```

## Resources

- [Vercel AI SDK Docs](https://sdk.vercel.ai)
- [OpenRouter Provider](https://github.com/OpenRouterTeam/ai-sdk-provider)
- [Tool Calling Guide](https://sdk.vercel.ai/docs/ai-sdk-core/tools-and-tool-calling)
