---
name: chatkit-integration
description: Foundation skill for integrating OpenAI ChatKit framework with custom backends. This skill should be used for initial ChatKit setup including server implementation, React component integration, authentication, context injection, and database persistence. For streaming UI patterns use chatkit-streaming. For interactive widgets and actions use chatkit-actions.
---

# ChatKit Integration Skill (Tier 1: Foundation)

## Overview

This skill provides the foundation for ChatKit integration - getting the basic chat working end-to-end with your custom backend and agent. It covers:

- **Backend**: ChatKitServer setup, database persistence, agent wiring
- **Frontend**: useChatKit configuration, authentication, context injection
- **Infrastructure**: Script loading, httpOnly cookie proxy (Next.js)

**For advanced capabilities, see related skills:**
- `chatkit-streaming` (Tier 2): Response lifecycle, progress updates, client effects
- `chatkit-actions` (Tier 3): Interactive widgets, entity tagging, composer tools

## Persona

You are a full-stack engineer integrating OpenAI ChatKit framework with a custom backend and AI agents. You understand that ChatKit provides standardized conversation UI/UX, but requires custom integration to work with domain-specific agents and context.

## Questions to Ask Before Implementing

1. **Backend Integration**:
   - What agent framework are you using? (OpenAI Agents SDK, LangChain, custom)
   - What tools does your agent need? (RAG search, custom functions)
   - What context does your agent need? (user profile, page context, conversation history)
   - What database are you using? (PostgreSQL, MongoDB, Redis)

2. **Frontend Integration**:
   - What frontend framework? (React, Next.js, Docusaurus)
   - How is authentication handled? (OAuth, JWT, session cookies, **httpOnly cookies**)
   - Are auth tokens stored in httpOnly cookies? (Requires server-side proxy)
   - What context can you extract client-side? (page URL, title, DOM content)
   - Do you need custom UI features? (text selection, personalization menu)

3. **Context Requirements**:
   - What user information is available? (name, email, role, preferences)
   - What page context is needed? (URL, title, headings, content)
   - How should context be transmitted? (headers, metadata, query params)
   - Should context be included in every request or only when needed?

4. **Persistence Requirements**:
   - Do conversations need to persist across sessions?
   - What's the expected conversation volume? (affects database choice)
   - Do you need multi-tenancy? (organization isolation)
   - What's the retention policy? (how long to keep conversations)

## Principles

### Backend Principles

1. **Extend ChatKit Server, Don't Replace**
   - Inherit from `ChatKitServer[RequestContext]`
   - Override only `respond()` method for agent execution
   - Let base class handle read-only operations (threads.list, items.list)
   - **Rationale**: ChatKit handles protocol, you handle agent logic

2. **Context Injection in Prompt**
   - Include conversation history as string in system prompt (CarFixer pattern)
   - Include user context (name, profile) in system prompt
   - Include page context (current page) in system prompt
   - **Rationale**: Agent SDK receives single prompt, history must be in prompt

3. **User Isolation via RequestContext**
   - All operations scoped by `user_id` in `RequestContext`
   - Store operations filter by `user_id` automatically
   - Never expose data across users
   - **Rationale**: Multi-tenant safety, data privacy

4. **Graceful Degradation**
   - System starts even if database unavailable (ChatKit disabled)
   - RAG search can fail without blocking ChatKit
   - Log warnings but don't crash
   - **Rationale**: Partial functionality better than no functionality

5. **Connection Pool Warmup**
   - Pre-warm database connections on startup
   - Avoids 7+ second first-request delay
   - Test connections before use (`pool_pre_ping=True`)
   - **Rationale**: Production-ready performance

### Frontend Principles

1. **Custom Fetch Interceptor**
   - Provide custom `fetch` function to `useChatKit` config
   - Intercept all ChatKit requests
   - Add authentication headers (`X-User-ID`)
   - Add metadata (userInfo, pageContext) to request body
   - **Rationale**: ChatKit doesn't handle auth natively, you must inject it

2. **Script Loading Detection**
   - Check for ChatKit custom element before rendering
   - Listen for script load events
   - Only render ChatKit component when script ready
   - Handle script load failures gracefully
   - **Rationale**: External script required, component fails without it

3. **Page Context Extraction**
   - Extract client-side (DOM, window.location)
   - Include: URL, title, path, headings, meta description
   - Send with every message (in metadata)
   - **Rationale**: Agent needs to know what user is viewing

4. **Build-Time Configuration**
   - Read env vars in `docusaurus.config.ts` (build-time)
   - Add to `customFields` for client-side access
   - Don't use `process.env` in browser code
   - **Rationale**: Static sites bake config at build time

5. **Authentication Gate**
   - Require login before allowing chat access
   - Show login prompt if not authenticated
   - Redirect to OAuth flow
   - **Rationale**: User ID required for conversation persistence

6. **httpOnly Cookie Proxy (Next.js)**
   - httpOnly cookies cannot be accessed from JavaScript (security feature)
   - Create server-side API route to read cookies and add Authorization header
   - Proxy forwards requests to backend with JWT token
   - **Rationale**: Secure token storage requires server-side access

7. **Next.js Script Loading Strategy**
   - Use `beforeInteractive` for web component scripts in `layout.tsx`
   - Place Script in `<head>` element
   - Script must load before React hydration for custom elements
   - **Rationale**: Web components must be defined before React renders them

## Implementation Patterns

### Pattern 1: ChatKit Server with Custom Agent

**When**: Integrating ChatKit with OpenAI Agents SDK

**Implementation**:
```python
from chatkit.server import ChatKitServer
from agents import Agent, Runner
from chatkit.agents import stream_agent_response

class CustomChatKitServer(ChatKitServer[RequestContext]):
    """Extend ChatKit server with custom agent."""
    
    async def respond(
        self,
        thread: ThreadMetadata,
        input_user_message: UserMessageItem | None,
        context: RequestContext,
    ) -> AsyncIterator[ThreadStreamEvent]:
        # Only handle user messages (let base class handle read-only ops)
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
        
        # Build context strings
        user_context_str = f"\nUser: {user_info.get('name')}\n"
        page_context_str = f"\nPage: {page_context.get('title')}\n"
        
        # Create agent with tools
        agent = Agent(
            name="Assistant",
            tools=[your_search_tool],
            instructions=f"{history_str}\n{user_context_str}{page_context_str}\n{system_prompt}",
        )
        
        # Convert message to agent input
        converter = YourThreadItemConverter()
        agent_input = await converter.to_agent_input(input_user_message)
        
        # Run agent with streaming
        agent_context = YourAgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )
        result = Runner.run_streamed(agent, agent_input, context=agent_context)
        
        # Stream results
        async for event in stream_agent_response(agent_context, result):
            yield event
```

**Evidence**: `rag-agent/chatkit_server.py:100-270`

### Pattern 2: Custom Fetch Interceptor

**When**: Adding authentication and context to ChatKit requests

**Implementation**:
```typescript
const { control, sendUserMessage } = useChatKit({
  api: {
    url: `${backendUrl}/chatkit`,
    domainKey: domainKey,
    
    // Custom fetch to inject auth and context
    fetch: async (url: string, options: RequestInit) => {
      // Check authentication
      if (!isLoggedIn) {
        throw new Error('User must be logged in');
      }
      
      const userId = session.user.id;
      const pageContext = getPageContext();
      const userInfo = {
        id: userId,
        name: session.user.name,
        email: session.user.email,
        // ... other user fields
      };
      
      // Modify request body to add metadata
      let modifiedOptions = { ...options };
      if (modifiedOptions.body && typeof modifiedOptions.body === 'string') {
        const parsed = JSON.parse(modifiedOptions.body);
        if (parsed.type === 'threads.create' && parsed.params?.input) {
          parsed.params.input.metadata = {
            userId,
            userInfo,
            pageContext,
            ...parsed.params.input.metadata,
          };
          modifiedOptions.body = JSON.stringify(parsed);
        } else if (parsed.type === 'threads.run' && parsed.params?.input) {
          if (!parsed.params.input.metadata) {
            parsed.params.input.metadata = {};
          }
          parsed.params.input.metadata.userInfo = userInfo;
          parsed.params.input.metadata.pageContext = pageContext;
          modifiedOptions.body = JSON.stringify(parsed);
        }
      }
      
      // Add authentication header
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

**Evidence**: `robolearn-interface/src/components/ChatKitWidget/index.tsx:197-240`

### Pattern 3: Script Loading Detection

**When**: ChatKit requires external script, component must wait

**Implementation**:
```typescript
const [scriptStatus, setScriptStatus] = useState<'pending' | 'ready' | 'error'>(
  isBrowser && window.customElements?.get('openai-chatkit') ? 'ready' : 'pending'
);

useEffect(() => {
  if (scriptStatus !== 'pending') return;
  
  // Check if already loaded
  if (window.customElements?.get('openai-chatkit')) {
    setScriptStatus('ready');
    return;
  }
  
  // Listen for script load events
  const handleLoaded = () => setScriptStatus('ready');
  const handleError = () => setScriptStatus('error');
  
  window.addEventListener('chatkit-script-loaded', handleLoaded);
  window.addEventListener('chatkit-script-error', handleError);
  
  // Timeout after 5 seconds
  const timeoutId = setTimeout(() => {
    if (scriptStatus === 'pending') {
      setScriptStatus('error');
    }
  }, 5000);
  
  return () => {
    window.removeEventListener('chatkit-script-loaded', handleLoaded);
    window.removeEventListener('chatkit-script-error', handleError);
    clearTimeout(timeoutId);
  };
}, [scriptStatus]);

// Only render ChatKit when script ready
{isOpen && scriptStatus === 'ready' && (
  <ChatKit control={control} />
)}
```

**Evidence**: `robolearn-interface/src/components/ChatKitWidget/index.tsx:67-113`

### Pattern 4: Page Context Extraction

**When**: Agent needs to know what page user is viewing

**Implementation**:
```typescript
const getPageContext = useCallback(() => {
  if (typeof window === 'undefined') return null;
  
  // Extract meta tags
  const metaDescription = document.querySelector('meta[name="description"]')
    ?.getAttribute('content') || '';
  
  // Find main content
  const mainContent = document.querySelector('article') || 
                     document.querySelector('main') || 
                     document.body;
  
  // Extract headings
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
    timestamp: new Date().toISOString(),
  };
}, []);
```

**Evidence**: `robolearn-interface/src/components/ChatKitWidget/index.tsx:121-151`

### Pattern 5: Text Selection "Ask" Feature

**When**: Users want to ask questions about selected content

**Implementation**:
```typescript
// Detect text selection
useEffect(() => {
  const handleSelection = () => {
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) {
      setSelectedText('');
      setSelectionPosition(null);
      return;
    }
    
    const selectedText = selection.toString().trim();
    if (selectedText.length > 0) {
      setSelectedText(selectedText);
      
      // Get selection position
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      setSelectionPosition({
        x: rect.left + rect.width / 2,
        y: rect.top - 10,
      });
    }
  };
  
  document.addEventListener('selectionchange', handleSelection);
  document.addEventListener('mouseup', handleSelection);
  
  return () => {
    document.removeEventListener('selectionchange', handleSelection);
    document.removeEventListener('mouseup', handleSelection);
  };
}, []);

// Send selected text
const handleAskSelectedText = useCallback(async () => {
  const pageContext = getPageContext();
  const messageText = `Can you explain this from "${pageContext.title}":\n\n"${selectedText}"`;
  
  if (!isOpen) {
    setIsOpen(true);
    await new Promise(resolve => setTimeout(resolve, 300));
  }
  
  await sendUserMessage({
    text: messageText,
    newThread: false,
  });
  
  // Clear selection
  window.getSelection()?.removeAllRanges();
  setSelectedText('');
  setSelectionPosition(null);
}, [selectedText, isOpen, sendUserMessage, getPageContext]);
```

**Evidence**: `robolearn-interface/src/components/ChatKitWidget/index.tsx:153-187`, `273-331`

### Pattern 6: httpOnly Cookie Proxy (Next.js App Router)

**When**: Authentication tokens stored in httpOnly cookies (cannot be read by JavaScript)

**Implementation**:
```typescript
// app/api/chatkit/route.ts
import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function POST(request: NextRequest) {
  const cookieStore = await cookies();

  // Read httpOnly cookie (only accessible server-side)
  const idToken = cookieStore.get("taskflow_id_token")?.value;

  if (!idToken) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }

  // Build target URL - note: ChatKit endpoint is at /chatkit, NOT /api/chatkit
  const url = new URL("/chatkit", API_BASE);

  try {
    const body = await request.text();

    // Forward request with Authorization header
    const response = await fetch(url.toString(), {
      method: "POST",
      headers: {
        Authorization: `Bearer ${idToken}`,
        "Content-Type": "application/json",
        // Forward custom headers
        "X-User-ID": request.headers.get("X-User-ID") || "",
        "X-Page-URL": request.headers.get("X-Page-URL") || "",
      },
      body: body || undefined,
    });

    // Handle SSE streaming responses
    if (response.headers.get("content-type")?.includes("text/event-stream")) {
      return new Response(response.body, {
        status: response.status,
        headers: {
          "Content-Type": "text/event-stream",
          "Cache-Control": "no-cache",
          "Connection": "keep-alive",
        },
      });
    }

    // Return JSON for non-streaming responses
    const data = await response.json().catch(() => null);
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("[ChatKit Proxy] Error:", error);
    return NextResponse.json({ error: "ChatKit proxy request failed" }, { status: 500 });
  }
}
```

**Evidence**: `web-dashboard/src/app/api/chatkit/route.ts`

### Pattern 7: Next.js Script Loading for Web Components

**When**: ChatKit script must load before React hydration

**Implementation**:
```tsx
// app/layout.tsx
import Script from "next/script";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        {/* MUST be in <head> with beforeInteractive for web components */}
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

**In ChatKit Widget** - wait for custom element:
```typescript
// components/chat/ChatKitWidget.tsx
const [scriptStatus, setScriptStatus] = useState<'pending' | 'ready' | 'error'>(
  isBrowser && window.customElements?.get('openai-chatkit') ? 'ready' : 'pending'
);

useEffect(() => {
  if (!isBrowser) return;

  // Already registered
  if (window.customElements?.get('openai-chatkit')) {
    setScriptStatus('ready');
    return;
  }

  // Wait for custom element to be defined
  customElements.whenDefined('openai-chatkit').then(() => {
    setScriptStatus('ready');
  });
}, []);

// Only render when ready
{isOpen && scriptStatus === 'ready' && <ChatKit control={control} />}
```

**Evidence**: `web-dashboard/src/app/layout.tsx`, `web-dashboard/src/components/chat/ChatKitWidget.tsx:42-93`

### Pattern 8: Custom Fetch with Proxy Authentication (Next.js)

**When**: Using useChatKit with httpOnly cookie proxy

**Implementation**:
```typescript
const chatkitProxyUrl = "/api/chatkit"; // Proxy handles auth

const { control, sendUserMessage } = useChatKit({
  api: {
    url: chatkitProxyUrl,
    domainKey: domainKey,

    // Custom fetch - auth handled by proxy, inject context
    fetch: async (input: RequestInfo | URL, options?: RequestInit) => {
      const url = typeof input === 'string' ? input : input.toString();

      // Client-side auth check (proxy will verify token)
      if (!isAuthenticated) {
        throw new Error('User must be logged in');
      }

      const userId = user.sub;
      const pageContext = getPageContext();

      // Inject metadata into request body
      let modifiedOptions = { ...options } as RequestInit;
      if (modifiedOptions.body && typeof modifiedOptions.body === 'string') {
        try {
          const parsed = JSON.parse(modifiedOptions.body);
          if (parsed.type === 'threads.create' && parsed.params?.input) {
            parsed.params.input.metadata = {
              userId,
              userInfo: { id: userId, name: user.name },
              pageContext,
              ...parsed.params.input.metadata,
            };
            modifiedOptions.body = JSON.stringify(parsed);
          } else if (parsed.type === 'threads.run' && parsed.params?.input) {
            parsed.params.input.metadata = {
              ...parsed.params.input.metadata,
              userInfo: { id: userId, name: user.name },
              pageContext,
            };
            modifiedOptions.body = JSON.stringify(parsed);
          }
        } catch { /* Ignore non-JSON */ }
      }

      return fetch(url, {
        ...modifiedOptions,
        credentials: 'include', // Include cookies for proxy auth
        headers: {
          ...modifiedOptions.headers,
          'X-User-ID': userId,
          'X-Page-URL': pageContext?.url || '',
          'Content-Type': 'application/json',
        },
      });
    },
  },
});
```

**Evidence**: `web-dashboard/src/components/chat/ChatKitWidget.tsx:168-296`

## When to Apply

- Integrating ChatKit with custom backend
- Adding authentication to ChatKit
- Injecting context (user, page) into agent prompts
- Implementing text selection "Ask" functionality
- Building conversational AI interfaces
- **Next.js App Router with httpOnly cookies** (use Pattern 6-8)
- **External web component scripts in Next.js** (use Pattern 7)

## Contraindications

- **Simple chat without persistence**: ChatKit may be overkill
- **No user authentication**: ChatKit requires user_id for isolation
- **Serverless functions**: Connection pooling doesn't work well
- **Very low traffic**: Overhead not justified

## Common Pitfalls

1. **History Not in Prompt**: Agent doesn't remember conversation
   - **Fix**: Include history as string in system prompt (not as messages)

2. **Context Not Transmitted**: Agent doesn't receive user/page context
   - **Fix**: Add to request metadata, extract in backend, include in prompt

3. **Script Not Loaded**: ChatKit component fails to render
   - **Fix**: Detect script loading, wait before rendering

4. **Auth Headers Missing**: Backend rejects requests
   - **Fix**: Use custom fetch interceptor to add headers

5. **Database Not Warmed**: First request takes 7+ seconds
   - **Fix**: Pre-warm connection pool on startup

6. **httpOnly Cookies Not Accessible (Next.js)**: Can't read auth token from JavaScript
   - **Symptom**: `document.cookie` returns nothing, "id_token not found"
   - **Why**: httpOnly cookies are a security feature - cannot be read by JavaScript
   - **Fix**: Create server-side API route proxy that reads cookies and adds Authorization header

7. **Script Loading Too Late (Next.js)**: "ChatKit web component is unavailable"
   - **Symptom**: 404 errors, custom element not defined
   - **Why**: `afterInteractive` strategy loads after React hydration
   - **Fix**: Use `beforeInteractive` in `<head>` within `layout.tsx`

8. **Wrong Backend Endpoint**: 404 on ChatKit requests
   - **Symptom**: `/api/proxy/chatkit` returns 404
   - **Why**: General proxy adds `/api/` prefix, but ChatKit is at `/chatkit`
   - **Fix**: Create dedicated proxy that routes to exact endpoint path

9. **MCP Tools Missing Auth Token**: Agent calls MCP tools without credentials
   - **Fix**: Pass token via system prompt so LLM includes in tool calls

10. **E402 Linter Error**: Imports after load_dotenv()
   - **Fix**: Add `# noqa: E402` to intentional imports after dotenv

11. **Type Annotation vs Runtime Mismatch (Action context parameter)**
   - **Symptom**: ValidationError trying to create RequestContext from RequestContext
   - **Why**: Type hint says `context: dict[str, Any]` but ChatKit SDK passes `RequestContext` object
   - **Fix**: Use `context` directly, don't wrap it in RequestContext constructor
   - **Detection**: Error message shows `Input should be a valid dictionary [input_value=RequestContext(...)]`

12. **Python Auto-Reload Not Working**: Changes don't take effect
   - **Symptom**: Old code still runs despite file changes
   - **Why**: Python bytecode cache (.pyc files) or uvicorn reload mechanism lag
   - **Fix**: Kill process manually and restart, or delete __pycache__ directories
   - **Prevention**: Use `--reload` flag with uvicorn, but be aware it's not 100% reliable

13. **Missing Pydantic Model Required Fields**: ValidationError on ChatKit types
   - **Symptom**: "Field required" errors when creating UserMessageItem, Action, etc.
   - **Why**: Pydantic models have strict validation, all required fields must be present
   - **Fix**: Check ChatKit type definitions, include all required fields with correct types
   - **Common mistakes**: Missing id, thread_id, created_at, inference_options fields

## Pattern 6: MCP Agent Authentication (NEW)

**When**: MCP tools need to call authenticated APIs

**Problem**: MCP protocol doesn't forward auth headers. Tools need user credentials.

**Solution**: Pass auth credentials via agent system prompt. LLM includes them in every tool call.

**Implementation**:
```python
# 1. Extract token at endpoint
@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    auth_header = request.headers.get("Authorization")
    access_token = None
    if auth_header and auth_header.startswith("Bearer "):
        access_token = auth_header[7:]  # Remove "Bearer " prefix

    # Add to metadata
    metadata["access_token"] = access_token

# 2. System prompt template
SYSTEM_PROMPT = """You are Assistant.

## Authentication Context
- User ID: {user_id}
- Access Token: {access_token}

CRITICAL: When calling ANY MCP tool, you MUST ALWAYS include:
- user_id: "{user_id}"
- access_token: "{access_token}"

{rest_of_prompt}
"""

# 3. Format with credentials
instructions = SYSTEM_PROMPT.format(
    user_id=context.user_id,
    access_token=context.metadata.get("access_token", ""),
    ...
)
```

**Flow**:
```
Frontend (Authorization: Bearer <jwt>)
    → /chatkit endpoint (extract token)
    → ChatKit server (add to metadata)
    → Agent prompt (include credentials)
    → LLM (includes in tool params)
    → MCP tool (receives token)
    → API call (Authorization header)
```

**Evidence**: `packages/api/src/taskflow_api/main.py`, `packages/api/src/taskflow_api/services/chat_agent.py`

## Pattern 7: Separate ChatKit Store Configuration

**When**: ChatKit needs its own database schema/connection

**Implementation**:
```python
# config.py - Ignore ChatKit env vars in main Settings
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",  # Ignore TASKFLOW_CHATKIT_* vars
    )

    @property
    def chat_enabled(self) -> bool:
        return os.getenv("TASKFLOW_CHATKIT_DATABASE_URL") is not None

# chatkit_store/config.py - Separate config for ChatKit
class StoreConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="TASKFLOW_CHATKIT_",  # Reads TASKFLOW_CHATKIT_DATABASE_URL
    )
    database_url: str
    schema_name: str = "taskflow_chat"  # Separate schema
```

**Evidence**: `packages/api/src/taskflow_api/config.py`, `packages/api/src/taskflow_api/chatkit_store/config.py`

## Tier Boundaries

### This Skill Covers (Tier 1: Foundation)

- ✅ ChatKitServer setup with `respond()` method
- ✅ `useChatKit` basic configuration
- ✅ Custom fetch interceptor for authentication
- ✅ Context injection (user info, page context)
- ✅ Script loading detection
- ✅ httpOnly cookie proxy (Next.js)
- ✅ Database persistence setup
- ✅ MCP tool authentication via prompt

### Use chatkit-streaming For (Tier 2: Real-time)

- ⏭️ `onResponseStart` / `onResponseEnd` handlers
- ⏭️ `onEffect` for fire-and-forget client updates
- ⏭️ `ProgressUpdateEvent` for loading states
- ⏭️ Thread lifecycle events
- ⏭️ Thread title generation

### Use chatkit-actions For (Tier 3: Interactive)

- ⏭️ Widget templates (`.widget` files)
- ⏭️ `widgets.onAction` handler
- ⏭️ `action()` method in ChatKitServer
- ⏭️ `sendCustomAction()` for widget updates
- ⏭️ Entity tagging (@mentions)
- ⏭️ Composer tools (mode selection)
- ⏭️ `ThreadItemReplacedEvent`

## References

- **ChatKit Server Spec**: `specs/007-chatkit-server/spec.md`
- **ChatKit UI Spec**: `specs/008-chatkit-ui-widget/spec.md`
- **Reference Docs**: `references/nextjs-httponly-cookie-proxy.md`, `references/nextjs-script-loading.md`
- **Blueprints**: `blueprints/openai-chatkit-advanced-samples-main/`

## Related Skills

- `chatkit-streaming` - Response lifecycle, progress updates, client effects
- `chatkit-actions` - Interactive widgets, entity tagging, composer tools


