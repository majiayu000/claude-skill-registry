---
name: chatkit-ui-skill
description: Production-ready OpenAI ChatKit conversational UI skill for integrating AI chat interface into Todo app dashboard. Handles conversation state, message rendering, and backend communication.
---

# ChatKit UI Skill

Use this skill when implementing a conversational AI chat interface using OpenAI ChatKit in the Todo app.

## When to Use

- Building chat UI component for AI assistant
- Managing conversation state and message history
- Integrating chat interface with FastAPI backend
- Rendering user and AI messages
- Handling real-time chat interactions

## Core Responsibilities

### 1. Conversation Identity
- Generate unique `conversation_id` on first interaction
- Persist conversation ID across session
- Include conversation ID in every backend request
- Handle conversation resume after refresh

### 2. ChatKit Integration
```typescript
// components/chat/ChatWidget.tsx
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useEffect, useState } from 'react';

export function ChatWidget({ userId }: { userId: string }) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { control } = useChatKit({
    api: {
      async getClientSecret(existing) {
        if (existing) {
          // Refresh expired token
          const res = await fetch('/api/chatkit/refresh', {
            method: 'POST',
            body: JSON.stringify({ token: existing }),
            headers: { 'Content-Type': 'application/json' },
          });
          const { client_secret } = await res.json();
          return client_secret;
        }

        // Create new session
        const res = await fetch('/api/chatkit/session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        });
        const { client_secret } = await res.json();
        return client_secret;
      },
    },
    theme: {
      colorScheme: 'light',
      radius: 'round',
      color: {
        accent: { primary: '#8B5CF6', level: 2 },
      },
    },
    composer: {
      placeholder: 'Ask me to manage your tasks...',
    },
    startScreen: {
      greeting: 'How can I help with your tasks?',
      prompts: [
        {
          label: 'Add a new task',
          prompt: 'Add a task to buy groceries',
          icon: 'plus',
        },
        {
          label: 'Show my tasks',
          prompt: 'Show me all my tasks',
          icon: 'list',
        },
      ],
    },
    onReady: () => {
      console.log('ChatKit is ready');
    },
    onError: ({ error }) => {
      console.error('ChatKit error:', error);
      setError(error.message);
    },
    onResponseStart: () => {
      setIsLoading(true);
      setError(null);
    },
    onResponseEnd: () => {
      setIsLoading(false);
    },
    onThreadChange: ({ threadId }) => {
      console.log('Thread changed to:', threadId);
      // Store thread ID in localStorage or database
      localStorage.setItem('lastThreadId', threadId || '');
    },
    onClientTool: async (toolCall) => {
      // Handle client tool calls from the backend
      const { name, params } = toolCall;

      switch (name) {
        case 'task_created':
          console.log('Task created:', params);
          return { success: true };
        case 'task_updated':
          console.log('Task updated:', params);
          return { success: true };
        case 'task_deleted':
          console.log('Task deleted:', params);
          return { success: true };
        default:
          throw new Error(`Unhandled client tool: ${name}`);
      }
    },
  });

  return (
    <div className="chat-container">
      {isLoading && <div className="loading-indicator">AI is thinking...</div>}
      {error && <div className="error-banner">{error}</div>}
      <ChatKit control={control} className="h-[600px] w-[400px]" />
    </div>
  );
}
```

## Event Handling Patterns

### ChatKit Event Integration
```typescript
// components/chat/ChatWidget.tsx
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useEffect, useState } from 'react';

function ChatWithEventHandling({ userId }: { userId: string }) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { control, sendUserMessage, focusComposer, setThreadId } = useChatKit({
    api: {
      async getClientSecret() {
        const res = await fetch('/api/chatkit/session', { method: 'POST' });
        return (await res.json()).client_secret;
      },
    },
    onReady: () => {
      console.log('ChatKit is ready');
    },
    onError: ({ error }) => {
      console.error('ChatKit error:', error);
      setError(error.message);

      // Send to error tracking service
      fetch('/api/errors', {
        method: 'POST',
        body: JSON.stringify({
          error: error.message,
          stack: error.stack,
          timestamp: new Date().toISOString(),
        }),
        headers: { 'Content-Type': 'application/json' },
      });
    },
    onResponseStart: () => {
      setIsLoading(true);
      setError(null);
    },
    onResponseEnd: () => {
      setIsLoading(false);
    },
    onThreadChange: ({ threadId }) => {
      console.log('Thread changed to:', threadId);

      // Track in analytics
      fetch('/api/analytics/thread-change', {
        method: 'POST',
        body: JSON.stringify({ threadId }),
        headers: { 'Content-Type': 'application/json' },
      });
    },
    onThreadLoadStart: ({ threadId }) => {
      console.log('Loading thread:', threadId);
    },
    onThreadLoadEnd: ({ threadId }) => {
      console.log('Thread loaded:', threadId);
    },
    onLog: ({ name, data }) => {
      console.log('ChatKit log:', name, data);

      // Send to analytics
      if (name === 'message.send') {
        fetch('/api/analytics/message', {
          method: 'POST',
          body: JSON.stringify(data),
          headers: { 'Content-Type': 'application/json' },
        });
      }
    }
  });

  return (
    <div className="chat-container">
      {isLoading && <div className="loading-indicator">AI is thinking...</div>}
      {error && <div className="error-banner">{error}</div>}
      <ChatKit control={control} className="h-[600px] w-[400px]" />
    </div>
  );
}
```

## Client Tool Integration

### Handling Client Tools from Backend
```typescript
// components/chat/ChatWidget.tsx
const { control } = useChatKit({
  api: {
    async getClientSecret() {
      const res = await fetch('/api/chatkit/session', { method: 'POST' });
      return (await res.json()).client_secret;
    },
  },
  onClientTool: async (toolCall) => {
    const { name, params } = toolCall;

    switch (name) {
      case 'task_created':
        console.log('Task created:', params);
        // Update UI to reflect new task
        return { success: true };
      case 'task_updated':
        console.log('Task updated:', params);
        // Update UI to reflect task changes
        return { success: true };
      case 'task_deleted':
        console.log('Task deleted:', params);
        // Update UI to remove task
        return { success: true };
      case 'open_tab':
        window.open(params.url, '_blank', 'noopener');
        return { opened: true };
      default:
        throw new Error(`Unhandled client tool: ${name}`);
    }
  },
});
```

## Theming and Customization

### Custom Theme Configuration
```typescript
// components/chat/ChatWidget.tsx
const { control } = useChatKit({
  theme: {
    colorScheme: 'dark', // 'light' or 'dark'
    radius: 'round', // 'square', 'soft', or 'round'
    color: {
      accent: { primary: '#8B5CF6', level: 2 }, // Primary accent color
    },
  },
  header: {
    enabled: true,
    rightAction: {
      icon: 'light-mode',
      onClick: () => console.log('Toggle theme'),
    },
  },
  history: {
    enabled: true,
    showDelete: true,
    showRename: true,
  },
  startScreen: {
    greeting: 'How can I help with your tasks?',
    prompts: [
      {
        label: 'Add a new task',
        prompt: 'Add a task to buy groceries',
        icon: 'plus',
      },
      {
        label: 'Show my tasks',
        prompt: 'Show me all my tasks',
        icon: 'list',
      },
    ],
  },
  composer: {
    placeholder: 'Ask me to manage your tasks...',
  },
  threadItemActions: {
    feedback: true,
    retry: true,
  },
});
```

## Dashboard Integration

```tsx
// app/dashboard/page.tsx
import { ChatWidget } from "@/components/chat/ChatWidget";
import { TaskList } from "@/components/tasks/TaskList";

export default function Dashboard({ userId }: { userId: string }) {
  return (
    <div className="dashboard-layout">
      <aside className="task-panel">
        <TaskList userId={userId} />
      </aside>
      <aside className="chat-panel">
        <ChatWidget userId={userId} />
      </aside>
    </div>
  );
}
```

## FastAPI Backend Integration

### ChatKit Endpoint Handler
```python
# backend/app/api/routes/chat.py
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import StreamingResponse, Response
from chatkit.server import StreamingResult
from typing import AsyncIterator

app = FastAPI(title="ChatKit API")

@app.post("/chatkit")
async def chatkit_endpoint(
    request: Request,
    server = Depends(get_chatkit_server)
) -> Response:
    """
    Central endpoint that processes all ChatKit requests and returns streaming responses.
    Delegates request handling to the configured ChatKit server, which manages
    agent execution, tool invocation, and event streaming.
    """
    try:
        payload = await request.body()
        result = await server.process(payload, {"request": request})

        if isinstance(result, StreamingResult):
            return StreamingResponse(result, media_type="text/event-stream")
        if hasattr(result, "json"):
            return Response(content=result.json, media_type="application/json")
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Agent Response Handler
```python
# backend/app/agents/chat_agent.py
from chatkit.server import ChatKitServer
from chatkit.types import ThreadMetadata, UserMessageItem, ThreadStreamEvent
from chatkit.agents import AgentContext, stream_agent_response
from agents import Runner
from typing import AsyncIterator

class TodoAssistantServer(ChatKitServer[dict]):
    """
    Core method that converts user messages into agent inputs and streams back
    assistant responses. Handles thread state management, message history,
    and coordinates tool execution with the OpenAI Agents SDK.
    """
    async def respond(
        self,
        thread: ThreadMetadata,
        item: UserMessageItem | None,
        context: dict,
    ) -> AsyncIterator[ThreadStreamEvent]:
        agent_context = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        agent_input = await self._to_agent_input(thread, item)
        if agent_input is None:
            return

        result = Runner.run_streamed(
            self.assistant,
            agent_input,
            context=agent_context,
        )

        async for event in stream_agent_response(agent_context, result):
            yield event
```

### Agent Tool Definition
```python
# backend/app/tools/task_tools.py
from agents import function_tool, RunContextWrapper
from chatkit.agents import AgentContext, ClientToolCall

@function_tool(
    description_override="Create a new task for the user"
)
async def create_task(
    ctx: RunContextWrapper[AgentContext],
    title: str,
    description: str = "",
    priority: str = "normal"
) -> dict[str, str] | None:
    """
    Creates a new task in the database.
    """
    try:
        # Assuming task service is available via context
        task_service = ctx.context.request_context.get("task_service")
        new_task = await task_service.create_task(
            user_id=ctx.context.thread.metadata.get("user_id"),
            title=title,
            description=description,
            priority=priority
        )

        # Trigger client-side notification
        ctx.context.client_tool_call = ClientToolCall(
            name="task_created",
            arguments={
                "task_id": str(new_task.id),
                "title": new_task.title,
                "status": "created"
            },
        )

        return {
            "task_id": str(new_task.id),
            "status": "created",
            "message": f"Task '{new_task.title}' created successfully"
        }
    except Exception as e:
        print(f"Error creating task: {e}")
        return None
```

## Security Requirements

1. **Domain Allowlist**: Add production domain to OpenAI dashboard
   ```
   https://platform.openai.com/settings/organization/security/domain-allowlist
   ```

2. **Environment Variables**:
   ```bash
   # .env.local
   NEXT_PUBLIC_OPENAI_DOMAIN_KEY="your-domain-key"
   CHATKIT_API_KEY="your-chatkit-api-key"
   ```

3. **Backend Authentication**: Include JWT token in chat requests

## Responsiveness

```css
/* Mobile first approach */
.dashboard-layout {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (min-width: 768px) {
  .dashboard-layout {
    flex-direction: row;
  }

  .task-panel {
    flex: 2;
  }

  .chat-panel {
    flex: 1;
    max-width: 400px;
  }
}
```

## Best Practices

1. **Single Conversation ID**: Never regenerate during active session
2. **Optimistic Updates**: Show user message immediately
3. **Loading States**: Disable input while AI is responding
4. **Auto Scroll**: Keep latest message visible
5. **Error Recovery**: Clear, actionable error messages
6. **Persist State**: Store conversation ID in localStorage (optional)
7. **Clean Teardown**: Clear chat state on logout
8. **Client Tool Integration**: Handle tool callbacks from backend properly
9. **Event Monitoring**: Track important events for analytics and debugging
10. **Streaming Responses**: Leverage ChatKit's streaming capabilities for better UX

## Example Commands User Can Type

| User Input | Expected Behavior |
|------------|-------------------|
| "Add a task to buy groceries" | Create task via MCP tool |
| "Show me all my tasks" | List all tasks |
| "Mark task 3 as complete" | Complete specific task |
| "Delete the meeting task" | Delete task by title |
| "What's pending?" | Filter pending tasks |

## Backend Integration

Chat widget expects these endpoints:
```
POST /chatkit - Main ChatKit endpoint for all chat interactions
POST /api/chatkit/session - Create new ChatKit session
POST /api/chatkit/refresh - Refresh ChatKit session
```

Backend handles:
- OpenAI Agents SDK execution
- MCP tool invocation
- Conversation state persistence
- Message history storage
- Client tool callbacks
- Streaming responses to UI

---

**Production Standard**: This skill ensures a stable, secure, and user-friendly chat interface that acts as the communication layer between users and AI agents.
