---
name: ai-app
description: |
  Full-stack AI application generator with Next.js, AI SDK, and ai-elements.
  Use when creating chatbots, agent dashboards, or custom AI applications.

  Triggers: chatbot, chat app, agent dashboard, AI application, Next.js AI,
  useChat, streamText, ai-elements, build AI app, create chatbot
---

# AI App Generator

Build full-stack AI applications with Next.js, AI SDK, and ai-elements.

## Quick Start

### 1. Scaffold Project

```bash
bunx --bun shadcn@latest create --preset "https://ui.shadcn.com/init?base=radix&style=vega&baseColor=zinc&iconLibrary=lucide&font=inter" --template next my-ai-app
cd my-ai-app
```

### 2. Install Dependencies

```bash
bun add ai @ai-sdk/react @ai-sdk/anthropic zod
bunx --bun ai-elements@latest
```

### 3. Configure Environment

```bash
# .env.local - Choose your provider
ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-...
# GOOGLE_GENERATIVE_AI_API_KEY=...
```

### 4. Generate Application

Based on user requirements, generate:
- **Chatbot**: See [references/chatbot.md](references/chatbot.md)
- **Agent Dashboard**: See [references/agent-dashboard.md](references/agent-dashboard.md)
- **Custom**: Combine patterns as needed

## Application Types

### Chatbot

Simple conversational AI with streaming responses.

| Feature | Implementation |
|---------|----------------|
| Chat UI | Conversation + Message + PromptInput |
| API | streamText + toUIMessageStreamResponse |
| Extras | Reasoning, Sources, File attachments |

### Agent Dashboard

Multi-agent interface with tool visualization.

| Feature | Implementation |
|---------|----------------|
| Agents | ToolLoopAgent with tools |
| UI | Dashboard layout + Tool components |
| API | createAgentUIStreamResponse |
| Extras | Status monitoring, tool approval |

### Custom AI App

Mix and match based on user needs:
- Web search chatbot
- Code generation assistant
- Document analyzer
- Multi-modal chat

## Project Structure

```
my-ai-app/
├── app/
│   ├── page.tsx                 # Main UI
│   ├── layout.tsx               # Root layout
│   ├── globals.css              # Theme
│   └── api/
│       └── chat/
│           └── route.ts         # AI endpoint
├── components/
│   ├── ai-elements/             # AI Elements components
│   ├── ui/                      # shadcn/ui components
│   └── chat.tsx                 # Chat component (if extracted)
├── lib/
│   ├── utils.ts                 # Utilities
│   └── ai.ts                    # AI configuration (optional)
├── ai/                          # Agent definitions (if needed)
│   └── assistant.ts
└── .env.local                   # API keys
```

See [references/project-structure.md](references/project-structure.md) for details.

## Core Patterns

### API Route

```typescript
// app/api/chat/route.ts
import { streamText, UIMessage, convertToModelMessages } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: anthropic('claude-sonnet-4-5'),
    messages: convertToModelMessages(messages),
    system: 'You are a helpful assistant.',
  });

  return result.toUIMessageStreamResponse({
    sendSources: true,
    sendReasoning: true,
  });
}
```

### Chat Page

```tsx
// app/page.tsx
'use client';
import { useChat } from '@ai-sdk/react';
import {
  Conversation,
  ConversationContent,
  ConversationScrollButton,
} from '@/components/ai-elements/conversation';
import {
  Message,
  MessageContent,
  MessageResponse,
} from '@/components/ai-elements/message';
import {
  PromptInput,
  PromptInputBody,
  PromptInputTextarea,
  PromptInputFooter,
  PromptInputSubmit,
  type PromptInputMessage,
} from '@/components/ai-elements/prompt-input';
import { Loader } from '@/components/ai-elements/loader';
import { useState } from 'react';

export default function ChatPage() {
  const [input, setInput] = useState('');
  const { messages, sendMessage, status } = useChat();

  const handleSubmit = (message: PromptInputMessage) => {
    if (!message.text.trim()) return;
    sendMessage({ text: message.text, files: message.files });
    setInput('');
  };

  return (
    <div className="flex h-screen flex-col p-4">
      <Conversation className="flex-1">
        <ConversationContent>
          {messages.map((message) => (
            <div key={message.id}>
              {message.parts.map((part, i) => {
                if (part.type === 'text') {
                  return (
                    <Message key={i} from={message.role}>
                      <MessageContent>
                        <MessageResponse>{part.text}</MessageResponse>
                      </MessageContent>
                    </Message>
                  );
                }
                return null;
              })}
            </div>
          ))}
          {status === 'submitted' && <Loader />}
        </ConversationContent>
        <ConversationScrollButton />
      </Conversation>

      <PromptInput onSubmit={handleSubmit} className="mt-4">
        <PromptInputBody>
          <PromptInputTextarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
        </PromptInputBody>
        <PromptInputFooter>
          <div />
          <PromptInputSubmit status={status} />
        </PromptInputFooter>
      </PromptInput>
    </div>
  );
}
```

## Skill References

For detailed patterns, see:

| Need | Skill | Reference |
|------|-------|-----------|
| Chat UI components | `/ai-elements` | [chatbot.md](references/chatbot.md) |
| Next.js patterns | `/nextjs-shadcn` | [architecture.md](../nextjs-shadcn/references/architecture.md) |
| AI SDK functions | `/ai-sdk-6` | [core-functions.md](../ai-sdk-6/references/core-functions.md) |
| Agents & tools | `/ai-sdk-6` | [agents.md](../ai-sdk-6/references/agents.md) |
| Caching | `/cache-components` | [REFERENCE.md](../cache-components/REFERENCE.md) |
| Code review & cleanup | `/code-simplifier` | DRY/KISS/YAGNI validation |

## Workflow

### Phase 1: Understand Requirements

Ask user:
- What type of AI app? (chatbot, agent, custom)
- What features? (reasoning, sources, tools, file upload)
- What theme/colors? (zinc, neutral, blue, violet, green, orange)
- What border radius style? (sharp 0.25rem, default 0.5rem, rounded 0.75rem, pill 1.3rem)

### Phase 2: Scaffold Project

Run scaffolding commands based on requirements.

### Phase 3: Generate Files

Create files based on application type:
- API route (`app/api/chat/route.ts`)
- Main page (`app/page.tsx`)
- Components (if needed)
- Agents (if needed)

### Phase 4: Configure

- Set up `.env.local`
- Configure `next.config.ts` if needed
- Add any additional dependencies

### Phase 5: Verify

```bash
bun dev
```

Test the application works correctly.

## References

- [Chatbot Templates](references/chatbot.md) - Full chatbot implementation
- [Agent Dashboard Templates](references/agent-dashboard.md) - Agent-based apps
- [Project Structure](references/project-structure.md) - Directory layout
- [Examples](references/examples.md) - Copy-paste examples

## Package Manager

**Always use bun**, never npm:
- `bun add` (not npm install)
- `bunx --bun` (not npx)
- `bun dev` (not npm run dev)
