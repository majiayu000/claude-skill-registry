---
name: chatkit-frontend-integration
description: |
  This skill configures OpenAI ChatKit for React frontends with proper domain security, authentication, and backend integration. It covers ChatKit UI setup, domain allowlist configuration, domain key injection, client secret management, and production vs localhost deployment patterns. Use when integrating ChatKit widget, configuring domain security, or connecting ChatKit UI to backend endpoints.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# ChatKit Frontend Integration

## What This Skill Does

This skill provides comprehensive guidance for integrating OpenAI ChatKit into React applications. It covers:

- ChatKit UI component setup with `@openai/chatkit-react`
- Domain allowlist security configuration
- Domain key injection for custom backends
- Client secret authentication flow
- Backend endpoint connection patterns
- Production vs localhost deployment differences

## When to Use

- When setting up ChatKit widget in a React application
- When configuring domain allowlist for ChatKit security
- When implementing domain key injection for custom integrations
- When connecting ChatKit frontend to a backend endpoint
- When handling authentication with client secrets
- When troubleshooting "blank screen" or domain verification issues
- When deploying ChatKit to production environments

## When NOT to Use

- When building backend ChatKit server (use chatkit-python-backend skill)
- When working on non-ChatKit chat implementations
- When using vanilla JavaScript without React
- When specifications don't require ChatKit integration

## Required Clarifications

Before implementing ChatKit, clarify:

1. **Integration Type**: Hosted (OpenAI-managed) or Custom/Self-hosted backend?
2. **Environment**: Production domain or localhost development?
3. **Authentication**: Using client secrets or domain keys?
4. **Backend Framework**: FastAPI, Next.js API routes, or other?

---

## Core Concepts

### Architecture Overview

ChatKit uses a **three-party authentication system**:

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│   Client    │ ───► │   Backend    │ ───► │  OpenAI API     │
│  (ChatKit)  │ ◄─── │   Server     │ ◄─── │                 │
└─────────────┘      └──────────────┘      └─────────────────┘
     │                      │                      │
     │ 1. Request secret    │ 2. Generate token    │
     │ ◄────────────────────│ ◄────────────────────│
     │                      │                      │
     │ 3. Direct chat       │                      │
     │ ─────────────────────────────────────────►  │
```

1. **Client** requests a short-lived `client_secret` from your backend
2. **Backend** uses your API key to generate the token via OpenAI
3. **Client** uses the token to communicate directly with OpenAI

### Integration Types

| Type | Backend | Domain Key | Use Case |
|------|---------|------------|----------|
| **Hosted** | OpenAI-managed | Not needed | Agent Builder workflows |
| **Custom** | Self-hosted | Required | Full control, custom logic |

---

## Installation

### Package Installation

```bash
# React package (recommended)
npm install @openai/chatkit-react

# TypeScript types (optional, for enhanced type support)
npm install @openai/chatkit
```

### CDN Script (Alternative)

```html
<script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js" async></script>
```

### TypeScript Configuration

Add to `tsconfig.json` for global type support:

```json
{
  "compilerOptions": {
    "types": ["@openai/chatkit"]
  }
}
```

---

## Domain Allowlist Configuration (CRITICAL)

### Why This Matters

ChatKit **will not render** on domains not explicitly allowed. This is the most common cause of "blank screen" issues.

### Configuration Steps

1. Navigate to: **https://platform.openai.com/settings/organization/security/domain-allowlist**
2. Add your production domain (e.g., `myapp.com`)
3. Wait **20-30 minutes** for verification to activate
4. For localhost: See [Localhost Development](#localhost-development)

### Common Mistakes

```typescript
// BAD: Will fail silently on unregistered domain
const { control } = useChatKit({
  api: { url: '/api/chat' }  // Domain not in allowlist
});

// GOOD: After adding domain to allowlist
const { control } = useChatKit({
  api: {
    async getClientSecret() { /* ... */ }
  }
});
```

### Domain Verification Behavior

- ChatKit calls `POST /v1/chatkit/domain_keys/verify_hosted`
- If domain not in allowlist: silent failure, blank widget
- No console errors shown (security feature)
- Mismatched API key organization: authorization errors

---

## Frontend Integration

### Basic Setup (Hosted Backend)

```tsx
// components/Chat.tsx
import { ChatKit, useChatKit } from '@openai/chatkit-react';

export function Chat() {
  const { control } = useChatKit({
    api: {
      async getClientSecret(existingSecret) {
        // Request new or refresh existing token
        const endpoint = existingSecret
          ? '/api/chatkit/refresh'
          : '/api/chatkit/session';

        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: existingSecret
            ? JSON.stringify({ currentSecret: existingSecret })
            : undefined,
        });

        if (!res.ok) throw new Error('Failed to get client secret');

        const { client_secret } = await res.json();
        return client_secret;
      },
    },
  });

  return (
    <ChatKit
      control={control}
      className="h-[600px] w-full max-w-[400px]"
    />
  );
}
```

### Custom Backend Setup (Domain Key)

```tsx
// components/Chat.tsx
import { ChatKit, useChatKit } from '@openai/chatkit-react';

export function Chat() {
  const { control } = useChatKit({
    api: {
      url: process.env.NEXT_PUBLIC_CHATKIT_API_URL,
      domainKey: process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY,
    },
  });

  return (
    <ChatKit
      control={control}
      className="h-[600px] w-full max-w-[400px]"
    />
  );
}
```

### Full-Featured Implementation

```tsx
// components/ChatWidget.tsx
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useState, useCallback } from 'react';

interface ChatWidgetProps {
  userId?: string;
  threadId?: string;
  onError?: (error: Error) => void;
}

export function ChatWidget({ userId, threadId, onError }: ChatWidgetProps) {
  const [isReady, setIsReady] = useState(false);

  const handleError = useCallback((event: CustomEvent) => {
    console.error('ChatKit error:', event.detail);
    onError?.(new Error(event.detail?.message || 'ChatKit error'));
  }, [onError]);

  const handleReady = useCallback(() => {
    setIsReady(true);
  }, []);

  const { control, ref, setThreadId, sendUserMessage } = useChatKit({
    api: {
      async getClientSecret(existing) {
        const res = await fetch('/api/chatkit/session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            userId,
            refreshToken: existing
          }),
        });

        if (!res.ok) {
          const error = await res.json();
          throw new Error(error.message || 'Session creation failed');
        }

        const { client_secret } = await res.json();
        return client_secret;
      },
    },
    // Event handlers
    onError: handleError,
    onReady: handleReady,
    onResponseStart: () => console.log('Response started'),
    onResponseEnd: () => console.log('Response ended'),
    onThreadChange: (e) => console.log('Thread changed:', e.detail),
  });

  // Set initial thread if provided
  useEffect(() => {
    if (threadId && isReady) {
      setThreadId(threadId);
    }
  }, [threadId, isReady, setThreadId]);

  return (
    <div className="relative">
      {!isReady && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100">
          <span className="animate-pulse">Loading chat...</span>
        </div>
      )}
      <ChatKit
        ref={ref}
        control={control}
        className="h-[600px] w-full rounded-lg shadow-lg"
      />
    </div>
  );
}
```

---

## useChatKit Hook API

### Configuration Options

```typescript
interface UseChatKitOptions {
  api: {
    // For hosted integration (recommended)
    getClientSecret?: (existing?: string) => Promise<string>;

    // For custom backend
    url?: string;
    domainKey?: string;
  };

  // Event handlers
  onError?: (event: CustomEvent) => void;
  onReady?: () => void;
  onResponseStart?: () => void;
  onResponseEnd?: () => void;
  onThreadChange?: (event: CustomEvent) => void;
  onThreadLoadStart?: () => void;
  onThreadLoadEnd?: () => void;
}
```

### Returned Methods

```typescript
const {
  control,           // Pass to <ChatKit control={control} />
  ref,               // Optional ref for imperative access

  // Imperative methods
  focusComposer,     // Focus the input field
  setThreadId,       // Switch to a different thread
  sendUserMessage,   // Programmatically send a message
  setComposerValue,  // Set input field value
  fetchUpdates,      // Fetch latest updates
  sendCustomAction,  // Send custom widget action
  showHistory,       // Show conversation history
  hideHistory,       // Hide conversation history
} = useChatKit(options);
```

---

## Backend Endpoint Examples

### FastAPI (Python)

```python
# app/api/chatkit.py
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel

router = APIRouter(prefix="/api/chatkit")
client = OpenAI()

class SessionRequest(BaseModel):
    userId: str | None = None
    refreshToken: str | None = None

class SessionResponse(BaseModel):
    client_secret: str

@router.post("/session", response_model=SessionResponse)
async def create_session(request: SessionRequest):
    try:
        # Create or refresh ChatKit session
        session = client.chatkit.sessions.create(
            # Configure based on your needs
            model="gpt-4o",
            tools=[],
        )
        return SessionResponse(client_secret=session.client_secret)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refresh", response_model=SessionResponse)
async def refresh_session(request: SessionRequest):
    try:
        # Refresh existing session
        session = client.chatkit.sessions.refresh(
            client_secret=request.refreshToken
        )
        return SessionResponse(client_secret=session.client_secret)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Next.js API Route

```typescript
// app/api/chatkit/session/route.ts
import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';

const openai = new OpenAI();

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Create ChatKit session
    const session = await openai.chatkit.sessions.create({
      model: 'gpt-4o',
      // Add your configuration
    });

    return NextResponse.json({
      client_secret: session.client_secret
    });
  } catch (error) {
    console.error('ChatKit session error:', error);
    return NextResponse.json(
      { error: 'Failed to create session' },
      { status: 500 }
    );
  }
}
```

---

## Localhost Development

### The Challenge

- Localhost (`localhost`, `127.0.0.1`) cannot be added to domain allowlist
- Domain verification will fail for local development
- This is a security feature, not a bug

### Solutions

#### Option 1: Ngrok Tunneling (Recommended)

```bash
# Install ngrok
npm install -g ngrok

# Start your dev server
npm run dev  # Usually http://localhost:3000

# In another terminal, create tunnel
ngrok http 3000
```

Then add the ngrok domain (e.g., `abc123.ngrok.io`) to your allowlist.

#### Option 2: Custom API Integration

Use `api.url` and `api.domainKey` instead of hosted integration:

```tsx
const { control } = useChatKit({
  api: {
    url: 'http://localhost:8000/api/chatkit',
    domainKey: process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY,
  },
});
```

#### Option 3: Proxy Configuration

```typescript
// next.config.js
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/chatkit/:path*',
        destination: 'https://api.openai.com/v1/chatkit/:path*',
      },
    ];
  },
};
```

---

## Production Deployment

### Environment Variables

```bash
# .env.production
NEXT_PUBLIC_CHATKIT_API_URL=https://api.yourdomain.com/chatkit
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=dk_xxxxxxxxxxxx  # For custom integration only
OPENAI_API_KEY=sk_xxxxxxxxxxxx  # Server-side only, never expose
```

### Pre-Deployment Checklist

```markdown
- [ ] Production domain added to OpenAI allowlist
- [ ] Waited 20-30 minutes after adding domain
- [ ] API key matches organization with domain allowlist
- [ ] OPENAI_API_KEY is server-side only (not NEXT_PUBLIC_)
- [ ] Error boundaries implemented around ChatKit
- [ ] Loading states for initial render
- [ ] Token refresh logic implemented
```

### Security Best Practices

```typescript
// NEVER do this - exposes API key
const { control } = useChatKit({
  api: {
    apiKey: process.env.OPENAI_API_KEY,  // WRONG!
  },
});

// ALWAYS do this - use backend for token generation
const { control } = useChatKit({
  api: {
    async getClientSecret() {
      const res = await fetch('/api/chatkit/session', { method: 'POST' });
      const { client_secret } = await res.json();
      return client_secret;
    },
  },
});
```

---

## Troubleshooting

### Blank Screen / Widget Not Rendering

1. **Check domain allowlist** at https://platform.openai.com/settings/organization/security/domain-allowlist
2. Verify domain matches exactly (including `www.` if used)
3. Wait 20-30 minutes after adding new domain
4. Check browser console for network errors

### 401/403 Authorization Errors

1. Verify API key belongs to same organization as allowlist
2. Check API key has ChatKit permissions
3. Ensure `getClientSecret` endpoint is accessible

### Token Refresh Failures

```typescript
// Implement proper refresh logic
async getClientSecret(existing) {
  if (!existing) {
    // First-time token request
    return await createNewSession();
  }

  try {
    // Try to refresh
    return await refreshSession(existing);
  } catch (error) {
    // If refresh fails, create new session
    return await createNewSession();
  }
}
```

### CORS Issues

```python
# FastAPI CORS configuration
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://yourdomain.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## File Structure

```
src/
├── components/
│   └── chat/
│       ├── ChatWidget.tsx       # Main ChatKit wrapper
│       ├── ChatError.tsx        # Error boundary
│       └── ChatLoading.tsx      # Loading state
├── hooks/
│   └── useChatSession.ts        # Session management hook
├── lib/
│   └── chatkit/
│       ├── client.ts            # API client
│       └── types.ts             # Type definitions
└── app/
    └── api/
        └── chatkit/
            └── session/
                └── route.ts     # Session endpoint
```

---

## Integration with Other Skills

- **frontend-architecture**: ChatKit components fit within frontend structure
- **fastapi-architecture**: Backend endpoints follow FastAPI patterns
- **auth-aware-ui**: ChatKit integrates with existing auth flow
- **api-client-design**: Session management follows API patterns

---

## References

- [ChatKit.js Documentation](https://openai.github.io/chatkit-js/)
- [ChatKit React Package](https://github.com/openai/chatkit-js/tree/main/packages/chatkit-react)
- [ChatKit Python SDK](https://github.com/openai/chatkit-python)
- [Advanced Samples](https://github.com/openai/openai-chatkit-advanced-samples)
- [Domain Allowlist Settings](https://platform.openai.com/settings/organization/security/domain-allowlist)
