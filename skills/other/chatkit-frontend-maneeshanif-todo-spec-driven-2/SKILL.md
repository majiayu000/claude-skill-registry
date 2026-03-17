---
name: chatkit-frontend
description: Build production-ready chat UI with OpenAI ChatKit React components. Handles ChatKit installation, useChatKit hook configuration, theming, streaming display, conversation sidebar, and rich widgets. Use when implementing chat interface, migrating from custom UI to ChatKit, or adding AI chat features for Phase 3.
allowed-tools: Bash, Write, Read, Edit, Glob, Grep
---

# ChatKit Frontend Skill

Production-ready skill for implementing OpenAI ChatKit in Next.js applications.

**Official Documentation** (ALWAYS verify before implementation):
- [OpenAI ChatKit Docs](https://platform.openai.com/docs/guides/chatkit)
- [ChatKit.js Docs](https://openai.github.io/chatkit-js/)
- [GitHub Repository](https://github.com/openai/chatkit-js)
- [Advanced Samples](https://github.com/openai/openai-chatkit-advanced-samples)
- [Domain Allowlist](https://platform.openai.com/settings/organization/security/domain-allowlist) - Required for production

---

## Overview

OpenAI ChatKit is a batteries-included framework for building AI-powered chat experiences with:

- **Deep UI Customization** - Theme, colors, radius, typography
- **Built-in Streaming** - Natural real-time conversations
- **Tool Integration** - Display agent actions and reasoning
- **Interactive Widgets** - Rich content in chat messages
- **File Handling** - Upload and attachment support
- **Thread Management** - Conversation history and switching

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Next.js Frontend                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐      ┌──────────────────────────────────────────┐ │
│  │ ConversationSidebar │    │  ChatKit Component                       │ │
│  │ (Custom)            │    │  ┌────────────────────────────────────┐  │ │
│  │                     │    │  │  <ChatKit control={control} />     │  │ │
│  │ - Thread list       │◄──►│  │  - Messages                        │  │ │
│  │ - New chat          │    │  │  - Input                           │  │ │
│  │ - Delete/rename     │    │  │  - Streaming                       │  │ │
│  └──────────────────┘      │  │  - Tool indicators                 │  │ │
│                             │  └────────────────────────────────────┘  │ │
│                             └──────────────────────────────────────────┘ │
│                                              │                           │
│                          ┌───────────────────▼───────────────────┐      │
│                          │  useChatKit Hook                       │      │
│                          │  - api: { url, domainKey }             │      │
│                          │  - theme: { colorScheme, radius }      │      │
│                          │  - startScreen: { greeting, prompts }  │      │
│                          │  - onClientTool: (invocation) => {}    │      │
│                          └───────────────────┬───────────────────┘      │
└──────────────────────────────────────────────┼───────────────────────────┘
                                               │ SSE Stream
                          ┌────────────────────▼────────────────────┐
                          │  FastAPI Backend                         │
                          │  POST /chatkit                           │
                          │  - ChatKit-compatible SSE format         │
                          └─────────────────────────────────────────┘
```

---

## Installation

### Step 1: Install ChatKit Package

```bash
cd frontend
npm install @openai/chatkit-react
```

### Step 2: Verify Installation

```bash
# Check package.json
grep chatkit package.json
```

---

## Quick Start

### Basic ChatKit Integration

```tsx
// app/chat/page.tsx
'use client';

import { ChatKit, useChatKit } from '@openai/chatkit-react';

export default function ChatPage() {
  const { control } = useChatKit({
    api: {
      url: `${process.env.NEXT_PUBLIC_API_URL}/chatkit`,
      domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY || 'local-dev',
    },
  });

  return (
    <div className="h-screen w-full">
      <ChatKit control={control} className="h-full w-full" />
    </div>
  );
}
```

### With Full Configuration

```tsx
// app/chat/page.tsx
'use client';

import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useAuthStore } from '@/stores/auth-store';
import { useConversationStore } from '@/stores/conversation-store';

export default function ChatPage() {
  const { user } = useAuthStore();
  const { currentConversation, refreshConversations } = useConversationStore();

  const { control } = useChatKit({
    // API Configuration
    api: {
      url: `${process.env.NEXT_PUBLIC_API_URL}/chatkit`,
      domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY || 'local-dev',
    },

    // Theme Configuration
    theme: {
      colorScheme: 'light', // 'light' | 'dark' | 'system'
      radius: 'round',      // 'sharp' | 'round' | 'pill'
      color: {
        accent: { primary: '#0066cc', level: 2 },
        grayscale: { hue: 220, tint: 6, shade: -4 },
      },
    },

    // Start Screen
    startScreen: {
      greeting: `Hello${user?.name ? `, ${user.name}` : ''}! How can I help you today?`,
      prompts: [
        'Show my tasks',
        'Add a new task',
        'What tasks are due today?',
        'Mark my grocery task as complete',
      ],
    },

    // Header Configuration
    header: {
      enabled: true,
      title: 'Task Assistant',
    },

    // Composer Configuration
    composer: {
      placeholder: 'Ask about your tasks...',
    },

    // History (built-in - optional, we use custom sidebar)
    history: {
      enabled: false, // Disable built-in, use custom ConversationSidebar
    },

    // Client-side Tool Handling
    onClientTool: async (invocation) => {
      console.log('Client tool invoked:', invocation.name, invocation.params);

      // Handle client-side tools (theme switching, etc.)
      if (invocation.name === 'switch_theme') {
        // Handle theme change
        return { success: true };
      }

      return { success: false };
    },

    // Error Handling
    onError: ({ error }) => {
      console.error('ChatKit error:', error);
    },

    // Message Events
    onMessage: (message) => {
      console.log('New message:', message);
      // Refresh conversations after message
      refreshConversations();
    },
  });

  return (
    <div className="h-screen w-full">
      <ChatKit
        control={control}
        className="h-full w-full max-w-4xl mx-auto"
      />
    </div>
  );
}
```

---

## Project Structure

```
frontend/
├── app/
│   └── chat/
│       ├── layout.tsx              # Chat layout with sidebar
│       └── page.tsx                # ChatKit page
│
├── components/
│   ├── chat/
│   │   └── ChatKitWrapper.tsx      # Optional ChatKit wrapper
│   │
│   └── conversation/               # Custom sidebar (keep existing)
│       ├── ConversationSidebar.tsx
│       ├── ConversationList.tsx
│       ├── ConversationItem.tsx
│       └── NewChatButton.tsx
│
├── stores/
│   └── conversation-store.ts       # Conversation state (keep existing)
│
└── lib/
    └── chatkit/
        └── config.ts               # ChatKit configuration utilities
```

---

## Theming

### Dark Mode Support

```tsx
'use client';

import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useTheme } from 'next-themes';

export function ThemedChatKit() {
  const { theme } = useTheme();
  const isDark = theme === 'dark';

  const { control } = useChatKit({
    api: { url: '/chatkit', domainKey: 'local-dev' },
    theme: {
      colorScheme: isDark ? 'dark' : 'light',
      radius: 'round',
      color: {
        grayscale: {
          hue: 220,
          tint: 6,
          shade: isDark ? -1 : -4,
        },
        accent: {
          primary: isDark ? '#f1f5f9' : '#0f172a',
          level: 1,
        },
      },
    },
  });

  return <ChatKit control={control} className="h-full w-full" />;
}
```

### Tailwind CSS Integration

```tsx
<ChatKit
  control={control}
  className="
    h-full w-full
    [--chatkit-bg:hsl(var(--background))]
    [--chatkit-text:hsl(var(--foreground))]
    [--chatkit-primary:hsl(var(--primary))]
    [--chatkit-border:hsl(var(--border))]
  "
/>
```

---

## Conversation Management

### Custom Sidebar with ChatKit

```tsx
// app/chat/layout.tsx
'use client';

import { ConversationSidebar } from '@/components/conversation/ConversationSidebar';

export default function ChatLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen">
      {/* Custom Conversation Sidebar */}
      <ConversationSidebar />

      {/* ChatKit Area */}
      <div className="flex-1 overflow-hidden">
        {children}
      </div>
    </div>
  );
}
```

### Thread Switching

```tsx
// When user selects a conversation from sidebar
const handleSelectConversation = (conversationId: number) => {
  // Update URL or state
  router.push(`/chat?thread=${conversationId}`);

  // ChatKit will load the thread automatically if configured
};
```

---

## Environment Variables

```env
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000

# ChatKit Domain Key (REQUIRED for production)
# Get from: https://platform.openai.com/settings/organization/security/domain-allowlist
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-here
```

### Domain Allowlist Configuration (Production)

1. Deploy frontend to get production URL (e.g., `https://your-app.vercel.app`)
2. Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
3. Add your production domain
4. Copy domain key to `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`

**Note**: localhost works without domain allowlist configuration.

---

## Migration from Custom UI

### Before (Custom Components)

```tsx
// OLD: Custom chat interface
import { ChatContainer } from '@/components/chat/ChatContainer';
import { MessageList } from '@/components/chat/MessageList';
import { MessageInput } from '@/components/chat/MessageInput';

export default function ChatPage() {
  return (
    <ChatContainer>
      <MessageList messages={messages} />
      <MessageInput onSend={sendMessage} />
    </ChatContainer>
  );
}
```

### After (ChatKit)

```tsx
// NEW: ChatKit
import { ChatKit, useChatKit } from '@openai/chatkit-react';

export default function ChatPage() {
  const { control } = useChatKit({
    api: { url: '/chatkit', domainKey: 'local-dev' },
  });

  return <ChatKit control={control} className="h-full w-full" />;
}
```

### What to Keep

- `ConversationSidebar` - Better UX than built-in history
- `conversation-store.ts` - Thread management state
- Auth integration - User context for ChatKit

### What to Remove

- `ChatContainer.tsx` - Replaced by ChatKit
- `MessageList.tsx` - Replaced by ChatKit
- `MessageInput.tsx` - Replaced by ChatKit
- `StreamingMessage.tsx` - Replaced by ChatKit
- Custom SSE client (partially) - ChatKit handles streaming

---

## Verification Checklist

- [ ] `@openai/chatkit-react` installed
- [ ] ChatKit page created at `/chat`
- [ ] `useChatKit` hook configured with API URL
- [ ] Theme matches app design system
- [ ] Dark mode works correctly
- [ ] Start screen shows greeting and prompts
- [ ] Custom ConversationSidebar integrated
- [ ] Backend `/chatkit` endpoint working
- [ ] Streaming responses display correctly
- [ ] Domain allowlist configured (production)
- [ ] Mobile responsive design

---

## Common Issues

### ChatKit Not Rendering

```tsx
// Ensure client-side rendering
'use client';

// Check control is initialized
if (!control) return <div>Loading...</div>;
```

### CORS Errors

```python
# Backend: Add ChatKit origins to CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### SSE Format Issues

```python
# Backend: Use correct SSE format for ChatKit
yield f"data: {json.dumps({'type': 'text', 'content': chunk})}\n\n"
yield "data: [DONE]\n\n"
```

---

## See Also

- [REFERENCE.md](./REFERENCE.md) - Complete API reference
- [examples.md](./examples.md) - Full code examples
- [templates/](./templates/) - Starter templates
- [chatkit-backend skill](../chatkit-backend/) - Backend integration
