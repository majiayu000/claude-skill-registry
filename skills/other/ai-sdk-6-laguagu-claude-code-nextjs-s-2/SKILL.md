---
name: ai-sdk-6
description: Vercel AI SDK v6 development. Use when building AI agents, chatbots, tool integrations, or streaming applications with the ai package.
---

# Vercel AI SDK v6 Development Guide

Use this skill when developing AI-powered features using Vercel AI SDK v6 (`ai` package).

## Quick Reference

### Installation

```bash
bun add ai @ai-sdk/anthropic zod
```

### Core Functions

| Function       | Purpose                                                           |
| -------------- | ----------------------------------------------------------------- |
| `generateText` | Non-streaming text generation (+ structured output with `Output`) |
| `streamText`   | Streaming text generation (+ structured output with `Output`)     |

> **v6 Note**: `generateObject`/`streamObject` are deprecated.
> Use `generateText`/`streamText` with `output: Output.object({ schema })` instead.

### Structured Output (v6)

```typescript
import { generateText, Output } from "ai";
import { z } from "zod";

const { output } = await generateText({
  model: anthropic("claude-sonnet-4-5"),
  output: Output.object({
    schema: z.object({
      sentiment: z.enum(["positive", "neutral", "negative"]),
      topics: z.array(z.string()),
    }),
  }),
  prompt: "Analyze this feedback...",
});
```

Output types: `Output.object()`, `Output.array()`, `Output.choice()`, `Output.json()`

### Agent Class (v6 Key Feature)

```typescript
import { ToolLoopAgent, tool, stepCountIs } from "ai";
import { anthropic } from "@ai-sdk/anthropic";
import { z } from "zod";

const myAgent = new ToolLoopAgent({
  model: anthropic("claude-sonnet-4-5"),
  instructions: "You are a helpful assistant.",
  tools: {
    getData: tool({
      description: "Fetch data from API",
      inputSchema: z.object({
        query: z.string(),
      }),
      execute: async ({ query }) => {
        return { result: "data" };
      },
    }),
  },
  stopWhen: stepCountIs(20),
});

// Usage
const { text } = await myAgent.generate({ prompt: "Hello" });
const stream = myAgent.stream({ prompt: "Hello" });
```

### API Route with Agent

```typescript
// app/api/chat/route.ts
import { createAgentUIStreamResponse } from "ai";
import { myAgent } from "@/agents/my-agent";

export async function POST(request: Request) {
  const { messages } = await request.json();

  return createAgentUIStreamResponse({
    agent: myAgent,
    uiMessages: messages,
  });
}
```

### useChat Hook (Client)

```typescript
"use client";
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";
import { useState } from "react";

export function Chat() {
  const [input, setInput] = useState("");
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({
      api: "/api/chat",
    }),
  });

  return (
    <>
      {messages.map((msg) => (
        <div key={msg.id}>
          {msg.parts.map((part, i) =>
            part.type === "text" ? <span key={i}>{part.text}</span> : null
          )}
        </div>
      ))}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (input.trim()) {
            sendMessage({ text: input });
            setInput("");
          }
        }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={status !== "ready"}
        />
        <button type="submit" disabled={status !== "ready"}>
          Send
        </button>
      </form>
    </>
  );
}
```

> **v6 Note**: `useChat` no longer manages input state internally. Use `useState` for controlled inputs.

## Reference Documentation

For detailed information, see:

- [agents.md](references/agents.md) - ToolLoopAgent, loop control, workflows
- [core-functions.md](references/core-functions.md) - generateText, streamText, Output patterns
- [tools.md](references/tools.md) - Tool definition with Zod schemas
- [ui-hooks.md](references/ui-hooks.md) - useChat, UIMessage, streaming
- [middleware.md](references/middleware.md) - Custom middleware patterns
- [mcp.md](references/mcp.md) - MCP server integration

## Official Documentation

For the latest information, see [AI SDK docs](https://ai-sdk.dev/docs/agents).
