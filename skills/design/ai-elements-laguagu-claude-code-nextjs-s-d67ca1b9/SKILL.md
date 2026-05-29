---
name: ai-elements
description: AI Elements component library for AI-native applications. Use when building chatbots, AI workflows, or integrating with Vercel AI SDK's useChat hook.
---

# AI Elements

Build AI-native applications with pre-built components on shadcn/ui.

## Quick Start

```bash
# Install all AI Elements components
bunx --bun ai-elements@latest
# or via shadcn CLI
bunx --bun shadcn@latest add @ai-elements/all

# Install AI SDK dependencies
bun add ai @ai-sdk/react zod
```

Components install to `@/components/ai-elements/`.

## Component Quick Reference

### Chatbot Components

| Component | Purpose |
|-----------|---------|
| `Conversation` | Auto-scroll chat container |
| `Message` | Single message wrapper (user/assistant) |
| `MessageResponse` | Streaming markdown renderer (uses `streamdown`) |
| `PromptInput` | Rich input with attachments, model picker |
| `Reasoning` | Collapsible thinking display |
| `Sources` | Citation/reference display |
| `Tool` | Tool execution visualization |
| `ChainOfThought` | Step-by-step breakdown |
| `InlineCitation` | Inline citation badge with hover card carousel |
| `Plan` | Collapsible plan card with streaming title |
| `Task` | Collapsible task breakdown display |
| `Queue` | Todo/message queue with sections |

### Workflow Components

| Component | Purpose |
|-----------|---------|
| `Canvas` | React Flow wrapper for visual workflows |
| `Node` | Workflow node with header/content/footer |
| `Edge` | Animated/temporary edge connections |
| `Controls` | Zoom/fit view controls |
| `Panel` | Positioned overlay panels |
| `Context` | Token usage tracking display |

### Utility Components

| Component | Purpose |
|-----------|---------|
| `CodeBlock` | Syntax highlighted code (Shiki) |
| `Loader` | Loading indicator |
| `Shimmer` | Streaming text effect |
| `Confirmation` | Tool confirmation dialog |
| `Suggestion` | Quick action chips |
| `ModelSelector` | Model picker dialog with provider logos |
| `OpenIn` | Open query in external chat (ChatGPT, Claude, etc.) |
| `WebPreview` | Iframe preview with URL bar and console |

## Core Integration Pattern

```tsx
'use client';
import { useChat } from '@ai-sdk/react';
import { Conversation, ConversationContent } from '@/components/ai-elements/conversation';
import { Message, MessageContent, MessageResponse } from '@/components/ai-elements/message';
import { Reasoning, ReasoningTrigger, ReasoningContent } from '@/components/ai-elements/reasoning';
import { Sources, SourcesTrigger, SourcesContent, Source } from '@/components/ai-elements/sources';

export function Chat() {
  const { messages, sendMessage, status } = useChat();

  return (
    <Conversation>
      <ConversationContent>
        {messages.map((message) => (
          <div key={message.id}>
            {message.parts.map((part, i) => {
              switch (part.type) {
                case 'text':
                  return (
                    <Message key={i} from={message.role}>
                      <MessageContent>
                        <MessageResponse>{part.text}</MessageResponse>
                      </MessageContent>
                    </Message>
                  );
                case 'reasoning':
                  return (
                    <Reasoning key={i} isStreaming={status === 'streaming'}>
                      <ReasoningTrigger />
                      <ReasoningContent>{part.text}</ReasoningContent>
                    </Reasoning>
                  );
                case 'source-url':
                  return <Source key={i} href={part.url} title={part.title} />;
              }
            })}
          </div>
        ))}
      </ConversationContent>
    </Conversation>
  );
}
```

## API Route Pattern

```typescript
// app/api/chat/route.ts
import { streamText, UIMessage, convertToModelMessages } from 'ai';

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages, model }: { messages: UIMessage[]; model: string } = await req.json();

  const result = streamText({
    model,
    messages: convertToModelMessages(messages),
    system: 'You are a helpful assistant.',
  });

  return result.toUIMessageStreamResponse({
    sendSources: true,
    sendReasoning: true,
  });
}
```

## Key Patterns

### Message Parts Switching

Messages have `parts` array. Switch on `part.type`:
- `text` - Regular text content
- `reasoning` - Model thinking/reasoning
- `source-url` - Citation with URL
- `tool-*` - Tool invocations (input, output, error)

### Compound Components

Most components use compound pattern:
```tsx
<Conversation>
  <ConversationContent>{/* messages */}</ConversationContent>
  <ConversationScrollButton />
</Conversation>

<Message from="assistant">
  <MessageContent>
    <MessageResponse>{text}</MessageResponse>
  </MessageContent>
  <MessageActions>
    <MessageAction label="Copy"><CopyIcon /></MessageAction>
  </MessageActions>
</Message>
```

### File Attachments

```tsx
<PromptInput onSubmit={handleSubmit} globalDrop multiple>
  <PromptInputHeader>
    <PromptInputAttachments>
      {(attachment) => <PromptInputAttachment data={attachment} />}
    </PromptInputAttachments>
  </PromptInputHeader>
  <PromptInputBody>
    <PromptInputTextarea />
  </PromptInputBody>
  <PromptInputFooter>
    <PromptInputTools>
      <PromptInputActionMenu>
        <PromptInputActionMenuTrigger />
        <PromptInputActionMenuContent>
          <PromptInputActionAddAttachments />
        </PromptInputActionMenuContent>
      </PromptInputActionMenu>
    </PromptInputTools>
    <PromptInputSubmit status={status} />
  </PromptInputFooter>
</PromptInput>
```

## References

- [Chatbot Components](references/chatbot.md) - Conversation, Message, PromptInput, Reasoning, Sources, Tool, InlineCitation, Plan, Task, Queue
- [Workflow Components](references/workflow.md) - Canvas, Node, Edge, Controls
- [Utility Components](references/utilities.md) - CodeBlock, Loader, Shimmer, ModelSelector, OpenIn, WebPreview
- [AI SDK Integration](references/integration.md) - useChat, API routes, message parts

## Dependencies

Key dependencies used by AI Elements:

| Package | Purpose |
|---------|---------|
| `streamdown` | Streaming markdown renderer for `MessageResponse` and `Reasoning` |
| `shiki` | Syntax highlighting for `CodeBlock` |
| `use-stick-to-bottom` | Auto-scroll behavior for `Conversation` |
| `motion` | Animations for `Shimmer` |
| `tokenlens` | Token cost calculation for `Context` |

## Package Manager

**Always use bun**, never npm:
- `bun add` (not npm install)
- `bunx --bun` (not npx)
