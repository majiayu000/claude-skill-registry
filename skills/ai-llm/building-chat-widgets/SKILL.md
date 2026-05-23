---
name: building-chat-widgets
description: Build interactive AI chat widgets with buttons, forms, and bidirectional actions. Use when creating agentic UIs with clickable widgets, entity tagging (@mentions), composer tools, or server-handled widget actions. Covers full widget lifecycle. NOT when building simple text-only chat without interactive elements.
---

# Building Chat Widgets

Create interactive widgets for AI chat with actions and entity tagging.

## Quick Start

```typescript
const chatkit = useChatKit({
  api: { url: API_URL, domainKey: DOMAIN_KEY },

  widgets: {
    onAction: async (action, widgetItem) => {
      if (action.type === "view_details") {
        navigate(`/details/${action.payload.id}`);
      }
    },
  },
});
```

---

## Action Handler Types

| Handler | Defined In | Processed By | Use Case |
|---------|------------|--------------|----------|
| `"client"` | Widget template | Frontend `onAction` | Navigation, local state |
| `"server"` | Widget template | Backend `action()` | Data mutation, widget replacement |

---

## Widget Lifecycle

```
1. Agent tool generates widget → yield WidgetItem
2. Widget renders in chat with action buttons
3. User clicks action → action dispatched
4. Handler processes action:
   - client: onAction callback in frontend
   - server: action() method in ChatKitServer
5. Optional: Widget replaced with updated state
```

---

## Core Patterns

### 1. Widget Templates

Define reusable widget layouts with dynamic data:

```json
{
  "type": "ListView",
  "children": [
    {
      "type": "ListViewItem",
      "key": "item-1",
      "onClickAction": {
        "type": "item.select",
        "handler": "client",
        "payload": { "itemId": "item-1" }
      },
      "children": [
        {
          "type": "Row",
          "gap": 3,
          "children": [
            { "type": "Icon", "name": "check", "color": "success" },
            { "type": "Text", "value": "Item title", "weight": "semibold" }
          ]
        }
      ]
    }
  ]
}
```

### 2. Client-Handled Actions

Actions that update local state, navigate, or send follow-up messages:

**Widget Definition:**

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

**Frontend Handler:**

```typescript
const chatkit = useChatKit({
  api: { url: API_URL, domainKey: DOMAIN_KEY },

  widgets: {
    onAction: async (action, widgetItem) => {
      switch (action.type) {
        case "open_article":
          navigate(`/article/${action.payload?.id}`);
          break;

        case "more_suggestions":
          await chatkit.sendUserMessage({ text: "More suggestions, please" });
          break;

        case "select_option":
          setSelectedOption(action.payload?.optionId);
          break;
      }
    },
  },
});
```

### 3. Server-Handled Actions

Actions that mutate data, update widgets, or require backend processing:

**Widget Definition:**

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

**Backend Handler:**

```python
from chatkit.types import (
    Action, WidgetItem, ThreadItemReplacedEvent,
    ThreadItemDoneEvent, AssistantMessageItem, ClientEffectEvent,
)

class MyServer(ChatKitServer[dict]):

    async def action(
        self,
        thread: ThreadMetadata,
        action: Action[str, Any],
        sender: WidgetItem | None,
        context: RequestContext,  # Note: Already RequestContext, not dict
    ) -> AsyncIterator[ThreadStreamEvent]:

        if action.type == "line.select":
            line_id = action.payload["id"]  # Use .payload, not .arguments

            # 1. Update widget with selection
            updated_widget = build_selector_widget(selected=line_id)
            yield ThreadItemReplacedEvent(
                item=sender.model_copy(update={"widget": updated_widget})
            )

            # 2. Stream assistant message
            yield ThreadItemDoneEvent(
                item=AssistantMessageItem(
                    id=self.store.generate_item_id("msg", thread, context),
                    thread_id=thread.id,
                    created_at=datetime.now(),
                    content=[{"text": f"Selected {line_id}"}],
                )
            )

            # 3. Trigger client effect
            yield ClientEffectEvent(
                name="selection_changed",
                data={"lineId": line_id},
            )
```

### 4. Entity Tagging (@mentions)

Allow users to @mention entities in messages:

```typescript
const chatkit = useChatKit({
  api: { url: API_URL, domainKey: DOMAIN_KEY },

  entities: {
    onTagSearch: async (query: string): Promise<Entity[]> => {
      const results = await fetch(`/api/search?q=${query}`).then(r => r.json());

      return results.map((item) => ({
        id: item.id,
        title: item.name,
        icon: item.type === "person" ? "profile" : "document",
        group: item.type === "People" ? "People" : "Articles",
        interactive: true,
        data: { type: item.type, article_id: item.id },
      }));
    },

    onClick: (entity: Entity) => {
      if (entity.data?.article_id) {
        navigate(`/article/${entity.data.article_id}`);
      }
    },
  },
});
```

### 5. Composer Tools (Mode Selection)

Let users select different AI modes from the composer:

```typescript
const TOOL_CHOICES = [
  {
    id: "general",
    label: "Chat",
    icon: "sparkle",
    placeholderOverride: "Ask anything...",
    pinned: true,
  },
  {
    id: "event_finder",
    label: "Find Events",
    icon: "calendar",
    placeholderOverride: "What events are you looking for?",
    pinned: true,
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

**Backend Routing:**

```python
async def respond(self, thread, item, context):
    tool_choice = context.metadata.get("tool_choice")

    if tool_choice == "event_finder":
        agent = self.event_finder_agent
    else:
        agent = self.general_agent

    result = Runner.run_streamed(agent, input_items)
    async for event in stream_agent_response(context, result):
        yield event
```

---

## Widget Component Reference

### Layout Components

| Component | Props | Description |
|-----------|-------|-------------|
| `ListView` | `children` | Scrollable list container |
| `ListViewItem` | `key`, `onClickAction`, `children` | Clickable list item |
| `Row` | `gap`, `align`, `justify`, `children` | Horizontal flex |
| `Col` | `gap`, `padding`, `children` | Vertical flex |
| `Box` | `size`, `radius`, `background`, `padding` | Styled container |

### Content Components

| Component | Props | Description |
|-----------|-------|-------------|
| `Text` | `value`, `size`, `weight`, `color` | Text display |
| `Title` | `value`, `size`, `weight` | Heading text |
| `Image` | `src`, `alt`, `width`, `height` | Image display |
| `Icon` | `name`, `size`, `color` | Icon from set |

### Interactive Components

| Component | Props | Description |
|-----------|-------|-------------|
| `Button` | `label`, `variant`, `onClickAction` | Clickable button |

---

## Critical Implementation Details

### Action Object Structure

**IMPORTANT**: Use `action.payload`, NOT `action.arguments`:

```python
# WRONG - Will cause AttributeError
action.arguments

# CORRECT
action.payload
```

### Context Parameter

The `context` parameter is `RequestContext`, not `dict`:

```python
# WRONG - Tries to wrap RequestContext
request_context = RequestContext(metadata=context)

# CORRECT - Use directly
user_id = context.user_id
```

### UserMessageItem Required Fields

When creating synthetic user messages:

```python
from chatkit.types import UserMessageItem, UserMessageTextContent

# Include ALL required fields
synthetic_message = UserMessageItem(
    id=self.store.generate_item_id("message", thread, context),
    thread_id=thread.id,
    created_at=datetime.now(),
    content=[UserMessageTextContent(type="input_text", text=message_text)],
    inference_options={},
)
```

---

## Anti-Patterns

1. **Mixing handlers** - Don't handle same action in both client and server
2. **Missing payload** - Always include data in action payload
3. **Using action.arguments** - Use `action.payload`
4. **Wrapping RequestContext** - Context is already RequestContext
5. **Missing UserMessageItem fields** - Include id, thread_id, created_at
6. **Wrong content type** - Use `type="input_text"` for user messages

---

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ building-chat-widgets skill ready`

## If Verification Fails

1. Check: references/ folder has widget-patterns.md
2. **Stop and report** if still failing

## References

- [references/widget-patterns.md](references/widget-patterns.md) - Complete widget patterns
- [references/server-action-handler.md](references/server-action-handler.md) - Backend action handling
