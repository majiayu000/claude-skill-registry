---
name: chatkit-botbuilder
description: Guide for creating production-grade ChatKit chatbots that integrate OpenAI Agents SDK with MCP tools and custom backends. Use when building AI-powered chatbots with specialized capabilities, real-time task execution, and user isolation for any application.
license: Complete terms in LICENSE.txt
---

# ChatKit Botbuilder

## Overview

Create production-grade chatbots using the OpenAI ChatKit framework. This skill enables building chatbots that:

- **Integrate AI Agents**: Use OpenAI Agents SDK for intelligent conversation handling
- **Execute Tools**: Connect MCP (Model Context Protocol) tools for real-world task execution
- **Support Custom Backends**: Build FastAPI backends with full protocol support
- **Ensure User Isolation**: Implement multi-user systems with JWT authentication
- **Real-Time Synchronization**: Enable live UI updates when chatbot performs actions
- **Flexible Deployment**: Deploy to web, mobile, or desktop applications

This skill provides the complete architecture pattern for ChatKit integration, from frontend configuration to backend server implementation.

---

## When to Use This Skill

Use this skill when you need to:

1. **Build a task management chatbot** - Create conversational interfaces for task creation, updates, completion
2. **Integrate AI into existing apps** - Add ChatKit to dashboards, web apps, or platforms
3. **Create specialized AI assistants** - Build domain-specific chatbots with custom tool integrations
4. **Implement multi-user chatbots** - Create systems where each user has isolated conversations and data
5. **Add real-time capabilities** - Build chatbots that trigger actual application changes
6. **Deploy AI conversations** - Create chatbots that interact with your database and APIs

---

## Architecture Overview

### High-Level Flow

```
User Message
    ↓
ChatKit Frontend (React/Next.js)
    ↓ [JWT Token in Authorization Header]
    ↓
FastAPI Backend (ChatKit Server)
    ↓ [Extract user_id from JWT]
    ↓
OpenAI Agent (Agents SDK)
    ↓ [Needs tool execution]
    ↓
MCP Tools (Custom Tool Functions)
    ↓ [Creates/Updates/Lists data]
    ↓
Database (User-Isolated Data)
    ↓
Response → ChatKit → Frontend → User
```

### Key Components

1. **Frontend (Next.js + ChatKit SDK)**
   - ChatKit UI component with conversation history
   - JWT token management in localStorage
   - Custom fetch wrapper with Bearer token authentication
   - Real-time auto-refresh to sync with backend changes

2. **Backend (FastAPI + ChatKit Server)**
   - ChatKit protocol endpoint handling requests
   - MyChatKitServer class extending ChatKitServer
   - User isolation through JWT middleware
   - Tool wrapper functions for automatic user_id injection

3. **Agent (OpenAI Agents SDK)**
   - Task management agent with instructions
   - Tool registration and execution
   - Session management

4. **Tools (MCP + Custom Functions)**
   - Wrapped functions injecting user_id automatically
   - Database operations with user isolation
   - Consistent error handling

5. **Database**
   - SQLModel ORM models
   - Per-user task filtering
   - Conversation persistence

---

## Quick Start Workflow

### Phase 1: Backend Setup (FastAPI)

**1. Create ChatKit Server Class**

```python
from chatkit.server import ChatKitServer
from chatkit.store import Store

class MyChatKitServer(ChatKitServer):
    def __init__(self):
        store = CustomChatKitStore()
        super().__init__(store=store)

    async def respond(self, thread, input, context):
        """Process user message and stream AI response"""
        user_id = getattr(context, 'user_id', None)
        # Create agent with wrapped tools
        # Stream response using official pattern
```

**2. Create MCP Tool Wrappers**

```python
# Extract user_id from context and inject into tool calls
def add_task_wrapper(title: str, description: str = None):
    return mcp_add_task(user_id=user_id, title=title, description=description)

def list_tasks_wrapper(status: str = "all"):
    return mcp_list_tasks(user_id=user_id, status=status)
```

**3. Create FastAPI Endpoint**

```python
@router.post("/api/v1/chatkit")
async def chatkit_protocol_endpoint(request: Request):
    user_id = request.state.user_id  # From JWT middleware
    context = create_context_object(user_id=user_id)
    result = await chatkit_server.process(body, context)
    return StreamingResponse(result, media_type="text/event-stream")
```

**4. Configure JWT Middleware**

```python
class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Extract JWT token from Authorization header
        # Decode and set request.state.user_id
        # All endpoints have access to authenticated user_id
```

### Phase 2: Frontend Setup (Next.js + React)

**1. Configure ChatKit SDK**

```typescript
const chatKitConfig: UseChatKitOptions = {
  api: {
    url: `${API_BASE_URL}/api/v1/chatkit`,
    domainKey: 'your-domain-key',
    fetch: authenticatedFetch, // Custom fetch with JWT
  },
  theme: 'light',
  header: { enabled: true, title: { text: 'AI Chat' } },
  history: { enabled: true },
}
```

**2. Create Authenticated Fetch Wrapper**

```typescript
async function authenticatedFetch(input, options) {
  const token = localStorage.getItem('access_token')
  const headers = {
    ...options?.headers,
    'Authorization': `Bearer ${token}`,
  }
  return fetch(input, { ...options, headers })
}
```

**3. Integrate ChatKit Widget**

```typescript
import { ChatKitWidget } from '@openai/chatkit-react'

export default function Dashboard() {
  return (
    <div className="flex gap-4">
      {/* Your app content */}
      {showChat && (
        <ChatKitWidget {...chatKitConfig} />
      )}
    </div>
  )
}
```

**4. Add Auto-Refresh for Real-Time Sync**

```typescript
useEffect(() => {
  if (!showChatKit) return

  // Refresh immediately when chat opens
  fetchTasks()

  // Refresh every 1 second for real-time updates
  const interval = setInterval(() => {
    fetchTasks()
  }, 1000)

  return () => clearInterval(interval)
}, [showChatKit])
```

### Phase 3: Tool Implementation (MCP)

**1. Create MCP Tools with User Isolation**

```python
def add_task(user_id: str, title: str, description: Optional[str] = None):
    """Create task - receives user_id from wrapper"""
    task = Task(
        id=str(uuid.uuid4()),
        user_id=user_id,  # Critical: ensure user isolation
        title=title,
        description=description,
        completed=False,
        created_at=datetime.utcnow(),
    )
    with Session(engine) as session:
        session.add(task)
        session.commit()
```

**2. Register MCP Tools**

```python
mcp_server = MCPServer()
mcp_server.register_tool("add_task", add_task)
mcp_server.register_tool("list_tasks", list_tasks)
mcp_server.register_tool("delete_task", delete_task)
# ... more tools
```

---

## Core Patterns & Best Practices

### 1. User Isolation Strategy

**Three-Level Guarantee:**

1. **Middleware Level** - JWT validation ensures only authenticated users
2. **Tool Level** - Wrapper functions automatically inject user_id
3. **Database Level** - All queries filtered by user_id

```python
# Middleware extracts user_id from token
request.state.user_id = payload.get("user_id")

# Tool wrapper captures and injects it
def add_task_wrapper(title):
    return mcp_add_task(user_id=user_id, ...)

# Database enforces it
WHERE user_id = ? AND task_id = ?
```

### 2. Message Flow with User Context

```
User sends: "Create a task called 'Buy milk'"
    ↓
ChatKit Protocol: POST /api/v1/chatkit
    Header: Authorization: Bearer <JWT>
    Body: { "type": "message", "text": "Create..." }
    ↓
JWT Middleware:
    Extracts user_id from token → request.state.user_id
    ↓
ChatKit Server (MyChatKitServer.respond):
    Gets user_id from context
    Creates wrapper functions capturing user_id
    Passes wrappers to Agent
    ↓
OpenAI Agent:
    Receives message: "Create a task..."
    Selects tool: add_task_wrapper
    Calls: add_task_wrapper(title="Buy milk")
    ↓
Wrapper Function:
    Calls: mcp_add_task(user_id="user-123", title="Buy milk")
    ↓
MCP Tool:
    Creates task with correct user_id
    Returns: {"task_id": "...", "title": "Buy milk"}
    ↓
Agent Response:
    "I've created 'Buy milk' task ✓"
    ↓
ChatKit Frontend:
    Displays response
    Auto-refreshes task list → Sees new task
```

### 3. Streaming Response Pattern

```python
# Official ChatKit pattern using Runner.run_streamed
result = Runner.run_streamed(
    task_agent.agent,
    agent_input,
    context=agent_context,
)

# Stream events using official stream_agent_response
async for event in stream_agent_response(agent_context, result):
    yield event
```

### 4. Thread and Item Management

```python
# Add user message to thread
await self.store.add_thread_item(thread.id, input, context)

# Load conversation history
items_page = await self.store.load_thread_items(
    thread.id,
    after=None,
    limit=30,
    order="desc",
    context=context,
)

# Convert to agent input
agent_input = await simple_to_agent_input(items)
```

---

## Integration Patterns

### Pattern 1: Task Management Chatbot (Basic)

**What it does:**
- Users create tasks by talking to ChatKit
- ChatKit shows task list in sidebar
- Auto-refresh keeps task list in sync

**Files to reference:**
- [TaskPilotAI Backend Architecture](./references/taskpilot_backend_architecture.md)
- [Frontend Integration Pattern](./references/frontend_integration.md)

### Pattern 2: Multi-App ChatKit Deployment

**What it does:**
- Deploy ChatKit to multiple applications
- Share the same backend and database
- Each app has isolated user contexts

**Key setup:**
- Use environment variables for API_BASE_URL
- Configure domain key per application
- Implement per-app authentication

### Pattern 3: Real-Time Collaboration

**What it does:**
- Multiple users chat with the same chatbot instance
- Auto-refresh keeps everyone's data in sync
- User isolation prevents cross-user data leaks

**Implementation:**
- WebSocket connections for true real-time (optional advanced)
- Polling with auto-refresh for simplicity
- Database transactions for data consistency

---

## Common Issues & Solutions

### Issue 1: Tasks Created in ChatKit Don't Appear in Dashboard

**Root Cause:** user_id not passed to MCP tools

**Solution:** Use wrapper functions that capture and inject user_id
```python
def add_task_wrapper(title):
    return mcp_add_task(user_id=user_id, title=title)
```

### Issue 2: One User Sees Another User's Tasks

**Root Cause:** Missing user_id filter in database queries

**Solution:** Always filter by user_id at the tool level
```python
stmt = select(Task).where(
    Task.user_id == user_id,
    Task.completed == False
)
```

### Issue 3: ChatKit API Endpoint Not Found

**Root Cause:** Router not included in FastAPI app

**Solution:** Include router in main.py
```python
from routes import chatkit
app.include_router(chatkit.router)
```

### Issue 4: Chat Widget Not Showing Messages

**Root Cause:** Custom fetch not adding JWT token

**Solution:** Ensure authenticatedFetch adds Bearer token
```typescript
const token = localStorage.getItem('access_token')
headers['Authorization'] = `Bearer ${token}`
```

---

## Advanced Topics

### Real-Time Updates (WebSocket)

For true real-time (not polling):
- Implement WebSocket endpoint alongside HTTP endpoint
- Broadcast updates to all connected clients
- Maintain connection state with user context

### Custom Tool Schemas

Structure tool responses for ChatKit widgets:
```python
return {
    "tasks": task_list,
    "total": len(task_list),
    "pending": pending_count,
    "message": "You have 5 tasks",
    "widget": {
        "type": "card",
        "items": formatted_items,
    }
}
```

### Session Persistence

Store conversation history in database:
- Link conversations to users
- Retrieve chat history for context
- Allow resuming conversations

---

## Resources

This skill includes comprehensive resources for building ChatKit chatbots:

### references/

**Backend Architecture:** Complete FastAPI ChatKit server implementation details and patterns

**Frontend Integration:** Next.js ChatKit widget configuration and authentication

**MCP Tools Guide:** Creating wrapped tool functions with automatic user_id injection

**User Isolation:** Three-level user isolation strategy and verification checklist

### scripts/

**chatkit_server_template.py** - FastAPI ChatKit server boilerplate with all required methods

**mcp_wrapper_generator.py** - Script to auto-generate MCP tool wrappers

**frontend_config_generator.ts** - TypeScript config generator for ChatKit frontend setup

### assets/

**chatkit-nextjs-template/** - Complete Next.js project with ChatKit integrated

**fastapi-backend-template/** - Complete FastAPI backend with ChatKit server implementation

---

## Verification Checklist

When building a ChatKit chatbot, verify:

- [ ] JWT middleware extracts user_id from token
- [ ] ChatKit endpoint receives user_id in context
- [ ] Tool wrappers capture and inject user_id
- [ ] Database queries filter by user_id
- [ ] Frontend authenticatedFetch includes Bearer token
- [ ] ChatKit configuration points to correct backend endpoint
- [ ] Auto-refresh periodically fetches updated data
- [ ] One user cannot see another user's data
- [ ] Chatbot can successfully call MCP tools
- [ ] Tool responses appear in ChatKit conversation
- [ ] Real-time sync works between chatbot and dashboard

---

## Next Steps

1. **For a new project:** Copy the template from `assets/fastapi-backend-template/` and `assets/chatkit-nextjs-template/`
2. **For existing app:** Follow the "Integration Patterns" section and reference the architecture guides
3. **For advanced features:** Read the "Advanced Topics" section and extend as needed
4. **For troubleshooting:** Check "Common Issues & Solutions" and verify the checklist

