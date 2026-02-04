---
name: chatkit-integration
description: Integrate OpenAI ChatKit framework with custom backend and AI agents. Handles ChatKit server implementation, React component integration, context injection, and conversation persistence.
---

# ChatKit Integration Skill

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
   - How is authentication handled? (OAuth, JWT, session cookies)
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

## When to Apply

- Integrating ChatKit with custom backend
- Adding authentication to ChatKit
- Injecting context (user, page) into agent prompts
- Implementing text selection "Ask" functionality
- Building conversational AI interfaces

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

## References

- **ChatKit Server Spec**: `specs/007-chatkit-server/spec.md`
- **ChatKit UI Spec**: `specs/008-chatkit-ui-widget/spec.md`
- **Implementation**: `rag-agent/chatkit_server.py`, `robolearn-interface/src/components/ChatKitWidget/`


