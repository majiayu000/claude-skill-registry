---
name: configure-chatkit
description: This skill should be used when setting up OpenAI ChatKit in Next.js, adding domain allowlist to environment, building chat UI component, integrating with /api/chat endpoint, displaying history and tool calls visually, and integrating Better Auth session.
---

# Configure ChatKit Skill

This skill provides guidance for integrating OpenAI ChatKit in a Next.js frontend.

## Purpose

Setup OpenAI ChatKit in Next.js:
- Add domain allowlist key to environment
- Build chat UI component
- POST to /api/chat endpoint with conversation_id
- Display conversation history and tool calls visually
- Integrate Better Auth session

## When to Use

Use this skill when:
- Building the chatbot frontend UI
- Integrating ChatKit components
- Setting up chat API communication
- Displaying tool execution results
- Connecting frontend with authenticated backend

## Capabilities

- **ChatKit Integration**: Use OpenAI ChatKit for chat UI
- **Environment Configuration**: Set up domain allowlist
- **API Communication**: POST to chat endpoint with conversation context
- **Visual Feedback**: Display history, tool calls, and results
- **Authentication**: Integrate Better Auth session

## Environment Setup

```env
# .env.local
NEXT_PUBLIC_CHAT_KIT_PUBLIC_KEY=your_chatkit_public_key
CHAT_KIT_SECRET=your_chatkit_secret_key
CHAT_KIT_INSTANCE_ID=your_instance_id
NEXT_PUBLIC_ALLOWED_DOMAINS=localhost:3000,yourdomain.com
```

## Implementation Pattern

### Chat Component

```tsx
"use client";

import { useState, useEffect, useRef } from "react";
import { useChat } from "@openai/chatkit";
import { useSession } from "better-auth/react";

interface ChatWidgetProps {
  conversationId?: string;
}

export function ChatWidget({ conversationId }: ChatWidgetProps) {
  const { data: session } = useSession();
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const {
    messages,
    sendMessage,
    isLoading: chatLoading,
    error
  } = useChat({
    apiUrl: "/api/chat",
    conversationId,
    auth: {
      getToken: () => session?.accessToken
    }
  });

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    setIsLoading(true);
    try {
      await sendMessage(input);
      setInput("");
    } catch (err) {
      console.error("Failed to send message:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((msg) => (
          <MessageBubble
            key={msg.id}
            role={msg.role}
            content={msg.content}
            toolCalls={msg.tool_calls}
          />
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask me to manage your tasks..."
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading}>
          {isLoading ? "Sending..." : "Send"}
        </button>
      </div>

      {error && <ErrorToast message={error.message} />}
    </div>
  );
}
```

### Message Bubble with Tool Calls

```tsx
interface MessageBubbleProps {
  role: "user" | "assistant" | "tool";
  content: string;
  toolCalls?: ToolCall[];
}

function MessageBubble({ role, content, toolCalls }: MessageBubbleProps) {
  const isUser = role === "user";

  return (
    <div className={`message ${isUser ? "user" : "assistant"}`}>
      <div className="message-content">{content}</div>

      {toolCalls && toolCalls.length > 0 && (
        <div className="tool-calls">
          {toolCalls.map((call) => (
            <ToolCallBadge key={call.id} tool={call} />
          ))}
        </div>
      )}
    </div>
  );
}

function ToolCallBadge({ tool }: { tool: ToolCall }) {
  return (
    <div className="tool-badge">
      <span className="tool-icon">🔧</span>
      <span className="tool-name">{tool.name}</span>
      {tool.status === "completed" && <span className="check">✓</span>}
      {tool.status === "failed" && <span className="x">✗</span>}
    </div>
  );
}
```

### API Communication

```tsx
async function sendMessage(message: string): Promise<void> {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${session?.accessToken}`
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId
    })
  });

  if (!response.ok) {
    throw new Error("Failed to send message");
  }

  const data = await response.json();
  // Update conversation_id if new
  if (!conversationId && data.conversation_id) {
    setConversationId(data.conversation_id);
  }
}
```

### Better Auth Integration

```tsx
"use client";

import { SessionProvider } from "better-auth/react";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  return (
    <SessionProvider>
      {children}
    </SessionProvider>
  );
}

// In your chat component
const { data: session } = useSession();

useEffect(() => {
  if (session?.accessToken) {
    // Configure chat client with auth token
    chatClient.setAuthToken(session.accessToken);
  }
}, [session]);
```

## Styling (Tailwind CSS)

```tsx
.chat-container {
  @apply flex flex-col h-full max-w-2xl mx-auto border rounded-lg shadow-lg;
}

.chat-messages {
  @apply flex-1 overflow-y-auto p-4 space-y-4;
}

.message {
  @apply p-3 rounded-lg max-w-[80%];
}

.message.user {
  @apply bg-blue-500 text-white ml-auto;
}

.message.assistant {
  @apply bg-gray-100 text-gray-900;
}

.chat-input {
  @apply border-t p-4 flex gap-2;
}

.chat-input input {
  @apply flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2;
}

.chat-input button {
  @apply px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600;
}

.tool-calls {
  @apply mt-2 flex flex-wrap gap-2;
}

.tool-badge {
  @apply inline-flex items-center gap-1 px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded;
}

.error-toast {
  @apply absolute bottom-20 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow;
}
```

## Error Handling

```tsx
function ErrorToast({ message }: { message: string }) {
  return (
    <div className="error-toast">
      <span>Error: {message}</span>
      <button onClick={() => clearError()}>Dismiss</button>
    </div>
  );
}

function LoadingIndicator() {
  return (
    <div className="typing-indicator">
      <span></span>
      <span></span>
      <span></span>
    </div>
  );
}
```

## Verification Checklist

- [ ] ChatKit configured with allowed domains
- [ ] Chat widget displays messages correctly
- [ ] Messages sent to /api/chat endpoint
- [ ] Conversation ID maintained across messages
- [ ] Tool calls displayed visually
- [ ] Better Auth session integrated
- [ ] Error toasts shown on failures
- [ ] Loading indicators during API calls
