---
name: chatkit-actions
description: Implements interactive widget actions and bidirectional communication patterns for ChatKit. This skill should be used when building AI-driven interactive UIs with buttons, forms, entity tagging (@mentions), composer tools, and server-handled widget actions. Covers the full widget lifecycle from creation to replacement.
---

# ChatKit Actions Skill

## Overview

This skill unlocks the full power of ChatKit's agentic UI capabilities - where AI can render interactive widgets, users can click buttons that trigger both client and server actions, and the conversation becomes a two-way interactive experience.

## Core Concepts

### Action Handler Types

Widgets can specify where actions are handled:

| Handler | Defined In | Processed By | Use Case |
|---------|------------|--------------|----------|
| `"client"` | Widget template | Frontend `onAction` | Navigation, local state, send follow-up |
| `"server"` | Widget template | Backend `action()` method | Data mutation, widget replacement |

### Widget Lifecycle

```
1. Agent tool generates widget → yield WidgetItem
2. Widget renders in chat with action buttons
3. User clicks action → action dispatched
4. Handler processes action:
   - client: onAction callback in frontend
   - server: action() method in ChatKitServer
5. Optional: Widget replaced with updated state
```

## Implementation Patterns

### Pattern 1: Widget Templates (.widget files)

**When**: Define reusable widget layouts with dynamic data

**Widget Template Format**:
```json
{
  "version": "1.0",
  "name": "task_list",
  "template": "{\"type\":\"ListView\",\"children\":[...jinja template...]}",
  "jsonSchema": {
    "type": "object",
    "properties": {
      "tasks": { "type": "array", "items": {...} }
    }
  }
}
```

**Widget Components Available**:
- Layout: `ListView`, `ListViewItem`, `Row`, `Col`, `Box`
- Content: `Text`, `Title`, `Image`, `Icon`
- Interactive: `Button` (with `onClickAction`)
- Styling: `gap`, `padding`, `background`, `border`, `radius`

**Example - Task List Widget**:
```json
{
  "type": "ListView",
  "children": [
    {
      "type": "ListViewItem",
      "key": "task-1",
      "onClickAction": {
        "type": "task.select",
        "handler": "client",
        "payload": { "taskId": "task-1" }
      },
      "children": [
        {
          "type": "Row",
          "gap": 3,
          "children": [
            { "type": "Icon", "name": "check", "color": "success" },
            { "type": "Text", "value": "Complete review", "weight": "semibold" }
          ]
        }
      ]
    }
  ]
}
```

**Python - Loading Templates**:
```python
from chatkit.widgets import WidgetTemplate, WidgetRoot

# Load template from file
task_list_template = WidgetTemplate.from_file("task_list.widget")

def build_task_list_widget(tasks: list[Task]) -> WidgetRoot:
    return task_list_template.build(
        data={
            "tasks": [task.model_dump() for task in tasks],
            "selected": None,
        }
    )
```

**Evidence**: `cat-lounge/backend/app/widgets/cat_name_suggestions.widget`

### Pattern 2: Client-Handled Actions

**When**: Actions that update local state, navigate, or send follow-up messages

**Widget Definition (handler: "client")**:
```json
{
  "type": "Button",
  "label": "View Article",
  "onClickAction": {
    "type": "open_article",
    "handler": "client",
    "payload": { "id": "article-123" }
  }
}
```

**Frontend Handler**:
```typescript
import { useChatKit, type Widgets } from "@openai/chatkit-react";

const chatkit = useChatKit({
  api: { url: API_URL, domainKey: DOMAIN_KEY },

  widgets: {
    onAction: async (
      action: { type: string; payload?: Record<string, unknown> },
      widgetItem: { id: string; widget: Widgets.Card | Widgets.ListView }
    ) => {
      switch (action.type) {
        case "open_article":
          // Navigate to article
          navigate(`/article/${action.payload?.id}`);
          break;

        case "more_suggestions":
          // Send follow-up message
          await chatkit.sendUserMessage({ text: "More suggestions, please" });
          break;

        case "select_option":
          // Update local state
          setSelectedOption(action.payload?.optionId);
          break;
      }
    },
  },
});
```

**Evidence**: `news-guide/frontend/src/components/ChatKitPanel.tsx:55-79`

### Pattern 3: Server-Handled Actions

**When**: Actions that mutate data, update widgets, or require backend processing

**Widget Definition (handler: "server")**:
```json
{
  "type": "ListViewItem",
  "onClickAction": {
    "type": "line.select",
    "handler": "server",
    "payload": { "id": "blue-line" }
  }
}
```

**Backend Handler**:
```python
from chatkit.server import ChatKitServer
from chatkit.types import (
    Action,
    WidgetItem,
    ThreadItemReplacedEvent,
    ThreadItemDoneEvent,
    AssistantMessageItem,
    HiddenContextItem,
    ClientEffectEvent,
)

class MyServer(ChatKitServer[dict]):

    async def action(
        self,
        thread: ThreadMetadata,
        action: Action[str, Any],
        sender: WidgetItem | None,
        context: dict[str, Any],
    ) -> AsyncIterator[ThreadStreamEvent]:

        if action.type == "line.select":
            line_id = action.payload["id"]

            # 1. Update widget with selection
            updated_widget = build_line_selector_widget(
                lines=self.lines,
                selected=line_id,
            )
            yield ThreadItemReplacedEvent(
                item=sender.model_copy(update={"widget": updated_widget})
            )

            # 2. Add hidden context for future agent input
            await self.store.add_thread_item(
                thread.id,
                HiddenContextItem(
                    id=self.store.generate_item_id("ctx", thread, context),
                    thread_id=thread.id,
                    created_at=datetime.now(),
                    content=f"<LINE_SELECTED>{line_id}</LINE_SELECTED>",
                ),
                context=context,
            )

            # 3. Stream assistant message
            yield ThreadItemDoneEvent(
                item=AssistantMessageItem(
                    id=self.store.generate_item_id("msg", thread, context),
                    thread_id=thread.id,
                    created_at=datetime.now(),
                    content=[{"text": f"Selected {line_id}. Where to add station?"}],
                )
            )

            # 4. Trigger client effect
            yield ClientEffectEvent(
                name="location_select_mode",
                data={"lineId": line_id},
            )
```

**Evidence**: `metro-map/backend/app/server.py`

### Pattern 4: Client-to-Server Action Forwarding

**When**: Client handles action locally, then notifies server for persistence/widget update

**Frontend - Send Custom Action**:
```typescript
widgets: {
  onAction: async (action, widgetItem) => {
    if (action.type === "select_name") {
      // 1. Forward to server for processing
      await chatkit.sendCustomAction(action, widgetItem.id);

      // 2. Optionally refresh local state after server processes
      const data = await refreshCatStatus();
      if (data) {
        handleStatusUpdate(data, `Now called ${data.name}`);
      }
    }
  },
}
```

**Evidence**: `cat-lounge/frontend/src/components/ChatKitPanel.tsx:68-80`

### Pattern 5: Entity Tagging (@mentions)

**When**: Allow users to @mention entities (users, articles, tasks) in messages

**Frontend - Entity Configuration**:
```typescript
import { useChatKit, type Entity } from "@openai/chatkit-react";

const chatkit = useChatKit({
  api: { url: API_URL, domainKey: DOMAIN_KEY },

  entities: {
    // Search for entities as user types @...
    onTagSearch: async (query: string): Promise<Entity[]> => {
      const results = await fetch(`/api/search?q=${query}`).then(r => r.json());

      return results.map((item) => ({
        id: item.id,
        title: item.name,
        icon: item.type === "person" ? "profile" : "document",
        group: item.type === "People" ? "People" : "Articles",
        interactive: true,
        data: {
          type: item.type,
          article_id: item.id,
        },
      }));
    },

    // Handle entity click (e.g., navigate)
    onClick: (entity: Entity) => {
      if (entity.data?.article_id) {
        navigate(`/article/${entity.data.article_id}`);
      }
    },

    // Render entity preview on hover
    onRequestPreview: async (entity: Entity) => {
      const details = await fetch(`/api/entity/${entity.id}`).then(r => r.json());

      return {
        preview: {
          type: "Card",
          children: [
            { type: "Text", value: entity.title, weight: "bold" },
            { type: "Text", value: details.description, color: "tertiary" },
          ],
        },
      };
    },
  },
});
```

**Backend - Converting Entity Tags**:
```python
# thread_item_converter.py
class EntityAwareConverter(BasicThreadItemConverter):
    """Convert entity tags to model-readable markers."""

    async def to_agent_input(self, items: list[ThreadItem]) -> list:
        result = []
        for item in items:
            if isinstance(item, UserMessageItem):
                content = item.content
                # Convert entity tags to XML markers
                for entity in item.entities or []:
                    if entity.type == "article":
                        content = content.replace(
                            f"@{entity.title}",
                            f"<ARTICLE_REFERENCE id='{entity.id}'>{entity.title}</ARTICLE_REFERENCE>"
                        )
                result.append({"role": "user", "content": content})
        return result
```

**Evidence**:
- `news-guide/frontend/src/components/ChatKitPanel.tsx:122-126`
- `news-guide/backend/app/thread_item_converter.py`
- `metro-map/frontend/src/components/ChatKitPanel.tsx:73-117`

### Pattern 6: Composer Tools (Mode Selection)

**When**: Let users select different AI modes/tools from the composer

**Frontend - Tool Configuration**:
```typescript
const TOOL_CHOICES = [
  {
    id: "general",
    label: "Chat",
    shortLabel: "Chat",
    icon: "sparkle",
    placeholderOverride: "Ask anything...",
    pinned: true,
  },
  {
    id: "event_finder",
    label: "Find Events",
    shortLabel: "Events",
    icon: "calendar",
    placeholderOverride: "What events are you looking for?",
    pinned: true,
  },
  {
    id: "puzzle",
    label: "Word Puzzle",
    shortLabel: "Puzzle",
    icon: "bolt",
    placeholderOverride: "Ready for today's puzzle?",
    pinned: false,
  },
];

const chatkit = useChatKit({
  api: { url: API_URL, domainKey: DOMAIN_KEY },
  composer: {
    placeholder: "What would you like to do?",
    tools: TOOL_CHOICES,
  },
});
```

**Backend - Routing by Tool Choice**:
```python
# server.py
async def respond(self, thread, item, context):
    tool_choice = context.get("tool_choice")

    if tool_choice == "event_finder":
        agent = self.event_finder_agent
    elif tool_choice == "puzzle":
        agent = self.puzzle_agent
    else:
        agent = self.general_agent

    # Run selected agent
    result = Runner.run_streamed(agent, input_items, context=agent_context)
    async for event in stream_agent_response(agent_context, result):
        yield event
```

**Evidence**: `news-guide/frontend/src/lib/config.ts`

### Pattern 7: Thread Item Actions (Feedback/Retry/Share)

**When**: Enable built-in actions on AI messages

**Frontend Configuration**:
```typescript
const chatkit = useChatKit({
  api: { url: API_URL, domainKey: DOMAIN_KEY },

  threadItemActions: {
    feedback: true,   // Thumbs up/down
    retry: true,      // Regenerate response
    share: true,      // Share message
  },

  onLog: ({ name, data }) => {
    if (name === "message.feedback") {
      // Track feedback analytics
      fetch("/api/analytics/feedback", {
        method: "POST",
        body: JSON.stringify(data),
      });
    }
    if (name === "message.share") {
      // Track share events
      fetch("/api/analytics/share", {
        method: "POST",
        body: JSON.stringify(data),
      });
    }
  },
});
```

### Pattern 8: Widget Streaming from Tools

**When**: Agent tool generates a widget as part of response

**Backend - Tool with Widget Output**:
```python
from chatkit.types import WidgetItem
from agents import function_tool

@function_tool
async def show_article_list(ctx: AgentContext, query: str) -> str:
    """Show a list of articles matching the query."""

    articles = await article_store.search(query)

    # Build widget
    widget = build_article_list_widget(articles)

    # Yield widget item
    widget_item = WidgetItem(
        id=ctx.store.generate_item_id("widget", ctx.thread, ctx.request_context),
        thread_id=ctx.thread.id,
        created_at=datetime.now(),
        widget=widget,
    )

    # Save to store
    await ctx.store.add_thread_item(ctx.thread.id, widget_item, ctx.request_context)

    # Yield as event
    yield ThreadItemDoneEvent(item=widget_item)

    return f"Showing {len(articles)} articles"
```

**Evidence**: `news-guide/backend/app/agents/news_agent.py`

## Widget Component Reference

### Layout Components

| Component | Props | Description |
|-----------|-------|-------------|
| `ListView` | `children` | Scrollable list container |
| `ListViewItem` | `key`, `onClickAction`, `children` | Clickable list item |
| `Row` | `gap`, `align`, `justify`, `children` | Horizontal flex |
| `Col` | `gap`, `align`, `justify`, `flex`, `padding`, `children` | Vertical flex |
| `Box` | `size`, `radius`, `background`, `border`, `padding` | Container with styling |

### Content Components

| Component | Props | Description |
|-----------|-------|-------------|
| `Text` | `value`, `size`, `weight`, `color`, `maxLines` | Text display |
| `Title` | `value`, `size`, `weight` | Heading text |
| `Image` | `src`, `alt`, `width`, `height`, `fit`, `radius` | Image display |
| `Icon` | `name`, `size`, `color` | Icon from icon set |

### Interactive Components

| Component | Props | Description |
|-----------|-------|-------------|
| `Button` | `label`, `variant`, `color`, `size`, `pill`, `block`, `iconStart`, `iconEnd`, `onClickAction`, `disabled` | Clickable button |

### Action Structure

```typescript
interface Action {
  type: string;           // Action identifier
  handler: "client" | "server";
  payload?: Record<string, unknown>;
}
```

## Common Patterns Summary

| Pattern | Frontend | Backend | Use Case |
|---------|----------|---------|----------|
| Navigation | `onAction` → navigate | - | Open details page |
| Follow-up | `onAction` → sendUserMessage | - | "More suggestions" |
| Selection | `sendCustomAction` | `action()` → `ThreadItemReplacedEvent` | Select from list |
| Data mutation | `sendCustomAction` | `action()` → update DB | Approve/reject |
| @mentions | `entities.onTagSearch` | `ThreadItemConverter` | Reference entities |
| Mode switch | `composer.tools` | Route by tool_choice | Different agents |

## Critical Implementation Details

### Action Object Structure

**IMPORTANT**: The `Action` object uses `payload`, NOT `arguments`:

```python
# ❌ WRONG - Will cause AttributeError
action.arguments  # 'Action' object has no attribute 'arguments'

# ✅ CORRECT
action.payload    # Access action data via .payload
```

**Action Type Definition**:
```python
from chatkit.types import Action

# Action[str, Any] has these fields:
action.type      # str - action identifier (e.g., "task.start")
action.payload   # dict[str, Any] - action data
action.handler   # "client" | "server" - where action is processed
```

### Server Action Handler Signature

**CRITICAL**: The `context` parameter is `RequestContext`, NOT `dict[str, Any]`

```python
# Type annotation vs runtime reality mismatch
async def action(
    self,
    thread: ThreadMetadata,
    action: Action[str, Any],
    sender: WidgetItem | None,
    context: dict[str, Any],  # ⚠️ Type hint says dict, but runtime is RequestContext!
) -> AsyncIterator[ThreadStreamEvent]:

    # ❌ WRONG - Tries to wrap RequestContext inside RequestContext
    request_context = RequestContext(metadata=context)

    # ✅ CORRECT - Use context directly, it's already RequestContext
    user_id = context.user_id
    metadata = context.metadata
```

**Why this happens**: ChatKit SDK passes `RequestContext` object at runtime, despite type annotations suggesting `dict`. Always use `context` directly without wrapping.

### UserMessageItem Required Fields

When creating synthetic user messages from actions, **ALL** these fields are required:

```python
from chatkit.types import UserMessageItem, UserMessageTextContent
from datetime import datetime

# ❌ WRONG - Missing required fields causes ValidationError
synthetic_message = UserMessageItem(
    content=[UserMessageTextContent(type="text", text=message_text)]
)

# ✅ CORRECT - Include all required fields
synthetic_message = UserMessageItem(
    id=self.store.generate_item_id("message", thread, context),
    thread_id=thread.id,
    created_at=datetime.now(),
    content=[UserMessageTextContent(type="input_text", text=message_text)],
    inference_options={},
)
```

**Required fields**:
- `id`: Generate via `store.generate_item_id("message", thread, context)`
- `thread_id`: From `thread.id` parameter
- `created_at`: Current timestamp via `datetime.now()`
- `content`: List of content blocks (UserMessageTextContent)
- `inference_options`: Empty dict `{}` if no special options

**UserMessageTextContent type values**:
- ✅ `type="input_text"` - User text input (correct)
- ❌ `type="text"` - Invalid for UserMessageTextContent (causes ValidationError)

### Local Tool Wrappers for Widget Streaming

**Problem**: Agent calls MCP tool successfully, but widget doesn't appear in UI.

**Root Cause**: Widgets stream via `RunHooks` pattern. MCP tools alone don't trigger widget rendering - you need **local tool wrappers**.

**Solution Pattern**:

```python
# 1. Create local tool wrapper
from agents import function_tool

@function_tool
async def show_task_form(
    ctx: RunContextWrapper[TaskFlowAgentContext],
) -> str:
    """Show interactive task creation form widget."""

    agent_ctx = ctx.context
    mcp_url = agent_ctx.mcp_server_url

    # Call MCP tool via HTTP
    result = await _call_mcp_tool(
        mcp_url,
        "taskflow_show_task_form",
        arguments={"params": {"user_id": agent_ctx.user_id}},
        access_token=agent_ctx.access_token,
    )

    # Return result - RunHooks will intercept and stream widget
    return json.dumps(result)

# 2. Register local wrapper with agent
agent = Agent(
    name="TaskFlow Assistant",
    tools=[
        show_task_form,  # Local wrapper - triggers RunHooks
        # ... other local wrappers
    ],
)

# 3. In RunHooks.on_tool_end() - Stream widget
async def on_tool_end(self, output: str | None, tool_name: str) -> None:
    if tool_name == "show_task_form":
        result = json.loads(output)
        if result.get("action") == "show_form":
            widget = build_task_form_widget()
            yield WidgetItem(...)
```

**Key insight**: Direct MCP tools → no widgets. Local wrappers → RunHooks → widgets streamed.

## Common Pydantic Validation Errors

### Error 1: 'Action' object has no attribute 'arguments'

```
AttributeError: 'Action[str, Any]' object has no attribute 'arguments'
```

**Fix**: Use `action.payload` instead of `action.arguments`

### Error 2: UserMessageTextContent type mismatch

```
ValidationError: Input should be 'input_text' [type=literal_error, input_value='text']
```

**Fix**: Use `type="input_text"` for user input, not `type="text"`

### Error 3: UserMessageItem missing required fields

```
4 validation errors for UserMessageItem
- id: Field required
- thread_id: Field required
- created_at: Field required
- inference_options: Field required
```

**Fix**: Include all required fields when creating UserMessageItem (see pattern above)

### Error 4: RequestContext wrapping issue

```
2 validation errors for RequestContext
user_id: Field required
metadata: Input should be a valid dictionary [input_value=RequestContext(...)]
```

**Fix**: Don't wrap `context` - it's already a RequestContext object

## Widget Action Testing Checklist

Before claiming widget actions are complete, test:

- [ ] Widget renders with correct data
- [ ] All buttons have clear labels (not just icons)
- [ ] Client actions navigate/update UI correctly
- [ ] Server actions call backend successfully
- [ ] Action payload contains all required data
- [ ] Widget updates after server action completes
- [ ] No AttributeError on action.payload access
- [ ] No ValidationError on UserMessageItem creation
- [ ] Local tool wrappers trigger widget streaming
- [ ] All status transitions have appropriate buttons
- [ ] Test with real user session (not mock data)
- [ ] Check browser console for errors
- [ ] Verify backend logs show action processing
- [ ] Test error cases (network failure, invalid data)

## Anti-Patterns to Avoid

1. **Mixing handlers** - Don't handle same action in both client and server
2. **Missing payload** - Always include necessary data in action payload
3. **Forgetting widget ID** - `sendCustomAction` requires widget ID for updates
4. **Not updating widget** - Server actions should yield `ThreadItemReplacedEvent`
5. **Blocking in onAction** - Keep client handlers fast, offload to server
6. **Using action.arguments** - Use `action.payload` (arguments doesn't exist)
7. **Wrapping RequestContext** - Context is already RequestContext, don't wrap it
8. **Missing UserMessageItem fields** - Include id, thread_id, created_at, inference_options
9. **Wrong content type** - Use `type="input_text"` for user messages
10. **No local tool wrappers** - MCP tools alone don't stream widgets
11. **Not testing thoroughly** - Test all actions with real data before claiming done
12. **Assuming type hints are correct** - ChatKit has type annotation vs runtime mismatches

## References

### Documentation
- `references/widget-templates.md` - Widget template syntax
- `references/client-vs-server-actions.md` - Action routing guide
- `references/entity-tagging.md` - @mention implementation
- `references/composer-tools.md` - Tool choice patterns
- `references/server-action-handler.py` - Complete backend action handler pattern

### Widget Template Assets
- `assets/line-select.widget` - Server action selection list (metro-map pattern)
- `assets/name-suggestions.widget` - Client action with "more" button (cat-lounge pattern)
- `assets/article-list.widget` - Rich card layout with images (news-guide pattern)

## Evidence Sources

All patterns derived from OpenAI ChatKit advanced samples:
- `blueprints/openai-chatkit-advanced-samples-main/examples/cat-lounge/`
- `blueprints/openai-chatkit-advanced-samples-main/examples/metro-map/`
- `blueprints/openai-chatkit-advanced-samples-main/examples/news-guide/`
