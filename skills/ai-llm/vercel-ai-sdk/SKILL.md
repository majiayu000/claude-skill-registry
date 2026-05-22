---
name: vercel-ai-sdk
description: Guide for integrating Vercel AI SDK into Remix apps. Build AI chatbots, text completion, and agents within your Shopify app.
---

# Vercel AI SDK for Remix Integration

The Vercel AI SDK is the standard for building AI UIs. It abstracts streaming, state management, and provider differences.

## 1. Setup

```bash
npm install ai @ai-sdk/openai
```

## 2. Server-side Streaming (`action` function)

Remix uses `Response` objects. The AI SDK has a helper `StreamingTextResponse`.

```typescript
// app/routes/api.chat.ts
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { ActionFunctionArgs } from "@remix-run/node";

export const action = async ({ request }: ActionFunctionArgs) => {
  const { messages } = await request.json();

  const result = await streamText({
    model: openai('gpt-4-turbo'),
    messages,
  });

  return result.toDataStreamResponse();
};
```

## 3. Client-side UI hooks

Use `useChat` to manage message state and input automatically.

```tsx
// app/routes/app.assistant.tsx
import { useChat } from 'ai/react';

export default function AssistantPage() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/chat', // points to the action above
  });

  return (
    <div className="chat-container">
      {messages.map(m => (
        <div key={m.id} className={m.role === 'user' ? 'user-msg' : 'ai-msg'}>
          {m.content}
        </div>
      ))}
      
      <form onSubmit={handleSubmit}>
        <input 
          value={input} 
          onChange={handleInputChange} 
          placeholder="Ask AI something..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

## 4. Shopify Context Injection
You often want the AI to know about the current Store. Retrieve data in the `action` and inject it as a "System Message".

```typescript
// app/routes/api.chat.ts
const { session } = await authenticate.admin(request);
// Fetch store data with Mongoose
const products = await Product.find({ shop: session.shop }).limit(5).lean();
const contextInfo = JSON.stringify(products);

const result = await streamText({
  model: openai('gpt-4o'),
  system: `You are a helper for shop ${session.shop}. Here are likely relevant products: ${contextInfo}`,
  messages,
});
```

## 5. Deployment Note (Streaming)
Streaming works out-of-the-box on Vercel, Fly.io, and VPS. 
If using standard Node.js adapter, ensure your server supports standard Web Streams (Node 18+).
