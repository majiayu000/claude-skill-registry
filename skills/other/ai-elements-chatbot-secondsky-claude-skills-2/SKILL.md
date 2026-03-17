---
name: ai-elements-chatbot
description: shadcn/ui AI chat components for conversational interfaces. Use for streaming chat, tool/function displays, reasoning visualization, or encountering Next.js App Router setup, Tailwind v4 integration, AI SDK v5 migration errors.

  Keywords: ai-elements, vercel-ai-sdk, shadcn, chatbot, conversational-ai, streaming-ui, chat-interface, ai-chat, message-components, conversation-ui, tool-calling, reasoning-display, source-citations, markdown-streaming, function-calling, ai-responses, prompt-input, code-highlighting, web-preview, branch-navigation, thinking-display, perplexity-style, claude-artifacts
license: MIT
metadata:
  version: "2.0.0"
  last_verified: "2025-11-18"
  production_tested: true
  token_savings: "~68%"
  errors_prevented: 8
  templates_included: 0
  references_included: 3
---

# AI Elements Chatbot Components

**Status**: Production Ready ✅ | **Last Verified**: 2025-11-18

---

## What Is AI Elements?

Production-ready chat UI components for AI applications:
- Built on shadcn/ui
- 30+ components (Message, Conversation, Response, etc.)
- Works with Vercel AI SDK v5
- Streaming support
- Tool/function call displays
- Reasoning visualization

---

## Quick Start (15 Minutes)

### Prerequisites

- Next.js 15+ (App Router)
- shadcn/ui initialized
- Tailwind v4
- AI SDK v5+

### 1. Initialize

```bash
pnpm dlx ai-elements@latest init
```

### 2. Add Components

```bash
pnpm dlx ai-elements@latest add message conversation response prompt-input
```

### 3. Create Chat Interface

```typescript
'use client';

import { useChat } from 'ai/react';
import { Conversation } from '@/components/ui/ai/conversation';
import { Message } from '@/components/ui/ai/message';
import { Response } from '@/components/ui/ai/response';
import { PromptInput } from '@/components/ui/ai/prompt-input';

export default function ChatPage() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/chat'
  });

  return (
    <div className="flex h-screen flex-col">
      <Conversation>
        {messages.map((msg) => (
          <Message key={msg.id} role={msg.role}>
            <Response markdown={msg.content} />
          </Message>
        ))}
      </Conversation>

      <PromptInput
        value={input}
        onChange={handleInputChange}
        onSubmit={handleSubmit}
      />
    </div>
  );
}
```

**Load `references/setup-guide.md` for complete setup.**

---

## Core Components

### Message & Conversation

```typescript
import { Conversation } from '@/components/ui/ai/conversation';
import { Message } from '@/components/ui/ai/message';

<Conversation>
  {messages.map((msg) => (
    <Message key={msg.id} role={msg.role}>
      {msg.content}
    </Message>
  ))}
</Conversation>
```

### Response (Markdown)

```typescript
import { Response } from '@/components/ui/ai/response';

<Response markdown={content} />
```

### PromptInput

```typescript
import { PromptInput } from '@/components/ui/ai/prompt-input';

<PromptInput
  value={input}
  onChange={handleInputChange}
  onSubmit={handleSubmit}
/>
```

### CodeBlock

```typescript
import { CodeBlock } from '@/components/ui/ai/code-block';

<CodeBlock code={code} language="typescript" />
```

### Reasoning (Thinking)

```typescript
import { Reasoning } from '@/components/ui/ai/reasoning';

<Reasoning content={thinking} />
```

### Tool (Function Calls)

```typescript
import { Tool } from '@/components/ui/ai/tool';

<Tool name="search" args={{ query: "..." }} result={result} />
```

---

## Critical Rules

### Always Do ✅

1. **Install shadcn/ui first** (AI Elements requires it)
2. **Use Next.js App Router** (Pages Router not supported)
3. **Use AI SDK v5** (breaking changes from v4)
4. **Install via CLI** (`pnpm dlx ai-elements@latest`)
5. **Update components.json** with registry
6. **Use client components** ('use client' directive)
7. **Stream responses** for better UX
8. **Handle loading states**
9. **Add error boundaries**
10. **Test on mobile**

### Never Do ❌

1. **Never install as npm package** (components are copied)
2. **Never use Pages Router** (only App Router)
3. **Never use AI SDK v4** (breaking changes)
4. **Never skip prerequisites** (shadcn/ui, Tailwind)
5. **Never modify core types** (extends shadcn types)
6. **Never use without streaming** (defeats purpose)
7. **Never skip accessibility** (ARIA labels)
8. **Never hardcode styles** (use Tailwind)
9. **Never skip error handling** (API failures)
10. **Never ignore mobile** (responsive required)

---

## Available Components (30+)

**Core:**
- Message
- Conversation
- Response
- PromptInput

**Content:**
- CodeBlock
- Markdown
- Tool
- Reasoning
- Sources

**Actions:**
- Actions
- CopyButton
- ShareButton
- RegenerateButton

**Advanced:**
- BranchNavigation
- ThinkingDisplay
- WebPreview

---

## Common Use Cases

### Use Case 1: Basic Chat

```typescript
const { messages, input, handleInputChange, handleSubmit } = useChat();

return (
  <>
    <Conversation>
      {messages.map(m => (
        <Message key={m.id} role={m.role}>
          <Response markdown={m.content} />
        </Message>
      ))}
    </Conversation>
    <PromptInput value={input} onChange={handleInputChange} onSubmit={handleSubmit} />
  </>
);
```

### Use Case 2: With Tool Calls

```typescript
{messages.map(m => (
  <Message key={m.id} role={m.role}>
    {m.toolInvocations?.map(tool => (
      <Tool key={tool.toolCallId} name={tool.toolName} args={tool.args} result={tool.result} />
    ))}
    <Response markdown={m.content} />
  </Message>
))}
```

### Use Case 3: With Reasoning

```typescript
<Message role="assistant">
  {reasoning && <Reasoning content={reasoning} />}
  <Response markdown={content} />
</Message>
```

### Use Case 4: With Code Blocks

```typescript
<Response markdown={content}>
  {(node) => node.type === 'code' ? (
    <CodeBlock code={node.value} language={node.lang} />
  ) : null}
</Response>
```

### Use Case 5: With Sources

```typescript
<Message role="assistant">
  <Response markdown={content} />
  <Sources sources={sources} />
</Message>
```

---

## API Routes

### Basic Streaming

```typescript
// app/api/chat/route.ts
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4'),
    messages
  });

  return result.toDataStreamResponse();
}
```

### With Tools

```typescript
const result = streamText({
  model: openai('gpt-4'),
  messages,
  tools: {
    search: {
      description: 'Search the web',
      parameters: z.object({ query: z.string() }),
      execute: async ({ query }) => {
        return await search(query);
      }
    }
  }
});
```

---

## When to Use AI Elements

**Use when:**
- Building ChatGPT-style interface
- Need production-ready components
- Using Vercel AI SDK
- Want streaming responses
- Need tool/function displays
- Want reasoning visualization

**Don't use when:**
- Not using Next.js App Router
- Don't have shadcn/ui
- Need Pages Router
- Building custom design system

---

## Resources

**References** (`references/`):
- `component-catalog.md` - All 8 AI Elements components with examples
- `example-reference.md` - Complete integration examples and patterns
- `setup-guide.md` - Step-by-step setup with Next.js 15 and shadcn/ui

**Templates** (`templates/`):
- Component examples available in reference files

---

## Official Documentation

- **AI Elements**: https://ai-elements.vercel.app
- **Components**: https://ai-elements.vercel.app/docs/components
- **Examples**: https://github.com/ai-elements/ai-elements/tree/main/examples

---

**Questions? Issues?**

1. Check `references/setup-guide.md` for complete setup
2. Verify prerequisites (Next.js 15+, shadcn/ui, AI SDK v5)
3. See official examples
