---
name: building-chat-interfaces
description: |
  Build AI chat interfaces with custom backends, authentication, and context injection.
  Use when integrating chat UI with AI agents, adding auth to chat, injecting user/page context,
  or implementing httpOnly cookie proxies. Covers ChatKitServer, useChatKit, and MCP auth patterns.
  NOT when building simple chatbots without persistence or custom agent integration.
---

# Building Chat Interfaces

Build production-grade AI chat interfaces with custom backend integration.

## Quick Start

```bash
# Backend (Python)
uv add chatkit-sdk agents httpx

# Frontend (React)
npm install @openai/chatkit-react
```

---

## Core Architecture

```
Frontend (React)                    Backend (Python)
┌─────────────────┐                ┌─────────────────┐
│  useChatKit()   │───HTTP/SSE───>│  ChatKitServer  │
│  - custom fetch │                │  - respond()    │
│  - auth headers │                │  - store        │
│  - page context │                │  - agent        │
└─────────────────┘                └─────────────────┘
```

---

## Backend Patterns

### 1. ChatKit Server with Custom Agent

```python
from chatkit.server import ChatKitServer
from chatkit.agents import stream_agent_response
from agents import Agent, Runner

class CustomChatKitServer(ChatKitServer[RequestContext]):
    """Extend ChatKit server with custom agent."""

    async def respond(
        self,
        thread: ThreadMetadata,
        input_user_message: UserMessageItem | None,
        context: RequestContext,
    ) -> AsyncIterator[ThreadStreamEvent]:
        if not input_user_message:
            return

        # Load conversation history
        previous_items = await self.store.load_thread_items(
            thread.id, after=None, limit=10, order="desc", context=context
        )

        # Build history string for prompt
        history_str = "\n".join([
            f"{item.role}: {item.content}"
            for item in reversed(previous_items.data)
        ])

        # Extract context from metadata
        user_info = context.metadata.get('userInfo', {})
        page_context = context.metadata.get('pageContext', {})

        # Create agent with context in instructions
        agent = Agent(
            name="Assistant",
            tools=[your_search_tool],
            instructions=f"{history_str}\nUser: {user_info.get('name')}\n{system_prompt}",
        )

        # Run agent with streaming
        result = Runner.run_streamed(agent, input_user_message.content)
        async for event in stream_agent_response(context, result):
            yield event
```

### 2. Database Persistence

```python
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)

# Pre-warm connections on startup
async def warmup_pool():
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
```

### 3. JWT/JWKS Authentication

```python
from jose import jwt
import httpx

async def get_current_user(authorization: str = Header()):
    token = authorization.replace("Bearer ", "")
    async with httpx.AsyncClient() as client:
        jwks = (await client.get(JWKS_URL)).json()
    payload = jwt.decode(token, jwks, algorithms=["RS256"])
    return payload
```

---

## Frontend Patterns

### 1. Custom Fetch Interceptor

```typescript
const { control, sendUserMessage } = useChatKit({
  api: {
    url: `${backendUrl}/chatkit`,
    domainKey: domainKey,

    // Custom fetch to inject auth and context
    fetch: async (url: string, options: RequestInit) => {
      if (!isLoggedIn) {
        throw new Error('User must be logged in');
      }

      const pageContext = getPageContext();
      const userInfo = { id: userId, name: user.name };

      // Inject metadata into request body
      let modifiedOptions = { ...options };
      if (modifiedOptions.body && typeof modifiedOptions.body === 'string') {
        const parsed = JSON.parse(modifiedOptions.body);
        if (parsed.params?.input) {
          parsed.params.input.metadata = {
            userId, userInfo, pageContext,
            ...parsed.params.input.metadata,
          };
          modifiedOptions.body = JSON.stringify(parsed);
        }
      }

      return fetch(url, {
        ...modifiedOptions,
        headers: {
          ...modifiedOptions.headers,
          'X-User-ID': userId,
          'Content-Type': 'application/json',
        },
      });
    },
  },
});
```

### 2. Page Context Extraction

```typescript
const getPageContext = useCallback(() => {
  if (typeof window === 'undefined') return null;

  const metaDescription = document.querySelector('meta[name="description"]')
    ?.getAttribute('content') || '';

  const mainContent = document.querySelector('article') ||
                     document.querySelector('main') ||
                     document.body;

  const headings = Array.from(mainContent.querySelectorAll('h1, h2, h3'))
    .slice(0, 5)
    .map(h => h.textContent?.trim())
    .filter(Boolean)
    .join(', ');

  return {
    url: window.location.href,
    title: document.title,
    path: window.location.pathname,
    description: metaDescription,
    headings: headings,
  };
}, []);
```

### 3. Script Loading Detection

```typescript
const [scriptStatus, setScriptStatus] = useState<'pending' | 'ready' | 'error'>(
  isBrowser && window.customElements?.get('openai-chatkit') ? 'ready' : 'pending'
);

useEffect(() => {
  if (!isBrowser || scriptStatus !== 'pending') return;

  if (window.customElements?.get('openai-chatkit')) {
    setScriptStatus('ready');
    return;
  }

  customElements.whenDefined('openai-chatkit').then(() => {
    setScriptStatus('ready');
  });
}, []);

// Only render when ready
{isOpen && scriptStatus === 'ready' && <ChatKit control={control} />}
```

---

## Next.js Integration

### httpOnly Cookie Proxy

When auth tokens are in httpOnly cookies (can't be read by JavaScript):

```typescript
// app/api/chatkit/route.ts
import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

export async function POST(request: NextRequest) {
  const cookieStore = await cookies();
  const idToken = cookieStore.get("auth_token")?.value;

  if (!idToken) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }

  const response = await fetch(`${API_BASE}/chatkit`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${idToken}`,
      "Content-Type": "application/json",
    },
    body: await request.text(),
  });

  // Handle SSE streaming
  if (response.headers.get("content-type")?.includes("text/event-stream")) {
    return new Response(response.body, {
      status: response.status,
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
      },
    });
  }

  return NextResponse.json(await response.json(), { status: response.status });
}
```

### Script Loading Strategy

```tsx
// app/layout.tsx
import Script from "next/script";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        {/* MUST be beforeInteractive for web components */}
        <Script
          src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
          strategy="beforeInteractive"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

---

## MCP Tool Authentication

MCP protocol doesn't forward auth headers. Pass credentials via system prompt:

```python
SYSTEM_PROMPT = """You are Assistant.

## Authentication Context
- User ID: {user_id}
- Access Token: {access_token}

CRITICAL: When calling ANY MCP tool, include:
- user_id: "{user_id}"
- access_token: "{access_token}"
"""

# Format with credentials
instructions = SYSTEM_PROMPT.format(
    user_id=context.user_id,
    access_token=context.metadata.get("access_token", ""),
)
```

---

## Common Pitfalls

| Issue | Symptom | Fix |
|-------|---------|-----|
| History not in prompt | Agent doesn't remember conversation | Include history as string in system prompt |
| Context not transmitted | Agent missing user/page info | Add to request metadata, extract in backend |
| Script not loaded | Component fails to render | Detect script loading, wait before rendering |
| Auth headers missing | Backend rejects requests | Use custom fetch interceptor |
| httpOnly cookies | Can't read token from JS | Create server-side API route proxy |
| First request slow | 7+ second delay | Pre-warm database connection pool |

---

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ building-chat-interfaces skill ready`

## If Verification Fails

1. Check: references/ folder has chatkit-integration-patterns.md
2. **Stop and report** if still failing

## Related Skills (Tiered System)

- **streaming-llm-responses** - Tier 2: Response lifecycle, progress updates, client effects
- **building-chat-widgets** - Tier 3: Interactive widgets, entity tagging, composer tools
- **fetching-library-docs** - ChatKit docs: `--library-id /openai/chatkit --topic useChatKit`

## References

- [references/chatkit-integration-patterns.md](references/chatkit-integration-patterns.md) - Complete patterns with evidence
- [references/nextjs-httponly-proxy.md](references/nextjs-httponly-proxy.md) - Next.js cookie proxy patterns